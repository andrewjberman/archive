"""AMGT_RESAPP round 78 -- AMGT-bb-12: the planted FWD-14 lapse (CTO round-77 ruling 6).

  --crit AC1 --where local [--write <folder>]     the plant and its control, through the route's own function
  --crit AC2 --where local                        the committed record of the plant
  --crit ORGANIC --where deployed                 the organic arm: what the deployed page says about the real list

THE PLANT IS A PLANT AND SAYS SO. Both packaged list files (lib/research/lists/data/publishers.json and
social_accounts.json) are COPIED, byte for byte, into a temporary folder. In the COPY of the social account list the
review date is set to PLANT_REVIEWED_AT, which puts its due date in the past. The packaged files are never opened for
writing; their SHA-256 is taken before and after and must not move.

THE FUNCTION IS THE ROUTE'S OWN. `lib.research.api.scoped_amgt.read_list_register()` finds the list files in the `data`
folder beside `lib.research.lists.rot`'s module file and takes no path. For the length of one call, in this process
only, this script points that module's `__file__` at the temporary folder and calls the handler with
GET /api/scoped/amgt/freshness?view=page -- the same handler, the same `owner_line.lists_statement(read_list_register())`
the deployed route runs. It is put back in a `finally`. No file under lib/ is edited and nothing is deployed, so the
DEPLOYED page never shows the plant: this proves what the page says when a list lapses, not that one has lapsed.

AC1 (PASSES at the base: the outcome is provable today with no build):
    C1 planted: the page's lists statement says "The social account list is out of date: its review fell due on
       <the planted due date>." and marks that list out of date;
    C2 it names the owner: the owner line reads "<owner> owns the publisher list and the social account list." with the
       owner the list file itself names, and the planted list's owner is that same name;
    C3 the difference arm inside the plant: the publisher list, whose copy was not changed, still reads in date;
    C4 the control: on an unchanged copy the social account list reads what the packaged file implies today (in date
       until its real due moment passes), so the sentence in C1 comes from the planted date and nothing else;
    C5 the packaged files' SHA-256 are the same before and after, and the register read names the temporary folder.
    With --write <folder> the record is written there as PLANTED_LAPSE.json.
AC2 (FAILS at the base, where no worker has committed a record): exactly one PLANTED_LAPSE.json sits under a worker's
    deliverables folder; it says planted true, carries the out-of-date sentence and the owner's name, and its control
    reads the list in date or names the real due moment as passed.
ORGANIC (not a worker criterion; the issuer's read on or after the real due moment): exit 0 only when the DEPLOYED page
    says the social account list is out of date. The script prints the exact UTC moment the list falls due.
Verdict: R78 BB12 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import datetime
import glob
import hashlib
import json
import os
import shutil
import sys
import tempfile

LIST_FILES = ("publishers.json", "social_accounts.json")
PLANT_REVIEWED_AT = "2026-08-01T00:00Z"
RECORD_GLOB = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~*/PLANTED_LAPSE.json"
FN = "opal-amgt-scoped-api"
PATH = "/api/scoped/amgt/freshness"


def _event():
    return {"rawPath": PATH, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"},
            "queryStringParameters": {"view": "page"}}


def _sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _when(text):
    for fmt in ("%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.datetime.strptime(text, fmt).replace(tzinfo=datetime.timezone.utc)
        except ValueError:
            continue
    raise ValueError("unreadable review date %r" % text)


def _due(document):
    return _when(document["reviewed_at"]) + datetime.timedelta(days=document["review_interval_days"])


def served_lists(folder):
    """The page view's `lists` block and the register's read record, with the list files taken from `folder`/data."""
    from lib.research.api import scoped_amgt
    from lib.research.lists import rot as rot_module

    real = rot_module.__file__
    rot_module.__file__ = os.path.join(folder, "rot.py")
    try:
        register = scoped_amgt.read_list_register()
        response = scoped_amgt.handler(_event())
    finally:
        rot_module.__file__ = real
    body = json.loads(response.get("body") or "{}")
    read_paths = sorted(str((register.get("reads") or {}).get(n, {}).get("object_key")) for n in (register.get("reads") or {}))
    return response.get("statusCode"), body.get("lists") or {}, read_paths


def _part(lists, name):
    return next((p for p in lists.get("lists") or [] if p.get("name") == name), {})


def run_plant():
    from lib.research.lists import rot as rot_module

    data_dir = os.path.join(os.path.dirname(os.path.abspath(rot_module.__file__)), "data")
    packaged = {n: os.path.join(data_dir, n) for n in LIST_FILES}
    before = {n: _sha(p) for n, p in packaged.items()}
    with open(packaged["social_accounts.json"], encoding="utf-8") as fh:
        real_social = json.load(fh)
    out = {"planted_stated": True, "plant": {"file": "a COPY of social_accounts.json", "field": "reviewed_at",
                                            "packaged_value": real_social.get("reviewed_at"),
                                            "planted_value": PLANT_REVIEWED_AT},
           "packaged_sha256_before": before, "owner_in_the_list_file": real_social.get("owner"),
           "real_due_utc": _due(real_social).strftime("%Y-%m-%dT%H:%MZ"),
           "read_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    for arm in ("control", "planted"):
        folder = tempfile.mkdtemp(prefix="r78_bb12_%s_" % arm)
        try:
            os.makedirs(os.path.join(folder, "data"))
            for n, p in packaged.items():
                shutil.copyfile(p, os.path.join(folder, "data", n))
            if arm == "planted":
                copy = os.path.join(folder, "data", "social_accounts.json")
                with open(copy, encoding="utf-8") as fh:
                    document = json.load(fh)
                document["reviewed_at"] = PLANT_REVIEWED_AT
                out["planted_due"] = _due(document).strftime("%Y-%m-%d")
                with open(copy, "w", encoding="utf-8", newline="\n") as fh:
                    json.dump(document, fh)
            code, lists, read_paths = served_lists(folder)
            out["planted_arm" if arm == "planted" else arm] = {"status_code": code, "lists": lists,
                        "read_from_the_temporary_folder": bool(read_paths) and all(
                            os.path.normcase(os.path.abspath(p)).startswith(os.path.normcase(os.path.abspath(folder)))
                            for p in read_paths)}
        finally:
            shutil.rmtree(folder, ignore_errors=True)
    out["packaged_sha256_after"] = {n: _sha(p) for n, p in packaged.items()}
    return out


def grade(out, clause):
    planted, control = out.get("planted_arm") or {}, out.get("control") or {}
    lists_p, lists_c = planted.get("lists") or {}, control.get("lists") or {}
    owner = out.get("owner_in_the_list_file")
    sentence = "The social account list is out of date: its review fell due on %s." % out.get("planted_due")
    print("   planted: owner line %r" % lists_p.get("owner_line"))
    print("   planted: %r" % lists_p.get("out_of_date"))
    print("   control: %r" % lists_c.get("out_of_date"))
    clause("C1 planted: the page says the social account list is out of date, with its due date",
           planted.get("status_code") == 200 and sentence in str(lists_p.get("out_of_date"))
           and _part(lists_p, "social account list").get("out_of_date") is True, sentence)
    clause("C2 it names the owner", bool(owner) and lists_p.get("owner_line")
           == "%s owns the publisher list and the social account list." % owner
           and _part(lists_p, "social account list").get("owner") == owner, "owner %r" % owner)
    clause("C3 the unchanged publisher list still reads in date beside it",
           _part(lists_p, "publisher list").get("out_of_date") is False
           and "The publisher list is in date" in str(lists_p.get("out_of_date")))
    real_due = _when(out["real_due_utc"])
    read_at = _when(out["read_at_utc"])
    expect_lapsed = real_due < read_at
    clause("C4 the control: the unchanged copy reads what the packaged file implies today",
           _part(lists_c, "social account list").get("out_of_date") is expect_lapsed
           and (expect_lapsed or "The social account list is in date" in str(lists_c.get("out_of_date"))),
           "real due %s; read at %s; expected out of date %s" % (out["real_due_utc"], out["read_at_utc"], expect_lapsed))
    clause("C5 the packaged files did not move and the copies were the files read",
           out.get("packaged_sha256_before") == out.get("packaged_sha256_after")
           and planted.get("read_from_the_temporary_folder") is True
           and control.get("read_from_the_temporary_folder") is True,
           "sha256 social %s" % str((out.get("packaged_sha256_after") or {}).get("social_accounts.json"))[:16])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "ORGANIC"), required=True)
    ap.add_argument("--where", choices=("local", "deployed"), default="local")
    ap.add_argument("--write", default=None, help="folder to write PLANTED_LAPSE.json to (AC1 only)")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print("%s %s %s" % ("PASS" if cond else "FAIL", name, detail))

    if a.crit == "ORGANIC":
        import boto3

        lam = boto3.client("lambda", region_name="us-east-1")
        raw = json.loads(lam.invoke(FunctionName=FN, Payload=json.dumps(_event()).encode())["Payload"].read())
        lists = json.loads(raw.get("body") or "{}").get("lists") or {}
        part = _part(lists, "social account list")
        print("   deployed owner line: %r" % lists.get("owner_line"))
        print("   deployed: %r" % lists.get("out_of_date"))
        from lib.research.lists import rot as rot_module

        with open(os.path.join(os.path.dirname(os.path.abspath(rot_module.__file__)), "data", "social_accounts.json"),
                  encoding="utf-8") as fh:
            due = _due(json.load(fh))
        print("   the packaged social account list falls due at %s; now %s" % (
            due.strftime("%Y-%m-%dT%H:%MZ"), datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")))
        clause("C1 the deployed page says the social account list is out of date and names its owner",
               part.get("out_of_date") is True and bool(part.get("owner")) and str(part.get("owner")) in str(
                   lists.get("owner_line")), "out_of_date %r owner %r" % (part.get("out_of_date"), part.get("owner")))
        return verdict(a, ok)

    if a.crit == "AC2":
        found = sorted(glob.glob(RECORD_GLOB))
        clause("C0 exactly one committed record", len(found) == 1, "%d found %s" % (len(found), found))
        if len(found) != 1:
            return verdict(a, ok)
        with open(found[0], encoding="utf-8") as fh:
            out = json.load(fh)
        clause("C0b the record says it is a plant", out.get("planted_stated") is True)
    else:
        out = run_plant()
    grade(out, clause)
    if a.crit == "AC1" and a.write:
        os.makedirs(a.write, exist_ok=True)
        with open(os.path.join(a.write, "PLANTED_LAPSE.json"), "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print("   wrote PLANTED_LAPSE.json to %s" % a.write)
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print("R78 BB12 %s SERVED: %s" % (a.crit, "YES" if yes else "NO"))
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
