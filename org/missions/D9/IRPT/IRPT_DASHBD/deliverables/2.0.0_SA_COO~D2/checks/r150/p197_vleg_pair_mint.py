"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- the V leg of the 49 Financial filled-report pass, steps (2) and (3) (CTO msg 10509): two synthetic principals in `opal-users-v2`, minted by `0.7.0_AE_CloudOps~IB2`
so `2.0.0_SA_COO~S2` can grade the live route and one export on the canary: COVERING (one OPAL_GLOBAL internal-staff viewer, whose scope covers 49 Financial by role) and NON-COVERING (one Cottonwood viewer with a non-empty
scope over Cottonwood accounts that excludes every 49 Financial account). No user-to-advisor link is hand-typed and no ownership map or partner table is edited. Both rows are REMOVED after the issuer's word and read back ABSENT twice.
WORLD (two users rows written and removed). The record is the applier's; the checker re-reads the table.

  DBC197-1-AC1  the record: both principals' classes and digests (never the addresses), the read-backs, the hand-over of both sessions by broker to S2, the removal after the issuer's word, two ABSENT reads each, no address
  DBC197-2-AC1  FRESH live reads: both rows are absent (a consistent get and the email index each), so nothing was left behind

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_197")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/VLEG_PAIR_MINT_RECORD.json"
EMAILS = {"COVERING": "v328-cover-r150@opal.invalid", "NON_COVERING": "v328-ctrl-r150@opal.invalid"}
DIGESTS = {k: hashlib.sha256(v.encode("utf-8")).hexdigest()[:12] for k, v in EMAILS.items()}
CLASSES = {"COVERING": "OPAL_GLOBAL", "NON_COVERING": "COTTONWOOD_SCOPED"}
TABLE, INDEX, REGION = "opal-users-v2", "email-index", "us-east-1"
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("email_digest12", "handed_utc", "removed_utc", "minted_utc")
ABSENT2 = [{"gsi": "ABSENT", "consistent": "ABSENT"}, {"gsi": "ABSENT", "consistent": "ABSENT"}]


