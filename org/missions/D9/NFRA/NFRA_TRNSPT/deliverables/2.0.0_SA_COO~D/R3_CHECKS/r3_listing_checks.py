"""NFRA_TRNSPT round 3 -- the laptop's checks of the gateway's LISTING route (GET /hx/mail/messages).

The four checks of ORDER_FOR_SITE_Z_HX_MAIL_LISTING_ROUTE_20261001.md, run from the laptop against the released route
with the project's own client (data/transcripts/scripts/outlook/gateway_mail.py). Run from the repository root:

    python org/missions/D9/NFRA/NFRA_TRNSPT/deliverables/2.0.0_SA_COO~D/R3_CHECKS/r3_listing_checks.py

Prints only positions, counts, id tails, booleans and statuses: no address, no subject, no body. A sender is named
by its POSITION in the sorted author table. The bearer is read by name and held in memory only.

  CHECK 1  a table sender's window containing 2026-07-06 lists the row whose message_id ends AACniYutAAA=, and its
           internetMessageId equals the one the message route returns for that id
  CHECK 2  an off-table sender is 403 sender_not_allowed; a table sender's window with no mail is 200 with zero rows
  CHECK 3  page_size=1 over a window holding two or more rows pages to the end with no row twice and the same rows
           the default page size returns
  CHECK 4  a wrong bearer and no bearer are 401 on this path. (The transcripts and /ms bearers are other prefixes'
           secrets: this seat does not read them, so that arm stays site Z's own run.)

Last line: LISTING-CHECKS-OK n=4 or LISTING-CHECKS-FAIL <which>.
"""
import hashlib
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.getcwd())
from data.transcripts.scripts.outlook import criterion, gateway_mail  # noqa: E402

TAIL = "AACniYutAAA="
OFF_TABLE = "nobody@off-table.example.invalid"


