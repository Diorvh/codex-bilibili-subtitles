from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIRECTORY = (
    REPOSITORY_ROOT
    / "skills"
    / "extract-bilibili-subtitles"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIRECTORY))

import format_subtitles as formatter  # noqa: E402


FIXTURE = REPOSITORY_ROOT / "tests" / "fixtures" / "sample.srt"


class SubtitleFormattingTests(unittest.TestCase):
    def test_parses_synthetic_fixture(self) -> None:
        cues = formatter.parse_srt(FIXTURE)
        self.assertEqual(len(cues), 3)
        self.assertEqual(cues[0].start_label, "00:00:00")
        self.assertEqual(cues[2].start_seconds, 301.0)

    def test_creates_faithful_and_reading_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            plain_path, reading_path = formatter.create_transcripts(
                FIXTURE,
                output_directory,
            )

            plain_text = plain_path.read_text(encoding="utf-8-sig")
            reading_text = reading_path.read_text(encoding="utf-8-sig")
            self.assertIn("这是专门编写的测试字幕。", plain_text)
            self.assertNotIn("00:00:00,000", plain_text)
            self.assertIn("## 00:00-05:00", reading_text)
            self.assertIn("## 05:00-10:00", reading_text)

    def test_does_not_overwrite_existing_transcript(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory)
            plain_path, _ = formatter.create_transcripts(FIXTURE, output_directory)
            plain_path.write_text("user edit", encoding="utf-8")
            formatter.create_transcripts(FIXTURE, output_directory)
            self.assertEqual(plain_path.read_text(encoding="utf-8"), "user edit")

    def test_rejects_invalid_timestamp(self) -> None:
        with self.assertRaises(ValueError):
            formatter.parse_timestamp("00:00:XX,000")


if __name__ == "__main__":
    unittest.main()
