# IB-rt-3 RESULT -- ONE OPAQUE-ID NORMALIZER AND THE GRAIN

**TO:** `IRPT_BCKEND.TO-IB-rt-3` | **worker:** `0.9.0_WK_IRPT_BCKEND~1` | **branch:** `wk-irpt_bckend-2-1`
**Executes:** the CTO's round-1 ruling 4 (ONE OPAQUE-ID NORMALIZER; the account-only vs relationship grain).
**Closes (proposes to close, the CVO grades):** rows `W1-S7`, `W1-S9`, `W2-S11`, `W2-S2`.
**Filed this cell:** `W1-S11` (OBSERVATION/INERT), `W1-S12` (BLOCKING/ARMED -- the layer MERGE, not this build), `W1-S13` (OBSERVATION/INERT -- arm (b)'s floor).

---

## 1. WHAT WAS BUILT

| artifact | what it is |
|---|---|
| `infra/aws/lambda/investor-reporting/_ids/ids.py` | THE one definition. `opaque_account/relationship/client/firm`, `opaque(kind, firm, raw)`, `is_issued`, `require_*`, `IdRefused`, `projection_for(firm)`, `raw_key_for`, `firm_ids`. Round 1's exact grammar, so the id space does NOT move. |
| `infra/aws/lambda/investor-reporting/_ids/raw_keys.json` | the upstream field each firm's id is minted from, DECLARED with a `file:line` citation, a `round_1_state` and a MEASURED coverage figure. |
| `infra/aws/lambda/investor-reporting/_ids/tests/test_ids.py` | 29 tests carrying the INDEPENDENT ORACLE -- it re-derives the grammar inline rather than calling the module it grades. |
| `directory_runner.py`, `holdings_snapshot.py` | `opaque_id` is now a BINDING to `_ids.opaque`; 0 occurrences of the grammar remain in either file; the three `<firm>:acct:` mint sites emit the bare issued id. |
| `_scope/resolve.py` (+ its fixtures) | the opaque-id SHAPE check is `_ids.is_issued('account', v)`, not a local bare-24-hex regex that matched 0 of 80 real directory ids (row W1-S11). |
| `layers/irpt-common/build_layer.py`, `ci/lambda-layer-map.json` | the layer carries `ids.py`, `raw_keys.json` and the firm registry, staged from the COMMITTED blob; `irpt-common:5` published and both consumers moved onto it. |

**THE RAW KEY CHANGED FOR TWO FIRMS, and that is what made round 1's ids unequal.**

| firm | directory read in ROUND 1 | declared and read NOW | round-1 result | now |
|---|---|---|---|---|
| inflection | `accounts_v2.account_number` (`acct#9d4420e3`) | `accounts_v2.account_id` (`1003`) -- two columns of ONE table | 0 of 790 | **790 of 790** |
| cottonwood | `fact_allocations['Account Number']` (masked, `*****4583`) | `fact_allocations.AccountID` (`acct#7d2371a7`), MEASURED to be the same value space as `fact_model_assignment.external_id` | 0 of 946 | **837 of 837** (the directory population, whole) |
| 49financial | the crosswalk's account id | unchanged | already agreed | **5,856 of 5,873** |

COT needed NO new join: `fact_allocations.AccountID` already IS the `external_id` space (837 of 837 distinct values present in the assignment table), so the directory mints the declared key from a table it already loads.

---

## 2. ACCEPTANCE

### `RT3-AC1` -- PASS-by-output

```
timeout 900 python org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1/battery_ib_rt_3.py
-> rc 0, final line: IBRT3-ONE-ID-SPACE
```

Full output: `IB-rt-3_RT3-AC1_battery_output.txt` (11,194 bytes). Per arm:

- **(a) ONE DEFINITION.** 67 python files scanned across the two named trees; 5 grammar occurrences; **0 of 5 are a second opaque-id definition outside `_ids/`**. The three hits outside `_ids/` are classified and printed: `intake/poller.py:274` mints a `"REQ-"` request id, `ycharts/generate/job.py:495` mints an `"ATT-"` attempt id -- different id spaces entirely -- and `tests/test_holdings_snapshot.py:357` is the GUARD's own assertion text, inside a string literal. The classification is by `ast` -- a hit counts as prose only when a string CONSTANT'S OWN VALUE contains the grammar (a docstring, or the guard's assertion text), never merely because some other literal sits on the line -- plus the namespace prefix READ FROM THE STATEMENT, printed per hit, and it is fail-closed: a hit with no prefix is called an opaque-id mint. `:acct:` census: **0 live-code sites of 5 textual hits** (all 5 are prose in docstrings that explain what was removed). The layer zip's `python/ids.py` and `python/raw_keys.json` are **byte-equal to the COMMITTED blobs** (14,173 / 5,990 bytes) -- compared against `git show HEAD:<path>`, never the worktree file, because on an autocrlf box the checkout is not the record.
- **(b) THREE PRODUCERS, THREE FIRMS.** Read from the LANDED QA objects through their own `latest.json` pointers, then handed to the REAL `_scope.resolve` and the REAL `performance/handler.check_scope`:

  | firm | directory | holdings | holdings ids in directory | directory ids in holdings | `:acct:` | third producer | adapter |
  |---|---|---|---|---|---|---|---|
  | 49financial | 7,480 | 5,873 | **5,856 of 5,873** | 5,856 of 7,480 | 0 | 25 of 25 | accepted |
  | cottonwood | 837 | 961 | 837 of 961 | **837 of 837** | 0 | 25 of 25 | accepted |
  | inflection | 874 | 790 | **790 of 790** | 790 of 874 | 0 | 25 of 25 | accepted |

  0 ids of non-issued shape anywhere. **The face's floor (`N >= 7,453 / 790 / 946`) is not reachable and is filed as row `W1-S13`:** N there is the JOIN of two producers whose populations come from different upstream tables, and 7,453 exceeds the entire 49F holdings artifact while 946 exceeds the entire COT directory. Both directions are printed with both denominators rather than one N.
- **(c) TYPED REFUSALS.** `4 of 4` per kind for all four kinds, 0 echoing the refused value, plus `2 of 2` mint-side refusals (an unregistered firm token, a name-shaped raw key) **and a POSITIVE CONTROL** -- a genuinely issued id of that kind is ACCEPTED, so the four refusals are a discriminating instrument and not a requirer that says no to everything. The firm requirer's fourth case is the REQUEST-CONTROLLED raw firm token (`"inflection"`), because for that kind an issued firm id is the correct input and a skip there would have made `4 of 4` a fiction.
- **(d) THE GRAIN, THREE FIXTURES.** `3 of 3`, through `_scope.resolve` AND `directory/handler.resolve` in-process. Account-only: the entry carries NO `relationship_id` and the permitted set is exactly its one account. Multi-relationship: one account listed under three relationships, two of them granted, collapses to ONE id in the permitted set, and resolving through either relationship names the same id. Relationship reaching outside: the permitted set stays `[A_MULTI]`, the resolver carries a `partial_reason`, and the handler answers `ok=false` / `UNSUPPORTED` with `1 of 2` counted -- never the whole, never a silently narrowed set dressed as a whole one.
  **ONE DEVIATION FROM THE FACE'S WORDING, stated:** the face says the account-only case is `relationship_id: null`. `DirectoryEntry` types `ids.relationship_id` as a bare string and does not require it, so a literal `null` FAILS the schema; the fixture OMITS the field, which is the same meaning in the shape the contract accepts. `_scope._relationship_index` reads `ids.get("relationship_id") is None` and so treats both spellings identically.
- **(e) THE PROJECTION RESOLVES.** RAW upstream keys read from the tables `raw_keys.json` CITES (49F `fact_allocation_account_map.account_number` padded by the producer's own `_pad10`; INF `accounts_v2.account_id`; COT `fact_allocations.AccountID`), 25 per firm, granted through `_scope.advisor_grant` with `_ids.projection_for(firm)` as `id_projection`: **`0 of 25` UNPROJECTED-ID for all three firms**, 25 of 25 projected, resolved in the directory 25/25 (INF), 25/25 (COT), 24/25 (49F -- the one gap is `NOT-IN-DIRECTORY`, a population fact, printed by reason). **NEGATIVE CONTROL:** the same keys with NO projection resolve `0 of 25` and every gap is NAMED `UNPROJECTED-ID` (`25 of 25`) -- without that control the arm would prove nothing.
- **(f) THE LAYER LANDED.** `irpt-common:5`; live `CodeSha256 = ZUcsQUOsc3lT2cKlnur5rCAZc/a0rCkKvU5pjg11U20=` EQUAL to the built zip's own sha (content, never filename); both consumers on `:5` (**2 of 2**); the ledger entry `20260911T1256Z_irpt-bckend-rt3_deploy_completion.md` CLOSED with 0 legs open; the OPEN sentinel committed BEFORE the act at `7faaa119df` and removed by the close at `7a56abaccb`; both roots plan `No changes.`

**INSTRUMENT TRAP MET AND FIXED, recorded because the failure was SILENT:** the first run of arm (f) read an EMPTY layer version with `rc=0`. `.tools/aws.cmd` runs through `cmd.exe`, which ate the `&` in the JMESPath `max_by(LayerVersions,&Version).Version` as a command separator -- a false ABSENT, not an error. The battery now queries `LayerVersions[0].Version` (the API already returns newest-first) and the comment in the source says why.

### `RT3-AC2` -- JUDGMENT, RECORDED, NOT SELF-GRADED

Output for `3.0.0_SA_CVO` at L9. No verdict is offered.

**(i) Which raw key the directory USED in round 1 versus the one declared now, and what that means for any artifact a consumer read in round 1.**
INF: round 1 minted from `accounts_v2.account_number` (`acct#9d4420e3`); now `accounts_v2.account_id` (`1003`). COT: round 1 minted from `fact_allocations['Account Number']`, a MASKED string (`*****4583`); now `fact_allocations.AccountID` (`acct#7d2371a7`). Consequence: **every INF and COT account id in every round-1 directory artifact is a DIFFERENT STRING from the id this cell mints for the same account.** The ids did not move because the grammar moved -- the grammar is byte-identical and `opaque_firm('49financial')` still reproduces `fir_c9fc04650e2134d6ea033da2`, the id round 1's own fixtures pinned -- they moved because the INPUT changed. A consumer that stored a round-1 INF or COT account id holds a handle that resolves to NOTHING after this cell; a consumer that stored a 49F id is unaffected. No production artifact was overwritten here (QA prefixes only), so the exposure is limited to whatever read the round-1 QA objects; the production first-mint rides IB-rt-6, and whether that needs a migration or a clean mint is a decision this cell does not own. The masked COT key is the sharper half: a masked string is not a key at all, and any round-1 COT id minted from it was never able to join anything.

**(ii) Whether the salt/grammar choice makes an id re-identifiable from a public key space.**
The grammar is `sha256(ID_NAMESPACE|firm|kind|raw)[:24]`, and `ID_NAMESPACE` defaults to the LITERAL CONSTANT `IRPT_DIRECTORY_ID_NS_V1`, which lives in source and in the layer -- **it is a namespace, not a secret**. So an adversary who holds the namespace and a candidate key space can re-derive ids by enumeration, and the account key spaces are small: a 10-digit zero-padded account number is `10^10` candidates, which is hours on commodity hardware, and a real adversary would not enumerate blindly but confirm a SPECIFIC account number they already hold. **An opaque id is therefore a STABLE HANDLE, not a privacy barrier, against anyone who already knows a raw key and the namespace.** What it does buy: it is not guessable from the id alone, it carries no upstream structure, and the firm is in the payload so the same raw key under two firms mints two ids. `ids.py` reads `IRPT_DIRECTORY_ID_NAMESPACE` from the environment, so a SECRET salt is a configuration change and not a code change -- but setting one re-mints every id in the estate, which is the same migration question as (i) and is why this cell did not set one on its own authority. Collision: 24 hex = 96 bits, birthday bound ~2^48; at 7,480 ids per firm the collision probability is ~1e-24, and `_mint` is deterministic, so equality is exact rather than probabilistic at these sizes.

**(iii) What the equal-ids proof cannot show about a client that exists in one source and not another.**
The join proves that for every account BOTH producers hold, the two ids are the same string. It is silent on every account only one producer holds, and those sets are not small: 49F has 17 holdings accounts the directory does not carry and 1,624 directory accounts with no holdings row; COT has 124 holdings accounts absent from the directory; INF has 84 directory accounts with no holdings row. **A missing account and a mis-keyed account are INDISTINGUISHABLE to this arm** -- both appear as "not in the join" -- so a systematic drop in either producer would leave arm (b) at 100% of a quietly smaller population. The arm also cannot show the declared key is the RIGHT key: two producers reading the same WRONG field would agree perfectly, and the only defence here is the declaration's `file:line` citation plus the coverage figure, both of which are human-checkable rather than machine-proved. Nor does it reach the CLIENT grain: the join is over account ids, so a client that exists in the directory and not in the holdings source (or a household split differently by the two builds) is invisible to it -- what arm (d) proves about clients is only that the account-vs-relationship grain does not widen a permitted set.

---

## 3. PREFLIGHT (recorded per the face)

- **comp-iam Phase 1** -- `comp-iam service irpt-performance-adapter` and `comp-iam service irpt-narrative` (the two-argument form is not accepted by the tool; run once each). `irpt-performance-adapter-role`: 1 statement, 3 `logs:*` actions on its own log group only. `irpt-narrative-role`: 4 statements -- its own log group, read-only DynamoDB on two news tables, `s3:GetObject` on `opal-data-news-v2/trending_reports/*`, and a prefix-CONDITIONED `s3:ListBucket`. **Neither role was touched by this cell**: a layer version change is a function-configuration change, not a permission change.
- **comp-iam Phase 2** -- `comp-iam gaps`: `Total: 12 missing | 291 deny-present | 1 coverage-unknown | 2 resource-mismatch across 31 service(s)`; resource plane 836 calls across 96 mapped roles. **0 rows name `irpt-performance-adapter` or `irpt-narrative`** (measured by counting matching lines in the tool's own output). BLIND SPOT carried from the face: DESIRED plane only, and a GRANTED-BROAD wildcard cannot be falsified by a resource check.
- **comp-schedule** -- DECLARED-NOT-APPLICABLE at the cut and still true: this cell creates, changes and fires no schedule, rule or trigger.
- **comp-adversary** -- the assignee's instrument at report time; its findings are the three surprise rows above.

## 4. BOUNDS HELD

NO live vendor call (every read is S3, Lambda or Terraform on Opal infrastructure). No monitor, alarm, SNS or SES. No cross-firm read: each firm's artifacts are read from that firm's OWN bucket. No credential in any artifact -- `IdRefused` carries the value's SHAPE (type, length, character class) and never the value, and no raw upstream key is printed in this document, the battery output or the surprise rows. No served output touched: all rebuilt artifacts are under `investor-reporting/qa/`. Deploys through `.tools/safe-apply.sh` with the sentinel committed before the act and the ledger closed before the grading reads.
