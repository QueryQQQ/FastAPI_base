"""FastAPI 项目入口。
运行：
    uvicorn app.main:app --reload
"""
# 演示依赖注入系统
# 依赖注入系统与中间件区别：中间件是每个请求都会执行，依赖注入系统可以指定接口执行代码
# 2.调用depends
from mimetypes import common_types
from shutil import register_unpack_format

from fastapi import FastAPI,Query,Depends

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hello World"}

# 分页参数逻辑共用： 新闻列表和用户列表
# 1.创建依赖项
async def common_parameters(
        skip: int = Query(0, ge = 0),
        limit: int = Query(10, le =60)
):
    return{
        "skip": skip,
        "limit": limit
    }

@app.get("/news/news_list")
# 3.声明依赖项
async def get_news_list(commons=Depends(common_parameters)):
    return commons

@app.get("/user/user_list")
async def get_user_list(commmons=Depends(common_parameters)):
    return commmons