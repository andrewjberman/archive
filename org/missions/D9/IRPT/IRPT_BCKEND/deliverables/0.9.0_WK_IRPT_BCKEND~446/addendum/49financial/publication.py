"""Version-pinned holdings artifacts and one conditional publication index.

Addresses come from the canonical builder in the server's firm home. An index
contains one accepted manifest per business date; immutable prior revisions stay
in history. No artifact is discoverable through this index until every write has
been read back by its exact S3 version and verified. Caller supplies an index
captured before building, so a concurrent publication cannot be overwritten.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import re
from urllib.parse import urlsplit

MAX_JSON_BYTES = 4 * 1024 * 1024
MAX_INDEX_BYTES = 1024 * 1024
MAX_GOLD_BYTES = 64 * 1024 * 1024
MAX_SELECTED_READ_BYTES = 64 * 1024 * 1024
MAX_PUBLICATION_ACCOUNTS = 25000
MAX_PUBLICATION_PARTS = 256
MAX_SELECTED_PART_READS = 64


class PublicationRefused(RuntimeError):
    pass


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(body):
    return hashlib.sha256(body).hexdigest()


def _version(value):
    if not isinstance(value, str) or not value or value == "null":
        raise PublicationRefused("versioned storage is required")
    return value


def _missing(exc):
    response = getattr(exc, "response", {})
    return str(response.get("Error", {}).get("Code")) in ("NoSuchKey", "404")


def _date(value):
    if not isinstance(value, str) or dt.date.fromisoformat(value).isoformat() != value:
        raise PublicationRefused("ISO business date required")
    return value


def _account_groups(nodes):
    """Group complete account trees; refuse duplicate, cyclic or orphan graphs."""
    by_id = {n["node_id"]: n for n in nodes}
    if len(by_id) != len(nodes):
        raise PublicationRefused("duplicate node identity in publication")
    roots, groups = {}, {}
    for node_id in by_id:
        trail, seen, current = [], set(), node_id
        while current not in roots:
            if current in seen or current not in by_id:
                raise PublicationRefused("cyclic or orphan publication tree")
            seen.add(current)
            trail.append(current)
            parent = by_id[current].get("parent_node_id")
            if parent is None:
                if by_id[current].get("node_kind") != "ACCOUNT":
                    raise PublicationRefused("publication root is not an account")
                roots[current] = current
                break
            current = parent
        for member in trail:
            roots[member] = roots[current]
    for node in nodes:
        groups.setdefault(roots[node["node_id"]], []).append(node)
    return groups


def _platinum_plan(snapshot, revision):
    header = {key: value for key, value in snapshot.items() if key != "nodes"}
    header_body = canonical_bytes(header)
    if len(header_body) > MAX_JSON_BYTES:
        raise PublicationRefused("Platinum header exceeds bound")
    groups = _account_groups(snapshot["nodes"])
    if len(groups) > MAX_PUBLICATION_ACCOUNTS:
        raise PublicationRefused("publication account count exceeds bound")
    if set(groups) != set(snapshot["scope"]["account_ids"]):
        raise PublicationRefused("publication account population differs from header")
    parts, members, nodes = [], [], []
    target = min(1024 * 1024, MAX_JSON_BYTES)

    def part_body(rows):
        return canonical_bytes({"firm_id": snapshot["scope"]["firm_id"],
                                "revision": revision, "nodes": rows})

    overhead = len(part_body([]))
    part_size = overhead
    for account, group in sorted(groups.items()):
        group_size = len(canonical_bytes(group)) - 2  # brackets supplied by part_body
        candidate_size = part_size + group_size + bool(nodes)
        if nodes and candidate_size > target:
            parts.append((members, part_body(nodes)))
            members, nodes = [], []
            part_size = overhead
        if overhead + group_size > MAX_JSON_BYTES:
            raise PublicationRefused("one complete account tree exceeds Platinum bound")
        part_size += group_size + bool(nodes)
        members.append(account)
        nodes.extend(group)
    if nodes:
        parts.append((members, part_body(nodes)))
    if len(parts) > MAX_PUBLICATION_PARTS:
        raise PublicationRefused("publication part count exceeds bound")
    return header_body, parts


class HoldingsPublication:
    def __init__(self, s3, firm, *, address_builder=None, qa=False):
        from opal_naming import address, lookup
        firms = {lookup("49financial")["long"], lookup("cottonwood")["long"],
                 lookup("inflection")["long"]}
        if firm not in firms:
            raise PublicationRefused("canonical private firm required")
        if address_builder is None:
            address_builder = address
        self.s3, self.firm = s3, firm
        self.source = lookup("irpt")["long"]
        self.address_builder = address_builder
        self.table = "holdings_qa" if qa else "holdings"

    def location(self, tier, partition, object_name):
        url = urlsplit(self.address_builder(self.source, self.firm, tier,
                                            self.table, partition, object_name))
        if url.scheme != "s3" or not url.netloc or not url.path:
            raise PublicationRefused("canonical builder returned no S3 address")
        return url.netloc, url.path.lstrip("/")

    def begin(self):
        """Capture current publication before reading/building the source snapshot."""
        bucket, key = self.location("platinum", "current", "manifest.json")
        try:
            response = self.s3.get_object(Bucket=bucket, Key=key)
        except Exception as exc:
            if _missing(exc):
                return {"etag": None, "document": None}
            raise PublicationRefused("publication index unavailable") from exc
        version = _version(response.get("VersionId"))
        body = response["Body"].read(MAX_INDEX_BYTES + 1)
        if len(body) > MAX_INDEX_BYTES:
            raise PublicationRefused("publication index exceeds bound")
        doc = json.loads(body)
        self._validate_index(doc)
        if not response.get("ETag"):
            raise PublicationRefused("publication index identity invalid")
        return {"etag": response["ETag"], "document": doc,
                "reference": {"bucket": bucket, "key": key, "version_id": version,
                              "sha256": digest(body), "byte_length": len(body)}}

    def _validate_index(self, doc):
        if (not isinstance(doc, dict)
                or doc.get("schema_version") != "irpt-holdings-index-v1"
                or doc.get("firm_id") != self.firm
                or not isinstance(doc.get("dates"), dict) or not doc["dates"]):
            raise PublicationRefused("publication index identity invalid")
        for date, row in doc["dates"].items():
            _date(date)
            if (not isinstance(row, dict)
                    or not re.fullmatch(r"[0-9a-f]{64}", str(row.get("revision", "")))
                    or not isinstance(row.get("manifest"), dict)):
                raise PublicationRefused("publication index row invalid")
        if doc.get("latest_date") != max(doc["dates"]):
            raise PublicationRefused("publication index latest date invalid")

    def validate_reference(self, ref, *, expected_location, max_bytes):
        """Validate inventory metadata without fetching unselected private bytes."""
        if not isinstance(ref, dict):
            raise PublicationRefused("immutable object reference required")
        bucket, key = expected_location
        if (ref.get("bucket") != bucket or ref.get("key") != key
                or not isinstance(ref.get("sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", ref["sha256"])
                or type(ref.get("byte_length")) is not int
                or not 0 < ref["byte_length"] <= max_bytes):
            raise PublicationRefused("object reference outside expected identity or bound")
        return _version(ref.get("version_id"))

    def read_exact(self, ref, *, expected_location, max_bytes):
        version = self.validate_reference(ref, expected_location=expected_location, max_bytes=max_bytes)
        bucket, key = expected_location
        response = self.s3.get_object(Bucket=bucket, Key=key, VersionId=version)
        if response.get("VersionId") != version:
            raise PublicationRefused("object version changed")
        body = response["Body"].read(max_bytes + 1)
        if len(body) != ref["byte_length"] or digest(body) != ref["sha256"]:
            raise PublicationRefused("object bytes differ from accepted reference")
        return body

    def _put_verified(self, location, body, content_type):
        bucket, key = location
        try:
            response = self.s3.put_object(Bucket=bucket, Key=key, Body=body,
                                          ContentType=content_type, IfNoneMatch="*")
            version = _version(response.get("VersionId"))
        except Exception as exc:
            code = str(getattr(exc, "response", {}).get("Error", {}).get("Code"))
            if code not in ("PreconditionFailed", "412"):
                raise
            # Same-byte retry may reuse a retained immutable object; a digest
            # collision, substituted body or missing version refuses publication.
            response = self.s3.get_object(Bucket=bucket, Key=key)
            version = _version(response.get("VersionId"))
        ref = {"bucket": bucket, "key": key, "version_id": version,
               "sha256": digest(body), "byte_length": len(body)}
        self.read_exact(ref, expected_location=location, max_bytes=len(body))
        return ref

    def publish(self, snapshot, gold_bytes, *, business_date, expected, validate, source_objects=None,
                # BEGIN ABSENT-AT-SOURCE-B
                absent_at_source=None
                # END ABSENT-AT-SOURCE-B
                ):
        """Publish only after validation and artifact readback succeed.

        Index readback follows the conditional write. A failure returns no
        receipt but the write may have succeeded: this is an unconfirmed outcome.
        Reconcile the exact index version before retrying; no rollback or blind
        retry is implied.
        """
        _date(business_date)
        if (snapshot.get("scope", {}).get("firm_id") != self.firm
                or validate(snapshot) is not True):
            raise PublicationRefused("snapshot validation/firm/date refused")
        if len(snapshot.get("scope", {}).get("account_ids", [])) > MAX_PUBLICATION_ACCOUNTS:
            raise PublicationRefused("publication account count exceeds bound")
        if source_objects is not None:
            if not isinstance(source_objects, list) or not source_objects:
                raise PublicationRefused("source object receipts required")
            source_digest = digest(canonical_bytes(source_objects))
            if not any(row.get("source") == "irpt-source-objects"
                       and row.get("revision") == source_digest
                       for row in snapshot.get("source_set_revision", [])):
                raise PublicationRefused("source receipts not bound to snapshot revision")
        prior = expected.get("document")
        if prior is not None:
            self._validate_index(prior)
            if not expected.get("etag"):
                raise PublicationRefused("captured index ETag required")
        elif expected.get("etag") is not None:
            raise PublicationRefused("absent index cannot have an ETag")
        if not isinstance(gold_bytes, bytes) or not 0 < len(gold_bytes) <= MAX_GOLD_BYTES:
            raise PublicationRefused("bounded Gold Parquet required")
        # Publisher-only dependency: the Lambda reader never imports pyarrow.
        # Verify actual Parquet and all node fields before accepting either tier.
        try:
            import pyarrow.parquet as pq
            rows = pq.read_table(io.BytesIO(gold_bytes), columns=["node_json"]).to_pylist()
            nodes = [json.loads(row["node_json"]) for row in rows]
            if canonical_bytes(nodes) != canonical_bytes(snapshot["nodes"]):
                raise ValueError("Gold and Platinum nodes differ")
        except Exception as exc:
            raise PublicationRefused("Gold Parquet does not preserve snapshot nodes") from exc
        body = canonical_bytes(snapshot)
        revision = digest(body)
        plan = _platinum_plan(snapshot, revision) if len(body) > MAX_JSON_BYTES else None
        partition = "date=" + business_date
        gold = self._put_verified(self.location("gold", partition, revision + ".parquet"),
                                  gold_bytes, "application/vnd.apache.parquet")
        manifest = {"schema_version": "irpt-holdings-manifest-v1", "firm_id": self.firm,
                    "business_date": business_date, "revision": revision,
                    "gold": gold,
                    "source_set_revision": snapshot.get("source_set_revision"),
                    "clocks": snapshot.get("clocks")}
        if plan is None:
            manifest["platinum"] = self._put_verified(
                self.location("platinum", partition, revision + ".json"), body, "application/json")
        else:
            manifest["schema_version"] = "irpt-holdings-manifest-v2"
            header, parts = plan
            manifest["platinum_header"] = self._put_verified(
                self.location("platinum", partition, revision + ".header.json"), header, "application/json")
            manifest["partitions"] = []
            for number, (accounts, part_body) in enumerate(parts):
                ref = self._put_verified(self.location(
                    "platinum", partition, revision + ".part%05d.json" % number), part_body, "application/json")
                manifest["partitions"].append({"account_ids": accounts, "object": ref})
        if source_objects is not None:
            manifest["source_objects"] = source_objects
        # BEGIN ABSENT-AT-SOURCE-B
        if isinstance(absent_at_source, list) and absent_at_source:
            manifest["absent_at_source"] = absent_at_source
        # END ABSENT-AT-SOURCE-B
        manifest_body = canonical_bytes(manifest)
        if len(manifest_body) > MAX_JSON_BYTES:
            raise PublicationRefused("accepted manifest exceeds bound")
        manifest_ref = self._put_verified(
            self.location("platinum", partition, revision + ".manifest.json"),
            manifest_body, "application/json")
        dates = dict(prior["dates"]) if prior is not None else {}
        dates[business_date] = {"revision": revision, "manifest": manifest_ref}
        index = {"schema_version": "irpt-holdings-index-v1", "firm_id": self.firm,
                 "latest_date": max(dates), "dates": dates}
        index_body = canonical_bytes(index)
        if len(index_body) > MAX_INDEX_BYTES:
            raise PublicationRefused("publication index exceeds bound")
        bucket, key = self.location("platinum", "current", "manifest.json")
        condition = {"IfMatch": expected["etag"]} if expected.get("etag") else {"IfNoneMatch": "*"}
        result = self.s3.put_object(Bucket=bucket, Key=key, Body=index_body,
                                    ContentType="application/json", **condition)
        index_ref = {"bucket": bucket, "key": key,
                     "version_id": _version(result.get("VersionId")),
                     "sha256": digest(index_body), "byte_length": len(index_body)}
        # A later publisher can advance current immediately. Verify this write's
        # exact version, never whichever index happens to be current at readback.
        self.read_exact(index_ref, expected_location=(bucket, key), max_bytes=MAX_INDEX_BYTES)
        return {"revision": revision, "manifest": manifest_ref,
                "index_version": index_ref["version_id"], "index_sha256": digest(index_body),
                "acceptance_receipt": self._acceptance_receipt(index_ref, index, business_date)}

    def load(self, *, as_of=None, account_ids=None):
        document, manifest, _ = self.capture(as_of=as_of, account_ids=account_ids)
        return document, manifest

    def _acceptance_receipt(self, index_ref, index, date):
        row = index["dates"].get(date)
        if not isinstance(row, dict) or set(row) != {"revision", "manifest"}:
            raise PublicationRefused("no accepted holdings revision for date")
        receipt = {"schema_version": "irpt-holdings-acceptance-v1", "firm_id": self.firm,
                   "business_date": date, "index": index_ref, "date_row": row}
        # No alias to the mutable begin()/manifest return values.
        return json.loads(canonical_bytes(receipt))

    def capture(self, *, as_of=None, account_ids=None):
        """Return (document, manifest, private acceptance receipt) from observed index.

        This proves publication history, NOT actual-custody economics or caller
        authorization. P must store this receipt inside its trusted binding and
        independently authorize the exact selected accounts on every replay.
        """
        try:
            observed = self.begin()
            index = observed["document"]
            if index is None:
                raise PublicationRefused("no accepted holdings publication")
            date = _date(as_of) if as_of is not None else index["latest_date"]
            receipt = self._acceptance_receipt(observed["reference"], index, date)
            document, manifest = self._load_accepted_row(date, receipt["date_row"], account_ids)
            return document, manifest, receipt
        except PublicationRefused:
            raise
        except Exception as exc:
            raise PublicationRefused("accepted publication capture unavailable or invalid") from exc

    def load_pinned(self, receipt, *, account_ids=None):
        """Replay a server-bound receipt; never read the current index as a fallback.

        The full original snapshot identity is receipt.date_row.revision even
        when returned nodes are selected partitions or a wrapper decorates them.
        A standalone immutable manifest is insufficient evidence of acceptance.
        """
        try:
            if (not isinstance(receipt, dict)
                    or set(receipt) != {"schema_version", "firm_id", "business_date", "index", "date_row"}
                    or receipt["schema_version"] != "irpt-holdings-acceptance-v1"
                    or receipt["firm_id"] != self.firm):
                raise PublicationRefused("acceptance receipt identity invalid")
            date = _date(receipt["business_date"])
            row = receipt["date_row"]
            if not isinstance(row, dict) or set(row) != {"revision", "manifest"}:
                raise PublicationRefused("acceptance receipt date row invalid")
            # Strict private protocol: extra reference fields cannot carry a
            # second, unvalidated identity inside the trusted binding.
            for ref in (receipt["index"], row["manifest"]):
                if not isinstance(ref, dict) or set(ref) != {
                        "bucket", "key", "version_id", "sha256", "byte_length"}:
                    raise PublicationRefused("acceptance receipt reference invalid")
            body = self.read_exact(receipt["index"], expected_location=self.location(
                "platinum", "current", "manifest.json"), max_bytes=MAX_INDEX_BYTES)
            index = json.loads(body)
            self._validate_index(index)
            if canonical_bytes(index["dates"].get(date)) != canonical_bytes(row):
                raise PublicationRefused("index did not accept this exact date row")
            return self._load_accepted_row(date, row, account_ids)
        except PublicationRefused:
            raise
        except Exception as exc:
            raise PublicationRefused("pinned publication unavailable or invalid") from exc

    def _load_accepted_row(self, date, row, account_ids):
        revision, partition = row["revision"], "date=" + date
        manifest = json.loads(self.read_exact(row["manifest"], expected_location=self.location(
            "platinum", partition, revision + ".manifest.json"), max_bytes=MAX_JSON_BYTES))
        if (manifest.get("firm_id") != self.firm or manifest.get("business_date") != date
                or manifest.get("revision") != revision
                or manifest.get("schema_version") not in ("irpt-holdings-manifest-v1", "irpt-holdings-manifest-v2")):
            raise PublicationRefused("accepted manifest identity invalid")
        self.validate_reference(manifest.get("gold"), expected_location=self.location(
            "gold", partition, revision + ".parquet"), max_bytes=MAX_GOLD_BYTES)
        if manifest["schema_version"] == "irpt-holdings-manifest-v1":
            body = self.read_exact(manifest["platinum"], expected_location=self.location(
                "platinum", partition, revision + ".json"), max_bytes=MAX_JSON_BYTES)
            if digest(body) != revision:
                raise PublicationRefused("accepted snapshot revision mismatch")
            document = json.loads(body)
            if account_ids is not None:
                selected = set(account_ids)
                members = set(document.get("scope", {}).get("account_ids", []))
                groups = _account_groups(document["nodes"])
                if not selected or not selected <= members or set(groups) != members:
                    raise PublicationRefused("selected accounts absent from accepted publication")
        else:
            document = self._load_parts(manifest, partition, revision, account_ids)
        if (document.get("scope", {}).get("firm_id") != self.firm
                or document.get("source_set_revision") != manifest.get("source_set_revision")
                or document.get("clocks") != manifest.get("clocks")):
            raise PublicationRefused("accepted snapshot and manifest disagree")
        if len(document.get("scope", {}).get("account_ids", [])) > MAX_PUBLICATION_ACCOUNTS:
            raise PublicationRefused("publication account count exceeds bound")
        return document, manifest

    def _load_parts(self, manifest, partition, revision, account_ids):
        header = self.read_exact(manifest["platinum_header"], expected_location=self.location(
            "platinum", partition, revision + ".header.json"), max_bytes=MAX_JSON_BYTES)
        document = json.loads(header)
        partitions = manifest.get("partitions")
        if (not isinstance(partitions, list) or not partitions
                or len(partitions) > MAX_PUBLICATION_PARTS):
            raise PublicationRefused("accepted partition count missing or exceeds bound")
        members = set()
        for number, part in enumerate(partitions):
            if not isinstance(part, dict):
                raise PublicationRefused("accepted partition entry invalid")
            self.validate_reference(part.get("object"), expected_location=self.location(
                "platinum", partition, revision + ".part%05d.json" % number), max_bytes=MAX_JSON_BYTES)
            ids = part.get("account_ids")
            if (not isinstance(ids, list) or not ids or any(not isinstance(x, str) for x in ids)
                    or len(set(ids)) != len(ids) or members.intersection(ids)):
                raise PublicationRefused("accepted partition membership ambiguous")
            members.update(ids)
            if len(members) > MAX_PUBLICATION_ACCOUNTS:
                raise PublicationRefused("publication account count exceeds bound")
        if members != set(document.get("scope", {}).get("account_ids", [])):
            raise PublicationRefused("accepted partition census differs from header")
        selected = members if account_ids is None else set(account_ids)
        if not selected or not selected <= members:
            raise PublicationRefused("selected accounts absent from accepted publication")
        needed = [part for part in partitions if selected.intersection(part["account_ids"])]
        if len(needed) > MAX_SELECTED_PART_READS:
            raise PublicationRefused("selected publication request count exceeds bound")
        nodes, read_bytes = [], len(header)
        for number, part in enumerate(partitions):
            if not selected.intersection(part["account_ids"]):
                continue
            declared_size = part["object"].get("byte_length")
            if type(declared_size) is not int or read_bytes + declared_size > MAX_SELECTED_READ_BYTES:
                raise PublicationRefused("selected publication retrieval exceeds bound")
            body = self.read_exact(part["object"], expected_location=self.location(
                "platinum", partition, revision + ".part%05d.json" % number), max_bytes=MAX_JSON_BYTES)
            read_bytes += len(body)
            piece = json.loads(body)
            if piece.get("firm_id") != self.firm or piece.get("revision") != revision:
                raise PublicationRefused("accepted partition identity differs")
            groups = _account_groups(piece["nodes"])
            if set(groups) != set(part["account_ids"]):
                raise PublicationRefused("accepted partition account census differs")
            for account, group in groups.items():
                if account in selected:
                    nodes.extend(group)
        # Header retains the full source census until the guarded projector
        # re-derives the selected totals. No partially loaded document is served.
        document["nodes"] = nodes
        if len(canonical_bytes(document)) > MAX_JSON_BYTES:
            raise PublicationRefused("selected holdings exceed bounded JSON response")
        return document
