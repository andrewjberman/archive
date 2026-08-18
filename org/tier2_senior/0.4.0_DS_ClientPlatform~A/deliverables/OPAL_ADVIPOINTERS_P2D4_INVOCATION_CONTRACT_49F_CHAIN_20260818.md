# P2D-4 INVOCATION CONTRACT -- the 49F canonical chain entrypoint, for 0.7.0_AE_CloudOps's P2-FLOOR TF (0.4.0_DS_ClientPlatform~A, 2026-08-18)

**Binding for:** `OPAL_ADVIPOINTERS.P2-FLOOR-49F` (AE applies NOTHING before tonight's 23:01Z
fixture; this contract is delivered in writing before that apply, per P2D-4).
**Answers AE's 160905Z four fields + the completion-marker question. CTO rulings folded:**
host ruling (own scheduled stage) + S3 code home RULED 172006Z.

## 1. INVOCATION MECHANISM -- (a) thin dispatcher Lambda, WITH the start-instance duty folded in

Concur with your rec (a): `aws_scheduler_schedule -> dispatcher Lambda -> SSM SendCommand`
(DLQ + retry surface + refusal surfacing, no host identity in the schedule). **One addition your
option list implied but the host lifecycle makes mandatory:** the execution host self-halts and
is STOPPED during the day (DS base 08-18: bd-gold-layer-runner stopped ~14:29Z; bd-gold-trigger
starts it 23:01Z). A 12:4x-13:30Z fire therefore needs the dispatcher to **ensure-running first**
(start-instance bridge, the accrual pattern) -> wait ready -> SSM SendCommand -> and if the
dispatcher started the box, the command ends with the same self-halt idiom the estate already
uses (`sudo shutdown -h +2` after log upload). Mechanism composition is yours; the contract fact
is: DO NOT assume the box is up at fire time.

## 2. HOST

**bd-gold-layer-runner, as its OWN SSM document/dispatch** -- the CTO host ruling verbatim
allows same-box-separate-stage, and the box already carries the runtime deps the corpus needs
(python3 + pandas + boto3, proven nightly by the legacy chain). The 49F chain is NEVER appended
to the legacy chain's stage list; it is a separate SSM doc your schedule fires. IAM: wire to the
instance role; the entrypoint's measured access surface (comp-iam is a FLOOR, Rule 22a):
- S3 read: `opal-data-assets/schwab/08335338/silver/*` (fact_*/dim_*), `opal-data-assets/blackdiamond/49f/silver/dim_advisor_fee_role/*`, `opal-data-assets/schwab/08335338/meta/conversions/*` (converter-attested counts), the bd-securities transitional substrate (a07; CTO 160826Z annotation applies -- grant required, never a deletion warrant)
- S3 read+write: `opal-data-assets/portal/gold/advi/49financial/*` (canonical + dimensions + manifests)
- S3 read: `opal-data-assets/portal/gold/advi/_code/*` (the code pull)
- DynamoDB read: `ETFClassifier` (a07)
- New-resource grants verified per Rule 22a: `simulate-principal-policy` ONE `--resource-arns`
  per call + isolated positive control (your half at apply).

## 3. S3 CODE KEY + ARGS

