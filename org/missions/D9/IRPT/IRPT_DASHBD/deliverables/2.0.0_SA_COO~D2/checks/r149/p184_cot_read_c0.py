"""IRPT_DASHBD round 150, workstream COTREAD (issuer 2.0.0_SA_COO~D2) -- DB-b-318, C0 of the Cottonwood Performance read path (CTO ruling A, msg 10134, `RULING_COTTONWOOD_READ_PATH_OPTION_A_20261017.md` @6bfcbcf2cc): a READ-ONLY trace by the
one IRPT CloudOps lane `0.7.0_AE_CloudOps~IB2`. It writes nothing. It answers three open items before any code is cut: what the live 49F read function says today to a synthetic staff request for the firm cottonwood (and
to a 49F control), whether the Cottonwood ownership-map and directory objects exist, and where the API authorizer keeps its firm handling. WORLD (read only); the record is the applier's; the checker re-reads the world.

  DBC184-1-AC1  the record: probes by label (statuses and reason codes only), the object existence flags, the authorizer's identity, no write, no id
  DBC184-2-AC1  FRESH live reads: the two ownership-map keys and the directory pointer exist as the record says, and the 49F read function is unchanged (code hash and bucket map equal the record's)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_184")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_READ_C0_RECORD.json"
FUNCTION = "irpt-49f-reporting-read-lambda"
LABELS = ["cottonwood-client-1-manifest", "cottonwood-client-1-series", "control-49f-manifest"]
OWN_KEYS = {"legacy": "platinum/cottonwood/ownership_map.json", "canonical": "advi/cottonwood/platinum/cottonwood/ownership_map.json"}
OWN_BUCKET = "opal-data-cottonwood"
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("request_id", "code_sha256_before", "code_sha256_after", "invoked_utc", "authorizer_id")
REASON = re.compile(r"^[A-Z][A-Z0-9_]{2,40}$")


def check_record(rec):
    exp = {"claim", "applier", "no_write", "probes", "ownership_map", "directory", "authorizer", "function", "notes", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured" and rec["applier"] == APPLIER and rec["no_write"] is True, "claim measured, the applier named and no_write true")
    pr = rec["probes"]
    need(isinstance(pr, list) and [p.get("label") for p in pr] == LABELS, "probes must be exactly the three labels in order: %s" % LABELS)
    for p in pr:
        need(set(p) == {"label", "method", "status", "reason_code", "content_encoding", "invoked_utc", "request_id"}, "probe keys: %s" % p.get("label"))
        need(p["method"] == "lambda-invoke" and is_int(p["status"]) and 100 <= p["status"] <= 599 and H.UTC.match(str(p["invoked_utc"])) and nes(p["request_id"]), "probe %s: lambda-invoke, a status, a UTC time, a request id" % p["label"])
        need(p["reason_code"] is None or REASON.match(str(p["reason_code"])), "probe %s: reason_code a token or null, never a sentence" % p["label"])
    need(pr[2]["status"] == 200, "the 49F control must answer 200 (the live function works for its own firm)")
    need(pr[0]["reason_code"] is not None and pr[1]["reason_code"] is not None, "the two cottonwood probes must carry the refusal reason token (a refusal envelope has no statusCode, so the status alone does not say refused)")
    om = rec["ownership_map"]
    need(isinstance(om, dict) and set(om) == {"bucket", "legacy_key_exists", "canonical_key_exists"} and om["bucket"] == OWN_BUCKET and isinstance(om["legacy_key_exists"], bool) and isinstance(om["canonical_key_exists"], bool), "ownership_map: the bucket and two booleans")
    dr = rec["directory"]
    need(isinstance(dr, dict) and set(dr) == {"latest_json_exists", "entry_count"} and isinstance(dr["latest_json_exists"], bool) and is_int(dr["entry_count"]) and dr["entry_count"] >= 0, "directory: latest_json_exists and an entry count")
    au = rec["authorizer"]
    need(isinstance(au, dict) and set(au) == {"authorizer_id", "type", "function_name", "firm_handling_location", "lists_firms"}, "authorizer keys")
    need(nes(au["authorizer_id"]) and nes(au["type"]) and nes(au["function_name"]) and nes(au["firm_handling_location"]) and isinstance(au["lists_firms"], bool), "authorizer: identity, type, function, where the firm handling lives (a repo path or 'none'), and a boolean")
    fn = rec["function"]
    need(isinstance(fn, dict) and set(fn) == {"name", "code_sha256_before", "code_sha256_after", "directory_bucket_map"} and fn["name"] == FUNCTION and fn["code_sha256_before"] == fn["code_sha256_after"] and nes(fn["code_sha256_after"]), "function: the 49F read function, code hash equal before and after")
    need(isinstance(fn["directory_bucket_map"], list) and all(isinstance(x, str) for x in fn["directory_bucket_map"]) and "cottonwood" not in fn["directory_bucket_map"], "function.directory_bucket_map: the firm tokens it maps (a list), without cottonwood")
    need(isinstance(rec["notes"], str) and 20 <= len(rec["notes"]) <= 1800 and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "notes (words, 20 to 1800 characters) and the reads block")
    return True


def digit_runs(rec):
    out = []

    def walk(x, key=""):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, str) and key not in H.DIGIT_OK_KEYS and re.search(r"\d{8,}", x):
            out.append((key, x[:20]))
    walk(rec)
    return out


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    check_record(rec)
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    if cid == "DBC184-1-AC1":
        print("OK: three labelled probes (statuses and reason codes only, the 49F control 200), the ownership-map and directory existence flags, the authorizer's identity and firm-handling location, the function unchanged, no write, no id")
        return True
    import boto3
    lam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("s3")

    def exists(key):
        try:
            s3.head_object(Bucket=OWN_BUCKET, Key=key)
            return True
        except Exception as ex:  # noqa: BLE001
            code = getattr(ex, "response", {}).get("Error", {}).get("Code", "")
            need(code in ("404", "NoSuchKey", "NotFound"), "head_object failed with %s, not a clean absence" % (code or type(ex).__name__))
            return False
    om = rec["ownership_map"]
    need(exists(OWN_KEYS["legacy"]) == om["legacy_key_exists"] and exists(OWN_KEYS["canonical"]) == om["canonical_key_exists"], "the ownership-map existence flags differ from the live reads")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    need(cfg["CodeSha256"] == rec["function"]["code_sha256_after"], "the 49F read function's code hash differs from the record: a write happened")
    raw = (cfg.get("Environment") or {}).get("Variables", {}).get("IRPT_DIRECTORY_BUCKET_MAP", "{}")
    need(sorted(json.loads(raw)) == sorted(rec["function"]["directory_bucket_map"]), "the live directory bucket map differs from the record")
    print("OK: live: the ownership-map flags equal the record's, the 49F read function runs the recorded code hash and the recorded bucket map (nothing was written)")
    return True


def synthetic():
    pr = lambda lab, st, rc: {"label": lab, "method": "lambda-invoke", "status": st, "reason_code": rc, "content_encoding": None, "invoked_utc": "2026-10-17T02:10:00Z", "request_id": "r-" + lab}  # noqa: E731
    return {"claim": "measured", "applier": APPLIER, "no_write": True,
            "probes": [pr(LABELS[0], 403, "FIRM_BINDING"), pr(LABELS[1], 403, "FIRM_BINDING"), pr(LABELS[2], 200, None)],
            "ownership_map": {"bucket": OWN_BUCKET, "legacy_key_exists": False, "canonical_key_exists": False},
            "directory": {"latest_json_exists": True, "entry_count": 271},
            "authorizer": {"authorizer_id": "naqxlm", "type": "REQUEST", "function_name": "irpt-edge-authorizer", "firm_handling_location": "none", "lists_firms": False},
            "function": {"name": FUNCTION, "code_sha256_before": "abc=", "code_sha256_after": "abc=", "directory_bucket_map": ["49financial"]},
            "notes": "Read only: three synthetic invokes by label, two existence heads, one authorizer read; nothing was written.", "reads": {"vendor_calls": 0, "secret_reads": 0}}


def selftest():
    rec = synthetic()
    check_record(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "no_write": lambda r: r.update(no_write=False),
        "applier": lambda r: r.update(applier="0.7.0_AE_CloudOps~DB2"),
        "label order": lambda r: r["probes"].reverse(),
        "label missing": lambda r: r["probes"].pop(),
        "control status": lambda r: r["probes"][2].update(status=403),
        "reason sentence": lambda r: r["probes"][0].update(reason_code="the firm is refused"),
        "status text": lambda r: r["probes"][0].update(status="403"),
        "ownership bucket": lambda r: r["ownership_map"].update(bucket="opal-data-49financial"),
        "ownership flag": lambda r: r["ownership_map"].update(legacy_key_exists="no"),
        "directory count": lambda r: r["directory"].update(entry_count=-1),
        "authorizer missing": lambda r: r["authorizer"].pop("type"),
        "function changed": lambda r: r["function"].update(code_sha256_after="def="),
        "cottonwood already mapped": lambda r: r["function"].update(directory_bucket_map=["49financial", "cottonwood"]),
        "reads": lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}),
        "notes short": lambda r: r.update(notes="ok"),
    }
    n = 0
    for label, mut in arms.items():
        r = copy.deepcopy(rec)
        try:
            mut(r)
            check_record(r)
        except (Fail, KeyError, AssertionError, IndexError):
            n += 1
            continue
        raise AssertionError("arm passed: " + label)
    r = copy.deepcopy(rec)
    r["notes"] = "an account id 1234567890 slipped in " + "x" * 10
    need(digit_runs(r), "digit-run detector")
    print("selftest: record clauses behave on a green arm and %d red arms" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
