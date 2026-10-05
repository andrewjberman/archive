"""RIV-gc-1 AC1 (Andrew smoke S2, 2026-10-04): a figure the account states that sits in a fund-pack fact the model did not
cite is attached to the account's citations, not reported as invented. Measured: IDVZ "The last 30 days" (run
20261002T110438Z) FAILED "figures not in any cited row: $1.6 million, $1.3 million"; both are real facts the model left out
of `cited` -- T7 Reckitt add 1,564,110.98 and T9 Iberdrola add 1,292,762.88 -- and re-grading with them cited PASSES.
"$1.3 million" also matches a second fact (T8), so a value match can be ambiguous.

Interface (prescribed): `ai_accounts.attach_uncited(body: str, facts: list[dict], cited: list[dict]) -> tuple[list[dict], list[str]]`.
For each figure in `body` that matches no value of the `cited` rows (the grader's own matcher, `_matches`): if exactly ONE
fact NOT already cited matches it, that fact's `cited_row` is returned (a copy carrying `"auto_cited": True`); if two or more
match, nothing is attached for it and one note names the figure and the fact ids (e.g. "$1.3 million: T8, T9"). `run_chain`
calls it after building `cited` and before `grounding_check`; an ambiguous figure's note joins the FAIL reason.
  - (a) "$1.6 million" with T7 = 1,564,110.98 uncited -> T7's row is attached with auto_cited, and grounding passes on cited + it;
  - (b) "$1.3 million" with T8 = 1,302,400.00 and T9 = 1,292,762.88 both uncited -> nothing attached; one note names T8 and T9;
  - (c) control: "$9.9 million" matching no fact -> nothing attached, no note, and grounding still FAILS.
FAIL at base: (a) and (b) FAIL (no attach_uncited); (c) PASSES (grounding_check exists)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def fact(fid, value):
    return {"id": fid, "text": f"{fid} fact", "value": value,
            "cited_row": {"table": "trade_schedule", "key": f"IDVZ|{fid}|2026-09-14", "revision": "fx", "value": value}}


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import ai_accounts as aa

    facts = [fact("T1", 2198653.59), fact("T7", 1564110.98), fact("T8", 1302400.00), fact("T9", 1292762.88)]
    cited = [facts[0]["cited_row"]]
    fn = getattr(aa, "attach_uncited", None)

    body_a = "IDVZ added AstraZeneca PLC for $2.2 million and Reckitt Benckiser Group PLC for $1.6 million."
    if fn is None:
        v.check(False, "(a) attach_uncited exists and attaches the one uncited fact T7")
    else:
        rows, notes = fn(body_a, facts, cited)
        ok, why = aa.grounding_check(body_a, cited + rows)
        print("(a) attached:", [r.get("key") for r in rows], "notes:", notes, "grounding:", ok, why)
        v.check(len(rows) == 1 and rows[0].get("key", "").startswith("IDVZ|T7|") and rows[0].get("auto_cited") is True
                and not notes and ok, "(a) the one uncited fact T7 is attached (auto_cited) and grounding passes")

    body_b = "IDVZ added AstraZeneca PLC for $2.2 million and Iberdrola SA for $1.3 million."
    if fn is None:
        v.check(False, "(b) an ambiguous figure attaches nothing and its note names T8 and T9")
    else:
        rows, notes = fn(body_b, facts, cited)
        print("(b) attached:", [r.get("key") for r in rows], "notes:", notes)
        v.check(not rows and len(notes) == 1 and "T8" in notes[0] and "T9" in notes[0],
                "(b) an ambiguous figure attaches nothing and one note names T8 and T9")

    body_c = "IDVZ added AstraZeneca PLC for $2.2 million and a mystery line for $9.9 million."
    rows, notes = fn(body_c, facts, cited) if fn else ([], [])
    ok, why = aa.grounding_check(body_c, cited + rows)
    print("(c) attached:", rows, "notes:", notes, "grounding:", ok, why)
    v.check(not rows and not notes and not ok, "(c) control: a figure in no fact attaches nothing and grounding still FAILS")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
