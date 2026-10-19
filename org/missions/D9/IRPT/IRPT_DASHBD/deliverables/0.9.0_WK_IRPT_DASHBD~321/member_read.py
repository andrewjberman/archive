"""IRPT_DASHBD round 133, cell DB-i-21 (worker 0.9.0_WK_IRPT_DASHBD~321) -- the S60 membership read, by hashed id.

Reads the latest date partition of the landed Scope account-return silver (one LIST and one GET, through the GET-only
InflectionSilverReader), and the round-119 active-roster response held as a private local file (read only; it is the file the
round-119 record hashed). Each account is keyed by the SAME id-to-string rule as account_record_read.py (key_of), hashed with
sha256 before anything is written. Writes a PRIVATE extract (hashed ids, a null-start flag and a class word per feed account)
and the repo record. No write call, no vendor call, no credential read; ids are never printed.

Usage: python -I <this file>
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
ADAPTERS = ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"
PRIV = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~321")
R119 = ROOT / "org" / "missions" / "D9" / "IRPT" / "IRPT_DASHBD" / "deliverables" / "0.9.0_WK_IRPT_DASHBD~307" / "ACCOUNT_RECORD_READ_R119.json"
ROSTER = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~307/get1_newportfolio_active.json")
EXTRACT = PRIV / "membership_extract.json"
REC = HERE / "S60_MEMBERSHIP_R133.json"
SCRIPT_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~321/member_read.py"
NSD = "NO_START_DATE_AT_SOURCE"

sys.path.insert(0, str(ADAPTERS))
import inflection_account_dim as iad  # noqa: E402  (the GET-only silver reader)
import inflection_account_return_daily as iar  # noqa: E402  (ORION_SILVER, the granted silver prefix)


def key_of(raw):
    """The id-to-string rule of account_record_read.py, unchanged: integral numbers as digits, text stripped, blank is None."""
    if raw is None:
        return None
    if isinstance(raw, float):
        if raw != raw:
            return None
        if raw.is_integer():
            return str(int(raw))
    if isinstance(raw, int):
        return str(raw)
    text = str(raw).strip()
    return text or None


def dig(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rows_of(body):
    """The roster rows: the first list the body holds, as account_record_read.py reads them."""
    if isinstance(body, dict):
        return next((v for v in body.values() if isinstance(v, list)), [])
    return body if isinstance(body, list) else []


def refuse(msg):
    print("REFUSED: %s" % msg)
    sys.exit(2)


def main():
    r119 = json.loads(R119.read_bytes().decode("utf-8"))
    g1 = [g for g in r119["gets"] if g["kind"] == "newportfolio_active"]
    if len(g1) != 1:
        refuse("round-119 record holds no single newportfolio_active get")
    id_key = g1[0]["account_id_key"]
    s60 = r119["roles_sha256"]["missing_sha256"]

    roster_bytes = ROSTER.read_bytes()
    if hashlib.sha256(roster_bytes).hexdigest() != g1[0]["response_file"]["sha256"]:
        refuse("roster file is not the file the round-119 record hashed")
    rows = [r for r in rows_of(json.loads(roster_bytes.decode("utf-8"))) if isinstance(r, dict)]
    roster_ids, null_ids, nonnull_ids = set(), set(), set()
    for r in rows:
        i = key_of(r.get(id_key))
        if i is None:
            continue
        roster_ids.add(i)
        v = r.get("accountStartDate")
        if v is None or (isinstance(v, str) and not v.strip()):
            null_ids.add(i)
        else:
            nonnull_ids.add(i)

    reader = iad.InflectionSilverReader()
    table = iar.ORION_SILVER + "scope_account_returns"
    parts = reader.list_partitions(table)
    if not parts:
        refuse("no date partition under the scope account-return table")
    newest = parts[-1]
    frame = reader.read_parquet(table.rstrip("/") + "/" + newest + "/data.parquet")

    accounts, feed_null_id = {}, 0
    for acc, st, rc in zip(frame["account_id"].tolist(), frame["status"].tolist(), frame["reason_class"].tolist()):
        k = key_of(acc)
        if k is None:
            feed_null_id += 1
            continue
        h = dig(k)
        if h in accounts:
            refuse("a feed account repeats in the latest partition: no extract written")
        if st == "RETURNED":
            word = "RETURNED"
        elif st == "ABSENT":
            word = rc if isinstance(rc, str) and rc else "NO_REASON"
        else:
            word = "UNKNOWN_STATUS"
        accounts[h] = {"roster_null_start": k in null_ids, "feed_class": word}
    if feed_null_id:
        refuse("%d feed row(s) carry no account id: no extract written" % feed_null_id)
    feed_ids = {key_of(a) for a in frame["account_id"].tolist()}
    if not (feed_ids & roster_ids):
        refuse("the feed's account ids match no roster id under %s: no extract written" % id_key)

    extract = {"silver_partitions": len(parts), "accounts": accounts}
    EXTRACT.parent.mkdir(parents=True, exist_ok=True)
    EXTRACT.write_bytes((json.dumps(extract, sort_keys=True) + "\n").encode("utf-8"))
    ext_sha = hashlib.sha256(EXTRACT.read_bytes()).hexdigest()

    a = {h for h, v in accounts.items() if v["roster_null_start"]}
    b = {h for h, v in accounts.items() if v["feed_class"] == NSD}
    amb, bma = sorted(a - b), sorted(b - a)
    in_diff = s60 in set(amb) | set(bma)
    verdict = "NO_DIFFERENCE" if not amb and not bma else "DIFFERENCE_SHOWN"
    s60_null = bool(accounts.get(s60, {}).get("roster_null_start"))
    s60_class = accounts[s60]["feed_class"] if s60 in accounts else "NOT_IN_FEED"
    amb_classes = [accounts[h]["feed_class"] for h in amb]

    n_null_all = len(null_ids)
    n_null_outside = len(null_ids - feed_ids)
    basis = (
        "Silver: %d date partition(s) listed under the Scope account-return table; the latest partition holds %d feed accounts, "
        "one row each. Roster: the round-119 active-roster response (verified against the hash the round-119 record holds) carries "
        "%d rows and %d distinct ids, of which %d carry a null or empty start date; %d of those null-start ids are not in the latest "
        "partition and so fall outside this extract. Within the feed accounts: %d carry a null roster start date and %d carry the feed "
        "class %s. Difference A minus B (null start in the roster, not %s in the feed): %d account(s), feed class word(s): %s. "
        "Difference B minus A (%s in the feed, not null in the roster): %d account(s). Verdict %s. S60's account: %s the roster "
        "null-start set; feed class %s; %s either difference. This establishes the counts and class words of the latest partition "
        "against the roster file, over the feed accounts only. It does not establish the cause of any difference, the meaning of a "
        "null start date in the roster, or the state of any account outside the feed or in an earlier partition."
    ) % (
        len(parts), len(accounts), len(rows), len(roster_ids), n_null_all, n_null_outside,
        len(a), len(b), NSD, NSD, len(amb), (", ".join(amb_classes) or "none"),
        NSD, len(bma), verdict, "in" if s60_null else "not in", s60_class, "inside" if in_diff else "outside",
    )

    rec = {
        "script": {"file": SCRIPT_REL, "sha256": hashlib.sha256(Path(__file__).resolve().read_bytes()).hexdigest()},
        "extract": {"path": EXTRACT.as_posix(), "sha256": ext_sha},
        "silver_partitions": len(parts),
        "feed_accounts": len(accounts),
        "roster_null_start": len(a),
        "feed_no_start_date": len(b),
        "a_minus_b_sha256": amb,
        "a_minus_b_feed_class": amb_classes,
        "b_minus_a_sha256": bma,
        "s60_account_sha256": s60,
        "s60_in_roster_null_start": s60_null,
        "s60_feed_class": s60_class,
        "s60_in_difference": in_diff,
        "verdict": verdict,
        "reads": {"s3_reads": reader.reads, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
        "basis_words": basis,
    }
    REC.write_text(json.dumps(rec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("partitions=%d feed_accounts=%d roster_null_start_in_feed=%d feed_no_start_date=%d" % (
        len(parts), len(accounts), len(a), len(b)))
    print("roster_rows=%d roster_distinct_ids=%d roster_null_all=%d null_outside_feed=%d" % (
        len(rows), len(roster_ids), n_null_all, n_null_outside))
    print("difference_a_minus_b=%d difference_b_minus_a=%d verdict=%s" % (len(amb), len(bma), verdict))
    print("a_minus_b_feed_class=%s" % (",".join(amb_classes) or "none"))
    print("s60_in_roster_null_start=%s s60_feed_class=%s s60_in_difference=%s" % (s60_null, s60_class, in_diff))
    print("s3_reads=%d extract_sha256=%s" % (reader.reads, ext_sha))


if __name__ == "__main__":
    main()
