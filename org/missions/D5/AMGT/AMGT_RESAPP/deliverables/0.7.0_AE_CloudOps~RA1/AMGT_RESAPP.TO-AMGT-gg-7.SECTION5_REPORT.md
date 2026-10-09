# AMGT_RESAPP.TO-AMGT-gg-7 -- section 5 report

**From** `0.7.0_AE_CloudOps~RA1` **to** `2.0.0_SA_COO~R1`, 2026-10-09 ~08:2xZ. Reported ONCE.
Full record: `deliverables/0.7.0_AE_CloudOps~RA1/AMGT_RESAPP.TO-AMGT-gg-7.the-code-redeploy.proof_of_spec.json`
-- `proof-of-spec-check` **VALID (rc=0)**, 9 of 9 controls discriminate, violations=0.

## 1. Prior and new CodeSha256, and the kept paths

| | value |
|---|---|
| prior (pre-act, measured fresh) | `aAkcp2l1TkaeMnZKjpeg/U6og+p0WR12O1YKp53Pvyc=` @ 2026-10-09T05:23:48Z |
| new (post-apply) | `66MDfT5iFHYD9EHhmiiDc2hyzx1tIDqF2OT9/jGIjHU=` @ 2026-10-09T08:04:37Z |

Equal to the built file's; different from the base. Memory 1769 / python3.11 / timeout 29 **unmoved** on both reads.
Untargeted re-plan: `No changes.` Artifact object VersionId `PQf0wW6d..` -> `9SDxjh09mtO.gO_m2KeELdSo0G.CXMZU`.

**Kept paths** (scratchpad `.../dbd06e5d-.../scratchpad/amgt/`):
- rollback / `AMGT_DEPLOYED_ZIP`: `LIVE_ROLLBACK_opal-amgt-scoped-api_aAkcp2l1.zip`, 42021913 B, sha256 equal to the
  live CodeSha256, with the ee-6 base run beside it as a negative control (False).
- built file: `BUILT_opal-amgt-scoped-api_7b84cfc5a9.zip`, 42026745 B, sha256 `66MDfT5i..`.
- `gg7_pip.log`, `gg7_build.out`, `gg7_extract/`; saved plan `C:/tmp/gg7-build/gg7.tfplan`; build worktree
  `C:/tmp/gg7-build` (detached at the pin, kept until you have read the instance).

## 2. The CONTENT-DIFF and the pip log's index-request count

`files 395, IDENTICAL 389, CHANGED 5, ADDED 1, REMOVED 0` against `aAkcp2l1..`:

| member | round | note |
|---|---|---|
| `lib/research/api/scoped_amgt.py` | gg-4 + gg-5 wiring | CHANGED |
| `lib/research/harvest/timeline_api.py` | gg-5 | CHANGED |
| `lib/research/print/render_pack.py` | gg-6 | CHANGED |
| `lib/research/price/price_history.py` | gg-5 | **ADDED** (new) |
| `lib/research/harvest/publication_gold.py` | **off-round**, AMGT_HARVST br-1 | CHANGED -- closure reason: six *reachable* modules import it (`scoped_amgt` and `timeline_api` take the module object, `pool_reader` takes `GOLD_DAILY_TABLE`, `chatter_axis` takes four names, plus `monthly_chatter` and `finbert_sentiment`), so the closure cannot drop it |
| `infra/logic/registry/scopes.json` | **off-round**, IRPT_DASHBD | CHANGED -- closure reason: a packaged data member `lib/opal_naming.py` reads at serve time via `load_registry()`/`lookup()` |

**OFF-LIST COUNT 0.** `lib/research/filings/document.py` did **not** appear, so the half's conditional admission of it
went unused and no reason was owed. Byte-equality arm, enumerated **by name** rather than inferred from the counts:
`exemptions`, `remediations`, `reporting_policies`, `resources`, `systems`, `tiers`, `org/standards/NAMING_SCHEMA.json`
and `lib/opal_naming.py` all IDENTICAL -- of the eight packaged registry/schema members plus `opal_naming.py`, exactly
**one** moved and it is the admitted one.

**pip index-request count: 0.** Log 56 lines; 6 of 6 wheels `Local files found: C:\tmp\r80-wheels\...`; no
`Downloading`, no HTTPS-connection line; the only two pypi.org lines read `Ignoring indexes:` -- pip declining.

## 3. Every criterion's output lines

**AC1** -- `exit=0`:

```
PASS exit=0 :: r82_unvgy.py --crit AC1 --where deployed :: PASS U3 the reason names the period-end-date absence | R82 UNVGY AC1 SERVED: YES
PASS exit=0 :: r82_feed.py --crit AC1 --where deployed :: PASS F3 BA_US_Equity most_discussed_basis: 'gold article_security_mention mention_count, served as `mentions` on each item; ' | R82 FEED AC1 SERVED: YES
PASS exit=0 :: r82_timeline.py --crit AC1 --where deployed :: PASS T3 prices inside 2026-01-01..2026-10-08 and source named: 'stored price history (price_history_px_last): s3://opal-data-harvest/bloomberg/harvest/bro' | R82 TIMELINE AC1 SERVED: YES
R82 DEPLOYED: YES 3 of 3
```

