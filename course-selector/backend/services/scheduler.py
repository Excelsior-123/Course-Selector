def time_to_minutes(time_str):
    """Convert HH:MM to minutes since midnight"""
    hours, minutes = map(int, time_str.split(':'))
    return hours * 60 + minutes

def has_conflict(course1, course2):
    """Check if two courses have time conflicts"""
    for slot1 in course1["schedule"]:
        for slot2 in course2["schedule"]:
            if slot1["day"] != slot2["day"]:
                continue
            
            start1 = time_to_minutes(slot1["startTime"])
            end1 = time_to_minutes(slot1["endTime"])
            start2 = time_to_minutes(slot2["startTime"])
            end2 = time_to_minutes(slot2["endTime"])
            
            # Check overlap
            if start1 < end2 and start2 < end1:
                return True
    return False

def has_any_conflict(selected_courses, new_course):
    """Check if new course conflicts with any selected course"""
    for c in selected_courses:
        if has_conflict(c, new_course):
            return True
    return False

def calculate_workload(selected_courses):
    return sum(c["workload"] for c in selected_courses)

def calculate_average_rating(selected_courses):
    if not selected_courses:
        return 0
    return sum(c["rating"] for c in selected_courses) / len(selected_courses)

def calculate_average_difficulty(selected_courses):
    if not selected_courses:
        return 0
    return sum(c["difficulty"] for c in selected_courses) / len(selected_courses)

def calculate_total_credits(selected_courses):
    """Calculate total credits of selected courses"""
    return sum(c.get("credits", 0) for c in selected_courses)

def calculate_course_count(selected_courses):
    """Calculate number of selected courses"""
    return len(selected_courses)

def is_evening_course(course):
    """Check if a course has evening sessions (after 18:00)"""
    for slot in course.get("schedule", []):
        start_hour = int(slot["startTime"].split(":")[0])
        if start_hour >= 18:
            return True
    return False

def matches_hard_constraints(course, preferences):
    """
    Check if a course matches hard constraints (time, evening avoidance).
    Returns False if course violates any hard constraint.
    """
    time_constraints = preferences.get("timeConstraints", {})
    
    # Check evening avoidance - STRICT
    if time_constraints.get("avoidEvening", False):
        if is_evening_course(course):
            return False
    
    # Check preferred days
    preferred_days = time_constraints.get("preferredDays", [])
    if preferred_days:
        for slot in course.get("schedule", []):
            if slot["day"] not in preferred_days:
                return False
    
    # Check avoid days
    avoid_days = time_constraints.get("avoidDays", [])
    if avoid_days:
        for slot in course.get("schedule", []):
            if slot["day"] in avoid_days:
                return False
    
    # Check preferred time ranges
    preferred_ranges = time_constraints.get("preferredTimeRanges", [])
    if preferred_ranges:
        all_slots_in_range = True
        for slot in course.get("schedule", []):
            slot_in_range = False
            start_mins = time_to_minutes(slot["startTime"])
            end_mins = time_to_minutes(slot["endTime"])
            
            for range_spec in preferred_ranges:
                range_start = time_to_minutes(range_spec["start"])
                range_end = time_to_minutes(range_spec["end"])
                
                if start_mins >= range_start and end_mins <= range_end:
                    slot_in_range = True
                    break
            
            if not slot_in_range:
                all_slots_in_range = False
                break
        
        if not all_slots_in_range:
            return False
    
    return True

def check_final_constraints(selected_courses, preferences):
    """
    Final check to ensure all hard constraints are satisfied.
    Returns (is_valid, reason)
    """
    # Check exact courses - MOST IMPORTANT
    exact_courses = preferences.get("exactCourses")
    if exact_courses is not None:
        count = calculate_course_count(selected_courses)
        if count != exact_courses:
            return False, f"课程数量不符：已选{count}门，要求恰好{exact_courses}门"
    
    # Check min courses
    min_courses = preferences.get("minCourses")
    if min_courses is not None:
        count = calculate_course_count(selected_courses)
        if count < min_courses:
            return False, f"课程数不足：已选{count}门，要求至少{min_courses}门"
    
    # Check max courses - STRICT
    max_courses = preferences.get("maxCourses") or 8  # Handle None
    count = calculate_course_count(selected_courses)
    if max_courses and count > max_courses:
        return False, f"课程数超限：已选{count}门，上限{max_courses}门"
    
    # Check exact credits
    exact_credits = preferences.get("exactCredits")
    if exact_credits is not None:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits != exact_credits:
            return False, f"学分不匹配：已选{total_credits}学分，要求恰好{exact_credits}学分"
    
    # Check min credits
    min_credits = preferences.get("minCredits")
    if min_credits is not None:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits < min_credits:
            return False, f"学分不足：已选{total_credits}学分，要求至少{min_credits}学分"
    
    # Check max credits
    max_credits = preferences.get("maxCredits")
    if max_credits is not None:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits > max_credits:
            return False, f"学分超限：已选{total_credits}学分，上限{max_credits}学分"
    
    # Check evening avoidance - STRICT
    avoid_evening = preferences.get("timeConstraints", {}).get("avoidEvening", False)
    if avoid_evening:
        for course in selected_courses:
            if is_evening_course(course):
                return False, f"违反晚课限制：{course['name']}包含晚间时段"
    
    return True, "满足所有硬性约束"

