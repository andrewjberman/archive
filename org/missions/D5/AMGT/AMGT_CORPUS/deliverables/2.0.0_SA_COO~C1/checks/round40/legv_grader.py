"""AMGT_CORPUS round 40, CRPS-ap-10 (b) leg v (and (u) C1) -- grade one scheduled fire from the evidence file the site-Z read
order writes (AMGT_CORPUS.TO-READ-R40-ap10b-lv.*: sections `## fire log` and `## budget ledger`), plus BA US's newest served
model block read from S3 on this box.

Read-only: it reads one local file and S3 objects; no Bloomberg call, no write.

  python legv_grader.py <evidence.txt> <YYYY-MM-DD>      (PYTHONPATH=. from the repository root)
  python legv_grader.py --s3 <YYYY-MM-DD>                 (the dell1-readable side only, no site-Z file)

--s3 prints S1 (how many security keys carry a derived model block stamped <day>, against the 96 registered) and S2 (WHICH
pin fired, read from BA US's newest block of <day>: the four dispersion fields' unit is the pointer `SEE field_map.json` on
6402de5137 and a measured unit on 7580fe909c), then C1. It grades nothing site-Z-only: L2 and L3 need the site-Z evidence file.

Prints one line per limb and a last line `legv build <passed>/<graded>`:
  L1 fire      the refresh line reads `pulled 96 bloomberg_calls 768` and the fire's own line reads `as_of <day> rc 0`;
  L2 record    exactly one `budget_record amgt-model-block ... written 1` line in the fire log;
  L3 ledger    exactly one ledger line of mode `amgt-model-block` whose rows equal L2's records and whose batch_id ends
               `rows_unit=returned-records` (the (b) CTO half C1); every ledger line and the day's spent sum are printed;
  C1 (u)       BA US FY1 BEST_EPS_STDDEV beside FY1 BEST_EPS with unit and currency, from the newest block stamped <day>
               (printed, not graded: the unit is the pointer until (u) is fired).
"""
import json
import re
import sys

BUDGET_MODE = "amgt-model-block"
RE_REFRESH = re.compile(r"^refresh population registered (\d+) with_block (\d+) already_current (\d+) pulled (\d+) bloomberg_calls (\d+)$")
RE_RECORD = re.compile(
    r"^budget_record amgt-model-block rows (\d+) records (\d+) calls (\d+) security_fields (\d+) written ([01])$"
)


def sections(text):
    """{heading: [lines]} for every `## <heading>` in the evidence file."""
    out, cur = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line.rstrip("\r"))
    return out


def ledger_lines(lines):
    rows = []
    for line in lines:
        s = line.strip()
        if s.startswith("{"):
            try:
                rows.append(json.loads(s))
            except ValueError:
                continue
    return rows


def ba_c1(day):
    sys.path.insert(0, "integrations/bloomberg/research")
    import model_block_pull as m

    s3 = m._s3()
    prefix = f"derived/{m.ENGINE}/BA_US_Equity/"
    keys = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=m.BUCKET, Prefix=prefix).get("Contents", []))
    stamp_day = day.replace("-", "")
    keys = [k for k in keys if k[len(prefix):].startswith(stamp_day)]
    if not keys:
        return f"C1 (u)       ABSENT: no BA US block stamped {day} under {prefix}"
    doc = json.loads(s3.get_object(Bucket=m.BUCKET, Key=keys[-1])["Body"].read())
    figs = {(f.get("mnemonic"), f.get("fiscal_period")): f for f in doc.get("figures", [])}
    out = [f"C1 (u)       block {keys[-1]}"]
    for mne in ("BEST_EPS", "BEST_EPS_STDDEV"):
        f = figs.get((mne, "FY1"))
        if f is None:
            out.append(f"               {mne} FY1 ABSENT")
        else:
            out.append(f"               {mne} FY1 value {f.get('value')} currency {f.get('currency')} unit {f.get('unit')!r}")
    return "\n".join(out)


