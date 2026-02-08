#!/usr/bin/env python3
"""
icourse.club 课程数据爬虫
爬取高分课程并生成 courses.py 数据文件
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup
from typing import List, Dict

BASE_URL = "https://icourse.club"

def fetch_course_list(page: int = 1) -> List[Dict]:
    """Fetch course list from icourse.club"""
    url = f"{BASE_URL}/course/?page={page}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        courses = []
        
        # Find all course items
        course_items = soup.find_all('a', href=re.compile(r'/course/\d+/'))
        
        for item in course_items:
            try:
                # Extract course info
                name_elem = item.find('h4')
                if not name_elem:
                    continue
                
                course_name = name_elem.text.strip()
                course_url = item['href']
                course_id = re.search(r'/course/(\d+)/', course_url).group(1)
                
                # Find rating
                rating_elem = item.find(text=re.compile(r'\d+\.\d+'))
                rating = 0.0
                if rating_elem:
                    rating_match = re.search(r'(\d+\.\d+)', str(rating_elem))
                    if rating_match:
                        rating = float(rating_match.group(1))
                
                # Find stats
                stats = item.find_all(text=re.compile(r'课程难度|作业多少|给分好坏|收获大小'))
                difficulty = "中等"
                workload = "中等"
                grade = "一般"
                
                for stat in stats:
                    if '课程难度' in str(stat):
                        match = re.search(r'课程难度：(\S+)', str(stat))
                        if match:
                            difficulty = match.group(1)
                    elif '作业多少' in str(stat):
                        match = re.search(r'作业多少：(\S+)', str(stat))
                        if match:
                            workload = match.group(1)
                    elif '给分好坏' in str(stat):
                        match = re.search(r'给分好坏：(\S+)', str(stat))
                        if match:
                            grade = match.group(1)
                
                # Extract instructor from course name
                instructor = "未知"
                name_match = re.search(r'(.+?)（(.+?)）', course_name)
                if name_match:
                    course_name_clean = name_match.group(1)
                    instructor = name_match.group(2)
                else:
                    course_name_clean = course_name
                
                courses.append({
                    'id': course_id,
                    'name': course_name_clean,
                    'instructor': instructor,
                    'rating': rating,
                    'difficulty_text': difficulty,
                    'workload_text': workload,
                    'grade_text': grade,
                    'url': f"{BASE_URL}{course_url}"
                })
                
            except Exception as e:
                print(f"Error parsing course: {e}")
                continue
        
        return courses
        
    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return []

def fetch_course_detail(course_id: str) -> Dict:
    """Fetch detailed course info"""
    url = f"{BASE_URL}/course/{course_id}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract description
        desc_elem = soup.find('div', class_='course-description')
        description = ""
        if desc_elem:
            description = desc_elem.text.strip()
        
        # Extract reviews
        reviews = []
        review_items = soup.find_all('div', class_='review-item')[:3]  # Top 3 reviews
        
        for item in review_items:
            content_elem = item.find('div', class_='review-content')
            if content_elem:
                content = content_elem.text.strip()[:200]  # Limit length
                reviews.append({
                    'content': content,
                    'rating': 5,
                    'author': '匿名',
                    'date': '2024-01'
                })
        
        return {
            'description': description,
            'reviews': reviews
        }
        
    except Exception as e:
        print(f"Error fetching course detail {course_id}: {e}")
        return {'description': '', 'reviews': []}

def convert_to_course_format(course: Dict, detail: Dict, index: int) -> Dict:
    """Convert to our course format"""
    # Map difficulty text to number
    difficulty_map = {
        '简单': 1.5,
        '中等': 3.0,
        '困难': 4.5
    }
    difficulty = difficulty_map.get(course['difficulty_text'], 3.0)
    
    # Map workload text to number
    workload_map = {
        '很少': 1,
        '中等': 3,
        '很多': 5
    }
    workload = workload_map.get(course['workload_text'], 3)
    
    # Map grade text to grade distribution
    grade_dist = {"A": 30, "B": 40, "C": 25, "D": 5}
    if course['grade_text'] == '超好':
        grade_dist = {"A": 50, "B": 35, "C": 12, "D": 3}
    elif course['grade_text'] == '一般':
        grade_dist = {"A": 25, "B": 40, "C": 28, "D": 7}
    
    # Determine department based on course name
    dept_map = [
        ('数学', '数学科学学院'),
        ('物理', '物理学院'),
        ('计算机', '计算机科学与技术学院'),
        ('程序设计', '计算机科学与技术学院'),
        ('电子', '信息科学技术学院'),
        ('电路', '信息科学技术学院'),
        ('信号', '信息科学技术学院'),
        ('化学', '化学与材料科学学院'),
        ('生物', '生命科学学院'),
        ('心理', '人文与社会科学学院'),
        ('历史', '人文与社会科学学院'),
        ('哲学', '人文与社会科学学院'),
        ('艺术', '人文学院'),
        ('油画', '人文学院'),
        ('音乐', '人文学院'),
        ('电影', '人文学院'),
        ('交响', '人文学院'),
        ('体育', '体育教学部'),
        ('英语', '外语系'),
        ('思政', '马克思主义学院'),
        ('政治', '马克思主义学院'),
    ]
    
    department = '未知学院'
    for keyword, dept in dept_map:
        if keyword in course['name']:
            department = dept
            break
    
    # Generate schedule (placeholder)
    days = [1, 2, 3, 4, 5]
    import random
    day = random.choice(days)
    start_hour = random.choice([8, 10, 14, 16, 19])
    end_hour = start_hour + 2
    
    return {
        "id": f"COURSE{index}",
        "code": f"C{1000+index}",
        "name": course['name'],
        "nameEn": course['name'],
        "department": department,
        "credits": random.choice([2, 3, 4]),
        "schedule": [
            {"day": day, "startTime": f"{start_hour:02d}:00", "endTime": f"{end_hour:02d}:00", "location": f"{random.randint(1,5)}-{random.randint(101,401)}"}
        ],
        "instructor": course['instructor'],
        "difficulty": difficulty,
        "workload": workload,
        "rating": course['rating'],
        "gradeDistribution": grade_dist,
        "reviews": detail['reviews'] if detail['reviews'] else [
            {"content": f"{course['instructor']}老师讲课很好，推荐！", "rating": 5, "author": "匿名", "date": "2024-01"},
            {"content": f"课程{course['difficulty_text']}，给分{course['grade_text']}", "rating": 5, "author": "学生", "date": "2024-01"}
        ],
        "tags": ["热门"] if course['rating'] >= 9.5 else [],
        "description": detail['description'][:200] if detail['description'] else f"{course['name']}课程，由{course['instructor']}老师主讲。"
    }

def main():
    """Main function to scrape courses"""
    print("开始爬取 icourse.club 课程数据...")
    
    all_courses = []
    
    # Fetch top 5 pages (50 courses)
    for page in range(1, 6):
        print(f"正在爬取第 {page} 页...")
        courses = fetch_course_list(page)
        print(f"  找到 {len(courses)} 门课程")
        
        for i, course in enumerate(courses):
            print(f"  正在获取 {course['name']} 的详细信息...")
            detail = fetch_course_detail(course['id'])
            formatted = convert_to_course_format(course, detail, len(all_courses) + 1)
            all_courses.append(formatted)
            time.sleep(1)  # Be nice to the server
        
        time.sleep(2)
    
    # Generate Python file
    output = '''courses = [
'''
    
    for course in all_courses:
        output += f'''    {json.dumps(course, ensure_ascii=False, indent=4)},
'''
    
    output += ''']

def get_all_courses():
    """Get all available courses"""
    return courses

def get_course_by_id(course_id):
    """Get a course by its ID"""
    for course in courses:
        if course["id"] == course_id:
            return course
    return None

def get_courses_by_department(department):
    """Get courses by department"""
    return [c for c in courses if department in c["department"]]

def get_courses_by_tag(tag):
    """Get courses by tag"""
    return [c for c in courses if tag in c["tags"]]

def search_courses(keyword):
    """Search courses by keyword"""
    keyword = keyword.lower()
    return [c for c in courses if 
            keyword in c["name"].lower() or
            keyword in c["nameEn"].lower() or
            keyword in c["description"].lower() or
            any(keyword in tag.lower() for tag in c["tags"])]
'''
    
    with open('courses_generated.py', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"\n完成！共爬取 {len(all_courses)} 门课程")
    print("数据已保存到 courses_generated.py")

if __name__ == "__main__":
    main()
