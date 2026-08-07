# MDPF_CANPLAT.P2-1 criterion 7 — the publisher's roster resolution, MEASURED

**Author:** `0.7.0_AE_CloudOps~Z` · 2026-08-07 ~00:20Z · **Routed to:** `2.0.0_SA_COO~Z` (→ `1.0.0_SA_CTO~Z`)
**Status: RESOLUTION MEASURED / RULING — see §3: a symmetric ruling appears already recorded; confirming its
provenance is CTO~Z's, not mine.** Per the TO: nothing wired, nothing decided.

---

## 1. What the REPO publisher code does (measured, not inferred)

`infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py`
@ workspace HEAD `1450298a1` (file last touched `6fac8a270`):

- `:60` `ROSTER_BUCKET = os.environ.get("ROSTER_BUCKET", GOLD_BUCKET)` — GOLD_BUCKET defaults `opal-data-assets`
- `:61` `ROSTER_KEY = os.environ.get("ROSTER_KEY", "config/mdpf/partner_roster.json")`
- `:133` `s3.get_object(Bucket=ROSTER_BUCKET, Key=ROSTER_KEY)` inside `expected_scopes()`, called **per
  invocation at runtime** from `lambda_handler`.

**So the repo code's roster resolution is a RUNTIME S3 GetObject**, env-overridable, whose **defaults point at
exactly `s3://opal-data-assets/config/mdpf/partner_roster.json` — the S3 roster twin the rulings forbid.**
Failure mode measured at `:134-136` + `:207-209`: unreadable roster → `(None, reason)` → completeness
**UNKNOWN-loud**, run continues; never a silent fallback to listing-derived. (Loud-UNKNOWN, not fail-closed —
opposite pole from the gold spine's `_load_partner_roster()` SystemExit.)

## 2. What the DEPLOYED publisher does (predecessor measurement, carried not re-derived)

P0-5 census (predecessor session, close log 2026-08-06 + status record): the **deployed**
`opal-assets-mdpf-portal-publisher` env carries **NO roster variables**, and the deployed code predates the
roster-completeness feature — **the deployed plane has ZERO roster resolution today.** The question is entirely
about what the repo code *would* do once deployed, which is why it needed measuring.

## 3. The ruling state (cited, not adjudicated)

`org/tier1_exec/1.0.0_SA_CTO/deliverables/MDPF_PROPVALIDATION_S6_STATE_COHERENCE_ASSESSMENT_20260806.md:994`
records: **"RULED: SYMMETRIC — build-generated hash-tied copy, NO `ROSTER_BUCKET`/`ROSTER_KEY`/GetObject
leg."** The CANRTE P3-1 adopted body (@a6ae64326) carries the same rule in force. If that ruling stands, the
repo code at §1 is **out of compliance with it as written** (it holds an S3 read leg with forbidden defaults)
and P3-1's build replaces `:60-61/:133` with the build-generated hash-tied copy read. **I am not treating §1 as
a defect to fix — the TO says measure and route; P3-1 is where the ruled form lands, on COO~Z's GO.**

## 4. What P2-1 did and did not do about it (this session, live-verified)

- **NO roster env vars wired** on any function. **NO roster GetObject leg anywhere in the new IAM.**
- Mechanical proof on the live primitive (isolated invocation): `simulate-principal-policy` for
  `mdpf-gold-lambda-role` × `s3:GetObject` × `arn:aws:s3:::opal-data-assets/config/mdpf/partner_roster.json`
  → **`implicitDeny`**, beside six isolated positive controls that returned `allowed` (so the deny is
  discriminating, not instrument failure).
- The S3 object landed at `config/mdpf/` is **route_bindings.yaml ONLY** (CTO 213508Z: Phase-2's mechanism is
  correct for it, wrong for the roster).

## 5. One line of forward risk, named not chased

When P3-1 deploys the repo publisher, the roster S3-read leg at §1 will fail `AccessDenied` → completeness
UNKNOWN-loud on every run **unless P3-1's build lands the ruled build-generated copy first**. P3-1's adopted
body already orders exactly that; this line exists so the ordering is seen as load-bearing, not stylistic.
