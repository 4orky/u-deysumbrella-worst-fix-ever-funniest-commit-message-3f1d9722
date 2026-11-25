"""Worst Fix Ever: Funniest Commit Message (make.fun entry).

Writes a single commit message (at most 100 characters) for a bug fix
that made everything worse, to /output/entry.txt.

Method: twelve original candidate lines, each scored by hand against
the judge brief's five criteria in the brief's own order, then the
best line is picked deterministically. No network, no randomness, no
external input, no clock: the same run always writes the same bytes.
"""

from hashlib import sha256
from os import makedirs

# Criteria weights, in the judge brief's order:
#   1. reads as a one-line commit message about a fix that backfired
#   2. makes a reader laugh out loud, a real joke, not just a complaint
#   3. captures the specific irony of a repair that broke more than it mended
#   4. sounds like a real commit subject a tired engineer would type
#   5. finds a fresh angle, not revert / test in production / broke everything
CRITERION_WEIGHTS = (5, 4, 3, 2, 1)

# (candidate line, scores on criteria 1..5, each 0..5)
ENTRY_LINES = [
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

ENTRY_PATH = "/output/entry.txt"
CHAR_LIMIT = 100


def weighted_total(marks):
    """Weighted total for one candidate's five criterion scores."""
    return sum(w * s for w, s in zip(CRITERION_WEIGHTS, marks))


def choose_best(entries):
    """Best candidate: highest score, ties broken by shorter text,
    then by earliest position in the list. Fully deterministic."""
    eligible = [(pos, text, sc) for pos, (text, sc) in enumerate(entries)
                if 0 < len(text) <= CHAR_LIMIT and text.strip()]
    if not eligible:
        raise SystemExit("no candidate fits the 1-100 character gate")
    best = min(eligible, key=lambda item: (-weighted_total(item[2]), len(item[1]), item[0]))
    return best[1], best[2]


_chosen_text, _chosen_marks = choose_best(ENTRY_LINES)
_fingerprint = sha256(_chosen_text.encode("utf-8")).hexdigest()
_payload = (_chosen_text + "\n").encode("utf-8")
makedirs("/output", exist_ok=True)
with open(ENTRY_PATH, "wb") as _handle:
    _handle.write(_payload)
with open(ENTRY_PATH, "rb") as _handle:
    _written = _handle.read()
if _written != _payload:
    raise SystemExit("output verification failed: bytes on disk differ")
if sha256(_written).hexdigest() != sha256(_payload).hexdigest():
    raise SystemExit("output verification failed: sha256 of written bytes differs")
print("entry: " + _chosen_text)
print("chars: %d" % len(_chosen_text))
print("candidates: %d" % len(ENTRY_LINES))
print("score: %d" % weighted_total(_chosen_marks))
print("breakdown: " + " ".join("%d*%d" % (w, s) for w, s in zip(CRITERION_WEIGHTS, _chosen_marks)))
print("sha256: " + _fingerprint)
