# Bilibili Subtitles

[简体中文](README.zh-CN.md)

A lightweight, skills-only Codex plugin for extracting an existing subtitle track from one Bilibili video that the user is authorized to access, then producing searchable, readable transcript files locally. The repository includes the skill workflow, directly executable Python scripts, offline tests, and clear privacy and usage boundaries.

For interviews, podcasts, lectures, game guides, and other speech-focused videos, the visuals may not be necessary to understand the content. When the desired subtitle can be selected and displayed in the browser player, this plugin can usually retrieve it without downloading video or audio. Actual availability still depends on account access, the subtitle track, browser compatibility, and future changes to Bilibili and yt-dlp.

Typical uses include:

- reading long interviews, daily commentary, and podcast-style videos more efficiently;
- extracting text from lectures, software tutorials, and game guides;
- turning an existing subtitle track into a searchable document for annotation or later analysis;
- asking Codex to create a separate summary, outline, or corrected copy while preserving the source subtitle.

> [!WARNING]
> Bilibili's user agreement may restrict automated scripts that obtain platform content or data without written permission. Being able to play the video, being signed in, or using the result only for personal purposes does not necessarily make automated extraction compliant with platform terms or applicable law. This project does not guarantee the legality of any particular use. Before proceeding, independently confirm your authorization, applicable law, and the platform terms then in effect. See [Legal, copyright, and privacy boundaries](skills/extract-bilibili-subtitles/references/privacy-and-legal.md).

This project is not affiliated with, authorized by, endorsed by, or sponsored by Bilibili or yt-dlp.

## Key characteristics

- **Subtitle-only operation:** uses subtitle-specific options and never downloads video or audio. A subtitle file is commonly only tens of kilobytes, depending on its length and format.
- **Credentials remain local:** yt-dlp reads an existing local browser session in process. The user never needs to paste an account, password, or Cookie into Codex, and the plugin never exports a Cookie file.
- **Broad browser support:** Firefox, Chrome, Edge, Chromium, Brave, Opera, Vivaldi, Whale, and Safari on macOS.
- **Agent-friendly workflow:** the skill gives Codex a repeatable procedure and explicit permission boundaries instead of asking the agent to design a new extractor each time.
- **Source-preserving outputs:** the original SRT remains untouched; faithful TXT, readable Markdown, corrections, and summaries remain separate artifacts.
- **Narrow automation scope:** one explicit video per invocation, with no playlists, bulk URL lists, CAPTCHA bypass, DRM bypass, or access-control evasion.

## Quick start

### 1. Prepare the browser session

1. Sign in to Bilibili in Firefox, Chrome, Edge, or another supported browser.
2. Open the target video page.
3. Confirm that the desired subtitle can be selected and displayed in the player.
4. If the browser Cookie database is reported as locked, save your work, fully exit that browser, and retry. You can reopen it after extraction finishes.

Do not send a Bilibili account, password, Cookie, or browser profile to Codex, and do not export `cookies.txt`.

### 2. Install the runtime dependency

From the repository root on Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

This setup normally needs to be completed only once.

### 3. Ask Codex to prepare the command

After installing the plugin or placing `skills/extract-bilibili-subtitles` in the Codex skills directory, start a new Codex task and use a prompt such as:

```text
Use $extract-bilibili-subtitles to extract the existing Chinese subtitle from this video:
https://www.bilibili.com/video/BVxxxxxxxxxx/

I am signed in with Firefox and have confirmed that the player displays the subtitle.
Extract subtitles only, do not download video or audio, and write to subtitle-output.
```

Replace Firefox with Chrome or Edge when appropriate.

