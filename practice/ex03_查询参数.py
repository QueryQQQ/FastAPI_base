"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 查询参数来实现查询数据(引入query函数)
from fastapi import FastAPI, Query
app = FastAPI()

@app.get("/")
async def root():
    return{"msg": "Hello World"}

# 需求 查询新闻 分页skip：跳过的记录数，limit: 返回的记录数 10
# 查询参数出现在URL？之后，k1=v1&k2=v2

@app.get("/news_news_list")
async def get_news_list(
    # 最前面的数字代表默认值
    skip: int = Query(0, description="跳过的记录数", lt = 100),
    limit: int = Query(10, description= "返回的记录数")
):
    return {"skip": skip, "limit": limit}

# 练习
# 需求：设计接口查询图书，要求携带两个查询参数：图书分类和价格
# 图书分类：默认值为 Python开发，长度限制 5 ~ 255
# 价格：限制大小范围 50 ~ 100

@app.get("/news_books_list")
async def get_books_list(
    type: str = Query(0, description="请输入要查询的图书分类，长度5-255", min_length= 5, max_length= 256),
    price: int = Query(10, description= "请输入要查询的图书价格，范围50-100", gt = 49, lt = 101)
):
    return {"type": type, "price": price}