"""
    Flask Wordle Solver
    -----------
    Solving Wordle puzzles using 🐍 Python, Flask, and </> htmx.
    -----------
    :copyright: (c) 2023 Josh Duncan.
    :license: MIT, see LICENSE for more details.
"""

__app_name__ = "flask-wordle-solver"
__version__ = "0.2.1"

import os
import re
from collections import Counter
from typing import Any

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# load all valid wordle words
with open("words.txt") as f:
    WORDS: list[str] = f.read().splitlines()


def find_matching_words(
    corrects: list[str], valids: list[str], invalids: list[str]
) -> list[str]:
    """Find all words matching the current correct, valid, and invalid characters.

    Args:
        corrects (list[str]): Known correct characters.
        valids (list[str]): Known valid characters (in solution but wrong placement).
        invalids (list[str]): Known invalid characters.

    Returns:
        list[str]: Possible solution words at current puzzle state.
    """
    # parse invalid letters and reduce possibilities
    invalid_str = (
        f"(?!.*[{''.join(invalids)}])" if invalids.count("") != len(invalids) else ""
    )
    print(f"{invalid_str=}")
    regex = re.compile(rf"^{invalid_str}[a-z]{{5}}$")
    possible_words = list(filter(regex.match, WORDS))
    # parse valid letters and reduce possibilities
    valid_str = "".join([f"(?=.*[{v}])" for v in valids if v]) if valids else ""
    regex = re.compile(rf"^{valid_str}[a-z]{{5}}$")
    possible_words = list(filter(regex.match, possible_words))
    # parse correctly placed letters and reduce possibilities
    corrects_with_dots = (c if c else "." for c in corrects)
    correct_str = "".join(
        [f"[^{v}]" if v and c == "." else c for v, c in zip(valids, corrects_with_dots)]
    )
    regex = re.compile(rf"{correct_str}")
    possible_words = list(filter(regex.match, possible_words))
    # check to see if any characters are present more
    # than once and already have one valid placement
    multiples = [c for c in corrects_with_dots if c in valids]
    if multiples:
        return [w for c in multiples for w in possible_words if w.count(c) >= 1]
    return possible_words


def get_character_counts(
    matches: list[str], corrects: list[str], valids: list[str]
) -> dict[str, float]:
    """Get percentage of matching words each unplayed character is found in.

    Args:
        matches (list[str]): Possible solution words.
        corrects (list[str]): Known correct characters.
        valids (list[str]): Known valid characters (in solution but wrong placement).

    Returns:
        dict[str, float]: Unplayed character and percentage of times it is found
        in possible solution words.
    """
    character_counts = Counter(list("".join("".join(set(w)) for w in matches)))
    played_characters = corrects + valids
    character_percentages = {
        c: round((ct / len(matches)) * 100, 2)
        for c, ct in character_counts.items()
        if c not in played_characters
    }
    return dict(
        sorted(
            character_percentages.items(),
            key=lambda item: (item[1], item[0]),
            reverse=True,
        )
    )


@app.route("/", methods=["GET", "POST"])
def index() -> Any | str:
    """Base for single-page app."""
    if request.headers.get("HX-Request"):
        data = request.form
        corrects = []
        valids = []
        invalids = []
        # parse provided characters
        for k, v in data.items():
            if not v.isalpha():
                v = ""
            if "c" in k:
                corrects.append(v.lower())
            elif "v" in k:
                valids.append(v.lower())
            else:
                invalids.append(v.lower())
        matches = find_matching_words(corrects, valids, invalids)
        cts = get_character_counts(matches, corrects, valids)
        return render_template(
            "words.html", words=matches, cts=cts, valids=valids, corrects=corrects
        )
    cts = get_character_counts(WORDS, [], [])
    return render_template("index.html", words=WORDS, cts=cts, valids=[], corrects=[])
