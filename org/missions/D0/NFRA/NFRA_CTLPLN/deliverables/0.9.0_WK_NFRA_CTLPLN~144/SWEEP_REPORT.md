# CT-bf-1 regression sweep -- round-close-check.py before and after the grade-not-a-mention rule

Denominator: 232 runs = 232 (project, round) pairs from `org/missions/D*/*/*/decompositions/*DECOMP.round*.md` at HEAD, over 9 tree projects (ADVI_COTBKF 102, AMGT_CORPUS 48, COMM_ASSIST 13, LGIC_BLANKFIX 13, NFRA_CTLPLN 27, ETFS_RIVALS 11, NFRA_DEVPLN 9, IRPT_CUSTDY 6, NFRA_GATSCP 3). Each run: `python .tools/round-close-check.py --project <CODE> --round <n>`, timeout 120. Result: 0 timeouts, 0 non-zero exits, both sweeps.

Files (this folder):

- `SWEEP_BEFORE.txt` -- JUDGMENT and ROUND-CLOSE lines per run, before the change (committed @749ad4afa5).
- `SWEEP_AFTER.txt` -- the same, after the change.
- `SWEEP_CLASSIFIED.txt` -- every changed line, paired by (project, round, order, criterion), with the grading source before and after.

Measured change (JUDGMENT lines, 177 judgment criteria in both sweeps):

- 59 lines differ.
- 52 lines GRADED -> UNGRADED: 50 ADVI_COTBKF, 2 ETFS_RIVALS. Every one was graded by a CVO prose line in an INVESTIGATION row with no `grades` entry (the checker's own detail says "names it in prose only").
- 5 lines GRADED -> GRADED with the source changed (investigation row -> adjudication row), verdict unchanged (ADVI_COTBKF rounds 12, 53, 61, 66, 71).
- 2 lines GRADED -> GRADED, detail only (ADVI_COTBKF rounds 38, 61).
- ROUND-CLOSE lines: 38 differ (36 ADVI_COTBKF, 2 ETFS_RIVALS). 27 move MAY-CLOSE -> REFUSED (all ADVI_COTBKF); 11 stay REFUSED with a lower graded count.

Example of the flipped grade (verbatim, ADVI_COTBKF-D2-S30, `org/missions/D8/ADVI/ADVI_COTBKF/surprise-channel/investigations/INVESTIGATION_v1.md` @41f01e24e9 lines 2099-2118): one_line "L9 CB19s1-AC3 MET (the sweep list is a declared list ...". No `grades` key.

Stop condition (the order's rule): a project whose CVO graded only by prose in an investigation row would now read UNGRADED. That happened. The rule was NOT widened. BLOCKING rows filed in `org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md`: `NFRA_CTLPLN-W144-S1` (ADVI_COTBKF, all 50 flips named in notes) and `NFRA_CTLPLN-W144-S2` (ETFS_RIVALS, 2 flips). The issuer 2.0.0_SA_COO~C rules: re-grade these as `grades` entries, or widen the rule.
