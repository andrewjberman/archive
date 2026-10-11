# Packet -- R2-pk-2 deploy: the package route stops handing the packager the ticket, and its refusals carry codes (TCKT_VNEXT round 2)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~08:0xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** CTO rulings msg 4349 ("one cell ... with its own never-widen pair (it narrows)") and msg 4363 (the 200 narrows too,
after a count of the route's callers); `2.0.0_SA_COO~G2` msg 4347; decomposition `decompositions/TCKT_VNEXT_DECOMP_R2.md` ADDENDUM 2,
cells `R2-pk-1` (built) and `R2-pk-2` (this apply). The drain: `R2-pk-1` merged @04f1f0cf93 and its AMENDMENT 1 @be67d1fd38. On the
merged tree this seat re-ran: `PK-CODES-OK 5 of 5`, `PK-200-OK 2 of 2`, `RR-SHAPE-OK 4 of 4`, `TC-REGRESS-OK passed=161`;
`commit-gate.sh` clean on the handler.

**COO half: SIGNED below.** Code only: no env, no route, no IAM, no grant. **ORDERED AFTER the R2-tr-1 run**: that run's precheck
pins the live ticket build `W03VREoM`, so no order for this apply is cut until run 3 has ended.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `be67d1fd38`; file sha256 `cf10e19e423b25b7b74ce43efd24e73b90a8a90850094697f3f79ec7145e6e74` (`sha256sum`, this seat) |
| the diff from the build it replaces | `git diff --numstat a366ce52ec be67d1fd38 -- <file>` reads 16 added / 7 removed, all inside `package_ticket` plus one helper (`_ident`) by the worker's report; **the hunks were not read line by line by this seat** |
| live now | `opal-ticket-api` CodeSha256 `W03VREoM...`, LastModified 2026-10-11T04:19:14Z; deployed file `ca3be343...` (the R2-rr-2 build, pin `a366ce52ec`; the applier's read in TO-APPLY-R2-rr2 and `reread_27.py` on 2026-10-11 06:1xZ) |
| plan expected | `0 to add, 1 to change, 0 to destroy` (the function's source_code_hash only) |
| the issuer's precheck instrument | `R1_RUN/reread_27.py` keeps a hand list of allowed ticket builds (row D2-S28). The applier's report of the deployed file hash is followed, same sitting, by the issuer adding `cf10e19e...` to that list on the same three reads as before, or the next run's precheck refuses |

## 2. Blast radius, by branch

**Behaviour that moves (read from the code and its tests at `be67d1fd38`):** ONE route, `POST /api/scoped/tickets/{ticketId}/package`,
callable by ONE principal (the type definition's `package_principal`; every other caller is denied before any of this).
- Each of its five 409s gains a `code` field; the sentences are unchanged.
- The already-attached 409 also returns `package`: the stored pointers plus `attached_at` and `attached_by`.
- The changed-under-write 409 NO LONGER returns `ticket`.
- The 200 returns `{"package": <the same identity object>}` and NO LONGER returns `ticket`.
Everything it removes is a ticket read handed to a service principal; nothing is added but codes and the packager's own pointers.

**Who calls the route (the worker's count, H1; denominator: portal `src`, `lib/`, `workflows/`, `infra/aws/lambda/` minus tests):
1 caller.** `infra/aws/lambda/investor-reporting/ycharts/research/opal_packager.py:269` (`attach`), invoked at `:183`
(`ports["attach"](ticket_id, payload)`), which DISCARDS the answer. This seat read `:176-184` itself. 0 portal callers.
- **The one way this apply can hurt:** a DEPLOYED packager that reads `ticket` from the 200 or from the changed-under-write 409
  would fail after it. The tree's packager reads neither. **Not measured: that the deployed packager is the tree's bytes.** The
  applier reads it (section 3, step 1b) before the plan; a difference in the `attach` call site is a STOP.
- The packager's handling of the new codes is IRPT_ANLREQ's cell AR-g-32, cut after this apply; until then the packager treats
  every 409 as it does today, because the status and the sentences are unchanged.

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code | re-apply the build of `a366ce52ec` (file `ca3be343...`), same method |
| apply fails partway | nothing else to land (code only) | as above; the ledger stays open until one holds |
| step 1 finds the live file is NOT `ca3be343...`, or the deployed packager's `attach` site differs from the tree | nothing: STOP before any plan | none; reported to the CTO |

## 3. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST; read every live worktree's `.open_deploys/`, union them, print the per-tree denominator; an
   open entry naming `opal-ticket-api` other than this one is a STOP.
1. Before the apply: (a) download the live `opal-ticket-api` package and show the deployed `lambda_function.py` sha256 is
   `ca3be343...`; (b) name the function that runs `opal_packager.py`, download its live package, and show the lines around the
   `/package` call discard the answer as the tree's do. Either read failing is a STOP.
2. Apply through `safe-apply` (Terraform only), plan read first: exactly 1 to change.
3. After: CodeSha256 equals the uploaded zip, and the deployed file is `cf10e19e...`.
4. An unauthenticated POST to the package route returns 401.
5. `opal-tickets` ItemCount unchanged; `TCK-20261009-a1052909` reads the same status fields as before (positive control).
6. The replan is 0-diff.

**The live arms (a 409 carrying its code; a 200 without `ticket`) need the service principal's token and are NOT exercised here.**
They are exercised by the packager's next real attach, or by AR-g-32's own pair. This pair mints no identity and writes no ticket.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above and all three branches, on the ordering condition (after R2-tr-1's
run 3 has ended).

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
