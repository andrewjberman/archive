#!/usr/bin/env python3
"""HVST-w-2 AC4 (JUDGMENT -- PRESENTED, NOT GRADED; status UNVERIFIABLE-BY-INSTRUMENT, L9 = 3.0.0_SA_CVO~Z).

Question: are the rows `--new-only` skipped truly already held -- the SAME article -- or did a url/id mismatch skip a
NEW one? This script presents, per skipped listing item, the item's identifying fields beside the held article it was
matched to. It records NO verdict.

How a skip is decided by the producer (publishers.py seeking_alpha): a listing item is skipped when its `id` is in
`known_ids` (the local `articles` rows for THIS security), or `reuse()` finds it in the storage catalog, or the
harvest-grammar `article_known` finds the bronze article key in the bucket. The producer records no per-item skip
event, so the population of skips is reconstructed here from (1) the listing bytes the capture fetched (the local
listing outbox files) and (2) the receipts' accepted ids and the before-snapshot of held articles AC1 saved.

OFFLINE: reads w2_ac1_state.json and the local outbox; no network, no S3. `--selftest` exercises the matching code on
FABRICATED data only (output not part of any proof).
"""
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
REPO = HERE.parents[7]
SAMPLE_CAP = 40


def match_rows(items, held, accepted_ids, security_key):
    """items: listing items [{id,title,url,publishOn}]; held: {article_id: [held rows]}. Returns presentation rows."""
    out = []
    for it in items:
        iid = str(it.get("id"))
        if iid in accepted_ids:
            out.append(("ACCEPTED-THIS-RUN", it, None))
        elif iid in held:
            same_sec = [h for h in held[iid] if h["security_key"] == security_key]
            out.append(("SKIPPED: held for THIS security (known_ids)" if same_sec else "SKIPPED: held under ANOTHER security (reuse)",
                        it, (same_sec or held[iid])[0]))
        else:
            out.append(("NOT SKIPPED, NOT ACCEPTED (beyond the article target, rejected, or unreached)", it, None))
    return out


def present(rows, label):
    skips = [r for r in rows if r[0].startswith("SKIPPED")]
    print("%s: %d listing items; skipped %d; accepted %d; neither %d" % (
        label, len(rows), len(skips), sum(r[0].startswith("ACCEPTED") for r in rows),
        sum(r[0].startswith("NOT") for r in rows)))
    if len(skips) <= SAMPLE_CAP:
        sample, why = skips, "ALL skips (%d <= %d), a census: no selection to argue about" % (len(skips), SAMPLE_CAP)
    else:
        step = len(skips) / float(SAMPLE_CAP)
        sample = [skips[int(k * step)] for k in range(SAMPLE_CAP)]
        why = "every %.2fth of %d skips in listing order (deterministic, spans all ranks); sized at %d so each is read" % (step, len(skips), SAMPLE_CAP)
    print("sample: %s" % why)
    for kind, it, h in sample:
        attrs = it.get("attributes") or {}
        print("  SKIPPED ITEM   id=%s | title=%r | url=%s | published=%s" % (
            it.get("id"), (attrs.get("title") or it.get("title")), (it.get("links") or {}).get("self") or it.get("url"),
            attrs.get("publishOn") or it.get("published")))
        print("  HELD ARTICLE   id=%s | title=%r | url=%s | published=%s | held under security_key=%s" % (
            h["article_id"], h["title"], h["url"], h["published"], h["security_key"]))
        print("  matched by: %s" % kind)


