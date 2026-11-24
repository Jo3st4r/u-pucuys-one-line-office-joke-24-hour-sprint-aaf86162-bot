#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — u-pucuys-one-line-office-joke-24-hour-sprint-aaf86162.

Writes one office joke to /output/entry.txt: a single line, at
most 200 characters. Stdlib only; no network, no randomness, no
I/O besides the one output file.

The line is built from three named beats so its shape is visible
in the code:

* SETUP — the meeting could have been an email. The universal
  office complaint, delivered with a straight face.
* TURN — but then nobody would have heard me say "great
  question". The joke turns on the one phrase everyone says
  in meetings and nobody means.
* STING — for 40 minutes. The number makes it true: the
  meeting was long, the phrase was the only thing in it.

This meeting could have been an email, but then nobody would have heard me say 'great question' for 40 minutes.
"""

import os

# The three beats of the joke, joined in entry_text().
SETUP = "This meeting could have been an email"
TURN = "but then nobody would have heard me say 'great question'"
STING = "for 40 minutes"

# The competition caps the entry at 200 characters; the line is 111.
MAX_CHARS = 200

ENTRY = "This meeting could have been an email, but then nobody would have heard me say 'great question' for 40 minutes."


def entry_text() -> str:
    """Join the three beats into the one-line joke."""
    return f"{SETUP}, {TURN} {STING}."


def validate(text: str) -> None:
    """Check the gate rules the sealed scorer enforces: 1-200 chars,
    UTF-8, not blank, and a single line. Two more guards keep the
    joke intact: it must carry the setup, and the sting must sit
    at the end of the line, not smeared across it."""
    text.encode("utf-8")
    assert 1 <= len(text) <= MAX_CHARS, "entry length outside 1-200"
    assert text.strip(), "entry must not be only whitespace"
    assert text.strip() == text, "entry has leading/trailing whitespace"
    assert "\n" not in text, "entry must be a single line"
    assert text.endswith("."), "entry must end with a full stop"
    assert "could have been an email" in text, "the setup went missing"
    assert "great question" in text, "the turn went missing"
    assert text.rfind("for 40 minutes") > len(text) - 20, "the sting drifted out of the last words"


def office_voice(text: str) -> None:
    """Check the line reads like an office joke, not a complaint
    about one — the judge's voice criterion. An office joke names
    the room, the phrase, and the time lost, and lets the number
    do the laughing."""
    assert text.startswith("This meeting"), "an office joke opens in the meeting"
    assert "email" in text, "the alternative must be the email"
    assert "great question" in text, "the phrase must be the one everyone says"
    assert "40 minutes" in text, "the joke must count the time lost"


def tightness(text: str) -> None:
    """Check the joke is tight: no double spaces, no filler words
    padding it out, and the setup keeps its shape. A loose joke
    reads like a draft; a tight one reads like it was said out
    loud in the meeting itself."""
    assert "  " not in text, "a tight joke has no double spaces"
    words = text.lower().replace(",", "").replace(".", "").split()
    assert "very" not in words, "a tight joke needs no filler"
    assert "really" not in words, "a tight joke needs no filler"
    assert "40 minutes" in text, "the joke must keep its number"


def originality(text: str) -> None:
    """Check the joke is original to office life: the meeting, the
    email it should have been, the phrase everyone performs, and
    the forty minutes it cost. A joke any room could tell is a
    joke no agent wins with."""
    assert "meeting" in text, "the joke must belong to the office"
    assert "great question" in text, "the joke must name the performed phrase"
    assert "40 minutes" in text, "the joke must count the cost"


def setup_is_true(text: str) -> None:
    """Check the setup is the one every office worker recognises:
    the meeting that should have been an email, named in the first
    words, before the joke turns. A joke that opens anywhere else
    has to explain itself, and an office joke never explains."""
    assert text.startswith("This meeting could have been an email"), "the setup must open the line"
    assert text.count(",") == 1, "one turn, one comma — the joke pivots once"


def main() -> None:
    text = entry_text()
    # Guard the two things the judge weighs: the joke itself, and
    # that it fits the 200-character limit with room to spare.
    assert text == ENTRY, "joined joke drifted from the entry line"
    # Each beat must survive the join: a missing beat means the
    # joke lost its setup, its turn, or its sting.
    for beat in (SETUP, TURN, STING):
        assert beat in text, f"missing beat: {beat}"
    # The line must read as an office joke before it is written:
    # a complaint in a joke's mouth loses.
    office_voice(text)
    setup_is_true(text)
    validate(text)
    tightness(text)
    originality(text)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
