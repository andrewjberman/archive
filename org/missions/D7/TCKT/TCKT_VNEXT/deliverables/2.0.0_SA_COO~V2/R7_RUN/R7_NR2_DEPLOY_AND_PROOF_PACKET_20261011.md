# Packet -- R7-nr-2 deploy and R7-nr-3 proof: an internal caller the users table does not know is refused (TCKT_VNEXT round 7)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-12 ~00:1xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** PRD `prd/TCKT_VNEXT_PRD.md` v0.4 ADDENDUM 3 @8bb81f8d6c (C-FENCE), ratified-text half signed by `3.0.0_SA_CVO`
(@b667a5fb11, re-stamped @6839e70629); the CTO's round-7 analysis; the CTO's ruling msg 6176 on the callers with no row.
Decomposition `decompositions/TCKT_VNEXT_DECOMP_R7.md`, cells `R7-nr-1` (built, merged @09488abbb1), `R7-ct-1` (the count,
@8d900213a1), `R7-nr-2` (this apply) and `R7-nr-3` (the proof, four direct invocations, in this same pair).

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant. **THIS APPLY NARROWS WHO IS SERVED.**

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `09488abbb1`; file sha256 `f99a314b1b6bc482b560de2fefb38a907cbc9f09e48d926c4450de072c0c6ab9` (`git show HEAD:<file> \| sha256sum`, this seat) |
| the diff from the live build's file | 5 added / 4 removed, all inside `_profile_scope`: the docstring, and `if not keys:` now prints one line and returns the failed-lookup 403 where it returned no scope. Every hunk read by this seat |
| tests on the merged tree | `NR-REFUSE-OK passed=5 of 5`; `NR-REGRESS-OK passed=201 failed=0`; `commit-gate.sh` clean (this seat, 23:5xZ) |
| live now | `opal-ticket-api` CodeSha256 `Ob/MZBEO...`, LastModified 2026-10-11T22:16:38Z, Active, Successful (this seat, `get-function-configuration`, 00:0xZ). The deployed handler was `b7764fbd` at the applier's last read (22:16Z); NOT re-downloaded by this seat since |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |

## 2. What moves

Every route that resolves a scope (list, get, claim, complete, report, metrics, create and commentary-sent among them), for ONE
class of caller: INTERNAL (firm `opal-capital`, not a service subject) whose lower-cased address has NO PROFILE row in the users
table's email index. Before: served with no firm fence. After: 403 `{"error": "firm scope lookup failed"}`, the same answer a
failed lookup gets, and one log line `FIRM-SCOPE-NO-ROW: <table> has no PROFILE row for an internal caller; refusing` that
carries no address.

**Not moved, each held by a test:** a row with no firm list (reads every firm); a row with an empty list (reads every firm); a
list of firms; a malformed value (refused); more than one row (refused); clients and service subjects (they never reach the
lookup). **The rule keys on a row EXISTING, not on its status:** a disabled user's row still admits (two such rows exist; the
applier's finding in its count file). ADDENDUM 3 says "active"; the build does what the addendum's CONTRACT sentence says
("holds no PROFILE row"). Stated so it is not mistaken for covered.

**It widens nothing.**

## 3. Who is refused after it: the count, and the read the CTO asked for

The count (`org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r7_ct1/INTERNAL_CALLERS_AND_PROFILE_ROWS_20261011.json`
@8d900213a1; its check re-run by this seat, `CT1-TOTALS-OK`): users table 86 items scanned of 86, 56 PROFILE items, equal to the
email index's count; 23 rows with firm `opal-capital`; 9 distinct non-service addresses among the actors of 27 tickets; **30
distinct internal addresses: 23 with exactly one row (21 active, 2 disabled), 0 with more than one, 7 with none**; 0 rows whose
stored address differs in case. **No person is among the seven.**

The seven, by digest (sha256 of the lower-cased address, first 12 hex; the addresses are in msgs 6172 and 6175, not in this
file). Columns 3 and 4 are this seat's reads at 00:0xZ: one native search of the working tree for the six local parts, and one
full scan of `opal-tickets` (27 of 27 items, no further page).

