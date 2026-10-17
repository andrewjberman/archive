"""IRPT_DASHBD TO-DB-b-324 (applier 0.7.0_AE_CloudOps~IB2): C6a, the READ-ONLY measurement of what the Cottonwood ownership map can be built against.

  python -I cotown_324.py run        steps 2 to 5b: the published keys, the directory, the sheet, the bridge, the portal advisor ids -> state324/measure.json, and the two local files
  python -I cotown_324.py compile    assemble COT_OWNERSHIP_READ_RECORD.json from state324/

Client data stays in memory and in the two local files OUTSIDE the repo (C:/opal-intake/work/). Only counts, booleans and word classes are printed or written to the repo.
Writes nothing to AWS.
"""
import csv
import hashlib
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cotc0_318 as c0  # noqa: E402  (ids_module, published(), directory registry bucket logic)

STATE = HERE / "state324"
WORK = Path("C:/opal-intake/work")
INBOUND = Path("C:/opal-intake/inbound/cottonwood-match")
SHEET = INBOUND / "20261016T0225Z_cottonwood_account_household_match (1).csv"
SHEET_SHA = "3d565f649d5c541639e1ad36e9277f91192152bcac860c0461952c9ed23fb0d1"
PAIRS = INBOUND / "dell1_desktop_20261017/Cottonwood_match_list_118_pairs.csv"
PAIRS_SHA_BEGIN = "375689dc3c75a122"
REVIEW = INBOUND / "dell1_desktop_20261017/Cottonwood_Account_Match_Review_20261016.xlsx"
REVIEW_SHA_BEGIN = "7f8905b43d871b93"
PARTNER_TABLE, USERS_TABLE = "opal-partner-cottonwood", "opal-users-v2"
APPLIER = "0.7.0_AE_CloudOps~IB2"


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def norm(v):
    """Confidence and flag words: upper-case, trimmed."""
    return (v or "").strip().upper()


def norma(v):
    """An account key as the PUBLISHER holds it: trimmed and LOWER-case (all 939 published raw keys are lower-case; the sheets write them upper-case). The id mint is case-sensitive (ids._check_raw strips only), so the sheet's account is matched, and minted, in this form."""
    return (v or "").strip().lower()


