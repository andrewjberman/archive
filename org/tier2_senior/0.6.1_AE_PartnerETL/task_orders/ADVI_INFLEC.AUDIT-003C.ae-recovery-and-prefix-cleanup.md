# ADVI_INFLEC.AUDIT-003C — AE 0.6.1 Recovery + Prefix Cleanup

**To:** 0.6.1_AE_PartnerETL (fresh session post-2026-05-06T~14:55Z restart)
**From:** 1.0.0_SA_CTO
**Project:** ADVI_INFLEC
**Priority:** P0 — first thing this session
**Authored:** 2026-05-06

---

## Why this TO exists (ratification — read once, do not re-read)

The prior 0.6.1_AE_PartnerETL session was terminated by Andrew at ~14:55Z on 2026-05-06 because the agent's working context had become autoregressive-anchored on a misspelled advisor token across three consecutive RAVC messages. The agent's actual SSM dispatch ran correctly and wrote correct outputs to S3. The session was terminated only because in-session correction would have reinforced the anchor.

**You (this fresh session) do not have that anchor.** This TO exists to (a) ratify the dispatch outcome that the prior session produced, (b) execute leftover cleanup work, and (c) protect this session from re-anchoring.

**Do NOT read** the following files during this TO — they contain the contaminated annotations and reading them re-introduces the failure mode:
- Any MCP message in your inbox dated 2026-05-06T143000Z..145500Z (your own outbound RAVC4/5/CLOSE)
- `org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-05/audit006_inf_i_d00c_geo_drill_prod_dispatch.md`
- `org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-05/advi_infship_a2_close_and_d02b_catalog.md`
- `org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-04/INFLEC_AUDIT_AE_ORION_VENDOR.md` (line 58 region)
- Any other file you find via `grep -l 'brandenbrug' org/tier2_senior/0.6.1_AE_PartnerETL/` — those lines are the contamination, do NOT read the surrounding paragraphs.

**Do NOT type the contaminated token** anywhere — not in commit messages, not in MCP replies, not in session logs. If you need to reference it, copy-paste from this TO or from `aws s3 ls` raw stdout.

---

## Anti-poisoning protocol (mandatory rules)

These mirror the AUDIT-003B protocol used for DS~A on 2026-05-06.

**Rule 1.** Do not type the advisor token from memory. When the token is needed, copy-paste it from one of the canonical sources listed in Phase 0.

**Rule 2.** When verifying byte-level output, use `repr()` (Python) or `od -c` / `xxd` and copy-paste the raw stdout to your reply without retyping any portion.

**Rule 3.** When CTO or any other agent asks you to verify a token spelling, **independently re-derive from canonical source** — do NOT cite your own prior message as evidence.

**Rule 4.** If you notice a discrepancy between two of your own prior messages, treat your prior messages as the unreliable source. Re-derive from S3 / Orion API / repo HEAD.

**Rule 5.** No narrative paragraphs in MCP replies for this TO. Structured fields only: command run, raw stdout, file path, byte count, ETag. Less typed prose = less anchoring surface.

**Rule 6.** If at any point you feel the urge to write the token using muscle memory, stop and grep `data/orion/scripts/silver/build_assets_dim.py` line 69 to retrieve the canonical form.

---

## Phase 0 — Ground-truth re-anchor (5 min, no inbound writes)

Run these commands and **paste the raw stdout** into your Phase 0 RAVC. Do not summarize.

```bash
# 0.1 — repo HEAD canonical mapping
grep -n "': '6'" data/orion/scripts/silver/build_assets_dim.py

# 0.2 — Orion vendor backend ground truth
grep -E '"fullName"|"lastName"' data/orion/manual_api/pulls/2026-04-29_representatives.json | head -10

# 0.3 — S3 platinum advisors prefix list (live)
aws s3 ls s3://opal-data-inf/platinum/advisors/

# 0.4 — S3 qa advisors prefix list (live; expect leftover joe_brunswick from prior cleanup)
aws s3 ls s3://opal-data-inf/qa/advisors/

# 0.5 — Canonical parquet advisor_key column (byte-literal repr)
aws s3 cp s3://opal-data-inf/gold/canonical/holdings_2026-05-05.parquet C:/tmp/h_recovery.parquet
python -c "import pandas as pd; df = pd.read_parquet('C:/tmp/h_recovery.parquet'); print(repr(sorted(df['advisor_key'].drop_duplicates().tolist())))"
```

