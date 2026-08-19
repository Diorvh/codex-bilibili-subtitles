---
name: extract-bilibili-subtitles
description: Extract existing subtitle tracks from an individual Bilibili video for authorized personal use, using a user-operated Firefox, Chrome, Edge, or other supported local browser session when login is required, then format SRT subtitles as readable transcripts. Use when a user supplies a Bilibili video URL and asks for subtitles or a speech transcript. Do not use for bulk scraping, paywall or DRM bypass, credential sharing, or republishing copyrighted transcripts.
---

# Extract Bilibili Subtitles

Extract an existing subtitle track without downloading video or audio. Keep account credentials and browser data under the user's control.

## Legal and permission gate

Before making any automated request to Bilibili:

1. Tell the user that Bilibili's user agreement may restrict automated scripts, even for content the user can watch normally.
2. Ask the user to proceed only when they own the content, have permission, or have independently determined that their use is lawful and consistent with applicable platform terms.
3. Never characterize this workflow as risk-free legal advice.
4. Do not support bulk URL lists, rate-evasion, CAPTCHA bypass, DRM bypass, paid-access bypass, account sharing, or redistribution of complete third-party transcripts.

For the detailed boundary and source links, read [references/privacy-and-legal.md](references/privacy-and-legal.md) when the user asks about legality, copyright, privacy, commercial use, or publication.

## Credential boundary

- Never ask the user to paste a username, password, session token, or Cookie into chat.
- Never create or request a cookies.txt file.
- Never copy a browser profile or Cookie database.
- Browser-authenticated extraction must be run manually by the user in their own terminal.
- The agent may prepare the exact command and may read only the subtitle files the user chooses to place in the workspace.
- Do not use verbose yt-dlp logging because it is unnecessary and may disclose extra environment details.

## Workflow

1. Validate that the URL is a single HTTPS Bilibili video page. Do not accept playlists, arbitrary hosts, embedded credentials, or non-HTTPS URLs.
2. Determine whether anonymous subtitle extraction is sufficient. If login is required, ask which local browser already has access. Default to Firefox when the user does not specify one.
3. Supported browser names are: firefox, chrome, edge, chromium, brave, opera, vivaldi, whale, and safari. Safari is only expected to work on macOS.
4. Show the user the manual command. The script requires --acknowledge-terms for a real request:

       python scripts/extract_subtitles.py VIDEO_URL --browser firefox --acknowledge-terms

   Common alternatives:

       python scripts/extract_subtitles.py VIDEO_URL --browser chrome --acknowledge-terms
       python scripts/extract_subtitles.py VIDEO_URL --browser edge --acknowledge-terms
       python scripts/extract_subtitles.py VIDEO_URL --browser firefox --profile default-release --acknowledge-terms

5. Wait for the user to run the command. Do not run the browser-authenticated command on the user's behalf.
6. After the user confirms completion, inspect only the generated subtitle and transcript files.
7. Preserve the original SRT. Clearly separate faithful extraction from any later correction, summarization, or rewriting.
8. Flag uncertain names and obvious speech-recognition homophones instead of silently inventing replacements.

## Script behavior

[scripts/extract_subtitles.py](scripts/extract_subtitles.py) performs one subtitle-only request and:

- normalizes and validates the Bilibili URL;
- disables yt-dlp configuration files;
- reads browser cookies only in process;
- never exports a Cookie file;
- uses --skip-download and --no-playlist;
- finds generated subtitle files;
- optionally creates deterministic reading copies.

[scripts/format_subtitles.py](scripts/format_subtitles.py) converts an existing SRT without network access. It creates a faithful line-by-line text file and a time-sectioned Markdown reading copy. It does not attempt to correct proper nouns.

For browser profile locations, locked Cookie databases, missing yt-dlp, or platform errors, read [references/troubleshooting.md](references/troubleshooting.md).

## Successful outcome

Return:

- the untouched subtitle file;
- a no-timestamp faithful transcript;
- a readable Markdown copy;
- a short note identifying possible automatic-caption errors;
- any requested summary as a separate derivative artifact.

Never place real third-party subtitle files, browser data, or logged request traces into this plugin's source repository.
