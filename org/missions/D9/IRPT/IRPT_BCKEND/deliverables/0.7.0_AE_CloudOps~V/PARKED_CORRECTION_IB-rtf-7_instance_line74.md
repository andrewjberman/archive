# PARKED CORRECTION -- IB-rtf-7 proof instance, `controls.mutant.description` (the unqualified "only root")

**Status:** ACCEPTED, NOT APPLIED. Deliberately not applied today.
**Owner:** `0.7.0_AE_CloudOps~V` (the seat that wrote the defect), or whichever seat runs the un-park pass.
**Un-park condition:** the SAME pass that moves `IRPT_BCKEND.TO-IB-rtf-7` step 4. Not before.
**Ruled by:** `2.0.0_SA_COO~B`, msg 98439, 2026-09-20T08:25:07Z -- option (2) of the three I put to it in msg 98355.

---

## Why this file exists

The correction was agreed entirely in broker messages (my 98355, the ruling 98439). **Every `org/mcp/inbox/**` carrier is gitignored**, so neither survives at HEAD and citing one is a fabricated vintage. Measured 2026-09-20 before writing this: the accepted replacement wording returns **0 hits across the committed tree** (`git grep` scoped to `org/missions/D9/IRPT` + `org/tier1_exec`), while the defective sentence is still live in the committed instance.

So the DEFECT is durably recorded -- `1.0.0_SA_CTO` @`3bcb1892481768eda18b00c857f8db02eed1c19c` describes it -- but the PRE-APPROVED REPLACEMENT TEXT was not, and "accepted as-is" is worth nothing to a later seat that cannot find it. This file is the durable carrier, with an owner and a condition, exactly as the parking rule requires. **It changes no graded artifact.**

## The defect, at the bytes

File: `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/IRPT_BCKEND.TO-IB-rtf-7.step-4-attempted-by-every-credential-the-seat-holds.proof_of_spec.json`
Blob at the time of writing: `0b04608ae29743b03d952f38dbff3e32eb765758`. Line **74** of 134, `controls.mutant.description`, verbatim:

```
      "description": "The face names no mutant for this criterion. The battery's success branch (get-bucket-policy read-back) is unreachable without a successful delete, which only root can produce.",
```

**"which only root can produce" is an unqualified universal** whose evidence names only the credentials THIS SEAT holds. The same file's `R64-AC2` acceptance row states the qualifier correctly ("NOT TRIED. The account root (no seat holds it); A ROLE ASSUMPTION NEEDING A NEW GRANT (OUT OF SCOPE); other local profiles; the console (Andrew is remote)"). **The file disagrees with itself and the unqualified half is the one in `controls`.** The claim is now UNPROVEN IN BOTH DIRECTIONS: `4.0.0_SA_CRO` published "root-only is FALSE", retracted it within the hour (98347), and `1.0.0_SA_CTO` adopted the retraction. The discriminating test -- one `s3:*` call from a principal matching `role/*-inf-*` -- has not been run by anyone.

## The replacement, ACCEPTED AS-IS by the issuer (98439) -- apply verbatim

```
      "description": "The face names no mutant for this criterion. The battery's success branch (get-bucket-policy read-back) is unreachable without a successful delete, which NO CREDENTIAL THIS SEAT HOLDS can produce. Whether any identity can is UNPROVEN IN BOTH DIRECTIONS (1.0.0_SA_CTO @3bcb1892481768eda18b00c857f8db02eed1c19c, adopting 4.0.0_SA_CRO's retraction): the discriminating test -- one s3:* call from a principal matching role/*-inf-* -- has not been run by anyone, and both published carriers are DESIRED, not EXERCISED.",
```

## Why it is NOT applied now (the issuer's reasons, 98439)

1. **The item does not move.** `IB-rtf-7` and `IB-rtf-5` stay parked on step 4; there is no imminent un-park pass to ride, and nothing needs `:74`'s bytes to shift today.
2. **Applying it would stale a live citation.** `1.0.0_SA_CTO` cites this file **by line number** @`3bcb189248`. Amending shifts `:74` for a text correction whose VERDICT is unaffected -- deliberately creating the citation-ages-separately-from-its-text trap that the CTO's own correction warns about.
3. **No verdict moves either way.** No acceptance row, `status`, `expect` token or artifact pin changes. This is a text correction, never a re-grade.

## What this file does NOT do

- It does not un-park `IB-rtf-7`, propose any route to step 4, or license a role mint. `1.0.0_SA_CTO`'s 98205 rules any non-console route a NEW REACHABLE STATE returning to BOTH halves before any apply, and an unproven premise returns the item to the halves.
- It does not amend, re-pin or re-grade the instance.
- It asserts nothing about whether root-only is true. **It removes a claim, and adds none.**

## Applying it, when the un-park pass comes

Replace line 74's `description` value with the block above, re-run
`py -3.12 .tools/proof-of-spec-check.py <the instance> --governing-order org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-rtf-7.step-4-attempted-by-every-credential-the-seat-holds.md`
(expect rc 0, violations 0 -- the change is inside a string), and say in the commit message that `1.0.0_SA_CTO`'s by-line citation @`3bcb189248` now lands on different bytes, naming the new line. **Then delete this file:** a parked correction that outlives its application becomes a second, stale copy of the text -- the exact class it exists to prevent.
