# Security Policy

## Supported version

Security fixes currently target the latest release on the default branch.

## Reporting a vulnerability

Do not include passwords, Cookies, browser profiles, personal subtitle files, or other sensitive data in a public issue. Report only the minimum reproducible technical details. Until a private reporting channel is published, open a public issue containing a non-sensitive summary and ask the maintainer for a private contact route.

## Credential model

This project deliberately does not accept usernames, passwords, session tokens, Cookie strings, exported Cookie files, or copied browser Cookie databases. Authenticated extraction uses yt-dlp's local `--cookies-from-browser` integration and must be initiated manually by the user in their own terminal.

No design can guarantee that a third-party dependency or locally compromised machine will protect browser data. Review dependency updates, use an isolated Python environment, keep the browser and operating system patched, and run only source code you have inspected.

## Out of scope

- Requests to defeat CAPTCHA, DRM, paywalls, membership checks, or account controls;
- support for stolen, shared, or exported credentials;
- bulk collection, rate-limit evasion, or stealth scraping;
- redistribution of third-party subtitle content.
