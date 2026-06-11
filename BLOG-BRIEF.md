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

Reading time target: 12 to 16 minutes per language.

## Voice and audience

- **Audience:** experienced IT pros. Hyper-V and cluster operators, Windows Server admins, IT architects. They know what `Get-ClusterNetwork` does. Don't over-explain basics. Don't write to a beginner.
- **Voice:** pragmatic, evidence-based, calmly authoritative. First-person plural ("we", "wij"). CloudLabs is the speaking entity, we run Hyper-V Health Checks, we see patterns, we report findings.
- **British English.** Use British spelling and idiom: `-ise` (organise, optimise, prioritise, analyse), `-our` (behaviour, colour), `-re` (centre, fibre). Avoid the American defaults LLMs reach for (organize/behavior/center). Single quotes for nested quotes. "Whilst" is acceptable. Apply consistently across the entire article.
- **No marketing fluff.** No "leverage", "unlock", "robust solutions", "in today's fast-paced". No hyperbole. No "amazing", "powerful". Plain technical English and Dutch.
- **Concrete over abstract.** Use real product names (Intel X710, Mellanox CX-4, Dell iDRAC, HPE iLO). Real numbers ("three times as long"). Real failure modes ("Sev-1 at 03:00").
- **Calm urgency.** Problems are real but solvable in a maintenance window. Avoid fearmongering.
- **Match Hans's authentic published voice.** Hans's actual book chapters from his Hyper-V and VMM books score 100% Human on GPTZero. Rewrites by LLMs of the same content score 100% AI. The detector picks up real differences in cadence, sentence structure, and phrasing patterns. Treat detector pass as a calibration signal: if a draft scores AI, it has not matched the authentic voice yet, and needs more work. See "Authentic voice patterns" below for what that voice looks like in practice.

## Authentic voice patterns

The following is a calibration guide for matching Hans's voice. These are good writing principles independent of any AI-detection question. The goal is content that reads as written by a senior Hyper-V engineer who has worked in the field for two decades, in measured, useful, accurate prose.

**Punctuation rules (hard):**

- No em-dashes (—). Replace with commas, colons, parentheses, or a full stop and a new sentence.
- No en-dashes in prose. Use "to" in number ranges ("12 to 16 minutes", not "12–16").
- Hyphens in compound words are fine ("boot-critical", "two-node").

**Vocabulary to drop:**

delve, leverage, navigate, embark, robust, seamless, comprehensive, transformative, unparalleled, foster, harness, unleash, tapestry, weave, in today's fast-paced, the world of, journey, ecosystem, holistic, paradigm, synergy, revolutionise, game-changer. These are marketing language and Hans does not use them.

**Sentence shapes to avoid:**

- "Not just X, it's Y." / "It's not about X, it's about Y."
- "Whether you're X or Y..."
- Triadic lists used as a default rhythm. Mix in pairs and four-item lists.
- Paragraph openers: Moreover, Furthermore, Crucially, Importantly, Notably, It's worth noting that, In addition. Start paragraphs with content.
- Closing with "ultimately" or "at the end of the day".

**Hans's voice from his published book chapters** (use this as the calibration reference):

- Direct, factual openers. "A new VMM installation has a single, empty host group..." not "This one keeps coming up."
- "You can / You must / You will" instructional cadence in procedural sections.
- Full sentences. No fragments. No "But..." or "And..." as paragraph openers.
- Concrete scenarios with operational detail: "A non-enterprise scenario for this type of setup is a demo laptop with Windows Server 2008 R2 SP1 plus Hyper-V in a workgroup..."
- Slightly Dutch-English flavour: "under the wings of VMM 2012", "the newly supported X", "such Hyper-V hosts are often in a perimeter network or DMZ". Not perfectly polished American English.
- Summary pattern: "This chapter discussed X. The chapter also showed Y. Finally, Z. You learned how to..."
- Em-dashes absent. Contractions used sparingly. Formal-but-readable register.

**Calibration check before delivery:** read each paragraph aloud and ask "would Hans, a Hyper-V MVP who has been writing about this for two decades, actually write this, or does it sound like a generic blog template?" If template, rewrite to match the book voice.

## Article structure

1. **H1 title.** Descriptive, evergreen, no clickbait. Examples: "Hyper-V Cluster Health Check: 10 issues we keep finding in 2026", "Live Migration on the wrong network: a common Hyper-V pitfall".
2. **Meta line:** `By Hans Vredevoort · DATE · X minute read · CATEGORY`
3. **Lede (2 short paragraphs).** First paragraph: the problem in context. Second paragraph: what the article delivers.
4. **TOC** as numbered list (3 to 10 items typical).
5. **Body sections.** Each section: cause, then diagnose (with PowerShell or commands), then remediation. One concrete example or PowerShell snippet per section, not three.
6. **Mid-article CTA** (optional, halfway through):
   > Half the issues above take less than ten minutes to spot. The other half you only find if you know where to look. A CloudLabs Hyper-V Cluster Health Check maps them in two days with a severity-ranked action list. → Schedule a Health Check intro call
7. **"The pattern behind the list"** style closing paragraph that zooms out and reflects.
8. **CTA:** *Plan a Hyper-V Cluster Health Check introduction →*
9. **FAQ section.** 4 to 6 questions, plain-language answers. Reuse standard CloudLabs FAQ where applicable (How long does it take? Impact on production? Diff with audit? Azure Local scope? Remediation or advice?).

## Code blocks

Plain PowerShell, no syntax-highlighting hint. Triple-backtick fenced. Comment each major block with what it does. Keep blocks under ~15 lines.

## Bilingual rules

- English first, then Dutch (Nederlands). Match section structure 1-to-1.
- Dutch uses Dutch month names ("15 mei 2026" not "May 15"), "Door Hans Vredevoort", "minuten leestijd".
- Dutch keeps English technical terms (Live Migration, Cluster Shared Volume, Failover Cluster Manager, Test-Cluster, Witness, BlockCache, anti-affinity).
- Dutch tone: same authority, no anglicisms beyond technical terms. "Wij" not "We" (but be natural).
- Don't translate code or PowerShell.
- The GPTZero rules above apply to Dutch as well. Drop the Dutch equivalents of LLM-default words.

## What to include in the article body

Hand-pick from these depending on the topic:

- Root cause analysis (why this happens, not just what)
- PowerShell or commands for diagnosis
- A "CloudLabs finding template" call-out box describing how we score severity
- Vendor or product specifics where relevant (Dell, HPE, Lenovo, Intel, Mellanox)
- Version specifics for Windows Server 2016/2019/2022/2025 if behaviour differs
- A real-world consequence ("we have seen this happen twice")
- A reference to other articles in the CloudLabs corpus (don't try to format these as HTML links, just mention by title; the CloudLabs publish toolchain will wrap them in cross-blog LINK markers)

## What to avoid

- Generic intros ("In today's modern infrastructure...")
- Selling. The article is the proof, not the pitch.
- Telling the reader they should be terrified.
- "Best practices" as a heading. Replace with concrete actions.
- Excessive emoji or formatting tricks.
- Padding to hit a word count.

## Author and branding facts

- **Author:** Hans Vredevoort, Hyper-V & Cluster Consultant, MVP
- **Company:** CloudLabs (cldlbs.com)
- **Services:** Hyper-V Cluster Health Checks, remediation, advisory
- **Style of finding scoring:** Low, Medium, High severity
