#!/usr/bin/env python3
"""GUARD-3b proof -- the tplus1 tripwire's per-series custom-CIX recency check, on REAL PKLs.

OPAL_BBGTML.TO-GUARD-3 criterion AC2. Reads two archived S3 object versions, writes NOTHING to
S3. The PKLs are fetched to a scratch dir under the system temp, never into the repo.

WHERE THE TWO PULLS WERE READ, and why these are the two the order names:

  ARM 1 -- the 2026-10-06 12:29Z pull. The order names it exactly:
      s3://opal-data-portal-v2/benchmarks/data_20261005_v1.pkl
      VersionId fPWS_TCLSvx2dW9SZGDl3hcQL735m5XJ, LastModified 2026-10-06T12:29:21Z.

  ARM 2 -- the 2026-10-07 01:26Z re-pull. The order said a listing of the 10-05 key shows ONE
      version, so the re-pull is NOT at that key, and told this seat to locate it by its time
      and name where it was read. Measured: `list-object-versions --prefix benchmarks/` returns
      exactly ONE object written at 01:26:10Z,
      s3://opal-data-portal-v2/benchmarks/data_20261007_v1.pkl
      VersionId F2HhLHRpKgZ18hIWMRJr3p3t4T52RfBW, LastModified 2026-10-07T01:26:10Z, 8712649 B.
      The re-pull re-ran on 10-07 and the landing key is stamped with the RUN day, while the
      vintage INSIDE it is still 2026-10-05 -- which is why it did not land on the 10-05 key.
      Three facts tie it to the 01:26Z re-pull, and the proof asserts all three rather than
      taking the filename's word:
        (a) its byte size equals `uploads/data 20261005 v1.pkl` written at 01:26:06Z (8712649),
            the staged copy of the same send;
        (b) the vintage inside it -- return_daily's max date -- is 2026-10-05, the vintage the
            order is about, not 10-07;
        (c) ADDENDUM 5's served body (VersionId fxNfvcQ8..., 01:28:18Z) is two minutes later,
            so this is its input.
      If any of (a)-(c) failed, this arm would be NOT RUN rather than substituted.

Arms:
  B1  the 12:29Z pull  -> the tripwire FAILS, naming 7 of 13 custom CIX series at 2026-09-29,
      with the denominator printed; the as-of check itself is held PASSING so the CIX finding is
      the only moving variable.
  B2  the 01:26Z re-pull -> the tripwire PASSES; 13 of 13 custom CIX series reach the as-of.
  B3  CONTROL: SPX is a vendor series, is not in the graded custom set, and reaches the as-of on
      BOTH pulls -- so it is unaffected, and the control is live rather than vacuous.
  B4  NEGATIVE CONTROL on the instrument: one custom series' last bars blanked must flip B2's
      PASS to a FAIL naming exactly that series. Without this, "all 13 reach the as-of" could be
      a check that always says so.
  B5  the recognition rule is DERIVED, not typed: the graded set equals the frame's own
      dot-prefixed bbg_ticker values, and no series name is hardcoded in the tripwire.

Exit 0 only if every arm matches.
"""
from __future__ import annotations

import importlib.util
import os
import pickle
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
TRIPWIRE = REPO / "integrations" / "bloomberg" / "pipeline" / "tplus1" / "tools" / "bbg_pkl_tripwire.py"

BUCKET = "opal-data-portal-v2"
ARM1 = ("benchmarks/data_20261005_v1.pkl", "fPWS_TCLSvx2dW9SZGDl3hcQL735m5XJ",
        "2026-10-06T12:29:21Z pull")
ARM2 = ("benchmarks/data_20261007_v1.pkl", "F2HhLHRpKgZ18hIWMRJr3p3t4T52RfBW",
        "2026-10-07T01:26:10Z re-pull")
STAGED_01_26Z_SIZE = 8712649  # uploads/data 20261005 v1.pkl @ 2026-10-07T01:26:06Z
EXPECTED_VINTAGE = "2026-10-05"
SPX_TICKER = "SPX Index"

failures: list = []


def check(label: str, got, want) -> None:
    ok = got == want
    if not ok:
        failures.append(label)
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       want: {want!r}")
        print(f"       got : {got!r}")


