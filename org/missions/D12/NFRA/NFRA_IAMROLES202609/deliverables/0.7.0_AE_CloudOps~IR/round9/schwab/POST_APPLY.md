# IAM-z-2 PHASE B -- POST-APPLY: the delete landed and is verified; the `verified` line is WITHHELD pending a real run

**Seat:** `0.7.0_AE_CloudOps~IR` - **Order:** `NFRA_IAMROLES202609.TO-IAM-z-2` - **Risk:** WORLD
**Pair:** `NEVER_WIDEN_ROUND9_Z-2_COO_HALF.md` @`4afde83a62` + `..._CTO_HALF.md` @`c790b17440`
**GO:** msg 33453. **NEVER-2 entry:** `iamroles-r9-narrow-schwab`, opened 04:27Z -- **STILL OPEN** by design.
**Delete floor (recorded before the call):** `2026-10-12T04:29:20Z`; the call completed `04:29:22Z`.

> **The `POST-APPLY: schwab: verified` line is deliberately NOT written yet.** The cell makes that token
> the grade, and both halves plus the GO make branch A conditional on *"ONE real bd run on this role that
> STARTS AFTER the delete and completes successfully"*, with the GO adding: *"If none fires in your
> window, keep the entry open and say so; never substitute a simulation."* Half of that condition is met
> and half is not (section 3). Writing the token now would be exactly the substitution the pair forbids,
> so the entry stays open and this record says why.

---

## 1. BASELINE RE-READ -- ALL FOUR, the pair's stop condition

| # | value | result |
|---|---|---|
| 1 | live `schwab-bucket-access` vs `ROLLBACK_schwab-bucket-access.json` | canonically **EQUAL** (1 statement, 2 ARNs) |
| 2 | `list-role-policies` | **17** |
| 3 | `opal-data-schwab` | **`NoSuchBucket`** |
| 4 | act (a): `grep -c 'Bucket=SRC_BUCKET' build_canonical_daily.py` at HEAD | **0** |

**All four MATCHED, so the act was signed.**

## 2. THE DELETE -- LANDED AND VERIFIED

`aws iam delete-role-policy --role-name bd-exporter-ec2-role --policy-name schwab-bucket-access` -> rc=0.

| check | result |
|---|---|
| policy-name set, read back as a **difference** not a count | **17 -> 16**; `REMOVED: ['schwab-bucket-access']`; `ADDED: []` |
| `get-role-policy` on the deleted policy | **rc=254 `NoSuchEntity`** -- here the error IS the pass |
| positive control, same call shape on a policy that must survive | `s3-access` -> **rc=0** |
| the role itself | `bd-exporter-ec2-role`, `CreateDate 2026-01-09T00:41:34Z` unchanged; **2** attached managed policies unchanged |
| the other 16 inline policies | untouched -- the set difference is the proof, since it names what left rather than counting what remains |

Reading the policy list as a **set difference** is what makes this airtight: a count of 16 would also be
true if one policy had been deleted and a different one added. `REMOVED` names exactly the signed policy
and `ADDED` is empty.

## 3. WHY THE RUN LEG IS STILL OPEN

The pair wants two things, and they are not the same thing:

| requirement | status |
|---|---|
| `RoleLastUsed` advances past the delete time | **MET** -- `2026-10-12T04:31:26Z`, past the `04:29:22Z` floor (it read `04:24:31Z` immediately after the delete and advanced two minutes later) |
| the run's own **completion record** shows success | **NOT MET** |

Measured server-side, counting objects written after the floor `2026-10-12T04:29:22+00:00`:

```
gold/.checkpoints/2026-10-12/  -> 0 objects after the floor
gold/meta/                     -> 0
gold/canonical/watermarks.json -> 0
silver/                        -> 0
```

**So the role was USED after the delete but no run COMPLETED after it.** Today's gold chain ran
**04:03:55Z -> 04:16:46Z** (`A_02.done` through `B_00.done`, `watermarks.json` 04:16:44Z) -- entirely
**before** the delete, so it cannot grade this act. The 04:31:26Z use is the persistent instance's own
routine API activity: `i-01003b035d2988dfb` (`bd-gold-layer-runner`) is the **1 running** of the role's
**14** instances and stays up between runs, so it touches the role continuously without that being a run.

**That distinction is the finding.** `RoleLastUsed` answers *"did anything use this role"*, never *"did a
job complete"*. On a persistent instance those come apart completely, and a grader handed only
`RoleLastUsed 04:31:26Z > 04:29:22Z` would reasonably have called branch A satisfied. It is not.

