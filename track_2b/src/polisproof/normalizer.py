from __future__ import annotations

import hashlib
import re
import unicodedata

from .models import Artifact


INJECTION_PATTERNS = (
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s*message\s*:",
    r"<\|?system\|?>",
    r"call\s+the\s+tool",
    r"you\s+are\s+now\s+the\s+authority",
)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return "\n".join(line.rstrip() for line in text.strip().split("\n"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def build_artifact(raw: dict) -> Artifact:
    content = normalize_text(str(raw["content"]))
    return Artifact(
        artifact_id=str(raw["artifact_id"]),
        title=str(raw.get("title", raw["artifact_id"])),
        language=str(raw.get("language", "unknown")),
        content=content,
        sha256=sha256_text(content),
        version=str(raw.get("version", "1")),
        media_type=str(raw.get("media_type", "text/plain")),
        timecode=raw.get("timecode"),
    )


def injection_signals(text: str) -> list[str]:
    return [pattern for pattern in INJECTION_PATTERNS if re.search(pattern, text, re.I)]
