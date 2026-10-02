"""RIV-r-6 AC1 (repair): the AI card's absence sentence reads as a sentence. After "No AI account." the reason starts with a
capital letter (today it reads "No AI account. the research_hypotheses table is not built for ..."). The census card's
absence sentence follows the same rule (control on the shared `_absent` path)."""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    from rivalfunds import render

    ctx = {"day": "2026-10-02", "a1": {}}
    ai = render._ai_card(ctx, {"fund": "TXUE", "role": "rival"})
    m = re.search(r"No AI account\.</b>\s*(\S)", ai)
    print("AI card:", re.sub(r"<[^>]+>", " ", ai)[:160])
    v.check(bool(m) and m.group(1).isupper(), "the reason after 'No AI account.' starts with a capital letter")
    cen = render._census(ctx)
    m2 = re.search(r"Input census not available\.</b>\s*(\S)", cen)
    v.check(bool(m2) and m2.group(1).isupper(), "the census absence sentence starts with a capital letter")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