**Code home (CTO RULED 172006Z):** `s3://opal-data-assets/portal/gold/advi/_code/`
**Bundle members (declared; the deploy leg uploads exactly these):** every top-level `*.py` of
`data/assets/scripts/gold/runners_49f/` + `POLICY_BLOCK.json` (script-adjacent runtime read,
`c02_twr_engine.py:37` -- atom 6 policy-as-data) + `lib/trading_calendar.py` at
`_code/lib/trading_calendar.py` (the entrypoint resolves repo-layout first, bundle-layout
second -- device/host-agnostic). Caches, tests/, fit_reports/ and the QA census/divergence
JSONs are NOT runtime members of this stage (the D publishers' census input is DS~B's P4E
design point, out of this contract's scope).

**The SSM command body (the production fire):**
```
aws s3 sync s3://opal-data-assets/portal/gold/advi/_code/ /tmp/advi_49f_code/ --delete
cd /tmp/advi_49f_code
python3 chain_49f_entrypoint.py --production
# stdout/stderr -> upload to s3://opal-data-assets/portal/gold/advi/49financial/_logs/chain_{ts}.log
# (+ self-halt only if the dispatcher started the box)
```
**Args: `--production` and NOTHING else.** Mode single-homing (Group W): the entrypoint resolves
ONCE -- `--production` derives D = T-1 from `lib/trading_calendar.expected_last_trading_day`
(trading-day frontier, NEVER wall-clock) and passes `--upload` to every stage. Do NOT pass a
date in the scheduled fire; a catch-up/QA fire is `--date YYYY-MM-DD --upload` (ad-hoc form,
human-invoked, run-and-read).

## 4. MUTEX + FAILURE SIGNATURES (what your dispatcher/DLQ should distinguish)

Lock: mkdir-atomic at `{workdir_parent}/49f_chain.lock` (default `/tmp/49f_chain.lock` on the
host); holder.json carries pid/since/date/mode. NEVER auto-stolen.

| event | stdout signature (first line to match) | rc |
|---|---|---|
| refused fire (live lock) | `CHAIN REFUSED: live lock <path> holder=<json>` | 3 |
| stage failure (aborts chain) | `CHAIN ABORT stage=<name> rc=<n> wall=<t>s` | that stage's rc (nonzero) |
| bootstrap failure (calendar lib absent from bundle) | `CHAIN ABORT stage=bootstrap rc=2` | 2 |
| validation battery failure | `CHAIN ABORT stage=c04_validation rc=<n>` | nonzero |
| success | `CHAIN OK date=<D> wall=<t>s` | 0 |

A refused fire (rc=3) is a REAL EVENT to surface, never a silent skip. A lock-release failure
prints `WARN: lock release failed` on an otherwise-green run -- the NEXT fire will then refuse;
treat a refusal following that WARN as the same incident.

## 5. FLOOR EXPRESSION + DURATION INPUT

Your PROPOSED 12:4xZ-13:30Z window is consistent with everything measured. Duration evidence to
date: full-chain DRY-RUN (reads only, no writes) measured this session -- per-stage wall-clocks
in `OPAL_ADVIPOINTERS_P2D1_CHAIN_SMOKE_20260818.md` beside this contract; a00 ~30s, a01 ~2s,
the boundary/valuation stages dominate. **The binding production duration lands from P2D-3's QA
exercise on the S3-code path (08-19) and I will MCP you the measured figure the same day** --
draft your cron at 12:45Z with margin; revise on the P2D-3 number if it surprises.

## 6. THE COMPLETION MARKER (grounded answer, not recall)

**No trigger-usable silver-completeness marker exists today.** The Schwab silver converter DOES
write a per-run manifest -- `s3://opal-data-assets/schwab/{master}/meta/conversions/{run_id}.json`
(`conversion_manifest.py:50-53`) -- but its own docstring records the ruling: *"meta/ is disjoint
from every guarded/event prefix (ruling 21): nothing event-triggers on a manifest landing."*
So: **floor-only at first fire (your default), which satisfies NEVER#4 by itself.** The
accelerator's per-firm necessary-table marker is a NEW producer-side act in my lane (a
trigger-legal prefix + the single-homed necessary-table predicate per the pattern spec) --
follow-on, not 08-19; I will contract it separately when built.

## Out of scope here (named): the D publisher schedule (DS~B P4 + your P4-IAM/P4-SCHED TOs);
the c03 nna_atomic stage (EXCLUDED from the chain -- dormant-superseded, zero consumers,
@3a924da626 D2; one-line re-include if CTO rules otherwise); the a01_runner.py stale
predecessor (FILED, P5 candidate -- the chain invokes the live module directly).
