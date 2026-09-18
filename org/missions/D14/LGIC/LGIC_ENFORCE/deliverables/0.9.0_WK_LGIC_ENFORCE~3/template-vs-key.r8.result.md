# LGIC_ENFORCE.TO-EN-m-39-r8 -- result

Cell EN-m-39, round 8. Built `org/standards/NAMING_SCHEMA.json` `key.template_detection`
(v1.10 -> v1.11): a ROW-LEVEL mechanism distinguishing an S3 KEY TEMPLATE (a producer's key
FORMAT STRING, round 7's 15 `key_template_rows`) from an S3 KEY (a graded name), without
moving `S3Key` in `types_not_graded_by_kind` -- R-62 refused that move because `S3Key` is
EVERY key.

## What ran

1. `selftest-arms` first: 31 arms, 13 positive-satisfiability, 0 failures.
2. All four mechanical criteria measured FAIL at the cut (`no record`), matching the order.
3. Read `lib/opal_naming.py:493` and `:1012`, `R8_BASE.json`'s `exclusion_table_at_the_cut`,
   `LABEL_TRUTH_R7.json`'s `key_template_rows` (15 rows, all type S3Key/plane repo, each
   carrying `producer_runtime_fields` -- the brace tokens already present in the row's own
   `current` before any grade ran) and R-62's carrier.
4. Designed `key.template_detection`: a row's raw `current` is a TEMPLATE when it carries a
   `{[^{}]+}` token outside grade.placeholder's four sanctioned tokens ({system}, {source},
   {scope}, {cadence}). Added as pure schema DATA -- no code file reads it, so nothing live
   moves.
5. Verified `types_not_graded_by_kind` byte-identical apart from the new field: 8
   genuinely-not-graded, 7 still-routed (S3Key among them), matching R8_BASE's measured cut
   exactly, replicated against the real switch at `lib/opal_naming.py:1012`.
6. Built the discrimination arm: positive arm against round 7's 15 known templates (15/15
   selected); negative arm against 91 ordinary S3Key rows drawn from
   `PLACEHOLDER_CAMPAIGN_R6.json` (a corpus round 7 did not use to derive the 15) -- 0/91
   false positives, tested denominator positive.
7. Built the word-boundary token census for "S3Key": `comp-find 'S3Key' --files --all` found
   456 files; each read in full via Python (not parsed from comp-find's own truncated
   display) for an exact count -- 2,101,890 lines scanned, 10,771 whole-value occurrences,
   10,860 naive-total occurrences (89 substring-only, concentrated in identifier compounds
   like `S3KeyConstRecognizer`).
8. Wrote `TEMPLATE_VS_KEY_R8.json` with all four Rule 24 postulates, the token census, the
   exclusion table after (`deliberately_moved: []`), and the discrimination block.
9. Filed surprise row `LGIC_ENFORCE-W3-S17`: the negative-arm population itself surfaced
   `'silver/%s/'`, an S3Key row using a %-style substitution field the brace-only instrument
   (round 7's and this field's alike) does not detect -- filed as a shape, not re-decided.
10. Committed schema + deliverable + surprise row together (`21b9b46e80`). Re-ran all four
    criteria and selftest-arms at HEAD: unchanged PASS.

## Corrections made mid-flight

None needed re-doing; one design choice was revised before landing: the first token-census
attempt used `comp-find`'s own repo-wide display output for whole-value/substring counting
and undercounted both figures because `comp-find` truncates long lines. Caught before the
record was written (not after) by checking `content_lines` against `total_occurrences` and
finding a shortfall; replaced with a direct per-file Python read of every file `comp-find`
identified, which removed the truncation and produced the numbers in the record.

## Verdicts

- M39R8-AC1 (four postulates): PASS
- M39R8-AC2 (token census): PASS
- M39R8-AC3 (no grade change): PASS
- M39R8-AC4 (discriminates): PASS
- M39R8-AC5 (judgment): UNVERIFIABLE-BY-INSTRUMENT, oracle 3.0.0_SA_CVO