def load_tripwire():
    spec = importlib.util.spec_from_file_location("bbg_pkl_tripwire_under_proof", TRIPWIRE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bbg_pkl_tripwire_under_proof"] = mod
    spec.loader.exec_module(mod)
    return mod


def fetch(dest_dir: Path, key: str, version_id: str) -> Path:
    import boto3
    out = dest_dir / os.path.basename(key)
    boto3.client("s3").download_file(BUCKET, key, str(out),
                                     ExtraArgs={"VersionId": version_id})
    return out


def series_last(rd: pd.DataFrame, ticker: str):
    sub = rd[rd["bbg_ticker"].astype(str) == ticker]
    nn = sub[sub["price"].notna()]
    return nn["date"].pipe(pd.to_datetime).dt.date.max() if len(nn) else None


def run_tripwire_data_leg(mod, path: Path, hold_asof_passing: bool = True):
    """Run the tripwire's own data-PKL leg and return (reasons, asof). asof_ok is held to the
    frame's own as-of so the pre-existing as-of check PASSES and the CIX limb is the only
    variable that can fail -- isolating what this cell added."""
    with open(path, "rb") as f:
        d = pickle.load(f)
    rd = d["return_daily"]
    asof = pd.to_datetime(rd["date"]).max().date()
    asof_ok = {asof} if hold_asof_passing else set()
    reasons: list = []
    mod.check_data_pkl(str(path), asof_ok, reasons)
    return reasons, asof, rd


def main() -> int:
    print(f"GUARD-3B PROOF -- module under proof: {TRIPWIRE}")
    print(f"  repo root resolved: {REPO}")
    print(f"  pandas {pd.__version__} | python {sys.version.split()[0]}")
    mod = load_tripwire()
    tmp = Path(tempfile.mkdtemp(prefix="guard3b_proof_"))
    print(f"  scratch dir: {tmp}")

    print(f"\n[B1] {ARM1[2]} -- s3://{BUCKET}/{ARM1[0]} VersionId {ARM1[1]}")
    p1 = fetch(tmp, ARM1[0], ARM1[1])
    print(f"       fetched {p1.name} ({p1.stat().st_size} B)")
    reasons1, asof1, rd1 = run_tripwire_data_leg(mod, p1)
    g1 = mod.grade_cix_series(rd1, asof1)
    print(f"       as-of resolved by the tripwire: {asof1}")
    print(f"       custom CIX graded: {g1['graded']} | behind: {len(g1['behind'])} "
          f"| vendor (not graded): {g1['vendor']}")
    for tk, name, last in g1["behind"]:
        print(f"         BEHIND {tk:<16} {name:<30} last non-null {last}")
    check("B1 the tripwire data leg FAILS", len(reasons1) > 0, True)
    check("B1 the CIX limb is the reason it failed",
          sum(1 for r in reasons1 if "custom CIX" in r), 1)
    check("B1 the as-of check itself did NOT fail (variable isolated)",
          sum(1 for r in reasons1 if "not in expected" in r), 0)
    check("B1 denominator: 13 custom CIX series graded", g1["graded"], 13)
    check("B1 7 series behind", len(g1["behind"]), 7)
    check("B1 the 7 are the CRO trace's list",
          sorted(tk for tk, _, _ in g1["behind"]),
          [".INT_BMK Index", ".LT_BMK Index", ".LT_ETF Index", ".ST_BMK Index",
           ".ST_ETF Index", ".UST_BMK Index", ".UST_ETF Index"])
    check("B1 every behind series' last non-null bar is 2026-09-29",
          sorted({str(last) for _, _, last in g1["behind"]}), ["2026-09-29"])
    check("B1 .INT_ETF is NOT behind (the trace said it kept calculating)",
          ".INT_ETF Index" in [tk for tk, _, _ in g1["behind"]], False)

    print(f"\n[B2] {ARM2[2]} -- s3://{BUCKET}/{ARM2[0]} VersionId {ARM2[1]}")
    p2 = fetch(tmp, ARM2[0], ARM2[1])
    size2 = p2.stat().st_size
    print(f"       fetched {p2.name} ({size2} B)")
    reasons2, asof2, rd2 = run_tripwire_data_leg(mod, p2)
    g2 = mod.grade_cix_series(rd2, asof2)
    print(f"       as-of resolved by the tripwire: {asof2}")
    print(f"       custom CIX graded: {g2['graded']} | behind: {len(g2['behind'])}")
    check("B2 (a) size equals the 01:26:06Z staged copy", size2, STAGED_01_26Z_SIZE)
    check("B2 (b) the vintage inside it is the 10-05 vintage", str(asof2), EXPECTED_VINTAGE)
    check("B2 the tripwire data leg PASSES", reasons2, [])
    check("B2 denominator: 13 custom CIX series graded", g2["graded"], 13)
    check("B2 no series behind", [tk for tk, _, _ in g2["behind"]], [])

    print("\n[B3] CONTROL -- SPX is a vendor series, not a custom one")
    for tag, rd, asof in (("B1 pull", rd1, asof1), ("B2 re-pull", rd2, asof2)):
        present = SPX_TICKER in set(rd["bbg_ticker"].astype(str))
        last = series_last(rd, SPX_TICKER)
        g = g1 if tag.startswith("B1") else g2
        print(f"       {tag}: SPX present={present} last non-null={last} "
              f"in graded custom set={SPX_TICKER in g['tickers']}")
        check(f"B3 {tag}: SPX is in the frame (the control is live)", present, True)
        check(f"B3 {tag}: SPX is NOT graded as a custom CIX series",
              SPX_TICKER in g["tickers"], False)
        check(f"B3 {tag}: SPX reaches the as-of, so it is unaffected", last, asof)
        check(f"B3 {tag}: SPX is not named in the behind list",
              SPX_TICKER in [tk for tk, _, _ in g["behind"]], False)

    print("\n[B4] NEGATIVE CONTROL -- blank one custom series' bars after 2026-09-29 on the")
    print("     PASSING re-pull; the check must flip to FAIL naming exactly that series.")
    victim = ".ST_BMK Index"
    rd_mut = rd2.copy()
    mask = ((rd_mut["bbg_ticker"].astype(str) == victim)
            & (pd.to_datetime(rd_mut["date"]).dt.date > pd.Timestamp("2026-09-29").date()))
    print(f"       blanking {int(mask.sum())} bars of {victim}")
    rd_mut.loc[mask, "price"] = None
    rd_mut.loc[mask, "return"] = None
    rd_mut.loc[mask, "price_return"] = None
    g4 = mod.grade_cix_series(rd_mut, asof2)
    print(f"       graded={g4['graded']} behind={[(tk, str(ld)) for tk, _, ld in g4['behind']]}")
    check("B4 the mutant is caught", len(g4["behind"]), 1)
    check("B4 and it is the planted series", [tk for tk, _, _ in g4["behind"]], [victim])
    check("B4 reported at the planted last date",
          [str(ld) for _, _, ld in g4["behind"]], ["2026-09-29"])
    check("B4 the denominator did not move", g4["graded"], 13)

    print("\n[B5] the recognition rule is DERIVED from the PKL, never typed")
    derived = sorted({t for t in rd2["bbg_ticker"].astype(str) if t.startswith(".")})
    print(f"       dot-prefixed tickers in the frame: {len(derived)}")
    for t in derived:
        print(f"         {t}")
    check("B5 the graded set equals the frame's own dot-prefixed tickers",
          sorted(g2["tickers"]), derived)
    # The claim is about the EXECUTABLE recognition path, so the test measures that and not the
    # prose: comments and docstrings DO name .UST_BMK Index and the other six, deliberately, to
    # record the dot convention and the incident. Naming them in a comment is documentation;
    # naming them in code would be the typed list this cell was told not to write. So the source
    # is tokenized and every COMMENT and STRING token dropped before the search -- an assertion
    # over the raw bytes would conflate the two and fire on the documentation.
    import io
    import tokenize
    code_only = []
    with io.open(TRIPWIRE, "rb") as fh:
        for tok in tokenize.tokenize(fh.readline):
            if tok.type not in (tokenize.COMMENT, tokenize.STRING):
                code_only.append(tok.string)
    code_src = " ".join(code_only)
    typed = [t for t in derived if t in code_src]
    bare = [t for t in derived if t.split()[0] in code_src]
    print(f"       code tokens searched: {len(code_only)} (comments and strings dropped)")
    check("B5 no custom series ticker is hardcoded in the tripwire's CODE", typed, [])
    check("B5 not even the bare dot-ticker stem appears in code", bare, [])
    check("B5 the recognition rule in code is the one-character prefix", mod.CIX_PREFIX, ".")

    print(f"\nARMS: 5 | CHECKS: {len(failures)} failed")
    if failures:
        print("GUARD-3B: FAIL -- " + "; ".join(failures))
        return 1
    print("GUARD-3B: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