def check_record(rec):
    exp = {"claim", "applier", "ledger_entry", "principals", "mint", "handed", "removal", "notes", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured" and rec["applier"] == APPLIER and nes(rec["ledger_entry"]), "claim measured, the applier named, a ledger entry")
    ps = rec["principals"]
    need(isinstance(ps, list) and len(ps) == 2 and [p.get("role") for p in ps if isinstance(p, dict)] == ["COVERING", "NON_COVERING"], "principals: exactly two, COVERING then NON_COVERING")
    for p in ps:
        role = p["role"]
        need(set(p) == {"role", "email_digest12", "user_type", "firm", "class", "scope_nonempty", "covers_49f"} and p["email_digest12"] == DIGESTS[role] and nes(p["user_type"]) and nes(p["firm"]) and p["class"] == CLASSES[role],
             "%s principal: the digest of its fixed address (%s), the user type and firm as words, class %s" % (role, DIGESTS[role], CLASSES[role]))
    cov, non = ps
    need(cov["scope_nonempty"] is True and cov["covers_49f"] is True, "COVERING: a non-empty scope that covers 49 Financial")
    need(non["scope_nonempty"] is True and non["covers_49f"] is False, "NON_COVERING: a non-empty scope (Cottonwood) that covers NO 49 Financial account")
    m = rec["mint"]
    need(isinstance(m, dict) and set(m) == {"minted_utc", "readback_ok", "index_counts_after_mint"} and H.UTC.match(str(m["minted_utc"])) and m["readback_ok"] is True and m["index_counts_after_mint"] == [1, 1],
         "mint: a UTC time, both read-backs OK, the email index reading 1 for each after the mint")
    h = rec["handed"]
    need(isinstance(h, dict) and set(h) == {"to", "via", "handed_utc", "sessions"} and h["to"] == "2.0.0_SA_COO~S2" and h["via"] == "broker" and h["sessions"] == 2 and H.UTC.match(str(h["handed_utc"])),
         "handed: two sessions to 2.0.0_SA_COO~S2, by broker (never a file), at a UTC time")
    r = rec["removal"]
    need(isinstance(r, dict) and set(r) == {"after_issuer_word", "removed_utc", "absent_reads"} and r["after_issuer_word"] is True and H.UTC.match(str(r["removed_utc"])), "removal: after the issuer's word, at a UTC time")
    ar = r["absent_reads"]
    need(isinstance(ar, dict) and set(ar) == {"COVERING", "NON_COVERING"} and all(ar[k] == ABSENT2 for k in ar), "removal.absent_reads: two reads for EACH principal, each ABSENT on the index and on a consistent get")
    need(m["minted_utc"] <= h["handed_utc"] <= r["removed_utc"], "order in time: minted, handed over, then removed")
    need(isinstance(rec["notes"], str) and 20 <= len(rec["notes"]) <= 2400 and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "notes (words) and the reads block")
    need("within-firm advisor split" in rec["notes"] and "not exercised" in rec["notes"], "notes say the within-firm advisor split is not exercised and is owed once a 49 Financial advisor map exists (CTO msg 10509)")
    need(all("opal.invalid" not in rec["notes"] and e not in rec["notes"] for e in EMAILS.values()), "no address may be written in the record")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    check_record(rec)
    need(not H.digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(rec)[:2])
    if cid == "DBC197-1-AC1":
        print("OK: both principals' classes and digests, the read-backs, the two sessions handed to S2 by broker, the removal after the issuer's word, two ABSENT reads each, no address")
        return True
    if cid == "DBC197-2-AC1":
        import boto3
        ddb = boto3.client("dynamodb", region_name=REGION)
        for role, email in EMAILS.items():
            got = ddb.get_item(TableName=TABLE, Key={"PK": {"S": "USER#" + email}, "SK": {"S": "PROFILE"}}, ConsistentRead=True)
            need("Item" not in got, "the %s users row is still PRESENT on a consistent get" % role)
            q = ddb.query(TableName=TABLE, IndexName=INDEX, KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": email}}, Select="COUNT")
            need(q["Count"] == 0, "the %s email index still reads %d" % (role, q["Count"]))
        print("OK: live: both synthetic rows are ABSENT on a consistent get and on the email index")
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    return {"claim": "measured", "applier": APPLIER, "ledger_entry": "irpt-dashbd-vleg-pair-20261017",
            "principals": [
                {"role": "COVERING", "email_digest12": DIGESTS["COVERING"], "user_type": "dev", "firm": "opal-capital", "class": "OPAL_GLOBAL", "scope_nonempty": True, "covers_49f": True},
                {"role": "NON_COVERING", "email_digest12": DIGESTS["NON_COVERING"], "user_type": "test-filer", "firm": "cottonwood", "class": "COTTONWOOD_SCOPED", "scope_nonempty": True, "covers_49f": False}],
            "mint": {"minted_utc": "2026-10-17T12:20:00Z", "readback_ok": True, "index_counts_after_mint": [1, 1]},
            "handed": {"to": "2.0.0_SA_COO~S2", "via": "broker", "handed_utc": "2026-10-17T12:24:00Z", "sessions": 2},
            "removal": {"after_issuer_word": True, "removed_utc": "2026-10-17T12:50:00Z", "absent_reads": {"COVERING": copy.deepcopy(ABSENT2), "NON_COVERING": copy.deepcopy(ABSENT2)}},
            "notes": "Two synthetic principals, minted, handed over by broker, removed after the issuer's word and read back ABSENT twice; the within-firm advisor split is not exercised and is owed once a 49 Financial advisor map exists.",
            "reads": {"vendor_calls": 0, "secret_reads": 0}}


def selftest():
    rec = synthetic()
    check_record(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "applier": lambda r: r.update(applier="x"),
        "one principal": lambda r: r["principals"].pop(),
        "role order": lambda r: r["principals"].reverse(),
        "cover digest": lambda r: r["principals"][0].update(email_digest12="0" * 12),
        "ctrl digest": lambda r: r["principals"][1].update(email_digest12="0" * 12),
        "cover class": lambda r: r["principals"][0].update(**{"class": "FIRM_ADVISOR"}),
        "ctrl class": lambda r: r["principals"][1].update(**{"class": "OPAL_GLOBAL"}),
        "cover scope empty": lambda r: r["principals"][0].update(scope_nonempty=False),
        "cover not covering": lambda r: r["principals"][0].update(covers_49f=False),
        "ctrl scope empty": lambda r: r["principals"][1].update(scope_nonempty=False),
        "ctrl covers 49f": lambda r: r["principals"][1].update(covers_49f=True),
        "readback": lambda r: r["mint"].update(readback_ok=False),
        "index after mint": lambda r: r["mint"].update(index_counts_after_mint=[1, 0]),
        "handed to": lambda r: r["handed"].update(to="2.0.0_SA_COO~D2"),
        "handed via": lambda r: r["handed"].update(via="file"),
        "one session": lambda r: r["handed"].update(sessions=1),
        "removal word": lambda r: r["removal"].update(after_issuer_word=False),
        "one absent read": lambda r: r["removal"]["absent_reads"]["COVERING"].pop(),
        "present read": lambda r: r["removal"]["absent_reads"]["NON_COVERING"][1].update(consistent="PRESENT"),
        "gsi present": lambda r: r["removal"]["absent_reads"]["COVERING"][0].update(gsi="PRESENT"),
        "no reads for one": lambda r: r["removal"]["absent_reads"].pop("NON_COVERING"),
        "time order": lambda r: r["removal"].update(removed_utc="2026-10-17T12:10:00Z"),
        "advisor note": lambda r: r.update(notes="Two synthetic principals, minted, handed over by broker, removed and read back ABSENT twice."),
        "address in notes": lambda r: r.update(notes=r["notes"] + " " + EMAILS["COVERING"]),
        "reads": lambda r: r.update(reads={"vendor_calls": 0, "secret_reads": 1}),
        "extra key": lambda r: r.update(z=1),
    }
    n = 0
    for label, mut in arms.items():
        r = copy.deepcopy(rec)
        try:
            mut(r)
            check_record(r)
        except Fail:
            n += 1
            continue
        raise AssertionError("mutant passed: " + label)
    print("selftest: green on the synthetic record and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
