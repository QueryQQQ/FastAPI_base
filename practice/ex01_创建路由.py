from fastapi import FastAPI

# 创建fastAPI实例
# 后续所有装饰器在这里登记
app = FastAPI()

# 装饰器
# FastAPI实例.请求方法.请求路径 请求时执行下方函数
# 实现url地址和处理函数之间的映射关系
@app.get("/")
async def root():
    # 响应结果
    return {"message": "Hello World123"}


# 访问/hello 响应结果 msg：hello FastAPI        
@app.get("/hello")
async def get_hello():
    return {"msg":"hello FastAPI"}

# 路由定义  
# 路由就是URL地址和处理函数之间的映射关系
# 路由干什么：造一个路由对象，塞进app.routes里，将函数原样返回来

# 普通装饰器：名字被换掉了
# @my_decorator
# def plain(): return "原函数"

# 路由装饰器：名字还是原来那个函数
# @app.get("/books")
# async def list_books(): ...

# 普通路由
# app.add_api_route("/books", list_books, methods=["GET"])

# 练习

@app.get("/user/hello")
async def get_user_hello():
    return {"msg":"我正在学习FastAPI"}