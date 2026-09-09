THIS IS THE LAPTOP HALF; SITE Z'S RECORD IS THE OTHER HALF; THE PAIR IS GRADED AT L9

# CG-s-22 -- THE SITE-Z EXERCISE OF FWD-7's PERSON HALF, LAPTOP HALF

**Cell:** `CG-s-22` (decomposition v0.6, round 6) · **TO:** `NFRA_CLDGRPH.TO-CG-F-2` ·
**Assignee:** `0.9.0_WK_NFRA_CLDGRPH~1` · **Branch:** `wk-cldgrph-6-1` (LOCAL) ·
**Worktree:** `C:/tmp/wk-cldgrph-6-1` · **HEAD at hand-off:** `2c4e462a7b02c3ea00aadb7f87d209880b108a67`.

**TERMINAL STATUS: OPEN.** `F2-AC3` reads **1**, not `0`, and the order does not flip. The reason is
in s.3 and in row `NFRA_CLDGRPH-W1-S33`, and it is not a local copy of the graph.

**WHAT THIS ORDER DID NOT DO.** No local graph was created, opened or downloaded; no engine ran;
nothing was written to S3; no code was edited. One transport only -- `.tools/comp-kuzu --json` to the
public gateway to the service -- with a second, non-answer request per instant whose ONLY purpose is
the `Date` response header the skew criterion names. Site Z's record was not read and the pair was
not compared: both are `3.0.0_SA_CVO`'s at L9, and this seat cannot see site Z's tree.

## 1. THE RECORD

```json
{
  "machine": "laptop C:/tmp/wk-cldgrph-6-1 (worktree) on the device whose main workspace is C:/Users/AndrewBerman/Desktop/ajb_workspace",
  "question": "D-8's fixed question, unchanged, asked through the thin client to the public gateway",
  "cypher": "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t",
  "transport": ".tools/comp-kuzu --json -> https://mcp.opalinvest.dev/graph/cypher -> the served projection. No local database exists on this machine to fall back to.",
  "instants": [
    {
      "t": "2026-09-09T19:00:00Z",
      "label": "T0",
      "start": "2026-09-09T19:00:00.496Z",
      "end": "2026-09-09T19:00:03.966Z",
      "start_offset_s": 0.606,
      "window_s": 3.447,
      "skew_s": 0.347,
      "gateway_date": "Wed, 09 Sep 2026 19:00:04 GMT",
      "rows_sha256": "3071ef4c4bf5e16c946ffb59e142213cbea0e22d0c1103b0e26ce9890a8930df",
      "vintage": "2026-09-09T14:59:48.778469+00:00",
      "manifest": "86ea84674078",
      "rows_count": 58,
      "canon_bytes": 1535,
      "answer_file": "f2_answer_T0.json",
      "transcript": "f2_ask_T0.txt",
      "ask_rc": 0
    },
    {
      "t": "2026-09-09T20:00:00Z",
      "label": "T1",
      "start": "2026-09-09T20:00:01.107Z",
      "end": "2026-09-09T20:00:06.489Z",
      "start_offset_s": 1.310,
      "window_s": 5.362,
      "skew_s": 0.103,
      "gateway_date": "Wed, 09 Sep 2026 20:00:07 GMT",
      "rows_sha256": "3071ef4c4bf5e16c946ffb59e142213cbea0e22d0c1103b0e26ce9890a8930df",
      "vintage": "2026-09-09T14:59:48.778469+00:00",
      "manifest": "86ea84674078",
      "rows_count": 58,
      "canon_bytes": 1535,
      "answer_file": "f2_answer_T1.json",
      "transcript": "f2_ask_T1.txt",
      "ask_rc": 0
    },
    {
      "t": "2026-09-09T21:00:00Z",
      "label": "T2",
      "start": "2026-09-09T21:00:01.511Z",
      "end": "2026-09-09T21:00:07.450Z",
      "start_offset_s": 2.081,
      "window_s": 5.481,
      "skew_s": 0.056,
      "gateway_date": "Wed, 09 Sep 2026 21:00:08 GMT",
      "rows_sha256": "50170787e39ed1a3de76e536212b5505f8139efeaa5f81c17c4eed7e44fd3821",
      "vintage": "2026-09-09T20:04:09.034708+00:00",
      "manifest": "2ca2ec43cabf",
      "rows_count": 58,
      "canon_bytes": 1535,
      "answer_file": "f2_answer_T2.json",
      "transcript": "f2_ask_T2.txt",
      "ask_rc": 0,
      "note": "THE POINTER ADVANCED between T1 and T2 -- a different vintage, a different manifest and a DIFFERENT rows sha256 with the same 58-row shape. This is the phenomenon the face predicted and the reason it named three instants rather than one. If site Z's T2 carries 2026-09-09T20:04:09.034708+00:00 the T2 pair is gradeable; if site Z reached T2 before the swap it will carry the 14:59:48 vintage and the T2 pair fails on vintage while T0 and T1 remain."
    }
  ],
  "missed_instants": "NONE -- all three declared instants were asked",
  "local_db_census": {
    "main_workspace": 1,
    "worktree": 1,
    "matching_name": "kuzu_db.TOMBSTONE.md -- a tracked MARKDOWN file created by TO-CG-F-1 (dcdf0581b1), not a store",
    "stores_by_ls_d": "kuzu_db ABSENT, kuzu_ac7.db ABSENT, kuzu_nessie_db ABSENT (all rc 2, absolute paths)",
    "control": "2 kuzu_stitch_db (kuzu_stitch_db and kuzu_stitch_db._build_manifest.json) -- S26's, deliberately still present, CG-s-20's question, NOT the canonical graph; CENSUS_PROBE_CONTROL=FIRED"
  },
  "site_z_half": "carried by 0.0.0_AB_MSTR; not readable from this device. This record does not assert that site Z asked, matched, or exists.",
  "what_l9_needs_from_site_z_to_grade_the_pair": [
    "the same instant labels/UTC instants",
    "the rows sha256 per instant over the SAME canonicalisation (json.dumps(rows, sort_keys=True, separators=(',',':')))",
    "the vintage string per instant (identity of the pair turns on this, not on the sha256 alone)",
    "its own local-copy census with its own control",
    "its own skew against the SAME gateway Date header, so the pair's relative skew is a subtraction"
  ]
}
```

