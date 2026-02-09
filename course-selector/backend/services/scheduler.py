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

def check_constraints(selected_courses, preferences):
    """
    Check if selected courses meet user constraints.
    Returns (is_valid, reason)
    """
    # Check minimum credits requirement
    min_credits = preferences.get("minCredits")
    if min_credits:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits < min_credits:
            return False, f"学分不足：已选{total_credits}学分，要求至少{min_credits}学分"
    
    # Check exact credits requirement
    exact_credits = preferences.get("exactCredits")
    if exact_credits:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits != exact_credits:
            return False, f"学分不匹配：已选{total_credits}学分，要求恰好{exact_credits}学分"
    
    # Check maximum credits constraint
    max_credits = preferences.get("maxCredits")
    if max_credits:
        total_credits = calculate_total_credits(selected_courses)
        if total_credits > max_credits:
            return False, f"学分超限：已选{total_credits}学分，上限{max_credits}学分"
    
    # Check minimum courses requirement
    min_courses = preferences.get("minCourses")
    if min_courses:
        count = calculate_course_count(selected_courses)
        if count < min_courses:
            return False, f"课程数不足：已选{count}门，要求至少{min_courses}门"
    
    # Check exact courses requirement
    exact_courses = preferences.get("exactCourses")
    if exact_courses:
        count = calculate_course_count(selected_courses)
        if count != exact_courses:
            return False, f"课程数不匹配：已选{count}门，要求恰好{exact_courses}门"
    
    # Check maximum courses constraint
    max_courses = preferences.get("maxCourses", 8)
    count = calculate_course_count(selected_courses)
    if count > max_courses:
        return False, f"课程数超限：已选{count}门，上限{max_courses}门"
    
    return True, "满足所有约束"

def calculate_score(selected_courses, preferences=None):
    """Calculate a score for the schedule based on preferences"""
    if preferences is None:
        preferences = {}
    
    score = 0
    
    # Rating score (0-50) - higher rating = higher score
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
    
    # Number of courses bonus
    score += len(selected_courses) * 3
    
    # Credit hours bonus
    total_credits = calculate_total_credits(selected_courses)
    score += total_credits * 2
    
    # Time preference matching bonus
    if preferences.get("timeConstraints"):
        time_score = calculate_time_preference_score(selected_courses, preferences["timeConstraints"])
        score += time_score
    
    return score

def calculate_time_preference_score(selected_courses, time_constraints):
    """Calculate how well the schedule matches time preferences"""
    score = 0
    preferred_days = time_constraints.get("preferredDays", [1, 2, 3, 4, 5])
    preferred_ranges = time_constraints.get("preferredTimeRanges", [])
    avoid_evening = time_constraints.get("avoidEvening", False)
    
    for course in selected_courses:
        for slot in course["schedule"]:
            # Check day preference
            if slot["day"] in preferred_days:
                score += 2
            
            # Check time range preference
            if preferred_ranges:
                start_mins = time_to_minutes(slot["startTime"])
                end_mins = time_to_minutes(slot["endTime"])
                
                for range_spec in preferred_ranges:
                    range_start = time_to_minutes(range_spec["start"])
                    range_end = time_to_minutes(range_spec["end"])
                    
                    # Course falls within preferred range
                    if start_mins >= range_start and end_mins <= range_end:
                        score += 3
                        break
            
            # Check evening avoidance
            if avoid_evening:
                start_hour = int(slot["startTime"].split(":")[0])
                if start_hour < 18:  # Not evening
                    score += 1
    
    return score

def matches_time_preferences(course, time_constraints):
    """Check if a course matches time preferences"""
    if not time_constraints:
        return True
    
    preferred_days = time_constraints.get("preferredDays", [])
    avoid_days = time_constraints.get("avoidDays", [])
    preferred_ranges = time_constraints.get("preferredTimeRanges", [])
    avoid_evening = time_constraints.get("avoidEvening", False)
    
    for slot in course["schedule"]:
        # Check day constraints
        if avoid_days and slot["day"] in avoid_days:
            return False
        
        if preferred_days and slot["day"] not in preferred_days:
            return False
        
        # Check evening avoidance
        if avoid_evening:
            start_hour = int(slot["startTime"].split(":")[0])
            if start_hour >= 18:
                return False
        
        # Check time range preferences (if specified, at least one slot should match)
        if preferred_ranges:
            start_mins = time_to_minutes(slot["startTime"])
            end_mins = time_to_minutes(slot["endTime"])
            
            in_preferred_range = False
            for range_spec in preferred_ranges:
                range_start = time_to_minutes(range_spec["start"])
                range_end = time_to_minutes(range_spec["end"])
                
                if start_mins >= range_start and end_mins <= range_end:
                    in_preferred_range = True
                    break
            
            if not in_preferred_range:
                return False
    
    return True

def generate_optimal_schedule(available_courses, preferences=None):
    """
    Generate an optimal schedule from available courses.
    Priority: 1. Meet credit/course constraints 2. Optimize based on preferences
    """
    if preferences is None:
        preferences = {}
    
    required_courses = preferences.get("requiredCourses", [])
    
    # Start with required courses
    selected = list(required_courses)
    
    # Filter available courses based on time preferences and conflicts
    valid_courses = []
    for c in available_courses:
        if c["id"] in [s["id"] for s in selected]:
            continue
        if has_any_conflict(selected, c):
            continue
        if not matches_time_preferences(c, preferences.get("timeConstraints")):
            continue
        valid_courses.append(c)
    
    # Sort by comprehensive score (rating, ease, low workload)
    valid_courses.sort(key=lambda c: (
        c["rating"] * 2,  # High rating
        (5 - c["difficulty"]) * 1.5,  # Low difficulty
        (5 - c["workload"])  # Low workload
    ), reverse=True)
    
    # Phase 1: Meet minimum requirements
    min_credits = preferences.get("minCredits", 0)
    min_courses = preferences.get("minCourses", 0)
    max_courses = preferences.get("maxCourses", 6)
    max_credits = preferences.get("maxCredits", 25)
    
    # Add courses until minimums are met
    for course in valid_courses[:]:
        if len(selected) >= max_courses:
            break
        
        total_credits = calculate_total_credits(selected)
        if max_credits and total_credits >= max_credits:
            break
        
        if not has_any_conflict(selected, course):
            selected.append(course)
            valid_courses.remove(course)
    
    # Check if constraints are satisfied
    is_valid, reason = check_constraints(selected, preferences)
    
    # Phase 2: Optimize by replacing courses if possible
    if is_valid:
        # Try to improve the schedule by swapping courses
        for i, current_course in enumerate(selected):
            if current_course in required_courses:
                continue  # Don't replace required courses
            
            # Find a better replacement
            for alternative in valid_courses:
                # Check if alternative is better
                if (alternative["rating"] > current_course["rating"] or
                    (alternative["rating"] == current_course["rating"] and 
                     alternative["difficulty"] < current_course["difficulty"])):
                    
                    # Check if swap maintains validity
                    test_selection = selected[:i] + selected[i+1:] + [alternative]
                    still_valid, _ = check_constraints(test_selection, preferences)
                    
                    if still_valid and not has_any_conflict(test_selection[:-1], alternative):
                        selected[i] = alternative
                        valid_courses.remove(alternative)
                        valid_courses.append(current_course)
                        break
    
    # Calculate final statistics
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
