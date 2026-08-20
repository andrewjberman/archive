# TO NFRA_TRUNCLASS.SWEEP -- the TRUNCATION CLASS, censused across every comp-tool parser

<task_order id="NFRA_TRUNCLASS.SWEEP" project="NFRA_COMPRAIL">
<issued_to>0.8.0_AE_CloudComp</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-20T00:58Z</issued>
<status>staged -- GO paired; sequenced BEHIND the Andrew-prioritized dot-truncation fix, which is the specimen this census generalises</status>
<priority>P1 -- ANDREW-NAMED CLASS</priority>
<authority>Andrew-direct 2026-08-20 ~005xZ at the MSTR terminal, VERBATIM: "Yes we need to impriove comp-adversary, truncated outputs is a very risky error type and one we've seen crop up many times". Relayed by 0.0.0_AB_MSTR (record+broadcast same turn), which routes the class-sweep half to COO for the cut. CTO is mandate owner on the comp-adversary row itself.</authority>
</task_order>

## Why this exists: HE NAMED A CLASS, NOT A BUG

The operative words are **"one we've seen crop up many times."** The dot-truncation defect in
comp-adversary's source-2 path pin is the SPECIMEN. The class is:

> **AN INSTRUMENT SILENTLY OPERATES ON A TRUNCATED VERSION OF ITS INPUT AND RETURNS A WELL-FORMED
> ANSWER ABOUT THE TRUNCATED THING.**

That is why it is dangerous and why care cannot catch it: **the output is not malformed, not empty,
and carries no error.** It is true about *something* -- just not the thing asked. A `GONE` verdict
from a first-dot-split path is a correct answer about a path that does not exist.

**PRIOR SPECIMENS ALREADY ON THE ESTATE'S RECORD** -- this is the evidence for "many times", and they
are deliberately drawn from different tool families to show the class is not one parser's habit:
- `--query 'length(...)'` on a paginated `list-*` returning the PAGE count as a total (142 read as 100).
- `--no-paginate` returning page 1 as a clean complete-looking result (196 read as 50).
- `grep -c` on a single-line JSON payload returning 1 for everything -- read as *no duplication at all*.
- `grep -c` over a `git show` error string, counting zero matches IN AN ERROR MESSAGE.
- A non-recursive `s3 ls` silently cutting the domain to one prefix level.

## THE CENSUS -- classify, do not fix

**The sweep CLASSIFIES. Each fix rides its own tool's row.** A census that also repairs becomes a
project with no denominator and no end.

Search the comp-tool parsers for these shapes, and print the denominator of what you scanned:
1. **FIRST-DELIMITER SPLITS** -- `split('.')[0]`, `split('/')[0]`, `cut -d`, `partition()` -- anywhere
   the input can legitimately contain that delimiter. **`org/` is the fixture-rich case: every
   serial-named directory carries dots.**
2. **FIXED-WIDTH CUTS** -- slicing to N chars/lines where the input is variable-length.
3. **HEAD-N ON VARIABLE OUTPUT** -- `head -N`, `[:N]`, `--max-items` where N was chosen for display
   and is then reasoned from.
4. **SINGLE-PAGE READS** -- any paginated API consumed without walking the token, or any `list-*`
   whose result is filtered before materialising.

## Acceptance criteria
- **TRC-1 CENSUS COMPLETE WITH ITS DENOMINATOR** -- every `.tools/comp-*` executable and its engine
  modules scanned, count of files scanned printed beside the count of hits. **A hit count without a
  denominator is the very class this TO is about.**
- **TRC-2 EACH HIT CLASSIFIED, NOT FIXED** -- for each: the shape (1-4), whether the input can
  legitimately contain the delimiter/exceed the width, and **what a wrong answer would LOOK like**
  (the verdict it would produce). A hit whose input provably cannot trigger it is reported as
  EXAMINED-AND-SAFE, not omitted -- **omitting the safe ones destroys the denominator.**
- **TRC-3 SEVERITY BY WHAT THE OUTPUT AUTHORIZES**, not by frequency. A truncation feeding a
  GONE/ABSENT/UNUSED verdict outranks one feeding a display string, because **the first becomes a
  deletion warrant and the second becomes a cosmetic bug.**
- **TRC-4 THE PRIOR SPECIMENS RE-TESTED as regression fixtures** -- at minimum the dot-split case
  (CTO~Z's measured instance) and the single-line-JSON `grep -c` case. **If your census method does
  not FLAG the known specimens, the method is what you have measured, not the corpus.**
- **TRC-5 proof instance VALID rc=0**, ids `TRC-1..TRC-5`, run against the named expected-id set with
  the TRUE rc cited (measured without a pipe).

<proof_of_spec>
  <expected_criteria>TRC-1,TRC-2,TRC-3,TRC-4,TRC-5</expected_criteria>
  <instance_path>org/tier2_senior/0.8.0_AE_CloudComp/deliverables/NFRA_TRUNCLASS.SWEEP_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- **Do not fix anything you find.** Classify. Fixes ride each tool's own row, so each carries its own
  acceptance and its own reviewer.
- **Do not treat the four shapes as exhaustive.** They are the shapes we have MEASURED. A fifth shape
  you find is a finding, not an exception -- name it and count it.
- **Do not let this displace the Andrew-prioritized dot-truncation fix.** That fix is the specimen and
  it lands FIRST; this census generalises from it.

## Interim discipline, standing until the dot-fix lands
**A `GONE` verdict on any dot-bearing path is UNVERIFIED. Direct-check before acting on it.**

## Reporting
COO. CC CTO as mandate owner on the comp-adversary row. The census result is an input to the
instrument-repair batch, not a new workstream of its own.
