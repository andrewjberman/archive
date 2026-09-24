# AMGT_CORPUS round 2 -- never-widen pair, the crosswalk RE-MINT after the Z-S16 builder remedy (one `crosswalk.main --write-pool`, no vendor call)

Two halves. The COO half is below, signed by `2.0.0_SA_COO~X`. The CTO half is owed by `1.0.0_SA_CTO~Z` (R-59: a SECOND half,
because the first pair is bound to a before-state the fire changed) and lands in that seat's own folder with a pointer here.
The re-mint is NOT run until both halves are signed at these bytes and `closer/amgt-peers-z-20260924` @`a2b84a1b2a` has
drained onto CLOUD with `lib/research/identity/crosswalk.py` byte-identical to that commit.

## COO HALF -- `2.0.0_SA_COO~X`

**Sources:** row `AMGT_CORPUS-Z-S16` @`574a7e8755` (ARMED; conditions (1) builder resolves-by-folder, (2) ONE re-mint under a
fresh pair, (3) re-ingest reads 53 resolved); CTO R-59 (chain adopted; the re-mint's blast radius is NOT the first pair's);
`2.0.0_SA_COO~Z` msg 25469 (condition (1) BUILT @`a2b84a1b2a`, identity tests 97 of 97, live acceptance records 274 -> 254,
UNRESOLVED 60 -> 40, MEASURED 214 unchanged, multi-claimed forms 20 -> 0); the first pair (`NEVER_WIDEN_ROUND2_D5_REFIRE_HALVES.md`
@`4bbd43777c`, CTO half @`9a6472e58f`), whose writer census and reader census this half re-uses only where re-measured below.
Measured read-only by the issuer 2026-09-24 11:5xZ.

### THE ACT

ONE run, by this seat on this terminal, from the shared tree at a CLOUD HEAD that contains `a2b84a1b2a`:

    python -m lib.research.identity.crosswalk --as-of 2026-09-24 --write-pool

`crosswalk.main` (`:1197-1230` @`a2b84a1b2a`): reads the retained universe/v1 input ONCE (`load_identity_universe`), builds
ONE document (`build_crosswalk` with the universe input and `registrations.json` from disk, 28 rows @`b7819604e0`), serialises
it, and calls `write_pool(key, payload, document=document)` ONCE -- schema-validated BEFORE any put. **No Bloomberg call exists
on this path** (`main` imports no client; the 20 identities are already in `registrations.json` and raw-landed), so
C-NO-VENDOR-CALL is not touched. The call shape is named because the one-put property of `add_security` is call-shape-bound;
`crosswalk.main` puts once by construction (one `write_pool` call site at `:1223`).

### THE PURPOSE NUMBER, named first (the lesson of the first pair)

The act exists to move **UNRESOLVED 60 -> 40** and `resolved_folders` 0 -> 20 in the served document, and downstream to move
`ingest --write`'s `resolved_folders 33 -> 53`. If UNRESOLVED reads 60 after the put, the act FAILED at its purpose whatever the
blast-radius numbers say, and this seat reports that before anything else.

### BLAST RADIUS -- the act's own write set

1. **ONE conditional put on ONE key, `s3://opal-data-harvest/crosswalk/v1/2026-09-24.json`** (`write_pool` `:1125-1188`:
   `head_object`, `put_object` with `IfMatch <current ETag>` only when the stored `document-sha256` differs, read-back that
   RAISES on mismatch). No raw bronze landing (no vendor response to land), no registrations.json change, no other key.
2. This seat's deliverables: the run log and the probes.

### WRITER CENSUS -- N = 2, re-measured on the CHANGED file

`crosswalk.py` changed at `a2b84a1b2a` (1,205 -> 1,243 lines), so the census is re-run on THOSE bytes: `write_pool(` is
called at exactly ONE site in the file, `main` `:1223`; `add_security._mint_pool` (`add_security.py:379`, unchanged since
`a125f8be8b`) is the second writer. The first pair's unscoped sweep (1,009 hits / 72,661 files; every non-`lib/` hit a reader,
a bundle copy, a Get/List-only Terraform grant, a fixture or a log) is NOT re-run: the remedy touched one file, read above.
By branch: the producer bytes live on `closer/amgt-peers-z-20260924` until `0.0.0_AB_MSTR~Z`'s drain; the act runs ONLY on
CLOUD after `git show HEAD:lib/research/identity/crosswalk.py` hashes equal to `a2b84a1b2a`'s.

