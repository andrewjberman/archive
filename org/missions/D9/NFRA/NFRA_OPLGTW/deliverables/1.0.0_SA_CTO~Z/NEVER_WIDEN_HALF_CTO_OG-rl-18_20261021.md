# Never-widen half (CTO) -- OG-rl-18 (batch17): master-wide Schwab scope code, /callback master-admin exemption, owner-gated people-access routes, served catalog candidate e (SIGNED)

By: `1.0.0_SA_CTO~Z`, 2026-10-21 ~10:1xZ.
Against: `deliverables/0.7.0_AE_CloudOps~NFRA1/NEVER_WIDEN_ASK_OG-rl-18.md`, sha256
`b8c6641a6e728de3e49b1c8facf9bde92118c2f7967037836bf008a8a19fdf38`. This seat recomputed it, and it is equal.
Release: `7863a9d65b11170a30d663d76834104eadd6ce6a` on base `2923d1ee99a014dab841b181af08ca67c643705e` (R3c, live).
COO half: `deliverables/2.0.0_SA_COO~O/NEVER_WIDEN_HALF_COO_OG-rl-18_20261021.md` (N1-N6). CVO half: `deliverables/3.0.0_SA_CVO~Z/NEVER_WIDEN_HALF_CVO_OG-rl-18_20261021.md` @2aeefac3b1.
Basis: Andrew-direct ~17:2xZ 10-19 (Schwab covers the full accounts, no persisted list); this seat's round-46 analysis rank 6;
this seat's OG-gv-1 half (option 2); this seat's ferry 23:03Z (W1' at the gateway); ruling @9af9c984db (serve candidate e).

## Read by this seat, at the release bytes

- **The diff:** `git diff --stat 2923d1ee99 7863a9d65b` changes 13 files, +3260 -583, the twelve gateway files and the manifest,
  exactly as the ask's section 1. No `.tf`, no deploy script, no unit.
- **(1) Master-wide shape.**
  - `data_entitlement._master_accounts` accepts exactly the one-element list `["*"]`. The wildcard beside any other entry raises
    `Malformed`.
  - `check_scope` admits any non-empty list only when `is_master_wide`. An empty list still fails, and an explicit master still
    refuses an outside id.
  - The integration raises `scan_incomplete` when no complete snapshot exists, so the path is fail-closed.
  - Inert until a grant writes the sentinel. The ask reads 0 stored sentinels.
- **(2) The `/callback` exemption.**
  - `email_denial` exempts only when `route_class in (INTERNAL_PAGE, CONSENT)` and `_master_admin_email`. That is an exact,
    case-insensitive match against `MASTER_ADMIN_EMAILS`, and an unreadable config reads "not a master admin".
  - **Measured live by this seat at 10:0xZ:** `/opt/opal-gateway/.env` sets `MASTER_ADMIN_EMAILS` with **1 entry, and it is
    Andrew's** (counts only, over SSM). The exemption therefore reaches one person.
  - Both call sites pass `CONSENT`:
    - the state's declared email, at `server.py` ~682;
    - the validated principal's email, at `token_broker.py` ~393.
  - A request that merely declares the admin's email skips only the first check. The second check binds on the VALIDATED
    email, so a different denied principal still gets 403.
- **(3) People-access routes.**
  - `admin_people_access.py:78` `access_get` and `:166` `access_post` are both decorated `@owner_only`, which is W1' at the
    gateway.
  - The POST invokes the grant-writer Lambda (MP-pd-7, live since 2026-10-20 20:23Z) and writes nothing itself.
- **(4) Catalog.** `git show 7863a9d65b:.../app/refs/DATA_CATALOG.yaml | md5sum` reads `03d2dbbae1f07b8d4fa5f0eaa73355d6`. That
  is candidate e, as this seat ordered.
- **R3c hunk.** `from .catalog import key_in_data` and `or not key_in_data(key, self._contract) or not version` are present in
  the release blob's source-reference check. The hybrid sentence holds: trunk's whole blob already carries the OG-sk-2 hunk.

## One departure from this seat's OG-gv-1 half, accepted

That half asked for the `/callback` exemption "in its own small release, BEFORE the activation". Here it rides batch17 with
three other cells. **Accepted**, because what the condition protected still holds:
- the exemption is live before any activation, since the grant orders wait for this ledger CLOSED;
- with 0 stored sentinels, a rollback of batch17 is clean and takes the exemption back to today's 403 with nothing stranded.

## Conditions

1. **Release order (binding):** no grant order writes `["*"]` (OG-gv-1, OG-gm-1, Alyssa's grant) until this release's ledger
   reads CLOSED. A rollback after any sentinel is written is NOT clean: the old code reads it `Malformed`. Such a rollback first
   reverts the sentinel grants to their previous explicit scopes.
2. **Blast radius of this act:**
   - the gateway's twelve files and the one manifest key;
   - live at once: the `/callback` verdict for the one master-admin email, the two owner-gated routes, and the catalog tools'
     answers.
   - Rollback per key: redeploy the live ref's tree; the manifest key returns to `21ad40432cae`.
3. **Phase B re-reads the base on the host.** If it is not `2923d1ee99`, STOP and re-cut; this half does not carry to a re-cut.

Signed on the ask sha256 and `release_sha` above. Any change to the ask's bytes or the release re-opens this half.
