# NFRA_OUTSET.TO-OS-s-19 -- THE DEPLOY: result

**Assignee:** `0.7.0_AE_CloudOps~W` · **Issuer:** `2.0.0_SA_COO` · **Issuance:** `37b2a19129`
**Face vintage:** `cb43d05200` (AMENDED, remedy (c) on row `NFRA_OUTSET-S18`)
**Worked:** 2026-09-09 13:45Z -> 14:10Z (main tree, `CLOUD`) · **Order status: `complete`**

---

## THE ONE-PARAGRAPH ANSWER

**The estate now reads the runner at HEAD.** It had been serving a 2026-08-25 artifact through round
1 and everything since: 17 task orders passed, and the file the box actually pulls never moved. One
`s3api put-object` closed it, inside a change-management entry opened first and closed after, with
the verdict resting on a **content diff** rather than a timestamp. Served and HEAD are now
byte-identical at sha256 `88096c625bf70c3f`, and the comparator was proven able to fail before its
match was believed.

**What this does NOT do:** the seam still will not be read on the next fire, because
`ESTATE_OUTSET_SEAM_PREFIX` is set nowhere in Terraform (`NFRA_OUTSET-S16`). This order closes the
gap between HEAD and the served artifact. It does not turn the seam on, and no criterion here claims
it does.

---

## O19-AC1 -- MECHANICAL. **PASS.**

**Invocation, exactly as the AMENDED face names it:**
`timeout 300 python org/missions/D11/NFRA/NFRA_OUTSET/deliverables/0.7.0_AE_CloudOps~W/test_os19_served_matches_head.py`
**Expect:** `SERVED MATCHES HEAD` · **Observed:** `SERVED MATCHES HEAD`, rc **0**, captured unpiped.
**Second grain:** `pytest -q` -> `1 passed`. **Determinism:** two same-input repeats, verdict sets
identical.

**DENOMINATOR: 6 of 6 evaluated arms PASSED, 0 NOT-EVALUATED.**

| Arm | Result |
|---|---|
| A `head-object` vintage + ETag | 159,687 == 159,687; ETag `e75c59a35457535ca0d339c9f59589f5` == HEAD md5; LastModified 2026-09-09T13:53:22Z |
| **B CONTENT diff (the verdict)** | served sha256 `88096c625bf70c3f` == HEAD `88096c625bf70c3f`, 159,687 B both |
| C **negative control** | one bit flipped at offset 100 of a copy, length unchanged -> the same comparator reports MISMATCH |
| D token census, per-token control | 5 LIVE tokens agree; 1 INERT token refused as evidence |
| E same-program positive control | `_stratum(` 16 on both sides |
| F worktree == HEAD | identical sha256, 0 CRLF on both |

**Why B and not A.** Rule 22a's CODE trap: deployed bytes are diffed against the BUILD INPUT, never
by filename, and running-bytes-older-than-built passes every other rung. `head-object` says *when*
something was written and nothing about *what*. So the vintage is read and recorded, and the verdict
rests on a sha256 of the downloaded object against `git show HEAD:<path>`.

**Why C exists.** A comparison that cannot fail is not a comparison. Arm B compares two things that
should be equal, so on its own its pass is unattributable -- it would read identically if the
comparator were a constant. C mutates one bit of a copy, holds the length fixed so the check cannot
succeed on size alone, and proves the same comparator reports a mismatch.

**Arm D, and the row it was built from.** `W1-S27`: every token in a presence/absence census needs
its OWN positive control, because a census of four tokens is four detectors, not one. Row `S14`
measured the cost -- `W1-S25` cited `rerun_recipe` and `tool_invocation` as evidence, and both are
zero at HEAD too, so their zeros measured that row's spelling rather than the world. So D computes
each token's HEAD count FIRST and refuses any token absent there:

- **LIVE (5):** `_outset_read` 4, `OUTSET_ANSWER_STATE_TO_STATUS` 3, `ESTATE_OUTSET_SEAM_PREFIX` 5,
  `_outset_trace` 3, `render_trace` 2 -- each now equal in the served bytes, and **every one of them
  was 0 in the served object before this deploy.**
- **INERT (1):** `rerun_recipe`, carried deliberately as a sealed control. The arm asserts it is
  classified INERT and excluded, so the battery is tested for the very failure `S14` recorded.

