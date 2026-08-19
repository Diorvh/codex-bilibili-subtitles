---
name: extract-bilibili-subtitles
description: 提取用户有权访问的单个 B 站（Bilibili）视频已有字幕；需要登录时使用由用户本人操作的 Firefox、Chrome、Edge 或其他受支持的本机浏览器会话，并将 SRT 整理为可读文稿。Extract existing Bilibili subtitle tracks when a user provides a video URL and asks for subtitles or a transcript. Do not use for bulk scraping, access-control bypass, credential sharing, or unauthorized republication.
---

# 提取 B 站字幕 / Extract Bilibili Subtitles

提取播放器已经提供的字幕轨道，不下载视频或音频。账号凭据和浏览器数据始终由用户本人控制。

## 法律与权限门槛

向 B 站发起任何自动请求前：

1. 告知用户：即使视频能够正常播放，B 站用户协议仍可能限制自动程序或脚本；
2. 只有当用户拥有内容、已经取得许可，或已经自行确认其用途符合适用法律和平台条款时才继续；
3. 不得把本流程描述为没有风险，也不得将其表述为法律意见；
4. 不支持批量链接、限速规避、验证码绕过、DRM 绕过、付费访问绕过、账号共享或完整第三方文稿再发布。

当用户询问合法性、版权、隐私、商业使用或公开发布时，阅读[隐私、平台条款与版权边界](references/privacy-and-legal.md)。

## 凭据边界

- 不得要求用户把用户名、密码、会话令牌或 Cookie 粘贴到对话中；
- 不得创建或索取 `cookies.txt`；
- 不得复制浏览器配置文件或 Cookie 数据库；
- 需要浏览器登录状态的提取必须由用户在自己的终端中手动运行；
- Agent 可以准备准确命令，但只能读取用户选择放入工作区的字幕文件；
- 不启用 yt-dlp 详细日志，因为没有必要，而且可能暴露额外环境信息。

## 工作流程

1. 检查链接是否为单个 HTTPS B 站视频页面；不接受播放列表、任意其他主机、嵌入凭据的链接或非 HTTPS 链接；
2. 判断匿名提取是否足够。如果需要登录，询问哪个本机浏览器已经拥有访问权限；用户没有指定时默认使用 Firefox；
3. 支持的浏览器名称为：`firefox`、`chrome`、`edge`、`chromium`、`brave`、`opera`、`vivaldi`、`whale` 和 `safari`；Safari 只预期在 macOS 上工作；
4. 向用户显示手动执行命令。实际请求必须提供 `--acknowledge-terms`：

       python scripts/extract_subtitles.py VIDEO_URL --browser firefox --acknowledge-terms

   常见替代命令：

       python scripts/extract_subtitles.py VIDEO_URL --browser chrome --acknowledge-terms
       python scripts/extract_subtitles.py VIDEO_URL --browser edge --acknowledge-terms
       python scripts/extract_subtitles.py VIDEO_URL --browser firefox --profile default-release --acknowledge-terms

5. 等待用户运行命令，不得代替用户执行需要浏览器登录状态的命令；
6. 用户确认完成后，只检查生成的字幕和文稿文件；
7. 保留原始 SRT，把忠实提取与后续校正、总结或改写明确分开；
8. 标记不确定的人名和明显的语音识别同音错误，不要静默编造替换内容。

## 脚本行为

[scripts/extract_subtitles.py](scripts/extract_subtitles.py) 每次只执行一个字幕请求，并且：

- 规范化并校验 B 站链接；
- 禁用 yt-dlp 配置文件；
- 只在进程中读取浏览器 Cookie；
- 从不导出 Cookie 文件；
- 使用 `--skip-download` 和 `--no-playlist`；
- 查找生成的字幕文件；
- 可选生成确定性的阅读副本。

[scripts/format_subtitles.py](scripts/format_subtitles.py) 在不联网的情况下转换已有 SRT，生成逐条忠实 TXT 文稿和按时间分段的 Markdown 阅读稿，不尝试擅自修正专有名词。

遇到浏览器配置文件位置、Cookie 数据库占用、缺少 yt-dlp 或平台错误时，阅读[故障排查](references/troubleshooting.md)。

## 成功结果

应返回：

- 未经修改的原始字幕文件；
- 移除时间戳后的忠实文稿；
- 便于阅读的 Markdown 副本；
- 一段标记可能自动字幕错误的简短说明；
- 用户要求的摘要，且必须作为单独衍生文件保存。

不得把真实第三方字幕、浏览器数据或请求日志放入本插件源代码仓库。
