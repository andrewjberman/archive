#!/usr/bin/env python3
"""GUARD-4 proof -- the per-series custom-CIX recency limb ported into the TZERO tripwire.

OPAL_BBGTML.TO-GUARD-4 criterion AC1, on the same two real pulls the GUARD-3b proof used.
Writes NOTHING to S3. PKLs land in a scratch dir under the system temp, never in the repo.

Arms:
  C1  the 2026-10-06T12:29:21Z pull (benchmarks/data_20261005_v1.pkl VersionId fPWS_TCL...)
      -> the EDITED tzero copy FAILS, naming 7 of 13 custom CIX series at 2026-09-29, with the
      denominator printed. The as-of check is held passing so the CIX finding is the only
      moving variable.
  C2  the 2026-10-07T01:26:10Z re-pull (benchmarks/data_20261007_v1.pkl VersionId F2HhLHRp...)
      -> the EDITED tzero copy PASSES; 13 of 13 reach the as-of.
  C3  CONTROL: SPX is a vendor series, not in the graded custom set, reaches the as-of on both.
  C4  THE NEGATIVE CONTROL the order requires: the tzero copy AT ITS PARENT COMMIT reads PASS
      on the frozen pull. That is the difference the port makes. Without it the proof shows
      only that the new code runs.
      The parent bytes are pulled with `git show <parent>:<path>` and their git blob hash is
      asserted against the hash measured before the edit -- because a mangled `git show`
      returns CLEAN-EMPTY on this platform, so the hash IS the positive control that the
      retrieval worked. An empty or wrong retrieval fails the arm instead of silently
      reading PASS, which would have manufactured the very result C4 wants to see.
  C5  And the arm that closes the one claim row OPAL_BBGTML-Z-S12 left UNMEASURED: the tzero
      copy's OWN as-of-scoped presence check does NOT catch a frozen benchmark series. It
      grades MODEL_INDEX_NAMES only, and on the frozen pull all 5 models do reach the as-of
      while 7 benchmark/ETF series do not. So the port is not redundant with it.

Exit 0 only if every arm matches.
"""
from __future__ import annotations

import importlib.util
import os
import pickle
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
REL_TZERO = "integrations/bloomberg/pipeline/tzero/tools/bbg_pkl_tripwire.py"
TZERO = REPO / "integrations" / "bloomberg" / "pipeline" / "tzero" / "tools" / "bbg_pkl_tripwire.py"
sys.path.insert(0, str(REPO / ".tools"))
from msys_argv_guard import msys_safe_run  # noqa: E402

BUCKET = "opal-data-portal-v2"
ARM1 = ("benchmarks/data_20261005_v1.pkl", "fPWS_TCLSvx2dW9SZGDl3hcQL735m5XJ",
        "2026-10-06T12:29:21Z pull")
ARM2 = ("benchmarks/data_20261007_v1.pkl", "F2HhLHRpKgZ18hIWMRJr3p3t4T52RfBW",
        "2026-10-07T01:26:10Z re-pull")
PARENT_COMMIT = "c38d69aa3db051a1eb9ce7773301f8e4992bea96"
PARENT_BLOB = "f4ee4cae0d5707b26e46b3a5c535f5c9fc23d25a"
SPX_TICKER = "SPX Index"
THE_SEVEN = [".INT_BMK Index", ".LT_BMK Index", ".LT_ETF Index", ".ST_BMK Index",
             ".ST_ETF Index", ".UST_BMK Index", ".UST_ETF Index"]

failures: list = []


