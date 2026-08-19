# ADVI_BDPARITY.T2-DIMS -- dim_portfolio_group + bridge_group_account (BUILT + MEASURED; one gap DECLARED)

**Seat:** `0.4.0_DS_ClientPlatform~B` | **Issued by:** `2.0.0_SA_COO` | **Built:** 2026-08-19 ~2250Z
**TO:** `org/tier2_senior/0.4.0_DS_ClientPlatform~B/task_orders/ADVI_BDPARITY.T2-DIMS.portfolio-group-and-bridge.md`
(absorbing identity-spine **WP-2** -- one logical producer, one home)
**Tool:** `data/assets/scripts/gold/runners_49f/bd49f_dim_portfolio_group.py`
**Upstream:** `ADVI_IDSPINE.WP-1` silver `fact_bd_allocation` @`b885d682f8` (gate DISCHARGED)

---

## 0. HEADLINE: FOUR OF FIVE CRITERIA MET; T2-3 IS HALF-MET AND THE MISSING HALF IS NOT MINE TO BUILD

`Primary Portfolio Group` -- **BD dimension 436, the partition key the ruled basis names** -- **is not
in the feed.** Persisted template 390224 does not select it. So `is_primary` is emitted **all-null with
a declared reason** and the true-partition half of T2-3 is undeliverable until the vendor template is
amended. Everything else is built, measured, and converges with the T1 oracle.

**BOOK BASIS = GROUP-BASED**, stamped as columns on both tables and into the manifest. Andrew-direct
2026-08-19 ~2012Z *"All approved"* @1e0ec3b079. Serving remains P4-class through CTO.

---

## 1. THE MEASUREMENT (as_of 2026-08-18)

```
  silver rows in                    : 30577
  distinct (group,account) in silver: 29907
  bridge_group_account rows         : 29907
  dim_portfolio_group rows          : 201
  distinct accounts                 : 6155
  group_class census (MECE, 201 groups):
      advisor-book     186
      local-ops-view     9
      division           5
      firm-wide          1
  is_primary populated              : 0 of 29907  <- ABSENT UPSTREAM, declared not derived
```

| portfolio group | group_class | accts | book (group grain) |
|---|---|---:|---:|
| 49F Schwab AUM | firm-wide | 2989 | $745,570,084.08 |
| Alex Bright - Local Ops | local-ops-view | 2230 | $546,934,316.63 |
| Dallas Support | division | 1498 | $455,066,617.86 |
| Collin Plotts | advisor-book | 1771 | $447,585,918.41 |
| Lane Curry - Local Ops | local-ops-view | 1361 | $400,253,046.71 |
| Travis Penfield | advisor-book | 318 | $392,556,451.10 |
| 49 Private Wealth | division | 188 | $347,710,752.26 |
| Erick Webb - Local Ops | local-ops-view | 1187 | $329,704,079.66 |

**Travis reproduction (TO amendment 4):** his **$392,556,451.10 membership view IS derivable** and
matches the T1 oracle to the cent. The **primary-only view is NOT derivable** -- it needs dim 436.

---

## 2. ACCEPTANCE

### T2-1 DIMS LAND IN THE 49financial GOLD GRAMMAR -- **PARTIAL, deliberately**
Both tables build as parquet with a manifest in the `{table}/date={D}/` shape. **They are NOT minted to
`opal-data-49financial/gold/advi/dimensions/`,** and `--upload` is wired to **REFUSE** with its reason.
Two grounds, neither of them mine to overrule: WP-1's own silver partition is not minted either (DS base:
*"the first mint is not self-authorized yet, it is with COO"*), and minting a gold artifact whose declared
upstream does not yet exist in S3 would make the tables read from a different source than the ratified one
-- the two-homes defect, created by the fix for it.

### T2-2 BRIDGE COVERS THE EXPORT'S FULL MEMBERSHIP -- **PASS**
`export memberships 29907 | bridge memberships 29907 | missing 0 | extra 0 | coverage 100.0000%`

