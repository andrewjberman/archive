"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- C5 of the Cottonwood Performance read path (CTO msg 10324): one synthetic Opal-staff (OPAL_GLOBAL) principal in `opal-users-v2` with the fixed address
`c5-staff-r150@opal.invalid`, minted by `0.7.0_AE_CloudOps~IB2` so the issuer can sign in on 127.0.0.1:5174 and look at Thiessen's two Cottonwood accounts on the Performance tab, then REMOVED and read back ABSENT twice.
WORLD (a users row written and removed). The record is the applier's; the checker re-reads the table.

  DBC193-1-AC1  the record: the principal's class and digest (never the address), the readback, the hand-over by broker to the issuer, the removal after the issuer's word, two ABSENT reads
  DBC193-2-AC1  FRESH live reads: the row is absent (a consistent get and the email index), so nothing was left behind

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


H = helper("r147/p151_pubapply.py", "p151_helper_193")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_C5_SIGNIN_RECORD.json"
EMAIL = "c5-staff-r150@opal.invalid"
DIGEST12 = hashlib.sha256(EMAIL.encode("utf-8")).hexdigest()[:12]
TABLE, INDEX, REGION = "opal-users-v2", "email-index", "us-east-1"
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("email_digest12", "handed_utc", "removed_utc", "minted_utc")


def check_record(rec):
    exp = {"claim", "applier", "ledger_entry", "principal", "mint", "handed", "removal", "notes", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured" and rec["applier"] == APPLIER and nes(rec["ledger_entry"]), "claim measured, the applier named, a ledger entry")
    p = rec["principal"]
    need(isinstance(p, dict) and set(p) == {"email_digest12", "user_type", "firm", "class"} and p["email_digest12"] == DIGEST12 and nes(p["user_type"]) and nes(p["firm"]) and p["class"] == "OPAL_GLOBAL",
         "principal: the digest of the fixed address (%s), the user type and firm as words, class OPAL_GLOBAL" % DIGEST12)
    m = rec["mint"]
    need(isinstance(m, dict) and set(m) == {"minted_utc", "readback_ok", "index_count_after_mint"} and H.UTC.match(str(m["minted_utc"])) and m["readback_ok"] is True and m["index_count_after_mint"] == 1,
         "mint: a UTC time, the read-back OK, the email index reading 1 after the mint")
    h = rec["handed"]
    need(isinstance(h, dict) and set(h) == {"to", "via", "handed_utc"} and h["to"] == "2.0.0_SA_COO~D2" and h["via"] == "broker" and H.UTC.match(str(h["handed_utc"])),
         "handed: to the issuer, by broker (never a file), at a UTC time")
    r = rec["removal"]
    need(isinstance(r, dict) and set(r) == {"after_issuer_word", "removed_utc", "absent_reads"} and r["after_issuer_word"] is True and H.UTC.match(str(r["removed_utc"])), "removal: after the issuer's word, at a UTC time")
    ar = r["absent_reads"]
    need(isinstance(ar, list) and len(ar) == 2 and all(isinstance(x, dict) and set(x) == {"gsi", "consistent"} and x["gsi"] == "ABSENT" and x["consistent"] == "ABSENT" for x in ar), "removal.absent_reads: two reads, each ABSENT on the index and on a consistent get")
    need(H.UTC.match(str(h["handed_utc"])) and h["handed_utc"] <= r["removed_utc"] and m["minted_utc"] <= h["handed_utc"], "order in time: minted, handed over, then removed")
    need(isinstance(rec["notes"], str) and 20 <= len(rec["notes"]) <= 1800 and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "notes (words) and the reads block")
    need("opal.invalid" not in rec["notes"] and EMAIL not in rec["notes"], "the address must not be written in the record")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    check_record(rec)
    need(not H.digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(rec)[:2])
    if cid == "DBC193-1-AC1":
        print("OK: the principal's class and digest, the read-back, the hand-over by broker, the removal after the issuer's word, two ABSENT reads, no address")
        return True
    if cid == "DBC193-2-AC1":
        import boto3
        ddb = boto3.client("dynamodb", region_name=REGION)
        got = ddb.get_item(TableName=TABLE, Key={"PK": {"S": "USER#" + EMAIL}, "SK": {"S": "PROFILE"}}, ConsistentRead=True)
        need("Item" not in got, "the users row is still PRESENT on a consistent get")
        q = ddb.query(TableName=TABLE, IndexName=INDEX, KeyConditionExpression="email = :e", ExpressionAttributeValues={":e": {"S": EMAIL}}, Select="COUNT")
        need(q["Count"] == 0, "the email index still reads %d" % q["Count"])
        print("OK: live: the synthetic staff row is ABSENT on a consistent get and on the email index")
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    return {"claim": "measured", "applier": APPLIER, "ledger_entry": "irpt-dashbd-cottonwood-c5-signin-20261017",
            "principal": {"email_digest12": DIGEST12, "user_type": "dev", "firm": "opal-capital", "class": "OPAL_GLOBAL"},
            "mint": {"minted_utc": "2026-10-17T06:20:00Z", "readback_ok": True, "index_count_after_mint": 1},
            "handed": {"to": "2.0.0_SA_COO~D2", "via": "broker", "handed_utc": "2026-10-17T06:22:00Z"},
            "removal": {"after_issuer_word": True, "removed_utc": "2026-10-17T06:40:00Z", "absent_reads": [{"gsi": "ABSENT", "consistent": "ABSENT"}, {"gsi": "ABSENT", "consistent": "ABSENT"}]},
            "notes": "One synthetic staff principal, minted, handed over by broker, removed after the issuer's word and read back ABSENT twice.", "reads": {"vendor_calls": 0, "secret_reads": 0}}


def selftest():
    rec = synthetic()
    check_record(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "applier": lambda r: r.update(applier="x"),
        "digest": lambda r: r["principal"].update(email_digest12="0" * 12),
        "class": lambda r: r["principal"].update(**{"class": "FIRM_ADVISOR"}),
        "readback": lambda r: r["mint"].update(readback_ok=False),
        "index after mint": lambda r: r["mint"].update(index_count_after_mint=0),
        "handed to": lambda r: r["handed"].update(to="2.0.0_SA_COO~S2"),
        "handed via": lambda r: r["handed"].update(via="file"),
        "removal word": lambda r: r["removal"].update(after_issuer_word=False),
        "one absent read": lambda r: r["removal"]["absent_reads"].pop(),
        "present read": lambda r: r["removal"]["absent_reads"][1].update(consistent="PRESENT"),
        "gsi present": lambda r: r["removal"]["absent_reads"][0].update(gsi="PRESENT"),
        "time order": lambda r: r["removal"].update(removed_utc="2026-10-17T06:10:00Z"),
        "address in notes": lambda r: r.update(notes="the address was " + EMAIL + " for a while"),
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
