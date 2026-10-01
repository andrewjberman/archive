"""RIV-i-1 AC1 -- issuer positions resolve to a security key by a MEASURED join, never a guess (rows W1-S4/S5;
analysis ruling 6), and Bloomberg rows carry their key in the crosswalk's grammar.

Real data: the 2 newest BASG issuer days (2026-09-25, 2026-09-28) land as issuer bronze -> silver; the PFOE-group Excel BQL
captures for the same two dates import as Bloomberg bronze -> silver -- with ONE plant in the 2026-09-28 copy: an extra
BASG row 'ABNB LN Equity' whose POSITION equals the issuer's ABNB quantity (a second candidate for the same root ticker).
canonical_shape for 2026-09-28 then shows:
  - BASG (source issuer), non-cash rows other than ABNB: at least 95% RESOLVED, each joined row's security_id equal to the
    key grammar (spaces -> underscores) of a BASG Bloomberg row id at that date;
  - the issuer ABNB row is UNRESOLVED and its resolution_note names BOTH candidates (ambiguity is refused, never guessed);
  - Bloomberg-sourced PFOE rivals (WCMG, TSEL, ETFT, PCLG), non-cash rows: at least 95% RESOLVED, security_id in the key
    grammar of the row's own Bloomberg id;
  - the resolved fraction per fund is printed (the measured value RIV-d-4 sets the identity floor from).
Measured at the cut: root ticker equal AND |q_issuer - q_bloomberg| / q_bloomberg <= 2% joins 34 of 34 BASG non-cash rows on
2026-09-28 with 0 ambiguous; exact share equality joins 0 (the two sources differ by ~0.1% on the same report date)."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402

D0, D1 = "2026-09-25", "2026-09-28"


def planted_pfoe(sink_tmp: pathlib.Path) -> list[pathlib.Path]:
    out = []
    issuer_abnb = None
    for line in (c.main_root() / c.PFOE_CAPTURES_REL / "basg" / f"{D1}.txt").read_text(encoding="utf-8").splitlines()[1:]:
        f = line.split("|")
        if len(f) > 13 and f[4] == "BASG" and f[11].strip() == "ABNB":
            issuer_abnb = float(f[13])
    for d in (D0, D1):
        cap = c.capture(c.pfoe_capture(d))
        if d == D1:
            hdr = cap["rows"][0]
            tmpl = next(r for r in cap["rows"][1:] if str(r[hdr.index("ORIG_IDS")]).startswith("BASG")
                        and str(r[hdr.index("ID")]) == "ABNB US Equity")
            extra = list(tmpl)
            extra[hdr.index("ID")] = "ABNB LN Equity"
            extra[hdr.index("id()")] = "ABNB LN Equity"
            extra[hdr.index("POSITION")] = issuer_abnb
            cap = {**cap, "rows": cap["rows"] + [extra]}
        p = sink_tmp / f"{d}.json"
        p.write_text(json.dumps(cap), encoding="utf-8")
        out.append(p)
    return out


def frac(g):
    nc = g[~g["is_cash_line"].astype(bool)]
    return (int((nc["resolution_status"] == "RESOLVED").sum()), len(nc))


def run(v):
    c.setup_path()
    files = [p for p in c.archive_files(2)]
    sink = c.tmpdir("rv_i1a_")
    c.land(sink, files)
    c.replay("silver_issuer", sink, D1)
    caps = planted_pfoe(pathlib.Path(c.tmpdir("rv_i1p_")))
    c.import_bloomberg(sink, caps, batch_id="i1-imp")
    c.replay("silver_bloomberg", sink, D1)
    c.replay("gold_canonical_shape", sink, D1, batch_id="i1-g1")
    df, _ = c.read_parquets(c.gold_dir(sink, "canonical_shape") / f"date={D1}")
    latest = df[df["dataset_revision"] == df["dataset_revision"].max()]
    basg = latest[latest["fund_ticker"].astype(str).str.strip() == "BASG"]
    abnb = basg[basg["security_ticker"].astype(str).str.strip() == "ABNB"]
    rest = basg[basg["security_ticker"].astype(str).str.strip() != "ABNB"]
    ok, n = frac(rest)
    print(f"BASG (issuer) non-cash resolved {ok}/{n}")
    v.check(n > 0 and ok / n >= 0.95, f"BASG non-cash resolved >= 95% ({ok}/{n})")
    keys = set(latest.loc[latest["fund_ticker"].astype(str).str.strip() == "BASG", "security_id"].dropna().astype(str))
    bbg_keys = {s.replace(" ", "_") for s in (r[0] for r in [(x,) for x in _bbg_ids(caps[-1])])}
    joined = rest[rest["resolution_status"] == "RESOLVED"]
    v.check(len(joined) > 0 and set(joined["security_id"].astype(str)) <= bbg_keys,
            f"every joined BASG key is a BASG Bloomberg id in key grammar ({sorted(set(joined['security_id'].astype(str)) - bbg_keys)[:3]})")
    note = " ".join(abnb["resolution_note"].dropna().astype(str))
    v.check(len(abnb) == 1 and str(abnb["resolution_status"].iloc[0]) == "UNRESOLVED"
            and "ABNB US Equity" in note and "ABNB LN Equity" in note,
            f"ambiguous ABNB refused, both candidates named ({abnb['resolution_status'].tolist()}, {note[:120]!r})")
    for f in ("WCMG", "TSEL", "ETFT", "PCLG"):
        g = latest[latest["fund_ticker"].astype(str).str.strip() == f]
        ok, n = frac(g)
        good = g[(g["resolution_status"] == "RESOLVED") & ~g["is_cash_line"].astype(bool)]
        gram = all(str(a) == str(b).split(":")[0].replace(" ", "_") for a, b in zip(good["security_id"], good["position_id"]))
        print(f"{f} (bloomberg) non-cash resolved {ok}/{n}")
        v.check(n > 0 and ok / n >= 0.95 and gram, f"{f}: >= 95% resolved in the key grammar ({ok}/{n})")
    del keys


def _bbg_ids(cap_path):
    cap = c.capture(cap_path)
    hdr = cap["rows"][0]
    return [r[hdr.index("ID")] for r in cap["rows"][1:] if str(r[hdr.index("ORIG_IDS")]).startswith("BASG")]


failures = c.guarded("AC1", run)
print("AC1 RESULT: PASS 0 failures" if failures == 0 else f"AC1 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