def shape(v):
    v = (v or "").strip()
    if not v:
        return "blank"
    if re.fullmatch(r"[A-Za-z]{3}", v):
        return "three-letter-code"
    if re.fullmatch(r"[0-9]+", v):
        return "numeric"
    if re.fullmatch(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", v):
        return "uuid"
    if re.fullmatch(r"[A-Za-z0-9]+(_[A-Za-z0-9]+)+", v):
        return "underscore-slug"
    if re.fullmatch(r"[A-Za-z]+", v):
        return "word"
    return "other"


def review_answers_filled():
    """The non-blank cells under the header 'Your answer' on the sheet 'To confirm' of the review workbook (xlsx = zip of xml; no cell value is printed or kept)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main", "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    z = zipfile.ZipFile(REVIEW)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    target = None
    for s in wb.find("m:sheets", ns):
        if s.get("name") == "To confirm":
            target = rels[s.get("{%s}id" % ns["r"])]
    assert target, "sheet To confirm not found"
    sheet = ET.fromstring(z.read("xl/" + target.lstrip("/").replace("xl/", "")))
    rows = sheet.find("m:sheetData", ns).findall("m:row", ns)

    def cell_text(c):
        v = c.find("m:v", ns)
        if c.get("t") == "s" and v is not None:
            return shared[int(v.text)]
        if c.get("t") == "inlineStr":
            return "".join(t.text or "" for t in c.iter("{%s}t" % ns["m"]))
        return v.text if v is not None else ""
    col = None
    for r in rows[:6]:
        for c in r.findall("m:c", ns):
            if cell_text(c).strip().lower() == "your answer":
                col = re.match(r"[A-Z]+", c.get("r")).group(0)
                hdr = int(r.get("r"))
        if col:
            break
    assert col, "header Your answer not found"
    n = 0
    for r in rows:
        if int(r.get("r")) <= hdr:
            continue
        for c in r.findall("m:c", ns):
            if re.match(r"[A-Z]+", c.get("r")).group(0) == col and cell_text(c).strip():
                n += 1
    return n


def cmd_run():
    ids = c0.ids_module()
    WORK.mkdir(parents=True, exist_ok=True)
    # 2. published keys
    _, raws = c0.published("cottonwood", ids)
    print("STEP2 published prefixes=%d (denominator printed; expected 939)" % len(raws))
    (WORK / "cot_published_raw.txt").write_bytes(("\n".join(sorted(raws)) + "\n").encode("utf-8"))
    minted, unmint = {}, 0
    for raw in raws:
        try:
            minted[ids.opaque_account("cottonwood", raw)] = raw
        except ids.IdRefused:
            unmint += 1
    published = {"prefixes": len(raws), "mintable": len(minted), "unmintable": unmint}
    raw_set = set(raws)
    raw_shapes = {}
    for raw in raws:
        k = "digits-len%d" % len(raw) if raw.isdigit() else ("alnum-len%d" % len(raw) if raw.isalnum() else "other")
        raw_shapes[k] = raw_shapes.get(k, 0) + 1
    # 3. directory (byte-exact object written outside the repo)
    import json as _j
    reg = _j.loads((c0.ROOT / "data/firm_registry.json").read_text(encoding="utf-8"))
    bucket = [f["bucket"] for f in reg["firms"] if f.get("firm_id") == "cottonwood" and f.get("enabled") and f.get("bucket")]
    assert len(bucket) == 1
    ptr = _j.loads(c0.s3.get_object(Bucket=bucket[0], Key="investor-reporting/directory/latest.json")["Body"].read())
    body = c0.s3.get_object(Bucket=bucket[0], Key=ptr["key"])["Body"].read()
    (WORK / "cot_directory_latest.json").write_bytes(body)
    d = _j.loads(body.decode("utf-8"))
    ents = d.get("entries", [])
    dacc = set()
    for e in ents:
        dacc.update(str(a) for a in ((e.get("ids") or {}).get("account_ids") or []))
    directory = {"entries": len(ents), "entries_with_client_id": sum(1 for e in ents if (e.get("ids") or {}).get("client_id")),
                 "entries_with_relationship_id": sum(1 for e in ents if (e.get("ids") or {}).get("relationship_id")),
                 "entries_with_accounts": sum(1 for e in ents if (e.get("ids") or {}).get("account_ids")), "distinct_accounts": len(dacc),
                 "firm_id_opaque_present": bool(d.get("firm_id_opaque")), "accounts_in_published": len(dacc & set(minted)), "published_in_directory": len(set(minted) & dacc)}
    print("STEP3 directory", json.dumps(directory, sort_keys=True))
    # 4. the sheet
    sb = SHEET.read_bytes()
    if hashlib.sha256(sb).hexdigest() != SHEET_SHA:
        print("STOP: the sheet's sha256 differs")
        return 3
    rows = list(csv.DictReader(sb.decode("utf-8-sig").splitlines()))
    conf = [norm(r.get("confidence")) for r in rows]
    acc = [norma(r.get("account")) for r in rows]
    codes = [(r.get("advisor") or "").strip().lower() for r in rows]
    high = [i for i, c in enumerate(conf) if c == "HIGH"]
    med = [i for i, c in enumerate(conf) if c == "MEDIUM"]
    in_raw = [a in raw_set for a in acc]

    def minted_in_dir(a):
        try:
            return ids.opaque_account("cottonwood", a) in dacc
        except Exception:  # noqa: BLE001
            return False
    hbc = {}
    for i in high:
        hbc[codes[i]] = hbc.get(codes[i], 0) + 1
    sheet = {"pair": "newer", "rows": len(rows), "high": len(high), "medium": len(med), "low": conf.count("LOW"), "unmatched": conf.count("UNMATCHED"), "all_in_published_raw": sum(in_raw),
             "high_in_published_raw": sum(1 for i in high if in_raw[i]), "medium_in_published_raw": sum(1 for i in med if in_raw[i]), "high_in_directory": sum(1 for i in high if minted_in_dir(acc[i])),
             "advisor_codes": len({c for c in codes if c}), "high_by_advisor_code": hbc}
    print("STEP4 sheet", json.dumps({k: v for k, v in sheet.items() if k != "high_by_advisor_code"}, sort_keys=True), "high_by_code_counts", sorted(hbc.values()))
    sheet_shapes = {}
    for a in acc:
        k = "digits-len%d" % len(a) if a.isdigit() else ("alnum-len%d" % len(a) if a.isalnum() else "other")
        sheet_shapes[k] = sheet_shapes.get(k, 0) + 1
    # 4b. the bridge
    pb = PAIRS.read_bytes()
    if not hashlib.sha256(pb).hexdigest().startswith(PAIRS_SHA_BEGIN) or not hashlib.sha256(REVIEW.read_bytes()).hexdigest().startswith(REVIEW_SHA_BEGIN):
        print("STOP: the pair list or the review workbook differs from its recorded sha256")
        return 3
    pr = list(csv.DictReader(pb.decode("utf-8-sig").splitlines()))
    det = [p for p in pr if norm(p.get("to_confirm")).startswith("NO")]
    old_all = {norma(p["commonwealth_account"]) for p in pr}
    new_all = {norma(p["black_diamond_account"]) for p in pr}
    det_old_to_new = {}
    for p in det:
        det_old_to_new.setdefault(norma(p["commonwealth_account"]), set()).add(norma(p["black_diamond_account"]))
    direct = {i for i in high if in_raw[i]}
    via = {i for i in high if i not in direct and any(n in raw_set for n in det_old_to_new.get(acc[i], ()))}
    bridge = {"pairs": len(pr), "deterministic": len(det), "to_confirm": len(pr) - len(det), "distinct_old": len(old_all), "distinct_new": len(new_all),
              "sheet_accounts_in_old": sum(1 for a in acc if a in old_all), "sheet_high_in_old": sum(1 for i in high if acc[i] in old_all), "sheet_medium_in_old": sum(1 for i in med if acc[i] in old_all),
              "new_in_published_raw": len(new_all & raw_set), "deterministic_new_in_published_raw": len({norma(p["black_diamond_account"]) for p in det} & raw_set),
              "high_direct": len(direct), "high_via_deterministic_pairs": len(via), "high_left_out": len(high) - len(direct) - len(via), "grant_ready": len(direct) + len(via),
              "answers_filled": review_answers_filled()}
    print("STEP5b bridge", json.dumps(bridge, sort_keys=True))
    # the portal advisor ids (read only; the projection is ONE attribute; values are compared in memory and never printed)
    dyn = c0.boto3.client("dynamodb", region_name="us-east-1")
    n_users = 0
    for pg in dyn.get_paginator("query").paginate(TableName=USERS_TABLE, IndexName="firmId-index", KeyConditionExpression="firmId = :f", ExpressionAttributeValues={":f": {"S": "cottonwood"}}, Select="COUNT"):
        n_users += pg["Count"]
    keys = []
    for pg in dyn.get_paginator("scan").paginate(TableName=PARTNER_TABLE, ProjectionExpression="advisorKey"):
        keys += [i.get("advisorKey", {}).get("S", "") for i in pg["Items"]]
    with_id = [k for k in keys if k.strip()]
    shapes = sorted({shape(k) for k in with_id})
    found = {c for c in set(codes) if c and c in {k.strip().lower() for k in with_id}}
    users = {"table": PARTNER_TABLE, "firm_attribute": "firmId", "advisor_attribute": "advisorKey", "cottonwood_users": n_users, "cottonwood_users_with_advisor_id": len(with_id),
             "advisor_id_shapes": shapes, "sheet_codes_found_as_advisor_id": len(found), "high_rows_under_a_found_code": sum(1 for i in high if codes[i] in found), "second_source_available": False}
    print("USERS", json.dumps(users, sort_keys=True), "partner rows scanned", len(keys))
    sh_codes = sorted({shape(c) for c in set(codes) if c})
    print("sheet code shapes:", sh_codes, "| raw key shapes:", sorted(raw_shapes.items()), "| sheet account shapes:", sorted(sheet_shapes.items()))
    lf = {}
    for name, path in (("published_raw", WORK / "cot_published_raw.txt"), ("directory", WORK / "cot_directory_latest.json")):
        data = path.read_bytes()
        lf[name] = {"path": "C:/opal-intake/work/" + path.name, "sha256": hashlib.sha256(data).hexdigest(), "lines": len(data.splitlines())}
    save("measure.json", {"published": published, "directory": directory, "sheet": sheet, "bridge": bridge, "users": users, "local_files": lf,
                          "raw_shapes": raw_shapes, "sheet_shapes": sheet_shapes, "sheet_code_shapes": sh_codes})
    return 0


def cmd_probe():
    """Key-format probe, counts only (no value printed): how the published raw keys relate to the sheet's accounts and the bridge's current accounts."""
    raws = [x.strip() for x in (WORK / "cot_published_raw.txt").read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = list(csv.DictReader(SHEET.read_bytes().decode("utf-8-sig").splitlines()))
    sheet_acc = {norma(r.get("account")) for r in rows if norma(r.get("account"))}
    pr = list(csv.DictReader(PAIRS.read_bytes().decode("utf-8-sig").splitlines()))
    new_acc = {norma(p["black_diamond_account"]) for p in pr}
    up = [r.lower() for r in raws]

    def rel(a):
        return {"equal": a in up, "raw_endswith": any(r.endswith(a) for r in up), "raw_startswith": any(r.startswith(a) for r in up), "raw_contains": any(a in r for r in up),
                "a_contains_raw": any(r in a for r in up)}
    out = {}
    for name, acc in (("sheet_accounts", sheet_acc), ("bridge_current_accounts", new_acc)):
        tally = {}
        for a in acc:
            for k, v in rel(a).items():
                tally[k] = tally.get(k, 0) + int(v)
        out[name] = {"n": len(acc), **tally}
    out["raw_keys"] = {"n": len(raws), "all_digits": sum(1 for r in raws if r.isdigit()), "first_char_letter": sum(1 for r in raws if r[:1].isalpha()), "last_char_letter": sum(1 for r in raws if r[-1:].isalpha()),
                       "distinct_length_classes": sorted({len(r) for r in raws})}
    save("probe.json", out)
    print("PROBE", json.dumps(out, sort_keys=True))
    return 0


def cmd_compile():
    m = load("measure.json")
    rec = {"claim": "measured", "applier": APPLIER, "no_write_to_aws": True, "published": m["published"], "directory": m["directory"], "sheet": m["sheet"], "bridge": m["bridge"], "users": m["users"],
           "authorizer": {"header_source_path": "infra/aws/users/lambda/portal-authorizer/index.mjs",
                          "advisor_header_origin": "the advisorId claim of the signed token: the login function (infra/aws/opalinvest_dev/lambda/auth-handler/src/db.ts getPartnerIdentity) copies the advisorKey attribute of the user's row in the per-partner table opal-partner-<firm>, and the edge validator injects it as X-Advisor-Id"},
           "local_files": m["local_files"], "notes": (STATE / "notes.txt").read_text(encoding="ascii").strip(), "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "COT_OWNERSHIP_READ_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COT_OWNERSHIP_READ_RECORD.json")
    return 0


if __name__ == "__main__":
    sys.exit({"run": cmd_run, "probe": cmd_probe}.get(sys.argv[1], cmd_compile)())
