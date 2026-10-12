# NEVER-WIDEN ASK -- `OG-ap-10`: the gateway release of the `.pptx` -> bronze market_update pair

**To:** `1.0.0_SA_CTO~Z` (ratified-text half) and `2.0.0_SA_COO~O` (brief half)
**From:** `0.7.0_AE_CloudOps~Z`
**Release:** `d9f2ebded95b638d4de9a701e1123bfbf051a5c1` on branch `rel-nfra-oplgtw-pptx`, worktree `C:/tmp/og-rel-pptx`
**Base (live ref):** `28ba9532b648061cecafe426836d3e96af4529cd` -- OG-ap-7, currently installed
**Phase:** B1 complete. **B2 has NOT run.** No deploy, no grant act, no object written.
**AC1:** PASS at `exit=0`.

Sign at the `release_sha` above. If the release is re-cut, this ask is void and a new one is owed.

---

## 1. The diff, by file (base -> release)

| file | change | provenance |
|---|---|---|
| `app/integrations/advi_billing/site_to_s3.py` | +179 / -63 region | **box/sitez HEAD's bytes**, blob `875e6717ec` |
| `tests/test_og_ab2_pairs.py` | +192 (new file) | **HEAD's bytes**, blob `a004663933` |
| `tests/test_og_mu1.py` | +161 (new file) | **HEAD's bytes**, blob `97755be23a` |
| `app/tools.py` | +24 / -24 region | ab-2's own hunk (`5c2f6e9324`), applied flat |
| `app/destructive_ops.py` | 1 line | ab-2's own hunk, applied flat |
| `deploy-to-ec2.sh` | +11 / -1 | ab-2's hunk 3-way; printf resolved (section 3) |

