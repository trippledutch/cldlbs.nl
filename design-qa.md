# Design QA · CloudLabs / Antithesis reconstruction

- Source visual truth: the four user screenshots from 2026-09-01 at 13.03 and 13.14, plus `reference/antithesis/source-desktop.png` and `reference/antithesis/source-mobile.png`
- Implementation: `http://127.0.0.1:8000/preview-home.html`
- Implementation screenshots: `reference/antithesis/implementation-footer-equal.png` plus the earlier desktop and mobile captures.
- Desktop viewport: 1440 × 1024 CSS px, device scale factor 1
- Mobile device profile: Pixel 7, Chromium
- Source pixels: desktop 1440 × 7450; mobile 1097 × 27641
- Implementation pixels: desktop full-page capture at 1440 CSS px; mobile full-page Pixel 7 capture
- State: homepage, announcement visible, first carousel and first module tab active

## Full-view comparison evidence

The implementation follows the source's defining composition: slim announcement, dark navigation and hero, two-column hero with a data focal, proof/logo rail, three large numeric proofs, long dark editorial statement, dotted light chapter, three bordered benefit cards, large gradient product panel, four supporting columns, horizontal story carousel, warm solution chapter, content carousel, dark CTA and dense footer. Mobile collapses to the same single-column reading order as the source.

Intentional deviations are limited to CloudLabs copy and product meaning. The visible color roles, actual source font families, dashboard visual and four platform illustrations are reproduced locally with the user's permission.

## Focused-region comparison evidence

The desktop and mobile hero regions were inspected at original resolution. Heading scale, CTA grouping, focal proportion, top navigation density and the transition into the trust/proof rail match the source hierarchy. The report gate, story carousel and module tab regions were inspected separately through their browser states.

## Required fidelity surfaces

- Fonts and typography: the source Stringer, Onsite and Onsite Condensed files are stored locally and assigned to the same display, body and condensed roles.
- Spacing and layout rhythm: long-form chapter rhythm, major region proportions, gutters and mobile collapse match the source structure.
- Colors and tokens: matched to the source plum, coral, warm-white and lavender roles.
- Image quality and assets: no source assets are hotlinked. The five reference assets used in the platform chapter are stored locally at their supplied high resolution.
- Copy and content: all visible copy is CloudLabs-specific and avoids source wording.

## Comparison history

1. Initial full-page implementation capture showed blank reveal sections because a full-page screenshot did not trigger IntersectionObserver. Fixed by making all content visible without JavaScript; interactions now carry motion.
2. Browser test reported two font-resource 404s from inactive prototype paths. Fixed by copying and assigning the source fonts locally.
3. User screenshot comparison exposed incorrect blue/lime tokens, font choices, hero height and right-panel width. Replaced with the source fonts and plum/coral palette; hero, trust rail and evidence panel now use the measured source proportions.
4. The 13.14 screenshots exposed an underspecified platform chapter and testimonial grid. Rebuilt both: centered platform heading, 1150px gradient panel, real dashboard crop, four illustrated tiles, oversized whitespace, varied-width horizontal carousel and dotted transition.
5. The 13.22–13.25 references showed that the lower half still used simplified stand-ins. Replaced them with real portrait/video assets, expanded the testimonial track, rebuilt the modules chapter as a six-state vertical carousel, increased the knowledge-card hierarchy, and enlarged the CTA/footer composition.
6. The content review showed that the copied source structure did not yet tell CloudLabs' actual commercial story. Reframed the complete page around the funnel `acute outage → free Cluster Triage → top five signals → RCA or HealthCheck`, removed unrelated testimonial imagery, and generated six distinct infrastructure images tied to the six technical module states.
7. Final copy audit against `BRIEFING-CODEX.md` and the supplied triage notes removed the remaining generic dashboard, added a literal five-signal triage example, made the free/paid boundary explicit, added data-safety copy, and explicitly avoided a promised response time or emergency hotline.
8. Footer comparison against the 14.18 reference exposed an undersized single-row footer. Rebuilt it as a separate patterned CTA, divided five-column navigation/newsletter layer, and large lower brand/legal/trust row with matching vertical proportions.

## Interaction and browser checks

- Mobile menu opens and reports expanded state.
- Module tabs update the visible module content.
- Story carousel advances horizontally.
- Homepage heading and core content render.
- Browser console errors: none in final test.
- Automated result: 1 passed.

## Findings

No actionable P0, P1 or P2 visual mismatches remain in the supplied desktop states. The CloudLabs-specific triage funnel and technical imagery are intentional content improvements over the source.

## Follow-up polish

- P3: confirm long-term licensing before the copied source fonts move beyond this local preview.
- P3: produce original CloudLabs photography or 3D report imagery for a richer focal asset.

final result: passed
