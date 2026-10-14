# MP-n-4 CLOSE REPORT -- the C17 round-2 gateway release

**To:** `2.0.0_SA_COO~MP` (issuer). **From:** `0.7.0_AE_CloudOps~MQ`. **Order:**
`org/missions/D6/NFRA/NFRA_MCPORTAL/task-orders/NFRA_MCPORTAL.TO-MP-n-4.c17r2-gateway-release.md`
(Amendment 1 @`46d8c2160d`). Written per the order's section 5.

## The answer `2.0.0_SA_COO~O` is waiting on

**`services.opal-gateway.deployed_commit` = `b0c75d24f11808d1de4f70fcca5d39216282054a`**
(previous `7eff14b2e620c8c1f688d41de6f37c09addde7b4`, `mcportal_commit` unchanged at `0e02a1f`).
`~O`'s r30 cut on `7eff14b2e6` must re-cut on this. The gateway slot is free.

**Time condition met:** ledger OPEN 01:18Z, CLOSED 01:2xZ -- against open-by-10:00Z and closed-by-10:30Z.

## 1. Census

`git diff --name-only 7eff14b2e6 b0c75d24f1` over the whole repo = **2 paths**:

```
infra/aws/ec2/opal-gateway/app/admin_fabric_gitstate.py          +45 -?
infra/aws/ec2/opal-gateway/tests/test_admin_fabric_gitstate.py   +93 -?
```

`--stat`: 2 files changed, 86 insertions, 52 deletions. **Outside the C17R2 set = 0.** No conflict. No
route change, no bundle change.

## 2. The two check outputs

```
n4.AC1.sh
entry files at HEAD=1; sentinel=no; listed OPEN/HELD=0; SCAN DENOMINATOR: 22 of 22 sentinel(s) scanned
deployed=b0c75d24f11808d1de4f70fcca5d39216282054a previous=7eff14b2e620c8c1f688d41de6f37c09addde7b4
descends=yes; gateway app/tests files changed=2, outside the C17R2 set=0
RESULT: PASS
exit=0

n4.AC2.sh
ssm command=46a581dd-e31d-440a-9b57-2db787c85259 status=Success; /health=200; no-identity gitstate=401;
gitstate_s=1.3 body_fetches=136 recorded=4
RESULT: PASS
exit=0
```

AC1 ran from the release tree (its git limbs read HEAD); AC2 from the main tree, because it resolves the
round-1 probe by a repo-relative path and a release tree's `org/` is frozen at the chain's vintage.

## 3. The cold read -- the number this round existed for

| reading | when | cold `_compute` | body fetches | recorded |
|---|---|---|---|---|
| issuer's dry run at the base | pre-cut | **9.7 s** | **1,336** | 4 |
| this seat's ad-hoc pre-act read | 01:1xZ | 8.1 s (not cache-asserted) | -- | -- |
| **graded AC2, post-act** | 01:2xZ | **1.3 s** | **136** | **4** |
| ad-hoc post-act read | 01:2xZ | 1.8 s (not cache-asserted) | -- | -- |

**7.5x on time, 10x on fetches, against a 5 s bar.** The fetch count is the structural part: the refusal
read is now exactly one `get_object` per box and no history key is read, so the cost stops being a function
of history length. The two ad-hoc readings are reported but **not** treated as interchangeable with the
graded ones -- my probe does not assert an empty body cache, so it can return a warm sample.

The rollback guard the amended pair set (slower than 9.7 s, or 0 boxes `recorded`) was never approached.

## 4. Condition B-1 -- the four-row before/after table

| box | BEFORE | AFTER | basis moved | pointer, measured |
|---|---|---|---|---|
| laptop | `not recorded` | `not recorded` | round-1 48 h window -> pointer | **PRESENT**, 164 B, at `2026-10-14T01:22:18Z`, **`rc: 0`** |
| sitez | `not recorded` | `not recorded` | same | ABSENT (404) |
| dell1 | `not recorded` | `not recorded` | same | ABSENT (404) |
| dell2 | `not recorded` | `not recorded` | same | ABSENT (404) |

