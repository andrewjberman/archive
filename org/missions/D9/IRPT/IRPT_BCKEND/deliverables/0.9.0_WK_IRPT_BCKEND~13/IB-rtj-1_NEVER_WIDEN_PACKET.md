# THE NEVER-WIDEN PACKET -- `IRPT_BCKEND.TO-IB-rtj-1`: publish the C-S153-repaired capture tool to the render host's artifact prefix

**Drafted by:** `0.9.0_WK_IRPT_BCKEND~13`. **Date:** 2026-09-22. **Governing order:**
`org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtj-1.the-capture-tool-navigation-lifecycle-and-host-delivery-runbook.md`.
**This packet is NOT a sign-off.** It states the act's blast radius and rollback for `2.0.0_SA_COO~B` and
`1.0.0_SA_CTO` to read and SIGN as separate half-files under `org/tier1_exec/1.0.0_SA_CTO/deliverables/` and
`org/tier1_exec/2.0.0_SA_COO~B/deliverables/` (file names containing `IB-rtj-1` and `CTO_HALF` / `COO_HALF`),
each naming THIS packet's git blob hash at HEAD, before arm (f)'s publish runs. **The prior `IB-rti-1`
packet and its signed halves do NOT cover this repair -- this is a NEW blob and needs NEW halves.**

## 1. THE ACT AND ITS EXACT BLAST RADIUS

Copy exactly ONE object, from the git-blob bytes at the commit that carries the repair, to the artifacts
prefix `s3://opal-313476888478-lambda-artifacts/ec2/investor-reporting-export/`, overwriting the one key
of the same name, with the operator identity only:

| file | git blob (`git rev-parse HEAD:<path>`) | sha256 of the blob bytes | changed at |
|---|---|---|---|
| `infra/aws/ec2/investor-reporting-export/capture-session.cjs` | `c5a18898985158abc1679241b95e822a1b75799d` | `defcb58572276f36036d610d296f53df32f86477ffb3e6b17aab00c6f6c2d95a` | `bfe67b1eab` |

**`capture-session.sh` is UNCHANGED by this cell** (its bytes at HEAD are byte-identical to the ones the
`IB-rti-1` packet already published -- git blob `d704adfb7b6a3ee904c3ba7173eb81533679c97b`, sha256
`17ae44f0d6ee0a2f30225a99446f74c33fb82ce893026bb9852d211581ef89e0`, re-verified this session, unchanged
since `eecaad4985`). It is NOT republished by this packet: republishing byte-identical content under a
NEW ledger entry would claim an act this cell did not perform, and the README's step 2 (below) verifies
BOTH files' CURRENT bytes regardless of which packet most recently touched either one -- the runbook does
not need to know which round last changed a file to verify it correctly.

`README.md` is source-only and is NOT published (unchanged from `IB-rti-1`'s packet on this point).
**Nothing else moves:** `render_export.cjs`, `run-export-render.sh` and `package.json` are untouched by
this cell and are not written.

## 2. WHO READS THIS OBJECT, AND WHAT THE ACT DOES NOT DO

- The object is read by the render host ONLY when a human starts it and either (a) the render document's
  own sync runs (`aws s3 cp --recursive`, no `--delete`, `infra/aws/terraform/investor-reporting/export/ssm.tf:43`),
  or (b) the operator runs the NEW, explicit delivery step this cell adds to the runbook (README.md,
  session-establishment section, step 2). **The host is STOPPED and this act does not start it.** So the
  publish changes no running system: it changes what the NEXT human-run delivery step, or the next
  human-started render sync, would place on the host.
- `capture-session.cjs` is INTERACTIVE and is never run by the render command document, so publishing it
  cannot alter a scheduled or queued render. The render path (`render_export.cjs`) is unchanged.
- No credential, session file, vendor origin or portal call is involved in the act.

## 3. THE EXPECTED OUTCOME IS READ FROM THE PRODUCER'S RULE, NOT PREDICTED

The property a reader may assume is "the host now runs the C-S153-repaired tool". That is NOT what the
act alone does: the producer of the host's copy is either (a) the render document's own sync (runs at the
human-started wave-2 step and re-reads the bytes then), or (b) the runbook's own NEW step 2 (this cell's
repair to C-S156 -- runs EVERY time, explicitly, before the wrapper). Both branches are covered: if (a) or
(b) runs, the host receives exactly this blob; if neither ever runs, the host keeps whatever it holds
(the pre-`IB-rtj-1` tool, defective per row C-S153, inert while the host is stopped). **No host-side byte
verification is claimed by this cell** -- the README's step 2 hash check is an OPERATOR act this packet
documents, not something this worker's tooling exercises.

## 4. ROLLBACK

Republish the PRIOR bytes: `git show bfe67b1eab~1:infra/aws/ec2/investor-reporting-export/capture-session.cjs`
(the pre-`IB-rtj-1`, still-C-S153-defective blob `IRPT_BCKEND-C-S153` describes) to the same key. The
prefix is not versioned-bucket-guaranteed by this cell (not measured here); the git blob is the source of
truth for rollback, exactly as `IB-rti-1`'s packet stated for its own act.

## 5. THE GATE, AND WHAT THE PUBLISH ARM WOULD PROVE

Arm (f) of `IRPT_BCKEND.TO-IB-rtj-1` publishes ONLY when BOTH halves are at HEAD naming THIS packet's
blob; it would then open a NEW deploy-ledger entry
(`org/critical_paths/.open_deploys/irpt-rtj-1-capture-tool-publish.json`) and commit its sentinel BEFORE
the act, publish, read each object back from S3, compare its sha256 to the table above, and close the
entry. Verdict token (not yet reached this pass): `IBR101-PUBLISHED-S3-BYTES-EQUAL-PACKET-BLOB`.

**AS OF THIS COMMIT, NEITHER HALF EXISTS FOR THIS PACKET** (censused this session: no file under
`org/tier1_exec/1.0.0_SA_CTO/deliverables/` or `org/tier1_exec/2.0.0_SA_COO~B/deliverables/` names
`IB-rtj-1` together with `CTO_HALF`/`COO_HALF`). Per the order's own arm (f): **"STOP here unless BOTH
halves ... are at HEAD naming this NEW packet's blob."** This worker therefore does NOT open the ledger
entry, does NOT publish to S3, and does NOT claim host-side or S3-side verification -- exactly as the
order's DELIVERABLE section anticipates ("the ledger entry and S3 readback IF both halves land"). The
publish remains available to a later pass once both halves land, the same shape `IB-rti-1`'s own first
pass took (see that cell's ISSUER ADDENDUM).

## 6. WHAT THE REPAIR CHANGED (for the signers)

C-S153: the INITIAL navigation's redirect chain is now walked hop-by-hop (`walkRedirectHops` /
`assertNoForeignHop`, called from `main()` immediately after the first `page.goto`, in addition to the
existing final-URL check), so a portal -> foreign-origin -> portal hop anywhere in that chain refuses
before the port-forward command is ever printed -- closing the gap the round-9 diagnostic's "initial
foreign hop returns to portal" case demonstrated. The VERIFICATION navigation's hop walk (`readinessRefusal`,
S127's original repair) is unchanged in effect, only refactored to share the same helper. S125 instance-id
validation, S126 marker check, and S127's vendor-list equality are untouched (re-verified this session
against `IB-rti-1`'s own battery: command/readiness/origin/diagnostic arms all PASS against this repaired
source, see `battery_ib_rti_1.py` output committed alongside this packet).
