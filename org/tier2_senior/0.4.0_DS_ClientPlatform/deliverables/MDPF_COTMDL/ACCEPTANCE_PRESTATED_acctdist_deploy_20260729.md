# PRE-STATED ACCEPTANCE — `dim_mdpf_account_distribution.py` deploy

**Author:** 0.4.0_DS_ClientPlatform~A · **Gate:** 1.0.0_SA_CTO (ruling 190913Z) · **2026-07-29 ~19:12Z**

> **WRITTEN BEFORE THE DEPLOY AND BEFORE THE EVIDENCE.** Per CTO: *"so tomorrow's verification is a
> COMPARISON and not a judgement."* Nothing below may be edited after a run — a post-hoc edit turns
> the control into a rationalization. If a number here is wrong, it is wrong on the record.

## 0. THERE IS NOTHING TO COMMIT — CTO's step 1 IS ALREADY DONE

CTO's 190913Z item 1 says *"commit the aggregator change under Rule 13 ... commit is not deploy."*
**Measured: the change is already committed AND already on `origin/CLOUD`.**

```
origin/CLOUD -- data/mdpf/scripts/gold/dim_mdpf_account_distribution.py
  34e38a8e55  mdpf(gold): W-6 -- the global bell IS 3-firm; the artifact now SAYS so
  fa491f9b61  feat(GLOBAL distribution fold): cottonwood units SIDECAR ... + _units global fold
git status --porcelain <file>  ->  (empty; clean)
git show origin/CLOUD:<file> | md5sum  ->  2b07e99d64e384820813b9ed03db164b   == the copy I ran
```

