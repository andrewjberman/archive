"""RIV-g-3 AC1 -- canonical_shape v2 over REAL Bloomberg captures (3 IDVZ-group days) plus REAL BASG issuer days: G1 holds
the five IDVZ rivals from Bloomberg (IDVZ itself is home_producer_pending and is NOT read) and BASG from the issuer;
source_used is bloomberg / issuer accordingly, ONE source per (fund, report date); cash/currency lines are kept and flagged
is_cash_line (the capture's ' Curncy' positions); for the newest report every silver row of each rival is a G1 row."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    files = c.idvz_captures(3)
    sink = c.tmpdir("rv_g12_")
    c.land(sink, c.archive_files(2))
    c.replay("silver_issuer", sink, c.archive_meta(c.archive_files(1)[0])["requested_date"])
    res = c.run_idvz_chain(sink, files, "canonical")
    print("canonical:", str(res.get("canonical"))[:300])
    df, n = c.read_parquets(c.gold_dir(sink, "canonical_shape"))
    v.check(n >= 1 and len(df) > 0, f"G1 objects {n}, rows {len(df)}")
    fund_col = next((k for k in ("fund_ticker", "fund_id") if k in df.columns), None)
    v.check(fund_col is not None and "source_used" in df.columns and "is_cash_line" in df.columns,
            "columns fund, source_used, is_cash_line present")
    if fund_col is None or "source_used" not in df.columns:
        return
    funds = set(df[fund_col])
    rivals = set(c.IDVZ_GROUP[1:])
    v.check(rivals <= funds, f"the five IDVZ rivals present ({sorted(rivals - funds)} missing)")
    v.check("IDVZ" not in funds, "IDVZ (home_producer_pending) NOT read")
    v.check("BASG" in funds, "BASG present from the issuer")
    srcs = df.groupby(fund_col)["source_used"].unique().to_dict()
    v.check(all(list(srcs[f]) == ["bloomberg"] for f in rivals if f in srcs), f"rivals source_used bloomberg {({f: list(srcs.get(f, [])) for f in rivals})}")
    v.check(list(srcs.get("BASG", [])) == ["issuer"], f"BASG source_used issuer ({list(srcs.get('BASG', []))})")
    rd = next((k for k in ("report_date",) if k in df.columns), None)
    if rd:
        per = df.groupby([fund_col, rd])["source_used"].nunique()
        v.check(int(per.max()) == 1, f"one source per (fund, report date) (max {int(per.max())})")
    newest = files[-1]
    want = c.capture_rows_by_fund(newest)
    rep = c.capture(newest)["requested_date"]
    if rd:
        cur = df[df[rd].astype(str).str[:10] == rep]
        got = cur.groupby(fund_col).size().to_dict()
        v.check(all(got.get(f) == want.get(f) for f in rivals), f"newest report {rep}: G1 rows per rival {got} == capture {want}")
        hdr = c.capture(newest)["rows"][0]
        ncash = sum(1 for r in c.capture(newest)["rows"][1:] if str(r[hdr.index("ID")]).endswith(" Curncy")
                    and str(r[hdr.index("ORIG_IDS")]).split()[0] in rivals)
        v.check(int(cur["is_cash_line"].sum()) >= ncash > 0, f"cash lines kept and flagged: {int(cur['is_cash_line'].sum())} >= {ncash}")


failures = c.guarded("AC1", run)
if failures == 0:
    print("AC1 RESULT: PASS 0 failures")
else:
    print(f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
