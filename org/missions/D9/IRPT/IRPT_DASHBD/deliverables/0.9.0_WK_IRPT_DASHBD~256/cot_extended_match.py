"""Cottonwood extended match over the CRM extract (IRPT_DASHBD DB-b-325, round 150).

Worker 0.9.0_WK_IRPT_DASHBD~256. Method logic only; this file holds no client data.

Reads, in memory and never to disk: the CRM extract Files.zip (nested zips), the 939 published
keys, the Cottonwood directory, the dell1 match sheet and the 118-pair list. Writes one CSV row per
published key (sorted by key, header included): published_raw, confidence, method, household,
advisor_code, advisor_email, source.

Grant rule (CTO msg 10304): HIGH needs two certain links -- the advisor-to-household link (the CRM
household advisor equals the portfolio advisor of the account) and the account-to-key link (direct,
or through one of the deterministic pairs). MEDIUM only where a second independent source agrees.
LOW and UNMATCHED never grant. Nothing rides the unconfirmed ("yes") pairs.

Deterministic: sorted iteration, no clock, no random, no absolute path written to the output.
Usage: python -I cot_extended_match.py --zip Files.zip --raw raw.txt --dir dir.json
                 --sheet sheet.csv --pairs pairs.csv --out out.csv
"""
import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import defaultdict

ZIP_SHA_PREFIX = "c66bae52"
CRM_MEMBER = "CRM_CottonwoodCapitalAdvisors.zip"
PORTFOLIO_MEMBER = "Cottonwood Capital Advisors_Portfolio_Accounting_Performance_ClientDelivery.zip"
IMAGING_MEMBERS = ("HKE.zip", "HJH.zip", "4XF.zip")
COLS = ("published_raw", "confidence", "method", "household", "advisor_code", "advisor_email", "source")
RANK = {"HIGH": 3, "MEDIUM": 2, "LOW": 1, "UNMATCHED": 0}
SOURCE_OF = {"MD": "sheet-direct", "MP": "sheet-via-pair", "MX": "extended"}
GRANT_ORDER = ("MD", "MP", "MX")


def die(msg):
    sys.stderr.write("ERROR: " + msg + "\n")
    sys.exit(2)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def member(zf, fragment):
    names = [n for n in zf.namelist() if fragment in n and not n.endswith("/")]
    if len(names) != 1:
        die("expected one member containing %r, found %d" % (fragment, len(names)))
    return names[0]


def pipe_table(zf, fragment):
    raw = zf.read(member(zf, fragment)).decode("utf-8", errors="replace")
    rows = list(csv.reader(io.StringIO(raw), delimiter="|", quoting=csv.QUOTE_NONE))
    hdr = [h.strip() for h in rows[0]]
    good = [dict(zip(hdr, [v.strip() for v in r])) for r in rows[1:] if len(r) == len(hdr)]
    return good, len(rows) - 1 - len(good)