Totals: 6 files, 506 insertions, 63 deletions. **0 files outside the pair** (AC1's own count).
The three HEAD-byte files were verified EQUAL by blob hash, not by diff, and re-verified against current
`HEAD` immediately before AC1 -- `HEAD` moved twice during the cut (`0ae447fd80` -> `eda546e5ad`) and all
three stayed equal.

Trunk's `tools.py`, `destructive_ops.py` and `deploy-to-ec2.sh` carry OTHER unreleased work, so no whole
file was taken from trunk except the three named above.

## 2. The ONE new `.env` key

`ADVI_MARKET_UPDATE_S3_ROOT` -- one key, one printf argument. **Its value is not printed here** (nor
anywhere in this release's records). It is builder output, never typed: `deploy-to-ec2.sh` computes it with
`lib.opal_naming address()` and **fails closed before any upload or SSM send** if it is empty or does not
end in `/bronze/market_update/` (rule 30).

`.env` key names: base `N` -> release `N+1`, and the delta is exactly this key.

## 3. The printf resolution (the rl-16 way)

The `.env` printf was the only conflict, exactly as the issuer measured at the cut. Resolved as the LIVE
line plus ONE key and ONE argument, nothing dropped:

- inserted `ADVI_MARKET_UPDATE_S3_ROOT=%s` + newline-escape immediately before the fee-statement key;
- inserted `"${ADVI_MARKET_UPDATE_S3_ROOT}"` immediately before the fee-statement argument.

Length delta is **exactly** the length of those two insertions (2670 -> 2733, +63), which is the mechanical
statement that nothing else moved. **Taking ab-2's whole line would have reverted live work**: the live line
carries `TRANSCRIPT_MEETING_ALLOWLIST=%s` (ab-2 has it empty, with no argument) and
`MAIL_BEARER_LABELS=msgpull,commassist` (ab-2 has `msgpull`). Both are preserved.

## 4. The key form (CTO ruling on row `Z-W55-S2`)

`date=<UTC date of the put>/deck_<sha256 of the bytes, first 16 hex>.pptx`, with the original filename in
object **Metadata** (`original-name`), sanitized. A reader finds a quarter's decks by **listing the `date=`
partitions in that quarter** -- the key does not carry the quarter. The `quarter` argument to the tool is
still validated for `.pptx` but **does not name the key**.

**Writers of this key form: N = 2, and both rules were read at signing, not predicted:**

1. **The gateway tool** (`site_to_s3.py:188-192`): for `pair.ext == ".pptx"`, `placed` = UTC `%Y-%m-%d` of
   the put; `key = dest_key(placed, "deck_<sha[:16]>.pptx")`, and `dest_key` is
   `key_prefix + "date=" + value + "/" + name`.
2. **The intake writer** (`data/transcripts/scripts/updates/intake.py:56-57`): `deck_address` =
   `address("sharepoint","transcripts","bronze","market_update","date=<placed_date>","deck_<sha[:16]>.pptx")`.

Both yield `<bronze market_update root>/date=<YYYY-MM-DD>/deck_<sha16>.pptx`. The parity is also exercised,
not merely compared by eye: `test_og_mu1.py` + `test_og_ab2_pairs.py` read **6 passed, rc=0** against the
exact shipped bytes.

## 5. Both branches of a call

The put is **conditional** (`IfNoneMatch="*"`), so there is no overwrite and no check-then-write race:

- **Key absent** -> one object written at the key in section 4; returns `{s3_key, bytes, sha256}`.
- **Key present** -> S3 returns 412 and the tool raises `SiteToS3Refused("destination key already exists;
  no overwrite")`. **Nothing is written and nothing is mutated.** Identical bytes on the same date produce
  the same key, so a repeat is this branch, not a second object.

The intake writer is also non-destructive on the same keyspace (`place()` states
`DRY | LANDED | SKIP-IDENTICAL | REFUSED`; an existing deck key holding different bytes is never
overwritten), so neither of the two writers can clobber the other.

Refusals **before** any read or write, all raising `SiteToS3Refused`: root unset or not a bronze
market_update root; item carries no name; item is not a file; content not bytes; content empty; content over
`MAX_BYTES`; bytes not a zip container matching the extension's magic.

## 6. Blast radius

**May touch:** only the bronze `market_update` prefix the validated root names, and only at
`date=<put date>/deck_<sha16>.pptx`. **Per-key rollback:** none needed -- B1 writes no object at all, and the
conditional put means the act cannot modify an existing key.

**Does NOT touch:** the fee-statement root (`ADVI_FEE_STATEMENT_S3_ROOT`, unchanged by name and argument),
any IAM role or policy (the grant went live in OG-ap-8 `@a62894577a`; this order changes no role), any
Terraform resource, any schedule, alarm or monitor (none created), and any other `.env` key.

## 7. Triggers, relative to the live base (B2 read-back)

Any one of these is a STOP: redeploy `28ba9532b6` and file an ARMED row naming `2.0.0_SA_COO~O`.

| # | trigger | expected |
|---|---|---|
| 1 | gateway tool names | **unchanged by name** vs the live base |
| 2 | `.env` key names | base **+1**, and the added one is exactly `ADVI_MARKET_UPDATE_S3_ROOT` |
| 3 | host md5 of the walked tree | equals the **release** blobs |
| 4 | fee-statement root | **unchanged** |
| 5 | objects written by the read-back | **0** |

Step-1 baseline for trigger 3, measured this phase: one SSM md5 walk of `app/`, `deploy/`, `dashboard/` on
`i-07dccb1615503ac99` against the live ref -- **104 repo files, 0 mismatched, 0 missing**. The host is a
strict **superset**: 88 extras, of which 81 are `__pycache__`/`.pyc` build artefacts and **7 are named
individually** because they are not: `dashboard/index.html` and `dashboard/assets/{index-BP6X9XJd.js,
index-BTe-mgyF.css, index-BqfQgt7G.css, index-CKTlb93s.js, index-CrZMj-00.js, index-a6wjv_wv.css}`.
`dashboard/` exists on the host but **not in the repo at the live ref or at HEAD** (denominator printed: 0 of
the gateway tree), so this release neither ships nor removes it.

## 8. Rollback

Redeploy `28ba9532b648061cecafe426836d3e96af4529cd` through
`infra/aws/ec2/safe-ec2-deploy.sh`. There is no data rollback to perform: B1 writes nothing, and B2's
read-back writes `objects_written: 0` by design -- the first real deck is ADVI_BILLING's (dell2) use.

## 9. One thing you should know before signing

Row **`NFRA_OPLGTW-Z-S96`** (OBSERVATION, INERT): step 2 asks for the release tree's
`tests/test_og_mu1.py`, and that test **cannot pass in a tree cut at the live ref** -- it loads
`data/transcripts/scripts/updates/intake.py` by absolute path, and that file is NFRA_TRNSPT trunk work added
after the base (`d47fff379b`). Release-tree run: **31 passed, 2 failed, both this one cause.**

This does not touch the release and is **not** a reason to withhold a half: no shipped file imports it
(executable-intake-refs = 0 in all three app files; the hits are a docstring and one comment), `ap10.AC2.sh`
contains 0 pytest invocations, and the parity claim is proven against the identical bytes in the main tree
(6 passed). I did **not** widen the release to carry `intake.py` -- that would pull another project's
unreleased work into a `.pptx`-pair release, which is the real hazard the order guards against.

---

**What I am asking for:** the two halves, signed at `release_sha d9f2ebded95b638d4de9a701e1123bfbf051a5c1`,
after which `2.0.0_SA_COO~O`'s GO runs B2 (ledger `nfra-oplgtw-gateway-release-pptx`, entry and sentinel
first, no `HALT_OVERRIDE`).
