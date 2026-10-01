"""RIV-hp-1 AC1 -- canonical_shape reads the home funds from the Positioning pull's landing (C-HOME-PRODUCER v0.5;
row W1-S8; analysis ruling 4), as a named source, landing no second copy.

Real data: the Positioning landings s3://opal-data-etfs/bbg/<D>/constituents/constituents_issuer_fill.parquet for the
newest two IDVZ-capture dates are copied READ-ONLY into a local sink at the same keys; the last 2 IDVZ-group captures run
through canonical_shape. For the newest date:
  - G1 carries IDVZ and PFOE rows with source_used = 'home_producer';
  - per home fund, G1's row count equals that fund's row count in the landing for that date;
  - no non-universe fund of the landing (DIVZ, PFDE) appears in G1;
  - nothing is written under bbg/ or any silver prefix by the stage (no second copy): the sink's bbg/ tree holds only the
    two mirrored objects.
Control: a rival (TXUE) keeps source_used = 'bloomberg'."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    c.setup_path()
    import pandas as pd

    files = c.idvz_captures(2)
    sink = c.tmpdir("rv_hp1a_")
    dates = [c.capture(f)["requested_date"] for f in files]
    for d in dates:
        c.mirror_s3(sink, c.HOME_LANDING_FMT.format(d=d))
    c.run_idvz_chain(sink, files, "canonical")
    newest = dates[-1]
    df, n = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={newest}")
    v.check(n >= 1, f"a G1 object for {newest} ({n})")
    if not len(df):
        return
    latest = df[df["dataset_revision"] == df["dataset_revision"].max()]
    land = pd.read_parquet(c.local_path(sink, c.HOME_LANDING_FMT.format(d=newest)))
    land = land[land["date"].astype(str).str[:10] == newest]
    for fund in ("IDVZ", "PFOE"):
        g = latest[latest["fund_ticker"].astype(str).str.strip() == fund]
        want = int((land["fund_ticker"].astype(str) == fund).sum())
        src = set(g["source_used"].astype(str)) if "source_used" in g.columns else set()
        v.check(len(g) == want and want > 0 and src == {"home_producer"},
                f"{fund}: {len(g)} G1 rows vs {want} landing rows, source_used {sorted(src)}")
    v.check(not (set(latest["fund_ticker"].astype(str).str.strip()) & {"DIVZ", "PFDE"}), "no non-universe landing fund in G1")
    tx = latest[latest["fund_ticker"].astype(str).str.strip() == "TXUE"]
    v.check(len(tx) > 0 and set(tx["source_used"].astype(str)) == {"bloomberg"}, "control: TXUE source_used bloomberg")
    bbg_objs = sorted(p for p in c.local_path(sink, "s3://opal-data-etfs/bbg/x").parent.rglob("*") if p.is_file())
    v.check(len(bbg_objs) == 2, f"no second copy under bbg/ ({len(bbg_objs)} objects)")


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