def utc(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


def h16(text):
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def main():
    bearer = gateway_mail.read_bearer()
    client = gateway_mail.HxMailClient(bearer)
    senders = sorted(criterion.load_tables()[0])
    failed = []
    print("author table: %d sender(s); the route's base %s" % (len(senders), client.base_url))

    # ---- CHECK 1
    found = None
    per_sender = []
    for index, sender in enumerate(senders):
        try:
            rows = client.list_rows(sender, utc(2026, 7, 1), utc(2026, 7, 15))
        except gateway_mail.HxMailRefused as exc:
            per_sender.append("sender[%d] status=%s error=%s" % (index, exc.status, exc.error))
            continue
        per_sender.append("sender[%d] rows=%d" % (index, len(rows)))
        for row in rows:
            if row["message_id"].endswith(TAIL):
                found = (index, sender, row)
    print("CHECK 1 window 2026-07-01..2026-07-15: " + "; ".join(per_sender))
    ok1 = False
    if found:
        index, sender, row = found
        _raw, message = client.message(row["message_id"])
        same = bool(row.get("internetMessageId")) and row.get("internetMessageId") == message.get("internetMessageId")
        keys = sorted(row.keys())
        ok1 = same and row.get("hasAttachments") is True
        print("CHECK 1 row ...%s listed under sender[%d]; internetMessageId equal to the message route's: %s "
              "(sha16 %s / %s); hasAttachments %s; row keys %s" % (
                  TAIL, index, same, h16(row.get("internetMessageId")), h16(message.get("internetMessageId")),
                  row.get("hasAttachments"), keys))
    else:
        print("CHECK 1 the row ...%s was NOT listed" % TAIL)
    if not ok1:
        failed.append("1")

    # ---- CHECK 2
    try:
        client.list_page(OFF_TABLE, "2026-07-01T00:00:00Z", "2026-07-15T00:00:00Z")
        off = "200 (NOT refused)"
    except gateway_mail.HxMailRefused as exc:
        off = "%s %s" % (exc.status, exc.error)
    table_sender = found[1] if found else senders[0]
    try:
        empty = client.list_page(table_sender, "2020-01-01T00:00:00Z", "2020-01-15T00:00:00Z")
        empty_line = "200 rows=%d count=%s next_page_token=%s" % (len(empty["rows"]), empty.get("count"), empty.get("next_page_token"))
        ok_empty = len(empty["rows"]) == 0 and empty.get("count") == 0 and empty.get("next_page_token") is None
    except gateway_mail.HxMailRefused as exc:
        empty_line, ok_empty = "%s %s" % (exc.status, exc.error), False
    too_long = None
    try:
        client.list_page(table_sender, "2026-01-01T00:00:00Z", "2026-03-15T00:00:00Z")
        too_long = "200 (a 73-day window was NOT refused)"
    except gateway_mail.HxMailRefused as exc:
        too_long = "%s %s" % (exc.status, exc.error)
    print("CHECK 2 off-table sender: %s | a table sender's empty window (2020-01-01..15): %s | a 73-day window: %s" % (
        off, empty_line, too_long))
    if not (off == "403 sender_not_allowed" and ok_empty and too_long == "400 invalid_window"):
        failed.append("2")

    # ---- CHECK 3
    ok3 = False
    window = None
    end = utc(2026, 10, 1)
    for _ in range(12):
        start = end - timedelta(days=31)
        rows = client.list_rows(table_sender, start, end)
        if len(rows) >= 2:
            window = (start, end, rows)
            break
        end = start
    if window:
        start, end, rows = window
        paged, tokens, token, pages = [], [], None, 0
        while True:
            doc = client.list_page(table_sender, gateway_mail._iso(start), gateway_mail._iso(end), True, token, 1)
            pages += 1
            paged += [r["message_id"] for r in doc["rows"]]
            token = doc.get("next_page_token")
            if not token or pages > 60:
                break
            tokens.append(token)
        default_ids = [r["message_id"] for r in rows]
        ordered = [r["receivedDateTime"] for r in rows] == sorted(r["receivedDateTime"] for r in rows)
        ok3 = len(paged) == len(set(paged)) == len(default_ids) and paged == default_ids and len(tokens) >= 1 \
            and len(set(tokens)) == len(tokens) and ordered
        print("CHECK 3 window %s..%s: default page size rows=%d; page_size=1 pages=%d rows=%d distinct=%d "
              "tokens=%d distinct tokens=%d; same rows in the same order: %s; ascending by receivedDateTime: %s" % (
                  start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"), len(default_ids), pages, len(paged),
                  len(set(paged)), len(tokens), len(set(tokens)), paged == default_ids, ordered))
    else:
        print("CHECK 3 no 31-day window with two or more rows was found in the last 12 windows")
    if not ok3:
        failed.append("3")

    # ---- CHECK 4
    def status_with(value):
        try:
            gateway_mail.HxMailClient(value).list_page(table_sender, "2026-07-01T00:00:00Z", "2026-07-15T00:00:00Z")
            return "200 (NOT refused)"
        except gateway_mail.HxMailRefused as exc:
            return "%s %s" % (exc.status, exc.error)

    wrong = status_with("not-the-bearer-" + "x" * 24)
    import json
    import urllib.error
    import urllib.request
    query = "sender=%s&received_from=2026-07-01T00:00:00Z&received_to=2026-07-15T00:00:00Z" % "x%40example.invalid"
    try:
        with urllib.request.urlopen(urllib.request.Request(client.base_url + gateway_mail.PREFIX + "/messages?" + query),
                                    timeout=30) as resp:
            none = "%s (NOT refused)" % resp.status
    except urllib.error.HTTPError as exc:
        try:
            none = "%s %s" % (exc.code, json.loads(exc.read().decode("utf-8")).get("error"))
        except Exception:
            none = "%s (no json)" % exc.code
    print("CHECK 4 a wrong bearer: %s | no bearer: %s | the transcripts and /ms bearers: NOT RUN here (other "
          "prefixes' secrets; site Z ran that arm)" % (wrong, none))
    if not (wrong == "401 unauthorized" and none == "401 unauthorized"):
        failed.append("4")

    print("LISTING-CHECKS-OK n=4" if not failed else "LISTING-CHECKS-FAIL " + ",".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
