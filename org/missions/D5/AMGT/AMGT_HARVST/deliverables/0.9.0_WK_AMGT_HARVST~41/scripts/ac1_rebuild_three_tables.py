"""HVST-d-2 AC1: THE ACT. Rebuild article_security_mention -> chatter_daily -> chatter_event with the
common-name aliases, ONE put per table (write_gold, IfNoneMatch="*"), and prove the result landed inside
the never-widen pair ON THE SERVED PLANE (rows re-read from S3). No delete of any kind, no vendor call.

STOP RULES (nothing is written past the first that fires):
  * the BEFORE-state differs from the COO half s.3           -> STOP before the first put (exit 2, BLOCKING)
  * --as-of (today UTC) is not 2026-09-29 or 2026-09-30      -> STOP before the first put (exit 2)
  * the in-memory PREFLIGHT already moves a row outside the pair -> STOP before the first put (exit 2)
  * a producer exits non-zero (PreconditionFailed, HarvestStoreError read-back) -> report verbatim, build no later table
A second run finds the BEFORE-state changed and STOPs at the first rule, so this script cannot double-put."""
import datetime
import json
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _rebuild as R  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

ALLOWED_AS_OF = (datetime.date(2026, 9, 29), datetime.date(2026, 9, 30))
CLI = {pg.GOLD_TABLE: "build-mention", pg.GOLD_DAILY_TABLE: "build-daily", pg.GOLD_EVENT_TABLE: "build-event"}


def brief(e):
    return "%s %s..%s days=%s articles=%s A=%s B=%s pubs=%s lead=%s | %s" % (
        e["security_key"], e["first_day"], e["last_day"], e["days_span"], e["articles_total"], e["tier_a"],
        e["tier_b"], e["publishers_distinct"], e["lead_article_key"], R.a(e.get("lead_headline"), 80))


