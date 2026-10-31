"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示如何自定义响应类型
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hello World"}

# 需求：新闻接口  响应数据格式id，title，content

class News(BaseModel):
    id: int
    title: str
    content: str

# response_model通过一个pydantic模型来约束API端点输出格式
@app.get("/news/{id}", response_model=News)
async def get_news(id: int):
    return{
        "id":id,
        "title":f"这是第{id}本书",
        "content": "这是一本好书"
    }
