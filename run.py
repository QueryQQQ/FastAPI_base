"""统一启动入口：不管用哪个 Python 运行，都会自动切到项目虚拟环境。

用法（在项目根目录执行）：
    python run.py                 # 启动主应用 app.main:app，默认 8000 端口
    python run.py demo            # 启动示例文件 app/fastapi-1.py
    python run.py demo 8001       # 指定端口
    python run.py main 8002       # 主应用 + 指定端口

为什么需要它：
    1) 直接 `python app/main.py` 不行——FastAPI 应用要用 uvicorn 加载，不是执行；
    2) 忘了激活 .venv 时，`python` 会指向全局解释器，报 No module named 'fastapi'。
    这个脚本会检测当前解释器，不在 .venv 里就自动用 .venv 的 python 重新拉起自己。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PY = ROOT / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
SELF = Path(__file__).resolve()

# 允许的应用名 -> uvicorn 导入字符串
TARGETS = {
    "main": "app.main:app",
    "app": "app.main:app",
    "demo": "app.fastapi_1:app",
    "fastapi-1": "app.fastapi_1:app",
    "fastapi1": "app.fastapi_1:app",
}
DEFAULT_TARGET = "main"
DEFAULT_PORT = 8000


def is_project_venv() -> bool:
    """当前进程用的解释器是不是项目 .venv 里的那个。"""
    try:
        return Path(sys.executable).resolve() == VENV_PY.resolve()
    except OSError:
        return False


def relaunch_in_venv() -> None:
    """用 .venv 的解释器重新执行本脚本。"""
    if not VENV_PY.exists():
        sys.exit(
            f"[x] 找不到虚拟环境：{VENV_PY}\n"
            f"    请先在项目根执行：python -m venv .venv\n"
            f"    再执行：.venv\\Scripts\\python.exe -m pip install -r requirements.txt"
        )
    print(f"[i] 当前解释器不是项目虚拟环境：{sys.executable}")
    print(f"[i] 自动切换到：{VENV_PY}")
    raise SystemExit(subprocess.call([str(VENV_PY), str(SELF), *sys.argv[1:]]))


def parse_args(argv: list[str]) -> tuple[str, int]:
    """解析应用名和端口，两者都支持省略。"""
    target_name = DEFAULT_TARGET
    port = int(os.environ.get("PORT", DEFAULT_PORT))

    positional = [a for a in argv if not a.startswith("-")]
    if positional:
        key = positional[0].lower()
        if key.isdigit():
            port = int(key)
        elif key in TARGETS:
            target_name = key
        else:
            sys.exit(
                f"[x] 未知的应用名：{positional[0]}\n"
                f"    可用：{' / '.join(sorted(set(TARGETS)))}"
            )
    if len(positional) > 1 and positional[1].isdigit():
        port = int(positional[1])

    return TARGETS[target_name], port


def main() -> None:
    if not is_project_venv():
        relaunch_in_venv()

    os.chdir(ROOT)  # 保证 app 包可被导入
    sys.path.insert(0, str(ROOT))

    target, port = parse_args(sys.argv[1:])

    try:
        import uvicorn
    except ModuleNotFoundError:
        sys.exit("[x] 虚拟环境里没有 uvicorn，请执行：pip install -r requirements.txt")

    print(f"[i] Python  : {sys.executable}")
    print(f"[i] 应用    : {target}")
    print(f"[i] 地址    : http://127.0.0.1:{port}   文档: http://127.0.0.1:{port}/docs")
    print("[i] 停止服务：Ctrl+C")
    print()

    uvicorn.run(target, host="127.0.0.1", port=port, reload=True)


if __name__ == "__main__":
    main()
