# DRAFT, NOT ISSUED -- NFRA_OPLGTW cell `OG-mu-1` -- a muse-only narrowed OAuth client on the Opal gateway (CTO msgs 34775 and 34800; Andrew-direct 2026-10-16 ~06:5xZ and ~07:0xZ)

Status: QUEUED AFTER the 2026-10-16 ~22:00Z finish; not on the critical path (CTO: "Still after the 22:00Z finish; ap-23's re-cut comes first"). Cut it only once `OG-ap-23` has released.

Authority (VERBATIM, as the CTO relayed it):
- Andrew ~06:5xZ: "ok i want the COO~O to have this work folded in to OPLGTW, let CTO~Z know that." Record `org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/ANDREW_DIRECT_20261016_065xZ_MUSE_GATEWAY_SCOPE_FOLDS_INTO_OPLGTW_COO_O.md` @66f25c55e2.
- Andrew ~07:0xZ: "im fine with muse having full access for now, ultimately it should just have m365 teams/emai, but we can get there." Record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261016_070xZ_MUSE_FULL_GATEWAY_ACCESS_FOR_NOW_M365_TEAMS_EMAIL_TARGET.md` @adb8e79330.

Spec (read at that commit before cutting): `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_MUSE_ON_OPALGATEWAY_20261016_Z.md` @d5be3853aa, ruling 1; the CRO's scope `@6e57b47a6a` section 5, route C.

What it is (the CTO's words for the worker face, as narrowed by msg 34800): a client-keyed NARROWING of an unscoped identity. Muse's OAuth client sees ONLY the M365 mail and Teams tools (read AND send) plus `whoami`, and no other source. Until the cell lands muse keeps full gateway access (Andrew: "for now"); Andrew's own client keeps what it has today.

Criteria the CTO named (msg 34800): a Schwab call by muse's client REFUSES; a portal call by muse's client REFUSES; Andrew's own client still passes (negative control on the same tools). Each is one real call through the installed gateway, so the cut is a WORLD-class code cell plus a release, a never-widen ask NARROWING an identity (a half each from the CTO, COO and CVO), and a slot on the gateway host AFTER `OG-ap-23`.

Read before cutting, and answer in the face: where the client-to-tool narrowing lives (`app/data_entitlement.py` and the access layer; the person reader's records are `NFRA_MCPORTAL`'s writes); whether it is a tier list or a per-client allowlist; that the allowlist names the five M365 mail and Teams tools by their registered names (read `app/tools.py`, do not type a list from memory); and that the admission class of every tool it leaves reachable is the one the PRD rules (PRD v3.1 Ruling 2: client data is data-grant class, master_admin only per PRD v3.14).
