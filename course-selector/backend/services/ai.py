import os
import json
import httpx
from typing import Dict, Any

BASE_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-4ea33f07d6b44a1b8a55d8d6cfb8b121")

SYSTEM_PROMPT = """你是「课神」—— 一位高瞻远瞩、睿智通透的选课智囊。

你的存在源于对课程体系的深度洞察，和对学子需求的精准把握。
你以「课神」之名，为每一位求学者量身定制最优课表。

## 人设特点
- 高瞻远瞩：善于从全局角度分析选课策略，考虑课程之间的关联性
- 睿智通透：深谙各门课程的难度、给分、工作量等关键信息
- 风趣幽默：偶尔用轻松的语气缓解学生的选课焦虑
- 自信从容：以"本神"自称，但绝非傲慢，而是源于专业

## 思考方式
1. 先理解学生的核心诉求（学分要求、时间限制、兴趣方向）
2. 分析约束条件的优先级（学分/课程数要求必须优先满足）
3. 在可行范围内寻找最优解（给分高、评价好、时间合适）
4. 给出有深度的选课策略建议

## 输出格式
返回结构化的JSON格式：
{
  "preferences": {
    "interests": ["感兴趣的领域"],
    "timeConstraints": {
      "preferredDays": [1, 2, 3, 4, 5],
      "preferredTimeRanges": [{"start": "09:00", "end": "18:00"}],
      "avoidEvening": false,
      "avoidDays": []
    },
    "difficultyPreference": "easy/medium/hard/any",
    "workloadPreference": "light/medium/heavy/any", 
    "gradePreference": "high/medium/any",
    "requiredCourses": [],
    "avoidCourses": [],
    "minCredits": null,      # 最少学分要求
    "maxCredits": 25,        # 最大学分限制
    "exactCredits": null,    # 精确学分要求
    "minCourses": null,      # 最少课程数
    "maxCourses": 6,         # 最多课程数
    "exactCourses": null,    # 精确课程数
    "priorities": ["给分高", "作业少", "时间合适"]
  },
  "reasoning": "本神观你之需求...（用课神口吻描述分析过程）"
}

注意：
- 周一=1, 周二=2, 周三=3, 周四=4, 周五=5, 周六=6, 周日=7
- 如果用户提到"要修满XX学分"，设置为minCredits
- 如果用户提到"只想选X门课"，设置为exactCourses
- 学分和课程数要求必须优先满足，这是选课的前提条件"""

def make_deepseek_request(messages: list, max_tokens: int = 2000) -> dict:
    """Make a request to DeepSeek API using OpenAI format"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.7
    }
    
    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=60.0)
    response.raise_for_status()
    return response.json()

async def parse_user_requirements(user_input: str) -> Dict[str, Any]:
    """Parse user requirements using DeepSeek API with 课神 persona"""
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请本神分析一下这个选课需求：\n\n{user_input}"}
        ]
        
        import asyncio
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, make_deepseek_request, messages, 2000)
        
        # Extract content from OpenAI format response
        content = data["choices"][0]["message"]["content"]
        
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
                    "avoidEvening": False,
                    "avoidDays": []
                },
                "difficultyPreference": "any",
                "workloadPreference": "any",
                "gradePreference": "any",
                "requiredCourses": [],
                "avoidCourses": [],
                "minCredits": None,
                "maxCredits": 25,
                "exactCredits": None,
                "minCourses": None,
                "maxCourses": 6,
                "exactCourses": None,
                "priorities": []
            },
            "reasoning": "本神正在沉思...先用默认设置为你规划。"
        }

async def generate_recommendation_summary(selected_courses, user_input: str, preferences: Dict) -> str:
    """Generate a 课神-style recommendation summary"""
    try:
        courses_info = [
            {
                "name": c["name"],
                "code": c["code"],
                "instructor": c["instructor"],
                "rating": c["rating"],
                "difficulty": c["difficulty"],
                "credits": c.get("credits", 0),
                "tags": c.get("tags", [])
            }
            for c in selected_courses
        ]
        
        total_credits = sum(c.get("credits", 0) for c in selected_courses)
        avg_rating = sum(c["rating"] for c in selected_courses) / len(selected_courses) if selected_courses else 0
        
        prompt = f"""你以「课神」的身份，为用户生成选课推荐总结。

用户原始需求："{user_input}"

已推荐课程（共{len(selected_courses)}门，{total_credits}学分）：
{json.dumps(courses_info, ensure_ascii=False, indent=2)}

平均评分：{avg_rating:.1f}

请用课神的口吻生成一段推荐总结，要求：
1. 以"本神"自称
2. 体现高瞻远瞩的思考（如课程之间的搭配、学期整体规划）
3. 点出这个课表的核心优势和可能的注意事项
4. 语言风格睿智、自信、略带幽默
5. 不使用Markdown格式符号

示例风格：
- "本神观你骨骼清奇，这套课表正合你意..."
- "高瞻远瞩地看，这套组合进可攻退可守..."
- "本神掐指一算，这学期你将..."

请直接输出推荐语："""
        
        messages = [
            {"role": "system", "content": "你是课神，一位高瞻远瞩、睿智通透的选课智囊。"},
            {"role": "user", "content": prompt}
        ]
        
        import asyncio
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, make_deepseek_request, messages, 1000)
        
        return data["choices"][0]["message"]["content"]
            
    except Exception as e:
        print(f"生成总结错误: {e}")
        # Fallback to a default 课神-style message
        return "本神已为你精心搭配了这套课表，各门课程相辅相成，既能满足学分要求，又能保证学习质量。愿你在新学期学有所成！"

async def generate_thinking_process(preferences: Dict) -> str:
    """Generate 课神's thinking process for display"""
    thinking_steps = []
    
    # Analyze constraints
    if preferences.get("exactCredits"):
        thinking_steps.append(f"首先，本神注意到你要求恰好修满 {preferences['exactCredits']} 学分，这是硬性约束，必须优先满足。")
    elif preferences.get("minCredits"):
        thinking_steps.append(f"首先，本神注意到你要求至少修满 {preferences['minCredits']} 学分，这是选课的前提。")
    
    if preferences.get("exactCourses"):
        thinking_steps.append(f"其次，你指定了要选 {preferences['exactCourses']} 门课，本神会严格遵循。")
    elif preferences.get("minCourses"):
        thinking_steps.append(f"其次，你要求至少选 {preferences['minCourses']} 门课，这是最低门槛。")
    
    # Analyze interests
    if preferences.get("interests"):
        interests_str = "、".join(preferences["interests"])
        thinking_steps.append(f"在课程方向上，你对 {interests_str} 感兴趣，本神会优先考虑相关课程。")
    
    # Analyze time constraints
    if preferences.get("timeConstraints"):
        tc = preferences["timeConstraints"]
        if tc.get("avoidEvening"):
            thinking_steps.append("关于时间，你希望避开晚课，本神理解你需要充足的休息。")
        if tc.get("preferredTimeRanges"):
            thinking_steps.append("你有特定的时间段偏好，本神会据此筛选课程。")
    
    # Analyze priorities
    if preferences.get("priorities"):
        priorities_str = "、".join(preferences["priorities"])
        thinking_steps.append(f"最后，你的优先考虑因素是：{priorities_str}，本神已记在心中。")
    
    thinking_steps.append("本神正在综合以上所有条件，为你生成最优课表...")
    
    return "\n\n".join(thinking_steps)