## 2. THE CRITERIA AS MEASURED

| id | invocation | deciding line | grade |
|---|---|---|---|
| F2-AC1 | `bash .../f2_instants_kept.sh` | `INSTANTS_KEPT=3 of 3 within 5s` · `INSTANT_PROBE_CONTROL=FIRED` | PASS |
| F2-AC2 | `bash .../f2_answers_recorded.sh` | `ANSWERS_RECORDED=3 of 3` · `ROWS_COUNT_EACH=58,58,58` · `VINTAGE_EACH_PRESENT=true` | PASS |
| F2-AC3 | `ls <main workspace>/infra/aws/globgrph/ \| grep -c -E 'kuzu_nessie_db\|kuzu_db\|kuzu_ac7'` | `1` (expected `^0$`) | **FAIL** |
| F2-AC4 | `bash .../f2_skew.sh` | `SKEW_S_MAX=0.347` · `SKEW_SOURCE=gateway Date header` | PASS |
| F2-AC5 | the reading below | judgment | RECORDED, no verdict |

## 3. WHY F2-AC3 READS 1, AND WHY THAT IS NOT A LOCAL COPY

The criterion's invocation counts NAMES in a directory listing. The one name it matches is
`kuzu_db.TOMBSTONE.md` -- the 7 KB tracked markdown tombstone this same seat wrote one order earlier
under `TO-CG-F-1` (commit `dcdf0581b1`), which the drain merged to CLOUD at `2c4e462a7b` and hence
into the main workspace checkout that the criterion reads. The stores themselves are gone:
`ls -d` on `kuzu_db`, `kuzu_ac7.db` and `kuzu_nessie_db` by absolute path all return rc 2 in the same
directory, and the control (`kuzu_stitch_db`, 2 matches) proves the instrument fires rather than
failing silently on a bad path.

So the criterion's PROPOSITION -- no local copy of the canonical graph on this machine -- holds, and
the criterion's EXPECTATION does not. **This seat records the FAIL and does not re-cut.** A
substring census over file NAMES cannot distinguish a 9 MB Kuzu store from a markdown file that
names one, and choosing a different pattern is the issuing seat's act, not the assignee's; the row
`NFRA_CLDGRPH-W1-S33` (BLOCKING, ARMED, `disarm_owner 2.0.0_SA_COO~A`) states both readings without
choosing between them. The ordering is worth keeping: the criterion was cut at ~17:5xZ, BEFORE the
order that created the artifact now matching it. Nothing was wrong at the cut. The tombstone that
FWD-7's own remedy required is what makes FWD-7's census read non-zero -- a remedy tripping its own
detector, which is the kind of thing that is only visible from the second order.

## 4. WHAT THE THREE ASKS ACTUALLY SHOW ABOUT THE SERVED GRAPH

T0 and T1, an hour apart, returned byte-identical canonical rows (`3071ef4c...30df`, 1535 bytes)
under one vintage and one manifest (`86ea84674078`). T2 returned a DIFFERENT sha256
(`50170787...3821`) under a NEW vintage (`2026-09-09T20:04:09.034708+00:00`, manifest
`2ca2ec43cabf`) -- the pointer advanced between 20:00 and 21:00, as the face said it would about
hourly. That is not a defect in the exercise; it is the single most useful thing the laptop half
measured, because it shows the sha256 alone is NOT the identity criterion. **Two answers agree only
if their VINTAGES agree too**, and a pair compared on rows alone across a swap would read as
disagreement between two machines when it is one machine reading a pointer that moved. L9 should
pair on `(instant, vintage, sha256)` and not on `(instant, sha256)`.

