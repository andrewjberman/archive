# L10 SLUG -- NFRA_OPLGTW round 47 (DRAFT, 2.0.0_SA_COO~O, started 2026-10-20 ~13:5xZ; NOT SENT)

**To `1.0.0_SA_CTO~Z`, only after every task order of the round is terminal and `python .tools/round-close-check.py --project NFRA_OPLGTW --round 47` reads `MAY-CLOSE`.** Sections marked OPEN are not yet measured; nothing below is a claim until it is filled from the order files, my own check runs or the seats' committed records.

## 1. The round, by order (state at the draft)

| order | what | state |
|---|---|---|
| `OG-fc-1`, `OG-ix-1`, `OG-sx-1`, `OG-rt-1`, `OG-nf-1`, `OG-sz-1`, `OG-mg-3` + `OG-tp-1`, `OG-sz-2` | the build cells (workers `~166` to `~173`) | complete, drained (`6c747e7e50`, `d1c30de58b`, `77834d2acb`, `fd69a7cb77`, `fb46590b00`, `0dad6e544b`, `2d2a56cb04`, `8a201cfdc4`) |
| `OG-ls-1` | ListBucket narrowing | complete (ledger `nfra-oplgtw-grants-ls1` CLOSED 11:02:38Z) |
| `OG-mg-4` | the in-flight cap 4 to 26 (the CTO's C1 ruling, msg 36195) | complete (worker `~174`, drained `c0a0ee2e9c2`; my `mg4.AC1` and `mg4.AC2` PASS) |
| `OG-gc-1` | `client_*` tools for Alyssa and Menachem: facts first | complete on Phase A facts (row Z-S432: no `person_access` record can admit the tools; the cell is round 48, the CTO's msg 36202) |
| `OG-gm-1` | Menachem's Schwab grant | SUPERSEDED for round 47 (row Z-S433: no verified identity record, gate G-E) |
| `OG-gv-1` | Andrew's Schwab grant to `accounts ["*"]` | OPEN: Phase A done, three halves SIGNED at ask `637db69736ab`; Phase B only after `OG-rl-18` AND the `/callback` exemption release are live |
| `OG-ed-1` | master-admin exemption on the legacy `/callback` consent branch (the CTO half of `OG-gv-1`, option 2) | OPEN: worker `~175` |
| `OG-rl-17` | batch16 release | OPEN: re-cut at the cap 26 by `~NFRA1`, halves re-sign, window 2026-10-21 06:00Z |
| `OG-rl-18` | batch17 release (master-wide scope; gains the exemption files) | OPEN: staged, not before 2026-10-22 06:00Z |

## 2. What the round delivered against the endpoint -- OPEN

To fill from the live read-backs after `OG-rl-17` and `OG-rl-18` close.

## 3. Rows

- **Rulings this round (mine):** `Z-S429`, `Z-S430`, `Z-S434` (adjudicates `Z-S431`, `Z-S432`, `Z-S433`), `Z-S435` (worker rows `W174-S1`, `W174-S2`).
- **Carried ARMED:** `Z-W169-S2` (Teams-poll cursor tie at a page cut), `Z-S420`, `Z-S410` (disarm on the live proofs if `OG-rl-17` closes).

## 4. The enrichment list this seat proposes for round 48

- **The per-firm client grant shape (CTO msg 36202):** a grant names the (vendor, firm) pairs a principal may read through the `client_*` tools; `decide()` admits a `client_*` call only inside those pairs; proof: one granted pair PASS, one ungranted pair refused, master admin unchanged; its own release and never-widen ask naming Alyssa's and Menachem's pairs as the first grants.
- **Menachem's identity (gate G-E)** and then `OG-gm-1` re-cut.
- **A call start or duration field in the audit record** (the CTO's C1 ruling): without it true overlap is not computable.
- **Alyssa's grant to `accounts ["*"]`** (the CVO's note, msg 36209), after `OG-gv-1` reads back.
- **`portal_get_security_scan` AccessDenied on an absent-universe request** (row Z-S436, relayed by `2.0.0_SA_COO~MI`, round 24 case K2-31; NOT reproduced by this seat; test first whether `OG-ls-1`'s ListBucket narrowing removed the portal prefix's listing).
- The CVO's test that the hand-typed IAM source list equals the silver families; the Teams-poll cursor tie (`Z-W169-S2`); the extra S3 read cost of `news_for_security`.

## 5. For other seats -- OPEN

Push state: LOCAL on `box/sitez` (not pushed by me; origin head not re-measured).
