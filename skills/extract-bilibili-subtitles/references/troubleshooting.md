# 故障排查

故障排查应保持在本机，并且只收集必要信息。不得把浏览器 Cookie、密码、完整详细日志或浏览器数据库文件粘贴到对话或公开 Issue 中。

## 找不到 yt-dlp

在仓库根目录中，将固定版本依赖安装到实际运行脚本的 Python 环境：

```text
python -m pip install -r requirements.txt
```

然后检查版本：

```text
python -m yt_dlp --version
```

## 选择了错误的浏览器配置文件

通过 `--profile` 指定 yt-dlp 支持的配置文件名称或目录。例如：

```text
python scripts/extract_subtitles.py VIDEO_URL --browser firefox --profile default-release --acknowledge-terms
python scripts/extract_subtitles.py VIDEO_URL --browser chrome --profile "Profile 1" --acknowledge-terms
python scripts/extract_subtitles.py VIDEO_URL --browser edge --profile "Profile 2" --acknowledge-terms
```

不要把浏览器配置文件或 Cookie 数据库复制到仓库中。如果本机路径能够识别用户账号，也不要在 Issue 中公开该路径。

## Cookie 数据库被占用

保存浏览器中的工作，完全退出所选浏览器及其后台进程，然后重试；提取完成后可以重新打开浏览器。如果问题仍然存在，请更新到仓库固定的 yt-dlp 版本并检查上游浏览器 Cookie 文档，不要导出 Cookie。

## DPAPI、钥匙串或 keyring 错误

请使用拥有该浏览器配置文件的同一个操作系统用户运行脚本。在 Linux 上，Chromium 系浏览器可能需要 `--keyring basictext`、`gnomekeyring`、`kwallet`、`kwallet5` 或 `kwallet6`。Firefox 和 Safari 会按设计拒绝 `--keyring` 参数。

## Firefox Container

使用 `--container NAME`；在 yt-dlp 要求时也可以使用 `--container none`。非 Firefox 浏览器会按设计拒绝该参数。

## Safari

Safari Cookie 提取只支持 macOS。终端能否访问受保护的浏览器数据可能受 macOS 隐私设置控制。不要仅为了使用本工具而降低系统范围的安全保护。

## 播放器显示字幕，但脚本没有找到字幕

请检查：

1. 同一浏览器配置文件能够打开该视频并手动选择所需字幕；
2. 链接指向普通的单个 `/video/BV...` 或 `/video/av...` 页面；
3. 字幕语言选择器与实际轨道匹配，默认值为 `zh.*`；
4. 浏览器登录会话尚未过期；
5. 平台没有更改响应格式。

只有确有必要时才手动运行 yt-dlp 的字幕列表模式，并且不要启用详细日志或导出 Cookie。平台变化可能需要等待 yt-dlp 上游更新；不要增加绕过正常访问控制的抓取后备方案。

## 会员或付费格式警告

脚本只请求字幕。yt-dlp 在检查页面时仍可能输出不可用视频格式的信息，但这不代表脚本会下载媒体。不要尝试绕过会员或付费限制。

## 现有文件没有被覆盖

提取程序使用 `--no-overwrites`，整理程序也会保留已经存在的文稿衍生文件。如果确实需要重新生成，请先移动或重命名旧输出。这项设计可以防止自动重试破坏用户已经做过的修改。
