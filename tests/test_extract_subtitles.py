from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = (
    REPOSITORY_ROOT
    / "skills"
    / "extract-bilibili-subtitles"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIRECTORY))

import extract_subtitles as extractor  # noqa: E402


class UrlValidationTests(unittest.TestCase):
    def test_normalizes_single_bv_video_and_drops_tracking_query(self) -> None:
        url, video_id = extractor.normalize_video_url(
            "https://www.bilibili.com/video/BV1AbCdEfGhJ/"
            "?spm_id_from=test#fragment"
        )
        self.assertEqual(url, "https://www.bilibili.com/video/BV1AbCdEfGhJ/")
        self.assertEqual(video_id, "BV1AbCdEfGhJ")

    def test_accepts_single_av_video(self) -> None:
        url, video_id = extractor.normalize_video_url(
            "https://bilibili.com/video/av12345"
        )
        self.assertEqual(url, "https://bilibili.com/video/av12345")
        self.assertEqual(video_id.lower(), "av12345")

    def test_rejects_non_bilibili_host(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.normalize_video_url(
                "https://www.bilibili.com.example/video/BV1AbCdEfGhJ/"
            )

    def test_rejects_http(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.normalize_video_url(
                "http://www.bilibili.com/video/BV1AbCdEfGhJ/"
            )

    def test_rejects_playlist_path(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.normalize_video_url(
                "https://www.bilibili.com/video/BV1AbCdEfGhJ/p2"
            )

    def test_rejects_invalid_port_cleanly(self) -> None:
        with self.assertRaisesRegex(extractor.UserInputError, "invalid port"):
            extractor.normalize_video_url(
                "https://www.bilibili.com:notaport/video/BV1AbCdEfGhJ/"
            )


class BrowserSpecTests(unittest.TestCase):
    def test_common_browser_specs(self) -> None:
        self.assertEqual(extractor.build_browser_spec("firefox"), "firefox")
        self.assertEqual(
            extractor.build_browser_spec("chrome", profile="Profile 1"),
            "chrome:Profile 1",
        )
        self.assertEqual(
            extractor.build_browser_spec("edge", profile="Default"),
            "edge:Default",
        )

    def test_firefox_container(self) -> None:
        self.assertEqual(
            extractor.build_browser_spec(
                "firefox",
                profile="default-release",
                container="Work",
            ),
            "firefox:default-release::Work",
        )

    def test_rejects_firefox_keyring(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.build_browser_spec("firefox", keyring="basictext")

    def test_rejects_chrome_container(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.build_browser_spec("chrome", container="Work")

    def test_rejects_opera_profile(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.build_browser_spec("opera", profile="Default")

    def test_rejects_safari_outside_macos(self) -> None:
        with mock.patch.object(extractor.sys, "platform", "win32"):
            with self.assertRaises(extractor.UserInputError):
                extractor.build_browser_spec("safari")


class CommandBoundaryTests(unittest.TestCase):
    def test_accepts_normal_language_selectors(self) -> None:
        self.assertEqual(extractor.validate_language_selector("zh.*"), "zh.*")
        self.assertEqual(
            extractor.validate_language_selector("all,-live_chat"),
            "all,-live_chat",
        )

    def test_rejects_option_injection_as_language_selector(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.validate_language_selector("--exec")

    def test_rejects_language_selector_with_spaces(self) -> None:
        with self.assertRaises(extractor.UserInputError):
            extractor.validate_language_selector("zh.* --verbose")

    def test_command_is_subtitle_only_and_single_video(self) -> None:
        command = extractor.build_ytdlp_command(
            ytdlp_command=["yt-dlp"],
            normalized_url="https://www.bilibili.com/video/BV1AbCdEfGhJ/",
            output_directory=Path("output"),
            language="zh.*",
            browser_spec="edge:Default",
        )
        self.assertIn("--skip-download", command)
        self.assertIn("--no-playlist", command)
        self.assertIn("--no-config", command)
        self.assertIn("--cookies-from-browser", command)
        self.assertNotIn("--cookies", command)
        self.assertFalse(
            any(argument.startswith("--cookies=") for argument in command)
        )
        self.assertNotIn("--batch-file", command)
        self.assertEqual(command[-1], "https://www.bilibili.com/video/BV1AbCdEfGhJ/")

    def test_anonymous_command_has_no_browser_cookie_option(self) -> None:
        command = extractor.build_ytdlp_command(
            ytdlp_command=["yt-dlp"],
            normalized_url="https://www.bilibili.com/video/BV1AbCdEfGhJ/",
            output_directory=Path("output"),
            language="zh.*",
            browser_spec=None,
        )
        self.assertNotIn("--cookies-from-browser", command)


if __name__ == "__main__":
    unittest.main()
