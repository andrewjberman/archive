# AMGT_RESAPP round 68 -- `AMGT-ar-3` never-widen half (COO), `2.0.0_SA_COO~Z`, 2026-10-05 ~01:5xZ

**The act (ONE):** redeploy `opal-amgt-scoped-api` at build commit `7158bc9d4d`, or a descendant whose CONTENT-DIFF against the
DEPLOYED build equals the list below. Build and upload ONE artifact, then ONE code-only `safe-apply`. `memory_size` stays 1769.
- Executor: `0.7.0_AE_CloudOps~A`.
- Order: `task-orders/AMGT_RESAPP.TO-AMGT-ar-3.the-code-redeploy.md` (`<proof_genre>DEPLOY</proof_genre>`).
- It carries ar-1, drained `17dd36e08b` (the FWD-39 cloud repair), and ar-2, drained `7158bc9d4d` (plain reason words).

## THE BASE, read live at signing -- the rollback

| property | value |
|---|---|
| function CodeSha256 | `2rFeF57lMh8MkU6WRgZyImZt7RMlW14BdxmUjIBvSSQ=` (AMGT_CORPUS al-5's build, LastModified 2026-10-04T22:42:11Z; it carries round 67) |
| function MemorySize | 1769 |
| artifact S3 VersionId | `O1WGPxfTK9vszvvZqzzuOfjQAGMOIZiM` (al-5's upload, 2026-10-04T22:36:21Z) |
| open NEVER-2 entries on this function | none (`.open_deploys/` read at signing) |

## THE FILE LIST (`--build-only` at `7158bc9d4d`, from a detached checkout)

The build read cold-start FATAL [] and request-time break []. It is 253,758,579 B against the 262,144,000 B ceiling (96.8%,
8,385,421 B spare). Against the DEPLOYED `2rFeF57l...`: `CONTENT-DIFF SUMMARY: files 356, IDENTICAL 354, CHANGED 2, ADDED 0, REMOVED 0`.

| file | change | source | served effect |
|---|---|---|---|
| `lib/research/api/scoped_amgt.py` | CHANGED | ar-1 + ar-2 | Clouds: accent-safe tokens, the declared own-name aliases, compound parts, and the measured boilerplate (c27). A covered-no-block name's /thesis and /peers reasons and the /ledger source reasons read in plain words (c28) |
| `lib/research/coverage/covered_no_block.py` | CHANGED | ar-2 | the lead reason: "<Company> (<TICKER>) is a covered name (<universe>, as of <date>), and its research pack is not in yet." |

Any other changed file at build time is a STOP.

**New S3 read paths (CTO round-67 ruling 4): NONE.** I scanned the diff `8ba8bf3ab0..7158bc9d4d` under `lib/` for boto3, get_object,
list_objects, s3://, Bucket= and the snapshot readers. The only hits are a test double and a monkeypatch in the tests. So no
simulate arm is owed. If the build differs, the arm is owed for each added path.

## THE BLAST RADIUS -- what the act MAY touch, and the rollback

| act | what it MAY touch | rollback |
|---|---|---|
| upload | a new version of `research/opal-amgt-scoped-api.zip` (versioned) | the prior VersionId `O1WGPxfTK9vszvvZqzzuOfjQAGMOIZiM` |
| code-only `safe-apply` | the function's code only; memory stays 1769 | a code-only `safe-apply` with that VersionId, restoring `2rFeF57l...` |

## EXPECTED OUTCOME -- both branches

| check | base (deployed `2rFeF57l`, ~00:4xZ, and r67 c24 at ~01:3xZ) | after (local at `7158bc9d4d`, ~01:4xZ) |
|---|---|---|
| r68 c27 | NO: 6 own-name offenders, 82 clouds with boilerplate | YES: 233 names read, 199 serving, 0 own-name, 0 junk, 0 non-200 |
| r68 c28 | NO: DE /thesis 18 and /peers 3 jargon reasons; /ledger 12 | YES: 0 / 0 / 0 |
| r67 c23, c25, c26 | YES | YES |
| r67 c24 | YES since HARVST round 46 (ar-4, @4b2caa5a17): mismatches 0, no-table-row 0, unreadable 0 | YES (reason text only; tone and voters do not move) |
| r64 c9, c10 (30-day), c11-c14; r65 c17; r66 c18/c19/c22 | YES | YES |
| r64 c15 (cold, day route) | YES, 1.9-2.0 s at aq-5 | read on deployed |

**Failure branch:** any of the following is a ROLLBACK, per the table:
- c27 or c28 is not YES;
- any other check moves;
- c15 reads over 5 s;
- a non-200 on a covered key's overlay, thesis, peers, timeline, ledger or collected/chatter;
- the uncovered control ZZZZ_US_Equity answers anything other than 404.

## WHAT THIS HALF DOES NOT COVER

Any of the following in the plan is a STOP:
- a memory change;
- any IAM change;
- a store write or an S3 delete;
- a vendor call;
- a route or gateway change;
- a data-engineering operation.
