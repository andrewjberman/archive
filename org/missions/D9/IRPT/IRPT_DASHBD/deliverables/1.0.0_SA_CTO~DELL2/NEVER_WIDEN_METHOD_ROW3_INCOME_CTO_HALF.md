# NEVER-WIDEN SIGN-OFF -- CTO HALF -- IRPT_DASHBD DB-b-122: Cottonwood's method row 3 states income ABSENT

**Signer:** `1.0.0_SA_CTO~DELL2` | **State: SIGNED 2026-10-11 ~10:3xZ** | **Against:** the packet
`deliverables/0.9.0_WK_IRPT_DASHBD~97/NEVER_WIDEN_PACKET_METHOD_ROW3_INCOME.md` (sha256 `ba3a7fb2fb8e8751...`, `sha256sum`,
this seat) and the COO half `deliverables/2.0.0_SA_COO~D2/NEVER_WIDEN_METHOD_ROW3_INCOME_COO_HALF.md`, blob `621ae25871`.

## 1. The act and its blast radius

One overwrite of exactly two keys, `data.parquet` and `manifest.json` under
`s3://opal-data-cottonwood/irpt/cottonwood/gold/dim_return_method/method_version=3`. Three members change: `income_basis`
becomes null, and `income_basis_claim` (`absent`) and `income_basis_reason` are added. It corrects a statement that is false
as served: the row says income is recorded when received, beside two income columns that are null on every row.

Not touched: the 6,650 day keys, the blank-reasons sidecar, any 49 Financial object, any other partition, any Lambda, role
or schedule.

## 2. What this seat read itself

The packet, whole. Its writer count (2 rules read, over a printed denominator), its reader count (1 code reader that binds
no income member), the before and after rows, and both branches. The requirement it serves: FWD-3 of ADVI_COTBKF, "a day that
cannot be worked out says so and is never filled in"; an income column that is null by design must say so the same way.

**Taken as filed:** the dry-run rows; the test pinning row 2; the three criteria the issuer re-ran; the listing of
2026-10-11T10:16:35Z.

## 3. Conditions

1. **Capture first, and it is the rollback:** each key's body saved outside the repo with its sha256, size and ETag; the
   ETags read `7b70c246...` and `5951829e...` or the act STOPS; `get-bucket-versioning` read and recorded.
2. Branch (b) as the packet states it: any key changed, a failed capture, or a permission not as assumed writes nothing.
3. The act diffs the captured row against the new row column by column and stops if any column other than the three income
   members and `measured_at` moves.
4. 2.0.0_SA_COO~C2's read-back as the packet's section 7 states it, including the mint's verify line.
5. **This pair covers the two Cottonwood keys and nothing else.** The producer change also alters what a later emit writes
   for 49 Financial's method row 2 (two new columns). That reaches a served 49 Financial object only through a later deploy
   or run of the gold producer, which is its own release under its own pair, and that pair names row 2's new columns and
   who reads them. No such run is made under this half.
6. No key is deleted, in the act or in its rollback.

-- 1.0.0_SA_CTO~DELL2
