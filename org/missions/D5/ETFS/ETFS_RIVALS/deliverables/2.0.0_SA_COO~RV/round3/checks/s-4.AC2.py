"""RIV-s-4 AC2 -- the live G4 request is planned from REAL G1 (the seam to canonical_shape; the Terminal itself is
signed out, so the vendor end is not exercised here -- RIV-d-4 exercises it at the next sign-in).

Real data: the last 2 IDVZ-group captures through canonical_shape in a local sink. enrichment_bloomberg mode 'plan-market'
for the newest date returns:
  - securities == the distinct NON-cash security_bloomberg values of G1 at that date (denominator printed);
  - fields including GICS_SECTOR_NAME, GICS_INDUSTRY_GROUP_NAME, GICS_INDUSTRY_NAME, GICS_SUB_INDUSTRY_NAME, PX_LAST and
    CRNCY (the four GICS levels C-SHAPES names, plus the price and currency G4 carries);
  - no Bloomberg call (the plan is offline: it returns without a session)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

FIELDS = {"GICS_SECTOR_NAME", "GICS_INDUSTRY_GROUP_NAME", "GICS_INDUSTRY_NAME", "GICS_SUB_INDUSTRY_NAME", "PX_LAST", "CRNCY"}


def run(v):
    c.setup_path()
    from rivalfunds import enrichment_bloomberg

    files = c.idvz_captures(2)
    sink = c.tmpdir("rv_s4b_")
    c.run_idvz_chain(sink, files, "canonical")
    d = c.capture(files[-1])["requested_date"]
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={d}")
    latest = df[df["dataset_revision"] == df["dataset_revision"].max()]
    want = set(latest.loc[~latest["is_cash_line"].astype(bool), "security_bloomberg"].dropna().astype(str))
    want |= set(latest.loc[~latest["is_cash_line"].astype(bool) & latest["security_bloomberg"].isna(), "position_id"]
                .dropna().astype(str).str.split(":").str[0])
    print(f"G1 non-cash securities at {d}: {len(want)}")
    plan = enrichment_bloomberg.handler_entry({"mode": "plan-market", "date": d, "sink": f"local:{sink}"})
    got = set(map(str, (plan or {}).get("securities") or []))
    fields = set(map(str, (plan or {}).get("fields") or []))
    v.check(len(got) > 0 and got == want, f"plan securities {len(got)} == G1 non-cash {len(want)} (diff {sorted(got ^ want)[:4]})")
    v.check(FIELDS <= fields, f"plan fields include {sorted(FIELDS - fields) or 'all six'}")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
