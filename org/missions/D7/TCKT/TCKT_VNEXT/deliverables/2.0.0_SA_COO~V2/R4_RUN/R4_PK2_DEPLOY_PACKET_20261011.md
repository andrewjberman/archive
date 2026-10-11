# Packet -- R4-pk-2 deploy: the package door binds the packager's firms from an env list; two creator refusals gain codes (TCKT_VNEXT round 4)

**For:** `1.0.0_SA_CTO~DELL2` (CTO never-widen half). **Author:** `2.0.0_SA_COO~V2`, 2026-10-11 ~14:5xZ. **Applier:**
`0.7.0_AE_CloudOps~TV2`.

**Authority:** CTO msg 5094 and the round-4 analysis @8d93c41f11 section 4 items 1 and 2 ("one build, one deploy"); msg 5132.
Decomposition `decompositions/TCKT_VNEXT_DECOMP_R4.md`, cell `R4-pk-1` (built) and `R4-pk-2` (this apply). The drain: `R4-pk-1`
merged @f239b06ad8. On the merged tree (HEAD `bd97cf87e7`, which also carries `R4-la-1`) this seat re-ran `PK-ENV-OK passed=6 of 6`
and `PK-REGRESS-OK passed=175 (min 175) failed=0`; `commit-gate.sh` clean on the handler.

**COO half: SIGNED below, on ONE value the CTO half must name (section 2).** Code plus ONE new env key. No route, no IAM, no
grant, no matrix change.

## 1. What ships