def read_csv_file(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--raw", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--pairs", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    zdigest = sha256_of(a.zip)
    if not zdigest.startswith(ZIP_SHA_PREFIX):
        die("zip sha256 does not begin %s" % ZIP_SHA_PREFIX)

    # published keys (939) and the directory (census only)
    keys = sorted(set(x.strip() for x in open(a.raw, encoding="utf-8").read().splitlines() if x.strip()))
    up2raw = {k.upper(): k for k in keys}
    directory = json.load(open(a.dir, encoding="utf-8"))
    dir_accounts = set()
    for e in directory["entries"]:
        for acc in e["ids"]["account_ids"]:
            dir_accounts.add(str(acc).strip().upper())

    # pairs and sheet
    pairs = []
    for r in read_csv_file(a.pairs):
        pairs.append({
            "old": r["commonwealth_account"].strip().upper(),
            "bd": r["black_diamond_account"].strip().upper(),
            "det": r["to_confirm"].strip().lower().startswith("no"),
            "dell_hh": r["crm_household"].strip(),
        })
    sheet = defaultdict(list)
    for r in read_csv_file(a.sheet):
        sheet[r["account"].strip().upper()].append({
            "conf": r["confidence"].strip().upper(),
            "adv": r["advisor"].strip(),
            "conflict": r["conflict"].strip(),
            "raw_hh": r["hhid"].strip(),
        })

    # CRM tables, read in memory from the nested zip
    outer = zipfile.ZipFile(a.zip)
    crm = zipfile.ZipFile(io.BytesIO(outer.read(CRM_MEMBER)))
    hh_rows, hh_bad = pipe_table(crm, "Crmhouseholds_CottonwoodCapitalAdvisors")
    contacts, ct_bad = pipe_table(crm, "Contacts_CottonwoodCapitalAdvisors")
    users, us_bad = pipe_table(crm, "Users_CottonwoodCapitalAdvisors")
    c360, c3_bad = pipe_table(crm, "C360households_CottonwoodCapitalAdvisors")
    HH = {r["HouseholdID"]: r for r in hh_rows}
    HHID_TO_HID = {r["HHID"]: r["HouseholdID"] for r in hh_rows}
    ADV_OF_HH = {hid: r["AdvisorID"] for hid, r in HH.items()}
    # the sheet household cell reads "<HouseholdID> / HHID <HHID>"; both ids must agree on one row
    sheet_hh_pairs = 0
    for lst in sheet.values():
        for s in lst:
            m = re.fullmatch(r"(\d{7}) / HHID (\d{7})", s["raw_hh"])
            s["hh"] = m.group(1) if m and HHID_TO_HID.get(m.group(2)) == m.group(1) else ""
            sheet_hh_pairs += 1 if s["hh"] else 0
    DELL_IN_HH = sum(1 for p in pairs if p["dell_hh"] in HH)
    CONTACT_HH = {r["ContactID"]: r["HouseholdID"] for r in contacts}
    USER_EMAIL = {r["UserID"]: r["EmailAddress"] for r in users}
    c360_agree = sum(1 for r in c360 if HHID_TO_HID.get(r["HHID"]) and ADV_OF_HH.get(HHID_TO_HID[r["HHID"]]) == r["AdvisorID"])

    # portfolio: the advisor(s) the portfolio carries for each account (positions and TWR files)
    pa = zipfile.ZipFile(io.BytesIO(outer.read(PORTFOLIO_MEMBER)))
    ADV_ACCT = defaultdict(set)
    for frag, col in (("Historical_Positions", "AccountNumber"), ("Historical_Performance_TWR", "Account_Number")):
        tab, _ = pipe_table(pa, frag)
        for r in tab:
            acc = r[col].upper()
            if acc:
                ADV_ACCT[acc].add(r["Advisor_ID"])

    # activity notes: exact account tokens for the pair accounts, filed under one household
    OLD = set(p["old"] for p in pairs)
    cites = defaultdict(lambda: defaultdict(int))
    act_rows = act_hit_rows = ambiguous_ids = unresolved_hits = 0
    with crm.open(member(crm, "Activities_CottonwoodCapitalAdvisors")) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8", errors="replace", newline="")
        rdr = csv.reader(text, delimiter="|", quoting=csv.QUOTE_NONE)
        hdr = [h.strip() for h in next(rdr)]
        i_rid, i_subj, i_desc = hdr.index("regardingid"), hdr.index("subject"), hdr.index("activitydescription")
        for row in rdr:
            if len(row) != len(hdr):
                continue
            act_rows += 1
            hits = set(re.split(r"[^A-Z0-9]+", (row[i_subj] + " " + row[i_desc]).upper())) & OLD
            if not hits:
                continue
            act_hit_rows += 1
            rid = row[i_rid].strip()
            in_hh, in_ct = rid in HH, rid in CONTACT_HH
            if in_hh and in_ct:
                ambiguous_ids += 1
                continue
            if in_hh:
                hid = rid
            elif in_ct and CONTACT_HH[rid] in HH:
                hid = CONTACT_HH[rid]
            else:
                unresolved_hits += 1
                continue
            for acc in hits:
                cites[acc][hid] += 1

    def certain_hh(acc):
        h = cites.get(acc, {})
        if len(h) == 1:
            (hid, n), = h.items()
            if n >= 2:
                return hid
        return None

    def notes_top(acc):
        h = cites.get(acc, {})
        if not h:
            return None
        ranked = sorted(h.items(), key=lambda kv: (-kv[1], kv[0]))
        if len(ranked) > 1 and ranked[0][1] == ranked[1][1]:
            return None
        return ranked[0][0]

    # imaging index census (listing files only; counts, never values)
    img_files = img_old = img_bd = 0
    for name in IMAGING_MEMBERS:
        inner = zipfile.ZipFile(outer.open(name))
        for info in sorted(inner.infolist(), key=lambda i: i.filename):
            if info.is_dir() or not info.filename.endswith("Listing.csv"):
                continue
            img_files += 1
            toks = set(re.split(r"[^A-Z0-9]+", inner.read(info).decode("utf-8", errors="replace").upper()))
            img_old += len(toks & OLD)
            img_bd += len(toks & set(up2raw))

    det_by_bd = defaultdict(list)
    for p in pairs:
        det_by_bd[p["bd"]].append(p)

    rows = []
    tally = defaultdict(int)
    methods_used = defaultdict(int)
    for k in keys:
        ku = k.upper()
        grants = []   # (method, household, advisor)
        cands = []    # (household or None, method, det flag, medium flag)
        for s in sheet.get(ku, []):
            if s["conf"] == "HIGH" and not s["conflict"] and s["hh"]:
                hid = s["hh"]
                if ADV_OF_HH.get(hid) == s["adv"]:
                    grants.append(("MD", hid, s["adv"]))
        for p in det_by_bd.get(ku, []):
            if not p["det"]:
                # unconfirmed pair: a candidate only, never granted
                top = notes_top(p["old"])
                if top:
                    cands.append((top, "MY", False, False))
                continue
            for s in sheet.get(p["old"], []):
                if s["conf"] == "HIGH" and not s["conflict"] and s["hh"]:
                    hid = s["hh"]
                    if ADV_OF_HH.get(hid) == s["adv"]:
                        grants.append(("MP", hid, s["adv"]))
            ch = certain_hh(p["old"])
            if ch and ADV_ACCT.get(p["old"]) == {ADV_OF_HH.get(ch)}:
                grants.append(("MX", ch, ADV_OF_HH[ch]))
            top = notes_top(p["old"])
            support = [x for x in (p["dell_hh"], next((s["hh"] for s in sheet.get(p["old"], []) if s["hh"]), None)) if x]
            if top and top in support:
                cands.append((top, "MC", True, True))
            elif top:
                cands.append((top, "MC", True, False))
            elif support:
                cands.append((None, "MC", True, False))

        all_hh = set(g[1] for g in grants) | set(c[0] for c in cands if c[0])
        if len(all_hh) > 1:
            conf, method, hid, adv, src = "LOW", ("MC" if any(c[2] for c in cands) else "MY"), "", "", ""
            tally["conflicts"] += 1
        elif grants:
            g = min(grants, key=lambda x: GRANT_ORDER.index(x[0]))
            conf, method, hid, adv, src = "HIGH", g[0], g[1], g[2], SOURCE_OF[g[0]]
        elif any(c[3] for c in cands) and any(c[0] for c in cands):
            c = [c for c in cands if c[3] and c[0]][0]
            conf, method, hid, adv, src = "MEDIUM", "MC", c[0], ADV_OF_HH.get(c[0], ""), ""
        elif cands:
            c = sorted(cands, key=lambda x: (not x[2], x[1]))[0]
            conf, method, hid, adv, src = "LOW", c[1], "", "", ""
        else:
            conf, method, hid, adv, src = "UNMATCHED", "", "", "", ""
        email = USER_EMAIL.get(adv, "") if adv else ""
        tally[conf] += 1
        if method:
            methods_used[(conf, method)] += 1
        if conf == "HIGH":
            tally["HIGH_" + method] += 1
            tally["grant_advisor_blank"] += 0 if adv else 1
            tally["grant_adv_" + adv] = 1
            if email:
                tally["grant_adv_email_" + adv] = 1
        rows.append((k, conf, method, hid, adv, email, src))

    with open(a.out, "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(COLS)
        for r in rows:
            wr.writerow(r)

    grant_adv = sorted(x[len("grant_adv_"):] for x in tally if x.startswith("grant_adv_") and not x.startswith("grant_adv_email_"))
    grant_adv_email = sorted(x for x in tally if x.startswith("grant_adv_email_"))
    tallies = {
        "published": len(keys), "high": tally["HIGH"], "medium": tally["MEDIUM"], "low": tally["LOW"],
        "unmatched": tally["UNMATCHED"], "conflicts": tally["conflicts"],
        "sheet_high_direct": tally["HIGH_MD"], "sheet_high_via_deterministic_pairs": tally["HIGH_MP"],
        "extended_high": tally["HIGH_MX"], "grant_ready_total": tally["HIGH"],
        "left_out": len(keys) - tally["HIGH"], "high_without_advisor": tally["grant_advisor_blank"],
        "advisors_distinct": len(grant_adv), "advisors_with_email": len(grant_adv_email),
    }
    out_digest = sha256_of(a.out)
    print("zip sha256 prefix %s; directory entries %d; directory accounts %d (in published keys: %d)" % (
        zdigest[:8], len(directory["entries"]), len(dir_accounts), len(dir_accounts & set(up2raw))))
    print("crm rows: households %d (bad %d), contacts %d (bad %d), users %d (bad %d), c360 %d (bad %d), c360 advisor agree %d" % (
        len(hh_rows), hh_bad, len(contacts), ct_bad, len(users), us_bad, len(c360), c3_bad, c360_agree))
    print("activity rows %d; rows with a pair-account token %d; ambiguous ids %d; unresolved hits %d" % (
        act_rows, act_hit_rows, ambiguous_ids, unresolved_hits))
    print("imaging listings %d; pair-account tokens %d; published-key tokens %d" % (img_files, img_old, img_bd))
    print("sheet household cells resolved %d of %d; pair rows whose crm household is a HouseholdID %d of %d" % (
        sheet_hh_pairs, len(sum(sheet.values(), [])), DELL_IN_HH, len(pairs)))
    print("tallies " + json.dumps(tallies, sort_keys=True))
    print("methods " + json.dumps(sorted(["%s/%s=%d" % (c, m, n) for (c, m), n in methods_used.items()])))
    print("output rows %d sha256 %s" % (len(rows) + 1, out_digest))


if __name__ == "__main__":
    main()
