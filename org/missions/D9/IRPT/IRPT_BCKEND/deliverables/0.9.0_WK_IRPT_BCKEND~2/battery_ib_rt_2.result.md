# BATTERY `IB-rt-2` -- RESULT

**Run:** `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`
**Vintage:** branch `wk-irpt_bckend-2-2b`, after the six-root deploy closed at `737548f735`.
**Verbatim stdout:** `battery_ib_rt_2.result.txt` beside this file -- this document QUOTES that run and
adds nothing to it.

> **`10 of 13 arms PASS. 3 BLOCKED. THE TOKEN `IBRT2-SIX-GUARDED` IS WITHHELD, so `RT2-AC1` FAILS
> by output and the order stays OPEN.`** A battery that prints its token beside a blocked arm is a
> signature, not evidence.

**THIS SUPERSEDES THE PRE-REBOOT VINTAGE OF THIS FILE** (`0 of 8 in lane / 3 of 11 whole file`,
`7 of 10 arms`). It is a new run, not a correction: every number below comes from the run above.

---

## THE THREE BLOCKED ARMS, AND WHO OWNS EACH

| arm | reading | owner |
|---|---|---|
| `a2` zero over the whole file | `1 of 12` unguarded -- `irpt-holdings`, **out of `<paths>`** | row `W2-S30`, `2.0.0_SA_COO~B` |
| `g3` the refusal validates against `StatusEnvelope` | `0 of 11` -- `source_dates.required` is `['business_date']` | row `W2-S36`, `2.0.0_SA_COO~B` |
| `g2` success responses validate, SERVED | `0 of 11` -- needs a principal only an **operator** can mint | arm `(f)`, HUMAN-GATED |

**None is graded around and none is fixed halfway.**

---

## ARM (a) -- ZERO OF N, AND THE CONTROL

```
denominator: 12 published route(s) = 12 with a declared handler + 0 without
IN LANE (the 6 functions this order's <paths> name): 0 of 11 unguarded
WHOLE FILE                                         : 1 of 12 unguarded
  OUT OF LANE, named and not counted: GET /api/scoped/investor-reporting/holdings/{accountSetId}
                                      -> irpt-holdings (cell IB-rt-7, row IRPT_BCKEND-W2-S30)
[PASS]    a1 zero in lane -- 0 of 11 route(s) this order may open reach an unguarded handler
[BLOCKED] a2 zero over the whole file -- 1 of 12
  the control, on a THROWAWAY copy of the TABLE (never of a handler): 3 of 3 victim(s) moved the
  verdict to `1 of 11`
[PASS]    a3 the control fires -- 3 of 3
```

**THE POPULATION MOVED WHILE THIS CELL WAS DEAD.** The face's amendment names `holdings-snapshot`
as *"the one published route that has NO handler at HEAD"*. `IB-rt-7` has since landed
(`d9c940244a`) and DEPLOYED (`5a359024a9`) one, so `N` went from 11 to 12 and the twelfth is not
this order's to guard -- `infra/aws/lambda/investor-reporting/holdings/` and its Terraform root
are in neither half of `<paths>`. Row `W2-S30`, and **row `W2-S31` says what "unguarded" means
here**: the census grades the `__irpt_guarded__` MARK, and that handler enforces the same
`FirmBinding` and `Enforcer.guard()` INLINE. It is not a live cross-firm hole.

### The basename census (rows `W3-S22` / `W4-S24`)

```
2 basename match(es) across 8 function directory(ies) x 7 shared module(s):
  2 declared vendored copy(ies), 0 true collision(s)
[PASS] a4 no basename collision
```

`_authz/dispatch.py` is renamed to `_authz/authz_dispatch.py` with its one importer
(`_contracts/tests/test_seam_paired.py:41`) and **no shim**. The two remaining matches are
`irpt-holdings`' enforce.py/errors.py, each DECLARED in that function's own `STAGE_MANIFEST.json`
and `BUILD_MANIFEST.json` -- **a basename match is not automatically a collision, and grading it
as one would have failed this arm on a deliberate, documented act.** The discriminator is the
function's own manifest, never this battery's opinion about which copies look intentional.

---

## ARMS (b) (c) (d) -- THROUGH THE REAL ENTRY POINTS