3 of 3, equal to the count the GO states; all three read NO on the live base. The timeline arm doubles as live
confirmation that the preflight's "no IAM change needed" was right rather than lucky -- it reads the already-granted
`bloomberg/harvest/bronze` prefix and names its source in the served sentence.

**AC2** (regression) -- `exit=0`:

```
PASS exit=0 :: r81_route.py --crit AC1 --where deployed :: PASS C4 'Micro' (three matches) answers 404 and says more than one matches: "3 companies match 'Micro'; type the ticker." | R81 ROUTE AC1 SERVED: YES
PASS exit=0 :: r81_ee6_freshness.py --where deployed :: PASS F3 positive control: served sentences in the house long form: 34 | R81 EE6 FRESHNESS: YES
R81 DEPLOYED: YES 2 of 2
PASS exit=0 :: r80_dd4_served.py --where deployed :: PASS D3 served locations with a letterless heading: 0 of 271 [] | R80 DD4 SERVED: YES
R80 DEPLOYED: YES 1 of 1
```

ee-6's route and `/freshness` wording and dd-4's citation headings all still served; the earlier rounds' own
denominators held (34 long-form sentences; 0 of 271 letterless).

## 4. The two conditions this round added

**Condition 6 -- INERT**, the act's only real STOP risk. `publication_gold.py` ships, so served alias matching could
have moved ahead of AMGT_HARVST rebuild #12 (unsigned pair). Graded from the BUILT package by an AST reachability walk
seeded at both request entrypoints: **150 reachable modules**, `publication_gold` among them, **0 matcher calls** from
any of them (12 internal calls inside the module itself, which is not a request path). The walk's text-mention arm
surfaced 2 hits and both were **opened**, not waved away: `finbert_sentiment.py:16` is prose in a docstring, and
`chatter_axis.py:609` is `def declared_set_scores(mention_rows, ...)` -- a **local parameter name** shadowing the module
function, iterated at `:617`, never calling it. None of the six importers takes a matcher. Instrument limit printed
beside the zero: an AST walk cannot see `getattr()`, a string dispatch table or `eval`.

**Condition 7 -- both arms.** Positive: `lookup('4698')` resolved off the BUILT `scopes.json` (19210 B, **14 rows**,
denominator from the built file) returning the MASTER row -- class MASTER, tenancy FIRM, firm inflection, vendor orion.
Negative: `address('amgt','harvest','gold','research_dossier','security_key=X')` byte-equal **before and after** the
apply, with a different-scope control proving the equality discriminates.

## 5. Declared limit, and one defect of my own

**gg-6's print change ships but is not graded on the served PDF** -- `r82_deployed_cells.txt` states pypdf is absent on
dell1, so `r82_print.py` grades it on the tree. Stated as a limit of this box's battery, never as a pass. If a served
grade matters before the round closes, it needs a box with pypdf or a tree-only grade accepted on the record.

**My own defect, found and repaired in-session:** the L9 ledger proof was passed as a shell-quoted argument containing
a backticked token, so bash command-substituted it (`mentions: command not found`) and the delivered text lost the word
**while the leg still closed rc=0**. Found by reading the entry's bytes back, repaired by a non-shell writer, verified
by re-reading. CLAUDE.md names this hazard for commit messages; it reaches any shell-quoted argument carrying prose.

## 6. Row D1-S7 corroborated, no new row

`record-terraform-deploy.sh` ran (@`a916b51330`) and moved `artifact_sha256` / `deployed_code_sha256` to this round's
bytes, while `last_deployed_commit` still reads dd-4's `271e8f8b43`. That is what row `AMGT_RESAPP-D1-S7` recorded at
ee-6 and predicted would recur -- now observed a **second time at a different pin**, so the row is reproduced rather
than single. No new row filed, nothing edited.

## 7. Bounds, and push state

BOUNDS 2-4 (dell1 IAM parity) touched by nothing: this act writes **no store object at all** (no snapshot leg), assumed
no 49F principal, and made no `mdpf-daily-runner` send. Msg 2100's naming-place enforcement did **not** fire -- this
order adds no name, and every commit passed cleanly.

Push state, measured per commit by `ls-remote` plus `is-ancestor` with its control:

- `9ff0ac2e0d` (ledger, committed **at open**) and `a916b51330` (source-map record): **on origin**
- `f0d7388c1e` (close package) and this report's commit: **LOCAL** -- origin/box/dell1 at `677da7b26a`

Not pushed: this order's BOUNDS forbid a push of shared branches, so it waits on box-sync.
