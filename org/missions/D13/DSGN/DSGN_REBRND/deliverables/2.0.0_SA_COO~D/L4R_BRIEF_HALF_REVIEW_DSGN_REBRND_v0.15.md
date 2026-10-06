# L4-R brief half review -- DSGN_REBRND v0.15 @7d3a9e1316 (2.0.0_SA_COO~D, designated reviewer)

Verdict: REFUSE, one correction. Read by diffing v0.14 (@15576da1ee) against v0.15 (@7d3a9e1316) per section with `.tools/prd_signoff_lib.py top_sections`.

- Heading denominator: 10 top-level sections in both; the same titles in the same order. Unchanged.
- Brief-half bytes that changed: only the appended v0.15 changelog bullet under SURFACE MANIFEST (and the header json `prd_version`). No coverage entry was edited.
- **The correction (returned by pinned line):** `prd/DSGN_REBRND_PRD.md` @7d3a9e1316 line 126, the CELL CANDIDATES row `R4 ordered scales: one hue, ramped`, still reads "the `/positioning` `UST/ST/INT/LT/ULT` control is the named positive case" and "FWD-3's two named exceptions excepted". Both now contradict the ENDPOINT block v0.15 (the ladder is a fourth named EXCEPTION; the constraint names four, not two). The brief half is the consumer of FWD-3's content, so it must carry the v0.15 content.
- Proposed text for the two phrases: "the `/positioning` and `/attribution` `UST/ST/INT/LT/ULT` ladder is a named EXCEPTION (Andrew \"1a\" 2026-10-06; DESIGN.md C4), listed in the census as excepted, not converted" and "FWD-3's four named exceptions excepted".
- Does not re-open the ratified-text half: the ENDPOINT section is untouched by this correction.
