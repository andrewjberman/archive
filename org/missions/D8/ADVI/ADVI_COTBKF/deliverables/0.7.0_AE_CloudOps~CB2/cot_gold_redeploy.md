# ADVI_COTBKF.TO-CB-ax-2 -- the cot gold redeploy: four keys, no runtime `opal_naming`

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 50 | **Cell:** `CB-ax-2`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @2d0c98c8e3 (AMENDMENT 3, RELEASED)
**Criterion:** `CB50ax2-AC1` -- **PASS** | **Proof:** VALID (rc=0), first pass
**Ledger:** `.../20261009T1723Z_advi-cotbkf-cot-gold-redeploy-cb-ax-2-20261009_deploy_completion.md`,
opened @9f6f320f42 before the first write, 7 legs, CLOSED all proven.

---

## Outcome -- four keys, in the pair's order

| # | key | prior | new VersionId | bytes | sha256 |
|---|---|---|---|---|---|
| 1 | `code/gold/ticker_overrides.py` | **404, mints** | `qjQFQTPz7i9Xgo031VXGSJ0qA3K2HG8V` | 65,021 | `4d407c3a...7015` |
| 2 | `code/gold/legacy_addresses.json` | **404, mints** | `q.zGXhcophZPLllhNrEn6xAlqV0wMQw8` | 8,176 | `34dfcb37...fe17` |
| 3 | `code/gold/build_canonical_prices_v2.py` | `GAOI7tOR...` | `QCY7q9UQQ_k0gcWSnm8Aab_WUxe2iU1Y` | 42,400 | `8b733bb1...a76b` |
| 4 | `code/gold/B_00.canonical_holdings.py` | `hU7ZrZTD...` | `oLzqVDS_pXpbotVgv.unFNA17V3HBtoO` | 68,327 | `2b38b142...a36ec` |

The cot gold scripts now resolve their own firm from the `scopes.json` beside them and **fail closed**, with
no runtime `opal_naming`. `scopes.json` was **not** written -- its served sha256 already equals the repo
blob. Rollback is `copy-object` of the two script priors; the minted keys are never deleted by this seat.

**The ordering is load-bearing**, not cosmetic: the new scripts fail closed without the beside-files, so
minting 1 and 2 before deploying 3 and 4 is what prevents a window where a manual silver-prep would hit
the fail-closed STOP. Both prior script versions were proven retrievable after all four writes.

## The census

Both served priors are the versions **this seat deployed earlier today** -- `3ac0a502...` from CB-ap-2 and
`45fbbd92...` from CB-ao-1 -- so the baseline is continuous and measured rather than inherited.

- **Writer:** added 151, removed 31 = **182 changed lines** across 5 hunks. The pair says 182. Exact.
- **B_00:** added 22, removed 4 = **26 changed lines** in 2 hunks. The pair says 26. Exact.

The pair cites B_00's second change at `:1362-1365`, and on the HEAD side I measured a single added line
at **1383** -- which looked like a divergence and was not. `:1362-1365` is **prior-side** numbering, and
the four removed lines sit at prior 1362, 1363, 1364, 1365 precisely: the `sys.path.insert`, the
`from opal_naming import lookup`, the tree relpath, and the `_own_firm = _firm_lookup(...)` assignment.
They are replaced by HEAD:1383 `_own_firm = _own_firm_beside()`, **inside** `_ff_worker` (HEAD 1360-1442),
exactly as the pair states. The first change is HEAD 96-116, `def _own_firm_beside()` -- the beside-module
reader, outside `_ff_worker`. Changed lines outside the named changes: **0**.

`_ff_worker` moved from 1339-1424 at CB-ao-1 to 1360-1442 here, a shift of 21 -- precisely the lines the
own-firm reader adds above it. Consistent, not drift.

## A gate said STOP, and I measured instead of relying on WARN mode

On the writer's deploy, `safe-deploy` printed:

```
STOP: 1 hit(s) in OPEN-DEPLOY -- worktree C:/dev/wk-irpt-dashbd-86: ls-tree rc=128 (not readable, not clear)
CROSSBOX-DEPLOY ... open_deploy=hit verdict=STOP
WARN [seat-gates] would stop under ENFORCE (crossbox-deploy:data/cot); WARN mode proceeds.
```

The gate would have **blocked this act under ENFORCE**. It proceeded only because it is WARN. That is not
a licence, so before adding a second write I ran the NEVER-2 census:

- **68 live worktrees**, 66 readable, **2 unreadable** -- both `rc=128 "fatal: not a git repository"`.
- Those paths are **stale registrations**: two do not exist at all, one exists with no `.git`. **A path
  that is not a repository cannot hold an open-deploy sentinel**, so the hole the gate could not clear is
  administrative debris, not a tree concealing a live deploy. That converts "not readable, not clear" into
  clear, by an argument the gate itself cannot make.
- **The decisive read** -- the shared tree's 25 current sentinels: the only one OPEN against cot
  `code/gold` is this act's own. `irpt-fwd14-narrow-holdings-bundles` is OPEN but a different firm
  surface; the three cot-adjacent `secclass` entries are **HELD-SOVEREIGN-GATED**, parked awaiting a
  sovereign decision and not mid-write.

