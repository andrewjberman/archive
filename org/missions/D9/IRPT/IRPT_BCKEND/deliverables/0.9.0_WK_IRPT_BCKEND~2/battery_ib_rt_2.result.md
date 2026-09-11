# BATTERY IB-rt-2 -- GUARD THE SIX -- RESULT

**Run:** 2026-09-11 by `0.9.0_WK_IRPT_BCKEND~2` on branch `wk-irpt_bckend-2-2`, worktree
`/c/tmp/wk-irpt-2-2`, cut at `fa89acb5d3`; artifacts committed at `4356085122`.
**Invocation:** `timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2/battery_ib_rt_2.py`
**Token expected by RT2-AC1:** `IBRT2-SIX-GUARDED`
**Token emitted:** **NONE.** `BLOCKED: 3 of 10 arms FAIL or are BLOCKED -- the token is withheld.`

> **RT2-AC1 IS A FAIL AND THE ORDER STAYS OPEN.** Seven arms are met on real artifacts; three are
> blocked, each by a condition this order's `<paths>` cannot reach and each carrying a row with
> `2.0.0_SA_COO~B` as its disarm owner. **Nothing was applied and no ledger entry was opened.**

---

## SUMMARY

| arm | verdict | the number |
|---|---|---|
| a1 zero in lane | **PASS** | **0 of 8** routes this order may open reach an unguarded handler |
| a2 zero over the whole file | **BLOCKED** | **3 of 11** still do; all three are `irpt-status`'s (row W2-S19) |
| a3 the control fires | **PASS** | **3 of 3** victims move the verdict to `1 of 8` |
| b the swaps | **PASS** | **30 of 30** in-lane, 0 protected bytes in 30 of 30; **6 of 36 out of lane** |
| c the firm is the principal's | **PASS** | **5 of 5** refuse a claimed firm; **5 of 5** serve a reconciling one |
| d the projection | **PASS** | **5 of 5** `UNPROJECTED_GRANT`; **5 of 5** distinguish a revoked grant |
| b/c/d the envelope | **PASS** | **5 of 5** refusals carry a full `StatusEnvelope` |
| e deployed and verified | **BLOCKED** | **0 of 5** roots applied (rows W2-S21, W2-S22, W2-S24) |
| f the principal | **PASS** | **HUMAN-GATED**, 9 of 9 required elements, 0 secret values |
| g envelope conformance SERVED | **BLOCKED** | **0 of 11** deployed responses; in process **1 of 5** conform, **5 of 5** version refusals |

**7 of 10 arms PASS.**

---

## THE MEASUREMENT THAT CHANGED THE SHAPE OF THE CELL

Before anything was built, the census over the **real** entry points read **11 of 11 routes
unguarded** -- not the `6 of 11` the face inherits. Every one of the six dispatched functions'
DECLARED entry point was unwrapped, including the five the summary treats as already done.

The old number counted a route table the round-1 battery had partly populated itself. That is row
`IRPT_BCKEND-W1-S10`'s own lesson recurring inside the summary that records it, and it is now row
`W2-S20`. So the population here is **derived from three artifacts nobody writes for this census's
benefit**: the published `routes.json`, `lambda-source-map.json` (each function's `source_dir` and
`tf_file`), and that Terraform file's own `handler = "<module>.<attr>"`.

**The work was larger than the face's summary, not smaller.** Nothing was skipped on the strength
of the old number.

---

## ARM (a) -- ZERO OF N, AND THE CONTROL

```
denominator: 12 published route(s) = 11 with a declared handler + 1 without
  EXCLUDED, named and not counted: holdings-snapshot -- no handler at this vintage
IN LANE (the 5 functions this order's <paths> name): 0 of 8 unguarded
WHOLE FILE                                         : 3 of 11 unguarded
  out of lane: GET .../analysis/{jobId}/sections  -> irpt-status
  out of lane: GET .../status                     -> irpt-status
  out of lane: GET .../status/{jobId}             -> irpt-status
```

