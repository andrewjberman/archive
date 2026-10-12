"""count_stored_inputs.py -- a READ-ONLY count of the stored upload inputs the new template reader would read differently.

TO IRPT_ANLREQ.TO-AR-y-161 (round 16, workstream Y). It makes NO write call of any kind. It reads:
  * the requests table: one SCAN for the INPUT# rows; GetItem of the UPLOAD# row and of the ARTIFACT# rows each input
    names; one QUERY per tenant for the analysis# rows (only for a tenant that holds an input the new reader turns back);
  * the bucket: GetObject (by the version the ARTIFACT# row records) of a template input's retained original, of its
    normalized document (which holds the template stored at acceptance), and of the composition of each accepted request.

Live use (a reader seat that holds the reads):
  python count_stored_inputs.py --table <T> --bucket <B> --region <R> --new-reader <file> [--old-reader <file>] [--out <file>]
Offline proof (no AWS, no network; fetches the new reader with `git show` into a temp folder outside the checkout):
  python count_stored_inputs.py --self-test

The LAST line of stdout is ONE JSON object of counts and dates. No input id, upload id, file name, ticker, amount, account
value or person is ever printed. An input the script cannot read is counted `unreadable` under the error's code, never as
reading the same. A scan or query that fails exits 3 and prints the error's code on stderr.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter

NEW_READER_COMMIT = "d95cf11106"
READER_REL = "infra/aws/lambda/investor-reporting/intake/template_reader.py"
KNOWN_CAUSES = ("TOTAL_ROW_PRESENT", "HEADER_ROW_REPEATED", "ACCOUNT_COLUMN_SEVERAL_VALUES", "SHEETS_NOT_READ")
CODE_TEXT = re.compile(r"[A-Z][A-Z0-9_]{0,40}\Z")


class Unreadable(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


class ScanFailed(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def safe_code(exc):
    """The error's code, restricted to a short token (an AWS error code, or the exception class name)."""
    code = getattr(exc, "response", {}).get("Error", {}).get("Code") if isinstance(getattr(exc, "response", None), dict) else None
    code = code or type(exc).__name__
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", str(code))[:48] or "ERROR"


def plain(value):
    """DynamoDB typed value (low-level client) to a plain python value."""
    if isinstance(value, dict) and len(value) == 1:
        (kind, inner), = value.items()
        if kind == "S":
            return inner
        if kind == "N":
            number = float(inner)
            return int(number) if number == int(number) else number
        if kind == "BOOL":
            return bool(inner)
        if kind == "NULL":
            return None
        if kind == "M":
            return {key: plain(item) for key, item in inner.items()}
        if kind == "L":
            return [plain(item) for item in inner]
    return value


def plain_item(item):
    return {key: plain(value) for key, value in item.items()}


def load_reader(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def repo_root(start):
    got = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start, capture_output=True, text=True)
    if got.returncode != 0 or not got.stdout.strip():
        raise SystemExit("ERROR: not inside a git checkout (cannot place the running reader)")
    return got.stdout.strip()


class Reads:
    """The only AWS-facing surface: get-item, scan, query on the table; get-object on the bucket. Nothing else."""

    def __init__(self, ddb, s3, table, bucket):
        self.ddb, self.s3, self.table, self.bucket = ddb, s3, table, bucket

    def row(self, tenant, revision):
        try:
            got = self.ddb.get_item(TableName=self.table, ConsistentRead=True,
                                    Key={"tenant": {"S": tenant}, "request_revision": {"S": revision}})
        except Exception as exc:
            raise Unreadable(safe_code(exc)) from None
        return plain_item(got["Item"]) if got.get("Item") else None

    def blob(self, tenant, artifact_id):
        """The bytes of one retained artifact, by the version its ARTIFACT# row records, verified against its digest."""
        if not isinstance(artifact_id, str) or not artifact_id:
            raise Unreadable("ARTIFACT_ID_MISSING")
        item = self.row(tenant, "ARTIFACT#" + artifact_id)
        if item is None:
            raise Unreadable("ARTIFACT_ROW_MISSING")
        where, ref = item.get("blob"), item.get("ref")
        if not isinstance(where, dict) or not isinstance(ref, dict):
            raise Unreadable("ARTIFACT_ROW_SHAPE")
        if where.get("bucket") != self.bucket:
            raise Unreadable("BUCKET_NOT_THE_ARGUMENT")
        if not where.get("key") or not where.get("version_id") or where["version_id"] == "null":
            raise Unreadable("OBJECT_VERSION_MISSING")
        try:
            body = self.s3.get_object(Bucket=where["bucket"], Key=where["key"], VersionId=where["version_id"])["Body"]
            try:
                data = body.read()
            finally:
                body.close()
        except Exception as exc:
            raise Unreadable(safe_code(exc)) from None
        if hashlib.sha256(data).hexdigest() != ref.get("sha256"):
            raise Unreadable("DIGEST_MISMATCH")
        return data


