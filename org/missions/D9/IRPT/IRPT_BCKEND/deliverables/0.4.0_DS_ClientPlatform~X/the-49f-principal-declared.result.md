# IB-rtc-6 -- THE 49 FINANCIAL PRINCIPAL, DECLARED, PLANNED, AND THE SIGN-OFF PACKET: result

**TO:** `IRPT_BCKEND.TO-IB-rtc-6` | **serial:** `0.4.0_DS_ClientPlatform~X` |
**branch:** `wk-irpt_bckend-3-ds3` | **worktree:** `/c/tmp/wk-irpt-3-ds3` | **cut:** `7b2f8fe9bf`
**Invocation:** `timeout 900 py -3.12 org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.4.0_DS_ClientPlatform~X/battery_ib_rtc_6.py`
**Ruling executed:** R-44 @57bc083d45, up to the signature and no further.

**Nothing was applied, minted or granted.** The live plane is unchanged: the role does not exist
(`NoSuchEntity`), the host policy is the 32-statement document captured in
`IB-rtc-6_host_policy_before.json`, and the Lambda's environment has its 4 keys.

---

## What is declared (commits `04b6d95f61` runner half, `8d18193bcc` Terraform + dispatch half)

- **The role** `irpt-49f-directory-read-role` (builder output), in the directory root's new
  `principal_49f.tf`. Its trust is exactly one principal, `mdpf-daily-runner-ec2-role`, derived from the
  EC2 manifest.
- **Its policy** `irpt-49f-directory-read-policy`: `s3:GetObject` on the 5 dimension tables, and one
  `s3:ListBucket` conditioned to those 5 prefixes. No write and no other bucket.
- **The host role** gains one statement: `sts:AssumeRole` on that role.
- **The refresh Lambda** gains one env key: `IRPT_DIRECTORY_SOURCE_ROLE_MAP`.
- **`refresh.py`** hands the ARN to the 49 Financial build only.
- **`directory_runner.py`**: `Firm49F` reads its five tables through the assumed session, and the xref
  stays on the host session.

The packet (`NEVER_WIDEN_SIGNOFF_PACKET_IB-rtc-6.md`) sets out each key's statements, blast radius and
rollback.

## The six graded arms

| arm | deciding line | denominator |
|---|---|---|
| (a) NAME | `name("irpt", "49financial", "directory-read", "role") = irpt-49f-directory-read-role`; old denied prefixes matched `0 of 4`; the LIVE fence admits it: `True` | 4 old prefixes; 17 fence patterns |
| (b) DECLARATION | 5 GetObject prefixes; 1 ListBucket over 5 prefixes; 1 trust principal; host statements added 1, removed 0; other buckets 0; write actions 0; the plan TEXT agrees with the extract | read from 2 artifacts that must agree |
| (c) RUNNER | 8 passed, 0 failed; 49F through the ASSUMED session `1 of 1`; INF/COT through the HOST session `2 of 2` | 8 test arms |
| (d) WRITERS | `WRITERS: 12 of 262`; UNKNOWN 0; unsimulated 0; the new principal among them `0` (`implicitDeny`) | 262 principals (255 roles, 7 users) |
| (e) PLANS | directory `2 to add, 1 to change, 0 to destroy`; mdpf-pipeline `0 to add, 2 to change, 0 to destroy`; both text sha256 printed in the packet | 2 roots |
| (f) PACKET | keys `5 of 5` with a rollback; negative-control rows `6 of 6` | 5 keys, 6 controls |

## Things that changed the work, each on the record

1. **The fence moved** (row `S66`). `opal-data-49financial` no longer denies four named prefixes. LGIC
   EN-f-1 replaced that with `ArnNotLike [role/*-49f-*, exemptions]`. The name clears the old list
   (0 of 4) and, what matters now, carries the `49f` scope slot the fence admits. The host role is still
   denied, which is why it can't read the tables itself.
2. **The naming gate refused the typed legacy address** (row `S67`). `gold/advi/dimensions` in a new file
   is NEW and OUT-OF-PATTERN. The declaration now derives the root from the producer's own
   `runner_common.OUT_ROOT`, the constant the runner reads, citing that file by its repo path. The gate
   then passes, and the grant, the writer and the reader share one authority.
