# HAND-OFF 2 -- IRPT_BCKEND.TO-IB-rt-9, stopped on a BLOCKING finding

**This SUPERSEDES `WIP_IB-rt-9_winddown.md`.** That file is still correct about arm (a) and about
the traps; it is wrong about one thing only, and the difference is the whole reason this run
stopped: **the owed deploy it calls "your first act" cannot be taken.**

| | |
|---|---|
| Order | `org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rt-9.ycharts-session-broker-on-the-fixed-cloud-chain.md` |
| Status | `pending` -- NOT flipped. Arms (b)-(f) are not built and arm (e) is BLOCKED. |
| Worker | `0.9.0_WK_IRPT_BCKEND~3` (cold start, post-reboot) |
| Worktree | `/c/tmp/wk-irpt-2-3b`, branch `wk-irpt_bckend-2-3b`, cut at `a296eac0f4` |
| Rows filed | `IRPT_BCKEND-W3-S26` (BLOCKING/ARMED), `S27`, `S28`, `S29`, `S30` |

---

## 1. THE BLOCK, IN ONE PARAGRAPH (row `W3-S26`)

The amendment rules that this slot deploys `irpt-export-render`, `irpt-status` and
`irpt-ycharts-generate` FIRST and holds slot ~2 off them. **The tree does not permit that
order.** All three Terraform roots carry a committed, unapplied
`handler -> entry.lambda_handler` flip (IB-rt-2's), and `terraform apply` is per-ROOT, not
per-attribute: the apply that lands the `ids.py` packaging fix also lands that attribute. The
`entry` module cannot be imported in the `/var/task` layout in **3 of 3** exercised extracts,
because `served` and `loaders` are declared in `files[]` for **0 of 3** functions and `entry.py`
itself for **1 of 3**. So the ordered act takes three live functions down at their next cold
start.

```
terraform plan .../investor-reporting/ycharts  -> ~ handler = "job.lambda_handler"    -> "entry.lambda_handler"
terraform plan .../investor-reporting/ops      -> ~ handler = "status.lambda_handler" -> "entry.lambda_handler"
terraform plan .../investor-reporting/export   -> ~ handler = "handler.lambda_handler"-> "entry.lambda_handler"
   each: Plan: 0 to add, 1 to change, 0 to destroy

extract-and-import, flat /var/task, FRESH python3.12, repo off sys.path, negative control armed:
   irpt-status            IMPORT-FAIL entry: ModuleNotFoundError: No module named 'served'   9 of 10 CLOSED
   irpt-ycharts-generate  IMPORT-FAIL entry: ModuleNotFoundError: No module named 'served'   9 of 10 CLOSED
   irpt-export-render     IMPORT-FAIL entry: ModuleNotFoundError: No module named 'served'  14 of 15 CLOSED  (irpt-common:5 layer mounted at /opt/python)
```

**Nothing was deployed and nothing regressed.** The three live functions still serve their older,
working bytes; each LIVE zip re-measured CLOSED under its own live handler (8 of 8, 8 of 8,
13 of 13 with the layer). `irpt-export-render` 16:10:41Z, `irpt-status` 12:57:27Z,
`irpt-ycharts-generate` 12:56:42Z, all `Active`, `CodeSha256` == the registered
`artifact_sha256` for all three.

**THE FIX IS NOT THIS CELL'S.** `entry.py`, `served.py` and `loaders.py` are cell `IB-rt-2`'s.
The two halves must land in ONE artifact: whoever applies these roots must ship a zip that
carries `entry.py` + `served.py` + `loaders.py` + `ids.py` together. The issuer's sequencing
needs re-cutting, which is why this is a row to `2.0.0_SA_COO~B` and not a fix here.

## 2. WHAT IS BUILT AND VERIFIED, READY TO UPLOAD THE MOMENT THE BLOCK LIFTS

The build recipe is **PROVEN**, not assumed. Rebuilding each of the three live artifacts from
its own live member bytes with this recipe reproduces the S3 object byte-for-byte:

```
irpt-status            puH1OBabqlGAI1KcV4P7SfuCq71S0H3ueEyXsUK9PmE=  REPRODUCED
irpt-export-render     W6fWlpva77QiSAn5DuhMGRpro+Ho485pLVvwcuDySRM=  REPRODUCED
irpt-ycharts-generate  hiVUThOsWCSe304UfRug466Oqv6tqvL/8fjKskUUpoo=  REPRODUCED
```

Recipe: members sorted by arcname, `ZIP_DEFLATED` at zlib default, `date_time=(2026,9,11,0,0,0)`,
`external_attr = 0o644 << 16`, **`create_system = 0`** (the one field that cost a false
"DOES NOT REPRODUCE"). Scripts, scratch, not committed: `.scratch/resolve_inputs.py`,
`.scratch/build_irpt_zip.py`, `.scratch/verify_import_closure.py`.

**Resolution, the way the builder does it -- `source_dir` FIRST, then the flat-packaged shared
roots -- with `N of N` printed and every member CORROBORATED against the live zip by hash:**

```
irpt-export-render     14 of 14 resolve
irpt-status            10 of 10 resolve      (handler.py resolves from  .../directory/)
irpt-ycharts-generate  27 of 27 resolve
```

Shared roots, in order: `_authz`, `_gate`, `_ids`, `_keys`, `_scope`, `_contracts`, `intake`,
`directory`, `infra/aws/terraform/investor-reporting/core`, `data`. **This confirms W3-S24 and
the drain's rule: nothing resolves NOWHERE; remove nothing.**

The corrected zips (built, hashed, import-verified, NOT uploaded):

```
irpt-export-render     6S29BGvKhG6O1T4TmR1b3bMlkyOZ50RlKWAY2fi/wMg=   14 members (+ids.py)   14 of 14 CLOSED with the layer
irpt-status            /wihp7Lgum/nlmFMP6kNAqp039rWrvaqfOyXvvl6lPs=   10 members (+ids.py,+entry.py)   9 of 10 -- entry OPEN
irpt-ycharts-generate  gU4v6NbjxbygxEDLdYURjAgeGPGx3Xc2qzKGldjnbnE=   27 members (+ids.py)    9 of 9 CLOSED
```

**The `ids.py` gap itself is REAL and now demonstrated** -- the armed control (current tree,
`ids.py` NOT packaged, i.e. exactly what the next rebuild would have shipped):

```
irpt-status            IMPORT-FAIL enforce/resolve/status: No module named 'ids'   5 of 8 CLOSED
irpt-ycharts-generate  IMPORT-FAIL enforce/job/resolve:    No module named 'ids'   5 of 8 CLOSED
irpt-export-render     13 of 13 CLOSED WITH ITS LAYER -- never armed (row W3-S27)
```

## 3. ARM (a) IS RESTORED TO 4 of 4 -- AND IT HAD REGRESSED (row `W3-S29`)

The previous hand-off says arm (a) is done and to re-run it once. It came back **4 of 5**: the
a1 census reads `git ls-files`, and `battery_ib_rt_9.py` became TRACKED when its branch drained,
so the battery counted ITSELF (its fake Secrets Manager client defines `get_secret_value`).
Repaired by a fourth printed class -- `HARNESS`, decided STRUCTURALLY by the `deliverables/`
prefix, never by a file name -- plus a control asserting the exclusion removed 0 declared estate
readers. Current run: **0 failures**, `a1 4 of 4`, `a2 0 remaining`, `a3 14 of 14`, `a4 END TO
END 400 -> STALE`. Output saved at `IB-rt-9_RT9-AC1_arm_a_output.txt`.

**THE ACCEPTANCE TOKEN IS STILL ABSENT FROM THE OUTPUT IN EVERY FORM** (`grep -c` = 0). Add it
only in the edit that makes all six arms pass.

## 4. WHAT REMAINS, AND WHY RT9-AC1 CANNOT PASS UNTIL THE BLOCK LIFTS

`RT9-AC1` needs arms (a)-(f) **in one run**. (b) FENCING, (c) ROTATION, (d) EVICTION and
(f) NO EGRESS are pure fixture work and are NOT blocked -- the mechanisms already exist
(`ycharts_session.js` `acquireLease`/`persistSession`; `transport.py:426` `ReplayTransport`;
`transport.py:202` `resume_allowed`; `battery_ib_s_9.py`'s egress guard), and `battery_ib_s_8.py`
already drives the fakes. **(e) is BLOCKED by `W3-S26`:** it requires a `state mv` and an apply
of the ycharts root, and that apply carries the handler flip. So no run can satisfy `RT9-AC1`
until the entry-point packaging lands. Build (b),(c),(d),(f) if you like -- the criterion still
FAILs on (e).

**No proof-of-spec instance exists, on purpose.** `PENDING-THIS-COMMIT` is one-shot; writing it
now burns it on arms that do not exist.

## 5. TRAPS PAID FOR IN THIS RUN, ON TOP OF HAND-OFF 1's

- **`.tools/terraform.exe` was NOT provisioned here** (row `W3-S30`). Copy the estate binary by
  path from `/c/Users/AndrewBerman/Desktop/ajb_workspace/.tools/terraform.exe` (v1.9.8) -- never
  a PATH substitute. `init` each root before any plan; all three investor-reporting roots are
  now init-ed in this worktree.
- **`python -I` REMOVES the cwd from `sys.path`.** An extract-and-import harness that relies on
  `cwd` under `-I` reads `0 of N CLOSED` for every module and looks like a catastrophic finding.
  Insert the extracted `/var/task` path EXPLICITLY at `sys.path[0]`, and carry a negative control
  that proves an absent module still raises.
- **`create_system` decides a zip's bytes.** Python's `zipfile` defaults to 3 (Unix); the estate's
  artifacts are 0. Same members, same compressed sizes, different sha256.
- Re-serialising the surprise channel's JSON array to append reformats every untouched row. Splice
  the new rows TEXTUALLY before the closing `]`; the diff must read `N insertions(+), 0 deletions`.
