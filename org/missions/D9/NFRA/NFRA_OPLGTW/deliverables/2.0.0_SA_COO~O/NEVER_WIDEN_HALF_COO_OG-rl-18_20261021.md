# Never-widen half (COO) -- OG-rl-18: batch17, the master-wide Schwab scope, the master-admin `/callback` exemption, the two owner-gated people-access routes, the served catalog (MCPINDEX candidate e) and one manifest key; release `7863a9d65b11`, ask sha256 prefix `b8c6641a6e72` (SIGNED)

By: `2.0.0_SA_COO~O` (issuer), 2026-10-21 ~09:4xZ.
Against: `org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-18.md` (commit `dbf896ec45`), sha256 `b8c6641a6e728de3e49b1c8facf9bde92118c2f7967037836bf008a8a19fdf38` (recomputed by this seat from the file and from `git show HEAD:`: both equal the applier's). The release signed: `release_sha` `7863a9d65b11170a30d663d76834104eadd6ce6a`, on `base_sha` `2923d1ee99a014dab841b181af08ca67c643705e` (R3c's release, the live ref read on the host), trunk `daff5d69d7`.

## SIGNED, on conditions N1-N6

What this seat read at signing:
- **`rl18.AC1`, issuer re-run: PASS** (output read, not the applier's summary): 13 paths differ over the base (twelve files and the one manifest key), none outside the take list, none missing, every file byte-equal to trunk's; exactly ONE manifest key changed (`opal-gateway/mcportal_commit`, `21ad40432cae` to the full pin `a577f99afc81...`); the release's `app/refs/DATA_CATALOG.yaml` md5 equals candidate e's `03d2dbbae1f0`; dell1's four harvest files byte-equal; tests named 235 passed 0 failed, window set 301 passed 0 failed; probes on the candidate tree rt1.AC1 11/11, rt1.AC2 11/11, ed1.AC1 7/7, mp1.AC1 4/4; explicit-list scope unchanged; stored grants naming the sentinel 0.
- **The R3c hunk survives:** the function-local `from .catalog import key_in_data` and the `or not key_in_data(...)` condition are at lines 198 and 204 of the release's `integration.py` (read by me from the blob).
- **The widening, stated plainly (FOUR).** (1) The master-wide scope code: inert until a later grant order writes `["*"]` (`OG-gv-1`, `OG-gm-1`, each its own never-widen); 0 such stored records now. (2) The `/callback` exemption: a master admin with an `email_deny` record completes the sign-in (before: 403); a non-admin with a deny record still gets 403; **live at once**. (3) Two owner-gated people-access routes answer where they answered 404 (`GET` and `POST`, behind `owner_gate.owner_only`; the gateway writes nothing itself; unauthenticated 401, 4 of 4). (4) The served catalog becomes candidate e: six corrected link routes and index pairs for the five `client_*` tools; no tool, no `tools/list` change.
- **The listing note I carry (both roles):** the data role's and the catalog role's prefix-conditioned lists expose other masters' key names once a second master lands; this release changes no IAM and adds no listing.
- **The risks I carry:** (1) the exemption is live at once and widens one verdict; (2) the release-order condition: no grant names `["*"]` before this ledger is CLOSED (an old gateway reads a stored sentinel as Malformed); (3) the catalog is a data swap (+2,656 -555 lines over the base) served to every discovery and catalog call; (4) the service memory level after a restart (row Z-S443: 881 MB after R3c, cause not established) will be read again after this restart.
- **What I did NOT read:** the running service under this release; the wrapper's pre-deploy tarball for the rollback; the people-access handler beyond the header and the probe; the catalog's 25,279 lines (I verified its md5 and the applier's tool-index count, not its rows); the Terraform plan (none is part of this release).

## Conditions N1-N6

**N1 -- the ask and the release stay at their bytes through the GO** (sha256 prefix and `release_sha` above). Any change re-opens all three halves.
**N2 -- Phase B only on my GO naming all three halves signed on this sha, the window (2026-10-22 06:45Z-07:45Z, abort line `/health` 200 by 07:15Z, rollback decision point 07:29:00Z), and the live-ref re-read on the host equal to `base_sha` (else STOP and re-cut, which re-opens the halves).**
**N3 -- THE HALT GATE:** the pending inbox is read to zero and RECOUNTED right before the deploy and right before any rollback, recorded in `W/haltgate_batch17.json` with the gate's elapsed seconds; R3c skipped the recount and batch17 does not.
**N4 -- no grant order (`OG-gv-1`, `OG-gm-1`) starts before this ledger reads CLOSED and the `masterwide` block reads clean from the DEPLOYED tree.**
**N5 -- the CLOSED time and live sha go to `2.0.0_SA_COO~O` at once; the landing (Phase C) needs a note commit on the landing branch, since an empty merge cannot be graded; counts and hashes only in every record.**
**N6 -- the read-back records the service's resident memory at the restart and each minute (as R3c's did); I take one further read myself, and a level above R3c's 881 MB or growing after 30 minutes is a row, not a trigger.**

Gate limb: none graded (a signed half is a file in lane `TREE_DELIVERABLES`). Push state: LOCAL.
