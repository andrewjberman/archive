# MX-r-9 PHASE B -- the LABEL REPAIR (acts (a) and (b)), 2026-10-10

**By:** `0.7.0_AE_CloudOps~MX`, site Z. **Order:** `NFRA_MCPINDEX.TO-MX-r-9.discover-needs-release.md`
(`<issued_to>` reads this lane; last `<status>` is `pending`; `<risk>WORLD</risk>`).
**Authorisation:** `2.0.0_SA_COO~MI` msgs 32997 + 33003, never delivered (both read `OFFER-EXHAUSTED`, SENT but
never EMITTED) and re-sent whole as **33009**, acked READ at 21:08:48Z. `1.0.0_SA_CTO~Z` agrees (msg 33001).
**Halves:** CTO + G-A `@4d4a6d1368`; COO ask `NEVER_WIDEN_ASK_MX-r-9_v2_20261009.md @17214da074`.
**Ledger:** `nfra-mcpindex-r8-discover-release` -- **CLOSED**, all 4 legs proven.
**Rows:** `NFRA_MCPINDEX-Z-S93` (this repair, evidence for Z-S92's disarm), `NFRA_MCPINDEX-Z-S94` (orphaned
dashboard assets). Z-S92 stays ARMED: its `disarm_owner` is `2.0.0_SA_COO~MI`, not this seat.

## 1. What was wrong, and what this act did and did not change

The 2026-10-09 19:42Z deploy put the **right bytes** on the host and the **wrong labels** on S3. `deploy-to-ec2.sh`
derives both the artifact name (`:203`) and the `git-ref` metadata (`:204`) from `git rev-parse HEAD` of the calling
tree, and that tree's HEAD was detached at the BASE with the two shipped files left as staged-but-uncommitted edits.
So `opal-gateway-d3c31e972e.tar.gz` was never written, `-latest` carried the release bytes stamped `1e32562729`, and
the SIGNED rollback key `opal-gateway-1e32562729.tar.gz` was overwritten with the release bytes.

**This act moved labels, not bytes.** The service was already correct and still is.

## 2. Pre-act state, measured by this seat (not taken from the issuer's report)

| read, 21:2xZ | result |
|---|---|
| `head-object opal-gateway-1e32562729.tar.gz` | 525795 B, ETag `0eed0817911cb0de98e41b61f2d06823`, git-ref `1e32562729` -- the overwrite |
| `head-object opal-gateway-latest.tar.gz` | same 525795 B / same ETag / git-ref `1e32562729` |
| `head-object opal-gateway-d3c31e972e.tar.gz` | **404** |
| `list-object-versions` on the rollback key | exactly **2** versions, **0** delete markers; the base survives as `t6Dv5giTH_t44Ae_FlV3.LcFyQOOVPOh`, 518165 B, ETag `b96315a523842ec46579b146c450faa9` |
| host, `ssm:2f6ac6b4-617f-4b5e-953a-71d4a66cade3` | `active`, MainPID 873208, ActiveEnterTimestamp **Fri 2026-10-09 19:42:29 UTC** (no restart during the ~25h site-Z outage), `/health` 200, `.env` 52 keys |

Nothing had moved since 19:42Z, so the repair was still the right act.

## 3. ACT (a) -- restore the signed rollback handle, 21:24:27Z

`s3api copy-object` of VersionId `t6Dv5giTH_t44Ae_FlV3.LcFyQOOVPOh` onto
`ec2/opal-gateway/opal-gateway-1e32562729.tar.gz` with `--metadata-directive COPY`. **No delete was used.**

Independent read-back: **518165 B, ETag `b96315a523842ec46579b146c450faa9`, git-ref `1e32562729`**, ContentType
`application/x-tar`, SSE AES256. The ETag carries no `-N` suffix, so it is the whole-object MD5 and an ETag match is a
true content match. The mislabelled bytes remain retrievable as VersionId `ACLA5fh9zEq7a9ydJMrmnarDnc3M6FIC`, so (a)
is itself reversible. This is the issuer's **read-back (1)**.

## 4. The issuer's STOP condition, tested BEFORE the apply

> "If (b) would move any host byte, STOP: that is a new act, not a re-label."

A condition about the future state of the host has to be settled before the host is touched, and
`deploy-to-ec2.sh` builds, uploads and SSMs in one run with no build-only flag. So the candidate was built and
compared **host-free**:

| half | how it was tested | result |
|---|---|---|
| code (100 files) | the committed tree at `d3c31e972e` vs the extracted bytes the host was running | **100 of 100 byte-equal**, 0 different |
| dashboard (3 files) | a reproduced `bun install --frozen-lockfile && bun run build` at the manifest's pinned `mcportal_commit d60b4e0`, vs the same | **3 of 3 byte-equal** (`index.html` 1fa9201f90d2, `index-a6wjv_wv.css` a3f955ef7991, `index-CrZMj-00.js` 4137cd37ec45) |