| digest | what it is by form | in the workspace (native Grep of the repo root for the local part; 8 files hit in all, 7 outside the applier's own log) | tickets, and the date of its last event | disposition by msg 6176 |
|---|---|---|---|---|
| `a4e31dfe3845` | a D7 battery identity | no file | 1; 2026-08-20 | refused, needs nothing |
| `2a0d25d244de` | a D7 battery identity | no file | 1; 2026-08-20 | refused, needs nothing |
| `f5b36a62648f` | a D7 re-pin identity | no file | 1; 2026-08-20 | refused, needs nothing |
| `0fc033e47dd5` | a D7 cleanup identity | no file | 1; 2026-08-20 | refused, needs nothing |
| `edb39e14ed26` | a D8 live-edit proof identity | 4 files, all records of 2026-08-20: a session log and two proof instances under `org/tier2_senior/0.4.0_DE_ClientPlatform/`, and the site Z CTO's acceptance record under `org/tier1_exec/1.0.0_SA_CTO/deliverables/`; no code | 2; 2026-08-20 | refused, needs nothing |
| `04d65641b5af` | a promotion-test identity | 3 files: two session logs dated 2026-08-20 under `org/tier2_senior/0.4.0_DT_ClientPlatform/`, one task order under `org/tier2_senior/0.5.0_AE_OpalETL/`; no code | 2; 2026-08-20 | refused, needs nothing |
| `d97166486cae` | this project's own synthetic filer | (not searched: the runner mints it) | 14; 2026-10-11 | refused by design (msg 6176: needs nothing); its row exists only for a run and the applier deleted it at 19:10:54Z under TO-RUN-R4-tr1 |

- **No code mints or uses any of the six.** Every hit is a dated record of 2026-08-20, on the site Z lanes of that day. The
  search is the native Grep over the working tree, which skips git-ignored files; the nested `portal` and `opal_ai` trees were
  inside its root. An identity minted by code on another box and never committed here is not visible to it.
- **Last events: all six on 2026-08-20, 52 days before this packet.** By msg 6176, "no code and no event in 30 days is refused
  and needs nothing". None is named to an owner; nothing waits.
- **Nothing scheduled calls the service as one of them, by two reads:** the function's resource policy has ONE statement, the
  API Gateway service with the portal API's source ARN (this seat, 2026-10-11 22:4xZ), so no schedule or rule can invoke it
  directly; and a caller through the gateway needs a portal sign-in, which reads the caller's users row, and none of the six has
  one. NOT read: the gateway's access log for these six addresses.
- **What neither read can see:** a caller in neither table (a constructed event; an identity that has never touched a ticket).
  After the release such a caller is refused, which is the point of the release.

## 4. Branches and rollback

| branch | what is written | rollback |
|---|---|---|
| apply succeeds; N2 and N4 refused, N3 served | the function code | none |
| apply succeeds; **N3 (a caller WITH a row) is refused** | the function code | **ROLL BACK AT ONCE**: re-apply the build of `b6fcebb514` (handler `b7764fbd...`), same method. That reading means callers with rows are locked out, which the release must not do. The rollback re-admits the no-row caller, as it is today |
| apply succeeds; N2 or N4 is SERVED | the function code | none taken; STOP and report: the release did not do what it says, and nothing is worse than before |
| apply fails partway | nothing else to land (code only) | as the second row; the ledger stays open until one holds |
| step 1 finds the live handler is NOT `b7764fbd...` | nothing: STOP before any plan | none |
| N1 (before) is NOT served | nothing: STOP before any plan. The "before" state is not what this pair says it is | none |
| the plan shows anything but 1 to change, any route or any env diff | nothing: STOP | none |

## 5. The act, its four invocations and its after-reads

Row TCKT_VNEXT-D2-S46 (ARMED, owner the CTO) is the instrument and is cited here by the CTO's word: a direct invoke goes around
the authorizer and the function believes the event's caller. Four invocations, all `GET`, all with a constructed context; no
token is made; no identity is minted and no grant is added; **no users row is written or deleted**.

0. Open the NEVER-2 ledger entry FIRST; every live worktree's `.open_deploys/` unioned with its denominator; an open entry
   naming `opal-ticket-api` other than this one is a STOP.
1. Before: the live package downloaded, the deployed handler's sha256 `b7764fbd...`; env key names and count (9) with a hash of
   each value; the ticket route census (11); `opal-tickets` ItemCount (27 at this seat's read, 00:0xZ); the control ticket's
   status and events length. The control ticket is `TCK-20261011-e6433610`.
2. **N1, BEFORE the apply:** a constructed INTERNAL caller, firm `opal-capital`, with a made-up address on `opal.invalid` that
   has no users row (the shape of round 6's arm A4), `GET` the control ticket. Expected **200**.
3. Build and upload; the zip's handler hashes `f99a314b...`. Plan, then `safe-apply`: exactly 1 to change.
4. After: CodeSha256 equals the zip; the deployed handler is `f99a314b...`; env unchanged (9 and 9); routes unchanged (11).
5. **N2, AFTER:** the N1 caller, the same `GET`. Expected **403**, body `{"error": "firm scope lookup failed"}`.
6. **N3, AFTER, the twin:** a constructed INTERNAL caller whose address ALREADY has exactly one PROFILE row with no firm list:
   digest `e95c05c7ae90` in the count file (a non-human `Dev` identity; its row is `disabled`, which the rule does not read; no
   person is impersonated). The same `GET`. Expected **200**.
7. **N4, AFTER:** the N1 caller, `GET` the list. Expected **403**, the same body.
8. The log group, the minutes of steps 5 to 7: the count of `FIRM-SCOPE-NO-ROW` lines (expected 2) and that none contains `@`.
9. ItemCount unchanged; the control ticket's status and events length unchanged. The replan is 0-diff.
10. `RESULT.json` holds, per arm, the function status, the refusal body's fields for a refusal, and for a served arm the KEY NAMES
    and `status` only. **A served answer's body is never persisted.** No address in any tracked file: the digest only.

## 6. What this pair does not show

- The firm fence between two internal callers WITH rows (a staff row listing firm B asking for firm A's ticket). Tests only, as
  the round-6 packet said.
- That a real signed-in staff member is served after the release. N3 is a constructed context for an address that has a row; it
  proves the lookup finds a row and admits. A staff member's own sign-in is the organic case and is not driven here.
- Row TCKT_VNEXT-D2-S48: the investor-reporting service's internal reader still leaves a no-row caller unrestricted. Not touched.

## 7. COO half

SIGNED, `2.0.0_SA_COO~V2`, 2026-10-12 ~00:1xZ, for exactly: the code of `09488abbb1` (handler `f99a314b...`) applied to
`opal-ticket-api` by `safe-apply` with a plan of 1 to change; four direct `GET` invocations N1 to N4 as section 5 names them;
the reads of steps 1, 4, 8 and 9; the rollback of section 4. Blast radius: the one function's code. Writers of that property:
ONE (the ticket-center Terraform root, applied by `0.7.0_AE_CloudOps~TV2` under this project's orders; N = 1). Both branches
of every expected outcome are in section 4. Nothing here reaches the vendor path, the users table's rows, or any other service.
