import os
import json
import httpx
from typing import Dict, Any

BASE_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-4ea33f07d6b44a1b8a55d8d6cfb8b121")

SYSTEM_PROMPT = """你是「课神」—— 一位高瞻远瞩、睿智通透的选课智囊。

【最高优先级原则 - 必须严格遵守】
用户提到的以下三个约束是硬性要求，必须优先满足，其他所有偏好都要在这些约束之后考虑：

1. **学分要求**（最重要）
   - 如果用户说"想修满XX学分"、"要修XX学分"、"需要XX学分"→ 设置为 exactCredits
   - 如果用户说"至少XX学分"、"最少XX学分"→ 设置为 minCredits
   - 如果用户说"最多XX学分"、"不超过XX学分"→ 设置为 maxCredits

2. **课程数量要求**（次重要）
   - 如果用户说"想选X门课"、"要选X门课"、"只选X门课"→ 设置为 exactCourses
   - 如果用户说"至少X门"、"最少X门"→ 设置为 minCourses
   - 如果用户说"最多X门"、"不超过X门"→ 设置为 maxCourses

3. **时间限制**（第三重要）
   - 如果用户说"不要晚课"、"不选晚上的课"、"晚上没空"→ avoidEvening = true
   - 如果用户说"只要上午的课"→ preferredTimeRanges = [{"start": "08:00", "end": "12:00"}]
   - 如果用户说"只要下午的课"→ preferredTimeRanges = [{"start": "14:00", "end": "18:00"}]
   - 如果用户指定了具体时间如"9点到6点"→ 精确解析并设置

【绝对禁止】
- 严禁推荐超过用户要求的课程数量
- 严禁在用户明确不要晚课时推荐晚课
- 严禁忽视用户明确的学分要求

【思考方式】
1. 首先识别并记录用户的硬性约束（学分、课程数、时间）
2. 然后分析用户的偏好方向（给分高、作业少、感兴趣的课程类型）
3. 在推荐时，先确保满足硬性约束，再优化软性偏好

【输出格式】
返回结构化的JSON格式：
{
  "preferences": {
    "interests": ["感兴趣的领域"],
    "timeConstraints": {
      "preferredDays": [1, 2, 3, 4, 5],
      "preferredTimeRanges": [],
      "avoidEvening": false,
      "avoidDays": []
    },
    "difficultyPreference": "easy/medium/hard/any",
    "workloadPreference": "light/medium/heavy/any", 
    "gradePreference": "high/medium/any",
    "requiredCourses": [],
    "avoidCourses": [],
    "minCredits": null,
    "maxCredits": 25,
    "exactCredits": null,
    "minCourses": null,
    "maxCourses": 8,
    "exactCourses": null,
    "priorities": ["给分高", "作业少"]
  },
  "reasoning": "本神检测到你有以下硬性要求：1. 必须选X门课 2. 不要晚课 3. 要修满XX学分。在此基础上..."
}

注意：
- 周一=1, 周二=2, 周三=3, 周四=4, 周五=5, 周六=6, 周日=7
- 如果用户明确说"只想选4门"，必须设置 exactCourses: 4，而不是 maxCourses
- 如果用户说"不要晚课"，必须设置 avoidEvening: true
- 你的reasoning中必须明确说明你识别出的硬性约束"""

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
        "temperature": 0.3  # 降低温度，让输出更确定
    }
    
    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=60.0)
    response.raise_for_status()
    return response.json()

