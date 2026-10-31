$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$py = ".\.venv\Scripts\python.exe"

if (-not (Test-Path $py)) {
    Write-Host "[1/3] 首次运行，创建虚拟环境..." -ForegroundColor Cyan
    try {
        python -m venv .venv
    } catch {
        Write-Host "创建失败：未找到 python 命令。" -ForegroundColor Red
        Write-Host "请先安装 Python 3.12 以上版本，安装时勾选 Add python.exe to PATH。" -ForegroundColor Yellow
        Read-Host "按回车退出"
        exit 1
    }
    if (-not (Test-Path $py)) {
        Write-Host "虚拟环境创建失败，请检查 Python 安装。" -ForegroundColor Red
        Read-Host "按回车退出"
        exit 1
    }
} else {
    Write-Host "[1/3] 已存在虚拟环境，跳过创建。" -ForegroundColor DarkGray
}

Write-Host "[2/3] 检查并安装依赖..." -ForegroundColor Cyan
& $py -m pip install -q -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "直连失败，改用清华镜像重试..." -ForegroundColor Yellow
    & $py -m pip install -q -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    if ($LASTEXITCODE -ne 0) {
        Write-Host "依赖安装失败，请检查网络。" -ForegroundColor Red
        Read-Host "按回车退出"
        exit 1
    }
}

$port = if ($env:PORT) { $env:PORT } else { "8000" }

Write-Host "[3/3] 启动服务：http://127.0.0.1:$port/docs" -ForegroundColor Green
Write-Host "关闭此窗口即停止服务（或按 Ctrl+C）。" -ForegroundColor DarkGray
& $py -m uvicorn app.main:app --host 127.0.0.1 --port $port

Read-Host "服务已停止，按回车退出"
