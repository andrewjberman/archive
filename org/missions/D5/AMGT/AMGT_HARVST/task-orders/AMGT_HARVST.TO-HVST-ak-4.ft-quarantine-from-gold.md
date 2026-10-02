# AMGT_HARVST task order -- `HVST-ak-4` -- ROUND 38 AMENDMENT 1 (CTO msg 28715 ruling 3; 28731): THE ft QUARANTINE -- ft ROWS EXCLUDED FROM GOLD SERVING AND EVERY DOWNSTREAM USE, THE BYTES KEPT

<!-- ===================== WORKER FACE -- this is the WHOLE of the worker's context ===================== -->

<decomp_ref>
<decomp_doc>org/missions/D5/AMGT/AMGT_HARVST/decompositions/AMGT_HARVST_DECOMP.md</decomp_doc>
<owned_cells>HVST-ak-4</owned_cells>
</decomp_ref>
<issued_to>0.9.0_WK_AMGT_HARVST~90</issued_to>
<issued_by>2.0.0_SA_COO~H</issued_by>
<placeholders>NONE</placeholders>
<preflight>
comp-schedule: RUN at L5 (--drift) -- no schedule touched.
comp-iam: RUN at L5 -- LOCAL code and plants. No S3 write and no delete: the bronze and silver ft bytes are KEPT, and deletion is Andrew's word only. Served gold moves only at the issuer's rebuild #6, under its own never-widen pair. AC2 and AC3 read live gold and silver read-only through a capturing client that sends no put. 0 Lambda calls.
comp-adversary: RUN at L5 -- the adversary is a quarantine that hides ft from mention but leaves it in daily coverage, event rows, window rows or the scorer's queue; a filter that also drops a non-ft row; a "quarantine" that deletes bytes; or one that keys on a string an older row spells differently.
</preflight>

## 0. THE CELL

FT's terms, read verbatim, bar any automated read, storing and ML use of FT content: the Copyright Policy, T&C s.3.2,
and s.3.5 ("to generate any data"). The CTO ruled that the stored ft articles are QUARANTINED, not deleted: ft rows are
excluded from gold serving and from every downstream use, and the bytes are kept.

`lib/research/harvest/publication_gold.py` already holds one quarantine at KEY level for sa (HVST-ae-1):
`sa_quarantined_keys` (around line 891), which `build_daily` applies to the mention snapshot (around lines 865-867).
This cell adds the same at PUBLISHER level for ft, and it reaches every gold builder and both consumers:
- `ENABLED_PUBLISHERS` (around line 384) is `tuple(sorted(SOURCE_FOR_PUBLISHER))`, the denominator of daily coverage;
- `build_mention` (around line 1031) reads silver articles;
- `build_daily` (around line 859) reads the mention snapshot, every source's `listing_hit`, and the run records;
- `build_event` (around line 1505) reads the mention snapshot and a headline map;
- `lib/research/harvest/finbert_sentiment.py` `score_missing` queues articles for FinBERT;
- `lib/research/harvest/window_tone.py` `build_window` reads the mention snapshot.

## 1. THE BUILD (LOCAL)

1. In `publication_gold.py`, add `QUARANTINED_PUBLISHERS = {"ft": "<reason>"}`. The reason names FT T&C s.3.2/s.3.5
   and the Copyright Policy, the CTO ruling (msg 28715), "bytes kept; deletion is Andrew's word".
   - Add one helper, `is_quarantined(row)`, using `_row_publisher(row)`, so a row that predates the `publisher`
     column is caught by its key prefix.
   - Grade daily coverage over `GRADED_PUBLISHERS` = `ENABLED_PUBLISHERS` minus the quarantined ones. Every place that
     grades daily coverage, or writes `publishers_enabled`, uses `GRADED_PUBLISHERS`.
