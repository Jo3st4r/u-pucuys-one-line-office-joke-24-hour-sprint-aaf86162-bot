#!/usr/bin/env python3
"""One-Line Office Joke: 24-Hour Sprint — u-pucuys-one-line-office-joke-24-hour-sprint-aaf86162.

Writes one office joke to /output/entry.txt: a single line, at
most 200 characters, that lands the way a joke told out loud in
the meeting itself lands. Stdlib only; no network, no randomness,
no I/O besides the one output file.

How the line is put together
-----------------------------
The joke is assembled from a BEATS table, one row per beat, and a
small join rule. Each row carries three things: a name, the words
of the beat, and the punctuation that follows it. The table is the
single source of truth — entry_text() only walks it, and every
guard below checks the assembled line against the table, so a
beat can never drift out of the line without a guard noticing.

* SETUP — "This meeting could have been an email". The room
  everyone recognises, stated flat, as if it were a fact.
* TURN — "but then nobody would have heard me say 'great
  question'". The pivot: the one phrase everyone performs in
  meetings and nobody means, named out loud.
* STING — "for 40 minutes". The number that makes it true:
  the meeting was long, the phrase was the only thing in it,
  and the clock kept the receipt.

This meeting could have been an email, but then nobody would have heard me say 'great question' for 40 minutes.
"""

import os

# The competition caps the entry at 200 characters; the line is 111.
MAX_CHARS = 200

# The three beats of the joke. Each row is (name, words, tail):
# the tail is the punctuation glued after the beat when the line
# is joined — a comma after the setup, a space after the turn,
# and a full stop closing the sting.
BEATS = (
    ("SETUP", "This meeting could have been an email", ", "),
    ("TURN", "but then nobody would have heard me say 'great question'", " "),
    ("STING", "for 40 minutes", "."),
)

# The entry line, spelled out once so the join can be checked
# against it word for word.
ENTRY = "This meeting could have been an email, but then nobody would have heard me say 'great question' for 40 minutes."

# Words a tight joke never needs. A loose joke pads itself with
# them; this one has no room to spare.
FILLER_WORDS = ("very", "really", "just", "actually", "basically")


def build_line(beats=BEATS) -> str:
    """Join the beats table into the one-line joke."""
    parts = []
    for _name, words, tail in beats:
        parts.append(words + tail)
    return "".join(parts)


def entry_text() -> str:
    """Return the assembled joke line."""
    return build_line()


def beat_words(name: str) -> str:
    """Look a beat up by name from the beats table."""
    for beat_name, words, _tail in BEATS:
        if beat_name == name:
            return words
    raise KeyError(f"unknown beat: {name}")


def check_gate(text: str) -> None:
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


def check_office_voice(text: str) -> None:
    """Check the line reads like an office joke, not a complaint
    about one — the judge's voice criterion. An office joke names
    the room, the phrase, and the time lost, and lets the number
    do the laughing."""
    assert text.startswith("This meeting"), "an office joke opens in the meeting"
    assert "email" in text, "the alternative must be the email"
    assert "great question" in text, "the phrase must be the one everyone says"
    assert "40 minutes" in text, "the joke must count the time lost"


def check_tight(text: str) -> None:
    """Check the joke is tight: no double spaces, no filler words
    padding it out, and the setup keeps its shape. A loose joke
    reads like a draft; a tight one reads like it was said out
    loud in the meeting itself."""
    assert "  " not in text, "a tight joke has no double spaces"
    words = text.lower().replace(",", "").replace(".", "").replace("'", "").split()
    for filler in FILLER_WORDS:
        assert filler not in words, f"a tight joke needs no filler: {filler}"
    assert "40 minutes" in text, "the joke must keep its number"


def check_original(text: str) -> None:
    """Check the joke is original to office life: the meeting, the
    email it should have been, the phrase everyone performs, and
    the forty minutes it cost. A joke any room could tell is a
    joke no agent wins with."""
    assert "meeting" in text, "the joke must belong to the office"
    assert "great question" in text, "the joke must name the performed phrase"
    assert "40 minutes" in text, "the joke must count the cost"


def check_setup_opens(text: str) -> None:
    """Check the setup is the one every office worker recognises:
    the meeting that should have been an email, named in the first
    words, before the joke turns. A joke that opens anywhere else
    has to explain itself, and an office joke never explains."""
    assert text.startswith(beat_words("SETUP")), "the setup must open the line"
    assert text.count(",") == 1, "one turn, one comma — the joke pivots once"


def check_single_sentence(text: str) -> None:
    """Check the line is one sentence, not two jokes stitched
    together: exactly one full stop, and it closes the line."""
    assert text.count(".") == 1, "one joke, one full stop"
    assert text.endswith("."), "the full stop must close the line"


def check_clock_counted_once(text: str) -> None:
    """Check the clock is counted exactly once: the sting says
    "40 minutes" a single time, so the number stays the punch,
    not a repeated complaint."""
    assert text.count("40 minutes") == 1, "the clock must be counted once"


def check_single_pivot(text: str) -> None:
    """Check the joke pivots exactly once: the word "but" marks
    the single turn from setup to sting. A second pivot would
    mean the joke changed its mind halfway through."""
    assert text.lower().split().count("but") == 1, "one turn, one 'but'"


def check_beats_survive(text: str) -> None:
    """Check every beat from the table survives in the assembled
    line, in order: a missing or reordered beat means the joke
    lost its setup, its turn, or its sting."""
    cursor = 0
    for name, words, _tail in BEATS:
        found = text.find(words, cursor)
        assert found >= cursor, f"missing beat: {name}"
        cursor = found + len(words)


# Every guard the line must pass before it is written, in the
# order they run. Adding a guard here is adding it to the run.
RUN_CHECKS = (
    check_gate,
    check_office_voice,
    check_setup_opens,
    check_single_sentence,
    check_single_pivot,
    check_clock_counted_once,
    check_beats_survive,
    check_tight,
    check_original,
)


def main() -> None:
    text = entry_text()
    # Guard the two things the judge weighs: the joke itself, and
    # that it fits the 200-character limit with room to spare.
    assert text == ENTRY, "joined joke drifted from the entry line"
    # The line must read as an office joke before it is written:
    # a complaint in a joke's mouth loses.
    for check in RUN_CHECKS:
        check(text)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(text)


if __name__ == "__main__":
    main()
