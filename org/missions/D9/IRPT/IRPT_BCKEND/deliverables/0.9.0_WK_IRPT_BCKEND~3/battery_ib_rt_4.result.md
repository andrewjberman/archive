# `battery_ib_rt_4.result.md` -- RT4-AC1, five arms, **4 of 5 -- FAIL**

**TO:** `IRPT_BCKEND.TO-IB-rt-4` | **cell:** `IB-rt-4` (PRD cell B17) | **assignee:** `0.9.0_WK_IRPT_BCKEND~3`
**Branch:** `wk-irpt_bckend-2-3` | **worktree:** `/c/tmp/wk-irpt-2-3` | **base:** `7478fdf144`

**Invocation (the one the task order names):**
```
timeout 600 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/battery_ib_rt_4.py
```
**rc 1. `ARMS: 4 of 5`. `IBRT4-KEYS-TYPED` WITHHELD.** Full verbatim output:
`org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3/IB-rt-4_RT4-AC1_battery_output.txt`.

**The order stays open.** Arms (a)-(d) -- the whole substance of CTO ruling 4 -- pass. Arm (e)
fails on one of five Terraform roots for a reason that is not this cell's code and cannot be
cleared by this cell's authority. That is row `IRPT_BCKEND-W3-S17` and it is the report.

---

## Arm (e) first, because it is the one that fails

`terraform plan` on `infra/aws/terraform/investor-reporting/export`, **before any change of
mine**:

```
# aws_iam_role_policy.export_render_dispatch will be destroyed
#   (because aws_iam_role_policy.export_render_dispatch is not in configuration)
# aws_iam_role_policy.export_render_evidence will be destroyed
#   (because aws_iam_role_policy.export_render_evidence is not in configuration)
# aws_ssm_document.export_render_run will be destroyed
#   (because aws_ssm_document.export_render_run is not in configuration)
Plan: 0 to add, 1 to change, 3 to destroy.
```

Three resources sit in **state** and not in **configuration**, left that way when IB-s-14
removed them from the `.tf` at `1beda4bf49` without applying. Two of them are **IAM role
policies on a live function**.

The face's own condition for this cell's deploy is *"plans show only the code changes"*. This
plan does not. Destroying two live IAM role policies is a served-surface act (bound 7) with a
blast radius nobody signed, and finishing another cell's half-landed change is not in this
order's rectangle. **So `irpt-export-render`'s code change is committed and its apply is
withheld.**

A second writer is also on that root: `irpt-export-render`'s served `CodeSha256` moved from
`11ZotLOJLP5xWjGU` to `iq1u0SatjV0+OtFJ` (LastModified `2026-09-11T12:57:39Z`) during this
cell's run, by no act of mine.

**What DID deploy, verified:**

| root | apply | post-apply plan |
|---|---|---|
| directory | `0 added, 2 changed, 0 destroyed` | `No changes.` |
| intake | `0 added, 1 changed, 0 destroyed` | `No changes.` |
| ycharts | `0 added, 1 changed, 0 destroyed` | `No changes.` |
| ops | `0 added, 1 changed, 0 destroyed` | `No changes.` |
| **export** | **withheld** | **`0 to add, 1 to change, 3 to destroy`** |

Every pre-apply plan on the four was checked **before** the apply and the only differing
attributes on any resource were `s3_object_version` and `source_code_hash`. Five of six
functions serve the new bytes with `CodeSha256` equal to the zip rebuilt from committed source
**and** to the source-map registration -- three values compared against each other rather than
any one asserted. Four ledgers CLOSED, 5 legs each, 0 open markers, each sentinel carrying two
commits (open at `48313e9c0e` before the act, removed at `a36c28a079`).

---

## The arms that pass

### (a) N OF N CONSTRUCTORS -- `27 of 28` refused, `0` leaks

**The denominator is read off the module by AST, not from a list I wrote:**
`11 public callables - 4 readers = 7 constructors`. A builder added later is in the denominator
whether or not anyone remembers this file.

**Measured at round-1 HEAD, six of twenty-four pairs were ACCEPTED:**

| constructor | display name | e-mail | raw upstream key | firm token |
|---|---|---|---|---|
| `s3_evidence_key` | **ACCEPTED** | refused | **ACCEPTED** | refused |
| `quarantine_key` | **ACCEPTED** | **ACCEPTED** | **ACCEPTED** | **ACCEPTED** |
| `cache_key` / `idempotency_key` / `key_digest` / `queue_message` | refused | refused | refused | refused |
| `TenantBinding` | refused | refused | refused | *admitted -- tenant position* |

**The ruling named only `s3_evidence_key`.** `quarantine_key` is the worse of the two to have
left open, and the reason is what quarantine *is*: a message is written there precisely when its
origin could **not** be verified, so its components are the least trusted input this system
handles. Row `IRPT_BCKEND-W3-S13`. Had this cell verified the one constructor the ruling named,
`quarantine_key` would have passed untouched and the round would have recorded W3-S12 closed.

**`TenantBinding` admitting a firm id in its tenant position is printed as an ADMISSION, not
counted as a refusal.** That is the one place a firm id belongs -- bound from the sender's
domain at ingestion, not supplied by a request. A rule that refused it everywhere would be
wrong, and hiding the exception in a pass count would be worse.

**Both holes are closed by a POSITIVE ALLOWLIST of segment shapes** -- digits, ISO date, 64-hex
fingerprint, namespaced opaque id, enum token, structural word, file name -- which are exactly
the shapes the round-1 evidence keys already contain. A blocklist of bad-looking values fails
open on the first name nobody thought of.