def check(label: str, got, want) -> None:
    ok = got == want
    if not ok:
        failures.append(label)
    print(f"  {'OK  ' if ok else 'FAIL'} {label}")
    if not ok:
        print(f"       want: {want!r}")
        print(f"       got : {got!r}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def fetch(dest_dir: Path, key: str, version_id: str) -> Path:
    import boto3
    out = dest_dir / os.path.basename(key)
    boto3.client("s3").download_file(BUCKET, key, str(out),
                                     ExtraArgs={"VersionId": version_id})
    return out


def materialize_parent(tmp: Path) -> Path:
    """The tzero copy as it stood BEFORE this cell, straight out of git."""
    r = msys_safe_run(["git", "-C", str(REPO), "show", f"{PARENT_COMMIT}:{REL_TZERO}"],
                      capture_output=True, text=True, timeout=60)
    body = r.stdout or ""
    out = tmp / "tzero_parent_bbg_pkl_tripwire.py"
    out.write_text(body, encoding="ascii", newline="")
    # The hash IS the control: a mangled git show returns clean-empty on this platform.
    h = subprocess.run([sys.executable, "-c",
                        "import hashlib,sys,io;b=io.open(sys.argv[1],'rb').read();"
                        "print(hashlib.sha1(b'blob %d\\0'%len(b)+b).hexdigest())", str(out)],
                       capture_output=True, text=True).stdout.strip()
    print(f"       git show rc={r.returncode} bytes={len(body)} blob={h}")
    check("C4 the parent bytes retrieved are the bytes measured pre-edit (not a mangled empty)",
          h, PARENT_BLOB)
    return out


def leg(mod, path: Path):
    """Run the copy's own data-PKL leg with asof_ok held to the frame's own as-of, so the
    pre-existing as-of check passes and only the CIX limb can move the verdict."""
    with open(path, "rb") as f:
        d = pickle.load(f)
    rd = d["return_daily"]
    asof = pd.to_datetime(rd["date"]).max().date()
    reasons: list = []
    mod.check_data_pkl(str(path), {asof}, reasons)
    return reasons, asof, rd


def spx_last(rd: pd.DataFrame):
    sub = rd[rd["bbg_ticker"].astype(str) == SPX_TICKER]
    nn = sub[sub["price"].notna()]
    return pd.to_datetime(nn["date"]).dt.date.max() if len(nn) else None


def main() -> int:
    print(f"GUARD-4 PROOF -- module under proof: {TZERO}")
    print(f"  repo root resolved: {REPO}")
    print(f"  pandas {pd.__version__} | python {sys.version.split()[0]}")
    edited = load_module(TZERO, "tzero_edited")
    tmp = Path(tempfile.mkdtemp(prefix="guard4_proof_"))
    print(f"  scratch dir: {tmp}")

    print(f"\n[C1] {ARM1[2]} -- the EDITED tzero copy")
    p1 = fetch(tmp, ARM1[0], ARM1[1])
    reasons1, asof1, rd1 = leg(edited, p1)
    g1 = edited.grade_cix_series(rd1, asof1)
    print(f"       as-of resolved by the tzero copy: {asof1}")
    print(f"       custom CIX graded: {g1['graded']} | behind: {len(g1['behind'])} "
          f"| vendor not graded: {g1['vendor']}")
    check("C1 the edited tzero data leg FAILS", len(reasons1) > 0, True)
    check("C1 the CIX limb is why", sum(1 for r in reasons1 if "custom CIX" in r), 1)
    check("C1 the as-of check itself did not fail",
          sum(1 for r in reasons1 if "not in expected" in r), 0)
    check("C1 denominator 13 custom CIX graded", g1["graded"], 13)
    check("C1 7 behind, and they are the CRO trace's seven",
          sorted(tk for tk, _, _ in g1["behind"]), THE_SEVEN)
    check("C1 every one last non-null 2026-09-29",
          sorted({str(d) for _, _, d in g1["behind"]}), ["2026-09-29"])

    print(f"\n[C2] {ARM2[2]} -- the EDITED tzero copy")
    p2 = fetch(tmp, ARM2[0], ARM2[1])
    reasons2, asof2, rd2 = leg(edited, p2)
    g2 = edited.grade_cix_series(rd2, asof2)
    print(f"       as-of {asof2} | graded {g2['graded']} | behind {len(g2['behind'])}")
    check("C2 the edited tzero data leg PASSES", reasons2, [])
    check("C2 13 of 13 reach the as-of", (g2["graded"], len(g2["behind"])), (13, 0))

    print("\n[C3] CONTROL -- SPX is a vendor series")
    for tag, rd, asof, g in (("C1 pull", rd1, asof1, g1), ("C2 re-pull", rd2, asof2, g2)):
        last = spx_last(rd)
        print(f"       {tag}: SPX last non-null={last} in graded set={SPX_TICKER in g['tickers']}")
        check(f"C3 {tag}: SPX present (control is live)",
              SPX_TICKER in set(rd["bbg_ticker"].astype(str)), True)
        check(f"C3 {tag}: SPX not graded as custom", SPX_TICKER in g["tickers"], False)
        check(f"C3 {tag}: SPX reaches the as-of, unaffected", last, asof)

    print("\n[C4] THE NEGATIVE CONTROL -- the tzero copy at its PARENT commit, frozen pull")
    parent_path = materialize_parent(tmp)
    parent = load_module(parent_path, "tzero_parent")
    check("C4 the parent copy has NO CIX limb at all",
          hasattr(parent, "grade_cix_series"), False)
    reasons_p, asof_p, rd_p = leg(parent, p1)
    print(f"       parent copy on the FROZEN pull: as-of {asof_p}, reasons={reasons_p}")
    check("C4 the parent copy reads PASS on the frozen pull -- the gap the port closes",
          reasons_p, [])
    check("C4 so the port is the difference: same pull, parent PASS vs edited FAIL",
          (len(reasons_p), len(reasons1) > 0), (0, True))

    print("\n[C5] the tzero copy's OWN as-of-scoped presence check does NOT cover this")
    print("     (this closes the one claim row OPAL_BBGTML-Z-S12 left NOT MEASURED)")
    rd_dates = pd.to_datetime(rd1["date"])
    on_asof = set(rd1.loc[rd_dates.dt.date == asof1, "index_name"].unique())
    absent = edited.MODEL_INDEX_NAMES - on_asof
    print(f"       MODEL_INDEX_NAMES absent on the as-of: {sorted(absent)}")
    print(f"       benchmark/ETF series frozen on the same pull: {len(g1['behind'])}")
    check("C5 on the frozen pull all 5 MODELS do reach the as-of", sorted(absent), [])
    check("C5 while 7 benchmark/ETF series do not", len(g1["behind"]), 7)
    check("C5 none of the 7 is in MODEL_INDEX_NAMES, so the presence check cannot see them",
          sorted(n for _, n, _ in g1["behind"] if n in edited.MODEL_INDEX_NAMES), [])

    print(f"\nARMS: 5 | CHECKS: {len(failures)} failed")
    if failures:
        print("GUARD-4: FAIL -- " + "; ".join(failures))
        return 1
    print("GUARD-4: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
