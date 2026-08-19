# Troubleshooting

Keep troubleshooting local and minimal. Never paste browser Cookies, passwords, full verbose logs, or browser database files into chat or a public issue.

## yt-dlp is not found

From the repository root, install the pinned dependency into the Python environment that will run the script:

```text
python -m pip install -r requirements.txt
```

Then verify:

```text
python -m yt_dlp --version
```

## The wrong browser profile is selected

Use `--profile` with the profile name or profile directory supported by yt-dlp. Examples:

```text
python scripts/extract_subtitles.py VIDEO_URL --browser firefox --profile default-release --acknowledge-terms
python scripts/extract_subtitles.py VIDEO_URL --browser chrome --profile "Profile 1" --acknowledge-terms
python scripts/extract_subtitles.py VIDEO_URL --browser edge --profile "Profile 2" --acknowledge-terms
```

Do not copy the profile or Cookie database into the repository. Do not publish its path in an issue if the path identifies the local account.

## The Cookie database is locked

Save browser work and fully close the selected browser, including background processes, then retry. Reopen the browser afterward. If the error persists, update to the pinned yt-dlp version and check upstream browser-Cookie documentation without exporting Cookies.

## DPAPI, keychain, or keyring errors

Run the script as the same operating-system user who owns the browser profile. On Linux, Chromium-derived browsers may require `--keyring basictext`, `gnomekeyring`, `kwallet`, `kwallet5`, or `kwallet6`. `--keyring` is intentionally rejected for Firefox and Safari.

## Firefox Container

Use `--container NAME`, or `--container none` when required by yt-dlp. The option is intentionally rejected for non-Firefox browsers.

## Safari

Safari Cookie extraction is supported only on macOS. Granting terminal access to protected browser data may be controlled by macOS privacy settings. Do not weaken system-wide protections solely for this tool.

## The player shows subtitles but the script finds none

Check that:

1. the same browser profile can open the exact video and manually select the desired subtitle;
2. the URL points to one ordinary `/video/BV...` or `/video/av...` page;
3. the requested selector matches the track (default: `zh.*`);
4. the browser session has not expired;
5. the platform has not changed its response format.

Run yt-dlp's subtitle-listing mode manually only if needed, without verbose logging or Cookie export. Platform changes may require an upstream yt-dlp update; do not add scraping fallbacks that bypass normal access controls.

## Membership or paid-format warnings

The script requests subtitles only. yt-dlp may still print information about unavailable video formats during page inspection. That does not mean the script will download media. Do not attempt to bypass membership or payment restrictions.

## Existing files are not overwritten

The extractor uses `--no-overwrites`, and the formatter preserves existing transcript derivatives. Move or rename a previous output if you intentionally want a fresh copy. This prevents an automated retry from destroying user edits.