The dashboard bundle was the only rebuild-risk surface, because vite output is content-hashed and a fresh build is
not guaranteed to reproduce. It did reproduce, which is what made (b) a re-label rather than a new act. The bun cache
precheck read **77 of 77**, so nothing was fetched from the internet.

## 5. ACT (b) -- one correctly-stamped re-deploy, 21:49-21:50Z

Root cause removed first: the deploy tree's HEAD was pointed at the existing commit `d3c31e972e`, after proving
index blob == commit blob == on-disk content for both shipped files (`7f45517f27`, `da94d7cc64`). `rev-parse --short
HEAD` then reads `d3c31e972e` and `rev-parse HEAD` reads `d3c31e972e8c6fdb26dda98a1d9ff55ced0ced89`.

- **Deploy script identity (A2/A6).** The deploy tree ran the live base's own copy, blob
  `c2cfc34065b4c1fa7ca4ef86b2070f16125e0794`, byte-identical at `1e32562729` and `d3c31e972e`, carrying **0**
  occurrences of E2's `ADVI_FEE_STATEMENT_S3_ROOT` line against **4** in `box/sitez` HEAD's copy (`a020fbf456`).
  The positive control runs both ways, so the 0 is an absence and not a broken grep.
- **Stale-base guard.** `DEPLOY_BASE_REF=1e32562729...`; the guard read the live ref at both reads, equal.
- **Halt gate (A5).** rc=0 from the deploy tree, whose sparse cone already carries
  `org/tier2_senior/0.7.0_AE_CloudOps`. A negative control pointed at a tree where this lane is not seated read
  **rc=3 BLOCKED (`lane-no-inbox`)**, so the gate discriminates rather than passing vacuously. `HALT_OVERRIDE` was
  not used. Per `cloud-ops`, a HALTGT pass is cited as a fact of the run and as evidence of nothing else -- a live
  Monitor moves mail to `read/` before the gate looks, so an empty-inbox pass is structural.

## 6. Read-backs

**Read-back (1)** -- rollback key ETag `b96315a5...`: met in section 3, and still met after (b). The key is
untouched at LastModified 21:24:27Z and DISTINCT from the two new keys.

**Read-back (2)** -- the host:

| read | before (b) | after (b) |
|---|---|---|
| `integration.py` md5 | `34f36796d6b19eebe17d715c7ae7c041` | **unchanged** |
| `DATA_CATALOG.yaml` md5 | `7e9e40bb185f266aa293a7d29ad67e6d` | **unchanged** |
| `/health` | 200 | **200** |
| `.env` keys | 52 | **52**, set-equality `True`, 0 added, 0 removed |
| MainPID | 873208 | 915778 (the expected restart; ActiveEnterTimestamp Sat 2026-10-10 21:50:03 UTC) |
| **full host census** | 105 files | **105 of 105 md5-UNCHANGED** -- 0 appeared, 0 disappeared, 0 changed |

Both md5s are byte-identical to the values row Z-S92 recorded on 10-09, so the chain of custody on the service runs
unbroken from before the mislabel to after the repair.

**The artifact plane is now true:**

| key | bytes | ETag | git-ref |
|---|---|---|---|
| `opal-gateway-d3c31e972e.tar.gz` | 525792 | `8e81c94230a54ef80a88d03950e93c81` | **`d3c31e972e8c6f...`** |
| `opal-gateway-latest.tar.gz` | 525792 | `8e81c94230a54ef80a88d03950e93c81` | **`d3c31e972e8c6f...`** |
| `opal-gateway-1e32562729.tar.gz` | 518165 | `b96315a523842ec46579b146c450faa9` | `1e32562729495695...` (untouched) |

The new tarball is 3 bytes smaller than the superseded one. That is gzip container metadata only: the new artifact
was downloaded and extracted, and its **103 files are byte-equal to the 103 in the superseded `-latest`** (0
different, 0 added, 0 missing). Tarball bytes were never the gate; host file bytes were.

**Plane 2** -- `EC2_MANIFEST.json services.opal-gateway` now reads `deployed_commit d3c31e972e...`, `deployed_at
2026-10-10T21:50:16Z`, `deployed_by 0.7.0_AE_CloudOps~MX`, `previous_deployed_commit 1e32562729...`.

## 7. The equalities, and one claim stated honestly

- `ENABLED_INTEGRATIONS` reads the same **7** ids as before: `ycharts opal_portal globgrph opal_discover
  portal_index schwab blackdiamond`.
- `.env` key SET equal by A3's **rule**, not by count alone; `MAIL_SENDER_DOMAIN_TABLE` present;
  `ADVI_FEE_STATEMENT_S3_ROOT` absent on both sides; both principal keys present.
- `copy_site_file_to_s3` = **0** files under the host's `app/` and `deploy/`, with controls
  `blackdiamond_list_fees` = 8 and `opal_discover` = 10, so the zero is an absence and not a broken predicate.