def main():
    client = store._default_client()
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    print("== (a) BEFORE, from S3 (as-of for the run = %s UTC) ==" % as_of)
    before_parts, before_rows = {}, {}
    stop = None
    for t in R.TABLES:
        ps = R.parts(t, client)
        before_parts[t] = ps
        newest = ps[-1]
        rows = R.read_key(newest[0], client)
        before_rows[t] = rows
        want = R.BEFORE_EXPECT[t]
        print("%-26s parts=%d newest=%s ETag=%s rows=%d   (expected parts=%d newest=%s ETag=%s rows=%d)" % (
            t, len(ps), R.short(newest[0]), newest[1], len(rows), want[0], want[1], want[2], want[3]))
        for k, etag, size in ps:
            print("    part %-60s ETag=%s size=%d" % (R.short(k), etag, size))
        if (len(ps), R.short(newest[0]).replace(".parquet", ""), newest[1], len(rows)) != want:
            stop = "BEFORE-STATE of %s differs from the COO half s.3" % t
    if as_of not in ALLOWED_AS_OF:
        stop = "as-of %s is outside both halves (2026-09-29 or 2026-09-30 only)" % as_of
    if stop:
        print("STOP BEFORE THE FIRST PUT: %s. Nothing written. This is a BLOCKING row." % stop)
        print("AC1 FAIL")
        return 2

    print("\n== (a2) PREFLIGHT, in memory, against the pair (no put yet) ==")
    securities = R.load_securities()
    mem, n_art, _t = R.memory(securities, as_of, client)
    pm = R.classify_mention(before_rows[R.TABLES[0]], mem[R.TABLES[0]])
    pd = R.classify_daily(before_rows[R.TABLES[1]], mem[R.TABLES[1]], as_of)
    pe = R.classify_event(before_rows[R.TABLES[2]], mem[R.TABLES[2]])
    R.print_classification("preflight", pm, pd, pe)
    if pm["outside"] + pd["outside"] + pe["outside"]:
        print("STOP BEFORE THE FIRST PUT: the in-memory rebuild already moves rows outside the pair. Nothing written.")
        print("AC1 FAIL")
        return 2
    print("preflight inside the pair; %d securities, %d silver articles" % (len(securities), n_art))

    print("\n== (b) THE PRODUCERS, each once, verbatim ==")
    written = {}
    failed = None
    for t in R.TABLES:
        cmd = [sys.executable, "-m", "lib.research.harvest.publication_gold", CLI[t],
               "--securities-json", R.SECURITIES, "--as-of", as_of.isoformat()]
        print("$ python -m lib.research.harvest.publication_gold %s --securities-json <securities.universe.json> --as-of %s" % (CLI[t], as_of))
        proc = subprocess.run(cmd, cwd=R.REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(proc.stdout.rstrip())
        if proc.stderr.strip():
            print("stderr: " + proc.stderr.strip()[-1500:])
        print("rc=%d" % proc.returncode)
        if proc.returncode != 0:
            failed = t
            print("STOP: %s failed; the distrusted object (if any) stays and no later table is built." % t)
            break
        receipt = json.loads(proc.stdout.strip().splitlines()[-1])
        key = receipt["key"]
        head = client.head_object(Bucket=store.HARVEST_BUCKET, Key=key)
        written[t] = (key, head["ETag"].strip('"'), head["ContentLength"])
        print("write_gold receipt: key=%s ContentLength=%d ETag=%s" % (key, head["ContentLength"], written[t][1]))

    print("\n== (c) AFTER, re-read through publication_gold._latest_gold_snapshot_rows ==")
    after_parts, after_rows = {}, {}
    ok_c = True
    for t in R.TABLES:
        ps = R.parts(t, client)
        after_parts[t] = ps
        via = pg._latest_gold_snapshot_rows(t, client=client)
        after_rows[t] = via
        newest = ps[-1]
        is_written = t in written and newest[0] == written[t][0]
        direct = R.read_key(newest[0], client)
        same = [R.canon_row(r) for r in via] == [R.canon_row(r) for r in direct]
        print("%-26s parts=%d (was %d) newest=%s ETag=%s rows=%d  newest is the part just written: %s ; _latest_gold_snapshot_rows == that object: %s" % (
            t, len(ps), len(before_parts[t]), R.short(newest[0]), newest[1], len(via), is_written, same))
        ok_c = ok_c and is_written and same and len(ps) == len(before_parts[t]) + 1
    if failed:
        print("AC1 FAIL (producer for %s failed)" % failed)
        return 1

    print("\n== (d) MOVED ROWS against the pair, on the rows re-read from S3 ==")
    m = R.classify_mention(before_rows[R.TABLES[0]], after_rows[R.TABLES[0]])
    d = R.classify_daily(before_rows[R.TABLES[1]], after_rows[R.TABLES[1]], as_of)
    e = R.classify_event(before_rows[R.TABLES[2]], after_rows[R.TABLES[2]])
    R.print_classification("served", m, d, e)
    per = {}
    for p in m["added"]:
        per.setdefault(p[1], [0, 0])[0] += 1
    for p, _f in m["changed"]:
        per.setdefault(p[1], [0, 0])[1] += 1
    print("mention: every moved security (rows added / existing rows changed): %s" % json.dumps({k: v for k, v in sorted(per.items())}))
    print("daily: moved cells by security (days <= %s): %s ; extension cells (%s..%s) for all 191 securities: %d" % (
        d["srv_end"], d["moved"], d["srv_end"] + datetime.timedelta(days=1), as_of, d["ext"]))
    outside = m["outside"] + d["outside"] + e["outside"]
    print("rows OUTSIDE THE PAIR: %d" % len(outside))

    print("\n== (e) EVERY SERVED EVENT and what it became ==")
    b_ev = {r["event_id"]: r for r in before_rows[R.TABLES[2]]}
    a_ev = {r["event_id"]: r for r in after_rows[R.TABLES[2]]}
    for eid in sorted(b_ev, key=lambda i: (b_ev[i]["security_key"], b_ev[i]["first_day"])):
        fate = "kept" if eid in e["kept"] else ("moved" if eid in a_ev else "gone")
        print("  %-5s %s" % (fate.upper(), brief(b_ev[eid])))
    for eid in e["added"]:
        print("  NEW   %s" % brief(a_ev[eid]))
    print("served events: kept=%d moved=%d gone=%d ; new events=%d" % (len(e["kept"]), len(e["moved"]), len(e["gone"]), len(e["added"])))

    print("\n== (f) event_id unique ==")
    print("event_id unique in the served newest part: %s (%d ids, %d rows)" % (e["unique"], len(a_ev), len(after_rows[R.TABLES[2]])))

    print("\n== (g) EVERY PRIOR PART still exists, ETag unchanged ==")
    ok_g = True
    for t in R.TABLES:
        now = {k: (etag, size) for k, etag, size in after_parts[t]}
        bad = [k for k, etag, size in before_parts[t] if now.get(k) != (etag, size)]
        new = [k for k in now if k not in {p[0] for p in before_parts[t]}]
        print("%-26s prior parts %d of %d present with ETag and size unchanged ; parts added=%d %s" % (
            t, len(before_parts[t]) - len(bad), len(before_parts[t]), len(new), [R.short(k) for k in new]))
        ok_g = ok_g and not bad and len(new) == 1

    print("\n== S3 KEYS WRITTEN ==")
    for t in R.TABLES:
        k, etag, size = written[t]
        print("s3://%s/%s ETag=%s ContentLength=%d" % (store.HARVEST_BUCKET, k, etag, size))

    ok = ok_c and ok_g and not outside and e["unique"]
    for label, res in (("(c) newest part is the one just written, one part added per table", ok_c),
                       ("(d) zero rows outside the pair", not outside), ("(f) event_id unique", e["unique"]),
                       ("(g) prior parts intact", ok_g)):
        print("CHECK %-62s %s" % (label, "PASS" if res else "FAIL"))
    print("AC1 %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
