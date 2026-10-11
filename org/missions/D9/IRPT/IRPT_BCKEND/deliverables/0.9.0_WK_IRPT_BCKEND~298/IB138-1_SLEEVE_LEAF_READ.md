# IB138-1 -- can a served holdings answer carry a sleeve leaf with no security node beneath it?

Order IRPT_BCKEND.TO-IB-pr-440, worker 0.9.0_WK_IRPT_BCKEND~298. READ ONLY. Counts only. Detail: `IB138-1_sleeve_leaf_read.json`; counting code: `ib138_1_count.py`.

## 1. The producer's rule (claim: measured)

Yes, the producer can emit it. The serving code (`infra/aws/lambda/investor-reporting/holdings/snapshot.py:425-438`) builds no node: it keeps every node whose root account is selected and re-derives totals, so what the gold runner emits is served as emitted. Node kinds in the contract (`HoldingsSnapshot.schema.json:222-232`): ACCOUNT, SLEEVE, MODEL_WRAPPER (legacy), MODEL_LEAF, SECURITY, CASH, UNRESOLVED, CATEGORY.

How a sleeve becomes a node: the gold runner makes one level-1 node per account, with the account's custody value. In the SmartX-overlay builder its kind is CATEGORY (since ruling msg 102475), in three flavours read from `hierarchy_path`: Models, SMA Tax, Client (`holdings_49f.py:389`). Three ways it ends with no security beneath it:

- Drill withheld: positions that do not tie to the balance, or a null market value, leave the sleeve at the balance value with no child at all (`holdings_49f.py:472-482`; test `tests/test_holdings_49f.py:257-262` asserts no children; `tests/test_l0_categories.py:58-64` says a childless category is legitimate).
- Cash only: an account with no position rows gets one CASH child (`holdings_49f.py:501-506`).
- A Models sleeve whose model leaf has no assets holds a TARGET CASH node only (`holdings_49f.py:460-466`).

The Eclipse-overlay builder emits a node_kind SLEEVE (':managed') with a value and a MODEL_LEAF child only (`holdings_snapshot.py:1684-1708`). The contract's carrier for such money is `class_totals_remainder` (`snapshot.py:261,317-322`; test `tests/test_aggregates.py:126-151`). Securities under a Models sleeve are basis TARGET, which the aggregates exclude.

## 2. One served answer, one day (the SmartX-overlay firm)

- Read: the index, the accepted manifest, the header and all 188 of 188 parts (191 objects) of the platinum publication; address from `lib/opal_naming.address()`, the builder `publication.py` calls. Key: `irpt/<firm>/platinum/holdings/date=2026-10-07/<revision>.*`, no account id in any key.
- Index VersionId `JtucBrlvOJGxn5bGeDxaZtxjn5bXYFW9`, ETag `5639c030dd91929bdebd1a3ff58ac227`; manifest VersionId `rhncZNedrzimF43VGkEvYwcv8vHo6HPT`; revision `61537f66...f9a5`. Every part was read by its pinned version, size and sha256 matching.
- As-of: business date 2026-10-07 (custody 2026-10-07, overlay 2026-10-08). 7,620 accounts.
- `nodes_total` 154,473 = ACCOUNT 7,620 + CATEGORY 7,620 + MODEL_LEAF 7,553 + CASH 9,203 + SECURITY 122,477. Strict node_kind SLEEVE: 0.
- A sleeve is recognised as node_kind CATEGORY whose parent is an ACCOUNT node (or node_kind SLEEVE). 7,620 sleeves: 6,391 with a security node beneath, 1,229 with none, in 1,229 accounts.
- The 1,229 are labelled by the answer as: 8 `DRILL WITHHELD` fact, no child at all; 1,216 no mark, CASH children only; 5 no mark, a MODEL_LEAF of cash only. Of the 1,229, 333 carry a nonzero amount (7 withheld, 321 cash only, 5 model leaf).
- By path: Client 1,651 sleeves, 1,224 with none; Models 5,962, 5 with none; SMA Tax 7, 0 with none.
- Also: of the 6,391 with a security, 5,957 hold only TARGET-basis securities (the Models sleeves).

## 3. Verdict

Yes: in the one day read for the SmartX-overlay firm, 1,229 of 7,620 account-level sleeves have no security node beneath them (7 carry a nonzero amount and no child at all), though none of its 7 SMA Tax sleeves is among them; this is one firm on one day.

## 4. Control

Planted: an account, a sleeve with two securities, a sleeve with none (the order says four nodes; those parts make five, and five were planted). Planted 5 nodes, 2 sleeves, 1 with, 1 none, 1 account holding; read: the same. `planted == read`.

Nothing was written or served: reads of one firm's published objects only, through `.tools/aws`.
