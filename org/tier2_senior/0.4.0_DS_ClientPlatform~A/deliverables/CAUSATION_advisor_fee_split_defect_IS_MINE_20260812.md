# CAUSATION — the INF advisor fee-split defect is MINE. Root cause CLOSED, not open.

**2026-08-12 ~15:52Z, written into the record ahead of the device reboot** at base's explicit
ask (*"If you know anything about that basis change, write it into the record before the
reboot — your context may close it in one line"*). It does close it, and the line is: **I did
this.** Pairs with `org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/DEFECT_INF_ADVISOR_FEE_SPLIT_IS_FEE_EARNING_DROPPED_20260812.md`
(@97e2cadc14), whose symptom and mechanism are correct and whose "root cause OPEN" line is now
answered.

## THE CAUSE — one act, mine, deliberate, and incompletely censused

`is_fee_earning` did not "vanish." **I retired it from the silver billing dim on 2026-08-11**
as leg (b) of the flag act — **Andrew-direct instruction #2**, *"fix the is_fee_earning flag
derivation too when the window fix lands"* — under CTO's Rule-17 placement ruling that a
judgment classification is gold-tier, not silver. The derivation was re-homed to its single
gold-tier home `data/inf/scripts/gold/lib/fee_classification.py`. That act is correct and I
would take it again.

**The schema widening 13 -> 17 columns on 08-11 is also mine** (`ending_mv_reported` /
`ending_mv_source` from the window fix). Base marked the adjacency INFERRED and was right to:
**the two changes are the same act, deployed together, first exercised on the 08-12 scheduled
run** — which is exactly why both surfaced on the same partition. Adjacency, confirmed.

## ⛔ THE DEFECT IS THE CENSUS, NOT THE RETIREMENT

The retirement was gated on repointing every reader, and I repointed five and verified all
five deployed (md5 TIE, re-verified today): `INF_D_02` `4a61f28c` · `INF_D_00c` `a88c5997` ·
`INF_D_00f` `d769a8f7` · `INF_C_09` `faf9e9cd` · `INF_D_04` `eaae8fb4`.

**I enumerated the reader set over `data/inf/scripts/` and never over `infra/aws/lambda/`.**
The missed consumer is `infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py`,
which reads the billing dim at `:1059` and gates at `:495` on `is_fee_earning` being present.
Column gone -> gate False -> `fee_earning_aua` never written -> `:737` silently defaults 0.0
-> `:738` assigns the whole book to non-fee.

**MY OWN LEDGER NAMED THIS EXACT HAZARD AND I STILL MISSED IT.** The coupling note read:
*"(b) retire the silver-side `_derive_is_fee_earning` — fires WITH (d), never before (dropping
the column while D_02 reads it would silently vanish served advisor fee fields)."* I knew the
failure mode, I built the sequencing around it, **and then I enumerated the wrong denominator.**
A census over a subtree is not a census over consumers. **The gold scripts are one producer
tree; the Lambdas are another, and nothing in my search would ever have shown me the second.**

## SEVERITY — this one IS user-facing, unlike everything else in my day

Every other figure I moved today changed an undeployed emitter or matched a correct serve.
**This changed a LIVE served artifact**: advisors' `summary.json` shows `fee_earning_aua` 0.0
and their entire book as non-fee-earning. Base's `patrick_scanlan` instance: $0.00 fee-earning
beside $23,659,587.43 non-fee and a 114.5 bps earned rate — internally contradictory on its
face. **INFERRED, unmeasured: the blast radius is presumably every advisor summary object, not
one; I have not enumerated them.**

## ⛔ IT CANNOT LAND SAFELY BEFORE THE REBOOT — SAYING SO PLAINLY, PER MSTR

The correct fix is repointing the Lambda onto `lib/fee_classification.py`. **That is a Lambda
deploy, which is Terraform-only and not my lane**, and pushing an infra deploy into a reboot
wind-down is precisely the half-landed-deploy class NEVER#8 exists to prevent. **I am not
starting it.** Options for whoever holds it, with my read:

1. **REPOINT THE LAMBDA onto the gold lib** — the correct fix, matches the five gold repoints,
   preserves the single derivation home. Needs the Lambda lane (AE/DT) + a deploy window.
2. **Restore `is_fee_earning` to silver as a compatibility column** — fastest to serve-correct,
   but it **re-creates the second derivation home that Andrew's instruction #2 existed to
   remove**, and Rule 17 puts a judgment classification out of silver. I recommend against it
   except as an explicitly time-boxed shim with a named retirement act.
3. **Accept the wrong serve until the repoint lands** — only defensible with the blast radius
   measured first.

**My REC: (1), scheduled properly post-reboot. Not (2) — undoing a ruled act to patch my own
census miss trades a correct architecture for a fast number.** The decision is not mine.

## WHAT I OWE, WRITTEN DOWN BECAUSE NO SESSION SURVIVES THE REBOOT

- The repoint is **mine to build** if the Lambda lane takes patches from DS; **theirs if not**.
- **Before any fix: enumerate the blast radius** (how many advisor summary objects carry the
  zeroed split) — unmeasured, and the fix should not ship without its denominator.
- **The census lesson generalizes beyond this defect and is the part worth keeping:** any
  future silver column retirement must census consumers across **`data/*/scripts/` AND
  `infra/aws/lambda/` AND the portal**, because a producer tree is not a consumer set. Offered
  as a gate candidate for whoever owns the retirement checklist.
