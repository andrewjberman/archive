# WS-C7 SPECIMEN 2 -- rc=0 ON ZERO WORK, and the DENOMINATOR-BEFORE-THE-OPERATION control

**Captured:** 2026-07-31 by `0.7.0_AE_CloudOps~Z` (site Z)
**Scope authority:** `1.0.0_SA_CTO~Z` ruling `20260731T030549Z` -- WS-C7 specimen capture and
fixture authoring. **This fixture CAPTURES; it does not set the WS-C7 contract** (P2, CTO-owned).
**Observed:** 2026-07-31T~00:4xZ, querying the MCP audit lake.
**Status:** NOT FIXED, and deliberately so -- see "Why this one is not repaired". Live and
reproducible today.

---

## THESIS

> **The tool reported what it found. It had no channel for what it could not have found -- and it
> exited 0.**

`aws s3 sync` returned **RC=0 having downloaded 0 of 55,878 objects.** Under `--quiet`, the entire
event is: a clean exit code and an empty directory.

---

## OBSERVATION

```
aws s3 ls s3://opal-mcp-audit/audit/ --recursive --summarize
  -> Total Objects: 55878
     Total Size:    16802615

aws s3 sync s3://opal-mcp-audit/audit/ "$DEST" --quiet
  -> SYNC_RC=0
     files pulled: 0
```

**Cause:** the S3 keys embed ISO timestamps containing colons --
`audit/dt=2026-07-30/2026-07-30T02:08:35.459103+00:00-01b04ff7.jsonl`. **`:` is illegal in a Windows
filename.** Every single download failed:

```
download failed: s3://opal-mcp-audit/audit/dt=2026-07-30/2026-07-30T02:08:35.988538+00:00-...jsonl
  [Errno 22] Invalid argument: 'C:\...\2026-07-30T02:08:35.988538+00:00-...jsonl.911c9686'
```

**...and the command still exited 0.** Re-run without `--quiet` and the per-object failures print;
the exit code does not change. The `--quiet` flag does not suppress a *summary* of failures, because
no such summary is ever produced.

---

## FAILURE DIRECTION

**UNDER-REPORT.** Single limb, unambiguous. The instrument reported a true statement about what it
retrieved (nothing) and made no statement at all about the 55,878 objects it did not retrieve. The
denominator is absent from the output, so the result is unfalsifiable from the result alone.

**This is the WS-C7 standard's exact shape:** every tool reports what it FOUND; none reports what it
COULD NOT HAVE FOUND. Here the tool found nothing, said so accurately, and was catastrophically
misleading.

---

## THE CONTROL THAT CAUGHT IT -- capture the CONTROL, not the incident

**THE DENOMINATOR WAS TAKEN BEFORE THE OPERATION.**

The failure was caught only because `--summarize` had already established **55,878** as the object
count *before* the sync ran. An empty destination directory is then a CONTRADICTION rather than a
result. Without that prior number, `SYNC_RC=0` plus an empty directory is indistinguishable from a
correct sync of an empty prefix.

**The control is: put the check on the RETRIEVAL, not on the RESULT.**

**What could NOT have caught it:**

| Check | Verdict | Why it fails |
|---|---|---|
| `rc == 0` | PASS | The CLI exits 0 with every object failed |
| destination non-empty | FAIL, but uninterpretable | Cannot distinguish "empty source" from "everything failed" |
| stderr scan | PASS under `--quiet` | Per-object errors suppressed; no summary exists to suppress |
| retry | PASS-ish, same result | Deterministic failure -- retrying reproduces it exactly |

**Generalisation (this is the transferable half):** *a count taken AFTER an operation measures the
operation's own success claim; a count taken BEFORE it is independent of that claim.* Any traversal,
sync, scan, or sweep whose denominator is derived from its own output cannot detect having done
nothing.

---

## RE-DERIVATION (live today -- this specimen is NOT repaired)

```bash
# 1. Establish the denominator FIRST -- this is the control, not a preliminary.
aws s3 ls s3://opal-mcp-audit/audit/ --recursive --summarize | tail -3
#    -> Total Objects: <N>, N is large

# 2. Attempt the sync to a Windows path:
aws s3 sync s3://opal-mcp-audit/audit/ "<any windows dest>" --quiet ; echo "rc=$?"
#    -> rc=0

# 3. Count what actually arrived:
find "<dest>" -name '*.jsonl' | wc -l
#    -> 0
#    rc=0 AND 0-of-N IS the specimen.
```

**Positive control** (proves the machinery works and the failure is key-shaped, not
permissions-shaped): any prefix whose keys contain no colons syncs normally with the same
credentials.

**The working path, for anyone who needs this data:** do not download. Query
`opal_mcp.mcp_audit` via Athena, or read objects through boto3 in-process where no filename is ever
materialised.

---

## WHY THIS ONE IS NOT REPAIRED

There is no defect in *our* code to fix. `aws s3 sync` behaves as written; the S3 key convention is
reasonable; the Windows filename restriction is immovable. **The failure lives in the interaction**,
which is precisely why it is a WS-C7 specimen rather than a bug report: **no file in this repo is
wrong, and the estate can still silently get an empty dataset with a clean exit code.**

Repairing it would mean either changing the audit-lake key convention (a producer change with its
own blast radius, and not this lane's call) or wrapping every `s3 sync` in a denominator check --
which is a *control*, and controls are WS-C7's design output, not a fixture's to impose.

---

## OBSERVATION ROUTED TO WS-C7 DESIGN (not built here, per scope)

Recorded for `1.0.0_SA_CTO~Z`; **this fixture does not set the contract.**

1. **A recall standard needs a DENOMINATOR field, not merely a findings list.** "0 found" and
   "0 found of 55,878 attempted" are different claims, and only the second is falsifiable.
2. **Exit code is not a recall signal and should not be accepted as one.** This tool's `rc=0` is
   *correct* by its own contract -- it dispatched the transfers it was asked to. Recall is a
   different question from execution, and an instrument that conflates them cannot report the
   difference.
3. **A denominator derived from the operation's own output is not a control.** It must be
   established independently, and ideally *before* the operation runs.
4. **Same class, different door -- worth one line in the standard:** CLAUDE.md already records
   `git show <bad-ref> | grep -c foo` printing `0` (grep counted matches in an error message) and
   `objects=0` on unwritable filenames. This specimen is the second of those, met live, at scale,
   through a modern CLI that had every opportunity to report better.

---

## PROVENANCE

Observed while answering an Andrew-direct question about MCP audit records
(`s3://opal-mcp-audit/`, Athena `opal_mcp.mcp_audit`; the query that *did* work returned
andrew 54,976 / alyssa 895 calls). Session log `5fffc922d`. Scope grant: CTO~Z
`20260731T030549Z`. Handover: `20260731T024616Z`.
