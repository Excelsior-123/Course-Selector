# 智能选课助手 - Render 部署指南

## 1. 创建 GitHub 仓库
```bash
cd /home/lyli/.openclaw/workspace/course-selector
git init
git add .
git commit -m "Initial commit"
# 然后去 GitHub 创建新仓库，再执行：
# git remote add origin https://github.com/你的用户名/course-selector.git
# git push -u origin main
```

## 2. Render.com 部署
1. 访问 https://dashboard.render.com
2. 点击 "New Web Service"
3. 选择 "Build and deploy from a Git repository"
4. 连接你的 GitHub 仓库
5. 配置如下：
   - **Name**: course-selector
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python main.py`
   - **Environment Variables**:
     - `ANTHROPIC_API_KEY`: `sk-api-nNHt79hIL5GSXj5DBHSGEhIPsNilUJQBORmHk7vMbLQ0Pkd7MBGluf36N_mix9gl-18cStiunbpljKGYE_tsVLjSVYKA8-FGe-5xZM4HT6QMiCnj4G1bkl4`
     - `ANTHROPIC_BASE_URL`: `https://api.minimaxi.com/anthropic`
     - `PORT`: `3000`
6. 点击 "Create Web Service"

## 3. 访问
部署完成后，Render 会给你一个类似 `https://course-selector-xxx.onrender.com` 的链接。

## 项目结构
```
course-selector/
├── backend/          # FastAPI 后端
│   ├── main.py
│   ├── data/courses.py
│   ├── services/ai.py
│   └── services/scheduler.py
├── frontend/         # H5 前端
│   └── dist/index.html
└── render.yaml       # Render 配置文件
```
