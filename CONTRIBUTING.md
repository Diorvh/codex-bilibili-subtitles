# Contributing

Contributions are welcome when they preserve the project's narrow permission, privacy, and scope boundaries.

## Required boundaries

- Keep extraction limited to one explicit Bilibili video URL per invocation.
- Do not add playlists, bulk URL files, account rotation, proxy rotation, rate-limit evasion, CAPTCHA solving, DRM bypass, paywall bypass, or membership bypass.
- Do not add password, Cookie-string, Cookie-file, or browser-profile upload interfaces.
- Do not commit real subtitle tracks, media files, browser databases, account identifiers, or request logs.
- Tests must use synthetic, contributor-authored fixtures.
- Do not imply affiliation with Bilibili or legal approval of a user's intended use.

## Development

The runtime code uses only Python's standard library; yt-dlp is launched as a pinned external dependency.

Run the offline tests:

```text
python -m unittest discover -s tests -v
```

Validate the plugin and skill manifests with the official Codex plugin/skill validators before submitting a change.

## Pull requests

Explain the user need, the smallest behavior change, privacy and platform-term implications, and the tests performed. Dependency updates should link to upstream release information and should be tested against the supported browser matrix where practical.