def selftest():
    print("SELFTEST on FABRICATED data (not evidence)")
    held = {"1": [{"article_id": "1", "security_key": "S", "title": "Held one", "url": "u1", "published": "p1"}]}
    items = [{"id": 1, "attributes": {"title": "Held one", "publishOn": "p1"}, "links": {"self": "/news/1-x"}},
             {"id": 2, "attributes": {"title": "New two"}, "links": {"self": "/news/2-y"}}]
    present(match_rows(items, held, {"2"}, "S"), "selftest job")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return 0
    st = json.loads((DELIV / "w2_ac1_state.json").read_text(encoding="utf-8"))
    common = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--git-common-dir"], capture_output=True, text=True,
                            check=True).stdout.strip()
    main_tree = (Path(common) if Path(common).is_absolute() else (REPO / common)).resolve().parent
    rt = main_tree / ".runtime" / "opal-data-harvest"
    held = {}
    for h in st["held_before"]:
        held.setdefault(str(h["article_id"]), []).append(h)
    print("AC4 -- PRESENTED FOR L9, NOT GRADED HERE (judgment; status UNVERIFIABLE-BY-INSTRUMENT; grader 3.0.0_SA_CVO~Z)")
    print("held sa articles BEFORE the capture (AC1's snapshot of progress.sqlite3 `articles`): %d rows, %d distinct article ids, "
          "%d distinct securities" % (len(st["held_before"]), len(held), len({h["security_key"] for h in st["held_before"]})))
    t0, t1 = st["started_at"], st["finished_at"]
    con = sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % rt.as_posix(), uri=True)
    try:
        listings = con.execute("SELECT id,query,page,fetched_at,path,status FROM harvest_listing_outbox WHERE publisher='sa' "
                               "AND fetched_at >= ? AND fetched_at <= ?", (t0, t1)).fetchall()
    finally:
        con.close()
    print("sa listing pages fetched by the capture (local listing outbox, fetched_at within %s .. %s): %d" % (t0, t1, len(listing_ids(listings))))
    jobs = [j for i in st["invocations"] for j in i["jobs"]]
    total_skips = 0
    for j in jobs:
        acc = {str(a["article_id"]) for a in j["accepted"]}
        mine = [row for row in listings if row[1] == j["sa_symbol"]]
        held_here = sorted(h["article_id"] for h in st["held_before"] if h["security_key"] == j["security_key"])
        print("\njob %s | %s (sa_symbol %s) | status=%s bucket=%s | previously_stored=%s | accepted %d | held for this security before: %d %s" % (
            j["job_id"], j["security_key"], j["sa_symbol"], j["status"], j["bucket"], j["previously_stored"], len(acc), len(held_here),
            held_here[:8]))
        if not mine:
            print("  no listing page was fetched for this job (bucket=%s%s), so it has NO candidate items and made NO --new-only skip; "
                  "nothing to lay out. %s" % (
                      j["bucket"], ", status " + str(j["status"]),
                      "It was suppressed by the cooldown BEFORE it read known_ids, so its held count above is what --new-only WOULD have skipped, not what it did."
                      if j["bucket"] == "cooldown_suppressed" else
                      "Its account check returned an HTTP error before any listing request (see the ledger CALL 2 row)."))
            continue
        for row in mine:
            payload = json.loads(Path(row[4]).read_text(encoding="utf-8"))
            rows = match_rows(payload.get("data", []), held, acc, j["security_key"])
            total_skips += sum(r[0].startswith("SKIPPED") for r in rows)
            present(rows, "job %s listing page %s" % (j["job_id"], row[2]))
    print("\nTOTAL --new-only skips reconstructed across %d jobs: %d" % (len(jobs), total_skips))
    if total_skips == 0:
        print("ZERO skips to present. CAUSE: the capture never fetched a sa listing page -- job 1's account check returned HTTP 402 "
              "(events.jsonl, 351 B), the producer set a 3600 s sa cooldown, and the other 4 jobs were cooldown-suppressed. The "
              "--new-only skip logic was therefore never exercised on real listing items in this cell; whether it would drop a NEW "
              "article on an id/url mismatch is NOT answered by this run.")
    print("NO VERDICT RECORDED (judgment criterion; L9 grades it).")
    return 0


def listing_ids(rows):
    return [r[0] for r in rows]


if __name__ == "__main__":
    sys.exit(main())
