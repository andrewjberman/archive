"""IB-s-11 fixture generator -- scrub the captured September 10 performance bodies.

NOT Lambda runtime code and NOT part of the deployment package. It reads the raw vendor
bodies the CRO's probe wrote (`probe_performance.py --live ...`, per the evidence file's
own `meta.raw_storage`) and writes the SCRUBBED fixtures this cell commits under
infra/aws/lambda/investor-reporting/performance/fixtures/.

WHY IT EXISTS: the evidence file
docs/briefs/sources/INVESTOR_REPORTING_PERFORMANCE_EVIDENCE_20260910.json carries
RECEIPTS, FIELD SHAPES and VALIDATION AGGREGATES -- it carries no response bodies, and
`probe_performance.py` reads three HAR captures that are outside the repository. So the
fixture bytes are derived here, ONCE, and the derivation is tied to the evidence by
sha256: every source body's digest is asserted against the matching
`http_receipts[].response_sha256` before a single byte is copied.

WHAT IS SCRUBBED (bound 6 -- a recorded fixture is scrubbed before it is committed):
every client identifier -- account names, account numbers, external ids, Black Diamond
account/level ids, Orion household and account names, Orion group entity ids, the Orion
session id. Every NUMBER that carries economic meaning is preserved EXACTLY, because the
arithmetic ties (percent-vs-factor, linked factors vs summary, the value-shortcut
mismatch, the hierarchy sum) ARE the evidence and a perturbed number proves nothing.
Black Diamond SEGMENT names are BD's standard asset classification, not client identity,
and are kept.

Usage (offline, no network):
    python make_perf_fixtures.py --source <dir with *_live.bin> --out <fixtures dir>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[7]
EVIDENCE = REPO / "docs/briefs/sources/INVESTOR_REPORTING_PERFORMANCE_EVIDENCE_20260910.json"

# label -> fixture basename. bd_session_refresh has no saved body BY DESIGN (the probe
# never writes or digests a session-token response), so it is not a fixture; the handler
# arm that consumes it reads the receipt only.
BODY_LABELS = {
    "bd_114": "bd_401_period",
    "bd_117": "bd_401_series",
    "orion_252": "orion_captured_scope",
    "bd_refreshed_period": "bd_period",
    "bd_refreshed_series": "bd_series",
    "orion_daily": "orion_daily",
    "orion_value_check": "orion_value_check",
}
# orion_compact (5,290,686 bytes, the cumulative=true experiment) is NOT committed: its
# 4,278-point-per-92-date shape is exactly the redundancy the compact form avoids, and
# the counts that prove it are already in the evidence file's `validation` block.
NOT_COMMITTED = {"orion_compact", "bd_session_refresh"}

# String-valued keys whose value is a client identifier.
STRING_ID_KEYS = {"accountName", "accountNumber", "externalId", "sessionId"}
# Integer-valued keys whose value is a vendor-side client identifier at EVERY level.
INT_ID_KEYS = {"accountId", "groupEntityId"}
# Levels whose ids identify a CLIENT. A Segment/Class/Asset levelId is Black Diamond's
# own classification id (`Asset.CapSegmentId`), shared across every client of the tenant,
# so scrubbing it would destroy a non-identifying join key for no privacy gain.
CLIENT_LEVELS = ("Account", "Portfolio")


class Pseudonymiser:
    """Deterministic, collision-free, and reversible only with the original input."""

    def __init__(self) -> None:
        self.ints: dict[int, int] = {}
        self.strings: dict[str, str] = {}
        self.removed = 0

    def integer(self, value: int) -> int:
        if value not in self.ints:
            self.ints[value] = 900000001 + len(self.ints)
        self.removed += 1
        return self.ints[value]

    def string(self, key: str, value: str) -> str:
        token = key + "|" + value
        if token not in self.strings:
            self.strings[token] = "SCRUBBED-%s-%03d" % (key.upper(), len(self.strings) + 1)
        self.removed += 1
        return self.strings[token]


def scrub(node, pseudo: Pseudonymiser, parent_level: str = ""):
    """Recursive scrub. `parent_level` carries the enclosing BD descriptor level so an
    Account descriptor's name is removed while a Segment descriptor's name is kept."""
    if isinstance(node, dict):
        level = node.get("level") or node.get("descriptor", {}).get("level") or parent_level
        out = {}
        for key, value in node.items():
            if key in STRING_ID_KEYS and isinstance(value, str):
                out[key] = pseudo.string(key, value)
            elif key in INT_ID_KEYS and isinstance(value, int):
                out[key] = pseudo.integer(value)
            elif key == "levelId" and isinstance(value, int):
                out[key] = pseudo.integer(value) if level in CLIENT_LEVELS else value
            elif key == "levelKey" and isinstance(value, str):
                if level not in CLIENT_LEVELS:
                    out[key] = value
                else:
                    out[key] = str(pseudo.integer(int(value))) if value.isdigit() else pseudo.string(key, value)
            elif key == "name" and isinstance(value, str) and level in CLIENT_LEVELS + ("",):
                # BD Account descriptors and Orion calculated-group names.
                out[key] = pseudo.string("name", value)
            elif key == "number" and isinstance(value, str):
                out[key] = pseudo.string(key, value)
            elif key == "accounts" and isinstance(value, list) and all(isinstance(v, int) for v in value):
                out[key] = [pseudo.integer(v) for v in value]
            elif key == "levelFilters" and isinstance(value, list):
                out[key] = [scrub(v, pseudo, level) for v in value]
            else:
                out[key] = scrub(value, pseudo, level)
        # A BD Account levelFilter targets the account id; a Segment levelFilter targets
        # a classification id, which is not client identity.
        if str(out.get("target", "")).startswith("Account") and isinstance(out.get("value"), str):
            out["value"] = pseudo.string("levelFilterValue", str(node.get("value")))
        return out
    if isinstance(node, list):
        return [scrub(v, pseudo, parent_level) for v in node]
    return node


def leaked(original, scrubbed, pseudo: Pseudonymiser) -> list:
    """Falsifier: assert no original identifier survives anywhere in the scrubbed text."""
    text = json.dumps(scrubbed)
    hits = []
    for token, _ in pseudo.strings.items():
        raw = token.split("|", 1)[1]
        if raw and raw in text:
            hits.append("string:" + raw[:4] + "...")
    for raw_int in pseudo.ints:
        if ('"%d"' % raw_int) in text or (": %d," % raw_int) in text or (", %d," % raw_int) in text:
            hits.append("int:%d" % raw_int)
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", required=True, type=pathlib.Path)
    ap.add_argument("--out", required=True, type=pathlib.Path)
    args = ap.parse_args()

    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    receipts = {r["label"]: r for r in evidence["http_receipts"]}
    args.out.mkdir(parents=True, exist_ok=True)

    manifest = {
        "_generated_by": "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~4/make_perf_fixtures.py",
        "_cell": "IB-s-11",
        "_evidence": "docs/briefs/sources/INVESTOR_REPORTING_PERFORMANCE_EVIDENCE_20260910.json",
        "_evidence_sha256": hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
        "_claim": "measured -- every source body's sha256 was asserted equal to the evidence receipt's response_sha256 before scrubbing",
        "_scrub": "client identifiers replaced (account name/number/externalId, BD account+level ids, Orion group names and groupEntityId, sessionId); every economic number preserved exactly",
        "_not_committed": sorted(NOT_COMMITTED),
        "receipts": [],
    }
    total = 0
    for label, receipt in receipts.items():
        if label in NOT_COMMITTED:
            manifest["receipts"].append({
                "label": label, "status": receipt["status"], "body_committed": False,
                "reason": ("session-token response is never saved or digested by the probe"
                           if label == "bd_session_refresh"
                           else "cumulative=true experiment, 5,290,686 bytes; its counts are in the evidence validation block"),
            })
            continue
        raw = (args.source / (label + "_live.bin")).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != receipt.get("response_sha256"):
            print("ERROR: %s sha256 %s != evidence %s" % (label, digest, receipt.get("response_sha256")))
            return 1
        entry = {
            "label": label, "status": receipt["status"], "method": receipt["method"],
            "path": receipt["path"], "response_bytes": receipt["response_bytes"],
            "source_response_sha256": digest, "body_committed": bool(raw),
        }
        if not raw:
            entry["fixture"] = None
            entry["reason"] = "HTTP 401 with a zero-byte body -- the absent-with-reason arm"
        else:
            pseudo = Pseudonymiser()
            body = json.loads(raw.decode("utf-8-sig"))
            clean = scrub(body, pseudo)
            hits = leaked(body, clean, pseudo)
            if hits:
                print("ERROR: %s leaked %d identifier(s): %s" % (label, len(hits), hits[:3]))
                return 1
            name = BODY_LABELS[label] + ".json"
            (args.out / name).write_text(json.dumps(clean, indent=1, sort_keys=False), encoding="utf-8")
            entry["fixture"] = name
            entry["identifiers_replaced"] = pseudo.removed
            entry["fixture_sha256"] = hashlib.sha256((args.out / name).read_bytes()).hexdigest()
            total += 1
        manifest["receipts"].append(entry)

    manifest["_denominator"] = "%d of %d evidence receipts; %d bodies committed" % (
        len(manifest["receipts"]), len(receipts), total)
    (args.out / "FIXTURE_MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print("OK: %s" % manifest["_denominator"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