```
(b) six swaps x 6 dispatched function(s) ........................... 36 of 36
    difference control -- the authorized request is NOT refused ....  6 of 6
    ROW W1-S16, the seventh negative: an ADMIN principal addressing an advisor
    outside the verified firm is refused ...........................  6 of 6
    and its difference control -- the same admin principal reaching an
    IN-FIRM advisor is NOT refused OBJECT_NOT_COVERED ..............  6 of 6
(c) a claimed firm that disagrees -> FIRM_BINDING ..................  6 of 6
    a reconciling claim is NOT an obstacle ........................   6 of 6
(d) an UNPROJECTED grant refuses ..................................   6 of 6
    and a REVOKED grant does NOT read as an unprojected one .......   6 of 6
[PASS] b swaps | c the firm is the principal's | d the projection | b/c/d the envelope
```

**`36 of 36`, the arm's own bar, with nothing out of lane** -- `irpt-status` entered the swap set
when `W2-S19` was granted. Every refusal was serialised and searched for another firm's opaque id,
another advisor's id, an account outside the grant, another firm's report and pdf, a client
surname, an e-mail address and the refused firm token: **0 bytes of any of them in any of the 36.**

**`W1-S16` is closed by behaviour, not by wording.** `covers()` returned `True` for ANY advisor id
once the principal class was `FIRM_OPERATIONS` or `OPAL_GLOBAL`, while the comment beside it
claimed *"within the verified firm"*. It now checks self-address first (the viewer's own id came
from the trusted header set and `resolve_now` already granted on it), then membership of the
VERIFIED tenant's own ownership map, then the class. **The difference control is what makes the
negative mean anything**: a check that refused every advisor id would pass the negative and be
worthless.

⚠ **`b/c/d the envelope` is a KEY-PRESENCE check, NOT schema conformance** -- it reads the
StatusEnvelope top-level key set and cannot see the `business_date` defect that arm `g3` measures.
The arm now says so in its own output. Row `W2-S36`.

---

## ARM (e) -- DEPLOYED AND VERIFIED -- **MET, 6 of 6**

```
irpt-directory-search      entry.lambda_handler   sha EQUAL Active/Successful
irpt-performance-adapter   entry.lambda_handler   sha EQUAL Active/Successful
irpt-narrative             entry.lambda_handler   sha EQUAL Active/Successful
irpt-export-render         entry.lambda_handler   sha EQUAL Active/Successful
irpt-status                entry.lambda_handler   sha EQUAL Active/Successful
irpt-ycharts-generate      entry.lambda_handler   sha EQUAL Active/Successful
declared artifact_sha256 == live CodeSha256: 6 of 6; handler is the guarded entry: 6 of 6;
Active/Successful: 6 of 6
extract-and-import of the SERVED artifact, fresh interpreter, repo off sys.path, layer mounted
for the 3 that attach it:
  IMPORT-OK 6 of 6 | negative control FIRES 6 of 6 | VERIFIED 6 of 6
ledger: entry present=True, sentinel removed=True, legs recording a post-apply `No changes`
plan: 6 of 6
[PASS] e deployed and verified
```

**SIX ROOTS, ONE AT A TIME, EACH VERIFIED BEFORE THE NEXT WAS TOUCHED** (the issuer's addendum
control). Every plan read `0 to add, 1 to change, 0 to destroy` on exactly the handler, the
`s3_object_version` and the `source_code_hash` -- **nothing beyond the handler attribute and this
cell's own packaging.** The `performance` root holds `aws_lambda_layer_version.irpt_common` as a
MANAGED resource and its plan showed **no layer publish**; the `ycharts` root's session probe and
schedule did not move. Ledger `irpt-bckend-rt2` CLOSED, all 12 legs proven, sentinel removed,
committed BEFORE these grading reads.

### Two runtime-only defects that had to be fixed before any zip was worth building

1. **`entry.py` derived its package roots from the file's PARENT DIRECTORY**, which at `/var/task`
   is `/var` (gift 4 / row `W3-S26`). `_HERE` is now inserted unconditionally and the repo-shaped
   sibling roots only if they exist.
