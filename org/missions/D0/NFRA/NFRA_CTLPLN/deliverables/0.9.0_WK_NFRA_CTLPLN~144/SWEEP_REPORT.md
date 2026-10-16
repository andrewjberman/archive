# CT-bf-1 AMENDMENT 1 -- regression sweep, head-anchored rule

Denominator: 232 runs = 232 (project, round) pairs from `org/missions/D*/*/*/decompositions/*DECOMP.round<n>.md` (the two
`IRPT_CUSTDY_DECOMP.round7.addendum*.md` files are not round files and are excluded, as in the first seating), over 9 tree
projects. Each run: `python .tools/round-close-check.py --project <CODE> --round <n>`, timeout 120. Result: 0 timeouts, 0
non-zero exits. Runner: `sweep_runner.py`; comparator: `sweep_compare.py` (both in this folder).

Files (this folder):

- `SWEEP_BEFORE.txt` -- the CT-be-1 checker (`9a570bb671`), before any CT-bf-1 change (committed @749ad4afa5).
- `SWEEP_AFTER.txt` -- the HEAD-ANCHORED rule (the rule is committed @b71565bc7e; this sweep ran 2026-10-16 ~14:41Z on that code).
- `SWEEP_CLASSIFIED.txt` -- every changed line, paired by (project, round, order, criterion), with source before and after.
- `SWEEP_AFTER_FIRST_RULE.txt`, `SWEEP_CLASSIFIED_FIRST_RULE.txt` -- the withdrawn first rule (committed @eb794aa37d), kept as record.
- A drift control (the committed first-rule checker, rerun today) matched `SWEEP_AFTER_FIRST_RULE.txt` line for line: the
  sweep reads the same trees with the same results, so the differences below are the rule's effect alone.

Measured change (JUDGMENT lines, 177 judgment criteria in both sweeps):

- 8 lines differ.
- 7 lines GRADED -> UNGRADED (the stop condition).
- 1 line GRADED -> GRADED with the source changed (verdict NOT MET both sides): ADVI_COTBKF round 12 TO-CB-l-1 CB12l1-AC3,
  investigation row ADVI_COTBKF-D2-S24 -> adjudication row ADVI_COTBKF-C-S17. Allowed (source change, verdict unchanged).
- ROUND-CLOSE lines differ: 7. Verdict changes: 3 (MAY-CLOSE -> REFUSED: ADVI_COTBKF rounds 39, 51, 52). Other changed
  lines: ADVI_COTBKF rounds 28 and 34 (REFUSED, graded 2 -> 1), ETFS_RIVALS rounds 8 and 9 (REFUSED, graded 1 -> 0).

## STOP CONDITION NOT MET -- the issuer rules

The acceptance was zero GRADED -> UNGRADED lines and zero ROUND-CLOSE verdict changes. Both fail. Per the amendment, the
80-character head is NOT widened. The seven flipped grades, each with its row id and the first 120 characters of its one_line
(verbatim, from the row in the worktree at HEAD b71565bc7e):

1. round 28, TO-CB-ab-3 CB28ab3-AC3, row `ADVI_COTBKF-D2-S41`:
   "L9 round 28: CB28ab1-AC3 NOT MET as written ('decided ... before the run' fails for one rule), but the post-run continui"
   The head names CB28ab1-AC3 (another order); the CB28ab3-AC3 MET grade sits at character 476 ("AC3 MET: cap 0.5").
2. round 34, TO-CB-ah-2 CB34ah2-AC3, row `ADVI_COTBKF-D2-S58`:
   "L9 round 34: CB34ah1-AC2 MET -- rule commit e6544ecdfe (07:04 ET) precedes output 33b729fc1b (07:06); the class cross_fi"
   The head names CB34ah1-AC2; the CB34ah2-AC3 MET grade sits at character 302 ("AC3 MET -- rule 2536c4fc09").
3. round 39, TO-CB-am-1 CB39am1-AC2, row `ADVI_COTBKF-D2-S64`:
   "L9 rounds 36 and 39: CB36aj1-AC2 MET -- other_rows_identical=True and the verify reads 38/38; the bond and diff rule com"
   The head names CB36aj1-AC2; the CB39am1-AC2 MET grade sits at character 391. (Verdict MAY-CLOSE -> REFUSED.)
4. round 51, TO-CB-ay-1 CB51ay1-AC2, row `ADVI_COTBKF-D2-S76`:
   "L9 rounds 50-52: CB50ax1-AC2 MET (served writer and B_00 equal the repo bytes, no opal_naming import, own firm and 4 key"
   The head names CB50ax1-AC2; the CB51ay1-AC2 grade sits at character 217. (Verdict MAY-CLOSE -> REFUSED.)
5. round 52, TO-CB-az-1 CB52az1-AC2, row `ADVI_COTBKF-D2-S76`: the same one_line as item 4; the CB52az1-AC2 grade sits at
   character 457. (Verdict MAY-CLOSE -> REFUSED.)
6. round 8, TO-RIV-fc-1 J1, row `ETFS_RIVALS-Z-S47` (investigation file `INVESTIGATION_v1.Z.md`):
   "The first organic full-day page (2026-10-06, batch ai-2026-10-06-517fd371, 13 of 13 funds updated) renders with holding "
   The one_line carries no criterion token. The grade ("RIV-fc-1 J1 and RIV-ln-1 J1, both graded PASS-in-part") sits in
   `spec_asserts`, which the amendment excludes (only the one_line is the head).
7. round 9, TO-RIV-ln-1 J1, row `ETFS_RIVALS-Z-S47`: the same row as item 6.

What the seven share: each is a real CVO prose grade in a multi-criterion investigation row. In items 1-5 the head of the one_line
names a different criterion of the same round, and the grade for the named order is later in the row. In items 6-7 the grade is in
`spec_asserts`. The head rule reads each row as the amendment specifies, so the rule is working as written and the flips are the
open question for the issuer: re-grade these rows as `grades` entries, move the grade to the head of the row, or decide that the
head is not the right boundary for multi-criterion rows. The rule was not widened here.

Filed: `NFRA_CTLPLN-W144-S3` (BLOCKING) in `org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md`,
carrying this list.
