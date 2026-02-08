from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import pathlib

from data.courses import courses, get_all_courses, get_course_by_id
from services.scheduler import generate_optimal_schedule, generate_schedule_grid
from services.ai import parse_user_requirements, generate_recommendation_summary

load_dotenv()

app = FastAPI(
    title="Course Selector API",
    description="AI-powered course selection assistant",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    input: str
    selectedCourseIds: Optional[List[str]] = []

class ScheduleGridRequest(BaseModel):
    courseIds: List[str]

@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": str(__import__('datetime').datetime.now())}

@app.get("/api/courses")
def get_courses(department: Optional[str] = None, tag: Optional[str] = None, search: Optional[str] = None):
    result = get_all_courses()
    
    if department:
        result = [c for c in result if department in c["department"]]
    
    if tag:
        result = [c for c in result if tag in c["tags"]]
    
    if search:
        search_lower = search.lower()
        result = [c for c in result if 
                  search_lower in c["name"].lower() or
                  search_lower in c["nameEn"].lower() or
                  search_lower in c["code"].lower() or
                  search_lower in c["instructor"].lower()]
    
    return {
        "success": True,
        "count": len(result),
        "courses": result
    }

@app.get("/api/courses/{course_id}")
def get_course(course_id: str):
    course = get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"success": True, "course": course}

@app.post("/api/schedule/grid")
def get_schedule_grid(request: ScheduleGridRequest):
    selected_courses = [get_course_by_id(cid) for cid in request.courseIds if get_course_by_id(cid)]
    grid = generate_schedule_grid(selected_courses)
    return {
        "success": True,
        "grid": grid,
        "courses": selected_courses
    }

@app.post("/api/recommend")
async def recommend(request: RecommendRequest):
    try:
        print(f"收到选课请求: {request.input}")
        
        # Step 1: Parse user requirements with AI
        ai_result = await parse_user_requirements(request.input)
        preferences = ai_result["preferences"]
        
        print(f"解析的偏好: {preferences}")
        
        # Step 2: Filter courses based on preferences
        available_courses = get_all_courses()
        
        # Filter by interests
        if preferences.get("interests"):
            interest_matches = []
            for c in available_courses:
                for interest in preferences["interests"]:
                    if (interest in c["name"] or 
                        any(interest in tag for tag in c["tags"]) or
                        interest in c["description"]):
                        interest_matches.append(c)
                        break
            if interest_matches:
                available_courses = interest_matches
        
        # Filter by difficulty preference
        difficulty_pref = preferences.get("difficultyPreference", "any")
        if difficulty_pref == "easy":
            available_courses = [c for c in available_courses if c["difficulty"] <= 2.5]
        elif difficulty_pref == "hard":
            available_courses = [c for c in available_courses if c["difficulty"] >= 4]
        
        # Filter by workload preference
        workload_pref = preferences.get("workloadPreference", "any")
        if workload_pref == "light":
            available_courses = [c for c in available_courses if c["workload"] <= 2]
        
        # Filter by grade preference
        grade_pref = preferences.get("gradePreference", "any")
        if grade_pref == "high":
            available_courses = [c for c in available_courses 
                                 if c["gradeDistribution"]["A"] >= 30 
                                 or c["gradeDistribution"]["A"] + c["gradeDistribution"]["B"] >= 70]
        
        # Remove avoided courses
        if preferences.get("avoidCourses"):
            available_courses = [c for c in available_courses
                                 if not any(avoid in c["name"] or avoid in c["code"]
                                           for avoid in preferences["avoidCourses"])]
        
        # Step 3: Generate optimal schedule
        preferred_courses = []
        if preferences.get("interests"):
            for c in available_courses:
                for interest in preferences["interests"]:
                    if interest in c["name"] or interest in c["tags"]:
                        preferred_courses.append(c)
                        break
        
        schedule_result = generate_optimal_schedule(
            available_courses,
            {
                "requiredCourses": preferences.get("requiredCourses", []),
                "preferredCourses": preferred_courses,
                "preferEasy": difficulty_pref == "easy",
                "preferLightWorkload": workload_pref == "light",
                "maxCourses": preferences.get("maxCourses", 6)
            }
        )
        
        # Step 4: Generate AI summary
        summary = await generate_recommendation_summary(
            schedule_result["courses"],
            request.input,
            preferences
        )
        
        # Step 5: Generate schedule grid
        grid = generate_schedule_grid(schedule_result["courses"])
        
        return {
            "success": True,
            "data": {
                "preferences": preferences,
                "reasoning": ai_result.get("reasoning", ""),
                "summary": summary,
                "schedule": schedule_result,
                "grid": grid
            }
        }
        
    except Exception as e:
        print(f"推荐失败: {e}")
        raise HTTPException(status_code=500, detail=f"生成推荐时出错: {str(e)}")

@app.get("/api/filters")
def get_filters():
    departments = list(set(c["department"] for c in courses))
    tags = list(set(tag for c in courses for tag in c["tags"]))
    return {
        "success": True,
        "departments": departments,
        "tags": tags
    }

# Serve static frontend files
@app.get("/")
async def serve_index():
    current_dir = pathlib.Path(__file__).parent
    # Check multiple possible paths for frontend files
    possible_paths = [
        current_dir / "dist" / "index.html",
        current_dir / "frontend" / "dist" / "index.html",
        current_dir / ".." / "frontend" / "dist" / "index.html",
    ]
    for index_path in possible_paths:
        if index_path.exists():
            return FileResponse(str(index_path))
    return {"message": "Course Selector API - Frontend files not found"}

# Mount static files
possible_dirs = [
    pathlib.Path(__file__).parent / "dist",
    pathlib.Path(__file__).parent / "frontend" / "dist",
    pathlib.Path(__file__).parent / ".." / "frontend" / "dist",
]
for frontend_dir in possible_dirs:
    if frontend_dir.exists():
        app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
        break

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)