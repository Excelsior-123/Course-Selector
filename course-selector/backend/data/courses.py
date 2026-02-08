courses = [
    {
        "id": "CS101",
        "code": "CS101",
        "name": "计算机网络",
        "nameEn": "Computer Networks",
        "department": "计算机科学与技术学院",
        "credits": 3,
        "schedule": [
            {"day": 1, "startTime": "08:00", "endTime": "09:35", "location": "3A-201"},
            {"day": 3, "startTime": "08:00", "endTime": "09:35", "location": "3A-201"}
        ],
        "instructor": "张教授",
        "difficulty": 3.5,
        "workload": 3,
        "rating": 4.2,
        "gradeDistribution": {"A": 25, "B": 45, "C": 25, "D": 5},
        "reviews": [
            {"content": "讲课清晰，实验有意思，推荐！", "rating": 5, "author": "匿名用户", "date": "2024-01"},
            {"content": "考试有点难，但学到很多", "rating": 4, "author": "CS学生", "date": "2023-12"},
            {"content": "作业量适中，给分还不错", "rating": 4, "author": "大三学生", "date": "2023-12"}
        ],
        "tags": ["专业课", "理论+实验", "热门"],
        "description": "本课程介绍计算机网络的基本原理、协议和应用。"
    },
    {
        "id": "CS102",
        "code": "CS102",
        "name": "数据结构与算法",
        "nameEn": "Data Structures and Algorithms",
        "department": "计算机科学与技术学院",
        "credits": 4,
        "schedule": [
            {"day": 2, "startTime": "09:45", "endTime": "12:10", "location": "3B-105"},
            {"day": 4, "startTime": "09:45", "endTime": "12:10", "location": "3B-105"}
        ],
        "instructor": "李教授",
        "difficulty": 4.5,
        "workload": 5,
        "rating": 4.5,
        "gradeDistribution": {"A": 20, "B": 40, "C": 30, "D": 10},
        "reviews": [
            {"content": "硬核课程，打好基础很重要", "rating": 5, "author": "ACM队员", "date": "2024-01"},
            {"content": "作业很多但很有价值", "rating": 4, "author": "软工学生", "date": "2023-12"},
            {"content": "老师讲得非常好，就是考试难", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["核心课", "编程", "难但值得"],
        "description": "计算机科学核心课程，涵盖基本数据结构和算法设计与分析。"
    },
    {
        "id": "CS103",
        "code": "CS103",
        "name": "操作系统",
        "nameEn": "Operating Systems",
        "department": "计算机科学与技术学院",
        "credits": 4,
        "schedule": [
            {"day": 1, "startTime": "14:00", "endTime": "16:25", "location": "3A-301"},
            {"day": 3, "startTime": "14:00", "endTime": "16:25", "location": "3A-301"}
        ],
        "instructor": "王教授",
        "difficulty": 4.8,
        "workload": 5,
        "rating": 4.0,
        "gradeDistribution": {"A": 15, "B": 35, "C": 35, "D": 15},
        "reviews": [
            {"content": "OS课地狱难度，但真的能学到东西", "rating": 4, "author": "系统方向", "date": "2024-01"},
            {"content": "lab很难，建议提前预习", "rating": 3, "author": "匿名", "date": "2023-12"},
            {"content": "给分一般，但内容很实用", "rating": 4, "author": "研究生", "date": "2023-11"}
        ],
        "tags": ["核心课", "系统", "高难度"],
        "description": "深入讲解操作系统原理，包括进程管理、内存管理、文件系统等。"
    },
    {
        "id": "MATH101",
        "code": "MATH101",
        "name": "高等数学A",
        "nameEn": "Advanced Mathematics A",
        "department": "数学科学学院",
        "credits": 5,
        "schedule": [
            {"day": 1, "startTime": "08:00", "endTime": "09:35", "location": "5-101"},
            {"day": 2, "startTime": "08:00", "endTime": "09:35", "location": "5-101"},
            {"day": 4, "startTime": "08:00", "endTime": "09:35", "location": "5-101"}
        ],
        "instructor": "陈教授",
        "difficulty": 4.0,
        "workload": 4,
        "rating": 3.8,
        "gradeDistribution": {"A": 20, "B": 40, "C": 30, "D": 10},
        "reviews": [
            {"content": "基础课必须学好", "rating": 4, "author": "大一新生", "date": "2024-01"},
            {"content": "老师板书很清晰", "rating": 4, "author": "物理系", "date": "2023-12"},
            {"content": "考试难度适中", "rating": 3, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["基础课", "必修", "数学"],
        "description": "微积分、级数、微分方程等高等数学内容。"
    },
    {
        "id": "MATH201",
        "code": "MATH201",
        "name": "线性代数",
        "nameEn": "Linear Algebra",
        "department": "数学科学学院",
        "credits": 3,
        "schedule": [
            {"day": 2, "startTime": "14:00", "endTime": "16:25", "location": "5-203"},
            {"day": 5, "startTime": "08:00", "endTime": "09:35", "location": "5-203"}
        ],
        "instructor": "刘教授",
        "difficulty": 3.5,
        "workload": 3,
        "rating": 4.1,
        "gradeDistribution": {"A": 30, "B": 45, "C": 20, "D": 5},
        "reviews": [
            {"content": "工科必修课，老师讲得不错", "rating": 4, "author": "机械系", "date": "2024-01"},
            {"content": "作业量合适，给分 generous", "rating": 5, "author": "电子系", "date": "2023-12"},
            {"content": "概念有点抽象，需要多理解", "rating": 3, "author": "大一", "date": "2023-11"}
        ],
        "tags": ["基础课", "数学", "水课推荐"],
        "description": "矩阵理论、向量空间、线性变换等线性代数基础。"
    },
    {
        "id": "PE101",
        "code": "PE101",
        "name": "篮球",
        "nameEn": "Basketball",
        "department": "体育教学部",
        "credits": 1,
        "schedule": [
            {"day": 2, "startTime": "19:00", "endTime": "20:35", "location": "东区体育馆"}
        ],
        "instructor": "赵教练",
        "difficulty": 1.5,
        "workload": 1,
        "rating": 4.5,
        "gradeDistribution": {"A": 80, "B": 15, "C": 5, "D": 0},
        "reviews": [
            {"content": "给分超高，老师人很好", "rating": 5, "author": "篮球爱好者", "date": "2024-01"},
            {"content": "轻松拿A，推荐", "rating": 5, "author": "宅男", "date": "2023-12"},
            {"content": "可以锻炼身体，还能认识朋友", "rating": 4, "author": "大一", "date": "2023-11"}
        ],
        "tags": ["体育课", "水课", "给分高"],
        "description": "篮球基本技术与战术，体能训练。"
    },
    {
        "id": "PE102",
        "code": "PE102",
        "name": "游泳",
        "nameEn": "Swimming",
        "department": "体育教学部",
        "credits": 1,
        "schedule": [
            {"day": 3, "startTime": "19:00", "endTime": "20:35", "location": "游泳馆"},
            {"day": 5, "startTime": "19:00", "endTime": "20:35", "location": "游泳馆"}
        ],
        "instructor": "钱教练",
        "difficulty": 2.0,
        "workload": 1,
        "rating": 4.3,
        "gradeDistribution": {"A": 70, "B": 20, "C": 8, "D": 2},
        "reviews": [
            {"content": "学会了游泳，很有成就感", "rating": 5, "author": "旱鸭子", "date": "2024-01"},
            {"content": "水质不错，教练耐心", "rating": 4, "author": "匿名", "date": "2023-12"},
            {"content": "有点冷，但给分好", "rating": 4, "author": "南方同学", "date": "2023-11"}
        ],
        "tags": ["体育课", "实用技能", "给分高"],
        "description": "游泳基本技术，安全知识。"
    },
    {
        "id": "PE103",
        "code": "PE103",
        "name": "羽毛球",
        "nameEn": "Badminton",
        "department": "体育教学部",
        "credits": 1,
        "schedule": [
            {"day": 4, "startTime": "19:00", "endTime": "20:35", "location": "羽毛球馆"}
        ],
        "instructor": "孙教练",
        "difficulty": 2.0,
        "workload": 1,
        "rating": 4.4,
        "gradeDistribution": {"A": 75, "B": 20, "C": 4, "D": 1},
        "reviews": [
            {"content": "老师很专业，学到很多技巧", "rating": 5, "author": "羽球爱好者", "date": "2024-01"},
            {"content": "轻松愉快，给分好", "rating": 5, "author": "初学者", "date": "2023-12"},
            {"content": "场地有点紧张", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["体育课", "水课", "给分高"],
        "description": "羽毛球基本技术与战术。"
    },
    {
        "id": "ENG101",
        "code": "ENG101",
        "name": "大学英语III",
        "nameEn": "College English III",
        "department": "外语系",
        "credits": 2,
        "schedule": [
            {"day": 1, "startTime": "10:00", "endTime": "11:35", "location": "外语楼-301"},
            {"day": 3, "startTime": "10:00", "endTime": "11:35", "location": "外语楼-301"}
        ],
        "instructor": "Smith老师",
        "difficulty": 2.5,
        "workload": 2,
        "rating": 3.9,
        "gradeDistribution": {"A": 35, "B": 40, "C": 20, "D": 5},
        "reviews": [
            {"content": "外教课，练习口语的好机会", "rating": 4, "author": "英语爱好者", "date": "2024-01"},
            {"content": "作业不多，但课堂参与重要", "rating": 4, "author": "匿名", "date": "2023-12"},
            {"content": "给分一般，气氛轻松", "rating": 3, "author": "理工男", "date": "2023-11"}
        ],
        "tags": ["语言课", "外教", "口语"],
        "description": "提高英语听说读写能力，注重口语交流。"
    },
    {
        "id": "PHYS101",
        "code": "PHYS101",
        "name": "大学物理A",
        "nameEn": "College Physics A",
        "department": "物理学院",
        "credits": 4,
        "schedule": [
            {"day": 2, "startTime": "10:00", "endTime": "11:35", "location": "2-201"},
            {"day": 4, "startTime": "10:00", "endTime": "11:35", "location": "2-201"},
            {"day": 5, "startTime": "14:00", "endTime": "16:25", "location": "物理实验室"}
        ],
        "instructor": "周教授",
        "difficulty": 4.0,
        "workload": 4,
        "rating": 3.7,
        "gradeDistribution": {"A": 18, "B": 38, "C": 32, "D": 12},
        "reviews": [
            {"content": "物理基础很重要，老师讲得细", "rating": 4, "author": "物理竞赛生", "date": "2024-01"},
            {"content": "实验报告很多", "rating": 3, "author": "工科生", "date": "2023-12"},
            {"content": "考试比较难", "rating": 3, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["基础课", "理科", "实验多"],
        "description": "力学、热学、电磁学等大学物理基础。"
    },
    {
        "id": "CS201",
        "code": "CS201",
        "name": "数据库系统",
        "nameEn": "Database Systems",
        "department": "计算机科学与技术学院",
        "credits": 3,
        "schedule": [
            {"day": 1, "startTime": "19:00", "endTime": "21:25", "location": "3A-205"}
        ],
        "instructor": "吴教授",
        "difficulty": 3.0,
        "workload": 3,
        "rating": 4.3,
        "gradeDistribution": {"A": 30, "B": 45, "C": 20, "D": 5},
        "reviews": [
            {"content": "很实用，项目必备", "rating": 5, "author": "软工学生", "date": "2024-01"},
            {"content": "SQL练熟了就简单了", "rating": 4, "author": "匿名", "date": "2023-12"},
            {"content": "给分不错，推荐", "rating": 4, "author": "大四", "date": "2023-11"}
        ],
        "tags": ["专业课", "实用", "数据库"],
        "description": "数据库设计原理、SQL、事务处理等。"
    },
    {
        "id": "CS202",
        "code": "CS202",
        "name": "软件工程",
        "nameEn": "Software Engineering",
        "department": "计算机科学与技术学院",
        "credits": 3,
        "schedule": [
            {"day": 3, "startTime": "19:00", "endTime": "21:25", "location": "3A-207"}
        ],
        "instructor": "郑教授",
        "difficulty": 2.5,
        "workload": 3,
        "rating": 3.5,
        "gradeDistribution": {"A": 40, "B": 40, "C": 15, "D": 5},
        "reviews": [
            {"content": "小组项目多，实践性强", "rating": 4, "author": "PM方向", "date": "2024-01"},
            {"content": "理论有点枯燥", "rating": 3, "author": "技术宅", "date": "2023-12"},
            {"content": "给分很好", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["专业课", "团队协作", "项目制"],
        "description": "软件开发流程、项目管理、敏捷开发等。"
    },
    {
        "id": "ART101",
        "code": "ART101",
        "name": "西方艺术史",
        "nameEn": "History of Western Art",
        "department": "人文学院",
        "credits": 2,
        "schedule": [
            {"day": 2, "startTime": "19:00", "endTime": "20:35", "location": "人文楼-101"}
        ],
        "instructor": "黄教授",
        "difficulty": 1.5,
        "workload": 1,
        "rating": 4.6,
        "gradeDistribution": {"A": 60, "B": 30, "C": 8, "D": 2},
        "reviews": [
            {"content": "超级水课，给分超高", "rating": 5, "author": "理科生", "date": "2024-01"},
            {"content": "老师讲课很有趣", "rating": 5, "author": "艺术爱好者", "date": "2023-12"},
            {"content": "期末开卷，轻松拿A", "rating": 5, "author": "刷分党", "date": "2023-11"}
        ],
        "tags": ["通识课", "水课", "人文"],
        "description": "西方艺术发展历史，名画赏析。"
    },
    {
        "id": "ART102",
        "code": "ART102",
        "name": "电影赏析",
        "nameEn": "Film Appreciation",
        "department": "人文学院",
        "credits": 2,
        "schedule": [
            {"day": 4, "startTime": "19:00", "endTime": "21:25", "location": "人文楼-多媒体教室"}
        ],
        "instructor": "林教授",
        "difficulty": 1.5,
        "workload": 1,
        "rating": 4.7,
        "gradeDistribution": {"A": 65, "B": 25, "C": 8, "D": 2},
        "reviews": [
            {"content": "看电影就能拿学分", "rating": 5, "author": "电影迷", "date": "2024-01"},
            {"content": "老师点评很专业", "rating": 5, "author": "匿名", "date": "2023-12"},
            {"content": "期末交影评，超简单", "rating": 5, "author": "懒人", "date": "2023-11"}
        ],
        "tags": ["通识课", "水课", "给分高"],
        "description": "经典电影赏析，电影理论与批评。"
    },
    {
        "id": "ECON101",
        "code": "ECON101",
        "name": "经济学原理",
        "nameEn": "Principles of Economics",
        "department": "管理学院",
        "credits": 3,
        "schedule": [
            {"day": 1, "startTime": "14:00", "endTime": "16:25", "location": "管理楼-301"},
            {"day": 5, "startTime": "10:00", "endTime": "11:35", "location": "管理楼-301"}
        ],
        "instructor": "徐教授",
        "difficulty": 2.5,
        "workload": 2,
        "rating": 4.0,
        "gradeDistribution": {"A": 35, "B": 40, "C": 20, "D": 5},
        "reviews": [
            {"content": "经济学入门，很有意思", "rating": 4, "author": "工科生", "date": "2024-01"},
            {"content": "老师讲课生动", "rating": 4, "author": "双学位", "date": "2023-12"},
            {"content": "考试难度适中", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["通识课", "经管", "热门"],
        "description": "微观经济学与宏观经济学基础。"
    },
    {
        "id": "CS203",
        "code": "CS203",
        "name": "人工智能导论",
        "nameEn": "Introduction to AI",
        "department": "计算机科学与技术学院",
        "credits": 3,
        "schedule": [
            {"day": 2, "startTime": "14:00", "endTime": "16:25", "location": "3C-101"},
            {"day": 5, "startTime": "14:00", "endTime": "15:35", "location": "3C-101"}
        ],
        "instructor": "杨教授",
        "difficulty": 3.5,
        "workload": 3,
        "rating": 4.4,
        "gradeDistribution": {"A": 28, "B": 42, "C": 22, "D": 8},
        "reviews": [
            {"content": "前沿内容，老师讲得好", "rating": 5, "author": "AI方向", "date": "2024-01"},
            {"content": "作业有挑战性但有趣", "rating": 4, "author": "大四", "date": "2023-12"},
            {"content": "需要一定数学基础", "rating": 4, "author": "转专业", "date": "2023-11"}
        ],
        "tags": ["专业课", "前沿", "AI"],
        "description": "人工智能基本概念、机器学习、深度学习入门。"
    },
    {
        "id": "CS204",
        "code": "CS204",
        "name": "Web开发技术",
        "nameEn": "Web Development",
        "department": "计算机科学与技术学院",
        "credits": 2,
        "schedule": [
            {"day": 3, "startTime": "19:00", "endTime": "21:25", "location": "机房-302"}
        ],
        "instructor": "马老师",
        "difficulty": 2.0,
        "workload": 2,
        "rating": 4.5,
        "gradeDistribution": {"A": 45, "B": 40, "C": 12, "D": 3},
        "reviews": [
            {"content": "实用技能，学完能自己做网站", "rating": 5, "author": "前端爱好者", "date": "2024-01"},
            {"content": "项目驱动，很有成就感", "rating": 5, "author": "软工", "date": "2023-12"},
            {"content": "给分很好", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["专业课", "实用", "前端"],
        "description": "HTML、CSS、JavaScript及现代Web框架。"
    },
    {
        "id": "STAT101",
        "code": "STAT101",
        "name": "概率论与数理统计",
        "nameEn": "Probability and Statistics",
        "department": "数学科学学院",
        "credits": 3,
        "schedule": [
            {"day": 1, "startTime": "10:00", "endTime": "11:35", "location": "5-301"},
            {"day": 3, "startTime": "10:00", "endTime": "11:35", "location": "5-301"}
        ],
        "instructor": "朱教授",
        "difficulty": 3.5,
        "workload": 3,
        "rating": 3.9,
        "gradeDistribution": {"A": 25, "B": 45, "C": 22, "D": 8},
        "reviews": [
            {"content": "机器学习必备基础", "rating": 4, "author": "数据科学", "date": "2024-01"},
            {"content": "概念有点抽象", "rating": 3, "author": "工科生", "date": "2023-12"},
            {"content": "考试难度适中", "rating": 4, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["基础课", "数学", "必修"],
        "description": "概率论基础、随机变量、统计推断。"
    },
    {
        "id": "PHIL101",
        "code": "PHIL101",
        "name": "哲学导论",
        "nameEn": "Introduction to Philosophy",
        "department": "人文学院",
        "credits": 2,
        "schedule": [
            {"day": 3, "startTime": "19:00", "endTime": "20:35", "location": "人文楼-201"}
        ],
        "instructor": "高教授",
        "difficulty": 2.0,
        "workload": 1,
        "rating": 4.2,
        "gradeDistribution": {"A": 50, "B": 35, "C": 12, "D": 3},
        "reviews": [
            {"content": "开阔思维，很有意思", "rating": 5, "author": "理科生", "date": "2024-01"},
            {"content": "老师讲课有深度", "rating": 4, "author": "哲学爱好者", "date": "2023-12"},
            {"content": "给分不错", "rating": 4, "author": "刷分党", "date": "2023-11"}
        ],
        "tags": ["通识课", "人文", "思维"],
        "description": "哲学基本问题与思维方法。"
    },
    {
        "id": "CHEM101",
        "code": "CHEM101",
        "name": "大学化学",
        "nameEn": "College Chemistry",
        "department": "化学与材料学院",
        "credits": 3,
        "schedule": [
            {"day": 2, "startTime": "08:00", "endTime": "09:35", "location": "化学楼-101"},
            {"day": 4, "startTime": "08:00", "endTime": "09:35", "location": "化学楼-101"}
        ],
        "instructor": "田教授",
        "difficulty": 3.0,
        "workload": 3,
        "rating": 3.6,
        "gradeDistribution": {"A": 22, "B": 40, "C": 28, "D": 10},
        "reviews": [
            {"content": "实验很有趣", "rating": 4, "author": "材料系", "date": "2024-01"},
            {"content": "理论有点枯燥", "rating": 3, "author": "外系", "date": "2023-12"},
            {"content": "给分一般", "rating": 3, "author": "匿名", "date": "2023-11"}
        ],
        "tags": ["基础课", "理科", "实验"],
        "description": "无机化学、有机化学基础。"
    }
]

def get_all_courses():
    return courses

def get_course_by_id(course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None

def get_courses_by_department(department):
    return [c for c in courses if department in c["department"]]

def get_courses_by_tag(tag):
    return [c for c in courses if tag in c["tags"]]