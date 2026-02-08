import os
import json
import anthropic
from typing import Dict, Any

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY", "sk-api-nNHt79hIL5GSXj5DBHSGEhIPsNilUJQBORmHk7vMbLQ0Pkd7MBGluf36N_mix9gl-18cStiunbpljKGYE_tsVLjSVYKA8-FGe-5xZM4HT6QMiCnj4G1bkl4"),
    base_url=os.getenv("ANTHROPIC_BASE_URL", "https://api.minimaxi.com/anthropic"),
)

SYSTEM_PROMPT = """你是一个智能选课助手，帮助大学生解析选课需求并推荐最优课程组合。

你的任务是：
1. 解析用户的自然语言选课需求
2. 提取关键信息：
   - 感兴趣的课程类型/名称
   - 时间偏好（如"上午9点到下午6点"、"周二周四晚上"）
   - 难度偏好（如"考核简单"、"给分高"、"水课"）
   - 工作量偏好（如"作业少"）
   - 必选的课程
   - 想避开的课程

3. 返回结构化的JSON格式：
{
  "preferences": {
    "interests": ["计算机网络", "篮球"],
    "timeConstraints": {
      "preferredDays": [1, 2, 3, 4, 5],
      "preferredTimeRanges": [{"start": "09:00", "end": "18:00"}],
      "avoidEvening": false
    },
    "difficultyPreference": "easy",
    "workloadPreference": "light",
    "gradePreference": "high",
    "requiredCourses": [],
    "avoidCourses": [],
    "maxCourses": 6,
    "priorities": ["给分高", "作业少", "感兴趣"]
  },
  "reasoning": "用户想要选择计算机网络相关的专业课，同时选篮球课作为体育课..."
}

注意：
- 周一=1, 周二=2, 周三=3, 周四=4, 周五=5, 周六=6, 周日=7
- difficultyPreference: "easy", "medium", "hard", "any"
- workloadPreference: "light", "medium", "heavy", "any"
- gradePreference: "high", "medium", "any"
- 只返回JSON，不要其他文字"""

async def parse_user_requirements(user_input: str) -> Dict[str, Any]:
    """Parse user requirements using MiniMax-M2.1"""
    try:
        response = client.messages.create(
            model="MiniMax-M2.1",
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        content = response.content[0].text
        
        # Extract JSON from response
        json_start = content.find("{")
        json_end = content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            json_str = content[json_start:json_end]
            parsed = json.loads(json_str)
            return parsed
        
        raise ValueError("无法解析AI响应")
        
    except Exception as e:
        print(f"AI解析错误: {e}")
        # Return default preferences on error
        return {
            "preferences": {
                "interests": [],
                "timeConstraints": {
                    "preferredDays": [1, 2, 3, 4, 5],
                    "preferredTimeRanges": [],
                    "avoidEvening": False
                },
                "difficultyPreference": "any",
                "workloadPreference": "any",
                "gradePreference": "any",
                "requiredCourses": [],
                "avoidCourses": [],
                "maxCourses": 6,
                "priorities": []
            },
            "reasoning": "使用默认偏好设置"
        }

async def generate_recommendation_summary(selected_courses, user_input: str, preferences: Dict) -> str:
    """Generate a friendly recommendation summary"""
    try:
        courses_info = [
            {
                "name": c["name"],
                "code": c["code"],
                "instructor": c["instructor"],
                "rating": c["rating"],
                "difficulty": c["difficulty"]
            }
            for c in selected_courses
        ]
        
        prompt = f"""基于用户的选课需求："{user_input}"

已推荐以下课程：
{json.dumps(courses_info, ensure_ascii=False, indent=2)}

请生成一段友好的推荐总结，说明：
1. 为什么推荐这些课程
2. 课程组合的优点
3. 可能的注意事项

用中文回复，语气友好，像是一个贴心的学长/学姐在给出建议。"""
        
        response = client.messages.create(
            model="MiniMax-M2.1",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text
        
    except Exception as e:
        print(f"生成总结错误: {e}")
        return "已为您生成最优课程组合，请查看下方课表。"