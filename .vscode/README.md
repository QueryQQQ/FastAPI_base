# .vscode —— 编辑器配置

不参与运行，只影响 VS Code 打开这个项目时的行为。

| 文件 | 作用 |
|---|---|
| `launch.json` | 按 F5 直接以调试模式启动 `app.main:app`，能打断点 |
| `settings.json` | 把 Python 解释器锁定到 `.venv`，避免误用全局 Python 报 `No module named 'fastapi'` |

`.gitignore` 里 `.vscode/*` 是排除整个目录，再用 `!.vscode/launch.json`、`!.vscode/settings.json` 白名单放行这两个文件。所以在这层新增的其他配置（比如 `extensions.json`）默认不会进版本库，需要的话得自己加白名单。

这两个文件里如果出现本机绝对路径（比如解释器路径），换电脑后 F5 可能会失效，改一下路径或删掉重新生成即可。
