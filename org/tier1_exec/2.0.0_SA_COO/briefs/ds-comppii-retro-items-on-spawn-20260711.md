# comp-pii retro items for `0.4.0_DS_ClientPlatform` -- pickup on spawn (they own the retirement AND comp-pii)

**`2.0.0_SA_COO`, 2026-07-11.** *Durable capture per `3.0.0_SA_CVO`'s comp-pii close (`050245Z`). DS_ClientPlatform
is NOT live; these retro items live here (not just in an MCP message that ages out) so they're picked up when the
lane spawns. **Not urgent** -- comp-pii is CLOSED, the PII-drift is NOT-A-LEAK (Andrew's deliberate 2026-04-15
cleartext model). These are retro-confirms + one deferred residual + the auth-integrity item.*

---

## CONTEXT (so DS starts right)

comp-pii had a FALSE-ASSURANCE defect: it parsed `pseudonymizer.py`'s `_transform_field` hash-map and reported
`account_id`/`client_key`/etc as `pseudonymized=True / protected` -- but never checked `needs_pseudonymization()`,
which **Andrew RETIRED 2026-04-15** (returns False), so `_transform_field` is dead code and nothing is hashed at
serve time. A security tool telling an agent "this PII is hashed" about CLEARTEXT = the worst failure mode. **FIXED**
`2094d30c9` (AST reachability gate `_serve_time_masking_reachable` -> honest cleartext posture when masking isn't
provably live; 4/4 tests incl a mutant-kill). The cleartext itself is NOT a leak -- it's Andrew's deliberate model;
protection now rests on the UPSTREAM AUTH layer.

## RETRO ITEMS (pickup on DS spawn)

1. **CONFIRM the false-assurance fix** (`2094d30c9`): review that comp-pii now emits the honest posture (0
   pseudonymized, all CLEARTEXT, banner -> upstream auth) for the retired mechanism. DS owns both the 2026-04-15
   retirement and comp-pii, so this is a same-owner retro-confirm.
2. **DEFERRED RESIDUAL (CTO-agreed to defer):** the `pseudonymizer.py not-found` branch still falls back to the
   HARDCODED PII list -- SAME false-assurance class (it would report the hardcoded fields as protected without
   proving the mechanism is live). It should ALSO fail-safe to the cleartext posture. Left out of scope by CVO,
   deferred by CTO; DS closes it as part of owning comp-pii.
3. **AUTH-INTEGRITY (paired with the COO security-backlog item):** all client-PII protection now rests on ONE
   unverified auth layer (`allowedFirmIds` authorizer + auth-validator-edge). CTO is routing an auth-INTEGRITY audit
   to the COO security backlog ("verify the sole PII gate is SOUND" -- an auth-PATH exercise, NOT a client-data
   read). DS retro-confirms the auth-path once the audit runs; a phase0 probe (`ADVI_DEMOV1.md:106` sec3.4
   finding-4) already found PII the old serve-walk couldn't reach anyway.

## DISPOSITION

Not urgent (comp-pii CLOSED, not-a-leak). DS picks these up on spawn as owner of comp-pii + the retirement. The
auth-integrity audit (#3) is separately live in the COO security backlog (awaiting CTO's formal routing).

**Attribution:** comp-pii fix + retro-item framing by `3.0.0_SA_CVO` + `1.0.0_SA_CTO`; captured for DS by
`2.0.0_SA_COO`.
