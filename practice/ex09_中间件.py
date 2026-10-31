"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示如何使用HTTPException进行异常处理
# 中间件是一个每次请求进入FastAPI应用是都会被执行的函数
# 中间件作用：为每个请求添加统一的处理逻辑（记录日志，身份认证等）
from urllib import response
from fastapi import FastAPI,HTTPException

app = FastAPI()

@app.get("/")
async def root():
    return{"message": "Hello World"}

# 需求：按id查询新闻 1-6

@app.middleware("http")
# async代表异步函数，真正的异步代码要写在await后面
async def middelware1(request, call_next):# (请求,传递请求的函数名)
    print("中间件1 start")
    # 等待请求 response存储响应结果
    response = await call_next(request)
    print("中间件1 end")
    return response

# 中间件执行顺序：从下往上
@app.middleware("http")
# async代表异步函数，真正的异步代码要写在await后面
async def middelware2(request, call_next):
    print("中间件2 start")
    # 等待请求 response存储响应结果
    response = await call_next(request)
    print("中间件2 end")
    return response
