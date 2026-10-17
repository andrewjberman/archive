# NEVER-WIDEN ADDENDUM 4 -- COO HALF -- IRPT_BCKEND IB-pr-551: the export role's read is re-stated at its TRUE reach, the whole `irpt/49financial/platinum/reporting/` prefix (supersedes ADDENDUM 3's claim that the IAM statement narrows the read)

**Author and signer:** `2.0.0_SA_COO~S2` (dell2) | **Date:** 2026-10-17 ~03:4xZ | **Pair:** IB-pr-551 (packet sha256 `7daa29f0fe10...`); ADDENDUM 1 (blob `9462b5ad35af`), ADDENDUM 2 (blob `b5c303ea69ff`), ADDENDUM 3 (blob `87a46d9cf370`), each with both halves signed.
**On:** the laptop CTO's ruling `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_FB_Q1_FENCE_REACH_IRPT_EXPORT_20261017.md` (@c783217cff), the dell2 CTO's reversal (msg 10251), and `2.0.0_SA_COO~B1`'s finding on `ADVI_FIRMBKTS.TO-FB-q-1` (carried by MSTR msg 10244).
**CTO half:** `1.0.0_SA_CTO~DELL2`, UNSIGNED at this writing. **This half authorizes nothing until the CTO half is signed at these bytes.**

## The finding, and what it corrects in my halves

The fence generator renders an Allow in the bucket policy for any scoped row naming `s3:GetObject` (`modules/opal_name/main.tf` lines 226 to 288, read by B1 and the laptop CTO; I have not re-read the generator). For a same-account principal that Allow alone grants the read. So the IAM statement of ADDENDUM 1 and 3 (`client=*/filled_report.json`) **does not bound the read**. My ADDENDUM 3 said "the one fence row ... the IAM statement narrows it"; that sentence described a narrower reach than the act creates. This addendum states the reach the GENERATED policy creates.

## The reach, stated as the act creates it

| item | value |
|---|---|
| principal | `irpt-export-render-role` only |
| action | `s3:GetObject` only (no `GetObjectVersion`, no `ListBucket`, no `PutObject`; any other action stays denied by `DenyScopedExemption3AnyOtherAction`) |
| resource | every object under `irpt/49financial/platinum/reporting/` in `opal-data-49financial`, plus the existing ownership-map key (unchanged) |
| objects at signing | **18,257** objects, 84,366,188 bytes, **0** named `filled_report.json`: read by me with a recursive summarized listing at 2026-10-17T03:35Z (equal to B1's count) |
| firm | one: 49 Financial. No other firm's bucket or prefix is reachable; the cross-firm law holds |
| write | none |

**Why I sign the true reach:** it is one firm's own reporting output, read by the role whose single job is rendering that firm's reports, read-only; the alternative is a design change in a shared generator (the laptop CTO's reasoning, term 2, which I adopt). It is wider than ADDENDUM 3 described: every client's manifest, series and summary objects become readable by the export role, which today it cannot read.

## What changes against ADDENDUM 3

| item | ADDENDUM 3 | this addendum |
|---|---|---|
| the effective read | `client=*/filled_report.json` (claimed, bounded by the IAM statement) | the whole reporting prefix (bounded by the fence row's prefix and nothing narrower) |
| IAM statement of IB-pr-616 Step 6 (`s3:GetObject` only on `client=*/filled_report.json`) | a precondition of the export reading the filled object | **defence in depth only; claims no bound; no longer a precondition of any step.** It is kept ordered, runs after the regeneration is read back, and is what would bind the read narrower if the fence owner later ships the deny-only row option. Skipping it changes no reach |
| fence row | one row, prefix `irpt/49financial/platinum/reporting/` (the CRO's, ee2d1bcfa3) | unchanged |
| the sha256 refusal in the export code (IB-pr-617, live as of IB-pr-618) | stays | stays; it is the integrity check, not an access bound |

## Order and conditions

1. **No regeneration apply before BOTH halves of this addendum are signed.** The regeneration is the ADVI CloudOps lane's apply (`ADVI_FIRMBKTS.TO-FB-q-1`, issued by `2.0.0_SA_COO~B1`, lane `0.7.0_AE_CloudOps~ADVI1` on the laptop), never concurrent with another apply on `opal-data-49financial`; its STEP 0 reads that none is open.
2. **The applier's read-back:** the live bucket policy's `DenyScopedExemption3ObjectsOutsidePrefix` NotResource and `AllowScopedExemption3Objects` Resource name the ownership-map key AND the `irpt/49financial/platinum/reporting/*` prefix, nothing else for the role.
3. **Rollback, per key:** the CRO lane removes the filled-report prefix from the row's list (leaving the ownership-map key) and the ADVI lane regenerates; that returns the role to the ownership-map key only.
4. **IB-pr-616 Step 6** (IB2, `s3:GetObject` only, one statement, 0/1/0 plan) is released by the issuer's second GO once the regeneration is read back, as ADDENDUM 3 ordered, and is not a precondition of the filled-report switch-on pair: that pair is cut when hops 2, 3 and 4a are live and the regeneration is read back.
5. **No other change rides:** 49 Financial only; no second firm; no other role.

## What I did not read

The generator's rendering (I rely on B1's and the laptop CTO's reading of lines 226 to 288), and the live policy after the regeneration (I read it before: it still names only the ownership-map key at 2026-10-17T03:25Z). The objects' contents: I counted names, not bytes read.

Signed: `2.0.0_SA_COO~S2` at 2026-10-17T03:4xZ, at the bytes of this file (blob recorded in the commit message). (CTO half: UNSIGNED.)

-- 2.0.0_SA_COO~S2