## O19-AC2 -- JUDGMENT. THE LEDGER AND THE WINDOW. Recorded, NO VERDICT.

`3.0.0_SA_CVO` grades this at L9.

**The entry:** `org/critical_paths/change_management/20260909T1352Z_estate-report-runner-outset-seam-consumer_deploy_completion.md`.
**Opened 13:52Z and COMMITTED IN THE OPEN STATE at `6dbb1e6a3a`, before the upload** -- so "opened
first" is a fact in git history rather than a claim in prose. An entry written and closed in one
commit records both facts at the same instant and proves neither ordering. Closed 13:56Z after all
four legs verified.

**Every consumer of the key, censused rather than recalled.** `comp-find 'code/estate_report_runner\.py'`
-> **154 hits across 152,096 files scanned**, banded HEAD 3 / SURFACED 41 / CONFIG 32 / TEST 2 /
DOC 76. Exactly **one** functional consumer: `estate-report.service` on `i-0512bd3cbaf602b7f`, whose
`ExecStartPre` (`instance.tf:215`) pulls the key at every service start. The negative half was
checked so the count means something: `estate-report-orchestrator` carries one environment variable,
`ESTATE_INSTANCE_ID`, and never reads the code key. Everything else is documentation, audit logs,
message archives or this session's scratch copies. **One task family, no shared tag**, so the
NFRA_CLDGRPH-S31 hazard of one image act re-pointing several families does not arise.

**The window, plainly.** `estate-report-0900et` is ENABLED, `cron(0 9 * * ? *)` `America/New_York`.
Today's run launched 13:00:45Z and self-stopped 13:11:04Z. The upload ran at 13:53:20Z with the
instance state read as `stopped` immediately before the call. **It landed OUTSIDE the window, and
outside it in the safe direction:** today's `ExecStartPre` pull already happened at ~13:00:50Z and
could not be affected even in principle, and the next pull is about 21 hours away, so no run was
mid-flight against a changing key. Next fire **2026-09-10 13:00Z**.

**What I measured before acting on any open or red entry.** `.open_deploys/` holds 6 named entries
-- 4 OPEN (ADVI_INSURE x2, NFRA_OPSEC x2), 2 HELD-SOVEREIGN-GATED (D12 SMS, FRESHGUARD). A scoped
census of that directory returns 4 hits across 7 files and **all four sit inside
`.unindexed_red_state.json`**, a path-to-timestamp index rather than an open deploy. **Denominator
6 of 6 read; zero name this key.** The four index rows point at two ledgers both opened AND closed
on 2026-08-05, and two of the rows carry the **other device's** path prefix
(`C:\Users\Opal Bloomberg\...`) -- exactly the "an entry a device left open proves only that THAT
device saw no completion" shape. The artifact settled it rather than the entry: the served object's
vintage was 2026-08-25, three weeks later than both ledgers, so neither was an unfinished promote of
this key. **Nothing was half-landed and nothing here was a rewind.**

**The bytes uploaded were `git show HEAD:<path>`, not the worktree copy**, and the two were compared
rather than assumed equal -- a worktree hash on this autocrlf box hashes the checkout, not the
record. Measured identical here (arm F), so the distinction cost nothing today. Recorded because the
next file may differ.

**Rollback, recorded before the act rather than reconstructed under pressure:** S3 versioning is on;
the prior object is `VersionId bvnr1MynPuJ8Asn3u6Tgo9LPd5CrL5OO` (125,857 B, 2026-08-25T05:36:35Z),
restorable with a single `copy-object` from that version, in session, with no Terraform involvement.

## WHAT I DID NOT DO

- **No watcher, monitor, alarm or freshness checker** against the fire. Standing moratorium, and the
  scheduled fire is the acceptance rather than an ad-hoc run.
- **Did not start the instance** to force an early exercise. The face's own acceptance is the
  scheduled fire; an ad-hoc run would consume the discriminator it exists to produce.
- **Did not set `ESTATE_OUTSET_SEAM_PREFIX`** or build a publish cadence. `NFRA_OUTSET-S16` and
  `-S17`, both still ARMED and routed by the issuer to `1.0.0_SA_CTO`.
- **Did not push.** `git push` is refused under this order's BOUNDS.