**When the next qualifying run fires:** the daily gold chain is `cron(0 4 * * ? *)`
(`bd-canonical-prices-daily` -> `bd-gold-trigger`, `eventbridge.tf:384`), which already ran today, so the
next one is **2026-10-13 ~04:00Z**, about 23 hours out. The evening `MON-FRI` bd rules
(21:38 / 21:45 / 22:00 / 22:10 / 22:20 / 22:30 / 22:40Z) target **Lambdas**, not this EC2 role, so they do
not qualify either; I checked the two nearest candidates and both resolve to `module.*.function_arn`
(`bd-49f-keepalive` at `rate(15 minutes)`, and `bd_49f_session_trigger` at `cron(35 4)`).

**I did not dispatch a run.** The EC2 manifest's `_access_policy` for this instance is explicit:
*"EVENTBRIDGE ONLY. No agent, no human, no SSM command may start, stop, or run commands on this
instance."* Starting one to manufacture a grade would have broken that, and an ad-hoc artifact is not
production evidence in any case.

## 4. WHY BRANCH A IS STILL THE EXPECTED OUTCOME

No scheduled producer names the dead bucket. Of its 3 used call paths (survey section 4, row `Z-S52`):
`convert_schwab_uln_to_silver.py` is self-declared `*** DEPRECATED -- DO NOT USE ***`,
`rps_ingestion.py` has **0** references in the owning skill, and `sync_schwab_onedrive_to_s3.py` **is**
the skill's "Retired Step 1 (do not run)". The gold chain that ran at 04:03Z did so while the grant still
existed and did not touch `opal-data-schwab`; after the delete it has nothing to lose.

If the 2026-10-13 04:00Z chain completes normally, branch A closes. If it fails with `AccessDenied` on
`opal-data-schwab`, branch B applies: restore with
`put-role-policy --policy-name schwab-bucket-access --policy-document file://ROLLBACK_schwab-bucket-access.json`
(the rollback is in restorable document shape -- it was one of the two this round found wrapped and
re-captured), then file a row naming the run and the call path.

## 4a. A BRANCH-B SHORTCUT I TRIED, AND WHY ITS ZERO MEANS NOTHING

Rather than wait ~22h, I tried to watch branch B directly: look for `AccessDenied` on `opal-data-schwab`
in CloudTrail since the delete floor. It returned **0**, and that zero is **uninformative** -- recorded
here so no one reads it as "branch A confirmed", and so no one repeats the attempt.

```
cloudtrail lookup-events --start-time 2026-10-12T04:29:00Z (EventSource s3.amazonaws.com, 50-item page)
  events parsed: 38      with an errorCode: 0
  naming opal-data-schwab: 0      from bd-exporter-ec2-role: 0
  distinct eventNames in the page: ['GetBucketAcl', 'GetBucketVersioning']
  page window: 2026-10-12T04:51:35Z .. 06:00:26Z
```

The two event names were the tell -- 90 minutes of S3 activity on this estate and not one object-level
call -- so I checked the instrument's coverage instead of accepting the zero:

```
describe-trails -> opal-organization-trail (multi-region), opal-served-key-write-trail
get-event-selectors opal-organization-trail:
  { ReadWriteType: All,      IncludeManagementEvents: true,  DataResources: [] }
  { ReadWriteType: ReadOnly, IncludeManagementEvents: false, DataResources: [
      AWS::S3::Object -> arn:aws:s3:::opal-data-49financial/ , opal-data-bd/ , opal-data-cot/ , opal-data-inf/ ] }
```

**`opal-data-schwab` is not among the four prefixes with S3 data events, and the selector is `ReadOnly`
anyway.** So CloudTrail **structurally cannot** record a `GetObject` / `ListObjectsV2` / `PutObject`
against that bucket by any principal: the plane cannot produce a hit, so its zero is not a measurement of
the world. This is ABSENT, not EXERCISED-AGAINST -- a failure mode indistinguishable from a genuine
negative, which is exactly the thing a coverage denominator exists to expose.

**Two consequences.** (1) The pair chose the right oracle: the run's own completion record is the only
sound one available, and the shortcut I reached for has no coverage. (2) Nothing here is evidence that
nothing broke -- it is the absence of contrary evidence from an instrument that could not have supplied
any. The grade still waits on the 2026-10-13 ~04:00Z gold chain.

## 5. STATE

| leg | status |
|---|---|
| `delete` [activation] | **CLOSED** -- proven in section 2 |
| `realrun` [verify] | **OPEN** -- awaiting the 2026-10-13 ~04:00Z gold chain |

The NEVER-2 entry `iamroles-r9-narrow-schwab` is therefore **OPEN**, and a reader should take it as
exactly that: a world act that landed and is verified at the document level, with its consumer-level
grade still owed. **This is not a half-landed deploy** -- there is nothing further to apply, nothing
staged, and no rollback pending -- it is a completed change whose acceptance evidence arrives on someone
else's schedule, which is the one case NEVER-2's "finish in-session" cannot cover. Step 3 (the `SKILL.md`
correction) landed in PHASE A @`fd151c1946` and is not part of this act.
