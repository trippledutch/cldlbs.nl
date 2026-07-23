#!/usr/bin/env python3
"""Regenerate search-index.json for the topbar full-text search.

Scans every main + blog HTML page, extracts a bilingual title, a section
label and the visible main-content text, and writes a compact JSON index that
script.js fetches client-side. Pages marked noindex (partners) are skipped, so
stealth pages never surface in search.

Run after any content change:  python3 build-search-index.py
"""
import re, glob, json, html, pathlib

SKIP = {"404.html", "privacy.html", "calculator.html", "cases.html"}


def strip(t):
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    t = re.sub(r'<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def lang_title(block):
    en = re.search(r'<span lang="en">(.*?)</span>', block, re.S)
    nl = re.search(r'<span lang="nl">(.*?)</span>', block, re.S)
    return (strip(en.group(1)) if en else ''), (strip(nl.group(1)) if nl else '')


def main():
    index = []
    files = sorted(glob.glob("*.html")) + sorted(glob.glob("blog/*.html"))
    for f in files:
        if f in SKIP:
            continue
        s = pathlib.Path(f).read_text()
        if 'name="robots" content="noindex' in s:
            continue
        main = re.search(r'<main.*?</main>', s, re.S)
        if not main:
            continue
        mtext = main.group(0)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', mtext, re.S)
        ten, tnl = lang_title(h1.group(1)) if h1 else ('', '')
        if not ten:
            t = re.search(r'<title>(.*?)</title>', s, re.S)
            ten = tnl = (strip(t.group(1)).split(' · ')[0] if t else f)
        if not tnl:
            tnl = ten
        eb = re.search(r'class="eyebrow"[^>]*>(.*?)</div>', mtext, re.S)
        tag = re.search(r'class="tag">(.*?)</span>', mtext, re.S)
        section = strip(eb.group(1)) if eb else (strip(tag.group(1)) if tag else '')
        section = re.sub(r'^/\d+\s*·?\s*', '', section)
        cap = 20000 if f.startswith("blog/") else 6000
        index.append({"u": f, "te": ten, "tn": tnl, "s": section, "x": strip(mtext)[:cap]})

    out = pathlib.Path("search-index.json")
    out.write_text(json.dumps(index, ensure_ascii=False, separators=(',', ':')))
    print("indexed %d pages, %d KB" % (len(index), out.stat().st_size // 1024))


if __name__ == "__main__":
    main()
