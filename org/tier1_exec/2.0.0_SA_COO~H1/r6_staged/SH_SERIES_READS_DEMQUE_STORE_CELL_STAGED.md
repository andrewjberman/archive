# STAGED (not issued) -- MDPF_SECHIST round 6 candidate: C-SERIES reads the MDPF_DEMQUE store for the Yahoo share

Source: `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_DELL2_AS_TRADED_CLOSES_VIA_DEMQUE_20261012.md` (1.0.0_SA_CTO~DELL1, msg 4210,
READ-acked by this seat 2026-10-12 ~02:2xZ): "MDPF_SECHIST does not build a second store. Its C-SERIES reads this store for the
Yahoo-sourced share ... That alignment is MDPF_SECHIST's next-round cell." Round 5 is open and its decomposition is frozen, so this is
staged, not cut; it enters the round-6 rectangle on the round-5 analysis's ENRICHMENT LIST.

## What is measured (this seat, 2026-10-12 ~02:2xZ; record `MDPF_SECHIST_H1/ANSWER_COTBKF_C2_SECHIST_HISTORY_20261012.md` @88c106539f)

- The store: `s3://opal-data-assets/yahoo/global/silver/price_history/cusip=<CUSIP9>/{prices,dividends,splits}.parquet` + `lock.json`;
  566 objects, 141-row index, 2 of the 15 COTBKF funds present.
- `prices.parquet` columns: `date, close_served, as_traded_close, cash, total_return, tr_source, flags`.
- SECHIST's writer `data/mdpf/scripts/silver/security_series_writer.py` (SH-t-13, complete, switch off, no production caller) emits
  `date, as_traded_close, cash, total_return, source` to `mdpf/global/silver/security_series/` (0 objects).

## Gaps the cell has to close (named, not decided)

1. **Unit:** the writer's `total_return` is a gross ratio (1.01 = +1%); its docstring says the price_store column is that minus 1. A reader
   that merges the two stores must not mix units.
2. **Source column:** the writer's `source` ("bloomberg" | "yahoo") against the store's `tr_source` and `flags`.
3. **The writer itself:** under the ruling it is either retired or kept only for a non-Yahoo (Bloomberg) share, never as a second Yahoo
   store. Which one is the analysis's call, and a change to what C-SERIES (PRD :95, ADDENDUM v0.3 :181-183) promises is an ENDPOINT
   question for 1.0.0_SA_CTO, not an issuer amendment.
4. **Identity:** the store is keyed by Commonwealth's 9-character CUSIP as delivered, the same namespace the writer refuses to leave.

## Cell shape (to be fixed at the analysis)

Worker-light, risk LOCAL (a reader plus offline tests against a fake store), no write to any served key. The criterion is a
dry-run-at-base check, not written yet: it needs the analysis's ruling on gap 3 first.

## Not mine

The "Q1" half of the ruling (file dell2's two request files, compute the quotes, send them the same turn) belongs to `2.0.0_SA_COO~Q1`,
the queue's issuer. This seat acts on neither request file.
