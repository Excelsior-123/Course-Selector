from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import pathlib

from data.courses import courses, get_all_courses, get_course_by_id, search_courses
from services.scheduler import generate_optimal_schedule, generate_schedule_grid
from services.ai import parse_user_requirements, generate_recommendation_summary
import re

def extract_preferences_fallback(user_input: str):
    """Fallback method to extract preferences using keyword matching"""
    user_input_lower = user_input.lower()
    
    # Extract interests based on keywords
    interest_keywords = {
        "数学": ["数学分析", "高等数学", "线性代数", "拓扑学", "回归分析"],
        "计算机": ["计算机", "程序设计", "数据结构", "算法", "人工智能", "数据库", "网络"],
        "物理": ["物理", "量子力学"],
        "心理": ["心理学", "社会心理学"],
        "体育": ["篮球", "羽毛球", "游泳", "体育"],
        "艺术": ["艺术", "电影", "音乐"],
        "哲学": ["哲学"]
    }
    
    interests = []
    for category, keywords in interest_keywords.items():
        for keyword in keywords:
            if keyword in user_input_lower:
                interests.append(keyword)
                break
    
    # Determine preferences
    prefer_easy = any(kw in user_input_lower for kw in ["简单", "水课", "好拿分", "给分高", "容易"])
    prefer_light = any(kw in user_input_lower for kw in ["作业少", "轻松", "不费劲"])
    
    # Extract time constraints (basic)
    time_keywords = []
    if any(kw in user_input_lower for kw in ["上午", "早上"]):
        time_keywords.append("morning")
    if any(kw in user_input_lower for kw in ["下午", "晚上", "晚课"]):
        time_keywords.append("evening")
    
    return {
        "preferences": {
            "interests": interests,
            "timeConstraints": {
                "preferredDays": [1, 2, 3, 4, 5],
                "preferredTimeRanges": [],
                "avoidEvening": "晚上" not in user_input_lower and "晚课" in user_input_lower
            },
            "difficultyPreference": "easy" if prefer_easy else "any",
            "workloadPreference": "light" if prefer_light else "any",
            "gradePreference": "high" if prefer_easy else "any",
            "requiredCourses": [],
            "avoidCourses": [],
            "maxCourses": 6,
            "priorities": []
        },
        "reasoning": f"基于关键词提取：兴趣={interests}, 难度偏好={'简单' if prefer_easy else '任意'}"
    }

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
    import datetime
    api_key_status = "configured" if os.getenv("DEEPSEEK_API_KEY") else "missing"
    return {
        "status": "ok",
        "timestamp": str(datetime.datetime.now()),
        "api_key_status": api_key_status,
        "courses_count": len(courses)
    }

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
        
        # Check API key
        api_key = os.getenv("DEEPSEEK_API_KEY")
        print(f"API Key 状态: {'已设置' if api_key else '未设置'}")
        
        # Step 1: Parse user requirements with AI
        try:
            ai_result = await parse_user_requirements(request.input)
            preferences = ai_result["preferences"]
            print(f"AI 解析成功，偏好: {preferences}")
        except Exception as ai_error:
            print(f"AI 解析失败: {ai_error}")
            # Use basic keyword matching as fallback
            preferences = extract_preferences_fallback(request.input)
            print(f"使用备用解析: {preferences}")
        
        # Step 2: Filter courses based on preferences
        available_courses = get_all_courses()
        
        # Filter by interests - use search_courses for better matching
        if preferences.get("interests"):
            interest_matches = []
            for interest in preferences["interests"]:
                # Search in name, description, and tags
                matches = search_courses(interest)
                for m in matches:
                    if m not in interest_matches:
                        interest_matches.append(m)
            
            if interest_matches:
                available_courses = interest_matches
                print(f"根据兴趣 '{preferences['interests']}' 筛选出 {len(available_courses)} 门课程")
            else:
                print(f"未找到与兴趣 '{preferences['interests']}' 匹配的课程，使用全部课程")
        
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