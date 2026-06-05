# CloudLabs blog brief

A self-contained content brief to give to an AI that will draft a CloudLabs blog post from a conversation or topic notes. Output is Markdown only; HTML conversion, JSON-LD, cross-blog link wrapping, and publishing happen on the CloudLabs side via `publish.py`.

## How to use

Paste this entire file into a new AI conversation, followed by the topic and any source material (chat transcript, notes, requirements). Tell the AI: *"Use this brief to write a CloudLabs blog post about [topic]. Return the result in the exact output format specified at the end."*

## Output format

Markdown, not HTML. Both English and Dutch. The two languages cover the same structure 1-to-1.

Single document with this shape:

```
slug: <kebab-case-slug>
category: <short category>
read_time: <N> minutes
sticky: yes|no

# English

(full article here)

# Nederlands

(full article here)
```

Reading time target: 12–16 minutes per language.

## Voice and audience

- **Audience:** experienced IT pros — Hyper-V/cluster operators, Windows Server admins, IT architects. They know what `Get-ClusterNetwork` does. Don't over-explain basics. Don't write to a beginner.
- **Voice:** pragmatic, evidence-based, calmly authoritative. First-person plural ("we", "wij"). CloudLabs is the speaking entity — we run Hyper-V Health Checks, we see patterns, we report findings.
- **British English.** Use British spelling and idiom: `-ise` (organise, optimise, prioritise, analyse), `-our` (behaviour, colour), `-re` (centre, fibre). Avoid the American defaults LLMs reach for (organize/behavior/center). Single quotes for nested quotes. "Whilst" is acceptable. Apply consistently across the entire article.
- **No marketing fluff.** No "leverage", "unlock", "robust solutions", "in today's fast-paced". No hyperbole. No "amazing", "powerful". Plain technical English/Dutch.
- **Concrete over abstract.** Use real product names (Intel X710, Mellanox CX-4, Dell iDRAC, HPE iLO). Real numbers ("three times as long"). Real failure modes ("Sev-1 at 03:00").
- **Calm urgency.** Problems are real but solvable in a maintenance window. Avoid fearmongering.

## Article structure

1. **H1 title** — descriptive, evergreen, no clickbait. Examples: "Hyper-V Cluster Health Check: 10 issues we keep finding in 2026", "Live Migration on the wrong network: a common Hyper-V pitfall".
2. **Meta line:** `By Hans Vredevoort · DATE · X minute read · CATEGORY`
3. **Lede (2 short paragraphs).** First paragraph: the problem in context. Second paragraph: what the article delivers.
4. **TOC** as numbered list (3–10 items typical).
5. **Body sections.** Each section: cause → diagnose (with PowerShell or commands) → remediation. One concrete example or PowerShell snippet per section, not three.
6. **Mid-article CTA** (optional, halfway through):
   > Half the issues above take less than ten minutes to spot. The other half you only find if you know where to look. A CloudLabs Hyper-V Cluster Health Check maps them in two days with a severity-ranked action list. → Schedule a Health Check intro call
7. **"The pattern behind the list"** style closing paragraph that zooms out and reflects.
8. **CTA:** *Plan a Hyper-V Cluster Health Check introduction →*
9. **FAQ section.** 4–6 questions, plain-language answers. Reuse standard CloudLabs FAQ where applicable (How long does it take? Impact on production? Diff with audit? Azure Local scope? Remediation or advice?).

## Code blocks

Plain PowerShell, no syntax-highlighting hint. Triple-backtick fenced. Comment each major block with what it does. Keep blocks under ~15 lines.

## Bilingual rules

- English first, then Dutch (Nederlands). Match section structure 1-to-1.
- Dutch uses Dutch month names ("15 mei 2026" not "May 15"), "Door Hans Vredevoort", "minuten leestijd".
- Dutch keeps English technical terms (Live Migration, Cluster Shared Volume, Failover Cluster Manager, Test-Cluster, Witness, BlockCache, anti-affinity).
- Dutch tone: same authority, no anglicisms beyond technical terms. "Wij" not "We" (but be natural).
- Don't translate code or PowerShell.

## What to include in the article body

Hand-pick from these depending on the topic:

- Root cause analysis (why this happens, not just what)
- PowerShell or commands for diagnosis
- A "CloudLabs finding template" call-out box describing how we score severity
- Vendor or product specifics where relevant (Dell, HPE, Lenovo, Intel, Mellanox)
- Version specifics for Windows Server 2016/2019/2022/2025 if behavior differs
- A real-world consequence ("we have seen this happen twice")
- A reference to other articles in the CloudLabs corpus (don't try to format these as HTML links — just mention by title; the CloudLabs publish toolchain will wrap them in cross-blog LINK markers)

## What to avoid

- Generic intros ("In today's modern infrastructure…")
- Selling. The article is the proof, not the pitch.
- Telling the reader they should be terrified.
- "Best practices" as a heading — replace with concrete actions.
- Excessive emoji or formatting tricks.
- Padding to hit a word count.

## Author / branding facts

- **Author:** Hans Vredevoort, Hyper-V & Cluster Consultant, MVP
- **Company:** CloudLabs (cldlbs.com)
- **Services:** Hyper-V Cluster Health Checks, remediation, advisory
- **Style of finding scoring:** Low / Medium / High severity
