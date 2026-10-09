# ADVI_COTBKF.TO-CB-ap-2 -- deploy the cot price writer and its pinned registry

**archetype:** DEPLOY

**Seat:** `0.7.0_AE_CloudOps~CB2` | **Issuer:** `2.0.0_SA_COO~C2` | **Round:** 42 | **Cell:** `CB-ap-2`
**Risk class:** SERVED | **Date:** 2026-10-09 | **Order at:** @376c3f2418 (AMENDMENT 2, RELEASED)
**Criterion:** `CB42ap2-AC1` -- **PASS** | **Proof:** VALID (rc=0), first pass
**Ledger:** `.../20261009T1444Z_advi-cotbkf-writer-registry-deploy-cb-ap-2-20261009_deploy_completion.md`,
opened @5a3123b734, 5 legs, CLOSED all proven.

---

## Outcome -- two keys, one of them minting

| key | prior | new | bytes | sha256 |
|---|---|---|---|---|
| `code/gold/build_canonical_prices_v2.py` | `4M4XPMtc2JCbbWi22WuxrVIaicQqPzy6` | `GAOI7tORcF7V7F0fW9NMH35bonjXEwzj` | 36,335 | `3ac0a502...7f6682` |
| `code/gold/scopes.json` | **none (404, mints)** | `7ChC4J0GgHyfm7T5VLNe4bwQulg5OB0S` | 19,210 | `13947f7f...edeaade` |

Cottonwood's price writer now resolves `source_firm` from one registry file beside it. **Rollback is the
writer copy-back alone** -- the CTO half amends the COO half on exactly this point, because an S3 delete
is Andrew's act even for a key this act minted, and the BOUNDS line "delete a key this act minted" is
struck for `scopes.json`. The prior writer does not read it, so a writer-only revert leaves no
inconsistent state.

## The census, and a wording note I did *not* escalate

Condition 1 and order step 3 both say "the deploy tool's printed key list holds exactly these two keys."
**It cannot**, by the order's own design: `safe_deploy_core.upload_plan()` on the writer returns exactly
one entry, and `scopes.json` is absent from it because the order's **own step 5** deploys that key by a
separate `put-object`. One instrument cannot report a key it does not deploy.

I proceeded, and the reason is worth stating because last time I did the opposite. On CB-aj-2 the literal
reading of condition 2 said **STOP** -- proceeding would have meant overriding a stop, so I asked. Here
the gate's trigger is "anything else means STOP", and there *is* nothing else: the total write set was
enumerated from **both** instruments -- the tool's own `upload_plan` (1 entry, the writer, 0
bundle-members, no rider) plus the one explicit `put-object` key -- summing to exactly the two granted
keys and no third. The literal text mis-attributes which instrument reports the second key; it does not
instruct a stop. Blocking a released act to ask that would be friction over a non-question.

This is the **third** condition on this project whose literal text can't be read as written (see `D2-S42`
and `D2-S60` for the class, and CB-ao-1's stale line-range gloss). No new row: no claim here is false and
no test was weakened. The drafting pattern is the issuer's and CTO's to weigh.

## Before-reads

Writer `4M4XPMtc...`, 28,290 bytes, 2026-06-12 -- unchanged, and its age is consistent with the half's
note that it predates `source_firm`. `scopes.json` **404**, and that zero carries a positive control in
the same prefix (`B_00.canonical_holdings.py` returns 67,281 bytes), so the absence is real and not a
mangled key. Repo sha256 values measured, not assumed, and both equal the pair's table.

## The writes

**Writer:** the version re-read **gated** the write -- head-object and deploy in one invocation with the
deploy behind a conditional, so a moved version exits before `safe-deploy.sh` is reached. rc 0, gate PASS,
"1 path(s) to deploy (1 script, 0 bundle-member)", three declared-for-this-layer files explicitly
`[not shipped]`. No `--allow-stale`, no bypass audit entry. Lane ADMITTED -- recorded but **not** leaned
on, since APPLY-WHO is WARN-only by ruling 106858; the authority is the CTO half naming this seat.

**Registry:** the **404 was the gate**, not an earlier observation -- the `head_object` and the `put` ran
in one script where the put is unreachable unless the key reads absent, and a `head_object` failure for
any reason *other* than absence also exits, so an unexpected error could not be mistaken for a 404.

The bytes are the blob's: `git cat-file -p 261c0cf8...` piped straight to `put_object` with **no
`json.load`/`dumps` round trip**. That matters -- re-serialising JSON can change key order, whitespace and
unicode escaping, which would move the sha256 off the signed value. Verified 19,210 bytes /
`13947f7f...edeaade` *before* the put, so a mismatch would have stopped rather than been discovered after.
`ServerSideEncryption` was read from an existing object in the prefix (AES256) rather than typed, so the
minted key matches its neighbours instead of inheriting a default.