class Stats:
    def __init__(self):
        self.lanes, self.causes, self.unreadable = Counter(), Counter(), Counter()
        self.template = self.old_differs = self.same = self.differs = self.turned_back = 0
        self.with_report = self.without_report = self.requests = 0
        self.requests_unreadable, self.months = Counter(), Counter()
        self.latest = None

    def add_input(self, rec):
        self.lanes[rec["lane"]] += 1
        if rec["status"] == "not_template":
            return
        if rec["status"] == "unreadable":
            self.unreadable[rec["code"]] += 1
            if rec.get("counted_template"):
                self.template += 1
            return
        self.template += 1
        self.old_differs += 1 if rec["old_differs"] else 0
        if rec["status"] == "same":
            self.same += 1
            return
        self.differs += 1
        for cause in rec["causes"]:
            self.causes[cause] += 1
        self.turned_back += 1 if rec["turned_back"] else 0

    def add_report(self, times):
        if not times:
            self.without_report += 1
            return
        self.with_report += 1
        self.requests += len(times)
        top = max(times)
        day = datetime.datetime.fromtimestamp(top, tz=datetime.timezone.utc).strftime("%Y-%m-%d")
        self.months[day[:7]] += 1
        self.latest = max(self.latest or day, day)

    def to_json(self):
        return {"inputs_by_lane": dict(sorted(self.lanes.items())), "template_inputs": self.template,
                "old_reader_differs": self.old_differs, "read_the_same": self.same, "read_differently": self.differs,
                "by_cause": dict(sorted(self.causes.items())), "turned_back": self.turned_back,
                "turned_back_with_a_report": {"with": self.with_report, "without": self.without_report,
                                              "requests": self.requests,
                                              "requests_unreadable": dict(sorted(self.requests_unreadable.items())),
                                              "latest_report_day": self.latest,
                                              "latest_report_day_by_month": dict(sorted(self.months.items()))},
                "unreadable": dict(sorted(self.unreadable.items()))}


def cause_names(stored, new):
    stored_codes = {f.get("code") for f in stored.get("findings", [])}
    causes = []
    for code in sorted({f.get("code") for f in new.get("findings", [])} - stored_codes):
        causes.append(code if code in KNOWN_CAUSES else "OTHER:" + (code if isinstance(code, str) and CODE_TEXT.match(code) else "UNNAMED"))
    def rest(template):
        return {k: v for k, v in template.items() if k != "findings"}
    if rest(new) != rest(stored):
        causes.append("OTHER:NON_FINDING_DIFFERENCE")
    return causes or ["OTHER:SAME_CODES_DIFFERENT_FINDINGS"]


def classify(reads, row, old, new):
    """One INPUT# row to one record of counts. The input id stays in memory only (for the request join)."""
    tenant, rec = row.get("tenant"), {"tenant": row.get("tenant"), "input_id": row.get("identity")}
    try:
        upload = reads.row(tenant, "UPLOAD#" + str(row.get("upload_id")))
    except Unreadable as exc:
        return dict(rec, lane="UNKNOWN", status="unreadable", code=exc.code)
    if upload is None:
        return dict(rec, lane="UNKNOWN", status="unreadable", code="UPLOAD_ROW_MISSING")
    lane = upload.get("source_lane")
    lane = "CSV_UPLOAD" if lane is None else (lane if lane == "TEMPLATE_UPLOAD" else "OTHER_LANE")
    rec["lane"] = lane
    if lane != "TEMPLATE_UPLOAD":
        return dict(rec, status="not_template")
    rec["counted_template"] = True
    try:
        file_type = upload.get("file_type")
        if file_type not in ("csv", "xlsx"):
            raise Unreadable("FILE_TYPE_UNKNOWN")
        original = upload.get("artifact_ref")
        raw = reads.blob(tenant, original.get("artifact_id") if isinstance(original, dict) else None)
        if hashlib.sha256(raw).hexdigest() != upload.get("content_sha256"):
            raise Unreadable("DIGEST_MISMATCH")
        kept = row.get("artifact_ref")
        document = reads.blob(tenant, kept.get("artifact_id") if isinstance(kept, dict) else None)
        try:
            stored = json.loads(document).get("template")
        except (ValueError, AttributeError):
            raise Unreadable("STORED_DOCUMENT_NOT_JSON") from None
        if not isinstance(stored, dict):
            raise Unreadable("STORED_TEMPLATE_MISSING")
        try:
            by_old, by_new = old.read_template(raw, file_type), new.read_template(raw, file_type)
        except Exception:
            raise Unreadable("READER_RAISED") from None
    except Unreadable as exc:
        return dict(rec, status="unreadable", code=exc.code)
    rec["old_differs"] = by_old != stored
    if by_new == stored:
        return dict(rec, status="same")
    return dict(rec, status="differs", causes=cause_names(stored, by_new),
                turned_back=any(f.get("severity") == "ERROR" for f in by_new.get("findings", [])))