**`a2` IS BLOCKED, NOT GRADED AROUND.** The criterion's bar is `0 of N` with N = handler-bearing
routes = 11. Three of them dispatch to `irpt-status`, whose source directory
(`infra/aws/lambda/investor-reporting/ops/`) and Terraform root
(`infra/aws/terraform/investor-reporting/ops/`) appear in **neither half** of this order's
`<paths>`. The wrapper cannot be put on a handler this order may not open, and the preflight's own
rule is followed: *"a path you need that is not listed is a BLOCKING row, never an override."*
Row `IRPT_BCKEND-W2-S19`.

**THE CONTROL.** A throwaway copy of the **table** -- never of a handler, nothing in the real tree
patched -- with exactly one entry replaced by an unwrapped function reads `1 of 8`, for three
different victims. One victim would not distinguish a working census from one that checks index 0.

**AND THE MARK THE CENSUS TRUSTS IS EARNED.** `unguarded_routes()` trusts exactly one thing:
`__irpt_guarded__` on the object the route reaches. A module that merely SET the attribute would
make the census agree with it by construction. So `served.py` runs the **real** `Enforcer.guard()`
decorator at import on a probe function and **refuses to load** if the result is not marked; and
`Entry.handle` re-asserts it on the callable it is about to run. Neither is the evidence that the
guard WORKS -- the thirty swaps are.

---

## ARMS (b) (c) (d) -- THROUGH THE REAL ENTRY POINTS

**The subject is the deployed entry point.** Each case calls the very `lambda_handler` that the
published route file plus each function's Terraform `handler =` string resolve to. **The only
substitution is the storage boundary** -- IB-s-3's recorded artifacts instead of S3 -- and it
carries a **difference control**: the same recorded artifacts **serve** the authorized request and
**refuse** every swap. If the substitution were doing the work, both would look the same.

```
irpt-directory-search      firm   REFUSED FIRM_BINDING | advisor SERVED, 0 of 7 authorized-only ids
                           account/relationship/report/pdf  REFUSED OBJECT_NOT_COVERED
irpt-export-render         firm   REFUSED FIRM_BINDING | advisor REFUSED NOT_READY | 4x OBJECT_NOT_COVERED
irpt-narrative             firm   REFUSED FIRM_BINDING | advisor REFUSED OBJECT_NOT_COVERED | 4x OBJECT_NOT_COVERED
irpt-performance-adapter   firm   REFUSED FIRM_BINDING | advisor REFUSED NOT_AUTHORIZED | 4x OBJECT_NOT_COVERED
irpt-ycharts-generate      firm   REFUSED FIRM_BINDING | advisor REFUSED INVALID_INPUT | 4x OBJECT_NOT_COVERED
```

**"REFUSED" IS THE WRONG BAR FOR ONE OF THE SIX, AND SAYING SO IS THE POINT.** Five swaps name an
object or a firm the swapped request may not have, and those must be refused. The **advisor** swap
is different in kind: `ADVISOR_B` is a real advisor of the same firm with a grant of its own, so a
LIST operation answering it is correct behaviour -- the answer is not refused, it is **different**.
What must hold is that it never WIDENS, and the case asserts exactly that: **0 of 7** of the
authorized advisor's ids appear in the swapped advisor's answer. A refusal-only assertion would
never have checked the property that matters.

**THE BYTE CENSUS IS RELATIVE TO WHO IS ASKING.** `A5` and `ADVISOR_B` are advisor B's own account
and id: protected from advisor A, not protected from advisor B. A list that protected them
unconditionally fails on a right answer; a list that never protected them passes on a real leak.
**0 protected bytes in 30 of 30 refusals**, and the caller's own firm id is present because the v1
envelope requires it.

**(c)** A firm token in the body that disagrees with the verified principal is refused
`FIRM_BINDING` on **5 of 5**, and the refused value appears nowhere in the response. A claim that
AGREES is not an obstacle on **5 of 5**.

**(d)** A grant whose ids never join the directory refuses `UNPROJECTED_GRANT` on **5 of 5** rather
than serving the empty set it produces -- and **5 of 5** distinguish it from a REVOKED grant. The
two are indistinguishable in the RESULT; only the order of the checks tells them apart, and the
revoked case is what holds that order in place.