**The refusal carries no value, and seven renderings are censused per refusal**: `str()`,
`repr()`, `'%s'`, `'%r'`, an f-string, `exc.args`, and the public log line. `0` occurrences in
`27 of 27` refusals. One rendering is not a census -- a leak wearing a different syntax is the
same leak. `args` holds only the public message, so even a default traceback line is safe.

**`%r` placeholders inside a refusal construction: `0`.** The ruling says *twelve* become zero;
the module carried **eighteen across sixteen sites** when this cell measured it, so the fix is
defined by the census and both numbers are printed. Row `IRPT_BCKEND-W3-S16`. The six `%r` left
in the module are in `verify_against_layout`, comparing config to config.

### (b) THE POSITIVE STILL BUILDS -- `12 of 12` identical

**The oracle is the module at round-1 HEAD, loaded from git** -- not a remembered list of
expected strings, which the same hand that changed the code would have updated. Twelve round-1
valid inputs, including the IB-s-9 vendor-PDF key and the IB-s-10 sections key verbatim, build
byte-identical keys. **The refusal did not change the grammar.**

### (c) THE ENVELOPE EVERYWHERE -- `0 of 49` render the exception

25 modules, 49 except handlers, 18 binding the exception, **10 rendering it before this cell and
0 after**.

**The census is structural and it lives in the package, not the battery**
(`_authz/error_path_census.py`), so a later cell can re-run it. It counts `str(exc)`,
`repr(exc)`, a `%`-format operand, an f-string value and `.format(exc)`, and it does **not**
count `type(exc).__name__`.

**Its first cut reported TWELVE, and two were false positives** -- `directory/refresh.py` and
`ycharts/extract/extract.py` render only the exception's type, and `refresh.py` cites row
W2-S10 in a comment for doing exactly that. A census that over-fires sends a careful reader to
"fix" correct code and inflates the denominator its own fix is graded against.

**The sharpest of the ten was `intake/parse.py`:** a `jsonschema.ValidationError`'s first line
quotes the **instance**, so a holdings row carrying a client name went straight into a
contract-validation report. It now carries the failing keyword and the path.

`PUBLIC_REASONS` is a closed 14-member enum and `error_envelope()` refuses anything outside it.
There is **no parameter on it an exception fits into**, so the leak cannot type-check its way
back in.

### (d) INJECTED NEGATIVES -- `0 of 18`

A client name, an e-mail and an S3 key injected per family across six families. `0` occurrences
across body + headers + the public log. The envelope's only fields are
`['correlation_id', 'ok', 'public_reason_code']` -- **no field for a message, a stack or a path
to travel in**, which is stronger than a rule that they must not be set.

**And the correlation id resolves the other way:** the internal record *does* carry the detail,
for all 18. The detail moved; it did not disappear. A redaction that destroys the diagnostic
gets switched off the first time someone is debugging at 2am.

---

## What went wrong in my own instruments

Both were caught by having two instruments disagree, which is the only reason either surfaced.

1. **The battery reported a cleaner import closure than the truth.** `import_closure_report()`
   ran the check in-process and printed `6 of 6 CLOSED` while the standalone script printed
   `5 of 6`. The battery imports modules of its own first, so a packaged module's
   `import enforce` resolved from a leftover `sys.modules` entry instead of failing -- the check
   whose entire purpose is to prove a zip stands alone was leaning on the process it ran in.
   **A saved-and-restored `sys.modules` is not isolation; only a new interpreter is.** It now
   runs in a clean subprocess and reports `5 of 6`.
2. **The error-path census over-fired 2 of 12**, above.

The import-closure check exists at all because `CodeSha256` equality proves the bytes AWS serves
are the bytes we built and says **nothing** about whether they can be imported. It found a
second, unrelated defect: `export/download.py` has imported `enforce` at module level since
round 1 and `enforce.py` has never been in that function's zip, so the deployed download route
is dead on first call while every deploy-time rung reads green. Row `IRPT_BCKEND-W3-S14`.

---

## Rows filed

| id | class | hazard | one line |
|---|---|---|---|
| `W3-S13` | OBSERVATION | ARMED | The ruling named one leaky constructor; the census found two, and `quarantine_key` -- handling the least trusted input in the system -- accepted all four negatives. |
| `W3-S14` | OBSERVATION | ARMED | The deployed export download route is dead on import: it needs `enforce`, which its zip has never contained. |
| `W3-S15` | OBSERVATION | ARMED | Arm (c)'s denominator is except handlers; a public reason built on an ordinary return path is outside it, and one was reflecting caller input. |
| `W3-S16` | OBSERVATION | INERT | The ruling says twelve `%r` sites; the module carried eighteen across sixteen. |
| `W3-S17` | **BLOCKING** | ARMED | The export root would destroy three live resources that this ruling did not order; the apply is withheld and arm (e) fails. |
| `W3-S18` | OBSERVATION | ARMED | The source map's registered hash for `irpt-export-render` agrees with neither S3 nor the live function, and nothing standing catches that. |

---

## What this arm set does NOT show

1. **`irpt-export-render` is not running the fix.** Five of six functions are; that one serves
   round-1 bytes for the error path. The split is stated rather than averaged away.
2. **`parse.py` and `corrections.py` are in no function's packaged file list**, so two of the
   ten error-path fixes are not deployed anywhere by anyone. They are correct in the repo and
   serve nothing today.
3. **No S3 key already written was examined for a name-shaped component.** The bound forbids
   renaming one, and the census the `RT4-AC2` judgment record owes the CVO is a listing, not a
   move.
4. **The refusal's developer-only value can still be reached by a frame-locals dump.** No
   exception class can close that; it is closed by not enabling locals-bearing tracebacks in a
   request path, and it is stated in `errors.py`'s own docstring rather than left implied.