FOUR = ("BEST_CPS_STDDEV", "BEST_CPS_NUMEST", "BEST_EPS_STDDEV", "BEST_EPS_NUMEST")


def s3_side(day):
    sys.path.insert(0, "integrations/bloomberg/research")
    import model_block_pull as m

    s3 = m._s3()
    stamp_day = day.replace("-", "")
    latest = m._model_block_latest_stamps(s3)
    today = sorted(k for k, st in latest.items() if st.startswith(stamp_day))
    print(f"S1 blocks    {len(today)} security key(s) carry a derived block stamped {day} (registered 96)")
    prefix = f"derived/{m.ENGINE}/BA_US_Equity/"
    keys = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=m.BUCKET, Prefix=prefix).get("Contents", []))
    keys = [k for k in keys if k[len(prefix):].startswith(stamp_day)]
    if not keys:
        print(f"S2 pin       UNREAD: no BA US block stamped {day}")
        return 1
    doc = json.loads(s3.get_object(Bucket=m.BUCKET, Key=keys[-1])["Body"].read())
    units = sorted({str(f.get("unit")) for f in doc.get("figures", []) if f.get("mnemonic") in FOUR})
    pointer = any(u.startswith("SEE field_map.json") for u in units)
    print(f"S2 pin       {'a pin WITHOUT the map (pointer unit; today 6402de5137)' if pointer else 'a pin WITH the map (measured unit; today 7580fe909c)'}: block {keys[-1]}; units {units}")
    print(ba_c1(day))
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "--s3":
        return s3_side(argv[2])
    if len(argv) != 3:
        print(__doc__)
        return 2
    path, day = argv[1], argv[2]
    sec = sections(open(path, encoding="utf-8").read())
    fire = [s.strip() for s in sec.get("fire log", [])]
    passed = graded = 0

    graded += 1
    refresh = [RE_REFRESH.match(s) for s in fire]
    refresh = [r for r in refresh if r]
    done = f"induction_scheduled mode fire as_of {day} rc 0" in "\n".join(fire)
    ok = len(refresh) == 1 and refresh[0].group(4) == "96" and refresh[0].group(5) == "768" and done
    passed += ok
    got = refresh[0].group(0) if refresh else "no refresh line"
    print(f"L1 fire      {'PASS' if ok else 'FAIL'}: {got}; fire line as_of {day} rc 0 {'present' if done else 'ABSENT'}")

    graded += 1
    recs = [RE_RECORD.match(s) for s in fire]
    recs = [r for r in recs if r]
    ok = len(recs) == 1 and recs[0].group(5) == "1"
    passed += ok
    records = int(recs[0].group(2)) if recs else None
    print(f"L2 record    {'PASS' if ok else 'FAIL'}: {len(recs)} budget_record line(s)" + (f": {recs[0].group(0)}" if recs else ""))

    graded += 1
    rows = ledger_lines(sec.get("budget ledger", []))
    mine = [r for r in rows if r.get("mode") == BUDGET_MODE]
    ok = (
        len(mine) == 1
        and records is not None
        and int(mine[0].get("rows", -1)) == records
        and str(mine[0].get("batch_id", "")).endswith("rows_unit=returned-records")
    )
    passed += ok
    print(f"L3 ledger    {'PASS' if ok else 'FAIL'}: {len(rows)} ledger line(s), {len(mine)} of mode {BUDGET_MODE}; "
          f"spent {day} = {sum(int(r.get('rows', 0)) for r in rows)}")
    for r in rows:
        print(f"               {json.dumps(r)}")
    if mine and records:
        print(f"               rows {mine[0].get('rows')} vs records {records}; vs the 4,224 the CTO half expects: "
              f"{int(mine[0].get('rows', 0)) / 4224:.3f}")

    try:
        print(ba_c1(day))
    except Exception as exc:  # noqa: BLE001 -- C1 is printed, never graded
        print(f"C1 (u)       UNREAD: {type(exc).__name__}: {exc}")

    print(f"legv build {passed}/{graded}")
    return 0 if passed == graded else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
