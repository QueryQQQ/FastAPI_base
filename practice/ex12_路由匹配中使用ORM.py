"""FastAPI 项目入口。
运行：
    uvicorn app.main:app --reload
"""
# 演示在路由匹配中使用ORM
# 核心：创建依赖项，使用Depends注入处理函数

# 标准库
from datetime import datetime
from typing import AsyncGenerator
# web框架
from fastapi import Depends, FastAPI, Query
from sqlalchemy import DateTime, Float, String, func, select
# ORM
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

"""
1.uvicorn 启动：先把整个 .py 当普通脚本从上往下跑一遍
2.搭静态结构 
app = FastAPI()   create_async_engine(...)
class Book(Base)  @app.get("/books")
3.startup 事件触发:create_tables()
4.启动完成开始监听 127.0.0.1:8000
5.await db.scalars(stmt)发出请求并挂起
6.python协程挂起，执行SQL语句，将结果回传。 
7.scalars()从返回的结果取值，并组成列表输出。
8.返回结果
"""


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
    # mapped就是类型注解检查器+ORM元类（class定义完成的一瞬间执行的代码）
    # datetime python类型
    # mapped_column 列配置构造器，返回一个配置对象
    # func.now()SQL函数表达式，SQLAlchemy → 渲染成 now()
    # onupdate ORM 更新时自动刷新
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
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/books")
async def list_books(
    db: AsyncSession = Depends(get_db), # 依赖注入，需要调用get_db
    keyword: str | None = Query(None, description="按书名模糊查询"), # 查询参数
):
    stmt = select(Book) # 构造一个select对象
    if keyword: # 如果有关键词，就用.where返回一个带条件的查询
        # .like构造一个条件表达式
        # 两个 % 是 SQL 的通配符，含义是"keyword前面可以有任意字符，后面也可以有任意字符"。
        stmt = stmt.where(Book.bookname.like(f"%{keyword}%"))
    # 发送请求，之前全在本地运行，awit之后才是网络IO
    # 分组括号()，强制先算括号内得到ScalarResult，再.all()
    # await挂起行程，AsyncSession实例db，由Depends(get_db)达到，代表一次数据库对话
    # AsyncSession的方法.scalars，作用把每行的第一列剥出来
    # (stmt)传入测参数，目前为纯Python数据
    # .all全部执行
    books = (await db.scalars(stmt)).all() 
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
        for b in books # 将数据遍历成dict形式输出
    ]
