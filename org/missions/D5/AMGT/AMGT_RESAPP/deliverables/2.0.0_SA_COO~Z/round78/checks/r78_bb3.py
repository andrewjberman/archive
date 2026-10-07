"""AMGT_RESAPP round 78 -- AMGT-bb-3: the officer rank (round-77 analysis ruling 9).

  --crit AC1|AC2|AC3 --where local

The cell builds `lib.research.management.officer_rank` with two pure functions:
  title_rank(title)                          -> 0 (the company's chief executive), 1 (its chief financial officer), 2 (anyone else)
  rank_officers(officers, title_field="role") -> a NEW list: rank 0 rows, then rank 1 rows, then the rest, each group in
                                                the order it was given; the input list and its rows are not changed.

AC1 (build, pure): C1 every title in the labelled table below reads its rank (the titles are real ones, read from the
    stored Bloomberg officer lists and from the served filing rosters on 2026-10-07); C2 a roster given in the filing
    order Boeing's is served in comes back chief executive first, chief financial officer second, the rest in order;
    C3 the function is stable and safe: an empty list, a row with no title, a second pass changes nothing, the input
    list is not reordered, and `title_field="title"` reads the other field name.
AC2 (build, the seam against the real stored lists; reads only): every stored Bloomberg officer list is ranked; each
    result holds the same rows, never puts a lower rank ahead of a higher one and keeps the given order inside a rank
    (N of N printed, with how many lists changed order); NKE US opens with its President/CEO then its CFO.
AC3 (build): the plant tests in lib/research/management/tests/test_officer_rank.py pass.
Verdict: R78 BB3 <CRIT> SERVED: YES|NO (exit 0|1).
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

BUCKET = "opal-data-harvest"
PREFIX = "bloomberg/harvest/bronze/exec_officers/"
TEST = "lib/research/management/tests/test_officer_rank.py"

LABELLED = (
    # the company's chief executive
    (0, "Chief Executive Officer"), (0, "CEO"), (0, "President/CEO"), (0, "Chairman/CEO"), (0, "Chair/President/CEO"),
    (0, "President/CEO/Executive Director"), (0, "President/CEO:Group"),
    (0, "President/CEO:Group/Rep Exec Officer/Exec Officer"), (0, "Group CEO/Executive Director"),
    (0, "Co-Chief Executive Officer"), (0, "President/Co-CEO"), (0, "Co-Chairman/Co-President/Co-CEO"),
    (0, "Rotating Chief Executive Officer"), (0, "Interim CEO & Mng Dir"), (0, "Managing Director/CEO"),
    (0, "Vice Chairman/CEO"), (0, "CEO/General Manager"), (0, "Chairman-Mgmt Board/CEO"),
    (0, "President and Chief Executive Officer"), (0, "Director and Chief Executive Officer"),
    (0, "President and Chief Executive Officer, and a member of the Board"),
    (0, "Chair, and as our President and Chief Executive Officer"),
    (0, "Chairman of the Board, President and Chief Executive Officer"),
    (0, "Chairman of the Board, Chief Executive Officer and President"),
    (0, "Founder, Chairman and Chief Executive Officer"),
    # the company's chief financial officer
    (1, "Chief Financial Officer"), (1, "Exec VP/CFO"), (1, "CFO/Executive Director"), (1, "Exec VP/CFO/Treasurer"),
    (1, "Senior VP/CFO"), (1, "Exec VP/CFO/Interim Controller"), (1, "Senior VP/Interim CFO"),
    (1, "Group Chief Financial Officer"), (1, "Chief Financial and Strategy Officer"), (1, "Sr VP:Finance/CFO"),
    (1, "Senior Managing Corporate Executive Offi/CFO:Group"), (1, "CFO/Chairman:Iberdrola Espana"),
    (1, "Executive Vice President and Chief Financial Officer"),
    (1, "Senior Vice President and Chief Financial Officer"),
    # anyone else: a unit's or region's chief, a deputy, an adviser, any other title
    (2, "Chairman"), (2, "President"), (2, "Exec VP/COO"), (2, "CEO:North America"), (2, "CEO:Asia Pacific"),
    (2, "Exec VP/CEO:Europe"), (2, "Co-CEO:Corporate & Institutional Banking"), (2, "President & CEO:Japan"),
    (2, "Chairman & CEO:BNP Paribas Fortis"), (2, "CEO & Mng Dir:Hindustan Unilever Ltd"),
    (2, "Pres:Global Health/CEO:ViiV Healthcare"), (2, "Sr Mng Exec Ofcr/CEO:Energy Sector/CEO:Power Grids"),
    (2, "Regional Chief Executive"), (2, "Chief Strategy Officer/Regional Chief Executive"),
    (2, "Deputy CEO/Executive Director"), (2, "Co-Deputy COO/CEO:CIB"),
    (2, "Head:Chief Executive Office Strategy & Sustainabil"), (2, "Special Advisor to the CEO"),
    (2, "Brazil Chief Executive Officer"), (2, "Chief Growth Officer and US CEO"),
    (2, "Chief Executive Officer, Alibaba E-commerce Business Group"),
    (2, "Executive Vice President; President and Chief Executive Officer of Boeing Defense, Space & Security"),
    (2, "Executive Vice President; President and Chief Executive Officer, Boeing Commercial Airplanes"),
    (2, "Executive Vice President, President and Chief Executive Officer, Boeing Global Services"),
    (2, "CFO:EMEA"), (2, "CFO:Optum Insight"), (2, "Deputy CFO"), (2, "Deputy CFO/Chief Accounting Officer"),
    (2, "Managing Exec Officer/Dpty CFO:Group/Dpty CSO:Grou"), (2, "Executive Vice President and Chief Human Resources Officer"),
)

BOEING = (
    "Executive Vice President and Chief Human Resources Officer",
    "Chief Legal Officer and Executive Vice President, Global Compliance",
    "Executive Vice President and Chief Financial Officer",
    "Senior Vice President; President, Boeing Global",
    "President and Chief Executive Officer, and a member of the Board",
    "Executive Vice President; President and Chief Executive Officer of Boeing Defense, Space & Security",
    "Executive Vice President; President and Chief Executive Officer, Boeing Commercial Airplanes",
)


def _rows(titles, field="role"):
    return [{"name": "Person %d" % i, field: t} for i, t in enumerate(titles)]


def _stored_lists():
    import boto3

    s3 = boto3.client("s3", region_name="us-east-1")
    newest = {}
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for obj in page.get("Contents", []) or []:
            parts = obj["Key"][len(PREFIX):].split("/")
            if len(parts) == 2 and parts[1].endswith(".json"):
                newest[parts[0]] = max(newest.get(parts[0], ""), obj["Key"])
    lists = {}
    for folder, key in sorted(newest.items()):
        response = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8")).get("response") or {}
        officers = []
        for entry in response.get("COMPANY_EXEC_OFFICERS") or []:
            text = entry.get("Executive Officers") if isinstance(entry, dict) else entry
            if not isinstance(text, str) or not text.strip():
                continue
            name, _sep, title = text.partition(",  ")
            officers.append({"name": name.strip(), "role": title.strip() or None})
        lists[folder[len("security_key="):]] = officers
    return lists


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        if not os.path.isfile(TEST):
            clause("C1 the plant test file exists", False, TEST)
            return verdict(a, ok)
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", TEST], capture_output=True,
                           timeout=100)
        tail = (p.stdout + p.stderr).decode("utf-8", errors="replace").strip().split("\n")[-1]
        print("   " + tail)
        clause("C1 every plant case passes", p.returncode == 0 and " passed" in tail and "failed" not in tail,
               f"rc={p.returncode}")
        return verdict(a, ok)

    try:
        from lib.research.management import officer_rank
    except ImportError as err:
        clause("C0 lib.research.management.officer_rank imports", False, str(err))
        return verdict(a, ok)
    title_rank = getattr(officer_rank, "title_rank", None)
    rank_officers = getattr(officer_rank, "rank_officers", None)
    if not callable(title_rank) or not callable(rank_officers):
        clause("C0 officer_rank.title_rank and rank_officers exist", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        wrong = [(want, title, title_rank(title)) for want, title in LABELLED if title_rank(title) != want]
        for want, title, got in wrong[:8]:
            print("   want %d got %r: %s" % (want, got, title))
        clause("C1 every labelled title reads its rank", not wrong, "%d of %d" % (len(LABELLED) - len(wrong), len(LABELLED)))
        given = _rows(BOEING)
        ranked = rank_officers(given)
        roles = [r.get("role") for r in ranked]
        rest = [t for t in BOEING if t not in (BOEING[4], BOEING[2])]
        clause("C2 a filing-order roster comes back chief executive, chief financial officer, then as given",
               roles == [BOEING[4], BOEING[2]] + rest, "opens %r" % (roles[:2],))
        again = rank_officers(ranked)
        with_gap = rank_officers([{"name": "A", "role": None}, {"name": "B"}, {"name": "C", "role": "CEO"}])
        other = rank_officers(_rows(("Chairman", "Exec VP/CFO", "President/CEO"), field="title"), title_field="title")
        clause("C3 stable and safe",
               rank_officers([]) == [] and again == ranked and [r.get("role") for r in given] == list(BOEING)
               and [r.get("name") for r in with_gap] == ["C", "A", "B"] and title_rank(None) == 2 and title_rank("") == 2
               and [r.get("title") for r in other] == ["President/CEO", "Exec VP/CFO", "Chairman"],
               "no-title roster %r" % ([r.get("name") for r in with_gap],))
        return verdict(a, ok)

    lists = _stored_lists()
    good, changed, bad = 0, 0, []
    for name, officers in sorted(lists.items()):
        ranked = rank_officers(officers)
        ranks = [title_rank(r.get("role")) for r in ranked]
        same_rows = sorted(id(r) for r in ranked) == sorted(id(r) for r in officers)
        ordered = ranks == sorted(ranks)
        kept = all([r for r in ranked if title_rank(r.get("role")) == k] == [r for r in officers if title_rank(r.get("role")) == k]
                   for k in (0, 1, 2))
        if same_rows and ordered and kept:
            good += 1
        else:
            bad.append(name)
        changed += [id(r) for r in ranked] != [id(r) for r in officers]
    with_chief = sum(1 for o in lists.values() if any(title_rank(r.get("role")) == 0 for r in o))
    print("   stored lists %d; with a chief executive row %d; lists whose order the rank changes %d; e.g. wrong %s"
          % (len(lists), with_chief, changed, bad[:4]))
    clause("C1 every stored list is ranked without losing or misordering a row", bool(lists) and good == len(lists),
           "%d of %d" % (good, len(lists)))
    nke = [r.get("role") or "" for r in rank_officers(lists.get("NKE_US_Equity") or [])]
    clause("C2 NKE US opens with its President/CEO then its CFO",
           len(nke) >= 2 and nke[0] == "President/CEO" and "CFO" in nke[1], "opens %r" % (nke[:2],))
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB3 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
