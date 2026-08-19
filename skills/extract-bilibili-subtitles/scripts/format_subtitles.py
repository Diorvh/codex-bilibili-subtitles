#!/usr/bin/env python3
"""Create faithful, offline reading copies from an SRT subtitle file."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TIMESTAMP_PATTERN = re.compile(
    r"^(?P<hours>\d{2}):(?P<minutes>\d{2}):(?P<seconds>\d{2}),"
    r"(?P<milliseconds>\d{3})$"
)
TERMINAL_PUNCTUATION = set(".!?;。！？；")


@dataclass(frozen=True)
class Cue:
    start_seconds: float
    start_label: str
    text: str


def parse_timestamp(value: str) -> float:
    match = TIMESTAMP_PATTERN.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid SRT timestamp: {value}")
    return (
        int(match.group("hours")) * 3600
        + int(match.group("minutes")) * 60
        + int(match.group("seconds"))
        + int(match.group("milliseconds")) / 1000
    )


def parse_srt(source_path: Path) -> list[Cue]:
    raw_text = source_path.read_text(encoding="utf-8-sig")
    normalized_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n", normalized_text.strip())
    cues: list[Cue] = []

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start_value = lines[1].split("-->", maxsplit=1)[0].strip()
        cue_text = " ".join(lines[2:]).strip()
        if not cue_text:
            continue
        cues.append(
            Cue(
                start_seconds=parse_timestamp(start_value),
                start_label=start_value[:8],
                text=cue_text,
            )
        )

    if not cues:
        raise ValueError(f"No subtitle cues were parsed from: {source_path}")
    return cues


def format_section_label(start_seconds: int, section_seconds: int) -> str:
    end_seconds = start_seconds + section_seconds
    start_minutes, start_remainder = divmod(start_seconds, 60)
    end_minutes, end_remainder = divmod(end_seconds, 60)
    return (
        f"{start_minutes:02d}:{start_remainder:02d}"
        f"-{end_minutes:02d}:{end_remainder:02d}"
    )


def build_paragraphs(cues: list[Cue], character_limit: int) -> list[str]:
    paragraphs: list[str] = []
    current_parts: list[str] = []
    current_length = 0

    for cue in cues:
        projected_length = current_length + len(cue.text) + (1 if current_parts else 0)
        if current_parts and projected_length > character_limit:
            paragraphs.append(" ".join(current_parts))
            current_parts = []
            current_length = 0

        current_parts.append(cue.text)
        current_length += len(cue.text) + (1 if len(current_parts) > 1 else 0)

        if cue.text[-1] in TERMINAL_PUNCTUATION and current_length >= 120:
            paragraphs.append(" ".join(current_parts))
            current_parts = []
            current_length = 0

    if current_parts:
        paragraphs.append(" ".join(current_parts))
    return paragraphs


def choose_output_paths(source_path: Path, output_directory: Path) -> tuple[Path, Path]:
    base_name = source_path.stem
    return (
        output_directory / f"{base_name}.transcript.txt",
        output_directory / f"{base_name}.reading.md",
    )


def write_if_absent(path: Path, content: str) -> str:
    if path.exists():
        return "kept existing"
    path.write_text(content, encoding="utf-8-sig")
    return "created"


def create_transcripts(
    source_path: Path,
    output_directory: Path,
    section_minutes: int = 5,
    paragraph_character_limit: int = 420,
) -> tuple[Path, Path]:
    cues = parse_srt(source_path)
    output_directory.mkdir(parents=True, exist_ok=True)
    plain_path, reading_path = choose_output_paths(source_path, output_directory)

    plain_header = (
        f"Source subtitle: {source_path.name}\n"
        "Faithful copy: timestamps and sequence numbers removed; one original "
        "subtitle cue per line. Proper nouns are not corrected.\n\n"
    )
    plain_content = plain_header + "\n".join(cue.text for cue in cues) + "\n"

    section_seconds = section_minutes * 60
    grouped: dict[int, list[Cue]] = {}
    for cue in cues:
        section_start = int(cue.start_seconds // section_seconds) * section_seconds
        grouped.setdefault(section_start, []).append(cue)

    reading_lines = [
        f"# Transcript: {source_path.stem}",
        "",
        f"> Source subtitle: {source_path.name}",
        "> Timestamps and sequence numbers were removed. Cues were joined into "
        "time-based reading sections without correcting proper nouns.",
        "",
    ]
    for section_start in sorted(grouped):
        reading_lines.append(
            f"## {format_section_label(section_start, section_seconds)}"
        )
        reading_lines.append("")
        for paragraph in build_paragraphs(
            grouped[section_start],
            paragraph_character_limit,
        ):
            reading_lines.append(paragraph)
            reading_lines.append("")
    reading_content = "\n".join(reading_lines).rstrip() + "\n"

    plain_status = write_if_absent(plain_path, plain_content)
    reading_status = write_if_absent(reading_path, reading_content)
    print(f"{plain_status}: {plain_path}")
    print(f"{reading_status}: {reading_path}")
    return plain_path, reading_path


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create faithful transcript copies from an existing SRT file."
    )
    parser.add_argument("source", type=Path, help="Source SRT subtitle file.")
    parser.add_argument(
        "--output-directory",
        type=Path,
        default=None,
        help="Output directory. Default: the source file's directory.",
    )
    parser.add_argument(
        "--section-minutes",
        type=int,
        default=5,
        help="Length of time-based Markdown sections. Default: 5.",
    )
    parser.add_argument(
        "--paragraph-character-limit",
        type=int,
        default=420,
        help="Approximate paragraph size. Default: 420 characters.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(argv)
    try:
        source_path = arguments.source.expanduser().resolve()
        if not source_path.is_file() or source_path.suffix.lower() != ".srt":
            raise ValueError("The source must be an existing .srt file.")
        if arguments.section_minutes < 1 or arguments.section_minutes > 60:
            raise ValueError("--section-minutes must be between 1 and 60.")
        if (
            arguments.paragraph_character_limit < 120
            or arguments.paragraph_character_limit > 5000
        ):
            raise ValueError(
                "--paragraph-character-limit must be between 120 and 5000."
            )

        output_directory = (
            arguments.output_directory.expanduser().resolve()
            if arguments.output_directory is not None
            else source_path.parent
        )
        create_transcripts(
            source_path=source_path,
            output_directory=output_directory,
            section_minutes=arguments.section_minutes,
            paragraph_character_limit=arguments.paragraph_character_limit,
        )
        return 0
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