---

## ARM (e) -- DEPLOYED AND VERIFIED -- **BLOCKED, NOTHING APPLIED**

**0 of 5 roots applied. 0 of 5 `CodeSha256` verified. 0 ledger entries opened.** Three independent
blockers:

1. **THE BUILD INPUTS DO NOT RESOLVE** (row `W2-S21`). `irpt-ycharts-generate` declares 25 files of
   which **7 have never existed in this repository** -- and `git ls-tree` at `88c97c1529`, the very
   commit IB-s-9's CLOSED ledger names as "the COMMITTED source ... 25 members, byte-identical
   rebuild", does not carry them. `irpt-status` declares 7 of which 5 are absent.
   `irpt-directory-search` fails the builder's own disk-to-manifest parity check because two
   functions share one source directory. **The hazard is not the missing files; it is the green
   they produced** -- a closed ledger entry records a reproducibility that cannot be reproduced.
2. **ANOTHER CELL IS APPLYING THE EXPORT FUNCTION THIS WINDOW** (row `W2-S22`). The issuer's own
   hand-off says IB-rt-4 is re-applying its error-path envelope on `irpt-export-render` from slot
   ~3, while this order's `<paths>` grant `export/` and its Terraform root to this cell.
3. **THE SHARED CODE HAS NO IN-LANE CARRIER** (row `W2-S24`). `_authz` reaches the zips through the
   `irpt-common` LAYER, whose source dir, build script and `lambda-layer-map.json` are outside this
   order's `<paths>` -- and the layer was republished as **v5 at 13:08Z today** by another cell. The
   per-function alternative is vendoring, and **0 of 7** IRPT lambda directories carry the
   `BUILD_MANIFEST.json` the estate's own `vendor-manifest.sh` reads.

**A deploy whose input cannot be reproduced, on a function another cell is applying, is the
half-landed state NEVER-2 exists to prevent.** The code is committed; the deploy is the issuer's to
sequence.

---

## ARM (f) -- THE PRINCIPAL -- **HUMAN-GATED**

The mint path EXISTS and is named: authorizer `opal-portal-authorizer` verifying RS256 against the
secret **named** `opal/auth/jwt-public-key`; `generateAccessToken()` signing with the secret
**named** `opal/auth/jwt-private-key`; principals in DynamoDB `opal-users-v2`; the claims the edge
reads at `jwt.ts:167-187`; and a PRECEDENT -- a throwaway user created, exercised and
**verified-deleted** by `0.7.0_AE_CloudOps` in one bounded run.

**A worker may not walk it**: it is outside this order's `<paths>`, it is a write to the production
authentication plane, and the only alternative -- signing a token with the private key -- is a
worker reading a credential to mint itself an identity. **No secret value was read and none appears
in the record** (0 of 3 value-shaped tokens; names only).

The record names the operator's exact act, and it names the thing that would otherwise be
over-read: **the act belongs AFTER the deploy.** Run today it would reach the old unguarded handler
and return a passing-looking 200 from the very code this cell exists to replace.

`deliverables/0.9.0_WK_IRPT_BCKEND~2/RT2_test_principal_human_gated.md`.

---

## ARM (g) -- ENVELOPE CONFORMANCE, SERVED -- **BLOCKED**

```
IN PROCESS, against the v1 response contracts:
  irpt-directory-search      directory-search     CONFORMS
  irpt-export-render         refused NOT_READY
  irpt-narrative             refused INVALID_INPUT
  irpt-performance-adapter   refused DEPENDENCY_UNAVAILABLE
  irpt-ycharts-generate      refused INVALID_INPUT
  served-and-conforming: 1 of 5 in-lane function(s)
the X-Contract-Version check, IN PROCESS: mismatched refused CONTRACT_VERSION 5 of 5; absent 5 of 5
```

