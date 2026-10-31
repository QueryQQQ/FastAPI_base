"""FastAPI 项目入口。
运行：
    uvicorn app.main:app --reload
"""
# 演示聚合查询操作

# 标准库
from datetime import datetime
from typing import AsyncGenerator
# web框架
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import DateTime, Float, String, func, select
from pydantic import BaseModel
# ORM
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 创建实例，在这里相当于创建注册表容器
app = FastAPI()

# 1.创建异步引擎（数据库引擎）
# 方言+驱动://用户:密码@主机:端口/库名?参数
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8mb4"
# 建立引擎对象async_engine，相当于链接的属性
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,          # 可选，用于输出SQL日志
    pool_size=10,       # 设置连接池活跃的连接数
    max_overflow=20,    # 允许的额外链接数
)

# 2.定义模型类： 基类+表对应的模型类
# 先创建基类，所有表都需要的功能
# 基类： 创建时间，更新时间；
class Base(DeclarativeBase):  # 继承DeclarativeBase类
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), comment="修改时间"
    )

# 定义模型类
# 书籍表：id，书名，作者，简介，出版社
class Book(Base):
    __tablename__ = "book" # 数据表名

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str | None] = mapped_column(String(255), comment="出版社")

# 3.建表：定义函数建表 FastAPI启动时会调用的函数
async def create_tables():
    # 获取异步引擎，创建事务，建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# 将建表挂到应用启动事件上，在unicorn接受请求前执行一次
@app.on_event("startup")
async def start_event():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# 需求：查询功能的接口，查询图书。依赖注入：创建依赖项获取数据库会话 + Depends 注入路由处理函数
# 创建异步会话工厂
# 每次调用就会创建出一个会话（session）实例
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,          # 绑定数据库引擎
    class_=AsyncSession,        # 指定会话类
    expire_on_commit=False,     # 提交后会话不会过期，不会重新查询数据库
)

# 依赖项：每个请求进来开一个会话，请求结束自动关闭
async def get_database() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# 演示数据库新增数据的操作
# 需求：用户输入图书信息（id，书名，作者，价格，出版社）-> 新增
# 用户输入 -> 参数 -> 请求体

class BookBase(BaseModel):
    id:         int
    bookname:   str
    author:     str
    price:      float
    publisher:  str


#post添加，get查询
@app.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession = Depends(get_database)):
    # ORM对象 -> add -> commit
    book_obj = Book(**book.__dict__)
    db.add(book_obj)
    await db.commit()
    return book


# 演示数据库更新数据的操作
# 需求，先查再改
class BookUpdate(BaseModel):
    bookname:  str
    author:    str
    price:     float
    publisher: str

@app.put("/book/update_book")
# 定义请求体参数：定义新数据
async def update_book(book_id: int, data: BookUpdate, db: AsyncSession = Depends(get_database)):
    db_book = await db.get(Book, book_id) # 查询
    if db_book is None: # 定义没查到的情况
        raise HTTPException( # raise报异常
            status_code = 404,
            detail = "查无此书"
        )

    db_book.bookname = data.bookname
    db_book.author = data.author
    db_book.price = data.price
    db_book.publisher = data.publisher

    await db.commit()
    return db_book
    
# 演示数据库删除数据的操作
# 查询get -> delete删除 -> commit提交
@app.delete("/book/delete_book")
# 定义请求体参数：定义新数据
async def delete_book(book_id: int, db: AsyncSession = Depends(get_database)):
    # 先查再删
    db_book = await db.get(Book, book_id) 
    
    if db_book is None: # 定义没查到的情况
        raise HTTPException( # raise报异常
            status_code = 404,
            detail = "查无此书"
        )

    await db.delete(db_book)
    await db.commit()
    return {"message": "删除图书成功"}
