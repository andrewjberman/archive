# CALL -- the Anthropic key for 2.0.0_SA_COO~R2's session (AMGT_RESAPP, workstream AIFILL, 2026-10-16)

**The call:** may `2.0.0_SA_COO~R2` have `ANTHROPIC_API_KEY` in its shell environment, as the session that ran the producer on 2026-10-13 had it, so the issuer can run the grounding pass live?

**What created it (measured 2026-10-16 ~03:0xZ):** `python -m lib.research.aifill.run --key ASML_NA_Equity --out <dir>` on this box prints `BLOCKED: ANTHROPIC_API_KEY is not set` and stops before any model call. The key is read from that one variable (`lib/research/aifill/model.py` line 25) and nowhere else; this seat has not looked for it elsewhere and will not. A `--no-model` run works (document VALID, 5 blocks all NONE) and proves only the plumbing.

**What it gates:** the CTO's grade for round 106 (`ledger/CTO_RULING_FWD41_FIVE_NAME_READ_NOT_MET_20261014.md` item 4): "re-run all 95 names, re-validate them, then the CVO reads five NEW names drawn by sha256 over the date. The blocks return to the page only after that read is MET." In order:
1. One LOCAL live run (one name, `--out` a local folder, a local file only): the first real sample of the grounding record, including whether the model names a contradicting source (the one thing `AMGT-gs-1` could only test with stubs). Cost about 13 cents plus the grounding call (the 2026-10-13 web-search measure, `AMGT_RESAPP_AIFILL_DECOMP.md` section 2).
2. The 95-name re-run under the CTO's 150 USD ceiling (ruling item 5, "under Andrew's word on the Anthropic path"), stopping and reporting if it would exceed it.
3. The S3 write of the 95 documents: a never-widen sign-off (CTO + COO) is needed and is NOT asked here. Facts for it, measured now: address `s3://opal-data-harvest/amgt/harvest/gold/ai_fill/security_key=<KEY>/ai_fill.json` (printed by the run's DRY-RUN line); bucket `opal-data-harvest` versioning `Enabled`; the ASML object was last written 2026-10-14T03:08:03Z, 3,985 bytes, VersionId `Rvzofoe9.aphOdwDynb3av.3bCVJ0o0k`, so the rollback per key is restoring the prior VersionId. The AI-fill hold stays on the served API throughout, so no page reads these documents until the CTO lifts it.
4. `revalidate` over the 95, then the CVO's five-name read.

**REC:** yes, provision the key into this seat's launch environment, for the one local run first. Without it the seat does the work around it (the sign-off draft once the writers of the property are counted) and ticks WAITING.

-- 2.0.0_SA_COO~R2
