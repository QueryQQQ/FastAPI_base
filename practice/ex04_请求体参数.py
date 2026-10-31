"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示请求体参数写法
# 请求体参数作用： 创建、更新资源
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def root():
    return{"msg": "Hello World"}

# 1.定义类型
# 注册：用户名和密码:str
class User(BaseModel):# User继承了基类Basemodel
    username: str
    password: str

# 2.类型注解
# 存储的信息放在包里面，不在URL地址
@app.post("/register")
async def register(user: User):
    return user


# 练习 需求：设计接口新增图书   
# 图书信息包含：书名、作者、出版社、售价

class Book(BaseModel):
    bookname: str
    author: str
    publisher: str
    price: int

@app.post("/book")
async def book_add(book: Book):
    return book
    