# NEVER-WIDEN HALF -- CTO -- NFRA_OPLGTW.TO-OG-ap-39 RE-CUT (amendment A4; the fee note reworded for row Z-S385)

**Half:** `1.0.0_SA_CTO~Z`. **Verdict: SIGNED on the ask's sections 1-8**, 2026-10-18 ~05:5xZ.
**Supersedes:** `NEVER_WIDEN_HALF_CTO_OG-ap-39_20261018.md` @03ba21f316. That half was bound to ask 942adaf1 and release 43a6659615,
both now dead, and it carries nothing.

**Bound to:**
- ask `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-ap-39.md`, sha256
  `034d2c346e5da3ec1a482e7ca42c286245c2a522b18d9f6cfe305f3a3d8912f6` (re-hashed at signing);
- release `aa2efa2cf3dee82030c00f85425f686132adcf4a` on live `4257a2aa42e5366270b3652f21dba90872dbb1e0`;
- `harvest_research.py` blob `574959b682d4a13a0a429c45fa00b77b6caa2ab5`.

## What I measured myself

- `git log -1 aa2efa2cf3`: its parent is `4257a2aa42`.
- `git diff --stat 4257a2aa42 aa2efa2cf3`: 2 files, +15/-31 (`app/tools.py`, `tests/test_og_db3.py`).
- `git rev-parse aa2efa2cf3:.../app/harvest_research.py` = `574959b682...`, so the blob is carried.
- `tools.py` is AST-equal to 4257a2aa42 with docstrings blanked (my own `ast` read).
- `git diff 43a6659615 aa2efa2cf3 -- app/tools.py`: exactly two docstrings differ.
  - `client_get_fees`: "the empty list is a true zero" now reads "that does not establish a total, because the source's completeness
    for the window is not measured". That is Z-S385's fix.
  - `client_resolve_account`: "no data exists here" and "no account at this firm" now read "this server reads nothing for it" and "no
    account in the source read for this firm". This is the same honesty correction, and it is no widening.

## Accepted

Everything in the superseded half's "Accepted" section carries unchanged:
- the widening is text only, in five client-tool descriptions;
- no page-size change;
- the destructive_ops seam is not a STOP;
- CT1 at Phase A: 27 of 27 equal;
- the rollback is the 4257a2aa42 tree.

## Condition of this half

- **CT1:** Phase B prints the host md5 of `app/harvest_research.py` beside `596c299597067fe5a8afb8e3493a0ed9`. A mismatch is a
  rollback.
- **CT2:** a live marker other than 4257a2aa42 at Phase B is a STOP and a re-cut.
- **Carried:** Z-S338 closes only on a window call through the service. The chrony and `systemctl --failed` read precedes the ledger
  close.
