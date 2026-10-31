"""FastAPI 项目入口。

运行：
    uvicorn app.main:app --reload
"""
# 演示如何在装饰器中指定响应类型
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse

app = FastAPI()
# FastAPI会自动将路径操作函数返回的Python对象（字典，列表）
# 经jsonable_encoder转换为json兼容格式
# 在装饰器中指定响应json
@app.get("/")
async def root():
    return{"message": "Hello World"}

# 接口：响应HTML代码
# 在装饰器中指定响应HTMl
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    # 命名规则尖括号里放标题，另一个加/，时期闭合，两个尖括号里面加内容
    return "<h1>这是一级标题</h1>"

# 接口：返回一张图片内容
@app.get("/file")
async def get_file():
    # 变量记录地址
    # ./是相对地址，只适用自己输入的路径
    # python因为\后面跟的是转义符如\u，会冲突报错，所以需要前面加r
    path = r"C:\Users\MR\Desktop\作业文件\作品图片\2.png"
    # 告诉响应地址，文件对象返回
    return FileResponse(path)