# W4 — 0833 LANDING FACTS (0.6.2's half of the joint deliverable)

**For:** `0.4.0_DS_ClientPlatform` (column-census half) · **Workstream:** OPAL_RUNNERS W4 — the 49F-refactor falsifier
**Agent:** `0.6.2_AE_PartnerETL` · **Vintage:** live S3, 2026-07-14 ~03:15Z · **archetype:** VALIDATE
**Rule:** read-only; denominators enumerated at run time (13b); every claim carries its method.

DS owns the COLUMN side (what each type carries vs what Groups A/B consume). This is the LANDING side: the
denominator his census sits on. **Read the 0833 bytes from the monolith copy** — it is terminal and 3-tier
verified; staging is byte-identical by proof, not assertion.

---

## THE CONTAINER CHAIN (CTO rider c) — inherit the structure, not the trap

```
s3 object:  {master}.CRS{YYYYMMDD}.{TYPE}.zip
  layer 1:  member "{master}.CRS{YYYYMMDD}.{TYPE}.zip"   <- ANOTHER zip (starts PK\x03\x04)
  layer 2:  member "CRS{YYYYMMDD}.{TYPE}"                <- the pipe-delimited payload (H1/H2/D1[/D2]/T1)
```

**Depth 2, both masters, no divergence.** A parser that unwraps ONE layer reads the inner zip's *compressed
bytes* as text, finds no H1, and returns a clean all-zero column set — which on this falsifier reads as
"0833 cannot support Groups A/B." DS positive-controlled `crs_reader.py` against
`08335338/.../rps/20260710/...`: it unwraps both layers, finds D1 93,406×58 + D2 7,144×34, and **reconciles
to the T1 trailer at 100,550.** Immune to the trap, and a zero-column result from it is a T1 hard-raise, not
a silent empty (CTO rider b, satisfied structurally).

**PROVENANCE — is the nesting OURS or the VENDOR's? Grounded at the producer, not inferred.** Both producers
(`sdd-daily-pull.ps1`, `sdd-backfill-08335338.ps1`) were checked: neither compresses anything. The
`SerializeWithCompression` calls in them are SOAP-request serialization, not file zipping. **So bronze is raw
byte-for-byte and Rule 17a is intact — Schwab's SDD REST channel simply ships a zip-of-a-zip.** This is the
"is it ours or theirs" question that has no instrument; it was answered by reading the two producers.

---

## PER-TYPE LANDING TABLE — 0833 / master 08335338 / "49 FINANCIAL"

**Status: TERMINAL** (6,932 objects, stable across consecutive full scans; the 0833 REST backfill is done).
**Monolith ↔ staging object parity: 6,932 = 6,932 (verified this pass).**
Source of truth = `s3://opal-data-assets/schwab/08335338/bronze/{type}/{YYYYMMDD}/`.

| TYPE | partitions | first date | newest date | distinct dates |
|------|-----------:|-----------:|------------:|---------------:|
| acc  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| fam  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| rld  | 753 | 2023-07-12 | 2026-07-10 | 753 |
| rlu  | 12  | 2023-09-01 | 2026-06-05 | 12  |
| rly  | 36  | 2023-07-31 | 2026-06-30 | 36  |
| rps  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| rtu  | 12  | 2023-09-01 | 2026-06-05 | 12  |
| rty  | 36  | 2023-07-31 | 2026-06-30 | 36  |
| sec  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| slm  | 501 | 2024-07-12 | 2026-07-10 | 501 |
| tcf  | 753 | 2023-07-12 | 2026-07-10 | 753 |
| tcfx | 182 | 2025-10-17 | 2026-07-10 | 182 |
| tnn  | 102 | 2024-07-12 | 2026-07-10 | 102 |
| trn  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| uln  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| ult  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| upn  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| upt  | 505 | 2024-07-08 | 2026-07-10 | 505 |
| **TOTAL** | **6,932** | **2023-07-12** | **2026-07-10** | **753** |

### Landing facts DS's census must account for — none of these are column findings, they are DENOMINATOR facts

1. **The types do not share a start date, and that is real, not a gap.** `rld`/`tcf` reach back to
   2023-07-12 (the REST floor); `acc`/`rps`/`trn`/the U-series begin 2024-07-08; `tcfx` only 2025-10-17.
   A "column present since when?" question for Groups A/B must be asked **per type against its own first
   date**, never against the corpus minimum. A role/fee column that exists only in a type starting
   2024-07-08 is not "missing before 2024" — it is a different type's history.
2. **`rlu`/`rtu`/`rly`/`rty` are sparse by nature** (12 and 36 partitions — monthly/quarterly lot/realized
   products), not truncated feeds. Do not read their low partition count as a landing gap.
3. **`fam`/`slm` ship the `CS{MMDDYY}` filename encoding**, not `CRS{YYYYMMDD}` (the two products the
   date-regex traps have always been about). They are in the table under their real dates; a census that
   re-derives dates from filenames must handle both encodings or it will mis-place 1,006 files.
4. **Below the REST floor (2023-07-12): the 257 pre-floor `01_raw` objects** are a SEPARATE leg, currently
   thawing from Glacier (background). They are NOT in this table and NOT in the monolith yet. If DS's
   census needs pre-2023-07-12 history for any type, it does not exist in this tree tonight — flag it, do
   not assume it will appear.

### 0824 / master 08242234 — **NOT REPORTED. STILL MOVING.**

The 0824 wide-history pull is live (3,202 → 3,208 objects in a 20-second window this pass, climbing toward
~5,966). **I will not print a per-type table for 0824 tonight** — every count is a number that was never the
whole set (13b). DS: do not fix a 0824 denominator on anything I send before I MCP you its terminal count.

---

## Method (so the claims carry it — CTO rider a)

- Partition/date facts: `list_objects_v2` over the monolith prefix, keys parsed to `{type}/{YYYYMMDD}`,
  run-time enumerated, two consecutive full scans to establish terminal-vs-moving.
- Parity: independent full scans of the monolith and staging prefixes, object counts compared.
- Container chain: `zipfile` unwrap to non-zip content on real `rps` bytes; producer check by reading
  `sdd-daily-pull.ps1` + `sdd-backfill-08335338.ps1` for any compression call.
- **Not claimed here:** any column content. That is DS's half, and I do not adjudicate what a gap means —
  the gap list to Andrew is joint.
