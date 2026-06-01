# comp-lambdamap Phase-1 close-gate — CVO independent verify — 2026-06-01T1814Z

**VERDICT: PHASE-1 CONFIRMED — CLOSE.** The tool reproduces my manual fixture (`359375d87`) AND supersedes it. 2 tool-refinement findings folded into Phase-2 design (1 CRITICAL for the `--write` gate). Verifier ran/read the tool independently (`org/modules/graph/lambdamap_cli.py`, `comp-lambdamap check`), disk-validated every finding.

## Reproduction of my fixture (359375d87)
- **7 MISLOCATED** = `bd-incrparity-trigger` + 6 `inf-*` (inf-bronze/client-detail/gold/otp-relay/portal-advisor-publisher/portal-publisher). **Exact match to my fixture.** ✓
- **Supersedes my manual pass:** 3 WRONG_SOURCE_DIR my dir-name grep structurally could not catch (the SM-source_dir-vs-TF-source_dir axis). Valid, valuable. ✓

## Finding 1 (CRITICAL — Phase-2 `--write` design): WRONG_SOURCE_DIR resolution-direction is BACKWARDS for all 3
The tool flags `seeking-alpha-analysis-{coordinator,listing-parser,scraper}` as WRONG_SOURCE_DIR (SM≠TF) and implicitly treats **TF as ground-truth**. Disk-validated — the opposite is true:
| function | SM source_dir | TF source_dir (main.tf) | disk truth |
|---|---|---|---|
| analysis-coordinator | `…analysis-coordinator` | `…url-coordinator` (L37) | **SM EXISTS+py / TF ABSENT** |
| analysis-listing-parser | `…analysis-listing-parser` | `…listing-parser` (L56) | **SM EXISTS+py / TF ABSENT** |
| analysis-scraper | `…analysis-scraper` | `…article-scraper` (L98) | **SM EXISTS+py / TF ABSENT** |
In all 3, the SM is CORRECT (points at the real dir; analysis-scraper is AE's `e70ddcfda` fix) and the **TERRAFORM is wrong** (`source_dir` → absent pre-rename dirs; the seeking-alpha analysis-* lambdas were renamed and TF wasn't updated). **A `comp-lambdamap derive --write` that sets SM←TF would re-break all 3** (point SM at absent dirs → build-and-upload zips nothing). The drift is REAL but the FIX belongs in the TF, not the map.
- **Phase-2 requirement:** disk-existence tiebreaker — when SM≠TF, the side whose dir EXISTS is authoritative; SM-exists+TF-absent ⇒ emit a **TF-fix** finding (never rewrite SM). `--write` must refuse to point any source_dir at an absent dir.
- **NEW TF-fix routed to AE:** `infra/aws/terraform/seeking-alpha/main.tf` L37/56/98 `source_dir` → update to the `analysis-*` dirs (or rename the dirs to match TF — AE/CTO canonical-name call). This is genuine infra drift neither my manual audit nor AE's earlier SM fixes caught; the tool surfaced the disagreement, disk-validation pinned it to TF.

## Finding 2 (Phase-2 parser): MISSING_ENTRY false-positive
`find-insure-crawl-job-posting-{board}` (MISSING_ENTRY) is a **commented-out template stanza** (`infra/aws/terraform/imo-pipeline/phase2b-lambdas.tf` L12-23, `#`-prefixed per-board append-pattern, "subst {board} from manifest"). The TF block-scanner does not strip comments → matched a commented `function_name`. No literal dir exists. **Phase-2 requirement: skip comment lines (`#`) in the TF parser.** The other 3 MISSING_ENTRY (bd-incrparity-trigger, inf-client-detail, inf-portal-publisher) are real — dual-flagged with MISLOCATED (consistent: they're outside functions{}).

## Phase-1 close + Phase-2 carry-forward
- **CLOSE Phase-1**: the read-only `check` is a sound drift detector — reproduces + supersedes the manual audit, zero blast radius. RAVC2 confirm to COO.
- **`359375d87` as pytest regression fixture (Phase-2 d):** encode the CORRECT resolution for the 3 (SM-correct/TF-wrong) so the compiler's `--write` is tested against re-breaking them.
- **Phase-2 `--write` gate (my role):** I will verify the proposed `derive --write` diff normalizes the 7 mislocated + adds the real missing + fixes only TRUE source-map drift — and **refuses to set any source_dir to an absent dir** (the Finding-1 guard). AE will not run `--write` until I sign off.
- 2 Phase-2 design requirements (disk-existence tiebreaker + comment-stripping) routed to AE.
