"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# Path函数来实现注解
from fastapi import FastAPI, Path
app = FastAPI()

@app.get("/")
async def root():
    return{"msg": "Hello World"}

# 定义了路径参数id: URL路径的一部分
"""
gt:greater than ge:greater than or equal
lt:less than    le:less than or equal

...:表示必须填入参数, gt/ge：大于/大于等于, lt/le：小于/小于等于
   description: 描述 max_length:最大长度 min_length:最小长度


"""
@app.get("/book/{id}")
# 传入到函数形参id 
async def get_book(id : int = Path(..., gt=0, lt= 101, description="书籍id,范围1-100")): 
    # 返回字典框架
    return{"id" : id, "title": f"这是第{id}本数书"}

# 需求，茶轴书籍的作者，路径参数name，长度范围2-10
# gt lr 不能使用到str
@app.get("/author/{name}")
async def get_name(name: str = Path(...,min_length = 2, max_length = 10, description="输入书籍名字,长度范围2-10")):
    return{"msg": f"这是{name}的信息"}


# 案例
@app.get("/news/{id}/")
async def get_news_id(id : int = Path(..., gt=0, lt= 101, description="请输入你的id，范围1-100")): 
    return{"id" : id, "title": f"新闻分类id是{id}"}

@app.get("/news/{name}")
async def get_news_name(name: str = Path(...,min_length = 2, max_length = 10, description="请输入新闻分类名称,长度范围2-10")):
    return{"msg": f"新闻分类名称是{name}"}