def calculate_score(selected_courses, preferences=None):
    """Calculate a score for the schedule based on preferences"""
    if preferences is None:
        preferences = {}
    
    score = 0
    
    # Rating score (0-50)
    avg_rating = calculate_average_rating(selected_courses)
    score += avg_rating * 10
    
    # Difficulty preference
    avg_difficulty = calculate_average_difficulty(selected_courses)
    if preferences.get("preferEasy"):
        score += (5 - avg_difficulty) * 5
    elif preferences.get("preferHard"):
        score += avg_difficulty * 3
    
    # Workload preference
    total_workload = calculate_workload(selected_courses)
    if preferences.get("preferLightWorkload"):
        score += max(0, 30 - total_workload * 2)
    
    # Credit matching bonus
    exact_credits = preferences.get("exactCredits")
    if exact_credits:
        total_credits = calculate_total_credits(selected_courses)
        credit_diff = abs(total_credits - exact_credits)
        score -= credit_diff * 10  # Penalty for not matching exact credits
    
    return score

def generate_optimal_schedule(available_courses, preferences=None):
    """
    Generate an optimal schedule from available courses.
    STRICT PRIORITY:
    1. Must satisfy exactCourses/maxCourses constraint
    2. Must satisfy credit constraints
    3. Must satisfy evening avoidance
    4. Then optimize for rating, difficulty, etc.
    """
    if preferences is None:
        preferences = {}
    
    # Extract hard constraints - handle None values properly
    exact_courses = preferences.get("exactCourses")
    max_courses = preferences.get("maxCourses") or 8  # Use or to handle None
    min_courses = preferences.get("minCourses")
    
    exact_credits = preferences.get("exactCredits")
    min_credits = preferences.get("minCredits")
    max_credits = preferences.get("maxCredits")
    
    avoid_evening = preferences.get("timeConstraints", {}).get("avoidEvening", False)
    
    # Determine target course count
    if exact_courses is not None:
        target_courses = exact_courses
    else:
        target_courses = max_courses
    
    # Filter courses that match hard constraints
    valid_courses = []
    for c in available_courses:
        if matches_hard_constraints(c, preferences):
            valid_courses.append(c)
    
    print(f"[Scheduler] {len(valid_courses)} courses match hard constraints (from {len(available_courses)})")
    if avoid_evening:
        print(f"[Scheduler] Evening courses filtered out")
    
    # Sort by comprehensive score for selection priority
    valid_courses.sort(key=lambda c: (
        c["rating"] * 3,  # High rating is most important
        (5 - c["difficulty"]) * 2,  # Low difficulty
        (5 - c["workload"])  # Low workload
    ), reverse=True)
    
    # Greedily select courses
    selected = []
    
    for course in valid_courses:
        # Check if we've reached course limit
        if exact_courses is not None:
            if len(selected) >= exact_courses:
                break
        elif len(selected) >= max_courses:
            break
        
        # Check credit constraints before adding
        test_credits = calculate_total_credits(selected + [course])
        if max_credits is not None and test_credits > max_credits:
            continue
        if exact_credits is not None and test_credits > exact_credits:
            continue
        
        # Check conflict
        if has_any_conflict(selected, course):
            continue
        
        selected.append(course)
    
    # If we need exact credits, try to adjust
    if exact_credits is not None:
        current_credits = calculate_total_credits(selected)
        if current_credits < exact_credits:
            # Try to add more courses to reach exact credits
            for course in valid_courses:
                if course in selected:
                    continue
                if len(selected) >= max_courses:
                    break
                test_credits = calculate_total_credits(selected + [course])
                if test_credits <= exact_credits and not has_any_conflict(selected, course):
                    selected.append(course)
                    current_credits = test_credits
                    if current_credits == exact_credits:
                        break
    
    # Final constraint check
    is_valid, reason = check_final_constraints(selected, preferences)
    
    # Calculate statistics
    stats = {
        "totalCredits": calculate_total_credits(selected),
        "courseCount": calculate_course_count(selected),
        "totalWorkload": calculate_workload(selected),
        "averageRating": calculate_average_rating(selected),
        "averageDifficulty": calculate_average_difficulty(selected),
        "score": calculate_score(selected, preferences),
        "constraintsSatisfied": is_valid,
        "constraintsReason": reason if not is_valid else None
    }
    
    print(f"[Scheduler] Selected {len(selected)} courses, {stats['totalCredits']} credits")
    print(f"[Scheduler] Constraints satisfied: {is_valid}")
    if not is_valid:
        print(f"[Scheduler] Reason: {reason}")
    
    return {
        "courses": selected,
        "stats": stats,
        "conflicts": [],
        "preferences": preferences
    }

def generate_schedule_grid(courses):
    """Generate a visual schedule grid"""
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    hours = list(range(8, 22))  # 8:00 - 21:00
    
    grid = []
    for day_index, day in enumerate(days):
        day_slots = []
        for hour in hours:
            day_slots.append({
                "hour": hour,
                "time": f"{hour:02d}:00",
                "course": None,
                "isOccupied": False
            })
        grid.append({
            "day": day,
            "slots": day_slots
        })
    
    for course in courses:
        for slot in course["schedule"]:
            day_index = slot["day"] - 1
            if day_index < 0 or day_index >= 7:
                continue
            
            start_hour = int(slot["startTime"].split(":")[0])
            end_hour = int(slot["endTime"].split(":")[0])
            
            for h in range(start_hour, end_hour):
                slot_index = hours.index(h) if h in hours else -1
                if slot_index >= 0:
                    grid[day_index]["slots"][slot_index]["course"] = course
                    grid[day_index]["slots"][slot_index]["isOccupied"] = True
    
    return grid
