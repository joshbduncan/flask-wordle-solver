import os
import re

from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# load all valid wordle words
WORDS = open("words.txt", "r").read().splitlines()


def find_matching_words(invalids, valids, corrects):
    # parse invalid letters and reduce possibilities
    invalid_chrs = [i if i.isalpha() else "" for i in invalids]
    invalid_str = f"(?!.*[{''.join(invalid_chrs)}])" if "".join(invalid_chrs) else ""
    re1 = re.compile(rf"^{invalid_str}[a-z]{{5}}$")
    reduced1 = list(filter(re1.match, WORDS))
    # parse valid letters and reduce possibilities
    valid_chrs = [v if v.isalpha() else "" for v in valids]
    valid_str = "".join([f"(?=.*[{v}])" for v in valid_chrs if v])
    re2 = re.compile(rf"^{valid_str}[a-z]{{5}}$")
    reduced2 = list(filter(re2.match, reduced1))
    # parse correctly placed letters and reduce possibilities
    correct_chrs = [c if c.isalpha() else "." for c in corrects]
    correct_str = "".join(
        [f"[^{v}]" if v and c == "." else c for v, c in zip(valid_chrs, correct_chrs)]
    )
    re3 = re.compile(rf"{correct_str}")
    reduced3 = list(filter(re3.match, reduced2))
    return reduced3


def get_character_counts(matches, valid_chrs):
    matches_chrs = "".join(["".join(list(set(w))) for w in matches])
    ct = {}
    for c in "abcdefghijklmnopqrstuvwxyz":
        if c not in valid_chrs:
            if matches_chrs.count(c):
                ct[c] = round((matches_chrs.count(c) / len(matches)) * 100, 2)
    return dict(sorted(ct.items(), key=lambda item: item[1], reverse=True))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.headers.get("HX-Request"):
        data = request.form
        # parse provided characters
        invalids = [v.lower() for k, v in data.items() if "i" in k]
        valids = [v.lower() for k, v in data.items() if "v" in k]
        corrects = [v.lower() for k, v in data.items() if "c" in k]
        matches = find_matching_words(invalids, valids, corrects)
        if matches:
            cts = get_character_counts(matches, [*valids, *corrects])
        else:
            return '<h2 class="text-align-center">Sorry no matches!</h2>'
        return render_template("words.html", words=matches, cts=cts)
    cts = get_character_counts(WORDS, [])
    return render_template("index.html", words=WORDS, cts=cts)