3. **The lane gate refused the four `infra/aws` paths** (lane CLOUD_OPS_OR_ETL), the same gap as row
   `S64`. The order's `<paths>` grants them. They landed in one commit under the audited
   `GIT_COMMIT_AUTHOR_OVERRIDE=CLOUD_OPS_OR_ETL`; the runner half landed separately on the seat's own lane.
4. **The plan would have hidden the one env key** by printing the whole Lambda environment as "known
   after apply". The ARN is now built at plan time, and the plan shows exactly `+
   IRPT_DIRECTORY_SOURCE_ROLE_MAP` with 4 unchanged.
5. **mdpf-pipeline carries an unrelated pending change** (row `S68`, ARMED): `route_bindings.yaml`'s
   deployed hash matches neither the blob nor this box's CRLF copy. The packet prescribes a TARGETED
   apply for K3.
6. **IB-rtc-3 had not merged when this started** (row `S69`). This cell's `refresh.py` edit keeps to
   `dispatch()` and a new env reader.
   - **Trial merge** with `wk-irpt_bckend-3-2 @3ce04d8a52`: `git merge-tree` is clean.
   - **Merged tree tests**, on a throwaway commit object: runner tests 62 pass, directory tests 41 pass
     (IB-rtc-3's 4 new ones included).
7. **Once merged, any apply of these roots performs the act unsigned** (row `S65`, ARMED, owner
   `2.0.0_SA_COO~B`). The directory root is the refresh Lambda's deploy root.

Regression: runner tests 54 at the base and 62 at the tip (the 8 new, all passing). `refresh.py`'s own
tests pass 37 of 37 at both.

## R36-AC2 -- facts for `3.0.0_SA_CVO` (no verdict)

- **How narrow the trust is.** The trust names ONE principal ARN, the host role, and no service,
  wildcard or account root. The host's instance profile is attached to exactly one instance
  (`i-02448edb624a7a7cf`, measured). But every process on that host runs as the host role, so every
  process there (the mdpf daily chain, the accrual bridge's runs, the IRPT builds) could assume the
  principal, not only the directory build. Two narrower forms exist and are NOT declared here, because
  neither is in the root's idiom:
  - an `ec2:SourceInstanceARN` condition, which binds to the instance rather than the role;
  - an `sts:RoleSessionName` or `sts:SourceIdentity` condition, which the dispatch would then have to
    set, and which any code on the host could also set.
- **Does reading through the assumed role change what the runner writes?** No. Measured: the runner's
  write path (`land()`, its `put_object` calls, `_assert_destination`) has 0 changed lines. The writes
  use the process's default session, which is still the host role, and the destination bound is
  unchanged. The assumed session exists only inside `Firm49F._gold()`, for the five reads; the test
  shows the xref read stays on the host session.
- **Where the 49 Financial directory lands.** The destination comes from `data/firm_registry.json`:
  `49financial -> opal-data-bd`, a bucket it SHARES with the `mockadv` test tenant (key-prefix
  separation). The LGIC registry's `scope_bucket` for 49financial is `opal-data-49financial`, where the
  source tables live. So until D14 / ADVI_FIRMBKTS moves the destination, the two registries disagree
  about which bucket is "the firm's own". FWD-7's DONE WHEN (PRD B4: "in the FIRM's own bucket under
  `investor-reporting/directory/`") is met by the firm registry's reading, and not by the LGIC
  registry's. The census shows 12 principals can write that destination prefix today, 8 of them `bd-*`
  pipeline roles.

## Rows filed (5)

| id | class | standing | one line |
|---|---|---|---|
| `IRPT_BCKEND-S65` | OBSERVATION | ARMED (`2.0.0_SA_COO~B`) | once merged, any apply of these roots creates the principal without the sign-off |
| `IRPT_BCKEND-S66` | OBSERVATION | INERT | the face's name check names the old deny list; the live fence admits by scope slot |
| `IRPT_BCKEND-S67` | OBSERVATION | INERT | the naming gate refused the typed legacy address; derived from the producer's `OUT_ROOT` |
| `IRPT_BCKEND-S68` | OBSERVATION | ARMED (`2.0.0_SA_COO~B`) | an untargeted mdpf-pipeline apply would push an unrelated, CRLF-rendered config object |
| `IRPT_BCKEND-S69` | OBSERVATION | INERT | IB-rtc-3 had not merged; the `refresh.py` overlap is kept to `dispatch()` and merges cleanly |
