# app —— 可运行的应用包

项目对外提供的接口都在这一层。`practice/` 里的练习代码是学习草稿，不参与这里。

## 和 practice/ 的分工

| | `app/` | `practice/` |
|---|---|---|
| 定位 | 可运行、可部署的工程骨架 | 单个知识点的练习 |
| 入口 | `app.main:app` | `practice.exNN_xxx:app`，每个文件自带 `app` 实例 |
| 端口 | 8000 | 8001 |
| 改动影响 | 改变对外提供的接口，改前想清楚 | 只影响自己那个文件 |
| 会上线 | 会 | 永远不会 |

判断标准很简单：**这段代码是要给别人调用的，还是自己学一个概念？** 前者进 `app/`，后者进 `practice/`，两边不要混。

## 文件结构

```text
app/
├── __init__.py
├── main.py              # 入口：app 实例、ORM 模型、依赖注入、Book 的增改删
└── routers/
    ├── __init__.py
    └── items.py         # 示例 CRUD（内存存储），演示 Pydantic 字段校验
```

## 启动

在项目根目录（有 `.venv` 那层）执行：

```bash
python run.py                  # 推荐：自动切到 .venv，默认 8000 端口
uvicorn app.main:app --reload  # 已经激活 .venv 时也可以
```

起来之后先开 `http://127.0.0.1:8000/docs`，路由有没有注册上、参数长什么样，一眼就能看出来。

## 接口

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 探活，返回 `{"message": "Hello World"}` |
| POST | `/book/add_book` | 新增图书 |
| PUT | `/book/update_book` | 按 id 更新图书 |
| DELETE | `/book/delete_book` | 按 id 删除图书 |

请求体字段：`id` / `bookname` / `author` / `price` / `publisher`，对应数据库 `book` 表。

**查询接口还没搬进来。** 按条件查、聚合、分页目前只出现在 `practice/ex13` ～ `ex15` 里，`app/` 这边只有增改删。

## 数据库

- 驱动：`aiomysql`（异步 MySQL），引擎在 `main.py` 顶部创建
- 建表：`Base.metadata.create_all` 挂在 `startup` 事件上，服务启动时自动跑一次
- 会话：`get_database()` 是依赖项，每个请求开一个 `AsyncSession`，请求结束自动关闭
- 模型：`Book` → 表 `book`，字段 `id` / `bookname` / `author` / `price` / `publisher`

**连接串目前硬编码在代码里。** 这个仓库是公开的，口令不该待在源码里。改成从环境变量读：

```python
import os

ASYNC_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://user:pass@localhost:3306/dbname?charset=utf8mb4",
)
```

本地开发在项目根目录放一个 `.env`（`.gitignore` 已经排除了它），用 `python-dotenv` 加载即可。

## 两处待办

1. **`routers/items.py` 的 router 没有挂载**：文件里 `router = APIRouter(prefix="/items", ...)` 定义了，但 `main.py` 里没有 `app.include_router(router)`，所以 `/items` 系列接口现在打不开。要么补一行挂上，要么把这个文件当纯示例看。
2. **`@app.on_event("startup")` 已弃用**：新版 FastAPI 推荐改用 `lifespan`，启动和关闭逻辑写在一个上下文管理器里。现在还能用，启动时会打印 deprecated 警告。