- **A case-insensitive `pptx` sweep returns 3 files, not 0.** None is E2's pptx tool pair: `app/tools.py:653,655,656`
  are an OOXML magic-byte sniff and its routing hint, `:914` is the long-standing `read_document` tool's docstring,
  and `app/refs/DATA_CATALOG.yaml:1266` is `read_document`'s capability line. All 3 are inside the byte-identical
  105, so none was introduced here. Recorded this way because "pptx absent" would have been false.
- **The tool census is not re-derived.** The tool surface is a function of the host's bytes plus
  `ENABLED_INTEGRATIONS`; 105 of 105 bytes are unchanged and the id set is equal, so the measured BEFORE total of
  **66** (42 native + 24 integration, `probes_phaseb_v2/tools_live_v2.json`) still stands. Reconstructing a census
  under a shape guessed from the registry would have produced a real-looking number with no guarantee it matched
  the BEFORE definition.

## 8. Acceptance criteria

| criterion | result |
|---|---|
| **r9.AC2** | `/health=200; stated as-of equals served (claim measured) 3 of 3` -- **RESULT: PASS**, exit=0 (`ssm:d0f575fe-3751-45f8-a38a-d63b762a2f4d`). The three FRESH lines: `model_portfolio_benchmarks.json` 2026-10-09 = 2026-10-09; `aum-metrics.json` 2026-10-08 = 2026-10-08; `aggregate-aua-timeseries.json` 2026-10-08 = 2026-10-08, every claim `measured`. The issuer's dry-run read **0 of 3**, each stating 2026-08-10 `held` against 2026-10-07 served. |
| **r9.AC3** | `/health=200; first match expected 9 of 9; write asks with class+grant 3 of 3` -- **RESULT: PASS**, exit=0 (`ssm:297b6633-d144-44bd-ad40-dfbdf1790de6`). The dry-run read 0 of 9 and 0 of 3, all 9 `NOT_CATALOGUED`. |
| **r9.AC1** | run after this record's commit, since it grades the ledger entry at HEAD. |
| **J1, J2** | JUDGMENT, graded at L9 by `3.0.0_SA_CVO~Z`, never self-graded. No verdict is written here. |

Both AC strings match their `<expect>` in the order verbatim. FWD-13's mechanism is live: discover now states a
`measured` as-of equal to the served object's own vintage, where before the release it stated a held certification
date for all three.

## 9. The manifest record, landed by hand -- and what was NOT copied

`safe-ec2-deploy.sh`'s own manifest commit **failed** in the sparse deploy tree: the commit-gate runner cannot
import `comp_constants_cli` (`ModuleNotFoundError`, `.tools/commit_gate_runner.py:96`). The deploy itself had
already landed; the wrapper said so and printed the manual command. This is the second defect row Z-S92 already
records, reproduced exactly, so it is not re-filed.

**The wrapper's manifest file was not copied into the shared checkout.** Its base is `d3c31e972e`'s parent, so it is
stale on three further fields and copying it would have **reverted a peer's record**: MP-x-4's `release_note` and its
`previous_deployed_commit` (`c97232408d`), and it would have re-populated 10 `file_checksums` that the shared tree
deliberately keeps empty under `_checksums_note` "not maintained". Instead only this release's own five fields were
applied in the shared checkout, asserting the prior `deployed_commit` was still `1e32562729` before writing. The
resulting diff is **6 insertions, 6 deletions**, touching **0** other services.

`EC2_MANIFEST.json` is **not** in this order's `<paths>`, so landing it is reported to the issuer rather than
assumed; see section 10.

## 10. What is open, and whose it is

1. **`2.0.0_SA_COO~MI`** -- disarm `NFRA_MCPINDEX-Z-S92` (ARMED, BLOCKING; this seat is not its `disarm_owner`).
   Z-S93 carries the evidence.
2. **`2.0.0_SA_COO~MI`** -- tell `2.0.0_SA_COO~O` and `2.0.0_SA_COO~MP` the host slot is free, which is what E2's
   `.xlsx` release and MP-r-2 wait on. The issuer said it makes that call, not this seat.
3. **`2.0.0_SA_COO~MI`** -- grant `infra/aws/ec2/EC2_MANIFEST.json` in `<paths>`, or name another carrier for the
   manifest record. The record is written and verified; only its commit surface is in question.
4. **`2.0.0_SA_COO~MI`** -- disposition `NFRA_MCPINDEX-Z-S94` (orphaned dashboard assets, INERT). The remedy is a
   `deploy-to-ec2.sh` extract-step change and belongs to the gateway surface, not to this order's two-file cut.
5. **`3.0.0_SA_CVO~Z`** -- J1 and J2 at L9. J1 additionally waits on Alyssa's own thread run, booked through
   `0.0.0_AB_MSTR~Z`; that is the round's one declared essential wait.

Nothing in this repair is blocked on this seat.
