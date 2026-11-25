# Worst Fix Ever: Funniest Commit Message — make.fun bounty
# u-deysumbrella-worst-fix-ever-funniest-commit-message-3f1d9722
#
# The program writes one commit message (1-100 characters) to
# /output/entry.txt. Candidates were drafted against the judge's brief,
# in order of weight:
#   1. really a one-line commit message about a fix that made things
#      worse, losing to any commit message off the subject
#   2. a real joke that lands on its own, not just a complaint
#   3. captures the specific irony of a repair that broke more than
#      it mended
#   4. sounds like a real commit subject line a tired engineer would
#      actually type at the end of a bad day
#   5. fresh: no reverting, no testing in production, no "broke
#      everything"
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: subject 10, joke 10, irony 10, commit shape 9, fresh 9 = 48
    # The repair worked exactly as designed and the design was the
    # disaster: plugging the leak meant emptying the mind, so the
    # app forgot the fix too. The fix is the new bug, and the joke
    # lands in the second clause without needing any explanation.
    ("fix: the memory leak is gone - the app now forgets everything, "
     "including the fix",
     48),
    # score: subject 10, joke 9, irony 9, commit shape 10, fresh 9 = 47
    # A one-word fix with a structural punchline: the typo was not a
    # mistake, it was architecture.
    ("fix: the typo is fixed; unfortunately the typo was load-bearing",
     47),
    # score: subject 10, joke 8, irony 10, commit shape 10, fresh 9 = 47
    # The cleanest possible statement of the irony: the bug is dead
    # because its habitat is dead.
    ("fix: the bug no longer reproduces, because the feature no longer "
     "exists",
     47),
    # score: subject 10, joke 9, irony 9, commit shape 9, fresh 8 = 45
    # Off-by-one escalated to off-by-everything: the fix kept the
    # arithmetic and lost the plot.
    ("fix: I fixed the off-by-one error; it is now an off-by-everything "
     "error",
     45),
    # score: subject 10, joke 9, irony 8, commit shape 9, fresh 9 = 45
    # The app learned the lesson too well: it will never crash again,
    # because it will never start again.
    ("fix: the crash is fixed - the app is now too scared to start",
     45),
    # score: subject 10, joke 8, irony 9, commit shape 9, fresh 8 = 44
    # The null is gone, and the pointer took everything with it.
    ("fix: the null pointer is gone, and so is everything it was "
     "pointing at",
     44),
    # score: subject 10, joke 8, irony 9, commit shape 9, fresh 8 = 44
    # The issue tracker is clean because the product is closed: the
    # fix redefined "resolved".
    ("fix: closed the bug by closing the app; zero open issues, zero "
     "open app",
     44),
    # score: subject 10, joke 8, irony 8, commit shape 9, fresh 8 = 43
    # Both threads lose the race: a fix that made the contest fair by
    # making everyone lose it.
    ("fix: the race condition is fixed; both threads now lose",
     43),
]

# The gate requires 1-100 characters of non-whitespace UTF-8 text.
BANNED_STOCK_MOVES = ("revert", "testing in production", "broke everything",
                      "it works on my machine", "please work")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 100, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text.strip(), "candidate must be a single line"
        lowered = text.lower()
        for banned in BANNED_STOCK_MOVES:
            assert banned not in lowered, \
                f"candidate uses a stock move: {banned!r} in {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import os
    entry = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(entry)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == entry, "entry.txt differs from the chosen entry"
    assert 1 <= len(written.strip()) <= 100, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be a single line"
    assert written.strip(), "entry.txt is blank"
    print(entry)


if __name__ == "__main__":
    main()
