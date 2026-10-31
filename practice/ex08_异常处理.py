"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示如何使用HTTPException进行异常处理
from fastapi import FastAPI,HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hello World"}

# 需求：按id查询新闻 1-6

@app.get("/news/{id}")
async def get_news(id: int):
    id_list = [1,2,3,4,5,6]
    if id not in id_list:
        # raise抛出异常信息
        raise HTTPException(status_code=404,detail="你查找的信息不存在")
    return{"id":id}
