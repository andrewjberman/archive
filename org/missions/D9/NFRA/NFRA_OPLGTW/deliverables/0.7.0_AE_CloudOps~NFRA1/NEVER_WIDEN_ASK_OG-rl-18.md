# NEVER-WIDEN ASK -- `OG-rl-18` -- the round-47 seventeenth batched release (`batch17`): the MASTER-WIDE Schwab scope code (`OG-rt-1`), the master-admin exemption on the legacy `/callback` consent branch (`OG-ed-1`), the owner-gated people-access routes (`OG-mp-1`) and the served catalog (MCPINDEX candidate e); ONE code release plus one manifest key

Applier: `0.7.0_AE_CloudOps~NFRA1`. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-rl-18.round-47-seventeenth-batched-release-the-master-wide-schwab-scope.md` (GO for Phase A: the issuer's ferry 20261021T0826Z; method `OG-rl-17`'s). Source: the CTO's round-46 analysis rank 6 and Andrew-direct ~17:2xZ 10-19 ("there shouldnt be a persisted list").
**Phase A deploys and applies NOTHING in any form**, writes no SSM parameter and no store item. The release is LOCAL: branch `rel-nfra-oplgtw-batch17` in `C:/tmp/og-rel-batch17` (not pushed).
**The release signed:** `release_sha` `7863a9d65b11170a30d663d76834104eadd6ce6a`, cut on `base_sha` `2923d1ee99a014dab841b181af08ca67c643705e` = R3c's release = the live ref read on the host (`live_ref_host`, equal); from `trunk_sha` `daff5d69d7ce17adc5e751812f811e9d6a863572`. `6575999df5` (dell1's harvest release) is an ancestor of the base; dell1's four harvest files are byte-equal. **Phase B is not before 2026-10-22 06:00Z and only on the issuer's GO naming all three halves signed at `release_sha`**; the base is then re-read on the host (it must still equal `base_sha`, else STOP and re-cut).
Records: `W/rl18_release.json`, `W/PHASE_A_OG-rl-18.json`, `W/rl18_pa/{host,tests,sentinel_scan,live_named_reverse}.json`, `W/rl18_take.py`, `W/rl18_host.py`, `W/rl18_probe_*.py`, `W/rl18_tests.py`, `W/rl18_sentinel_scan.py`, `W/rl18_phasea.py`, `W/rl18_ask.py`.

## 1. The diff, by file (TWELVE gateway files and ONE manifest key; 13 paths over the base)

| file under `infra/aws/ec2/opal-gateway/` | lines | release blob | cell and reading |
|---|---|---|---|
| `app/data_entitlement.py` | +28 -6 | blob `881da34cda89` | OG-rt-1: WHOLE from trunk. The parser accepts exactly the one-element list `["*"]` for a granted master (the sentinel, `MASTER_WIDE`), `is_master_wide`, `check_scope` admits any non-empty account list for such a master; OG-ed-1: `email_denial` exempts the master-admin tier for `route_class` consent |
| `app/account_ref.py` | +39 -8 | blob `5036d306e238` | OG-rt-1: WHOLE from trunk. `candidate_accounts` and `AccountsUnavailable`; `accounts_of` threaded through `_resolve`, `resolve_refs`, `resolve_ref` |
| `app/integrations/schwab/integration.py` | +64 -8 | blob `144474475ee5` | OG-rt-1: trunk's WHOLE blob (the order's eight hunks, 11 at zero context) **over R3c's hybrid**: `account_filter_for`, the master-wide `account_count` 'all', `_master_accounts`, the two resolver call sites |
| `app/server.py` | +3 -2 | blob `be23ac0d2371` | OG-ed-1: WHOLE from trunk. The `/callback` branch passes `route_class=data_entitlement.CONSENT` |
| `app/token_broker.py` | +1 -1 | blob `2a8084538fcd` | OG-ed-1: WHOLE from trunk. `redeem_consent` passes the same class on the second check |
| `app/admin_api.py` | +2 -0 | blob `f5896882e533` | OG-mp-1: WHOLE from trunk. One import and one spread, `*admin_people_access.routes` |
| `app/refs/DATA_CATALOG.yaml` | +2656 -555 | blob `b71d79282d6a` | the served catalog: MCPINDEX candidate e, md5 `03d2dbbae1f07b8d4fa5f0eaa73355d6`, trunk commit `1ade26b4602` (data, not code) |
| `tests/test_og_rt1.py` | +158 -0 | blob `81e7609f81d6` | OG-rt-1: new, source only |
| `tests/test_og_ed1.py` | +160 -0 | blob `9d6f93d4d97b` | OG-ed-1: new, source only |
| `tests/test_scoped_consent_r253.py` | +1 -1 | blob `c5afd5611f68` | OG-ed-1: one assertion |
| `tests/test_login_admit_r24.py` | +1 -1 | blob `09991ea542d5` | OG-ed-1: one assertion |
| `tests/test_og_mp1.py` | +146 -0 | blob `cd3041302b5d` | OG-mp-1: new, source only |

**The manifest:** `infra/aws/ec2/EC2_MANIFEST.json`, +1 -1: exactly ONE key, `services.opal-gateway.mcportal_commit`, from `21ad40432cae0d09c5ab9d806307944baaf45cb9` (batch16's pin) to the FULL hash `a577f99afc81df4a42c1740c78cf58270c8991e5` (mcportal DEV, `ls-remote` read by `2.0.0_SA_COO~MP` and by the issuer). That is a change of what the dashboard bundle serves: the `/opalgateway` page's People panel and its audit list, and two render fixes (FWD-28, FWD-29). Nothing else in the manifest moves (the check requires exactly that one changed key).
Barred and absent (the check counts them at 0): the deploy script, the unit, every `deploy/` file, every `.tf`, every other file; the batch16 files are in the base and unchanged.

## 2. The widening, stated plainly: FOUR

1. **The Schwab scope code adds a grant shape that no stored grant uses.** A grant may now say `accounts[master] == ["*"]` (a master-wide master). **It widens nothing until a later grant order writes `["*"]`, and that order (`OG-gv-1`, `OG-gm-1`) is its own never-widen.** The store holds 0 such records now (a read-only strong scan of the 29 POLICY records, 9 of them with a scope). What the code will do for such a grant: read the master's own data without a stored account list (no account filter); resolve account references against the master's CURRENT accounts from the newest complete `dim_position` snapshot (`SchwabService._master_accounts`, one rows query on the account column through the same engine path, cached per master for the life of that snapshot's digest, the ids never logged or returned); a master-wide grant without a complete `dim_position` snapshot is refused fail-closed (`scan_incomplete`; the resolver maps an unreadable list to its UNAVAILABLE denial).
2. **The legacy `/callback` consent branch now lets a MASTER ADMIN (exactly one `MASTER_ADMIN_EMAILS` entry) complete the sign-in although an `email_deny` record names that email (before: 403).** No other email's verdict changes: **a non-admin with a deny record still gets 403**, an unreadable store still fails closed 503 for everyone else, an email that merely looks like the admin's still gets 403, and the master admin with no class keeps today's verdict. The browser routes already exempted the tier (`OG-en-14`); the CTO's half of `OG-gv-1` named this (option 2, msg 36207). **The exemption is live at once, not inert.**
3. **Two OWNER-GATED routes answer where they answered 404** (`OG-mp-1`, the CTO's ferry 17:30Z): `GET /api/admin/people/{tid}/{oid}/access` reads one person's `person_access` record (one strong get); `POST /api/admin/people/{tid}/{oid}/access` invokes the grant-writer Lambda and relays its verdict. **BOTH `admin_people_access` routes, `GET` and `POST /api/admin/people/{tid}/{oid}/access`, sit behind `owner_gate.owner_only`** (the CTO's ferry 23:03Z, msg 36245: that is W1' enforced at the gateway); with no verified identity both answer 401 (probe `mp1.AC1`, 4 of 4). **The routes are owner-gated and the gateway writes nothing itself**: the POST only invokes the Lambda. No new tool, no `tools/list` change, no IAM change.
4. **The catalog.** `app/refs/DATA_CATALOG.yaml` becomes MCPINDEX candidate e (md5 `03d2dbbae1f07b8d4fa5f0eaa73355d6`; the live and batch16 files read `bdfee515ec34`), so the discovery and catalog tools answer with six corrected link routes and with index pairs for the five `client_*` tools. No tool, no `tools/list` change, no IAM, no env key; the three code misroutes stay in round 48.

**The RELEASE-ORDER condition:** this code must be live **before any grant names** the sentinel `["*"]`: an OLD gateway reads a stored sentinel as `Malformed` and would deny that principal's whole Schwab access. So the grant orders start only after this ledger is CLOSED.
**The listing note covers BOTH roles** (the CVO's note on `OG-rl-19`, msg 36250): the data role's `ListBucket` on `schwab/49financial/silver/<table>/*` also exposes other masters' key names once they land, and the catalog role's prefix-conditioned list does the same under its prefix; a second master's move re-reads both. This release changes no IAM and adds no listing; the note is stated so the signers read it with the master-wide grants that follow.
**R3c hunk survives** (the CVO's note 2, shown by the hunk itself): R3c's change to `integration.py`, the function-local `from .catalog import key_in_data` and the condition `or not key_in_data(key, self._contract) or not version` in the source-reference check, is present in the release blob (lines 198 and 204 of `7863a9d65b11:infra/aws/ec2/opal-gateway/app/integrations/schwab/integration.py`); the release's diff against the live ref does not touch those lines.
**The hybrid sentence** (the CTO's condition 2 on `OG-rl-19`, msg 36247): this release takes trunk's WHOLE `app/integrations/schwab/integration.py` **over R3c's hybrid** (the base blob plus the one `OG-sk-2` hunk), adding `OG-rt-1`'s eight hunks; trunk's blob already carries the `OG-sk-2` hunk, so nothing of R3c is lost.

## 3. Phase A measurements (every host run in a FRESH process under the cgroup hard guard `oom_score_adj_1000_cgroup_memmax_1400mb`; the running service untouched: PID `49621` before and after, `NRestarts` 0; the scratch copies removed)

- **(a) The probes**, the python of `rt1.AC1`, `rt1.AC2`, `ed1.AC1` and `mp1.AC1` VERBATIM, each in one fresh process on the candidate stage on the host (the six app files laid over a copy of the service's tree, each equal to the release blob; the fixtures `ops/schwab_entitlement_admin.py` and `tests/test_email_deny.py` from the release tree): labelled lines ok: **rt1.AC1 11 of 11, rt1.AC2 11 of 11, ed1.AC1 7 of 7, mp1.AC1 4 of 4**.
- **(b) Explicit scopes unchanged: true.** One scope with two explicit masters (eight-digit fixture ids built at run time), parsed by the live ref's code and by the candidate's; `check_scope` for an in-list id, an out-of-list id, an empty list, an in-list id on the second master and a mixed list; the account list the resolver builds and the Schwab account filter; `scope_summary`'s `account_count`: all equal between the two.
- **(c) No stored sentinel:** 0 (strong read, counts only).
- **`bash -n deploy-to-ec2.sh`: ok; `--preflight-only`: PREFLIGHT OK; host-shaped import check:** 6 of 6 changed app modules import from the candidate scratch tree with the service's own `lib/` and `.venv`; the scratch registry counts 120 tools for both the candidate and the live ref: `tools/list` does not change.
- **Tests, release tree.** Named set (34 files, 3 new: the three new tests, the two edited, the entitlement, account-reference, grant-admin, owner-gate, contract and Schwab files): forward 235 passed, 30 failed; reverse 255 passed, 10 failed. **The failing count of this set depends on the order at the BASE as well** (32 forward, 12 reverse), and **every red of the release in either order is also red at the base in that order: new reds 0**. Window set (68 existing `test_og_*` files green at the base): 301 passed, 0 failed in both orders. With trunk's standards copy overlaid (uncommitted, restored to the live ref's bytes after: True) the two contract-copy tests that read red at the base pass.
- **Full suite, per test id** against a tree at the live ref (the same sparse cone and invocation): release 79 failed, base 79 failed; **only in the release: none; only at the base: none** (none: the two failing sets are identical per test id (79 of 79); the difference between the runs is the release's extra passing tests (the three new test files)).

## 4. The order of acts (Phase B), recorded in `W/CODE17_SERVED.json`

Window **2026-10-22 06:00Z to 06:45Z** (not before 06:00Z and not before one full day after `OG-rl-17`'s ledger closed, 2026-10-21 06:44Z), abort line `/health` 200 by 06:30Z; announce to `0.0.0_AB_MSTR~Z` (the gateway restarts once, about 16 seconds). Ledger `nfra-oplgtw-gateway-release-batch17`, entry AND sentinel first. THE HALT GATE: the pending inbox read to zero before the window, recorded in `W/haltgate_batch17.json`. Deploy from `C:/tmp/og-rel-batch17` through `safe-ec2-deploy.sh` with `DEPLOY_BASE_REF` the live ref read on the host, no `HALT_OVERRIDE`; then the unarmed served read, the 27-tool read, the md5 walk, the 30-minute read-back, the host clock and failed units read BEFORE the ledger closes, the `masterwide` block (the sentinel parses in the DEPLOYED tree, the explicit-scope comparison against the deployed code, the store re-scanned), the journal `POST /mcp` count and the audit-lake count for ONE window, then `rl18.AC2`, the landing.

## 5. Both branches

- **An explicit-list scope behaves as before** (probe (b), equal answers); **a sentinel scope parses and filters on nothing** (probes rt1.AC1 and rt1.AC2). Both branches are measured on the host in Phase A, and the explicit one is read again from the deployed tree in Phase B.
- **No stored sentinel exists before the grant orders**, so no principal's access changes by the code alone; the `/callback` exemption and the two routes are the only behaviours live at once.

## 6. Rollback

Redeploy the live ref's tree (the wrapper's pre-deploy tarball; `DEPLOY_BASE_REF` the live ref). **With NO stored sentinel the rollback is clean**, which is why the grant orders wait for this ledger to close; a sentinel written before a rollback would be read as `Malformed` by the old code. The rollback goes through the same halt gate, so the same empty inbox keeps it short.

## 7. Triggers (any one: roll back as section 6)

`/health` not 200 in 60 s; a tool of the 27 not answering; the `.env` key count not 65; `tools/list` changing from 103; md5 beyond the twelve files; host memory above 85 percent; `NRestarts` above 0; the marker not equal to the release; a Schwab tool answering differently for the explicit-list grants read in Phase B; any `audit-lake WARN` line during the read-back.

## 8. Gate lines

process-wide state this change touches: No process, logger, signal, thread, socket, environment key or global config changes, and no import-time side effect is added (I opened the six app diffs whole). app/data_entitlement.py (read per request by every Schwab tool and by the dispatch chokepoint's tool_denial): one module constant MASTER_WIDE, one constant CONSENT, two plain functions (_master_accounts, is_master_wide), the parser now accepts exactly the one-element list ["*"] for a granted master, check_scope admits any non-empty account list for a master-wide master, and email_denial exempts the master-admin tier for route_class consent. app/account_ref.py (the resolver): one exception class, one function (candidate_accounts) and an accounts_of keyword threaded through _resolve, resolve_refs and resolve_ref. app/integrations/schwab/integration.py (the Schwab filter helper): one function (account_filter_for), one method (_master_accounts, with a per-master cache keyed by the snapshot digest, created in __init__ of the service object, not at import) and the call sites that use them. app/server.py and app/token_broker.py: the consent class passed at two call sites. app/admin_api.py: one import and one spread into the route list (the two owner-gated people-access routes). app/refs/DATA_CATALOG.yaml is data. tools/list does NOT change (103, the candidate registry counts the same on the host); the stored grants are untouched (sentinel records in the store: 0).

I read: the diffs of `data_entitlement.py`, `account_ref.py`, `integration.py`, `server.py`, `token_broker.py` and `admin_api.py` whole, the people-access handler's header, `rt1.AC1`, `rt1.AC2`, `ed1.AC1`, `mp1.AC1` and `rl18.AC1` whole. No IAM, no Terraform, no SSM write, no store write, no bucket write, no env key, no deploy-script or unit edit. No account number, person's name, credential or object content appears here.

## 9. The three halves (sign ONCE, on `release_sha` `7863a9d65b11170a30d663d76834104eadd6ce6a` and this ask's sha256)

### CTO half (`1.0.0_SA_CTO~Z`)

To be signed on `release_sha` and this ask's sha256, with the widening (section 2: the master-wide shape, the exemption, the routes, the catalog), the release-order condition, the hybrid sentence and the R3c hunk read.

### COO half (`2.0.0_SA_COO~O`)

To be signed on `release_sha` and this ask's sha256, with the Phase A measurements (section 3), the order of acts and window (section 4), the rollback (section 6) and the triggers (section 7) read.

### CVO half (`3.0.0_SA_CVO~Z`)

To be signed on `release_sha` and this ask's sha256, with the process-wide state line (the verdict 35844; section 8), the widening (section 2), the listing note and the suite difference named (section 3) read.