**`directory-search` is the first route in this project whose response validates against its v1
response contract.** Getting there surfaced two contract-vs-handler disagreements worth naming:
`search()` returns ranked HITS (`entry_id`, `match_score`) which are a search result and not a
`DirectoryEntry`, so the entry now returns the full documents from `project()` **in search rank
order**; and a partly-permitted entry is **withheld and counted in `status`**, never trimmed into a
document that looks whole.

**THE VERSION CHECK IS REFUSED WITH THE STORAGE LOADERS REMOVED** -- the loaders are replaced by
functions that raise. If anything read a firm's artifacts before the version was checked, the case
would raise instead of refusing. That is the proof of the ordering, not an assertion about it.

**THE DEPLOYED HALF IS 0 of 0 AND IS PRINTED AS VACUOUS.** Nothing was deployed (arm (e)), so the
`X-Contract-Version` check is **COMMITTED AND NOT SERVED** and there is no deployed response to
validate. The amendment's denominator -- routes with a DEPLOYED handler at this HEAD -- is zero
until the deploy lands.

**AND NO REFUSAL CAN EVER VALIDATE AGAINST A RESPONSE CONTRACT** (row `W2-S25`): v1 requires
`firm_id` (the opaque id, which only exists inside a firm's directory artifact) and `data` (the
document, with no null branch). A version refusal must answer *before* any bucket is read, so it
has no legal value for either. The amendment's own words provide for this -- *"two shapes of one
family"* -- and refusals therefore use the `_authz` shape with a `StatusEnvelope` in `status`.

---

## FOUR DEFECTS THIS CELL FOUND IN ITSELF BEFORE THEY COULD BE SERVED

| what | why it read as fine | row |
|---|---|---|
| the published operation ids are hyphenated and `_keys.OPERATION_RE` admits no hyphen, so **every** guarded request was refused `KEY_REFUSED` | `KEY_REFUSED` is a legitimate member of the vocabulary, so "was it refused" was satisfied; only printing the CODE per swap showed all thirty were refused for one wrong reason | `W2-S26` |
| five entry modules and the shared boundary were all called `entry` -- in a flattened zip, the deployed function importing itself | the in-process census caught it as `partially initialized module`, which is the same defect the runtime would have hit | -- |
| three `handler.py` plus `job.py` and `status.py` share one interpreter, so performance got the DIRECTORY handler | it raised `AttributeError`, which the boundary classified as `UNEXPECTED` -- a wrong answer with a plausible code | -- |
| two authorized requests landed in the residual reason | `UNEXPECTED` is a declared member, so nothing failed | -- |

---

## ROWS FILED BY THIS CELL

| id | class / standing | what |
|---|---|---|
| `W2-S19` | **BLOCKING / ARMED** | `ops/` is in neither half of the grant; 3 of 11 routes cannot be guarded here |
| `W2-S20` | OBSERVATION | the real census reads 11 of 11 unguarded, not the inherited 6 of 11 |
| `W2-S21` | **BLOCKING / ARMED** | two served functions cannot be rebuilt from committed source; a third fails the parity check |
| `W2-S22` | **BLOCKING / ARMED** | two cells are pointed at one served function in one window |
| `W2-S23` | OBSERVATION | the ONE error envelope's closed vocabulary cannot express `CONTRACT_VERSION` |
| `W2-S24` | **BLOCKING / ARMED** | no in-lane carrier distributes `_authz` to the five zips |
| `W2-S25` | OBSERVATION | v1's response contracts have no refusal representation |
| `W2-S26` | OBSERVATION | the published operation ids are not admissible key components |
| `W2-S27` | OBSERVATION | a THIRD firm id spelling, on the vendor-routing axis |

---

## WHAT THIS BATTERY CANNOT SHOW

Everything between a client and `Entry.handle`: that the edge validator injects the headers this
boundary trusts for a token the authorizer accepted; API Gateway authorizer `naqxlm`'s result cache
and therefore a revocation's time-to-effect; and whether the deployed bytes are these bytes. Those
are the operator act in the HUMAN-GATED record and `IB-rtb-1`'s deployed replay. **An in-process
run grades the authorization DECISION; only the deployed replay grades the WIRE.**