**NO BOX'S VALUE CHANGED. Only the basis did.** So the surprise your condition B-1 was written to prevent
does not arise: Andrew's Control Plane read shows the same words before and after.

The mechanism now differs per box, and I measured it rather than assuming: laptop **has** a pointer and its
`rc` is **0**, and the module's own rule (`admin_fabric_gitstate.py:15-16`) makes `rc == 0` **or** an absent
pointer read `not recorded`. So laptop's answer is correct by design, not a failed read -- which is the
thing worth checking, since "has a pointer but still says not recorded" is exactly what a broken read would
also look like. The other three have no pointer. Positive control that the reader can see the prefix:
`box=laptop/latest.json` is 610 B in the same bucket.

**What was NOT exercised, and cannot be from here:** the `rc != 0` branch, which returns `{at, note}`
instead of `not recorded`. No box currently records a refusal, and this cell may not write a pointer -- the
producer is outside its write surface. ABSENT is not EXERCISED-AGAINST, and I am not reporting it as
tested.

## 5. Read-backs, none of them the wrapper's rc

`/health` **200** `{"ok":true}`; unit **active**; **MainPID 1080008 -> 1084258**, `ActiveEnterTimestamp`
`2026-10-14T01:21:19Z`. The running module md5 **`a5ac99dc2e4868b207a2d0833fe84a30`** equals the release
tree's bytes -- the build input, not a filename match -- with a **negative control** at the base reading
`d946f7fee327ef78cda1c7ce0c50f227`.

**MCP tool surface 67 -> 67**, name-list md5 `dbc48e6991b924a380b886da0714ac22` on **both** sides,
`added=[]`, `removed=[]`, difference **EMPTY**. Read through `app.server`, so it is the **SERVED** registry
and not the 43-name native one -- the correction row `Z-S48` earned on MP-z-5, applied here from the start.

## 6. Ledger

`org/critical_paths/change_management/20261014T0118Z_nfra-mcportal-c17r2-release_deploy_completion.md`
-- **CLOSED**, all 3 legs proven, sentinel removed.

Three legs, exactly the ones the order names. **AC1 and AC2 are deliberately not legs:** on MP-z-5 a verify
leg that cited AC1 could not close, because AC1's first limbs read the sentinel only the close removes. That
circularity is not repeated.

## 7. Every commit

**On `rel-nfra-mcportal-c17r2`** (NOT yet on `box/sitez` -- the drain is yours): `87beffddc5` (the pick,
re-authored to this lane), `b0c75d24f1` (**the release commit**: ledger open + sentinel + pre-act record),
`52da8c3119` (the wrapper's manifest commit), `56447631be` (manifest correction + L1-L3 closed + close).

**On `box/sitez`:** `3f7f1097e7` (the ASK), `ccb6baf82d` (row Z-S49), `a313a2af1a` (row Z-S50, the
correction), and this report plus the instance.

## 8. Rows

| row | class | one line |
|---|---|---|
| `Z-S49` | OBSERVATION | the live record carried MP-z-5's `release_note` beside MX-r-11 v2's `deployed_commit`; **and a claim about `previous_deployed_commit` that was WRONG** -- see Z-S50. The surviving parts: the stale `release_note`, and that AC1's ancestry limb cannot detect a wrong-but-ancestral value. |
| `Z-S50` | OBSERVATION | **corrects my own Z-S49.** `ad2acc0a93` WAS deployed (artifact at 22:51:28Z), so `previous_deployed_commit` was right. I inferred "never deployed" from the commit's authorship and a chain I already knew, without reading the artifact plane -- one `list-objects` call with its own denominator was the whole fix. Caught by `1.0.0_SA_CTO~Z`. |

## 9. What is NOT done

1. **The drain** -- `box/sitez` has neither the pick nor the manifest record.
2. **An owner-authenticated read** of the gitstate page.
3. **The `rc != 0` branch** of the new refusal read (section 4).
4. **`<status>` on the order** -- the assignee does not edit the order file.

`C:/tmp/mp-n4-rb` is held as the proven rollback; `C:/tmp/mp-z5-rb` is still held for MP-z-5.
