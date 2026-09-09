# EG-sb-7 -- rung 3 STOPS AND ASKS A PERSON

**TO:** `ETFS_GUARDRAIL.TO-EG-sb-7` · **Worker:** `0.9.0_WK_ETFS_GUARDRAIL~1` · **Worktree HEAD:** `745cd6b354` (branch `wk-ETFS_GUARDRAIL-1`) · **Verb:** wire.

## Module extended

`data/etfs/scripts/coverage/remediate.py`: added `rung3_stop_and_ask(partner, month, unresolved, *, s3=None, write=True) -> dict` and wired it into `remediate_month` as its LAST step, firing only when `unresolved` is non-empty AND `dry_run` is False (a plan is not a confirmed failure). Two new arms added to `data/etfs/scripts/coverage/tests/test_remediate.py` (arm (e)'s assertion was also updated -- see below).

## 1. S7B-AC1 -- the battery, 8 arms (N = EG-s-7's 6 + 2)

**Invocation:**
```
python -m pytest data/etfs/scripts/coverage/tests/test_remediate.py -q
```
**Output (rc=0):**
```
8 passed in 0.06s
```
New arms: (g) two D days for two different partners (cottonwood/inflection) -> the combined asks name both dates, both partners (`cottonwood`, `inflection`), both providers (`Black Diamond`, `Orion`), exactly one `put_object` per call (2 total), zero `head_object` calls; (h) zero `unresolved` -> `rung3_stop_and_ask` returns `asks: []` and makes NO write, and a fully-covered month's `remediate_month` result carries no `"ask"` key at all.

**Arm (e) revised, not weakened:** the original EG-s-7 assertion `s3.put_object_calls == []` is no longer the correct invariant once rung 3 exists -- a month with unresolved days is now SUPPOSED to write one ask. Renamed `test_ladder_never_writes_a_data_slice_only_the_ask`, now asserting (i) no `put_object` call ever targets a `daily/<partner>/*.json` key (rungs 1-2's own no-fabrication property, unchanged) and (ii) exactly one `put_object` call happens, targeting `platinum/reports/<month>/coverage_egress_ask.json`, carrying both of the fixture's unresolved days.

## 2. S7B-AC2 -- still no HTTP client; exactly one ask-writer

**Invocation:**
```
python -c "import re; s=open('data/etfs/scripts/coverage/remediate.py').read(); print('HTTP_CLIENT_IMPORTS=%d ASK_WRITER=%d' % (len(re.findall(r'^\s*(?:import|from)\s+(?:requests|urllib|http)\b', s, re.M)), len(re.findall(r'def rung3_stop_and_ask\(', s))))"
```
**Output (rc=0):**
```
HTTP_CLIENT_IMPORTS=0 ASK_WRITER=1
```

## 3. S7B-AC3 -- the ask names the date, provider, and per-use authorization

**Invocation:**
```
python -c "import json,sys; sys.path.insert(0,'data/etfs/scripts'); from coverage import remediate as r; a=r.rung3_stop_and_ask('cottonwood','2026-08',[{'date':'2026-08-04','class':'D','reason':'no partition'}], write=False); print('ASKS=%d PROVIDER=%s AUTH=%s' % (len(a['asks']), a['asks'][0]['provider'], a['authorization'][:8]))"
```
**Output (rc=0):**
```
ASKS=1 PROVIDER=Black Diamond AUTH=PER-USE
```
`write=False` -- no `s3` was even passed, and the function made no attempt to call one (the `write and asks and s3 is not None` guard short-circuits on `write=False` alone).

## 4. S7B-AC4 -- commit gate clean

**Invocation:**
```
bash .tools/commit-gate.sh data/etfs/scripts/coverage/remediate.py data/etfs/scripts/coverage/tests/test_remediate.py
```
**Output (rc=0):**
```
OK: pre-commit gate clean for 2 of 2 file(s)
```

## 5. The ask's JSON shape (example, from arm (g) combined)

```json
{
  "month": "2026-08",
  "generated_at": "2026-09-05T03:43:04.683767+00:00",
  "asks": [
    {
      "date": "2026-08-04",
      "partner": "cottonwood",
      "provider": "Black Diamond",
      "class": "D",
      "reason": "no fact_holdings partition for date 2026-08-04"
    }
  ],
  "authorization": "PER-USE -- a person decides; nothing here is executed by any process"
}
```
(measured directly via `rung3_stop_and_ask('cottonwood','2026-08',[...], write=False)`, `json.dumps(..., indent=2)`, this session.)
Written (when `write=True` and non-empty) to `s3://opal-data-etfs/platinum/reports/<month>/coverage_egress_ask.json` -- the reporter box's role already writes `platinum/reports/*` (S7-AC7 in `EG-s-7`'s own record; `WriteReports` Sid, `infra/aws/terraform/etfs-reports/iam.tf`), and the orchestrator (`EG-s-8`, not this order) already reads that prefix.

## 6. The provider map, with sources

| partner | provider | source |
|---|---|---|
| `cottonwood` | Black Diamond | the monolith's `blackdiamond/cottonwood/` upstream (this TO's own text) |
| `49financial` | Schwab | `schwab/08242234/` (this TO's own text) |
| `inflection` | Orion | `EG-s-12`'s measured answer (`inflection-deployed-bytes-vs-build-input.result.md`): the DEPLOYED `inf-etf-ownership-daily` reads `opal-data-inf/gold/canonical/holdings_<date>.parquet` -- the legacy monolith path; Orion is the vendor behind it, per the coordinator's hand-off confirmation |

## 7. S7B-AC5 -- THE ANSWER (judgment; recorded, no verdict)

- **Rung 3 is a DIFFERENT ACTOR, not a later automated step:** `rung3_stop_and_ask` accepts no `invoke` parameter at all -- there is nothing in its signature FOR it to call a producer or a provider with. It writes one artifact (a request) and returns; `authorization` states `"PER-USE -- a person decides; nothing here is executed by any process"` inside the artifact itself, not merely in a comment.
- **No standing egress grant exists anywhere this order touched:** the module carries `HTTP_CLIENT_IMPORTS=0` (S7B-AC2); no credential, secret, or provider SDK is imported or referenced anywhere in `remediate.py`; the only IAM surface this project ever granted (`EG-s-7`) is `lambda:InvokeFunction` on the three IN-ESTATE producers, never a Black Diamond / Schwab / Orion credential.
- **The ask is complete enough that a person can say yes without a follow-up question:** every entry names `date`, `partner`, `provider` AND `class`/`reason` (arm (g) asserts all four fields on both partners' asks); a person reading the artifact knows exactly which day, whose data, and from which vendor, without needing to ask this system anything back.
- **The ask never fabricates and never fires prematurely:** it fires only over `unresolved` days (never `expected_empty`/B days, which are correct-as-is); it does NOT fire under `dry_run=True` (arm (f) confirms no `"ask"` key when nothing was actually attempted); with zero unresolved, `asks: []` and no write happens at all (arm (h)).
- **Rung 3 does not leave Opal on its own:** the artifact write is scoped to `opal-data-etfs` (the SAME bucket rungs 1-2 already read/check), never any provider endpoint; the egress ITSELF -- actually contacting Black Diamond/Schwab/Orion -- is not this module's act at all, and cannot be, since it holds no such capability.

## 8. Push state (measured at report)

```
git ls-remote origin refs/heads/CLOUD
```
