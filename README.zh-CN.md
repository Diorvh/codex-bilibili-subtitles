# Bilibili Subtitles（B 站字幕提取）

[English](README.md)

这是一个面向 Codex 的轻量级纯 Skill 插件，用于从用户有权访问的单个 B 站视频中提取播放器已经提供的字幕轨道，并在本地生成便于检索和阅读的文稿。仓库同时提供 Skill 工作流程、可直接运行的 Python 脚本、离线测试，以及隐私和使用边界说明。

对于访谈、播客、课程讲解、游戏攻略和其他以口播信息为主的视频，画面往往不是理解内容的必要条件。只要目标视频在浏览器播放器中能够选择并显示字幕，本插件通常即可在不下载视频或音频的情况下提取相应字幕，从而帮助用户更高效地阅读、检索和整理口播内容。实际可用性仍取决于账号权限、字幕轨道状态、浏览器兼容性，以及 B 站和 yt-dlp 的后续变化。

典型应用场景包括：

- 快速阅读日更访谈、播客式视频或其他长篇口播内容；
- 提取课程讲解、软件教程和游戏攻略中的文字信息；
- 将已有字幕整理为便于搜索、批注或后续总结的本地文稿；
- 在保留原始字幕的前提下，由 Codex 另行生成摘要、提纲或校正稿。

> [!WARNING]
> B 站用户协议可能限制未经书面许可、通过自动程序或脚本获取平台内容或数据。能够正常播放、已经登录或仅供个人使用，并不必然意味着自动提取符合平台协议或适用法律。本项目不对任何具体用途作出合法性保证。使用前请自行确认内容授权、适用法律以及当时有效的平台条款。详见[法律、版权和隐私边界](skills/extract-bilibili-subtitles/references/privacy-and-legal.md)。

本项目与哔哩哔哩及 yt-dlp 均无隶属、授权、背书或赞助关系。

## 本插件的主要特点

- **只提取字幕**：使用字幕专用参数，不下载视频或音频；单个字幕文件通常仅为数十 KB，具体大小取决于字幕长度和格式。
- **凭据保持在本机**：通过 yt-dlp 在进程中读取本机浏览器的现有登录会话，不要求用户将账号、密码或 Cookie 粘贴到 Codex，也不会导出 Cookie 文件。
- **支持多种常见浏览器**：覆盖 Firefox、Chrome、Edge、Chromium、Brave、Opera、Vivaldi、Whale，以及 macOS 上的 Safari。
- **适合 Agent 使用**：Skill 提供明确的操作流程和权限边界，Codex 可以快速生成对应命令，而无需每次重新设计提取程序。
- **保留原始结果**：原始 SRT 字幕不会被修改；TXT 忠实文稿、Markdown 阅读稿、校正稿和摘要彼此分离。
- **限制自动化范围**：每次仅处理一个明确的视频链接，不支持播放列表、批量链接、验证码绕过、DRM 绕过或访问控制规避。

## 快速使用

### 1. 准备浏览器登录状态

1. 使用 Firefox、Chrome、Edge 或其他受支持的浏览器登录 B 站。
2. 打开目标视频页面。
3. 在播放器中确认“字幕”菜单可以选择并正常显示所需字幕。
4. 如果运行时提示浏览器 Cookie 数据库正在使用，可保存当前工作并完全退出该浏览器后重试；提取完成后可以重新打开浏览器。

不要把 B 站账号、密码、Cookie 或浏览器配置文件发送给 Codex，也不要导出 `cookies.txt`。

### 2. 安装运行依赖

在仓库根目录打开 Windows PowerShell，创建独立的 Python 环境并安装固定依赖：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

完成一次安装后，后续通常无需重复执行。

### 3. 由 Codex 协助生成命令

安装本插件或将 `skills/extract-bilibili-subtitles` 放入 Codex 的 Skills 目录后，请新建一个 Codex 任务，并发送类似指令：

```text
请使用 $extract-bilibili-subtitles 提取下面视频中播放器已经提供的中文字幕：
https://www.bilibili.com/video/BVxxxxxxxxxx/

我已经在 Firefox 中登录并确认播放器能够显示字幕。
只提取字幕，不下载视频或音频；输出到 subtitle-output。
```

如果使用 Chrome 或 Edge，请把提示中的浏览器名称相应改为 `Chrome` 或 `Edge`。

