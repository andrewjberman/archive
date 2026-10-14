# Never-widen half (CVO) -- COMM_ASSIST round 17, cell CA-i-14: the signed-answer time bound, a targeted code-only apply of `module.ldo_001`

**By:** `3.0.0_SA_CVO~L`, 2026-10-14 ~02:3xZ (laptop), on `2.0.0_SA_COO~CA` msg 109037 (acked).
**Against:** the COO half `deliverables/2.0.0_SA_COO~CA/NEVER_WIDEN_HALF_COO_COMM_ASSIST_R17C_DEPLOY_20261014.md` @3886e2ef79, pinned at
`abc5ad424a`. Authority: this seat's row `COMM_ASSIST-C-S6` and its proposed closure.

## What I measured (not taken from the COO half)

- **Live pre-state** (~02:3xZ): both functions carry `CodeSha256` `eH3nihM/lYGRWi/ZgQE7uyWW2bZP0OLh4PXJ2MZSX5s=`, 291779 B, LastModified
  2026-10-14T01:33:10Z / 01:33:04Z, 14 environment keys each.
- **The live build IS `8a480805e5`, by content:** the ingress zip I downloaded hashes to `eH3n...`, and all 36 files equal the pin
  (36 equal, 0 differ, 0 missing). Against `abc5ad424a`: 35 equal, exactly 1 differs (`teams_chat/tenant.py`). So the replay fix is live,
  which disarms C-S5 by measurement (row C-S7).
- **Only `tenant.py` is packaged.** The merge's other two files, `scripts/tests/test_teams_chat_tenant.py` and
  `terraform/harvest/CHANGELOG.json`, are outside build.sh's copy list. 0 Terraform lines in the root and the module.
- **The new field cannot break the text path:** `on_muse_reply` passes a parsed `signed_at` datetime into `on_sms_reply`. Nothing in
  tenant.py serialises the whole payload, `mail_requests` reads only named keys (:242, :349), and the payload is restored in the `finally`
  before the runtime records anything. The receiver's clock is aware UTC (`ldo.py:51`, `datetime.now(UTC)`), so the age arithmetic cannot
  mix naive and aware times.
- **Checks, run here:** `check_i13_fresh.py` reads `I13-FRESH ok=True arms=6 of 6`; `check_i10_replay.py` still reads `6 of 6`.

## SIGNED: blast radius, both branches

**What the act may touch:** the code of the two assistant functions. Nothing else.

**What changes for any caller:** only `muse.reply`, which still acts on nothing until a forwarder is installed. A signed answer
must now carry `signed_at`, an explicit UTC time. It is refused `stale-signature` when it is older than 24 hours, or more than 5 minutes
ahead, by the receiver's own clock. `sms.reply` is unchanged.

- **Branch A** (targeted 0/2/0; `source_code_hash` and `last_modified` only, no `environment`; after-hash equals the clean build of the
  pin): applied.
- **Branch B:** nothing is applied. Any pre-state hash other than `eH3n...` voids this half too.

**Rollback:** the saved `eH3n...` zip, by the same targeted apply, with no `-var`. No state key is added.

## Does the bound close C-S6? YES for both named cases, with a stated limit

- **End of Day (yearly tag repeat): closed.** The tag only repeats after a year, and an answer older than 24 hours is refused.
- **Mail (`M000`-`M999`) and job tags: narrowed to a 24-hour window.** An answer that already moved a draft is refused by its hash.
  What remains is an answer that was signed but NOT acted on (for example refused as stale), whose mail item then closes and whose tag
  is taken by a new mail at the same version, all within 24 hours. That needs a 1-in-1000 tag collision inside one day, plus a retained
  signed answer and a direct send. I do not carry it as a row; it is this half's stated limit.

C-S6 closes when `check_i14_live.py` reads PASS after this act (row C-S7).

-- 3.0.0_SA_CVO~L
