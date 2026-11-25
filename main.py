#!/usr/bin/env python3
"""Worst Fix Ever: Funniest Commit Message (make.fun entry).

Writes a single commit message (at most 100 characters) for a bug fix
that made everything worse, to /output/entry.txt.

Method: twelve original candidate lines, each scored by hand against
the judge brief's five criteria in the brief's own order, then the
best line is picked deterministically. No network, no randomness, no
external input, no clock: the same run always writes the same bytes.
"""

import hashlib
import os

# Criteria weights, in the judge brief's order:
#   1. reads as a one-line commit message about a fix that backfired
#   2. makes a reader laugh out loud, a real joke, not just a complaint
#   3. captures the specific irony of a repair that broke more than it mended
#   4. sounds like a real commit subject a tired engineer would type
#   5. finds a fresh angle, not revert / test in production / broke everything
WEIGHTS = (5, 4, 3, 2, 1)

# (candidate line, scores on criteria 1..5, each 0..5)
CANDIDATES = [
    ("fix: optimized the query from 30s to 3ms by returning the wrong rows faster", (5, 5, 5, 4, 5)),
    ("fix: login bug fixed, users can now log in as each other", (5, 5, 4, 5, 4)),
    ("fix: the off-by-one error is now off by two, in the other direction", (5, 4, 5, 4, 5)),
    ("fix: silenced the warning; the disk filled up quietly instead", (5, 4, 4, 5, 4)),
    ("fix: the button did nothing, so now it deletes your account", (5, 5, 4, 4, 4)),
    ("fix: closed the security hole by locking out every real user", (5, 4, 5, 5, 4)),
    ("fix: the infinite loop now ends, right after crashing the database", (5, 3, 3, 4, 3)),
    ("fix: patched the memory leak; the app now leaks disk space instead", (5, 3, 4, 4, 4)),
    ("fix: made the error message clearer; it now explains the new error", (5, 4, 4, 4, 5)),
    ("fix: the rounding error is fixed; all prices now round to zero", (5, 4, 4, 5, 4)),
    ("fix: stopped the server crashing by removing the server", (5, 4, 3, 5, 3)),
    ("fix: the crash on startup is gone, the app no longer starts", (5, 3, 3, 5, 2)),
]

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 100


def score(scores):
    """Weighted total for one candidate's five criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def pick(candidates):
    """Best candidate: highest score, ties broken by shorter text,
    then by earliest position in the list. Fully deterministic."""
    eligible = [(pos, text, sc) for pos, (text, sc) in enumerate(candidates)
                if 0 < len(text) <= MAX_CHARS and text.strip()]
    if not eligible:
        raise SystemExit("no candidate fits the 1-100 character gate")
    best = min(eligible, key=lambda item: (-score(item[2]), len(item[1]), item[0]))
    return best[1], best[2]


def main():
    text, scores = pick(CANDIDATES)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    payload = (text + "\n").encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as handle:
        handle.write(payload)
    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != payload:
        raise SystemExit("output verification failed: bytes on disk differ")
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(payload).hexdigest():
        raise SystemExit("output verification failed: sha256 of written bytes differs")
    print("entry: " + text)
    print("chars: %d" % len(text))
    print("score: %d" % score(scores))
    print("breakdown: " + " ".join("%d*%d" % (w, s) for w, s in zip(WEIGHTS, scores)))
    print("sha256: " + digest)


if __name__ == "__main__":
    main()
