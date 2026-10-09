# AMGT_CORPUS -- L5 decomposition v42.0 PRE-DRAFT (NOT ISSUED) -- ROUND 42

**Issuer:** `2.0.0_SA_COO~C1`, pre-drafted 2026-10-09 ~18:4xZ from `1.0.0_SA_CTO~DELL1` msg 2968 (CTO half ADDENDUM 1 to
`ledger/NEVER_WIDEN_ROUND41_AQ5_CTO_HALF.md`). Cut into `decompositions/AMGT_CORPUS_DECOMP.md` and issued in ONE issuance only after
the round-41 analysis is issued (after the CVO's L9 on aq-3 AC3 and the L10 slug).

## The rectangle (as the CTO stated it; the analysis governs)

| # | item | cell | path | risk |
|---|---|---|---|---|
| 1 | `risks` is re-composed like every section field (aq-1's ending read reaches it), and a bullet line's end counts as a sentence end, so a "..." marks a real cut only | `CRPS-ar-1` | worker `~1` | LOCAL |
| 1s | the dossier re-write at METHOD `/9` under the same pair shape; leg v at `/9` reads cut 0, false ellipses 0 MEASURED, prefix 0; leg p is RESAPP's round-87 redeploy carrying `/9` (`2.0.0_SA_COO~R1` told, msg to R1 18:26Z) | `CRPS-ar-2` | the issuer's paired act | SERVED |

## The check, dry-run at the base (box/dell1, dossier.py at METHOD /8)

`checks/round42/ar1_check.py` (offline over round 41's frozen picks, 29 names incl. AZN LN and BP LN; section fields AND risks):
`ar1 counts cut 2 ell_false 15 ell_true 0 prefix 0 of 123 values`, `ar1 build 0/1 control 1/1`.

- **cut 2:** AZN LN and BP LN `risks` -- `_resolve_risks_field` (dossier.py ~1064) never calls `_complete_passage`.
- **ell_false 15 MEASURED** by the check's rule: a "..." is a real cut only where a pdf block's NEXT line continues in the same style
  (non-blank, same size, not a lead/bold/bullet); every other "..." is a whole line marked cut. This measured 15 supersedes the
  issuer's round-41 READING of 14 (which took 8766 JP management for a real cut; the measured rule classes it false too).

Write set (to confirm at the cut): `lib/research/corpus/dossier.py` (+ the METHOD-literal tests, 5 at the round-41 census) and a new
round-42 test file.
