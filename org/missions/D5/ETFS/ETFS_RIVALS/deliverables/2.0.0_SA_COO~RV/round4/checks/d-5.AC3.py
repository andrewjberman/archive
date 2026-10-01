"""RIV-d-5 AC3 (live, READ-ONLY) -- the revision contract and the identity alias, served:
  - served G1 for 2026-09-29 sources its GICS from the LIVE G4 (market-20260929-53bc393958bd), never the QA import
    (market-20260929-afcd903ad844) -- the measured case of row W4-S5;
  - served G1 for the act's newest report date resolves BASG's non-cash rows at >= 0.90 (row W4-S2's 0 of 33 closed).
Reads d5_live.json `newest_report_date`; then the newest served G1 object per date by the contract's own order
(`revision.newest`, RIV-v-2) from the tree this check runs in."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402
import _live as L  # noqa: E402


def newest_g1(d):
    from rivalfunds import revision

    ks = [k for k in L.keys(f"rivalfunds/etfs/gold/canonical_shape/date={d}/") if k.endswith(".parquet")]
    k = revision.newest([f"s3://{L.BUCKET}/{x}" for x in ks])
    return k, L.parquet(k[len(f"s3://{L.BUCKET}/"):]) if k else None


def run(v):
    c.setup_path()
    k, g = newest_g1("2026-09-29")
    srcs = set(g.loc[g["gics_status"].astype(str) == "RESOLVED", "gics_source"].astype(str)) if g is not None else set()
    print("2026-09-29 G1", k, "gics sources", sorted(srcs)[:2])
    v.check(bool(srcs) and all("53bc393958bd" in s for s in srcs), "2026-09-29 G1 GICS comes from the live G4 only")
    rd = L.record().get("newest_report_date")
    k, g = newest_g1(rd)
    b = g[(g["fund_ticker"].astype(str).str.strip() == "BASG") & ~g["is_cash_line"].astype(bool)] if g is not None else None
    frac = float((b["resolution_status"] == "RESOLVED").mean()) if b is not None and len(b) else 0.0
    print(f"{rd} G1 {k}: BASG resolved {frac:.3f} of {0 if b is None else len(b)}")
    v.check(frac >= 0.90, f"{rd} BASG resolves {frac:.3f} >= 0.90")


failures = c.guarded("AC3", run)
print("AC3 RESULT: PASS 0 failures" if failures == 0 else f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
