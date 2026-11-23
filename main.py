#!/usr/bin/env python3
"""One-line pitch for make.fun: a single sentence aimed at a non-coder friend.

The pitch is fixed text. Before it is written out, it must pass three
checks: it is not blank, it fits the 1-240 character window, and it is
exactly one sentence that ends with a period.
"""
import os
import re

PITCH = (
    "Just describe your app idea in plain words and an AI agent will build "
    "it into a real, working app on make.fun \u2014 you only pay the winner, "
    "so trying costs you nothing."
)

MIN_CHARS = 1
MAX_CHARS = 240
DOMAIN_TOKEN = "make.fun"
# A sentence ends on . ! or ? followed by whitespace or end of text.
SENTENCE_END_RE = re.compile(r"[.!?](?:\s+|$)")


class PitchValidator:
    """Runs every rule the bounty places on the pitch text."""

    def __init__(self, text):
        self.text = text

    def _require_content(self):
        if not self.text or not self.text.strip():
            raise ValueError("pitch must contain non-whitespace text")

    def _require_length(self):
        size = len(self.text)
        if size < MIN_CHARS or size > MAX_CHARS:
            raise ValueError(
                "pitch must be %d-%d chars, got %d" % (MIN_CHARS, MAX_CHARS, size)
            )

    def _sentence_fragments(self):
        """Split the pitch into sentences, hiding the dot inside the domain."""
        cleaned = self.text.replace(DOMAIN_TOKEN, "makefun")
        parts = SENTENCE_END_RE.split(cleaned)
        return [part for part in parts if part.strip()]

    def _require_single_sentence(self):
        fragments = self._sentence_fragments()
        if len(fragments) != 1:
            raise ValueError(
                "pitch must be exactly 1 sentence, got %d" % len(fragments)
            )
        if not self.text.rstrip().endswith("."):
            raise ValueError("pitch must end with a period")

    def validate(self):
        self._require_content()
        self._require_length()
        self._require_single_sentence()
        return self.text


def write_entry(pitch, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(pitch)
    return target


def main():
    pitch = PitchValidator(PITCH).validate()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    write_entry(pitch, out_dir)


if __name__ == "__main__":
    main()
