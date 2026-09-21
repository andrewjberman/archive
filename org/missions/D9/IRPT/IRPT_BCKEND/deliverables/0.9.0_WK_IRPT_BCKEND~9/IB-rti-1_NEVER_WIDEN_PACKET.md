# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rti-1`: publish the repaired capture tool to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~9`. **Date:** 2026-09-21. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rti-1.the-capture-tool-repaired-command-readiness-origin.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rti-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (f)'s publish runs.

## 1. THE ACT AND ITS EXACT BLAST RADIUS

Copy exactly TWO objects, from the git-blob bytes at the commit that carries this packet, to the artifacts
prefix `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`, overwriting the two keys of the
same names, with the operator identity only:

| file | git blob (`git rev-parse HEAD:<path>`) | sha256 of the blob bytes |
|---|---|---|
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `ea60b932bd4fd8af1f08548ce51022c2740af8b2` | `5b26be9133ae468ddb55af4e34be860f7f2d7338dea496bfd71f0c43f5a01d23` |
| `infra/aws/ec2/investor-reporting-export/capture-session.sh` | `d704adfb7b6a3ee904c3ba7173eb81533679c97b` | `17ae44f0d6ee0a2f30225a99446f74c33fb82ce893026bb9852d211581ef89e0` |

`README.md` is source-only and is NOT published. Hashes are git-blob bytes (this box's `core.autocrlf` makes a raw
disk hash a different number for some files, row S113). **Nothing else moves:** `render_export.cjs`,
`run-export-render.sh` and `package.json` are untouched by this cell and are not written.

## 2. WHO READS THESE OBJECTS, AND WHAT THE ACT DOES NOT DO

- The two objects are read by the render host ONLY when a human starts it and its render document syncs the prefix
  (`aws s3 cp --recursive`, no `--delete`). **The host is STOPPED and this act does not start it.** So the publish
  changes no running system: it changes what the NEXT human-started sync would place on the host.
- `capture-session.cjs` is INTERACTIVE and is never run by the render command document, so publishing it cannot
  alter a scheduled or queued render. `capture-session.sh` likewise. The render path (`render_export.cjs`) is unchanged.
- No credential, session file, vendor origin or portal call is involved in the act.

## 3. THE EXPECTED OUTCOME IS READ FROM THE PRODUCER'S RULE, NOT PREDICTED

The property a reader may assume is "the host now runs the repaired tool". That is NOT what the act does: the
producer of the host's copy is the render document's own sync (`infra/aws/terraform/investor-reporting/export/ssm.tf`),
which runs at the human-started wave-2 step, and that step re-reads the bytes. Both branches are covered: if the
sync runs, the host receives exactly these two blobs; if it never runs, the host keeps whatever it holds (the
pre-repair tool, which is defective per rows C-S125/126/127 but inert while the host is stopped). **No host-side byte
verification is claimed by this cell.**

## 4. ROLLBACK

Per key, republish the PRIOR bytes: `git show eecaad4985:<path>` (the pre-repair blob) to the same key. Prior blobs:
`capture-session.cjs` `git rev-parse eecaad4985:infra/aws/ec2/investor-reporting-export/capture-session.cjs`,
`capture-session.sh` likewise. The prefix is not versioned-bucket-guaranteed by this cell (not measured here); the
git blob is the source of truth for rollback.

## 5. THE GATE, AND WHAT THE PUBLISH ARM PROVES

Arm (f) publishes only when BOTH halves are at HEAD naming this packet's blob; it opens a deploy-ledger entry
(`org/critical_paths/.open_deploys/irpt-rti-1-capture-tool-publish.json`) and commits its sentinel BEFORE the act,
reads each object back from S3, compares sha256 to the table above, and closes the entry. Verdict token:
`IBR91-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOBS`.

## 6. WHAT THE REPAIR CHANGED (for the signers)

S125 the printed port-forward command names a validated instance id (refuses and prints nothing otherwise); S126
"captured" requires 2xx + no sign-in redirect + no password input + the marker `[data-print-state]` (portal
`PrintEntry.tsx`, mounted only inside `ProtectedRoute`, portal `8894e765ac`); S127 the origin must be in a one-entry
allowlist, off-origin hops are refused and the saved state is origin-scoped. Open premise: `render_export.cjs` holds
no origin allowlist to be equal to (row `IRPT_BCKEND-W9-S1`); the vendor denylist IS equal and asserted so.