To keep login credentials outside the conversation, the skill instructs Codex to prepare the command but not to run an authenticated extraction on the user's behalf. Review the command and run it manually in your own terminal. It normally looks like this:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --acknowledge-terms
```

When it completes, return to Codex with a message such as:

```text
Subtitle extraction is complete. Read the subtitle and transcript files in subtitle-output.
Preserve the source subtitle, create a separate summary, and flag names or terms that may be transcription errors.
```

### 4. Review the outputs

The default output directory is `subtitle-output`. For an SRT track, the tool normally produces:

- `VIDEO_ID.zh.srt`: the untouched source subtitle track;
- `VIDEO_ID.zh.transcript.txt`: a faithful copy with one original cue per line and no timestamps;
- `VIDEO_ID.zh.reading.md`: a readable Markdown copy grouped into five-minute sections.

The formatter does not silently correct names, terminology, or speech-recognition homophones. Create corrections and summaries as separate derivative files instead of overwriting the SRT or faithful transcript.

## Safety-focused defaults

- Accepts only one HTTPS `bilibili.com/video/...` URL per run.
- Reads an existing local browser login session in process; it never accepts an account, password, Cookie string, or Cookie file.
- Uses `--skip-download` and does not download video or audio.
- Uses `--no-playlist` and does not process playlists or bulk URL lists.
- Requires `--acknowledge-terms` before a real request.
- Keeps the original subtitle file unchanged.
- Creates transcript derivatives locally and never uploads them.
- Does not bypass CAPTCHA, DRM, membership, paywalls, or access controls.

## Supported browsers

The browser names follow yt-dlp's `--cookies-from-browser` support:

| Browser | Option | Notes |
|---|---|---|
| Firefox | `firefox` | Supports an optional profile and Firefox container. |
| Google Chrome | `chrome` | Supports an optional profile. |
| Microsoft Edge | `edge` | Supports an optional profile. |
| Chromium | `chromium` | Supports an optional profile. |
| Brave | `brave` | Supports an optional profile. |
| Opera | `opera` | yt-dlp does not support selecting an Opera profile. |
| Vivaldi | `vivaldi` | Supports an optional profile. |
| Whale | `whale` | Supports an optional profile. |
| Safari | `safari` | macOS only. |

Browser support can change with yt-dlp and browser updates. This repository pins a tested yt-dlp version for reproducibility.

## Requirements

- Python 3.10 or later
- yt-dlp 2026.7.4 (installed from the pinned dependency file)
- A supported local browser; a subtitle that requires login must already be visible to the selected browser profile
- Anonymous mode is available for publicly accessible subtitles

## Direct script use

First perform a dry run. It validates the URL and prints the command without using the network or reading browser data:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --dry-run
```

For a real request, confirm the authorization and terms boundary explicitly:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py `
  "https://www.bilibili.com/video/BVxxxxxxxxxx/" `
  --browser firefox `
  --acknowledge-terms
```

Chrome and Edge examples:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --browser chrome --acknowledge-terms
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --browser edge --acknowledge-terms
```

If the subtitle is available without login:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py VIDEO_URL --anonymous --acknowledge-terms
```

The default output directory is `subtitle-output`. Use `--output-directory PATH` to change it.

### Common options

| Option | Purpose |
|---|---|
| `--browser firefox` | Use the local Firefox session. |
| `--browser chrome` | Use the local Chrome session. |
| `--browser edge` | Use the local Edge session. |
| `--profile PROFILE` | Select a browser profile name or directory when more than one profile exists. |
| `--container NAME` | Select a Firefox Container; valid only with Firefox. |
| `--anonymous` | Do not read a browser session; use only for publicly accessible subtitles. |
| `--language zh.*` | Set the yt-dlp subtitle-language selector; default: `zh.*`. |
| `--output-directory PATH` | Set the subtitle and transcript output directory. |
| `--skip-format` | Keep the subtitle file without generating TXT and Markdown derivatives. |
| `--dry-run` | Validate input and display the command without network or browser access. |
| `--acknowledge-terms` | Confirm that the user independently checked authorization, applicable law, and platform terms; required for a real request. |

Display the complete command reference with:

```powershell
.\.venv\Scripts\python.exe skills\extract-bilibili-subtitles\scripts\extract_subtitles.py --help
```

## Codex installation and credential boundary

The reusable skill is in `skills/extract-bilibili-subtitles`. A Codex installation can install the repository as a plugin, or the skill folder can be copied into the user's local Codex skills directory. After installing or updating it, start a new task and explicitly ask Codex to use `$extract-bilibili-subtitles`.

The skill deliberately instructs Codex not to run an authenticated extraction itself. Codex prepares the command; the user runs it in their own terminal so credentials remain outside the conversation.

## Tests

All tests are offline and use only synthetic subtitles:

```powershell
py -3 -m unittest discover -s tests -v
```

## Copyright, platform terms, and license

The original source code and documentation in this repository are licensed under the [MIT License](LICENSE). The MIT License does not apply to Bilibili videos, subtitle tracks, browser data, trademarks, or other third-party software, and it does not grant rights to copy, redistribute, adapt, translate, or commercially use that content.

This project provides a general-purpose technical tool and does not guarantee that any particular use is lawful or compliant with platform terms. Users must independently confirm that they are authorized to access and process the target subtitle and must comply with applicable law, Bilibili's then-current user agreement, and any other relevant obligations. Do not use this project for bulk collection, access-control evasion, unauthorized republication, or other unlawful or non-compliant activity. Responsibility for a particular use remains with the person carrying it out.

Before contributing, read [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not commit real third-party subtitle tracks, video or audio files, Cookie databases, exported Cookies, account data, or request traces.