def scan_inputs(ddb, table):
    rows, scanned, start = [], 0, None
    while True:
        # Every projected attribute goes through a name placeholder: a bare attribute that is a DynamoDB reserved word
        # (identity is one) is refused with ValidationException before any item is read (the first live run, 2026-10-12).
        names = {"#t": "tenant", "#r": "request_revision", "#i": "identity", "#u": "upload_id", "#a": "artifact_ref",
                 "#c": "content_sha256"}
        args = {"TableName": table, "ConsistentRead": True, "FilterExpression": "begins_with(#r, :p)",
                "ExpressionAttributeNames": names,
                "ExpressionAttributeValues": {":p": {"S": "INPUT#"}},
                "ProjectionExpression": ", ".join(sorted(names))}
        if start:
            args["ExclusiveStartKey"] = start
        try:
            page = ddb.scan(**args)
        except Exception as exc:
            raise ScanFailed(safe_code(exc)) from None
        scanned += page.get("ScannedCount", 0)
        rows.extend(plain_item(item) for item in page.get("Items", []))
        start = page.get("LastEvaluatedKey")
        if not start:
            return rows, scanned


def accepted_requests(ddb, table, tenant):
    out, start = [], None
    while True:
        args = {"TableName": table, "ConsistentRead": True, "KeyConditionExpression": "#t = :t AND begins_with(#r, :p)",
                "ExpressionAttributeNames": {"#t": "tenant", "#r": "request_revision"},
                "ExpressionAttributeValues": {":t": {"S": tenant}, ":p": {"S": "analysis#"}}}
        if start:
            args["ExclusiveStartKey"] = start
        try:
            page = ddb.query(**args)
        except Exception as exc:
            raise ScanFailed(safe_code(exc)) from None
        out.extend(plain_item(item) for item in page.get("Items", []))
        start = page.get("LastEvaluatedKey")
        if not start:
            return out


