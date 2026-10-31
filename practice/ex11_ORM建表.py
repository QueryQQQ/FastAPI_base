"""FastAPI 项目入口。
运行：
    uvicorn app.main:app --reload
"""
# 演示ORM（对象关系映射Mapping）建表
# ORM主要是在编程语言和关系型数据库之间建立映射
# 先安装驱动
# python -m pip install "sqlalchemy[asyncio]" aiomysql,指定python不容易装错
from traceback import print_exception
from fastapi import FastAPI,Query,Depends
from sqlalchemy import DateTime 
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func
from sqlalchemy import String
from sqlalchemy import Float


app = FastAPI()

# 1.创建异步引擎（数据库引擎）
# 语言+驱动://用户:密码@主机:端口/库名?参数
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8"# 数据库地址
# 建立引擎对象async_engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True, # 可选，用于输出SQL日志
    pool_size = 10,# 设置连接池活跃的连接数
    max_overflow = 20# 允许的额外链接数
)

# 2.定义模型类： 基类+表对应的模型类
# 先创建基类，所有表都需要的功能
# 基类： 创建时间，更新时间，书记表：id，书名，作者，介个，出版社
class Base(DeclarativeBase):# 继承DeclarativeBase类
    # 带括号是数据库为主，不带的是python为主
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,onupdate=func.now,comment="修改时间")
# 定义模型类
class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255),comment="书名")
    author: Mapped[str] = mapped_column(String(255),comment="作者")
    price: Mapped[float] = mapped_column(Float,comment="价格")
    publisher: Mapped[float] = mapped_column(String(255),comment="出版社")

# 3.建表：定义函数建表 FastAPI启动时会调用的函数
async def create_tables():
    # 获取异步引擎，创建事务，建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def start_event():
    await create_tables()


@app.get("/")
async def root():   
    return{"message": "Hello World"}