async def parse_user_requirements(user_input: str) -> Dict[str, Any]:
    """Parse user requirements using DeepSeek API with 课神 persona"""
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请本神分析一下这个选课需求，特别注意识别硬性约束（学分、课程数、时间限制）：\n\n{user_input}"}
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
            
            # 后处理：确保约束被正确设置
            prefs = parsed.get("preferences", {})
            
            # 如果用户明确说"想选X门课"，优先使用 exactCourses
            import re
            course_num_match = re.search(r'(想|要|只|需|准备|打算)选\s*(\d+)\s*门', user_input)
            if course_num_match:
                exact_courses = int(course_num_match.group(2))
                prefs["exactCourses"] = exact_courses
                prefs["maxCourses"] = exact_courses  # 同时限制最大数量
            
            # 检测"不要晚课"、"晚上没空"等
            if any(kw in user_input for kw in ["不要晚课", "不选晚课", "晚上没空", "晚上不行", "不要晚上"]):
                if "timeConstraints" not in prefs:
                    prefs["timeConstraints"] = {}
                prefs["timeConstraints"]["avoidEvening"] = True
            
            # 检测学分要求
            credit_match = re.search(r'(想|要|需|准备|打算|必须|得|需要)(修|选|上|满|凑|攒)(\s*满)?\s*(\d+)\s*学分', user_input)
            if credit_match:
                exact_credits = int(credit_match.group(4))
                prefs["exactCredits"] = exact_credits
            
            parsed["preferences"] = prefs
            return parsed
        
        raise ValueError("无法解析AI响应")
            
    except Exception as e:
        print(f"AI解析错误: {e}")
        # 使用正则表达式兜底解析
        import re
        prefs = {
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
            "maxCourses": 8,
            "exactCourses": None,
            "priorities": []
        }
        
        # 兜底正则解析
        course_num_match = re.search(r'(想|要|只|需|准备|打算)选\s*(\d+)\s*门', user_input)
        if course_num_match:
            prefs["exactCourses"] = int(course_num_match.group(2))
            prefs["maxCourses"] = int(course_num_match.group(2))
        
        if any(kw in user_input for kw in ["不要晚课", "不选晚课", "晚上没空"]):
            prefs["timeConstraints"]["avoidEvening"] = True
        
        credit_match = re.search(r'(\d+)\s*学分', user_input)
        if credit_match:
            prefs["exactCredits"] = int(credit_match.group(1))
        
        return {
            "preferences": prefs,
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
        
        # 获取用户的硬性约束
        exact_courses = preferences.get("exactCourses")
        avoid_evening = preferences.get("timeConstraints", {}).get("avoidEvening", False)
        exact_credits = preferences.get("exactCredits")
        
        constraint_desc = ""
        if exact_courses:
            constraint_desc += f"严格限定{exact_courses}门课程"
        if avoid_evening:
            constraint_desc += "，避开所有晚课"
        if exact_credits:
            constraint_desc += f"，确保{exact_credits}学分"
        
        prompt = f"""你以「课神」的身份，为用户生成选课推荐总结。

用户原始需求："{user_input}"

硬性约束：{constraint_desc}

已推荐课程（共{len(selected_courses)}门，{total_credits}学分）：
{json.dumps(courses_info, ensure_ascii=False, indent=2)}

平均评分：{avg_rating:.1f}

请用课神的口吻生成一段推荐总结，要求：
1. 以"本神"自称
2. 说明你如何严格遵守了用户的硬性约束（课程数量、时间限制、学分要求）
3. 点出这个课表在满足硬性约束前提下的优势
4. 语言风格睿智、自信、略带幽默
5. 不使用Markdown格式符号

请直接输出推荐语："""
        
        messages = [
            {"role": "system", "content": "你是课神，一位高瞻远瞩、睿智通透的选课智囊。你严格遵守用户的硬性约束。"},
            {"role": "user", "content": prompt}
        ]
        
        import asyncio
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, make_deepseek_request, messages, 1000)
        
        return data["choices"][0]["message"]["content"]
            
    except Exception as e:
        print(f"生成总结错误: {e}")
        # Fallback to a default 课神-style message
        return "本神已严格遵循你的要求，为你精心搭配了这套课表。各门课程符合你的时间和数量要求，愿你在新学期学有所成！"

async def generate_thinking_process(preferences: Dict) -> str:
    """Generate 课神's thinking process for display"""
    thinking_steps = []
    
    # 首先强调硬性约束
    has_constraint = False
    
    exact_courses = preferences.get("exactCourses")
    if exact_courses:
        thinking_steps.append(f"【硬性约束】检测到你要求恰好选 {exact_courses} 门课，本神将严格遵守，绝不多选。")
        has_constraint = True
    elif preferences.get("maxCourses") and preferences.get("maxCourses") < 8:
        thinking_steps.append(f"【硬性约束】检测到你最多选 {preferences['maxCourses']} 门课，本神将严格控制数量。")
        has_constraint = True
    
    exact_credits = preferences.get("exactCredits")
    if exact_credits:
        thinking_steps.append(f"【硬性约束】检测到你要求恰好修满 {exact_credits} 学分，本神将精确匹配。")
        has_constraint = True
    
    avoid_evening = preferences.get("timeConstraints", {}).get("avoidEvening", False)
    if avoid_evening:
        thinking_steps.append(f"【硬性约束】检测到你明确要求避开晚课，本神将过滤所有晚间课程。")
        has_constraint = True
    
    if not has_constraint:
        thinking_steps.append("本神正在分析你的选课需求...")
    
    # 分析其他偏好
    if preferences.get("interests"):
        interests_str = "、".join(preferences["interests"])
        thinking_steps.append(f"在软性偏好上，你对 {interests_str} 感兴趣。")
    
    thinking_steps.append("本神正在综合以上所有条件，为你生成最优课表...")
    
    return "\n\n".join(thinking_steps)
