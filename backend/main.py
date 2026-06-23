from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


posts: list[dict] = [
{
      "id": 1,
      "title": "FastAPI 入门指南",
      "content": "FastAPI 是一个现代、快速的 Web 框架...",
      "author": "张三",
      "tags": ["python", "fastapi", "backend"],
      "published": True,
      "created_at": "2024-01-15T08:30:00Z",
      "views": 1250
    },
    {
      "id": 2,
      "title": "异步编程最佳实践",
      "content": "在 Python 中使用 async/await 可以显著提升性能...",
      "author": "李四",
      "tags": ["async", "performance"],
      "published": True,
      "created_at": "2024-03-22T14:15:00Z",
      "views": 890
    },
    {
      "id": 3,
      "title": "草稿：数据库设计模式",
      "content": "这是一篇尚未完成的文章...",
      "author": "张三",
      "tags": ["database", "design"],
      "published": False,
      "created_at": "2024-06-10T09:00:00Z",
      "views": 0
    }
  ]

@app.get("/", response_class=HTMLResponse)
def read_root():
    return f"<h1>欢迎来到我的博客！</h1><p>访问 <a href='/api/posts'>/api/posts</a> 获取文章列表。</p>"

@app.get("/api/posts")
def read_posts():
    return posts    