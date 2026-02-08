FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY frontend/dist/ ./frontend/dist/

WORKDIR /app/backend

ENV PYTHONUNBUFFERED=1
ENV PORT=3000

EXPOSE 3000

CMD ["python", "main.py"]