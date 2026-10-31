"""FastAPI 项目入口。
运行：
    uvicorn app.main:app --reload
"""
# 演示数据库操作查询 116行

# 标准库
from datetime import datetime
from typing import AsyncGenerator
# web框架
from fastapi import Depends, FastAPI, Query
from sqlalchemy import DateTime, Float, String, func, select
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


@app.get("/books")
async def list_books(
    db: AsyncSession = Depends(get_database), # 依赖注入，需要调用get_db
    keyword: str | None = Query(None, description="按书名模糊查询"), # 查询参数
):
    stmt = select(Book) # 构造语句
    if keyword:
        stmt = stmt.where(Book.bookname.like(f"%{keyword}%"))

    books = (await db.scalars(stmt)).all() # 发送请求，之前全在本地运行，awit之后才是网络IO
    return [
        {
            "id": b.id,
            "bookname": b.bookname,
            "author": b.author,
            "price": b.price,
            "publisher": b.publisher,
            "create_time": b.create_time,
            "update_time": b.update_time,
        }
        for b in books
    ]

# 演示条件查询操作
# 1.比较判断 ==；>;<;<=;>=
# 2.模糊查询like()
# 3.与非查询 &；|； ~
# 4.包含查询in_()

# 1.比较判断
@app.get("/book/get_book/{book_id}")
async def get_book_list(book_id: int, db: AsyncSession = Depends(get_database)):
    result1 = await db.execute(select(Book).where(Book.id == book_id))
    book1 = result1.scalar_one_or_none()
    return book1

# 需求：条件 价格大于等于200
@app.get("/book/search_book")
async def get_search_book(db:AsyncSession = Depends(get_database)):
    result2 = await db.execute(select(Book).where(Book.price >= 200))
    book2 = result2.scalars().all()
    return book2

# 2.模糊查询
@app.get("/book/search_like_book")
async def get_search_like_book(db:AsyncSession = Depends(get_database)):
    # _限制字符数量，%不限制数量
    # result3 = await db.execute(select(Book).where(Book.author.like("曹_")))
    # 3.与非查询 &；|； ~
    # result3 = await db.execute(select(Book).where(Book.author.like("曹%") & (Book.price > 100)))

    # 需求： 书籍id列表，数据库里面的id如果在 书籍id列表里面，就返回
    # 包含查询in_()
    id_list = [1, 3, 5, 7]
    result3 = await db.execute(select(Book).where(Book.id.in_(id_list)))
    book3 = result3.scalars().all()
    return book3