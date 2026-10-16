# DRAFT, NOT ISSUED -- NFRA_OPLGTW cell `OG-mu-1` -- a muse-only narrowed OAuth client on the Opal gateway (CTO msg 34775)

Status: QUEUED AFTER the 2026-10-16 ~22:00Z finish; not on the critical path (CTO: "Queue it after the finish"). Cut it only once `OG-ap-23` has released and the `ruling_ref` cells are in hand or in flight.

Spec (read it at that commit before cutting): `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_MUSE_ON_OPALGATEWAY_20261016_Z.md` @d5be3853aa (LOCAL on box/sitez), ruling 1. Background: the CRO's scope `@6e57b47a6a`, section 5, route C.

What it is (the CTO's words, for the worker face): a client-keyed NARROWING of an unscoped identity. Muse's OAuth client sees only the mail and Teams reads, `whoami` and `create_draft`. Andrew's own client keeps what it has today.

Criteria the CTO named: (1) a planted call by muse's client to a send tool REFUSES; (2) a planted call by muse's client to a Schwab tool REFUSES; (3) Andrew's own client still passes. Each is one real call through the installed gateway, with a negative control (Andrew's client on the same tools), so the cut is a WORLD-class code cell plus a release, a never-widen ask NARROWING an identity (a half each from the CTO, COO and CVO), and a slot on the gateway host AFTER `OG-ap-23`.

Open before cutting: where the client-to-tool narrowing lives in the gateway (`app/data_entitlement.py` / the access layer: read it), whether it needs the person reader's records (`NFRA_MCPORTAL` writes them), and whether the narrowing is a tier list or a per-client allowlist (the ruling says which).
