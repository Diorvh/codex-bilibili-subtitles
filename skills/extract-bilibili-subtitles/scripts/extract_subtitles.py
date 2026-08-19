#!/usr/bin/env python3
"""Extract one existing subtitle track from an authorized Bilibili video.

The script deliberately does not accept passwords or Cookie files. When login
is needed, yt-dlp reads the selected browser's local Cookie database in process.
No video or audio is downloaded.
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse


SUPPORTED_BROWSERS = (
    "firefox",
    "chrome",
    "edge",
    "chromium",
    "brave",
    "opera",
    "vivaldi",
    "whale",
    "safari",
)
CHROMIUM_BROWSERS = {
    "brave",
    "chrome",
    "chromium",
    "edge",
    "opera",
    "vivaldi",
    "whale",
}
SUPPORTED_KEYRINGS = (
    "basictext",
    "gnomekeyring",
    "kwallet",
    "kwallet5",
    "kwallet6",
)
ALLOWED_HOSTS = {"www.bilibili.com", "bilibili.com"}
VIDEO_PATH_PATTERN = re.compile(
    r"^/video/(?P<video_id>BV[0-9A-Za-z]{10}|av[0-9]+)(?:/)?$",
    re.IGNORECASE,
)
SUBTITLE_EXTENSIONS = {".srt", ".vtt", ".ass", ".lrc", ".ttml", ".json"}
LANGUAGE_SELECTOR_PATTERN = re.compile(r"[0-9A-Za-z*?._,+-]+")


class UserInputError(ValueError):
    """Raised when an input violates the command's safety boundary."""


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract subtitles only from one Bilibili video that you are "
            "authorized to access. Video and audio are never downloaded."
        )
    )
    parser.add_argument("url", help="A single HTTPS Bilibili video-page URL.")
    parser.add_argument(
        "--browser",
        choices=SUPPORTED_BROWSERS,
        default="firefox",
        help="Browser containing the authorized login session. Default: firefox.",
    )
    parser.add_argument(
        "--profile",
        default="",
        help="Optional browser profile name or profile directory.",
    )
    parser.add_argument(
        "--container",
        default="",
        help="Optional Firefox container name. Use 'none' for no container.",
    )
    parser.add_argument(
        "--keyring",
        choices=SUPPORTED_KEYRINGS,
        default=None,
        help="Optional Chromium Cookie keyring on Linux.",
    )
    parser.add_argument(
        "--anonymous",
        action="store_true",
        help="Do not read browser cookies. Use only when the subtitle is public.",
    )
    parser.add_argument(
        "--language",
        default="zh.*",
        help="yt-dlp subtitle language selector. Default: zh.*",
    )
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=Path.cwd() / "subtitle-output",
        help="Output directory. Default: ./subtitle-output",
    )
    parser.add_argument(
        "--skip-format",
        action="store_true",
        help="Do not create transcript copies after an SRT is downloaded.",
    )
    parser.add_argument(
        "--acknowledge-terms",
        action="store_true",
        help=(
            "Confirm that you are authorized to access and process the subtitle "
            "and have independently checked applicable platform terms."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate inputs and print the sanitized command without running it.",
    )
    return parser.parse_args(argv)


def reject_control_characters(value: str, label: str) -> str:
    if any(ord(character) < 32 for character in value):
        raise UserInputError(f"{label} must not contain control characters.")
    return value


def normalize_video_url(value: str) -> tuple[str, str]:
    parsed = urlparse(value.strip())
    host = (parsed.hostname or "").lower()

    try:
        parsed_port = parsed.port
    except ValueError as error:
        raise UserInputError("The URL contains an invalid port.") from error

    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise UserInputError(
            "Only HTTPS video URLs on www.bilibili.com or bilibili.com are accepted."
        )
    if parsed.username or parsed.password:
        raise UserInputError("Embedded URL credentials are not accepted.")
    if parsed_port not in (None, 443):
        raise UserInputError("Non-standard URL ports are not accepted.")

    path_match = VIDEO_PATH_PATTERN.fullmatch(parsed.path)
    if not path_match:
        raise UserInputError(
            "The URL must identify one Bilibili video page, such as "
            "https://www.bilibili.com/video/BVxxxxxxxxxx/."
        )

    normalized_url = urlunparse(("https", host, parsed.path, "", "", ""))
    return normalized_url, path_match.group("video_id")


def validate_language_selector(value: str) -> str:
    value = reject_control_characters(value.strip(), "Language selector")
    if not value or len(value) > 64:
        raise UserInputError("Language selector must contain 1 to 64 characters.")
    if value.startswith("-") or not LANGUAGE_SELECTOR_PATTERN.fullmatch(value):
        raise UserInputError(
            "Language selector may contain only letters, numbers, '.', '*', '?', "
            "'_', '+', ',', and '-'; it must not begin with '-'."
        )
    return value


def build_browser_spec(
    browser: str,
    profile: str = "",
    keyring: str | None = None,
    container: str = "",
) -> str:
    profile = reject_control_characters(profile.strip(), "Profile")
    container = reject_control_characters(container.strip(), "Container")

    if keyring and browser not in CHROMIUM_BROWSERS:
        raise UserInputError("--keyring is only valid for Chromium-based browsers.")
    if container and browser != "firefox":
        raise UserInputError("--container is only valid with Firefox.")
    if profile and browser == "opera":
        raise UserInputError("yt-dlp does not support selecting an Opera profile.")
    if browser == "safari" and sys.platform != "darwin":
        raise UserInputError("Safari Cookie extraction is only supported on macOS.")

    browser_spec = browser
    if keyring:
        browser_spec += f"+{keyring}"
    if profile:
        browser_spec += f":{profile}"
    if container:
        browser_spec += f"::{container}"
    return browser_spec


def resolve_ytdlp_command() -> list[str]:
    executable = shutil.which("yt-dlp")
    if executable:
        return [executable]

    if importlib.util.find_spec("yt_dlp") is not None:
        return [sys.executable, "-m", "yt_dlp"]

    raise RuntimeError(
        "yt-dlp was not found. Install the pinned dependency with "
        "'python -m pip install -r requirements.txt' or install yt-dlp on PATH."
    )


def build_ytdlp_command(
    ytdlp_command: list[str],
    normalized_url: str,
    output_directory: Path,
    language: str,
    browser_spec: str | None,
) -> list[str]:
    output_template = output_directory / "%(id)s.%(ext)s"
    command = [
        *ytdlp_command,
        "--no-config",
        "--no-playlist",
        "--skip-download",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        language,
        "--sub-format",
        "srt/best",
        "--no-overwrites",
        "--windows-filenames",
        "--output",
        str(output_template),
    ]
    if browser_spec is not None:
        command.extend(["--cookies-from-browser", browser_spec])
    command.append(normalized_url)
    return command


def display_command(command: list[str]) -> str:
    if os.name == "nt":
        return subprocess.list2cmdline(command)
    return shlex.join(command)


def find_subtitle_files(output_directory: Path, video_id: str) -> list[Path]:
    if not output_directory.is_dir():
        return []
    return sorted(
        (
            path
            for path in output_directory.iterdir()
            if path.is_file()
            and path.suffix.lower() in SUBTITLE_EXTENSIONS
            and path.name.lower().startswith(video_id.lower())
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def format_srt_files(subtitle_files: list[Path], output_directory: Path) -> None:
    formatter = Path(__file__).resolve().with_name("format_subtitles.py")
    for subtitle_file in subtitle_files:
        if subtitle_file.suffix.lower() != ".srt":
            continue
        completed = subprocess.run(
            [
                sys.executable,
                str(formatter),
                str(subtitle_file),
                "--output-directory",
                str(output_directory),
            ],
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Subtitle extraction succeeded, but transcript formatting failed "
                f"for {subtitle_file.name}."
            )


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)

    try:
        normalized_url, video_id = normalize_video_url(arguments.url)
        language = validate_language_selector(arguments.language)
        browser_spec = None

        if arguments.anonymous:
            if arguments.profile or arguments.container or arguments.keyring:
                raise UserInputError(
                    "--anonymous cannot be combined with profile, container, or keyring."
                )
        else:
            browser_spec = build_browser_spec(
                browser=arguments.browser,
                profile=arguments.profile,
                keyring=arguments.keyring,
                container=arguments.container,
            )

        ytdlp_command = resolve_ytdlp_command()
        output_directory = arguments.output_directory.expanduser().resolve()
        command = build_ytdlp_command(
            ytdlp_command=ytdlp_command,
            normalized_url=normalized_url,
            output_directory=output_directory,
            language=language,
            browser_spec=browser_spec,
        )

        if arguments.dry_run:
            print("Validated dry run. No network or browser data was accessed.")
            print(display_command(command))
            return 0

        if not arguments.acknowledge_terms:
            raise UserInputError(
                "A real request requires --acknowledge-terms. Use it only after "
                "confirming that you are authorized to access and process the "
                "subtitle and have checked applicable platform terms."
            )

        output_directory.mkdir(parents=True, exist_ok=True)
        print("Subtitle-only extraction is starting.")
        print("No username, password, or Cookie file is accepted by this script.")
        print("Video and audio will not be downloaded.")
        print(f"Output directory: {output_directory}")
        if browser_spec is not None:
            print(f"Browser session: {arguments.browser}")
        else:
            print("Browser session: anonymous")
        print()

        process_environment = os.environ.copy()
        process_environment.setdefault("PYTHONUTF8", "1")
        completed = subprocess.run(
            command,
            check=False,
            env=process_environment,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"yt-dlp exited with code {completed.returncode}. See the message "
                "above and the troubleshooting reference."
            )

        subtitle_files = find_subtitle_files(output_directory, video_id)
        if not subtitle_files:
            raise RuntimeError(
                "yt-dlp completed, but no subtitle file was found. Confirm that "
                "the selected account can choose a subtitle track in the player."
            )

        if not arguments.skip_format:
            format_srt_files(subtitle_files, output_directory)

        print()
        print("Subtitle extraction completed:")
        for subtitle_file in subtitle_files:
            print(f"  {subtitle_file}")
        return 0

    except (OSError, RuntimeError, UserInputError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
