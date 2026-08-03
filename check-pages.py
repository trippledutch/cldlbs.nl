#!/usr/bin/env python3
"""Refuse a page that says something in one language and not in the other.

WHY THIS EXISTS. Every visible sentence on this site is a pair: an English span
and a Dutch one, and the language switch shows whichever the visitor picked. A
sentence that exists in only one of the two is invisible to half the readers and
looks finished to whoever wrote it.

It was measured by hand on 3 August 2026 while rewriting the partner page, and
the count came out even. A measurement somebody did once is not a property that
holds; the same week, the English half of the sample document set had been
broken for five days without anything saying so, because the verifier read only
the Dutch documents. This is the same gap, on the website side.

WHAT IT CHECKS, and the limits are part of the answer:

  - every <span lang="en"> has a <span lang="nl"> and the counts match per file
  - both members of a pair carry text; an empty one is a half translation
  - lang="en"/lang="nl" attributes outside <span> (the <html> element, the
    language buttons, hreflang links) are NOT counted, because they are
    machinery rather than content

  - it does NOT check that the two say the same thing. Nothing mechanical can.
    A pair whose Dutch half is a leftover from an older sentence passes here and
    has to be caught by reading.

Run: python3 check-pages.py [file.html ...]   (default: every page in the root)
Exit 0 when balanced, 1 when not.
"""

import glob
import os
import re
import sys

SPAN_OPEN = re.compile(r'<span lang="(en|nl)"[^>]*>')
PAIR = re.compile(r'<span lang="(en|nl)"[^>]*>(.*?)</span>', re.S)
TAGS = re.compile(r"<[^>]+>")


def counts(text):
    found = {"en": 0, "nl": 0}
    for m in SPAN_OPEN.finditer(text):
        found[m.group(1)] += 1
    return found


CONTENT_TAG = re.compile(r"<(?:img|source|video|iframe)\b", re.I)


def empty_halves(text):
    """A span that carries nothing: no words AND no image.

    A pair of which one half is empty renders as a blank line for half the
    visitors, and the page still looks complete to the person who wrote it.

    AN IMAGE COUNTS AS CONTENT, and the first run of this check proved why that
    has to be said. Eight spans were reported as empty on a page where the two
    halves each hold a different screenshot - one English, one Dutch - and
    stripping the tags left nothing behind. Measuring "no text" when the subject
    is "no content" is the same mistake as a detector that looks for a
    consequence.
    """
    out = []
    for m in PAIR.finditer(text):
        inner = m.group(2)
        if TAGS.sub("", inner).strip() or CONTENT_TAG.search(inner):
            continue
        out.append((m.group(1), m.start()))
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def main():
    files = sys.argv[1:]
    if not files:
        files = sorted(glob.glob("*.html")) + sorted(glob.glob("blog/*.html"))
    bad = 0
    for path in files:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        c = counts(text)
        holes = empty_halves(text)
        state = "OK" if c["en"] == c["nl"] and not holes else "FAIL"
        print("%-34s en=%-4d nl=%-4d %s" % (os.path.basename(path), c["en"], c["nl"], state))
        if c["en"] != c["nl"]:
            bad += 1
            print("     %d sentence(s) exist in one language only" % abs(c["en"] - c["nl"]))
        for lang, pos in holes:
            bad += 1
            print("     line %d: an empty lang=%s half" % (line_of(text, pos), lang))
    if bad:
        print("\n%d page(s) say something in one language and not in the other." % bad)
        return 1
    print("\nevery page carries both languages, %d file(s) read" % len(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