2. Exclude quarantined rows in each place below. A snapshot written before this change still carries ft, so every
   reader filters the rows it reads, not only the writer:
   - `build_mention`: no row for a quarantined publisher's silver article;
   - `build_daily`: quarantined rows leave the mention snapshot, the listing hits and the run records; ft never appears
     in `publishers_covered_codes` or `publishers_found_codes`;
   - `build_event`: quarantined mention rows leave before `event_rows`;
   - `finbert_sentiment.score_missing`: a quarantined publisher's article gets label null and `unscorable_reason` set
     to the quarantine reason, with 0 calls (this is PRD v0.16's FWD-16 clause);
   - `window_tone.build_window`: quarantined mention rows leave before `build_window_rows`.
3. Nothing is deleted or written to S3. Bronze, silver and the outbox stay untouched.
4. Plants in `lib/research/harvest/test_ak4_ft_quarantine.py`, with no network:
   - (i) a ft silver article gives no mention row, and a non-ft row is byte-identical to the build without the
     quarantine;
   - (ii) a mention row with `publisher` None and key `ft:...` is quarantined;
   - (iii) daily rows built from a fixture containing ft listing hits and run records never name ft, and
     `publishers_enabled` equals `len(GRADED_PUBLISHERS)`;
   - (iv) event rows built from a fixture with a ft burst carry no ft article;
   - (v) `score_missing` on a ft article makes 0 invoker calls and gives the reason;
   - (vi) window rows exclude ft articles from articles_total;
   - (vii) a mutant that filters only in `build_mention` fails (iii).
5. The research suites stay green except the 3 known stale tests (row Z-S68):
   `python -m pytest lib/research/harvest -q`. Report the counts before and after.

Worktree: `C:/Users/Opal Bloomberg/Desktop/wk-hvst-r36-90`, branch `wk-AMGT_HARVST-90-r38d`, cut from CLOUD at this
amendment's commit (sparse cone, which includes `lib`). Do not touch any `.runtime` directory.

<paths>
lib/research/harvest/publication_gold.py
lib/research/harvest/finbert_sentiment.py
lib/research/harvest/window_tone.py
lib/research/harvest/test_ak4_ft_quarantine.py
org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~90/
org/missions/D5/AMGT/AMGT_HARVST/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

## 2. PROOF OF SPEC (each invocation LITERAL; timeout 900)

<proof_of_spec>
  <criterion id="AC1" cell_refs="HVST-ak-4"><invocation>python -m pytest lib/research/harvest/test_ak4_ft_quarantine.py -rA --tb=line</invocation><expect>passed</expect></criterion>
  <criterion id="AC2" cell_refs="HVST-ak-4"><invocation>python org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round38/checks/ak-4.AC2.py</invocation><expect>AC2 RESULT: PASS</expect></criterion>
  <criterion id="AC3" cell_refs="HVST-ak-4"><invocation>python org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round38/checks/ak-4.AC3.py</invocation><expect>AC3 RESULT: PASS</expect></criterion>
</proof_of_spec>

- AC2 builds mention twice over 5 securities that carry served ft rows: once as shipped, and once with the quarantine
  emptied as the control. The only difference allowed is the ft rows.
- AC3 builds daily over the same securities. Both send no put.
- Run them from your worktree. If one cannot reach AWS there, mark it "issuer re-runs at the base after merge".
- INSTANCE NAMED EXACTLY
  `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~90/AMGT_HARVST.TO-HVST-ak-4.ft-quarantine-from-gold.proof_of_spec.json`
  with `to_id` `AMGT_HARVST.TO-HVST-ak-4.ft-quarantine-from-gold`.
- Do not edit this order file: the issuer flips its status.

<!-- ===================== RECORD FACE -- does NOT travel to the worker ===================== -->

**ISSUER NOTES:** CTO msg 28715 ruling 3 (analysis addendum 2 @ce138d2314), and 28731: rebuild #6 carries the ft
quarantine ALONE. The event rebuild and all tone or window serving are HELD on Andrew's card
(`CARD_HARVST_PUBLISHER_TERMS_20261002.md` @8d20bc24c8).

At the cut, served gold holds 926 ft mention rows of 23,691, and 5 daily rows naming ft in their codes. The cell
follows ak-1 on `~90`, because both write `publication_gold.py`.

After the merge: rebuild #6 (mention and daily) runs under a NEW never-widen pair. The COO half names the blast radius:
- mention: the 926 ft rows go; every other row gains the 3 tone fields as NULL (ak-1's schema; no value, because
  FWD-16 is held) and nothing else moves;
- daily: ft leaves the coverage codes, and `publishers_enabled` goes from 5 to 4 on every row;
- the rollback is the BEFORE snapshots as newer parts.
The CTO half is owed. The served events are NOT rebuilt (28731).

**COMPLETE 2026-10-02 ~21:3xZ (issuer):**
- AC1 PASS: 11 passed (worker). Merged @eff5c79d35.
- At the base:
  - AC2 PASS (`round38/ak-4.AC2.issuer_grade.txt`): shipped 1,920 rows with 0 ft; control 1,978 with 58 ft; 1,920
    non-ft keys in both and 0 differing; PUTS SENT 0.
  - AC3 PASS (`ak-4.AC3.issuer_grade.txt`): 1,375 daily rows, 0 naming ft, publishers_enabled 4 on every row.
- Row Z-W90-S22: 4 tests pinned ENABLED_PUBLISHERS as the graded set. It is resolved by the issuer's direct act (row
  Z-S69): the two test files now read GRADED_PUBLISHERS. The suite at the base reads 317 passed and 3 failed (the
  Z-S68 three only).
- Next is the rebuild #6 signing dry run (`round38/gold_rebuild6.signing.py`, ft quarantine only), then the COO half.

<risk>SERVED</risk>
<worker_class>worker</worker_class>
<status>complete</status>
<round>38</round>
<workstream>ftquarantine</workstream>
<slot>~90</slot>
<fabric>site-z</fabric>