So no other seat was mid-deploy on these four keys, and the write proceeded on that measurement. **Two
independent readings then agreed**: on B_00's deploy minutes later the same gate read
`open_deploy=clear verdict=CLEAR`, with nothing changed and no override used -- confirming the earlier
STOP was a transient census-readability artifact.

The stale registrations are a real item: under ENFORCE they would block every cot deploy on this device.
Pruning them is device infrastructure, not this seat's grant, so they are surfaced rather than fixed here.

## AC1 and the two reads the amendments add

**`6 passed`**, rc 0, on the served bytes. All **five** inputs the test copies from were replaced with
fetched served bytes and re-hashed in place first -- the writer, B_00, `ticker_overrides.py` at `GOLD/lib/`,
`legacy_addresses.json`, and `scopes.json` as well, which this act does not write but the gold run reads.

The no-`opal_naming` condition is enforced **by the test**, which is stronger than staging it myself: each
arm runs in a child interpreter whose `sys.path` is the temp dir only, with a hard import blocker on
`opal_naming`, and `_setup` asserts the copied `lib/` subset contains no `opal_naming.py`.

**No extra mutant was planted, and the reason is that the suite already is one.** Three of its six arms
remove a required beside-file and assert the script STOPs with a named error and **zero writes**. A
passing suite therefore shows the scripts fail closed rather than merely run, and shows the tests bind to
the files under test -- remove one and the verdict changes. The single thing the suite cannot show is
*which bytes* it read, and that is covered by the in-place re-hash above rather than by a redundant mutant.

**Import closure** (AMENDMENT 1 / ADDENDUM 23), by `ast` over the served bytes, module-level **and**
in-function, never a grep:

```
IMPORT-CLOSURE b00_modules=18 writer_modules=17 missing=0
```

Mirror denominator printed and paginated to exhaustion: `code/gold/` = **110 objects over 1 page**, `lib/`
holding **16** -- independently reproducing the issuer's 16. B_00: 18 imports, 12 stdlib, 3 installed,
3 local (`lib.config`, `lib.exclusions`, `lib.s3_layout`), each resolved against the actual listing and
all present. The writer: 17 imports, 12 stdlib, 5 installed, **zero local** -- the correct result, not a
gap: it loads `ticker_overrides.py` from beside itself via `importlib.util` at run time, so that
dependency *is* key 1 of this write set and cannot appear as a static import. The suite's
overrides-absent arm is what proves that run-time load.

**Written-key census:** carried by the suite's own arm (f), keys read equal the pre-change keys, no new key
class -- so CTO condition 2's census is the test's assertion rather than a separate claim of mine.

Worktree removed with `git worktree remove`; shared tree verified clean with all five files still at their
served hashes.

## Not claimed

CTO condition 3's live arm -- the first manual silver-prep after this deploy, which is D2-S62's closing
census (`source_firm=cottonwood`, `BREACH=0`, resolved paths printed) -- is the issuer's. No scheduled
output moves: the writer runs only on a manual silver-prep, and B_00's `_ff_worker` path stays unreached
while the rps prefix is empty.

**No client account id appears in any ledger line or in this log** (containment ruling item 6). This act's
evidence is code bytes, versions and import graphs.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `safe-deploy.sh` | writer, then B_00; no bypass flags either time | rc 0 both, 1 path / 0 bundle-member each; crossbox STOP then CLEAR, both recorded |
| `deploy_ledger.py` | `open` / `close-leg` x7 / `close` | 7 legs before the first write; CLOSED all proven; nothing left staged |
| NEVER-2 open-deploy census | `git worktree list --porcelain` + `ls-tree` per tree | 68 trees, 66 readable, 2 stale registrations; no conflicting open deploy |
| ast import-closure reader | written for this order, over the served bytes | `b00_modules=18 writer_modules=17 missing=0`; mirror 110 / `lib/` 16 |
| `aws s3api` / `boto3` | 2 404s with a control, 2 priors, 2 puts, 5 gets, 2 rollback heads | every zero with a control; 4 of 4 served shas equal; both rollbacks retrievable |
| `proof-of-spec-check.py` | `<instance> CB50ax2-AC1` | **VALID (rc=0)** first pass |

**What failed / gaps.** (1) The crossbox gate's STOP was a false alarm caused by stale worktree
registrations; it cost a full 68-tree census to clear and would be a hard block under ENFORCE. Surfaced.
(2) The pair's B_00 line citation is prior-side while my census is HEAD-side; that is a numbering
convention, not an error, but it reads as a divergence until resolved and cost a second measurement.
(3) The writer's census is checkable only by count and hunk placement, since the pair describes its 182
lines by content rather than by line bounds -- the count matched exactly, but a content-level check was
not available to me. (4) The AC1 expect is the bare word `passed`, satisfiable by a partial run; the real
bar is 6 of 6 and rc 0.

## Push state

MEASURED at write time -- see the final report line; re-measure at read time.
