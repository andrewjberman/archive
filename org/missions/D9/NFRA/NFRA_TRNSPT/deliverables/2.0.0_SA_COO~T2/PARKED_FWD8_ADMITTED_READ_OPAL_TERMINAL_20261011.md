# PARKED -- NFRA_TRNSPT FWD-8: the ADMITTED read of the second-reader role as Opal_Terminal

**Owner: Andrew.** Parked 2026-10-11 by 2.0.0_SA_COO~T2 on the CTO's ruling (1.0.0_SA_CTO~DELL2 msg 4272). **FWD-8 is UNGRADED until
this item is met.**

## The criterion, moved here with its text unchanged

From `NFRA_TRNSPT.TO-APPLY-a18.second-reader-role-laptop`, step 2:

> Proof (CTO half): as the new role (assumed from Opal_Terminal), GetObject one transcripts key = ADMITTED

Statuses only; no object content kept or printed. It is UNMET. The other clause of that step (an unnamed dell2 role's GetObject of the
same key = REFUSED) is MET: measured on dell2, 2026-10-09 14:5xZ, AccessDenied.

## What un-parks it

The read is run on the device that holds the Opal_Terminal access key, by whoever sits at it. No credential is copied to any other
box (CTO ruling, msgs 4271 and 4272: a seat holding a copy of the key proves only that the key travels).

**The device, as far as any record names it.** IAM user `arn:aws:iam::313476888478:user/Opal_Terminal`, created 2026-07-10 22:07Z,
tags `purpose=bloomberg-terminal-device`, `created_by=parity-with-Andrew_Berman` (read live 2026-10-11T06:2xZ). So the record that minted
it names the BLOOMBERG TERMINAL DEVICE. That device is NOT one of the four registered boxes (`org/devices/DEVICES.json`: laptop, sitez,
dell1, dell2), and the key is on none of the boxes that were read:
- site Z: one AWS profile, Andrew_Berman (0.7.0_AE_CloudOps~ZC on crossbox XB-20261011T055148Z-00a7);
- dell2: `default` only (the CTO's read, msg 4271).

**Not measured, and it matters:** the user's ONE access key (Active, created 2026-07-10 22:08Z) reads `LastUsedDate` NONE in IAM. No
record shows the key has ever been used from any machine, so which machine holds it, and whether any does, is unknown here. Andrew
names it.

## The act, when it is run (read-only)

1. `aws sts get-caller-identity`: the Arn must read `arn:aws:iam::313476888478:user/Opal_Terminal`.
2. `aws sts assume-role --role-arn arn:aws:iam::313476888478:role/teams-global-transcripts-second-reader-role --role-session-name a18-admitted-read`.
3. With the assumed role: `aws s3api get-object --bucket opal-data-transcripts --key "teams/transcripts/state/pull_runs/run=2026-10-11T03:38:57Z/run.json" <a temp file>`.
   Report the outcome (200 or the error code), `ContentLength` and `ServerSideEncryption`; delete the temp file. The key is a run record
   with no transcript text.

Full wording: `XB_ORDER_A18_ADMITTED_READ_TO_SITEZ_20261011.md` (the same act; site Z could not run it and does not owe it).

## Is it the same act as Andrew's own read for FWD-5?

No. FWD-5 grades on Andrew's read through the SILVER-ONLY reader role (`teams-global-transcripts-silver-reader-role`); this item is the
SECOND reader role, trusted to Opal_Terminal alone. Different role, different principal. If the Bloomberg terminal device is where
Andrew sits for both, the two reads can be done in one sitting, but each is its own proof.

## State of the surrounding records

- Live trust of the role (read 2026-10-11T06:27Z): exactly `arn:aws:iam::313476888478:user/Opal_Terminal`.
- Ledger `nfra-trnspt-a18-second-reader-laptop-20261009` stays HELD-SOVEREIGN-GATED on this read. That is accurate and is left as it is.
- Crossbox XB-20261011T055148Z-00a7 stays OPEN and is not owed by site Z (CTO msg 4271).

## UPDATE 2026-10-16 ~13:5xZ (2.0.0_SA_COO~T2): the identity is gone; the parked item cannot be run as written

Andrew-direct, relayed by `1.0.0_SA_CTO~DELL2` msg 9396 (record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_134xZ_SYNTHETIC_TEST_DELETES_NEED_NO_CALL_OPAL_TERMINAL_GONE_DELL2.md` @c2b2f1e950): "opal terminal key and account are already deleted from IAM". Row e260 is closed.

Measured read-only by the issuer, 2026-10-16: `iam get-user --user-name Opal_Terminal` answers `NoSuchEntity`. The second-reader role `teams-global-transcripts-second-reader-role` has ONE trust statement whose principal reads as the bare unique id `AIDAUR7FNW6PPTS7ZH2VB` (no condition): IAM renders a deleted principal that way, so the role trusts an identity that no longer exists and NO identity can assume it today. Step 2 of the parked act (assume the role from Opal_Terminal) and therefore step 3 (the ADMITTED GetObject) are unrunnable; the other clause (an unnamed dell2 role REFUSED) stays MET.

What a re-route needs, none of it cut here (NFRA_TRNSPT FWD-1..9 are HELD-AT-STOP, msg 7599, and the work is not in the commentary scope):
1. the CTO's word on FWD-8's ACCEPT list, which names "the terminal seat's account" (PRD v0.2): drop it as moot, or name the live identity that stands for it;
2. a change of the role's trust statement to the named live identity(ies) (Terraform, a WORLD act for a CloudOps seat under a pair), after which the ADMITTED read runs as that identity and the REFUSED arm is repeated;
3. or a re-grade of FWD-8 at the next analysis without the terminal clause.
