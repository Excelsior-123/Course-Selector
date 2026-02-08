# 智能选课助手 (Course Selector Assistant)

A full-stack H5 web application that helps university students select courses using natural language input and AI-powered recommendations.

![Screenshot](https://via.placeholder.com/800x600/667eea/ffffff?text=Course+Selector+App)

## 🌟 Features

- 🤖 **Natural Language Input** - Describe your preferences in plain Chinese
- 🎯 **AI-Powered Recommendations** - Uses MiniMax-M2.1 via Anthropic SDK
- 📅 **Smart Schedule Generation** - Automatic conflict detection and optimization
- 📱 **Mobile-First H5 Design** - Beautiful, responsive interface
- ⭐ **Course Reviews & Ratings** - Simulated USTC icourse.club data
- 📊 **Visual Timetable** - Color-coded weekly schedule view

## 🚀 Live Demo

**Deployed URL**: [Your deployment URL will be here]

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Vanilla HTML/JS + Tailwind CSS |
| Backend | Python FastAPI |
| AI Model | MiniMax-M2.1 (via Anthropic SDK) |
| Data | JSON Mock Database |

## 📁 Project Structure

```
course-selector/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── frontend/dist/          # Static frontend files
│   ├── data/
│   │   ├── __init__.py
│   │   └── courses.py          # 20 mock courses with reviews
│   └── services/
│       ├── __init__.py
│       ├── ai.py               # MiniMax-M2.1 integration
│       └── scheduler.py        # Schedule optimization algorithm
├── frontend/dist/
│   └── index.html              # Single-page application
├── Dockerfile                  # Container config
├── railway.json                # Railway deployment config
├── render.yaml                 # Render deployment config
└── README.md
```

## 🚦 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/course-selector.git
cd course-selector
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the server**
```bash
python main.py
```

5. **Open your browser**
Navigate to `http://localhost:3000`

## ☁️ Deployment

### Option 1: Railway (Recommended)

1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard:
   - `ANTHROPIC_API_KEY`
   - `ANTHROPIC_BASE_URL`
4. Deploy!

```bash
# Using Railway CLI
railway login
railary link
railway up
```

### Option 2: Render

1. Push code to GitHub
2. Create new Web Service on Render
3. Select Python environment
4. Add environment variables
5. Deploy!

```bash
# Using Render CLI
render deploy
```

### Option 3: Docker

```bash
docker build -t course-selector .
docker run -p 3000:3000 \
  -e ANTHROPIC_API_KEY=your_key \
  -e ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic \
  course-selector
```

## 🔌 API Endpoints

### POST /api/recommend
Get AI-powered course recommendations

**Request:**
```json
{
  "input": "我对计算机网络感兴趣，希望上午上课，选一门给分高的体育课"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "preferences": { ... },
    "summary": "AI生成的推荐总结...",
    "schedule": {
      "courses": [ ... ],
      "stats": {
        "courseCount": 5,
        "totalCredits": 14,
        "averageRating": 4.2,
        "averageDifficulty": 2.8
      }
    },
    "grid": [ ... ]
  }
}
```

### GET /api/courses
Get all courses with optional filters

```
GET /api/courses?department=计算机学院&tag=水课&search=网络
```

### GET /api/courses/{id}
Get specific course details

### GET /api/filters
Get available departments and tags

## 📱 Screenshots

### Input Screen
Users can enter natural language preferences like:
- "我对计算机网络感兴趣，希望上午9点到下午6点上课"
- "想找给分高的水课，作业少好拿A"
- "周二周四晚上有空的体育课"

### Results Screen
- AI-generated recommendation summary
- Visual weekly timetable with color-coded courses
- Expandable course cards with reviews, ratings, grade distribution

## 🎓 Sample Courses

The app includes 20 realistic mock courses:

| Course | Code | Dept | Difficulty | Grade A% |
|--------|------|------|------------|----------|
| 计算机网络 | CS101 | CS | 3.5 | 25% |
| 数据结构与算法 | CS102 | CS | 4.5 | 20% |
| 操作系统 | CS103 | CS | 4.8 | 15% |
| 高等数学A | MATH101 | Math | 4.0 | 20% |
| 线性代数 | MATH201 | Math | 3.5 | 30% |
| 篮球 | PE101 | PE | 1.5 | 80% |
| 游泳 | PE102 | PE | 2.0 | 70% |
| 羽毛球 | PE103 | PE | 2.0 | 75% |
| ... | ... | ... | ... | ... |

## 🔐 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | - | MiniMax API key |
| `ANTHROPIC_BASE_URL` | No | https://api.minimaxi.com/anthropic | API base URL |
| `PORT` | No | 3000 | Server port |

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Course data inspired by USTC icourse.club
- AI powered by MiniMax-M2.1
- Icons from Lucide

---

Built with ❤️ for university students everywhere