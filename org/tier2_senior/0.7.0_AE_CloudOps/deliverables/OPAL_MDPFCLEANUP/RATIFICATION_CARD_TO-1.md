# OPAL_MDPFCLEANUP — TO-1 RATIFICATION CARD (for Andrew, via COO card mechanism)

**Assembled:** 2026-08-14 ~17:5xZ by 0.7.0_AE_CloudOps · **Evidence base:** proof_TO-0 @15c2105781
(COO-validated 7/7) + the two pre-card reads (both CLOSED at the strongest plane, cited inline).
**The ask:** your word converts K-classes into the authorized kill set. Any row you dispute = KEEP.
**Reserved split, plainly:** stopping EC2 and deleting S3 objects are YOUR categories (standing
law); TF destroys of rules/schedules/Lambdas/alarms and code-path retirements are non-reserved and
execute on your one ratifying word per class.

---

## PRE-CARD READS (both closed, so this card carries no residuals)

1. **The serving repoint is APPLIED-plane confirmed.** The live distribution (EVTSA9VEHNZVH)
   binds `public-data-router:6` on `/api/general/*`; that version's DEPLOYED 332-byte source
   rewrites `/api/general/mdpf/` → `/platinum/mdpf/` (downloaded + read verbatim). json/mdpf is
   off the serving route at the deployed edge, not just in committed source.
2. **The adjacent `json/portfolios/account-distribution.json` is FE-dead.** portal/src
   `aum.ts:490-491` verbatim: *"the legacy json/portfolios/account-distribution.json read is
   dead. Every scope, Global included, reads the canonical platinum/mdpf/{scope}/account-
   distribution.json"*; the live fetch (`aum.ts:531`) requests `/api/general/mdpf/{firmId}/...`
   → platinum. So the kill scope offered below is the WHOLE 11:30Z job leg, not rule-only.
   *(Plane note: portal source at HEAD + the CANPLAT promote record; the deployed SPA bundle was
   promoted post-flip.)*

---

## WAVE 1 — NON-RESERVED (TF destroys + one code-path retirement; consumers-first ordering inside)

**Class K1 — DEAD-DISABLED (remedy: TF destroy, rule+Lambda+alarm together per resource):**
| Resource | Evidence |
|---|---|
| `bd-49f-runner` + `bd-49f-runner-daily` rule | rule DISABLED (cron 0 2Z), no 7d fires |
| `bd-49f-fees-runner` + `bd-49f-fees-runner-daily` rule | rule DISABLED, no 7d fires |
| `smartx-ec2-autostart` + `smartx-daily-export-trigger` rule | rule DISABLED (its EC2 is Wave-2) |
| `smartx-model-monthly-pull` Lambda | trigger ABSENT in BOTH namespaces (PRD said "disabled" — it is already gone); Lambda sits trigger-less |

**Class K2 — SUPERSEDED (remedy: retire consumers-first; successor live+proven):**
| Resource | Evidence |
|---|---|
| `smartx-account-distribution-daily` rule + the `{"job":"account_distribution"}` leg of `opal-smartx-ingestion-pipeline` (code-path retirement; the Lambda itself is KEEP for its main smartx jobs) | TO-0 claim b1: writes json/mdpf/{49f,inf}/account-distribution daily 11:30:39Z + json/portfolios/account-distribution (global) + a stale-input aum-metrics leg — ALL off-route per pre-card reads 1+2. Successor: publisher→platinum account-distribution ×4 scopes, live 17:35:41Z |
| `cot-session-complete` events-rule | fired 1x/7d while the chain completes daily — dead/schema-mismatched event leg (TRGALN-surfaced) |

## WAVE 2 — RESERVED (each class on YOUR word, per class; copy-manifest-first + DELTA accounting per the PRD)

**EC2 stops/terminations (your category):**
| Resource | State + gating |
|---|---|
| `mdpf-daily-runner` (i-02448edb624a7a7cf) | RUNNING since the morning fire; STOP is immediate-eligible on your word; TERMINATE gates on TO-2 (the dim re-home — this chain is the ONLY dim_model_portfolio producer, K3) |
| `smartx-exporter` (i-06ebcb27395eb3f49) | already stopped; TERMINATE on your word |

**S3 deletions (your category; NEVER#3 discipline on anything served-shaped):**
| Keys | Evidence + dating |
|---|---|
| `json/mdpf/*` (10 objects) | off-route at deployed edge (read 1); 2 keys still written daily by the K2 job (writer retires in Wave 1 FIRST, then these age dead); aggregate keys stale since 07-28 |
| `json/portfolios/account-distribution.json` (+ the job's aum-metrics twin if you rule it) | FE-dead (read 2); written daily by the same K2 job until Wave 1 retires it |
| `opal-data-mdpf` `cache/` (1 obj) | 87d stale — crosses the Rule-25 90d bar 2026-08-17; no declared exception; no code consumer found |
| `opal-data-mdpf` `bmkaud-evidence/` (10 objs) | 74d stale; not yet at the bar — dated honestly, your call to include or hold |
| `opal-data-mdpf` `mdpf/feeds/*` (1,214 objs) | NOT YET — live-consumed daily (K3-coupled); becomes deletable only after Wave 1 (job retire) + TO-2 (chain re-home) both land |

## K3 — NOT KILLABLE YET (listed so the sequence is visible; no word sought today)

`mdpf-daily-refresh-trigger` → `mdpf-daily-trigger` → runner EC2 chain (+ DLQ + 2 alarms +
`code/mdpf-daily-dispatch.sh`) · `wsb-49f-model-aua-daily` + `wsd-49f-partner-held-etf-daily` +
their schedulers (feeders to feeds/*): all gated on TO-2's dim re-home; wsb/wsd additionally on
Wave 1's job retirement (their last non-K3 consumer). Dependency chain: Wave 1 → TO-2 → these.

## KEEP CONFIRMATIONS (protected from every sweep above)

The §1 canonical set · `opal-data-mdpf/telemetry/` (live ops, written 17:35:33Z today) ·
`opal-data-mdpf/code/` (the Rule-12 S3 deploy home, written 17:28Z today — the PRD §3 K4 row
EXCLUDES it) · `platinum/mdpf/archive/` (444 objs, 8d — all underscore keys are this tree; no
live/dormant twins) · `opal-smartx-ingestion-pipeline` (KEEP; only its account_distribution JOB
LEG retires) · `yang-model-portfolio-benchmarks` (name-collision exclusion).