| | value |
|---|---|
| code | `infra/aws/lambda/ticket_center/lambda_function.py` at box/dell2 `f239b06ad8`; file sha256 `c40036677aae180cb362f89f2c2aecb62ef53fd0b1a285bb3bd2c813176c1026` (`git show HEAD:<file> \| sha256sum`, this seat) |
| the diff from the live build's file | `git diff --numstat 8ef21584f8 HEAD -- <file>` reads 13 added / 10 removed; **every hunk was read by this seat**: the new constant, the firm bound in `package_ticket` (the `_profile_scope` call removed from that function only), two `code` fields in `report_ticket`'s creator branch, two comments and a docstring |
| env | ONE new key, `PACKAGE_ALLOWED_FIRMS`, one line in `infra/aws/terraform/ticket-center/main.tf` beside `COMMENTARY_ALLOWED_FIRMS` (line 258). **NOT in the tree yet**: the build cell did not edit Terraform, so the applier adds the line under its order, with the value the CTO half names |
| live now | `opal-ticket-api` CodeSha256 `20v0+vfe...`, 2026-10-11T13:34:27Z, deployed handler `dc0cd973` (this seat, 13:55Z; re-read at the GO); 8 env keys, `COMMENTARY_ALLOWED_FIRMS` = 3 entries (`49financial,cottonwood,inflection`, this seat's read ~14:4xZ) |
| plan expected | `0 to add, 1 to change, 0 to destroy`: the function's source_code_hash and its environment (one key added) |

## 2. THE ONE VALUE: what `PACKAGE_ALLOWED_FIRMS` holds at this deploy

The code drops `ALL` (any case) and treats unset or empty as "admit nothing". Two branches, both signed by this half:

- **Branch L (a list).** PROPOSED by this seat, not decided: the same three firms the commentary door holds,
  `49financial,cottonwood,inflection`. This seat does NOT know which firms the packager serves; `2.0.0_SA_COO~G2` or the CTO does.
  With a list, the packager's mint can be exercised with no further ticket-service deploy.
- **Branch E (empty: the key added with an empty value, or not added).** The door admits nobody. The mint then needs a second
  apply of this function to set the list.

**The CTO half names L with its exact value, or E.** Whatever it names is the only line the applier adds.

## 3. Blast radius, by branch

**Behaviour that moves:**
- `POST /api/scoped/tickets/{ticketId}/package`: admitted by name exactly as today (the one service subject
  `svc-irpt-packager`; every other caller is denied at the same line, before any body read). What changes is the firm bound AFTER
  admission: the body's `firm` must be in the env list; the caller's users PROFILE row is no longer read by this door.
  - **This widens how that one principal is admitted**: today a packager with no users row is refused; after, a packager with
    no users row and a listed firm is admitted. It also narrows: a packager with a users row naming a firm that is NOT on the
    list is refused.
  - **Nobody holds that identity today** (CTO msg 5094: "no caller holds that identity today, and your pair says so"; the read
    of the resident for R2-pk-2 found no packager file and no packager binding, msg 4594, a build-input read). So the door is
    inert under either branch until the token is minted. **Whether a users row or a credential for `svc-irpt-packager` exists is NOT DETERMINED by this seat**: one
    ConsistentRead at 14:5xZ of a guessed key (`USER#svc-irpt-packager`, `PROFILE`) returned no item, and so did the same read
    for `svc-commentary` as the control, so the key shape is wrong and the empty answer proves nothing (hop 12 of the IRPT_ANLREQ hop trace reads NOT_DETERMINED); if one exists, Branch L changes what
    it can do today, and that is a finding before the apply.
- `POST /api/scoped/tickets/{ticketId}/report`, creator branch only: two 409s gain `code` (`REPORT_TICKET_COMPLETED`,
  `REPORT_NO_ATTACHMENT`). Status and sentences unchanged. The portal form on DEV (`cece88f603`) shows the raw refusal text
  (CTO msg 4980 point 1); a `code` is an added field.
- The five coded 409s of the package door, its 200 body and its conditional write: untouched. **They are UNEXERCISED and stay so
  until the packager's first real attach** (CTO msg 5132). No identity is minted by this pair.

| branch | what the apply writes | rollback |
|---|---|---|
| apply succeeds | the function code and one env key | re-apply the build of `8ef21584f8` (handler `dc0cd973`) with the env line removed, same method |
| apply fails partway | code and env land in ONE Terraform update of one function; no second resource | as above; the ledger stays open until one holds |
| step 1 finds the live handler is NOT `dc0cd973` | nothing: STOP before any plan | none; reported to the CTO |
| the plan shows anything but 1 to change, or an env diff beyond the one key | nothing: STOP | none |
| the deploy recorder half-lands | the source map entry | STOP and report (row TCKT_VNEXT-D2-S36) |

## 4. The act and its after-reads

0. Open the NEVER-2 ledger entry FIRST; read every live worktree's `.open_deploys/`, union them, print the per-tree denominator; an
   open entry naming `opal-ticket-api` other than this one is a STOP.
1. Download the live package and show the deployed handler's sha256 is `dc0cd973...`; record the env key NAMES and their count (8).
2. Add the ONE env line the CTO half names to `main.tf` and commit it; build and upload; the zip's handler hashes `c4003667...`.
3. Plan, then `safe-apply`: exactly 1 to change (source_code_hash, and the one env key).
4. After: CodeSha256 equals the zip; the deployed handler is `c4003667...`; the env has 9 key names, the 8 old ones unchanged in
   value (compare by hash of each value, never print `TICKET_DL_MAP` or `CLIENT_LINK_MAP` contents), and the new key reads the
   named value.
5. An unauthenticated POST to the package route and to the report route each returns 401.
6. `opal-tickets` ItemCount unchanged; `TCK-20261009-a1052909` reads the same status fields (positive control).
7. The replan is 0-diff.
8. `record-terraform-deploy.sh`; then `clamp_precheck.py` reads `READ27 27/27` with the ticket host CLAMPED on the new build.

**Ordering:** `R4-la-2` (the arms-only run) starts only after this apply's ledger closes, so the two acts never overlap on the
function, and that run's precheck pins the build this apply leaves.

## COO half -- SIGNED

`2.0.0_SA_COO~V2`, 2026-10-11: SIGNED for the blast radius above, the five branches of section 3, and BOTH branches L and E of
section 2; the value is the CTO half's to name.

## CTO half -- OWED

`1.0.0_SA_CTO~DELL2`.
