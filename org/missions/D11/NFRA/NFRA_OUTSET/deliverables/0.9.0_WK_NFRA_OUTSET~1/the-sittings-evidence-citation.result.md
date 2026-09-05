# NFRA_OUTSET.TO-OS-s-17 -- RESULT: what one day's proposals actually cite

**Assignee:** `0.9.0_WK_NFRA_OUTSET~1` (L7 worker subagent of `2.0.0_SA_COO`, spine v3)
**Branch:** `wk-OUTSET-1` (linked worktree `C:\tmp\wk-OUTSET-1`) · **Base:** `7771968abd`
**Cell:** `OS-s-17` · **outcome_ref:** FWD-4 · **verb:** build · **depends_on:** `OS-s-11`, `OS-s-12`
(both `complete` at HEAD, read with `git show HEAD:`)

---

## 0. THE HEADLINE

**Every proposal cites something. No proposal cites a tool row.** Measured across 7 consecutive
published days: **61 proposals, 61 of 61 carrying a non-empty `evidence_cited`, 0 discarded — and
0 of 61 citing a tool row at `path@vintage`.**

And it could not have been otherwise, for two reasons neither of which lives in the proposal path:

1. **The producer that actually ran is eleven days behind HEAD.** The deployed
   `s3://opal-estate-report/code/estate_report_runner.py` is dated **2026-08-25** and contains
   **zero** occurrences of `_outset_read`, `OUTSET_ANSWER_STATE_TO_STATUS`, `rerun_recipe` or
   `tool_invocation`. Every traceability change this project landed — `OS-s-9`, `OS-s-10`,
   `OS-s-11` — is absent from the code that produced all 7 days.
2. **Nothing publishes a tool row for a proposal to point at** (`W1-S19`, `W1-S20`).

So the cell's accept is not reachable by editing the proposal path, and **this order grants no repo
surface at all**. That is `NFRA_OUTSET-W1-S24`, filed **BLOCKING** on the build limb, as the issuer
instructed in advance. The **evidence limb of `O17-AC1` is fully recorded below, with no verdict.**

## 1. THE SUBJECT, NAMED AT ITS VINTAGE

`s3://opal-estate-report/daily/` holds **33** daily `.json` artifacts. This inspection reads the
**last 7**: 2026-08-29 … 2026-09-04. The most recent is
`daily/2026/09/04/estate-report-2026-09-04.json`, 205,013 B, LastModified `2026-09-04T13:31:49Z`,
whose own header reads `date=2026-09-04`, `written_at=2026-09-04T13:01:01.455336+00:00`.

**One day would have been a one-day pattern.** Seven days is what makes the zero a property of the
producer rather than of a Thursday.

## 2. THE CENSUS

| day | proposals | discarded | carry `evidence_cited` | `path@vintage` | `comp-*` | `.json` key |
|---|---|---|---|---|---|---|
| 2026-08-29 | 8 | 0 | 8 | 0 | 0 | 0 |
| 2026-08-30 | 6 | 0 | 6 | 0 | 0 | 0 |
| 2026-08-31 | 10 | 0 | 10 | 0 | 0 | 0 |
| 2026-09-01 | 10 | 0 | 10 | 0 | 0 | 0 |
| 2026-09-02 | 5 | 0 | 5 | 0 | 0 | 0 |
| 2026-09-03 | 12 | 0 | 12 | 0 | 0 | 0 |
| 2026-09-04 | 10 | 0 | 10 | 0 | 0 | 0 |
| **total** | **61** | **0** | **61** | **0** | **0** | **0** |

### 2.1 The controls, because a zero is the whole finding

A zero from a dead detector and a zero from a real absence are the same bytes. So:

- **POSITIVE CONTROL, on this very corpus:** the `@<hex>` detector **fires** — 2 of 61 proposals
  match, and on 2026-09-04 proposal 9's `evidence_cited` literally contains **`@351f309e`**. The
  instrument family is alive on the same strings that returned zero for the tool-row patterns.
- **NEGATIVE CONTROL:** `NFRA_OUTSET-W` (a token that must not appear) → **0 of 10**.
- **Corpus size the patterns ran over:** 3,040 characters across the 10 strings of 2026-09-04.

I did not use `comp-find` CONTENT mode for any of this. The corpus is a fetched JSON document, not
the repo, and it is parsed structurally — so neither of that tool's measured false-zero modes (rc=124
with no output; rc=0 with a confident denominator and no budget line) is in this path at all.

## 3. WHAT THE 61 CITATIONS *DO* CARRY

The finding is not "they cite nothing". On 2026-09-04: **7 of 10** quote a stratum, **7 of 10** name
a ruling, **6 of 10** carry a denominator-shaped number — all as **quoted prose inside one free-text
string**, e.g.

