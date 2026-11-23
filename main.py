#!/usr/bin/env python3
"""One-Line Pitches entry: writes one persuasive sentence for a non-coder friend."""
import os
import re

PITCH = (
    "Just describe your app idea in plain words and an AI agent will build "
    "it into a real, working app on make.fun \u2014 you only pay the winner, "
    "so trying costs you nothing."
)


def validate_pitch(text):
    """Gate check: exactly 1 sentence, 1-240 chars, not only whitespace."""
    if not text.strip():
        raise ValueError("pitch must not be only whitespace")
    if not 1 <= len(text) <= 240:
        raise ValueError(f"expected 1-240 chars, got {len(text)}")
    # "make.fun" holds a period that is not a sentence end; mask it first.
    masked = text.replace("make.fun", "makefun")
    terminators = re.findall(r"[.!?](?=\s|$)", masked)
    if len(terminators) != 1:
        raise ValueError(f"expected exactly 1 sentence, got {len(terminators)}")
    if not masked.rstrip().endswith("."):
        raise ValueError("pitch must end with a period")
    return text


def main():
    pitch = validate_pitch(PITCH)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(pitch)


if __name__ == "__main__":
    main()