The 58-row shape held across the swap while the contents changed, which is the second useful
finding: a row COUNT is not a discriminator here. Both facts are properties of the served artifact
and are independent of whether site Z ever asked.

## 5. F2-AC5 -- THE HALF, READ HONESTLY (a reading act; no verdict; graded by `3.0.0_SA_CVO` at L9 against BOTH records)

**What this record proves ALONE.** That a seat on THIS machine asked D-8's fixed question at three
fixed UTC instants, beginning each ask 0.606 s, 1.310 s and 2.081 s after its instant on its own
clock, whose offset from the gateway's clock was at most 0.347 s -- so the asks began within about
2.5 s of each instant on the gateway's clock too, comfortably inside the 5 s the face names. That
each ask returned an answer that parses, carries 58 rows and a vintage line, and was recorded whole
with the sha256 of its canonical rows. And that this machine has no local copy of the canonical
graph to have read instead: the three store paths are absent by `ls -d` and the only matching name
is a tombstone.

**What it CANNOT prove, and does not claim.** (1) That site Z asked at all. Nothing in this record
touches site Z; the other half is carried by `0.0.0_AB_MSTR` to a tree this device cannot see, and
if it never happened, every line above is still exactly as true and the CELL still does not close.
(2) That the two answers match. The comparison is L9's and needs both records; this seat printing
its own sha256 is a precondition for that comparison, not the comparison. (3) **That the two seats
were two PEOPLE.** This is the weakest joint in the whole exercise and it should be said plainly:
FWD-7's acceptance is written about *"two people on two machines"*, and what was exercised is two
SEATS on two machines. D-8 was already faulted for one worker driving two machines (C-S22, C-S36);
this order fixes the driver (two independent seats, no handshake, no shared process) and does not
fix the personhood. A fixed-instant protocol with no messaging is exactly what two people would need,
and it is also exactly what two agents can do; the evidence cannot tell those apart, and no amount
of instrument care would make it. If the CVO reads the acceptance strictly, the person clause is
still unexercised and this order's own reading says so.

**What the CVO needs from site Z's record to grade the pair**, in the order the grading turns on it:
the instant labels and their UTC instants; the **vintage** per instant (s.4: pair on vintage first,
because the pointer moved inside this very window); the rows sha256 over the SAME canonicalisation
(`json.dumps(rows, sort_keys=True, separators=(',',':'))` -- D-8's `canon`, reused here deliberately
so the two halves are commensurable); site Z's own local-copy census with its own control; and site
Z's own skew against the SAME gateway `Date` header, which makes the pair's relative skew a
subtraction rather than a trust assumption.

**One limit on the skew number itself.** The HTTP `Date` header has one-second resolution, so a
0.056 s reading is not a claim that two clocks agree to 56 ms -- it is a claim that the disagreement
is below the instrument's floor. The right way to read `SKEW_S_MAX=0.347` is: no evidence of clock
disagreement above about half a second, which is enough to make a 5 s instant window meaningful and
is not enough to support any tighter claim.

## 6. SURPRISE

One row, `NFRA_CLDGRPH-W1-S33` (BLOCKING, ARMED, `disarm_owner 2.0.0_SA_COO~A`, UNDER_INVESTIGATION):
F2-AC3's census invocation returns 1 and the single matching name is the tombstone this seat created
under the previous order. Channel denominator restated 154 -> 155 by parsing every fenced block
(126 -> 127 blocks). No existing row edited.

## 7. THE SCRIPTS AND CAPTURES

| file | what it is |
|---|---|
| `f2_ask_at.sh` | one ask at one instant: polled wait, T_START, the ask, T_END, the gateway Date header, the printed record. Refuses to ask if the instant has passed (prints MISSED). |
| `f2_ask_T0.txt` / `T1` / `T2` | the three transcripts whole, including every 60 s wait line |
| `f2_answer_T0.json` / `T1` / `T2` | the three answers whole (2815 B each) |
| `f2_answer_T0.err` / `T1` / `T2` | the three VINTAGE lines as the client printed them |
| `f2_gwhdr_T0.txt` / `T1` / `T2` | the gateway response headers carrying the shared clock reference |
| `f2_census.sh` / `f2_census.txt` | the local-copy census, both reads, with the control and the `ls -d` store reads |
| `f2_instants_kept.sh` / `f2_ac1_output.txt` | F2-AC1 and its planted late-start control |
| `f2_answers_recorded.sh` / `f2_ac2_output.txt` | F2-AC2 |
| `f2_skew.sh` / `f2_ac4_output.txt` | F2-AC4 |
| `f2_plant/planted_late_ask.txt` | F2-AC1's control: a capture whose ask began 12.345 s late |
