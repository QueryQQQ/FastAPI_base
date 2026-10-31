"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示请求体参数中使用Field函数来限制参数内容和描述
from fastapi import FastAPI
from pydantic import BaseModel,Field


app = FastAPI()

@app.get("/")
async def root():
    return{"msg": "Hello World"}

# 1.定义类型
# 注册：用户名和密码:str
# 用field函数实现类型注解
class User(BaseModel):# User继承了基类Basemodel
    username: str = Field(default="张三", min_length=2, max_length=10,description="用户名，长度要求2-10个字符")
    password: str = Field(min_length=3, max_length=20)

# 2.类型注解
# 存储的信息放在包里面，不在URL地址
@app.post("/register")
async def register(user: User):
    return user

# 练习 需求：设计接口新增图书
# 图书信息包含：书名、作者、出版社、售价

class Book(BaseModel):
    bookname: str = Field(..., min_length=2, max_length=20)
    author: str = Field(min_length=2, max_length=20)
    publisher: str = Field(default="黑心出版社")
    price: int = Field(..., gt = 0) 

@app.post("/book")
async def book_add(book: Book):
    return book
    