```
"evidence_ref stratum denominator: '6305 commits over trailing 14d; 24 chain-resolved
 resource labels; 0 co-change pairs with >=2 shared commits (records axis excluded)';
 evidence_ref ruling ..."
```

`evidence_status` across those 10: **MEASURED 8, UNMEASURED 1, INFERRED 1**, with
`evidence_status_defaulted = 0` — so no proposal fell through to the non-actionable label by default.

## 4. THE MECHANISM THE MANIFEST CREDITS IS REAL, AND IT ANSWERS A DIFFERENT QUESTION

Read from the **deployed** bytes — the code that actually produced these days — not from HEAD:

```
2125         cited = str(parsed.get("evidence_cited") or "")
2126         if not evidence_resolves(cited, str(cand.get("evidence_ref") or ""), nugget_ids):
2127             discarded.append({"candidate": cand, "evidence_cited": cited,
2128                               "discarded_because": "evidence_cited does not resolve to the "
2129                                                    "stated evidence_ref or a known ruling id"})
```

and the rule itself, at `:1551`:

```
    if any(i and len(i) >= 6 and i in cited for i in nugget_ids):
        return True
    toks = distinctive_tokens(ref)
    if not toks:
        return False
    return any(t in cited for t in toks)
```

Its own docstring records why it looks like that: *"MEASURED BROKEN 2026-08-06 and this is the
repair: a prefix match on a structured string tests the FORMAT, not the content — it passed 7 of 7
live author calls INCLUDING a planted fabrication, and only the mutation revealed it."*

**It is a sound anti-fabrication control, and it is scoped by the same set as the act.** It checks
the citation against **the `evidence_ref` the runner itself put in the prompt**. It can establish
that the model quoted what it was shown; it cannot establish that what it was shown came from a
named tool at a named vintage. **That is precisely the gap `OS-s-17` exists to close** — and closing
it is a producer change.

## 5. ACCEPTANCE

### O17-AC1 -- JUDGMENT (`judgment="true"`) -- RECORDED, NO VERDICT

*"ONE DAY'S PROPOSALS, each citing the tool row behind it at path@vintage. Evidence. NO VERDICT --
the CVO grades it at L9."*

**The evidence limb is recorded in full in sections 1–4 above and in `NFRA_OUTSET-W1-S24`:** one
day (2026-09-04) and six more beside it, 61 proposals, 61 cited, **0 citing a tool row**, with a live
positive control proving the zero is an absence.

**The build limb is BLOCKED and the block is a cut defect, filed as instructed.** Making a proposal
carry `path@vintage` requires editing
`infra/aws/ec2/estate-report-runner/estate_report_runner.py`; this order's `<paths>` grants **only**
the deliverables folder and the investigation channel. I read that file — from S3 and from HEAD — and
**did not write it**; `0.9.0_WK_NFRA_OUTSET~2` holds it for `OS-s-14` as this is written.

**Denominator:** 61 of 61 proposals inspected across 7 of 33 published days; 4 citation-shape
patterns run per proposal; 1 positive and 1 negative control; 2 planes read for the producer
(deployed S3 artifact and HEAD).

**No verdict is written here or in the proof-of-spec instance.** `3.0.0_SA_CVO` grades it at L9.

## 6. ROWS FILED (66 → 68, append-only)

- **`NFRA_OUTSET-W1-S24`** — **BLOCKING**, ARMED, disarm_owner `2.0.0_SA_COO`. The build limb needs
  a repo surface this order does not grant. Carries the whole census, both controls, and both
  structural reasons.
- **`NFRA_OUTSET-W1-S25`** — OBSERVATION, ARMED, disarm_owner `2.0.0_SA_COO`. **The deployed
  producer is 11 days behind HEAD and carries none of `OS-s-9`/`OS-s-10`/`OS-s-11`.** Committed ≠
  served, measured on content rather than filename (`_stratum(` appears 11 times, so it *is* the same
  program; the four new tokens appear 0 times, so it is a version from before this project).

## 7. WHAT I DID NOT DO

- **I did not write any repo file.** No code, no test, no engine — the `<paths>` block grants none,
  and the one file that would need changing is held by another worker this round.
- **I did not flip `<status>` to `complete`.** There is no mechanical criterion to pass, and a
  BLOCKING row says the cell's own accept is not reached. Flipping would assert a build that did not
  happen. The order stays open for the issuer, which is what a cut defect is for.
- **I did not deploy the runner**, and I am not proposing that it be deployed mid-round — `OS-s-14`
  is being written into that same file right now, and a deploy is a change-management act with its
  own ledger.
- **I wrote no verdict** on a judgment criterion.

## 8. PUSH STATE

**LOCAL.** Nothing pushed. Measured with `git ls-remote` at report time — see the WORKER REPORT.
