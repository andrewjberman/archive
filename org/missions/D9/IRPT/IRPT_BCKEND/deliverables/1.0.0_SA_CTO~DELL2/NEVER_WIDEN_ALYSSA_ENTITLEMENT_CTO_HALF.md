# NEVER-WIDEN SIGN-OFF -- CTO HALF -- X-1 filer entitlement: Alyssa files on behalf of the partner firms

**Signer:** `1.0.0_SA_CTO~DELL2` | **Date:** 2026-10-08 ~19:0xZ | **Asked by:** `2.0.0_SA_COO~Y2` msg 1446 (READ-acked)
**Against:** `org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~Y2/release2_ycg/NEVER_WIDEN_PAIR_ENTITLEMENT_ALYSSA.md` @a919a97d25.
**Authority:** Andrew-direct ~18:5xZ, VERBATIM "Alyssa can file on behalf of all partner firms" (@d78ef1df76).

## Ruling on the open question (narrowing (b)): option (i), and widened so that NOTHING she has today narrows

His word GRANTS filing. It does not ask to restrict her. Today her row has no `allowedFirmIds`, which reads as unrestricted.
`current_authority.py:135-141` would refuse generation for any data firm off a written list, and that refusal would start immediately on
live release 1. So the list names every firm she can reach today, not only the three partner firms.

**The list:** `["49financial", "cottonwood", "inflection", "opal-capital", "demo", "mockadv"]`. That is every firm in
`data/firm_registry.json` plus her home firm `opal-capital`.

Why this widens nothing beyond his word:
- **The on-behalf admit** (`uploads.py`) refuses `opal-capital` and global owners (`INPUT_ACCESS_DENIED`).
- **demo and mockadv:** E6's grant reads only `opal-partner-{49financial,cottonwood,inflection}`. So an on-behalf lookup at `demo` or
  `mockadv` fails closed.
- **The effective on-behalf reach** is therefore exactly the three partner firms. Generation reach is unchanged from today.

Before the write, `~Y2` checks `data/firm_registry.json`'s `pseudo` block. If it holds a firm she generates for today, that firm joins
the list. The packet records the check.

## Blast radius signed

- **The write:** ONE conditional `update-item` on `PK = USER#usr_63f855c7e1da`, `SK = PROFILE`:
  `SET allowedFirmIds = <the list above>`, with `attribute_not_exists(allowedFirmIds)`. No other field.
- **Rollback:** `REMOVE allowedFirmIds`, read back as ABSENT.
- **Both branches:**
  - **Written:** the read-back equals the list exactly, and no other projected field changed.
  - **Not written:** the condition fails, or the before-read is not ABSENT. STOP, and nothing moves.
- **Narrowing (a)**, an upload for a partner firm without `advisor_email` being refused once E6 is live, removes nothing she has. Today
  she cannot upload for a partner firm at all.
- **Unchanged:** portal, tickets and partner data (they read the authorizer's context, not the row) and every other principal.

## Conditions

1. **Behavior proof:** once E6 is live, under its ledger or a successor: one on-behalf admit with her principal, by opaque id, and one
   generation for `opal-capital` that answers as before (the no-narrowing arm).
2. **Her name appears in no record, file or message,** only `usr_63f855c7e1da`.

**Verdict: GIVEN**, for exactly this one write with the list above.

-- 1.0.0_SA_CTO~DELL2
