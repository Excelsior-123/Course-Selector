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

def calculate_score(selected_courses, preferences=None):
    """Calculate a score for the schedule based on preferences"""
    if preferences is None:
        preferences = {}
    
    score = 0
    
    # Rating score (0-50)
    score += calculate_average_rating(selected_courses) * 10
    
    # Difficulty preference
    avg_difficulty = calculate_average_difficulty(selected_courses)
    if preferences.get("preferEasy"):
        score += (5 - avg_difficulty) * 5
    
    # Workload preference
    total_workload = calculate_workload(selected_courses)
    if preferences.get("preferLightWorkload"):
        score += max(0, 30 - total_workload * 2)
    
    # Number of courses
    score += len(selected_courses) * 3
    
    # Credit hours
    total_credits = sum(c["credits"] for c in selected_courses)
    score += total_credits * 2
    
    return score

def generate_optimal_schedule(available_courses, preferences=None, max_courses=6):
    """Generate an optimal schedule from available courses"""
    if preferences is None:
        preferences = {}
    
    required_courses = preferences.get("requiredCourses", [])
    preferred_courses = preferences.get("preferredCourses", [])
    
    # Start with required courses
    selected = list(required_courses)
    
    # Filter out conflicting preferred courses
    valid_preferred = [c for c in preferred_courses 
                       if not has_any_conflict(selected, c) 
                       and c["id"] not in [s["id"] for s in selected]]
    
    # Sort by rating and preference score
    valid_preferred.sort(key=lambda c: c["rating"] * 2 - c["difficulty"], reverse=True)
    
    # Add preferred courses greedily
    for course in valid_preferred:
        if len(selected) >= max_courses:
            break
        if not has_any_conflict(selected, course):
            selected.append(course)
    
    # Fill remaining slots with highly-rated courses
    remaining = [c for c in available_courses 
                 if c["id"] not in [s["id"] for s in selected] 
                 and not has_any_conflict(selected, c)]
    
    remaining.sort(key=lambda c: c["rating"] * 2 + (5 - c["difficulty"]) + (5 - c["workload"]), reverse=True)
    
    for course in remaining:
        if len(selected) >= max_courses:
            break
        selected.append(course)
    
    # Calculate statistics
    stats = {
        "totalCredits": sum(c["credits"] for c in selected),
        "totalWorkload": calculate_workload(selected),
        "averageRating": calculate_average_rating(selected),
        "averageDifficulty": calculate_average_difficulty(selected),
        "courseCount": len(selected),
        "score": calculate_score(selected, preferences)
    }
    
    return {
        "courses": selected,
        "stats": stats,
        "conflicts": []
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