2. **The route table was a FILE READ, and the file is in no zip.** `operation_of` fell back to
   `from routetable import load_routes` whenever the event carried `routeKey` and no `operation` --
   and `api/integrations.tf:57` declares `payload_format_version = "2.0"` with NO request
   template, so **every production request carried exactly that shape.** Each `Entry` now carries
   its own `routes` map, derived from the published v1 file, checked at construction against its
   own `operations` and in the tree against `routes.json`. The live invoke below resolved
   `status-summary` from `routeKey` alone, which is that fix exercised in the runtime.

**The instrument took three versions and the first two called all six IMPORT-FAIL.** v1 set
`sys.path` to `[cwd]` and removed the STANDARD LIBRARY; v2 relied on `python -I`, which implies
`-P`, so the script's own directory was not on `sys.path`. **Both times the negative control
failed for the same reason as the positive arm -- and that agreement is the tell that the
instrument, not the artifact, is the subject.**

---

## ARM (f) -- THE PRINCIPAL -- **HUMAN-GATED, which its own rule admits as a PASS**

```
9 of 9 required elements present and 0 secret values
[PASS] f the principal
```

`RT2_test_principal_human_gated.md` names the operator's exact act: which account, which user
pool, which claim, the signing and verifying paths BY NAME, the expected served reading and the
expected refused reading. No secret value appears in it.

---

## ARM (g) -- ENVELOPE CONFORMANCE, SERVED

```
denominator: 11 route(s) with a DEPLOYED handler at this HEAD are this order's; 1 excluded:
  EXCLUDED, neither a pass nor a fail: GET .../holdings/{accountSetId} -- irpt-holdings,
                                       cell IB-rt-7, row IRPT_BCKEND-W2-S30
a mismatched X-Contract-Version is refused CONTRACT_VERSION on the DEPLOYED function: 11 of 11
the refusal validates against v1 StatusEnvelope: 0 of 11
[PASS]    g1 the version check is SERVED
[BLOCKED] g3 the refusal validates against StatusEnvelope
[BLOCKED] g2 success responses validate, SERVED
```

**`g1` IS THE HALF THE AMENDMENT SAYS THIS CELL SERVES, AND IT IS SERVED**: `IB-rt-1` committed
the `X-Contract-Version` check and deployed nothing; all six functions now carry it and refuse
`11 of 11` on the live plane, invoked by name. These calls are **safe by construction**: the
version is checked before an Enforcer is built, before storage is read and before anything is
enqueued -- proven in-process by the arm that refuses with the storage loaders REMOVED. No
directory was read, no job enqueued, no vendor chain reachable (bounds 1 and 2).

⚠ **`g1` AND `g3` ARE SEPARATE ARMS BECAUSE THE FIRST VERSION OF THIS ARM PASSED WHILE PRINTING
`0 of 11` BESIDE ITSELF.** A clean metric above a failing number reads as green. They are split so
neither carries the other.

**`g3`, row `W2-S36`:** v1's `StatusEnvelope` has `source_dates.required = ['business_date']` and
the boundary emits `source_dates: {source_completion_date: null}`. The top-level `required` does
NOT name it, which is why the key-presence arm passes. **Two defects, different owners, measured
apart:** a POST-READ refusal could carry the artifact's business date and does not (this cell's,
fixable in lane); a PRE-READ refusal has no artifact to take a date from and v1 admits no null
there (needs an amendment to a FROZEN contract this order may not touch). A post-read-only fix
would still leave `11 of 11` version refusals non-conforming and would spend a second six-root
deploy to move nothing, so the arm reads BLOCKED rather than PASS-with-a-repair.

**`g2`:** a SUCCESS response needs a principal the edge validator accepts, and arm `(f)` is
HUMAN-GATED. **Invoking with a fabricated advisor id would return a refusal, and counting that as
a validated response is exactly the wrong answer.** This half un-blocks the moment the operator
takes the act arm `(f)` names -- never by this cell.

---

## WHAT THIS RUN DOES NOT CLAIM

* No live vendor call, no mailbox read, no YCharts session (bound 1). The only live invocations
  are version-mismatch refusals, which return before any read.
* No monitor, alarm, SNS topic or SES send exists anywhere in this cell (bound 2).
* No served output outside the six functions this order names was touched (bound 7).
* `docs/contracts/` is unedited; the v1 freeze at `c22f179bbf` stands (`W2-S25`, `W2-S34`).
