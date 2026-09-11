# `battery_ib_rt_4.result.md` -- RT4-AC1, five arms, **5 of 5**

**TO:** `IRPT_BCKEND.TO-IB-rt-4` | **cell:** `IB-rt-4` (PRD cell B17) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-2-3` | **worktree:** `/c/tmp/wk-irpt-2-3` | **base:** `77b2acc7a9` (merged tip)

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_4.py
```
**rc 0. `ARMS: 5 of 5`. Last line `IBRT4-KEYS-TYPED`.** Full verbatim output (188 lines):
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-rt-4_RT4-AC1_battery_output.txt`.

This is the second execution of this order. The first reported `4 of 5` with arm (e) blocked on
row `W3-S17`; the issuer routed that row, the premise turned out to be wrong in a way that
changed nothing about the withheld apply being correct, and the work completes here at the
merged tip.

---

## The arms

### (a) N OF N CONSTRUCTORS -- `27 of 28` refused, `0` leaks

`11 public callables - 4 readers = 7 constructors`, read off the module by AST rather than from
a written list. Every constructor takes each of the four negatives; `27` refused with `0`
occurrences of the refused value across **seven renderings each** -- `str()`, `repr()`, `'%s'`,
`'%r'`, an f-string, `exc.args` and the public log line. One rendering is not a census; a leak
wearing a different syntax is the same leak.

The 28th is `TenantBinding` admitting a firm id in its **tenant position**, printed as an
ADMISSION and excluded from the refusal count rather than hidden inside it. That is the one
place a firm id belongs.

`%r` placeholders inside a refusal construction: **0**. The ruling says twelve; the module
carried **eighteen across sixteen sites** (row `W3-S16`), so the fix is defined by the census.

### (b) THE POSITIVE STILL BUILDS -- `12 of 12` identical

Against `_keys` at `7478fdf144`, loaded from git -- not a remembered list of expected strings,
which the same hand that changed the code would have updated. The IB-s-9 vendor-PDF key and the
IB-s-10 sections key are in the set verbatim. **The refusal did not change the grammar.**

### (c) THE ENVELOPE EVERYWHERE -- `0 of 57`

**The census re-ran over the MERGED module set, and that is what earned its keep.** The
population grew from 25 modules / 49 handlers to **30 / 57**. Nine paths rendered the caught
exception at this tip and only **two** were ones this order had seen before; seven were in code
that did not exist at the first cut, one of them a whole module (`dispatch.py`) the census had
never read. **Re-applying a remembered diff would have closed the two and left the seven.**

| module | what was leaking |
|---|---|
| `handler.py` | an `IdentityRefused`/`KeyError` 400 body -- a `KeyError`'s message **is** the missing key |
| `handler.py` | `PackageUnavailable` -> `str(exc)`, which quotes a portal checkout path |
| `handler.py` | the capabilities contract read -> a filesystem path |
| `dispatch.py` x2 | botocore error messages -- ARN, account id, request id |
| `render.py` x3 | `pypdf` ImportErrors -- import-machinery paths |
| `render.py` | the PDF parser message, which quotes the document's own bytes |

`PUBLIC_REASONS` is a closed 14-member enum; `error_envelope()` refuses anything outside it and
has **no parameter an exception fits into**. Arm (c)'s denominator is **not** widened (row
`W3-S15`, carried to L10 by name): it counts except handlers, the one ordinary-return instance
is fixed, and the dataflow census is not this order's to build.

### (d) INJECTED NEGATIVES -- `0 of 18`, and `18 of 18` the other way

A client name, an e-mail and an S3 key per family across six families: `0` occurrences across
body + headers + the public log, and `18 of 18` correlation ids resolving to an internal record
that **does** carry the value. The detail moved; it did not disappear. Envelope fields are
`['correlation_id', 'ok', 'public_reason_code']` -- no field for a message, a stack or a path
to travel in.

### (e) DEPLOYED -- the amendment's five steps

**(1) Plans.** `directory`, `intake`, `ycharts`, `ops`: `No changes`. `export`: not clean, and
every residual is another cell's --

```
FOREIGN-RESOURCE   aws_iam_role_policy.render_host_export_evidence    not in this branch's configuration
STALE-DECLARATION  aws_ssm_document.export_render_run                 live content is a sibling's newer version
STALE-DECLARATION  module.irpt_export_render.aws_lambda_function.this live content is a sibling's newer version
```

**Attribution rests on one verifiable fact: this order changed no Terraform configuration at
all** -- `git status --porcelain -- infra/aws/terraform/` is empty -- so no diff in any of those
plans can originate from this order's edits. Applying would **destroy** a live S3 grant on the
ycharts runner role, **delete** 21 command lines of render-host preflight including the
`RENDERER_MODULE_ABSENT` refusal branch, and **revert** `IRPT_PORTAL_ORIGIN` from
`portal.opalcapital.co` to `opalinvest.dev`. Row `W3-S20`.

This order's own convergence was measured **at the time of the act** and is in the ledger:
pre-apply `0 to add, 1 to change, 0 to destroy` with `source_code_hash` the only differing
attribute; post-apply `No changes`.

**Row `W3-S17` is closed by the tree.** The export root's baseline plan at this tip read
`No changes` *before* any upload. The three resources the pre-merge worktree read as orphans
were IB-rt-8's live declarations and the route was the merge. The withheld apply was still
correct -- that plan would have destroyed two live IAM role policies -- and the premise it was
reported under was wrong.

**(2) Import closure `6 of 6`**, in the real `/var/task` + `/opt/python` layout, using the
**published** layer zip fetched from S3. Row `W3-S14` is closed: `enforce.py`, `errors.py` and
`resolve.py` are in the export build input. `keys.py` is **not** -- the layer carries it, and a
second copy at `/var/task` would shadow the layer's and put two key grammars in one runtime.

**(3) The layer, and why it is not republished.** `3 of 3` functions on `irpt-common:5`; runtime
capabilities read on the **deployed** function returns `statusCode 200`, `FunctionError None`,
`CONTRACTS AVAILABLE: 5 of 5`. The published layer already carries the union at this tip --
measured in the zip itself: 5 contracts, `keys.py`, `firm_registry.json`, `bd_helpers.py`
present; `enforce.py`/`errors.py`/`resolve.py` absent, which is exactly why those three ride
the export zip. A rebuild is a 0-diff on content and a republish would mint a version with
identical bytes, on a surface three functions share. Row `W3-S21` records that the layer's own
`BUILD_MANIFEST` disagrees with what is published.

**(4) The ledger** CLOSED, 5 legs, 0 open markers, sentinel absent with **two** commits --
`862b0e4a6e` (OPEN, before the act) and `1577717530` (close, before the grading reads).

**(5) Triple equality `6 of 6`** -- `artifact_sha256 == S3 content-sha256 == live CodeSha256`,
three values compared against each other rather than any one asserted. **It read `0 of 6` at the
merged tip** (row `W3-S18`/`W3-S19`), because the drain took this order's code half and not its
registration half. Rebuilding from the merged tree reproduced the **live** bytes for five of six,
so those needed an honest registration and nothing else -- no upload, no apply, no churn.

---

## Controls

**Every arm was observed FAILING on the real artifact before it passed** -- a mutation of the
subject, not of a copy:

| arm | the failing observation |
|---|---|
| (a) | at round-1 HEAD, `6 of 24` (constructor, negative) pairs were **accepted** |
| (c) | `9` handlers rendered the exception at this tip, `0` after |
| (b) | the oracle **is** the round-1 module; a grammar change shows as a differing key |
| (e) | this order's first execution read `4 of 5` and withheld the token |

Two negative controls are built in: `error_envelope("MADE_UP_REASON")` must raise (prints
`a free-string reason is refused: True`), and the import-closure check was run against a
genuinely incomplete zip and reported `4 of 6` before the packaging repair.

**DETERMINISM, stated precisely rather than as one verdict.** Arms (a)-(d) are **byte-identical**
across three runs -- 109 lines each, 0 differing. **Arm (e) is not, and cannot be**: it reads a
live plane that sibling cells are writing while this order grades. Between two consecutive runs
the `ycharts` root moved from `No changes` to a pending `aws_ec2_instance_state.runner` change,
because a sibling touched the IB-s-8 host. **All five verdicts were identical across both runs**;
what moves is arm (e)'s narrative, not its answer.

---

## What went wrong in my own instruments

Three, each caught by two instruments disagreeing or by reading the actual diff.

1. **The ownership classifier labelled my own function FOREIGN.** A module-nested address
   (`module.irpt_export_render.aws_lambda_function.this`) has the inner name `this`, which
   appears in no root `.tf` -- so a name-only test called this order's own resource someone
   else's. That is precisely the self-serving label the classifier exists to avoid. The
   declaring token for a module-nested address is the **module** name.
2. **The first classifier called the SSM document "OURS"** because this branch declares that
   resource -- when the diff was that the live document is a sibling's version 3 and this
   branch's content is older. The resource was declared here; the **diff** was not. Reading the
   actual 21 removed lines is what showed it.
3. **Four roots reported `rc 1`** in the first graded run -- a missing `terraform init` in a new
   worktree, not a measurement. An rc is not a reading.

---

## Rows filed

| id | hazard | one line |
|---|---|---|
| `W3-S19` | ARMED | A two-part change was split by the drain: the code half merged, the packaging half did not, and the source map declared builds for two functions that cannot import. |
| `W3-S20` | ARMED | A sibling is writing to the shared export Terraform state while this order is non-terminal; converging from here would destroy one live resource and revert two. |
| `W3-S21` | ARMED | The `irpt-common` layer's own `BUILD_MANIFEST` disagrees with the layer that is published -- a wrong record on a surface three functions share. |
| `W3-S22` | ARMED | Two modules named `dispatch.py` collide on the flat `sys.path`, so IB-rt-8's own tests cannot see its dispatch module; in a zip carrying both, one would overwrite the other. |

---

## What this arm set does NOT show

1. **The export root is left non-converged**, by a sibling's in-flight work. This order's change
   is deployed and verified; the residual is named, addressed and rowed, not swept.
2. **`intake/parse.py` and `intake/corrections.py` are still in no function's file list**, so
   three of the ten error paths fixed in the first pass serve nothing today.
3. **Arm (c) counts except handlers**, not every expression that reaches a public reason
   (`W3-S15`).
4. **The `_authz/dispatch.py` collision is latent, not fixed** -- no function packages both
   today, and renaming either is another cell's module.