为了避免登录凭据进入对话，Skill 会要求 Codex 只准备命令，而不代替用户运行需要浏览器登录会话的提取。请检查 Codex 给出的命令，然后在自己的 PowerShell 中手动执行。命令通常类似：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --acknowledge-terms
```

命令完成后，可以回到 Codex 并发送：

```text
字幕提取已完成。请读取 subtitle-output 中生成的字幕和文稿，保留原始字幕，另外生成摘要，并标记可能识别错误的人名或术语。
```

### 4. 查看输出结果

默认输出目录为仓库根目录下的 `subtitle-output`。对于 SRT 字幕，通常会得到以下文件：

- `视频ID.zh.srt`：未经修改的原始字幕轨道；
- `视频ID.zh.transcript.txt`：移除序号和时间戳后，每条原字幕占一行的忠实文稿；
- `视频ID.zh.reading.md`：按五分钟分段、便于连续阅读的 Markdown 文稿。

整理程序不会擅自修正人名、术语或自动字幕中的同音错误。需要校正或总结时，应另行创建衍生文件，不要覆盖原始 SRT 和忠实文稿。

## 默认安全边界

- 每次只接受一个 HTTPS `bilibili.com/video/...` 链接；
- 只在进程中读取本机浏览器现有登录会话，不接受账号、密码、Cookie 字符串或 Cookie 文件；
- 使用 `--skip-download`，不下载视频或音频；
- 使用 `--no-playlist`，不处理播放列表或批量链接；
- 真正发起请求前必须显式提供 `--acknowledge-terms`；
- 原始字幕文件保持不变；
- 文稿只在本地生成，不会自动上传；
- 不绕过验证码、DRM、会员、付费墙或其他访问控制。

## 支持的浏览器

浏览器名称与 yt-dlp 的 `--cookies-from-browser` 支持保持一致：

| 浏览器 | 参数 | 说明 |
|---|---|---|
| Firefox | `firefox` | 支持可选配置文件和 Firefox Container。 |
| Google Chrome | `chrome` | 支持可选配置文件。 |
| Microsoft Edge | `edge` | 支持可选配置文件。 |
| Chromium | `chromium` | 支持可选配置文件。 |
| Brave | `brave` | 支持可选配置文件。 |
| Opera | `opera` | yt-dlp 不支持指定 Opera 配置文件。 |
| Vivaldi | `vivaldi` | 支持可选配置文件。 |
| Whale | `whale` | 支持可选配置文件。 |
| Safari | `safari` | 仅支持 macOS。 |

浏览器和 yt-dlp 更新后，兼容性可能变化。仓库固定了一个已测试的 yt-dlp 版本，便于复现。

## 环境要求

- Python 3.10 或更高版本；
- yt-dlp 2026.7.4，由仓库中的固定依赖安装；
- 受支持的本机浏览器；需要登录的字幕必须在所选浏览器配置文件中已经可见；
- 公开字幕也可以使用匿名模式。

## 直接运行脚本

先做离线预演。它只校验输入并显示将执行的命令，不联网，也不读取浏览器数据：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --dry-run
```

真正提取时，需显式确认已经独立检查权限和条款：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --acknowledge-terms
```

Chrome 与 Edge：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --browser chrome --acknowledge-terms
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --browser edge --acknowledge-terms
```

字幕无需登录即可访问时：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --anonymous --acknowledge-terms
```

默认输出目录为 `subtitle-output`，也可通过 `--output-directory 路径` 指定。

### 常用参数

| 参数 | 作用 |
|---|---|
| `--browser firefox` | 使用 Firefox 的本机登录会话。 |
| `--browser chrome` | 使用 Chrome 的本机登录会话。 |
| `--browser edge` | 使用 Edge 的本机登录会话。 |
| `--profile PROFILE` | 指定浏览器配置文件名称或目录；电脑中存在多个配置文件时使用。 |
| `--container NAME` | 指定 Firefox Container；仅适用于 Firefox。 |
| `--anonymous` | 不读取浏览器登录会话；仅适用于公开可用的字幕。 |
| `--language zh.*` | 指定 yt-dlp 字幕语言选择器；默认值为 `zh.*`。 |
| `--output-directory PATH` | 指定字幕和文稿的输出目录。 |
| `--skip-format` | 只保留字幕文件，不生成 TXT 和 Markdown 阅读稿。 |
| `--dry-run` | 只验证输入和显示命令，不联网、不读取浏览器数据。 |
| `--acknowledge-terms` | 确认使用者已自行检查内容权限、适用法律和平台条款；实际请求必须提供。 |

运行以下命令可以查看完整帮助：

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py --help
```

## Codex 安装位置与凭据边界

可复用 Skill 位于 `skills/extract-bilibili-subtitles`。可以将整个仓库安装为 Codex 插件，也可以把该 Skill 文件夹复制到用户的 Codex Skills 目录。安装或更新后，请新建一个 Codex 任务，并在指令中明确调用 `$extract-bilibili-subtitles`。

出于凭据隔离考虑，Skill 会要求 Codex 只准备命令，而不代替用户运行需要登录会话的提取。用户在自己的终端中执行命令，因此账号信息不会进入对话。

## 离线测试

测试仅使用仓库自带的虚构字幕，不访问网络：

```powershell
py -3 -m unittest discover -s tests -v
```

## 版权、平台条款与许可证

本仓库自行编写的源代码和文档采用 [MIT License](LICENSE)。MIT 许可证不适用于 B 站视频、字幕、浏览器数据、商标或其他第三方软件，也不会替使用者取得相关内容的复制、传播、改编、翻译或商业使用权。

本项目仅提供通用技术工具，不构成对任何特定用途合法性或平台合规性的保证。使用者应自行确认其有权访问和处理目标字幕，并遵守适用法律、B 站当时有效的用户协议以及其他相关约定。不得将本项目用于批量抓取、访问控制规避、未经授权的内容再发布或其他违法违规用途；由具体使用行为产生的责任应由实施者自行承担。

参与贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 和 [SECURITY.md](SECURITY.md)。禁止提交真实第三方字幕、视频/音频、Cookie 数据库、导出的 Cookie、账号资料或请求日志。