### T2-3 ZERO CROSS-GROUP SUMS EXPRESSIBLE -- **HALF MET, and the halves are named**

**MET, and it is the load-bearing half: the bridge carries NO money column.** Verified
`bridge money columns: []`. The double-count arises from spreading an additive quantity across
memberships; the quantity is not on the membership grain, so **the fan-out product cannot be
constructed** -- not "should not be", cannot. The book figure lives only at group grain in
`book_mv_not_additive_across_groups`, whose name carries its own non-additivity, with `additive: false`
in the manifest.

**The `--guard` fires loud:**
```
  naive SUM over dim rows (THE FORBIDDEN ACT) : $8,252,695,569.91
  distinct-account universe (NOT a book)      : $1,550,733,057.94
  phantom multiple                            : 5.32x
  bridge money columns                        : 0
  is_primary non-null                         : 0 of 29907
```

**NOT MET: a TRUE PARTITION.** Each-account-in-exactly-one-group requires dim 436. **The consequence is
the safe direction and worth stating precisely: absent the key these tables cannot produce an
account-partitioned total AT ALL -- correct or incorrect. The failure mode is CANNOT-ANSWER, never
ANSWERS-WRONGLY.** But it is a gap, and it is declared rather than papered over.

### T2-4 NO SERVED CONSUMPTION -- **PASS** (4 probes)
Not in `chain_49f_entrypoint.py:_stage_list` (0 refs) · nothing imports or invokes it · no `boto3`/
network primitive reachable in the write path and `--upload` refuses · `platinum/advi/49financial/` = **0 keys**.

### T2-5 proof instance VALID rc=0 positional T2-1..T2-5 -- see the instance.

---

## 3. THE PARTITION KEY -- WHY IT IS ABSENT AND WHY I DID NOT MANUFACTURE IT

Measured on the landed 2026-08-18 export, **all 92 vendor columns enumerated**:

| probe | result |
|---|---:|
| columns containing `primary` | **0** |
| columns containing `group` | 2 (`Portfolio Group`, `Portfolio Group Market Value`) |
| **positive control:** columns containing `portfolio` | **8** |

The positive control is what makes the zero a finding: the matcher discriminates, so the absence is real
and not a broken search. The pull sidecar's own level census agrees (`"Portfolio Group": 2`).

**Silver is not at fault.** Rule 17 preserved everything the vendor sent. **Preservation is not
provision** -- Rule 17 guarantees nothing is LOST; it cannot guarantee something was ever SENT. The gap
is upstream at the template's dimension selection and is fixable only vendor-side (add dim 436, re-pull).
*(DS base independently re-derived 0/2/8 and retracted their "every field you need is present" line.)*

**I did not derive `is_primary` from group naming**, and the TO forbids it explicitly. A heuristic
partition key would be **our reading of vendor strings dressed as a vendor assertion**, and it would be
invisible downstream *because it would look populated*. **An absent key is safer than an invented one.**

**The deliberate asymmetry with `group_class`, which I DID derive:** the TO sanctions that derivation
("derived per the transcript ruling") and forbids the other. The difference is real -- `group_class` is a
label we assign for our own navigation, falsifiable by reading the name; `is_primary` is a vendor
assertion about which group *owns* an account, and nothing in a name can establish it.

---

## 4. `group_class` -- THE MECE AXIS (Rule 24), AND THE JUDGMENT I DECLARED RATHER THAN BURIED

**Axis intent (24 iii):** *what KIND of book is this group?* One intent, one axis.
**Grain (24 ii):** every value is a property of one portfolio group.
**MECE (24 i):** rules are ordered, first match wins (exclusivity is structural); exhaustiveness is
enforced by `_classify` **raising on an unmatched name rather than defaulting** -- a silent default is how
a future "Houston Support" quietly becomes an advisor-book.
**State (24 iv):** all four values derive from the same landed column; one remedy moves them together.