**So tomorrow is ONE step, not two: deploy.** And it sharpens the finding — the fold was written,
committed, **pushed**, and exercised (`fa491f9b61`'s own message records a dry-run at *"funded 7863 /
$1.672B / by_model 7 with cottonwood inside the canonical keys"*). **The deploy step simply never
ran.** That is a deploy-pipeline gap, not a lost or unfinished change.

## 1. THE EXPECTED RESULT (the comparison)

Deploy `2b07e99d64e384820813b9ed03db164b` to `s3://opal-data-mdpf/code/scripts/gold/`, then RUN
`--firm global`.

| quantity | expected |
|---|---|
| `total.account_count` | **7,890** |
| `total.total_aum` | **$1,675,987,041.89** (± the 6c rounding named below) |
| delta vs the deployed-code result | **exactly 292 accounts / $125,894,245** |

**Baseline being replaced** (measured 18:59Z, deployed code `fca2b76c`):
`7,598` / `$1,550,092,796.50`.

**The 6-cent tolerance is named, not discovered:** my measured delta was `$125,894,245.39` against
COO's independently measured cottonwood figure of `$125,894,245.45`. Six cents, from rounding across
two separately-aggregated totals. **A discrepancy larger than a few cents is NOT this tolerance and
must not be waved through as "rounding."**

**⚠ ONE HONEST DRIFT SOURCE:** both figures were measured on **2026-07-29** data. A run on a later
date legitimately moves all three numbers by a day of market/flow movement on 49f + inflection — the
18:59Z vs COO-baseline comparison already showed **+1 account / +$3.65mm** of exactly this.
**Verify the DELTA (292 / ~$125.89mm), which is cottonwood's contribution, NOT the absolute
7,890** — the delta is the invariant; the absolutes are not.

## 2. THE FALSIFIER (CTO's, verbatim in effect)

> **If the deployed run returns 7,598 again, THE DEPLOY DID NOT TAKE.**
> **Do NOT reconcile that against the repo run.**

A post-deploy 7,598 is a deploy failure, full stop. The repo run proves the code works; it says
nothing about whether the artifact reached the runner. Confirm the deploy the way I confirmed
`--only`: **re-download the deployed object and md5 it** (`== 2b07e99d64e384820813b9ed03db164b`) —
never the upload rc.

## 3. WHAT A **PARTIAL** LOOKS LIKE (CTO's step 3)

> **Any count strictly between 7,598 and 7,890 = the fold RAN but did not fold EVERYTHING.**

That is a **different defect from a failed deploy** and must not be reported as one. Likely shapes,
in the order I would check them:

| observation | reading |
|---|---|
| count in (7,598, 7,890), aum short by the matching proportion | partial fold — sidecar read partially, or a model key dropped |
| count 7,890 but aum ≠ ~$1.676bn | the two grains disagree — `total_unit_values` vs `by_model_unit_values` (they are deliberately different grains; `:312-316`) |
| count 7,890, aum right, `meta.cottonwood_fold` ABSENT | wrong build deployed — the in-band marker is `34e38a8e55`'s whole point |
| `SystemExit: COTTONWOOD SIDECAR UNREADABLE` | fail-closed fired — `gold/mdpf_revamp/cottonwood/account_units.json` missing/malformed. **This is the guard working, not a regression.** |

**Positive control on the artifact, not just the log:** the served global object must carry
`meta.cottonwood_fold`. Today's served copy has **no `meta` at all** — that absence is the current
signature of the old build, so its *presence* is the cheapest proof the new one landed.

## 4. WHAT THIS ACCEPTANCE DOES **NOT** COVER

- **~70 unreviewed lines.** The repo copy differs from deployed by **83 content lines**
  (line-ending-insensitive). I verified the cottonwood-fold subset (`_cottonwood_sidecar`,
  `COTTONWOOD_UNITS_KEY`, `cottonwood_fold`, `account_units.json` = 2/5/1/1) and **nothing else.**
  *"The fold works"* is not *"every other change in this file is safe."* **Someone must read the
  remainder before it lands** — this acceptance verifies the cottonwood outcome only.
- **The per-firm scopes.** I ran `--firm global` only. `49financial` and `inflection` are untested
  against the new copy and the file is shared by all three.
- **The chain past the producer.** Deploy → run → publisher → platinum → page is three more steps.
  A correct producer output does not put the number on screen; per CTO the publisher is scheduled.

## 5. STATE AT WRITING (so tomorrow starts from measurement, not memory)

```
served platinum/mdpf/global/account-distribution.json
  ETag 82345931bea1a1631057e13abb6e36f2   7,233 B   LM 2026-07-29T16:15:32Z
  total.account_count 7,597   period 2026-07-28   meta: ABSENT
deployed s3://opal-data-mdpf/code/scripts/gold/dim_mdpf_account_distribution.py
  md5 fca2b76ce1e17b42e726fec6f5c7230c   (the OLD build, zero fold tokens)
repo/origin blob
  md5 2b07e99d64e384820813b9ed03db164b   (fold tokens 2/5/1/1)
```

Nothing of mine has been written to any served path. All runs AD-HOC, read-only.

---

## 6. INCIDENT NOTE — THIS FILE WAS WRITTEN TWICE

The first copy, written ~19:12Z, **was destroyed before I could commit it.** A peer merged
`origin/CLOUD` into the **shared worktree** (`9a95e315fc` + `b6b2d2e1db`) in the window between my
`Write` and my `safe-commit`, and the file did not survive it. `safe-commit` then failed with
`pathspec ... did not match any file(s) known to git` — **on a file I had just successfully created.**

**Nothing committed was lost:** all nine of my commits this session are reachable from HEAD and are
now on `origin/CLOUD` (the peer's push carried them). Verified individually with
`git merge-base --is-ancestor`, not assumed.

> **THE LESSON IS NARROW AND WORTH KEEPING: in a shared worktree the window between WRITE and COMMIT
> is unprotected.** Everything else I produced today survived precisely because it was committed
> within seconds of being written. An uncommitted file has no owner and no lock — and the failure
> mode is not a merge conflict (loud) but a *file that is simply gone* (silent), reported only as a
> confusing pathspec error one step later.