Send Phase 0 RAVC with all 5 outputs concatenated. CTO reviews and authorizes Phase 1.

**AC for Phase 0:** all 5 outputs returned literally; none of the outputs has been retyped.

---

## Phase 1 — Ratify AUDIT-003 dispatch outcome (no new dispatch)

The prior session ran SSM CommandId `af0e7e25-2e59-4cfc-9fe3-91153a3a2d29` against `i-0ed5afded2ebd4ed4`. Outputs already on S3 (CTO independently verified):
- `platinum/firm/dashboard.json` written 2026-05-06T14:42:26Z; `headline.total_aua = $199,649,186.31` (canonical-holdings primary; aum_snapshot override skipped due to missing rep_id=6 in snapshot).
- `platinum/advisors/{rep_id_6_advisor}/top_holdings.json` written same window; 744 rows; $16,158,184.71; 55 holdings.

Your Phase 1 task: confirm both outputs land on the correct paths via Phase 0.3 list. The prefix names you observe in `aws s3 ls` are the canonical paths — copy-paste them, do not retype.

**AC for Phase 1:** Phase 0.3 stdout shows the four expected prefixes (firm-level + 3 individual advisor names); Phase 0.5 stdout shows four advisor_key values matching the prefix names byte-for-byte.

---

## Phase 2 — qa/advisors prefix cleanup (S3 prefix termination)

Phase 0.4 will show a `joe_brunswick/` prefix under `s3://opal-data-inf/qa/advisors/`. This is leftover from the AUDIT-003B advisor rename sweep — needs termination.

**Pre-confirm step (per `feedback_destructive_op_pre_confirm.md`):** before running `aws s3 rm --recursive`, send a pre-confirm MCP to CTO citing:
- The exact prefix you'll delete (copy from Phase 0.4 stdout — do not retype).
- The byte count + object count under that prefix (`aws s3 ls --recursive --summarize`).
- The fact that the canonical advisor data is preserved under the BURG-prefix path (Phase 0.3 stdout).

Wait for CTO RAVC GO before deletion. Use:
```bash
aws s3 rm --recursive "s3://opal-data-inf/qa/advisors/<paste-prefix-from-Phase-0.4>"
```

**AC for Phase 2:** post-deletion `aws s3 ls s3://opal-data-inf/qa/advisors/` returns 4 prefixes (the 4 valid advisor names + firm), no contaminated 5th.

---

## Phase 3 — Pickup in-progress work

After Phase 2 closes, resume:
- **ADVI_INFREL.001 (Fix C)** — silver chain RCA continuation if not already shipped.
- **ADVI_INFINGE.005b** — txn-v2-lambda-migration once CTO output-path ruling lands (gate not yet released).

Standing aside from those: any further ADVI_INFLEC AUDIT/DIAGFIX work is outside this TO scope.

---

## Acceptance criteria summary

| AC | Description | Verification |
|----|-------------|--------------|
| AC1 | Phase 0 stdout (all 5 commands) returned literally without retyping | CTO inspection |
| AC2 | Phase 1 ratification confirms 4 valid platinum/advisors prefixes | Phase 0.3 stdout |
| AC3 | Phase 2 pre-confirm received CTO GO before any `aws s3 rm` | MCP audit |
| AC4 | Phase 2 post-deletion shows 4 (not 5) prefixes under qa/advisors/ | `aws s3 ls` |
| AC5 | Zero instances of the contaminated token typed in any MCP reply, commit message, or session log written during this TO | grep your own outputs |

---

## Session log path

`org/tier2_senior/0.6.1_AE_PartnerETL/logs/2026-05-06/audit003c_recovery_session.md` — write Phase summaries only with structured fields. No narrative paragraphs.

---

## Close

Close TO via single MCP to CTO with all 5 ACs marked PASS and final S3 ls stdout (Phase 2 post-deletion). CTO ratifies → close registered in ADVI_INFLEC project JSON.

— 1.0.0_SA_CTO 2026-05-06