def count(ddb, s3, table, bucket, old, new, now=None):
    reads = Reads(ddb, s3, table, bucket)
    rows, scanned = scan_inputs(ddb, table)
    total, tenants, back = Stats(), {}, {}
    for row in rows:
        rec = classify(reads, row, old, new)
        stats = tenants.setdefault(str(rec["tenant"]), Stats())
        for target in (total, stats):
            target.add_input(rec)
        if rec["status"] == "differs" and rec["turned_back"]:
            back.setdefault(str(rec["tenant"]), {})[rec["input_id"]] = []
    for tenant, named in back.items():
        stats = tenants[tenant]
        for item in accepted_requests(ddb, table, tenant):
            try:
                record = json.loads(item["record"])
                when = record["accepted_at"]
                if type(when) is not int:
                    raise Unreadable("ACCEPTED_AT_INVALID")
                document = json.loads(reads.blob(tenant, record["composition_ref"]["artifact_id"]))
                ids = {(document.get("browser") or {}).get("input_id"),
                       (((document.get("resolved") or {}).get("input_ref")) or {}).get("input_id")}
            except Unreadable as exc:
                code = exc.code
            except (ValueError, KeyError, TypeError, AttributeError):
                code = "REQUEST_RECORD_SHAPE"
            else:
                for input_id in ids & set(named):
                    named[input_id].append(when)
                continue
            for target in (total, stats):
                target.requests_unreadable[code] += 1
        for times in named.values():
            for target in (total, stats):
                target.add_report(times)
    out = total.to_json()
    out["items_scanned"] = scanned
    out["by_tenant"] = {tenant: tenants[tenant].to_json() for tenant in sorted(tenants)}
    out["read_at"] = (now or datetime.datetime.now(datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return out


# ----------------------------------------------------------------------------------------------------------------------
# the offline proof: in-memory fakes holding SYNTHETIC stored inputs
# ----------------------------------------------------------------------------------------------------------------------

class FakeClientError(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.response = {"Error": {"Code": code}}


def typed(value):
    if isinstance(value, bool):
        return {"BOOL": value}
    if isinstance(value, (int, float)):
        return {"N": str(value)}
    if value is None:
        return {"NULL": True}
    if isinstance(value, str):
        return {"S": value}
    if isinstance(value, list):
        return {"L": [typed(v) for v in value]}
    return {"M": {k: typed(v) for k, v in value.items()}}


class FakeDdb:
    PAGE = 7

    def __init__(self):
        self.rows, self.deny_scan, self.log = {}, False, Counter()

    def add(self, item):
        self.rows[(item["tenant"], item["request_revision"])] = item

    def get_item(self, **args):
        self.log["get_item"] += 1
        key = (args["Key"]["tenant"]["S"], args["Key"]["request_revision"]["S"])
        item = self.rows.get(key)
        return {"Item": {k: typed(v) for k, v in item.items()}} if item else {}

    def _page(self, args, wanted, size):
        keys = sorted(self.rows)
        begin = 0
        if args.get("ExclusiveStartKey"):
            begin = keys.index((args["ExclusiveStartKey"]["tenant"]["S"], args["ExclusiveStartKey"]["request_revision"]["S"])) + 1
        chunk = keys[begin:begin + size]
        got = {"Items": [{k: typed(v) for k, v in self.rows[key].items()} for key in chunk if wanted(key)],
               "ScannedCount": len(chunk)}
        if begin + size < len(keys):
            got["LastEvaluatedKey"] = {"tenant": {"S": chunk[-1][0]}, "request_revision": {"S": chunk[-1][1]}}
        return got

    def scan(self, **args):
        self.log["scan"] += 1
        if self.deny_scan:
            raise FakeClientError("AccessDeniedException")
        prefix = args["ExpressionAttributeValues"][":p"]["S"]
        return self._page(args, lambda key: key[1].startswith(prefix), self.PAGE)

    def query(self, **args):
        self.log["query"] += 1
        tenant, prefix = args["ExpressionAttributeValues"][":t"]["S"], args["ExpressionAttributeValues"][":p"]["S"]
        keys = [k for k in sorted(self.rows) if k[0] == tenant and k[1].startswith(prefix)]
        begin = 0
        if args.get("ExclusiveStartKey"):
            begin = keys.index((tenant, args["ExclusiveStartKey"]["request_revision"]["S"])) + 1
        chunk = keys[begin:begin + 2]
        got = {"Items": [{k: typed(v) for k, v in self.rows[key].items()} for key in chunk]}
        if begin + 2 < len(keys):
            got["LastEvaluatedKey"] = {"tenant": {"S": tenant}, "request_revision": {"S": chunk[-1][1]}}
        return got


class FakeS3:
    def __init__(self):
        self.objects, self.denied, self.log = {}, set(), Counter()

    def get_object(self, **args):
        self.log["get_object"] += 1
        key = (args["Bucket"], args["Key"], args["VersionId"])
        if key[1] in self.denied:
            raise FakeClientError("AccessDenied")
        if key not in self.objects:
            raise FakeClientError("NoSuchKey")
        return {"Body": io.BytesIO(self.objects[key])}


def xlsx(sheets):
    """A minimal workbook: [(sheet name, [[cell, ...], ...]), ...]; a str cell is inline text, anything else a number."""
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rid = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    pkg = "http://schemas.openxmlformats.org/package/2006/relationships"
    names = "".join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (n, i, i) for i, (n, _) in enumerate(sheets, 1))
    rels = "".join('<Relationship Id="rId%d" Type="%s/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, rid, i)
                   for i in range(1, len(sheets) + 1))
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as archive:
        archive.writestr("xl/workbook.xml", '<workbook xmlns="%s" xmlns:r="%s"><sheets>%s</sheets></workbook>' % (main, rid, names))
        archive.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="%s">%s</Relationships>' % (pkg, rels))
        for i, (_, grid) in enumerate(sheets, 1):
            body = ""
            for r, line in enumerate(grid, 1):
                cells = ""
                for c, value in enumerate(line):
                    addr = "%s%d" % ("ABCDEFG"[c], r)
                    cells += ('<c r="%s" t="inlineStr"><is><t>%s</t></is></c>' % (addr, value) if isinstance(value, str)
                              else '<c r="%s"><v>%s</v></c>' % (addr, value))
                body += '<row r="%d">%s</row>' % (r, cells)
            archive.writestr("xl/worksheets/sheet%d.xml" % i, '<worksheet xmlns="%s"><sheetData>%s</sheetData></worksheet>' % (main, body))
    return out.getvalue()


def fetch_new_reader(root, folder):
    got = subprocess.run(["git", "show", "%s:%s" % (NEW_READER_COMMIT, READER_REL)], cwd=root, capture_output=True)
    if got.returncode != 0 or not got.stdout:
        raise SystemExit("ERROR: git show %s:%s failed" % (NEW_READER_COMMIT, READER_REL))
    path = os.path.join(folder, "new_reader_under_test.py")
    with open(path, "wb") as handle:
        handle.write(got.stdout)
    return path


BUCKET, TABLE = "synthetic-bucket", "synthetic-table"
HEAD = "Ticker,Dollars\n"
SHEETS = {
    "clean": HEAD + "ZZAA,100\nZZBB,200\n",
    "total": HEAD + "ZZAA,100\nZZBB,200\nTotal,300\n",
    "repeat": HEAD + "ZZAA,100\nZZBB,200\nTicker,Dollars\nZZCC,50\n",
    "two_accounts": "Ticker,Dollars,Account\nZZAA,100,QQ-1\nZZBB,200,QQ-2\n",
    "both": HEAD + "ZZAA,100\nTotal,100\nTicker,Dollars\nZZCC,50\n",
}


def build_world(old):
    ddb, s3 = FakeDdb(), FakeS3()

    def artifact(tenant, label, data, claim=None):
        art = "ART-" + hashlib.sha256(label.encode()).hexdigest()
        key = "synthetic/%s/%s" % (tenant, art)
        ddb.add({"tenant": tenant, "request_revision": "ARTIFACT#" + art, "logical_id": label,
                 "ref": {"artifact_id": art, "sha256": claim or hashlib.sha256(data).hexdigest(), "byte_length": len(data)},
                 "blob": {"bucket": BUCKET, "key": key, "version_id": "v1"}})
        s3.objects[(BUCKET, key, "v1")] = data
        return art, key

    def stored_input(tenant, tag, raw, file_type="csv", lane="TEMPLATE_UPLOAD", fault=None, alter_template=False):
        upload_id = "UP-" + hashlib.sha256(tag.encode()).hexdigest()
        input_id = "portfolio_" + hashlib.sha256(("p" + tag).encode()).hexdigest()
        digest = hashlib.sha256(raw).hexdigest()
        art, key = artifact(tenant, "orig" + tag, raw)
        if fault == "missing":
            del s3.objects[(BUCKET, key, "v1")]
        elif fault == "denied":
            s3.denied.add(key)
        elif fault == "altered":
            s3.objects[(BUCKET, key, "v1")] = raw + b"x"
        upload = {"tenant": tenant, "request_revision": "UPLOAD#" + upload_id, "identity": upload_id,
                  "content_sha256": digest, "artifact_ref": {"artifact_id": art}}
        document = {"schema_version": "irpt-normalized-portfolio.v2", "source": {"lane": lane}}
        if lane == "TEMPLATE_UPLOAD":
            upload.update(source_lane="TEMPLATE_UPLOAD", file_type=file_type)
            document["template"] = old.read_template(raw, file_type)  # stored by the OLD reader
            if alter_template:
                document["template"]["basis"] = "TARGET_WEIGHT"
        ddb.add(upload)
        nart, _ = artifact(tenant, "norm" + tag, json.dumps(document, sort_keys=True).encode())
        ddb.add({"tenant": tenant, "request_revision": "INPUT#" + input_id, "identity": input_id, "upload_id": upload_id,
                 "artifact_ref": {"artifact_id": nart}, "content_sha256": hashlib.sha256(tag.encode()).hexdigest()})
        return input_id

    def accept(tenant, label, input_id, when, via="browser", unreadable=False):
        doc = {"schema_version": "irpt-analysis-composition.v1", "browser": {"x": 1}, "resolved": {"input_ref": {"input_id": "none"}}}
        doc["browser" if via == "browser" else "resolved"] = ({"input_id": input_id} if via == "browser" else {"input_ref": {"input_id": input_id}})
        art, key = artifact(tenant, "comp" + label, json.dumps(doc).encode())
        if unreadable:
            del s3.objects[(BUCKET, key, "v1")]
        rid = "REQ-" + hashlib.sha256(label.encode()).hexdigest()[:24]
        ddb.add({"tenant": tenant, "request_revision": "analysis#%s#1" % rid,
                 "record": json.dumps({"accepted_at": when, "composition_ref": {"artifact_id": art}})})

    def epoch(text):
        return int(datetime.datetime.strptime(text, "%Y-%m-%d").replace(tzinfo=datetime.timezone.utc).timestamp()) + 3600

    a1 = stored_input("firm-a", "a1", SHEETS["clean"].encode())
    a2 = stored_input("firm-a", "a2", SHEETS["total"].encode())
    stored_input("firm-a", "a3", SHEETS["repeat"].encode())
    stored_input("firm-a", "a4", SHEETS["clean"].encode(), lane="CSV_UPLOAD")
    stored_input("firm-a", "a5", SHEETS["both"].encode())
    stored_input("firm-a", "a6", SHEETS["clean"].encode(), alter_template=True)
    b1 = stored_input("firm-b", "b1", SHEETS["two_accounts"].encode())
    b2 = stored_input("firm-b", "b2", xlsx([("holdings_template", [["Ticker", "Dollars"], ["ZZAA", 100]]),
                                            ("Other", [["Ticker", "Dollars"], ["ZZBB", 5]])]), file_type="xlsx")
    stored_input("firm-b", "b3", SHEETS["clean"].encode(), fault="missing")
    stored_input("firm-b", "b4", SHEETS["clean"].encode(), fault="denied")
    stored_input("firm-b", "b5", SHEETS["clean"].encode(), fault="altered")
    accept("firm-a", "r1", a1, epoch("2026-09-20"))
    accept("firm-a", "r2", a2, epoch("2026-09-03"))
    accept("firm-a", "r3", a2, epoch("2026-10-02"), via="resolved")
    accept("firm-b", "r4", b1, epoch("2026-08-15"))
    accept("firm-b", "r5", b2, epoch("2026-09-09"))
    accept("firm-b", "r6", b1, epoch("2026-10-09"), unreadable=True)
    return ddb, s3


EXPECTED = {
    "inputs_by_lane": {"CSV_UPLOAD": 1, "TEMPLATE_UPLOAD": 10}, "template_inputs": 10, "old_reader_differs": 1,
    "read_the_same": 1, "read_differently": 6,
    "by_cause": {"ACCOUNT_COLUMN_SEVERAL_VALUES": 1, "HEADER_ROW_REPEATED": 2, "OTHER:NON_FINDING_DIFFERENCE": 1,
                 "SHEETS_NOT_READ": 1, "TOTAL_ROW_PRESENT": 2},
    "turned_back": 4,
    "turned_back_with_a_report": {"with": 2, "without": 2, "requests": 3, "requests_unreadable": {"NoSuchKey": 1},
                                  "latest_report_day": "2026-10-02",
                                  "latest_report_day_by_month": {"2026-08": 1, "2026-10": 1}},
    "unreadable": {"AccessDenied": 1, "DIGEST_MISMATCH": 1, "NoSuchKey": 1},
    "items_scanned": 11 * 4 + 6 * 2,
}
EXPECTED_TENANT = {
    "firm-a": {"inputs_by_lane": {"CSV_UPLOAD": 1, "TEMPLATE_UPLOAD": 5}, "template_inputs": 5, "old_reader_differs": 1,
               "read_the_same": 1, "read_differently": 4, "turned_back": 3, "unreadable": {},
               "with": 1, "without": 2},
    "firm-b": {"inputs_by_lane": {"TEMPLATE_UPLOAD": 5}, "template_inputs": 5, "old_reader_differs": 0,
               "read_the_same": 0, "read_differently": 2, "turned_back": 1,
               "unreadable": {"AccessDenied": 1, "DIGEST_MISMATCH": 1, "NoSuchKey": 1}, "with": 1, "without": 0},
}


def self_test(root):
    folder = tempfile.mkdtemp(prefix="count_stored_inputs_selftest_")
    try:
        new_path = fetch_new_reader(root, folder)
        old_path = os.path.join(root, *READER_REL.split("/"))
        print("self-test: new reader %s:%s sha256 %s" % (NEW_READER_COMMIT, READER_REL, file_sha256(new_path)), file=sys.stderr)
        print("self-test: old reader (this checkout) sha256 %s" % file_sha256(old_path), file=sys.stderr)
        old, new = load_reader(old_path, "old_template_reader_under_test"), load_reader(new_path, "new_template_reader_under_test")
        ddb, s3 = build_world(old)
        out = count(ddb, s3, TABLE, BUCKET, old, new)
        problems = []
        for key, want in EXPECTED.items():
            if out.get(key) != want:
                problems.append("%s: expected %r got %r" % (key, want, out.get(key)))
        for tenant, want in EXPECTED_TENANT.items():
            got = out["by_tenant"].get(tenant, {})
            for key, value in want.items():
                have = got.get("turned_back_with_a_report", {}).get(key) if key in ("with", "without") else got.get(key)
                if have != value:
                    problems.append("by_tenant[%s].%s: expected %r got %r" % (tenant, key, value, have))
        if sorted(out["by_tenant"]) != ["firm-a", "firm-b"]:
            problems.append("by_tenant keys")
        if len(ddb.rows) != 11 * 4 + 6 * 2:
            problems.append("the fake table holds %d rows" % len(ddb.rows))
        if out["template_inputs"] != out["read_the_same"] + out["read_differently"] + sum(out["unreadable"].values()):
            problems.append("template inputs are not read-the-same + read-differently + unreadable")
        text = json.dumps(out, sort_keys=True)
        for banned in ("portfolio_", "UP-", "REQ-", "ART-", ".csv", ".xlsx", "ZZ", "QQ-", "synthetic", "Total,"):
            if banned in text:
                problems.append("the output carries %r" % banned)
        if set(ddb.log) - {"get_item", "scan", "query"} or set(s3.log) - {"get_object"}:
            problems.append("a call other than get-item, scan, query, get-object reached a fake")
        denied = FakeDdb()
        denied.deny_scan = True
        try:
            count(denied, FakeS3(), TABLE, BUCKET, old, new)
            problems.append("a denied scan did not stop the count")
        except ScanFailed as exc:
            if exc.code != "AccessDeniedException":
                problems.append("a denied scan printed code %r" % exc.code)
        for line in problems:
            print("SELF-TEST FAIL: " + line, file=sys.stderr)
        if problems:
            return 1
        print("self-test: %d synthetic inputs, %d fake rows, scan pages %d, queries %d, objects read %d"
              % (11, len(ddb.rows), ddb.log["scan"], ddb.log["query"], s3.log["get_object"]), file=sys.stderr)
        print("SELF-TEST OK", file=sys.stderr)
        print(json.dumps(out, sort_keys=True))
        return 0
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--table")
    parser.add_argument("--bucket")
    parser.add_argument("--region")
    parser.add_argument("--new-reader", help="a file holding the new template reader (git show %s:%s)" % (NEW_READER_COMMIT, READER_REL))
    parser.add_argument("--old-reader", help="default: the running reader of the checkout this runs in")
    parser.add_argument("--out", help="also write the one JSON object to this file")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root(os.getcwd())
    if args.self_test:
        return self_test(root)
    if not (args.table and args.bucket and args.region and args.new_reader):
        parser.error("--table, --bucket, --region and --new-reader are required")
    old_path = args.old_reader or os.path.join(root, *READER_REL.split("/"))
    print("old reader sha256 %s; new reader sha256 %s" % (file_sha256(old_path), file_sha256(args.new_reader)), file=sys.stderr)
    old, new = load_reader(old_path, "old_template_reader_loaded"), load_reader(args.new_reader, "new_template_reader_loaded")
    import boto3  # only a live run needs it
    ddb, s3 = boto3.client("dynamodb", region_name=args.region), boto3.client("s3", region_name=args.region)
    try:
        out = count(ddb, s3, args.table, args.bucket, old, new)
    except ScanFailed as exc:
        print("SCAN_FAILED %s" % exc.code, file=sys.stderr)
        return 3
    line = json.dumps(out, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(line + "\n")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
