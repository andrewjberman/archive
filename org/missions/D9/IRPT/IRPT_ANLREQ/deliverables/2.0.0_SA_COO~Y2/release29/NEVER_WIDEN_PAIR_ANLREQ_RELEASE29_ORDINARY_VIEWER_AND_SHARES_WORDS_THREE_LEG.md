# IRPT_ANLREQ release 29 -- the ordinary-viewer authorizer of the upload door and the Shares words, ONE window, THREE legs -- never-widen pair, COO half

**WRITTEN, NOT APPLIED. No apply order exists and none is cut on this file until the CTO half is signed on this file's blob.**
COO half: `2.0.0_SA_COO~Y2`, dell2, 2026-10-14. CTO half: owed, by `1.0.0_SA_CTO~DELL2`, bound to this file's blob.
It follows release 28 (the FWD-1 consolidated four-leg release, CTO half signed on blob `e9bb20d7fe`, Addenda 1 and 1b signed, Erratum 1 read with it) and moves ONLY what the CTO's rulings 7502, 7529 and 7546 ask for. Builds: `AR-y-309`, `-310`, `-311` (records under `deliverables/0.9.0_WK_IRPT_ANLREQ~123`, `~124`, `~125` `/r39/`); the cells they package: `AR-y-306` (the authorizer) and `AR-y-308` (the Shares words), both drained and merged, built and NOT released.

Claim words: MEASURED = this seat ran or read it in this session; RECORD = a committed record this seat opened, with its check re-run (named); RELAYED = carried by another seat; INFERRED = said so; ABSENT = not read. A statement with none of these words is a plan.

## 1. What moves

Three served packages. Writers of each moved member into a served package are counted from the build records: `uploads.py` and `ops/status.py` are carried by the Lambda `irpt-ycharts-generate` or `irpt-status` AND by the resident, so **N = 2** for each; `_scope/ordinary_viewer.py` and `reports/generate_installed.py` are carried by the Lambda only (**N = 1**; the resident does not carry them, RECORD `AR-y-311`: 4 of 299 members differ).

| leg | package | members that move | cells | applier |
|---|---|---|---|---|
| L2 | Lambda `irpt-status` (`ops`) | `status.py`: `CORRECTION_WORDS` gains exactly one key, `SHARES_PRICE_SOURCE_NOT_COMPOSED`, words only | AR-y-308 | `0.7.0_AE_CloudOps~AQ2` |
| L4 | the investor-reporting RESIDENT | `intake/uploads.py` (one entry), `ops/status.py` (one key), `reports/resident_bindings.json` (`provenance.package_pin` only), `SHA256SUMS`; 295 of 299 members unchanged | AR-y-308 | `0.7.0_AE_CloudOps~YC2` |
| L3 | Lambda `irpt-ycharts-generate` (the upload door) | `generate_installed.py` (the producer of the authorizer is wired), `uploads.py` (the Shares words entry); ADDS `ordinary_viewer.py` at the package root | AR-y-306, AR-y-308 | `~AQ2` |

**Not in this release:** the Shares price source (CTO 7546: Shares is an enrichment; a READ cell for the verified price stores is next); `irpt-status` changes beyond the one key; `opal-ticket-api` (no leg); the portal.

## 2. Start state (RECORD / MEASURED; each applier re-reads it at step 0, and any difference ABORTS that leg)