**DECLARED JUDGMENT:** firm-level support/ops units not attached to a named advisor (`Dallas Support`,
`Centralized Client Ops`) are classed `division`. Under this axis's intent they are an org unit's view.
The alternative is a fifth value splitting business-division from support-unit -- **a taxonomy act for
the axis owner, not a silent pick by a producer.** Recorded, not decided.

**A measured trap in the classifier:** a naive person-name heuristic misclassifies `Dallas Support`
(1,498 accounts) as an advisor book. An org-token list fixes that but must **exclude city and given-name
words** -- measured false positives on real advisors: `Austin Bost`, `Austin Thompson`, `Faith Austin`,
`Lincoln Rock`, `Weston Kammer`, `August Vordenbaum`. *A token list that matches a person's name does not
classify groups, it mislabels advisors.*

---

## 5. THE SUPERVISION SLEEVE -- FOUND HERE, CORRECTED BACK INTO T1

The T2 producer and the T1 oracle disagreed on 14 of 201 groups. Chasing it found a **real vendor grain**:
`Account Supervised` splits an account into **Supervised** and **Unsupervised** slices, each with its own
market value and allocation. **They must be SUMMED**, proven not assumed -- for every sleeve,
`account_market_value / account_allocation == portfolio_group_market_value` **to the cent** (both divide
the same portfolio total), positive-controlled against an ordinary single-sleeve account. The corrected
key `(group, account, supervised)` has constant market value on **29,926 of 29,926 keys, zero exceptions**.

**3 accounts, 19 keys, 12 of 201 groups, $24,605,360.68 understated.** Both tools fixed; **Travis is not
among the 12**, so the T1 headline stands. Post-fix the two producers **converge across all 201 groups**
(max |delta| $0.005, total $0.18 -- rounding, not computation) despite reading different sources with
different dtypes.

**This also explains WP-1's own unexplained residual:** their `(PG, PortfolioID, AccountID, Relationship
ID)` key still lost 24 rows with no reason recorded. **The supervision axis is the missing term.** Routed
to `0.4.0_DS_ClientPlatform` as a grain-statement amendment.

---

## 6. CONTROLS

- **DETERMINISM: STABLE** -- two runs, all three outputs byte-identical
  (`dim` `5c957dc95b4c791c`, `bridge` `36978771eb2a9e74`, `manifest` `c4053fb3bf08dee0`).
- **CROSS-IMPLEMENTATION AGREEMENT** -- the strongest control available here, because the legs differ in
  derivation: bronze xlsx / positional / float vs silver parquet / named / decimal128. 201 groups, max
  |delta| $0.005.
- **SLEEVE CORRECTION** -- caught by that disagreement. Two artifacts agreeing proves little when they
  share a derivation; **these two do not share one, which is why the disagreement was informative.**

---

## 7. RESIDUALS

1. **BD dim 436 added to template 390224 + a re-pull** -- vendor-side, same egress class as T1's qt6
   re-run, held by `4.0.0_SA_CRO~A`'s continuing grant. Unblocks `is_primary`, the T2-3 partition half,
   and the primary-only Travis view. **It also improves the DAILY feed permanently, not just this build.**
2. **The gold mint** -- COO's call, sequenced behind WP-1's own silver mint.
3. **338 `(group, portfolio, account)` keys carrying two Relationship IDs** (DS base's WP-3 surface).
   Not merged, not resolved; my tables carry them as distinct silver rows collapsing correctly to one
   membership. A declared position is owed at WP-3.
4. **`group_class` fifth-value question** (support-unit vs business-division) -- axis owner's call.

## 8. COMPILER TOOLS

`comp-find --name "*bd_allocation*"` (1 hit / 27,010 files) located the WP-1 converter so the producer
could be exercised against the **ratified upstream** rather than a substitute source. `comp-find` content
probes supplied the T2-4 no-consumer denominators. `.tools/commit-gate.sh` on both scripts: BLOCKED first
on a real ruff finding (unused `Counter` import), fixed, then clean on 2 files.
`.tools/proof-of-spec-check.py` on the instance.
