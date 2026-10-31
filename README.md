# FastAPI_base

FastAPI 项目骨架，开箱即用：虚拟环境 + 分层路由 + Pydantic 校验 + 自动接口文档。

## 环境

| 项        | 值                               |
| -------- | ------------------------------- |
| Python   | 3.14.7（`D:\compiler\python314`） |
| 虚拟环境     | `.venv\`                        |
| fastapi  | 0.162.0                         |
| uvicorn  | 0.54.0                          |
| pydantic | 2.14.1                          |

## 目录

```
FastAPI_base/
├── .venv/                  # 虚拟环境（不进版本库）
├── .vscode/
│   ├── launch.json         # F5 直接调试
│   └── settings.json       # 锁定 .venv 解释器
├── app/
│   ├── main.py             # 入口：创建 app、挂中间件、注册路由
│   └── routers/
│       └── items.py        # 示例 CRUD（内存存储）
├── practice/               # 学习练习：一文件一应用，不参与部署
│   ├── README.md           # 命名规范、启动方式、端口约定
│   └── ex01_创建路由.py    # 练习 01：路由基础（共 16 个，ex01～ex16）
├── docs/
│   ├── fastapi-learning.md # 学习笔记与踩坑记录
│   └── deployment.md       # 迁移到另一台电脑的三种方案与详细步骤
├── bootstrap.ps1           # 一键：建环境 → 装依赖 → 启动（UTF-8 with BOM）
├── start.bat               # 双击入口，调用 bootstrap.ps1
├── requirements.txt
└── .gitignore
```

## 文档

- [FastAPI 学习笔记](docs/fastapi-learning.md) —— 概念速查、踩坑记录、待学清单
- [练习目录说明](practice/README.md) —— 练习写在哪、怎么命名、怎么启动
- [迁移到另一台电脑](docs/deployment.md) —— 三种方案对比、逐步命令、坑清单、一键脚本

## 用法

### 1. 激活虚拟环境

PowerShell：

```powershell
cd D:\Projects\vscodeProjects\FastAPI_base
.\.venv\Scripts\Activate.ps1
```

如果提示"禁止运行脚本"，先执行一次（只影响当前用户）：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Git Bash：

```bash
cd /d/Projects/vscodeProjects/FastAPI_base
source .venv/Scripts/activate
```

命令行前面出现 `(.venv)` 就成功了。

### 2. 启动

```bash
uvicorn app.main:app --reload
```

- <http://127.0.0.1:8000/> — 根路由
- <http://127.0.0.1:8000/health> — 健康检查
- <http://127.0.0.1:8000/docs> — Swagger 文档（可直接点着测接口）
- <http://127.0.0.1:8000/redoc> — ReDoc 文档

`--reload` 是监听代码改动自动重启，只在开发时用，生产别加。

### 3. 重装依赖

```bash
pip install -r requirements.txt
```

## 加新路由的套路

1. 在 `app/routers/` 下新建 `xxx.py`，写 `router = APIRouter(prefix="/xxx", tags=["xxx"])`
2. 在 `app/main.py` 里 `app.include_router(xxx.router)`

请求体/响应体用 Pydantic 的 `BaseModel` 定义，校验规则写在 `Field(...)` 里，FastAPI 会自动做参数校验并生成文档。

## 常见坑

- **`ModuleNotFoundError: No module named 'app'`**：不在项目根目录启动。先 `cd` 到 `FastAPI_base` 再跑 uvicorn。
- **8000 端口被占**：`uvicorn app.main:app --reload --port 8001`。
- **改了代码不生效**：确认命令里带了 `--reload`；或者你改的文件不在监听范围内。
- **PowerShell 里 `source` 报错**：`source` 是 bash 的写法，PowerShell 用 `.\.venv\Scripts\Activate.ps1`。