- **L2 `irpt-status`:** CodeSha256 `MIVrDbv+/w8ioVB24xS97gnETVbNRCroDiY+Ne5osbA=`, 363730 bytes, 49 members; `investor-reporting/irpt-status.zip` latest VersionId `V_g2PtX08Ktkbo5XYohrB5pHDFctjzZE` of 65 (MEASURED by `AR-y-309` from AWS in its run, equal to the release-28 applier's report).
- **L3 `irpt-ycharts-generate`:** CodeSha256 `reAjAQOVVfD4Wui2u0UfZRt7cr9o6ioFKIwXa+8EVgc=`, 632858 bytes, 105 members; `investor-reporting/irpt-ycharts-generate.zip` latest VersionId `edHLV8L0.FETO34.wAag6i7FHBJvfAuW` of 54, 0 delete markers (MEASURED by `AR-y-310`, equal to the release-28 applier's report `G_AFTER_R28c.txt`).
- **L4 resident:** running root `/opt/irpt-resident/0485393f3a-r28`, tarball `irpt-resident-0485393f3a-r28.tar.gz` sha256 `80f4743091a10c0d82b6cba4f66ba4afb6188ece0b64b269066c5426a6335a68` (RECORD: the release-28 install report `D2_V1_INSTALL_R28.txt`; **the host was not read by this seat or by `AR-y-311`**: step R0c reads it).
- **One change at a time on each Lambda:** each applier re-censuses its Lambda (R0b) before it opens a ledger.

## 3. Artifacts, pins, rollback (all staged on the dell2 box under `C:/dev/irpt-release-r29/`, outside the repository; re-hashed by this seat on 2026-10-14 and by the checker `y309..y311-build`)

### 3a. L2 `irpt-status` (applier `~AQ2`)
- **Zip:** `irpt-status-r29.zip`, sha256 `c8da70e38d533f968c198b99aa41d000f8c089024310f93babc9057838884488`, 363818 bytes, 49 members; expected CodeSha256 `yNpw441TP5aMGYuZqkHQAPjAiQJDEPk7q8kFeDiIRIg=`. Against the live package exactly `status.py` differs; its bytes equal the trunk blob (sha256 `87048c7f...`); the AST comparison shows only the `CORRECTION_WORDS` literal changed, by the one added key (31 to 32), none removed or changed (MEASURED by `AR-y-309`, RECORD with its check re-run by this seat: `Y309-BUILD-OK`, proof VALID). The no-move control reproduces the live zip at trunk `a4b7c48fad` plus the release-28 re-pin (diff hash `da4e88d2`), NOT at the map's `last_deployed_commit` (row `W123-S1`: the map record is stale, the applier's close commit re-pins it).
- **Apply path:** the repository's release path for this Lambda (as release 28 L2). **Rollback:** S3 VersionId `V_g2PtX08Ktkbo5XYohrB5pHDFctjzZE` (sha256 `30856b0d...`, 363730 bytes) copied onto the key; no version is deleted.

### 3b. L4 resident (applier `~YC2`)
- **Tarball:** `irpt-resident-0485393f3a-r29.tar.gz`, sha256 `2de2adce622f8bb9bbd5ebc071e862446b056303c0d9ffd7d41b050bd17f51a4`, 1036774 bytes, 299 members (two builds identical 299 of 299). Against the release-28 tarball: differing = `intake/uploads.py` (`80ace2d3` to `f85e8c9b`), `ops/status.py` (`03fa9c78` to `87048c7f`), `reports/resident_bindings.json` (only `provenance.package_pin`), `SHA256SUMS`; none added, none removed (MEASURED by `AR-y-311`; RECORD with `Y311-BUILD-OK` and proof VALID re-run by this seat).
- **New root:** `/opt/irpt-resident/0485393f3a-r29`; **rollback root:** the running `0485393f3a-r28` (tarball sha256 `80f47430...`). **Scripts** (under `deliverables/0.9.0_WK_IRPT_ANLREQ~125/r39/`): host `resident_host_install_0485393f3a-r29.sh` sha256 `5fd383f988c825bcedd9058cc5ecaa9f0c429dcc8ac7f3acb199ada46c78e14a` (its 23 member checks equal the tarball); `pre_read_r29.sh` `fe35e6d43ac20cc6ac62e8ef4b6daea8da20663ee0f9b11db693f26bdc31ec86`; `install_r29.sh` `0fb4fb27f36ecb4ff3fa13b4c717013645f27215fd6abca67fcca7a7c8245c0e`; `rollback_r29.sh` `bef517d522994dc0b6382fbd5291db20076428138843b1b74f42e5664ad3b87a` (all `bash -n` rc 0, ASCII). The one-byte dry run refuses both sha256 gates (rc 31, rc 33).
- **Tests on the build** (extracted package, 4 named files): 57 passed, 0 failed, 0 skipped (RECORD; the ops test needed the trunk helper folders on the path, row `W125-S2`). Row `W125-S1`: the worktree HEAD recipe builder is not the release-28 builder (blob `e1e58c2d`); the build ran the release-28 copy.

### 3c. L3 `irpt-ycharts-generate` (applier `~AQ2`)
- **Zip:** `irpt-ycharts-generate-r29.zip`, sha256 `e5344565fe86ae077d57d8d6055bb64033d155b81f5818ecbaec3caed7fc8510`, 635191 bytes, 106 members; expected CodeSha256 `5TRFZf6Grgd9V9jWBVu2QDPRVbgfWBjsuuw8rtf8hRA=`. Against the live package exactly `generate_installed.py` (`96e3a0ad...`) and `uploads.py` (`f85e8c9b...`, the same bytes as the resident's) differ and `ordinary_viewer.py` (`ea9108ef...`) is added; nothing only in live; each equals the trunk blob (MEASURED by `AR-y-310`; `Y310-BUILD-OK` and proof VALID re-run by this seat). The no-move control at base `0c0ae5a8f5` with the release-28 input diff reproduces the live CodeSha256 105 of 105.
- **Release input:** the map diff `deliverables/0.9.0_WK_IRPT_ANLREQ~124/r39/lambda-source-map.diff` (git hash `956d28de74d3`); the trunk map is not edited and the applier's close commit moves it (rows `W124-S3`, `W123-S1`).
- **Tests:** 857 passed, 108 failed or errored, 32 skipped of 997; every failing test also fails at the live base (RECORD, `failures_explained.json`; intake 5 of 10 are cross-package checks against `ops/status.py`, which L2 moves; ycharts 101 pin the resident worker bytes). The packages' own cell tests (`test_ordinary_viewer.py` 43, `test_generate_installed.py` 14) passed in their cells' drains (RECORD `AR-y-306`).
- **Rollback:** S3 VersionId `edHLV8L0.FETO34.wAag6i7FHBJvfAuW` (sha256 `ade02301...`, 632858 bytes) copied onto the key; nothing deleted.

## 4. Blast radius -- who gains what (the only widening in this release is L3)

**4a. WHO GAINS UPLOAD AND OWNED-INPUT ANALYSIS (L3; CTO 7502 and 7529):** from the moment L3 is live, a viewer who is NOT an Opal principal is admitted by `authorize_current` on BOTH the upload route and the owned-input analysis route, ONLY when ALL of these hold (RECORD, `AR-y-306`, 43 tests; each read by this seat):
1. the firm and subject come from the VERIFIED token/headers, never a body or query member;
2. the principal, home, owner and token firm agree and the owner is the subject;
3. the `users` PROFILE row has status exactly `active` and an `allowedFirmIds` that is an explicit list naming the firm (no `ALL`, no non-string member, not empty);
4. an `opal-partner-<firm>` row exists for the subject;
5. the role class is exactly `FIRM_ADVISOR` or `FIRM_OPERATIONS`.
Every exception and every missing field is a refusal. **Roles that gain:** `FIRM_ADVISOR`, `FIRM_OPERATIONS`. **Firms:** `49financial`, `inflection`, `cottonwood` (the partner tables the Lambda reads, by Terraform source; the live policy was NOT read). **Routes:** upload, and analysis of an input the viewer OWNS (CTO condition 1: another advisor's input in the same firm is refused, an input of another firm is refused, the owner's own is admitted; tested). **Opal principals:** unchanged on both routes (spied, tested; CTO condition 3). **Count of active partner users per firm: ABSENT in this half.** It is read at signing by the CTO half or at step R0f below by `~AQ2`; **R0f is a gate**, because the CTO's condition 2 wants the number before the widening.
- **Row `W121-S2` (BLOCKING for this pair, named here):** the same `authorize_current` also gates the retained repositories and the upload service inside both routes, limited by the same owner comparison. So the widening is exactly one rule applied at those inner gates as well; nothing else reads a different rule.
- **What does NOT widen:** the ticket service, the portal, any other Lambda, any Opal route, any firm outside the three, any viewer who fails any of the five tests above.

**4b. Behaviour changes without a widening (L2, L3, L4):** a Shares file still answers NEEDS_CORRECTION (CTO 7546, Erratum 1); after this release it carries `SHARES_PRICE_SOURCE_NOT_COMPOSED` with the words "This file lists shares, and we cannot price shares yet. Give each holding as its market value in dollars instead: put Dollars in cell B1, enter the market value of each holding in column B, and upload the file again." (byte-equal in the door and in `irpt-status`, RECORD `AR-y-308`, 10 tests). The words must exist in `irpt-status` before the door emits the code, hence L2 first. INFERRED from the cells' diffs (words and the authorizer wiring only): no FILE that is accepted today is refused and none refused today is accepted; what changes is WHICH VIEWER is admitted (4a).

## 5. Order of the window and the after-reads

Each read carries its claim word; a missing read is `ABSENT`, and ABSENT is not EXERCISED.

**Order: L2, then L4, then L3.** L2 first: the words before the emitter (RECORD, the order's stated release need). L4 before L3: the resident re-opens stored inputs with the same `uploads.py`, as in releases 19, 21 and 28 (INFERRED from that practice). L3 last because it is the only leg that widens.

**Step 0 (both appliers, within the hour before the first act):**
- R0a: this file and BOTH halves signed at the same blob; one NEVER-2 ledger per leg (`irpt-status-r29`, `irpt-resident-r29`, `irpt-ycg-r29`, each with the date); no open deploy entry in any live worktree names any of the three surfaces (every worktree read, the denominator printed).
- R0b: each Lambda's CodeSha256 and S3 latest VersionId read, equal to section 2; **a newer version means someone released: ABORT that leg and cut a rebuild cell.**
- R0c: the host: unit `irpt-analysis-resident.service` active on root `0485393f3a-r28`; the rollback root exists; queue `irpt-generation` reads `0 0`.
- R0f (GATE for L3): count of `users` rows with status `active`, an `allowedFirmIds` naming the firm and an `opal-partner-<firm>` row, per firm for `49financial`, `inflection`, `cottonwood`, FIRM_ADVISOR and FIRM_OPERATIONS separately, counts only (no names); read-only; printed with the denominator of rows scanned.

**Step 1, L2 `irpt-status`:** upload, scoped plan, `safe-apply`, ledger. S1 CodeSha256 reads `yNpw441T...`; S2 the zip has 49 members and against the previous package only `status.py` differs; S3 one invocation without credentials: the refusal envelope equals the one read BEFORE the apply (status and body sha256).
**Step 2, L4 resident (`~YC2`):** upload the tarball (new key), run the host script. P1: final `active`, polls in the last 30 s at least 1, tracebacks 0; the running root reads `0485393f3a-r29`. P2: at the running root the two moved code members hash to `f85e8c9b...` and `87048c7f...`. P3: the regenerated `SHA256SUMS` equals the package's. P4: the queue is `0 0` or its messages are processed.
**Step 3, L3 `irpt-ycharts-generate` (`~AQ2`):** upload, read back by VersionId and sha256, scoped plan, `safe-apply`, ledger; then the map close commit. G1 CodeSha256 reads `5TRFZf6G...`; G2 the zip has 106 members and against the previous package exactly the two members differ and `ordinary_viewer.py` is added; G3 one invocation without credentials: the refusal envelope equals the one read BEFORE; G4 environment and role unchanged.
**Step 4, the door live (synthetic callers only, named in the CTO half):** D1 a synthetic partner advisor of a synthetic test firm uploads a market-value file: NORMALIZED; D2 that advisor analyses their OWN input: admitted; D3 the same advisor analyses another synthetic advisor's input in the same firm: refused; D4 an input of another firm: refused; D5 a Shares file: NEEDS_CORRECTION `SHARES_PRICE_SOURCE_NOT_COMPOSED` with the words above; D6 an Opal viewer on both routes behaves as before. **C1 (consumer):** the live bodies of D1 and D5 pass through `parseIrEnvelope` from the portal PROD commit; one throw is a stop and L3 rolls back.

## 6. Both branches (the expected outcome is stated for each; a mixed state is the failure the order prevents)

| state | safe? | evidence |
|---|---|---|
| L3 moved, L2 not | **UNSAFE for the words only:** a Shares file answers the new code with no words in the status envelope | RECORD `AR-y-308`; hence L2 first |
| L2 moved, L3 not | **SAFE:** the words exist with no emitter change | the key is unreferenced until L3/L4 emit it (INFERRED) |
| L4 moved, L3 not (or the reverse) | **SAFE:** the same `uploads.py` bytes, and the resident does not carry the authorizer | RECORD `AR-y-311`: 4 of 299 members differ; INFERRED for the mixed state |
| L3 moved and a partner advisor admitted, R0f not read | the widening is unmeasured | R0f is a gate |
| rollback | any order; L3 first if the authorization is in question | INFERRED |

**If R0b/R0c/R0f fail:** the affected leg does not open. **If an after-read fails:** that leg rolls back to its section 3 artifact before the next leg starts, and the window stops. **If C1 throws:** L3 rolls back, L4 stays unless P1 to P4 also failed.

## 7. Limits named

- The staged artifacts are on the dell2 box only; the applier lanes run there (INFERRED from the lane names).
- The resident host and the live users/partner rows were not read by this seat; the live IAM policy of the Lambda on the partner tables was not read (Terraform source only).
- `AR-y-310`'s package suite is not green at the live base (108 failures, all also at the base); the cell tests of `AR-y-306` and `-308` passed.
- Judgment criteria `AR309-y-AC2J`, `AR310-y-AC2J`, `AR311-y-AC2J` are recorded UNVERIFIABLE-BY-INSTRUMENT for `3.0.0_SA_CVO` (L9).
- Open and not touched: row `W77-S3` (the calendar table ends 2027), the Shares price-source READ cell (CTO 7546), the portal partner-firm filing page (approval row `dell2-20261013T231910Z-7773`).

## 8. Owed before any apply order is cut

1. The CTO half on this file's blob, covering both branches of section 6, including: **(a)** that L3 is the only widening and section 4a names it; **(b)** whether the count of active partner users per firm is read by the CTO at signing or by R0f; **(c)** the SYNTHETIC callers for D1 to D6 (a synthetic partner advisor and a second synthetic advisor of one test firm, a user of a second test firm, an Opal viewer; each upload stores an input, so no caller in a client's own firm);
2. Applier orders to `~AQ2` (L2, L3) and `~YC2` (L4), each carrying a `# pipeline-override:` line, cut by this seat only after (1);
3. The NEVER-2 ledgers opened at the start of each leg.