### BEFORE-STATE -- the EXACT key (probe-4, 11:51:30Z; re-measured immediately before the act)

`versions 23, delete markers 0, latest VersionId tlVd1Cqrlhk93VurXE2jThhPNToWm0wA (11:11:02Z, the fire's put), size 583272,
ETag "0ea189e85079ab9a34eef5ecd05026c0", sha256 223264e2d0fd3caa..., metadata equal, denominators records 274 MEASURED 214
UNRESOLVED 60 registered 27 universe_registered 158`. Evidence `evidence/remint_probe4_before_*.json`.

### EXPECTED OUTCOME -- read from the producer's own rule, every branch, with the document PRE-BUILT

This seat built the document IN MEMORY on the branch bytes through `add_security._build_document` (the same `build_crosswalk`
call `main` makes, same inputs: universe/v1/2026-09-16.json, registrations 28 rows): **records 254, MEASURED 214, UNRESOLVED
40, registered 27, resolved_folders 20, universe_registered 158; 521 association forms, 0 multi-claimed; 20 records carry
`resolves_coverage_record`; ASML_NA_Equity present; folder 'UBS' has ONE record; payload 560,881 bytes, sha256 572edb49f9d7aa6f...**
- **put performed (the expected branch):** exactly ONE new version (24), `IfMatch` on the ETag above; the served document is
  the pre-built one (same bytes if the inputs are unchanged at run time -- the universe input and registrations.json are
  re-read by the act, so the sha is expected, not promised); MEASURED 214 -> 214, records 274 -> 254 (20 UNRESOLVED twins
  replaced in place, no key lost: the 214 MEASURED keys are a superset check this seat runs after), UNRESOLVED 60 -> 40.
- **already-current:** if the stored `document-sha256` already equals the payload's (someone minted the same bytes first),
  `put_performed` False, no version, the key byte-identical; the OK line says `already-current`.
- **schema refusal:** `write_pool` validates `document` first and RAISES with nothing put (crosswalk.schema.json admits
  `resolved_folders` at `a2b84a1b2a`; a mismatch is a refusal, never a put).
- **read-back mismatch:** raises AFTER the put; the new version is served; rollback below applies.

### PER-KEY ROLLBACK

`copy_object` from VersionId `tlVd1Cqrlhk93VurXE2jThhPNToWm0wA` onto the same key, then read back size 583272 / sha256
223264e2. No version is deleted. Triggers: more than one new version; MEASURED after != 214; any of the 214 MEASURED keys
absent after; UNRESOLVED after not 40 (a purpose failure is ALSO a rollback trigger here, because a document that moved the
count without resolving the folders is the shape Z-S16 names); any write outside the one key. On a trigger this seat rolls back
in-session, files a citing row, and reports.

### THE DISCRIMINATOR (this seat's)

`refire_versions_probe.py` before and after: versions 23 -> 24 exactly; `latest_version_id` changes once; denominators read
records 254 / MEASURED 214 / UNRESOLVED 40 / registered 27; then the superset check of the 214 keys against the prior version's
body; then `ingest --write` reading `resolved_folders 53` (the purpose, measured on the consumer).

### NOT COVERED

- any `add_security` run, any Bloomberg call, any `--batch` re-run (the same document could be minted that way; this half
  names `crosswalk.main` and only it);
- a second re-mint; any other dated key; `universe/v1/`; any delete;
- the re-ingest and the production sequence (drain duties that follow; bronze writes are write-once and not served);
- any reader-side claim about a screen.

**Signature (COO):** signed `2.0.0_SA_COO~X`, 2026-09-24, at the commit of this file. Bound to the before-state above and to
`crosswalk.py` @`a2b84a1b2a`; a different `latest_version_id` at run time, or different producer bytes on CLOUD, re-opens
this half.

## CTO HALF -- `1.0.0_SA_CTO~Z`

(owed; lands in that seat's folder, pointer to be added here)
