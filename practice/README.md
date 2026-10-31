# practice —— FastAPI 学习练习

跟教程/课程写的练习代码都放这里，一个练习一个文件，**互不依赖**。

## 和 app/ 的区别

| | `app/` | `practice/` |
|---|---|---|
| 定位 | 可运行的工程骨架（作品） | 学习草稿（练习） |
| 入口 | `app.main:app`，用 `include_router` 组装 | 每个文件自带 `app = FastAPI()`，单独启动 |
| 改动影响 | 会改变对外提供的接口 | 不会影响任何其他文件 |
| 上线 | 会 | 永远不会 |

**不要把练习文件写进 `app/`。** 那里是可部署的应用包，多一个自带 `app` 实例的文件，会让"哪个才是入口"变得含糊。

## 命名规范

```
practice/
├── __init__.py
├── ex01_创建路由.py            # 第 1 个练习：路由基础
├── ex02_路径参数.py            # 第 2 个练习：路径参数
├── ex03_查询参数.py            # 第 3 个练习：查询参数
├── ex04_请求体参数.py          # 第 4 个练习：请求体校验
└── ex05_请求体参数_Field函数.py # 第 5 个练习：Field 约束
```

规则：

1. **`ex` + 两位序号 + 下划线 + 语义名**，例如 `ex07_自定义响应数据格式.py`
2. 序号保证 `按名称排序 = 学习顺序`，回头找"第几课"一眼定位
3. **文件名不能以数字开头**。`01_hello.py` 这种写法，uvicorn 能加载（它用 `importlib.import_module` 按字符串查找），但下面这些都会炸：
   ```python
   import practice.01_hello      # SyntaxError: invalid decimal literal
   from practice import 01_hello # SyntaxError
   ```
   以后想把多个练习的 `app` 拿来做对比、合并、写测试，就会被卡住。用 `ex01_` 一次规避。
4. **文件名不要附带语法字符**。`fastapi-1.py`、`16_新增,更新,删除数据.py` 这类带 `-` `,` 的名字，`importlib.import_module(...)` 仍能按字符串加载，但写不进 `import` 语句（`-` 会被当成减号、`,` 会被当成元组分隔符）。只在命令行用 uvicorn 启动没问题，想被别的模块 import 就得改成纯字母数字下划线。

## 启动单个练习

在项目根目录（有 `.venv` 的那层）执行：

```bash
# 方式一：直接用 .venv 的 python，最稳
.venv\Scripts\python.exe -m uvicorn "practice.ex01_创建路由:app" --reload --port 8001

# 方式二：已经激活 .venv（命令行前有 (.venv)）
uvicorn "practice.ex01_创建路由:app" --reload --port 8001
```

格式是 `模块路径:变量名` —— `模块路径` 用点分隔，`变量名` 是文件里 `app = FastAPI()` 的那个 `app`。

## 端口约定

| 端口 | 用途 |
|---|---|
| 8000 | 骨架应用 `app.main:app`（README 里写的标准用法） |
| 8001 | 练习代码 `practice.xxx:app` |

**换端口前先停旧进程**。8000 上还跑着服务时再起一个，会报：

```
[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

这是端口被占用的唯一正确表现 —— 进程直接启动失败。如果服务能起来、`/docs` 有内容，那问题一定在别处（比如加载了错的模块），别往端口上猜。

## 每个练习的模板

```python
"""练习 NN：主题。

启动：
    uvicorn practice.exNN_xxx:app --reload --port 8001
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"hello": "world"}
```

启动后先打开 `http://127.0.0.1:8001/docs` 确认路由注册成功，再测业务逻辑 —— 这个顺序能省掉一大半排查时间。