**The window the preflight names** -- a manual silver-prep starting between the two writes would read the
new writer against an absent registry -- is now shut, both keys verified in place. Minting the registry
*first* would have eliminated it outright, since the CTO half establishes the prior writer never reads it.
I followed the order's stated sequence anyway and left the observation for the issuer: the preflight
already named this risk and chose its disposition, and that disposition is the issuer's to own, not mine
to substitute.

## AC1 -- and four mutants, two of which did not fire

`python -m pytest .../test_canonical_prices_source_firm.py -q` -> **8 passed**, rc 0, in a detached
worktree at HEAD holding **both** fetched served files: the writer at its repo path and `scopes.json` at
`infra/logic/registry/scopes.json`, which is "where the fixture copies the registry from" -- read out of
the test (`:123`), not guessed. Both re-hashed **in place** before the run.

A passing test says nothing about *which* files it read, so:

| mutant | site | result |
|---|---|---|
| A | first `source_firm` token in the writer | **did not fire** -- 8 passed |
| B | `REGISTRY_FILE = 'scopes.json'` (`:130`, the round-42 change) | **FIRED** -- 4 failed, rc 1 |
| C | every `opal-data-cot` spelling in the served registry (5x) | **did not fire** -- 8 passed |
| D | served registry replaced with invalid JSON | **FIRED** -- rc 2, error at collection |

**A did not fire because I aimed badly**, not because the test is blind: the first occurrence is the
module docstring at `:31`. A weak mutant that passes is evidence of nothing, and it would have been easy
to report as a pass. **B** then hit the load-bearing site and failed 4 tests including
`test_f_registry_file_beside_writer_cottonwood_address_reads_cottonwood` (`AssertionError {'absent': 78}`)
-- so the suite binds to the **served writer**.

**C did not fire for a reason that is the test's design, not a gap.** The test reads firm names *from* the
registry via `lookup()` -- its own docstring says "The firm names below are read from the registry
(lookup), not typed" -- so renaming a bucket moves **both** the expected and the actual through the same
file and the assertion still holds. It validates the resolution *mechanism*, not a hardcoded spelling.
Rather than leave that as a plausible story, **D** settled it: invalid JSON in the served registry drove
`rc 2`, an error at **collection**, `json.decoder.JSONDecodeError` raised through the test's own
`from opal_naming import lookup` chain. So the served registry file **is** read by this run. Its *bytes*
are carried by the sha256 read-back at leg P1, which is the right instrument for a data file.

All mutants reverted; suite re-read 8 passed rc 0. Worktree removed with `git worktree remove` (no
`rm -rf`), and the shared tree's copies of both files verified still at their served hashes with
`git status` clean.

## Not claimed

`D2-S62` closes on the **next manual silver-prep census** (`source_firm=cottonwood` on every row,
`BREACH=0`), which CTO condition 3 and order step 8 assign to the issuer under its own pair. The pinned
registry's staleness check is one line **inside** that census by the CTO's placement -- no monitor is
built -- and belongs to COTBKF's next issuance.

## Compiler Tools

| tool | invocation | result |
|---|---|---|
| `safe_deploy_core.upload_plan()` | on the writer, before any write | exactly 1 entry; `scopes.json` absent by design, so the two-key total came from both instruments |
| `safe-deploy.sh` | one file, no bypass flags | rc 0, gate PASS, 1 path, own `comp-pipescript deployed` VERIFY OK |
| `aws s3api` / `boto3` | before-reads incl. the 404 + control; `put_object` for the mint; read-backs; rollback head by VersionId | all as the pair states; both served sha256 equal; prior writer version retrievable |
| `deploy_ledger.py` | `open` / `close-leg` x5 / `close` | 5 legs before the write; CLOSED all proven; nothing left staged |
| `proof-of-spec-check.py` | `<instance> CB42ap2-AC1` | **VALID (rc=0)** first pass |

**What failed / gaps.** (1) Mutant A was aimed at a docstring and proved nothing; recorded rather than
quietly dropped, because a non-firing mutant reported as a pass is worse than no mutant. (2) Mutant C's
silence needed a fourth mutant to explain; "it probably reads the registry" was not good enough.
(3) `comp-pipescript deployed` covers the writer but not `scopes.json` -- it sweeps scripts, so the
registry key's currency rests on the sha256 read-back, which is why that read-back is the leg's evidence
rather than a tool verdict. (4) The AC1 expect is the bare word `passed`, satisfiable by a partial run;
the real bar is 8 of 8 and rc 0.

## Push state

MEASURED at write time -- see the final report line; re-measure at read time.
