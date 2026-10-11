"""IB-pr-421 vendor-path runner: ONE extracted Lambda zip, one process, offline, in-memory fakes, NO vendor call, no AWS, no Secrets Manager.
    python -I vendor_path_runner_421.py <extracted_zip_dir> <side:live|built> <out_json> <state_pickle> <fixtures_dir> <worktree_reports_tests> [<layer_python_dir> ...]
It drives the zip's OWN authorization factory (the class the zip's runtime.py builds) and its OWN retained.RetainedPerformance:
  fresh_<firm>   an admitted fresh vendor request for a PACKAGED firm, with neither IRPT_PERFORMANCE_APPROVED_PLAN nor
                 IRPT_PERF_VENDOR_EGRESS_AUTHORIZED set (the environment is cleared in this process), a fake table and a fake transport injected
                 through the factory's own transport_builder. Records whether a transport was produced, and for a produced one the sha256 of the
                 bodies the fake transport was asked to send against the sha256 of the requests the provider's own requests_for builds.
  reopen         the built side first computes a Cottonwood report once (fresh, through the zip's own factory and the fixture responses) and saves the
                 fake table and S3 as a pickle; both sides then ask for the SAME report again (the retained reopen) through the zip's own
                 RetainedPerformance, with the zip's own factory wrapped by a counter. Records the counter, the use-row count and the outcome class.
Nothing client-specific: synthetic ids only, and the output holds counts, sha256 and class names. ASCII only.
"""
import copy
import hashlib
import io
import json
import os
import pickle
import sys
from pathlib import Path
from types import SimpleNamespace

zip_dir, side, out_path, state_path, fixtures_dir, wt_tests = sys.argv[1:7]
# The layer dirs go AFTER the local site-packages: the layer's jsonschema needs a Linux-native rpds that cannot load here; the layer still
# supplies its own modules (ids, bd_helpers, irpt_contracts) because nothing local shadows them.
for _layer in sys.argv[7:]:
    sys.path.append(_layer)
sys.path.insert(0, zip_dir)
for _v in ("IRPT_PERFORMANCE_APPROVED_PLAN", "IRPT_PERF_VENDOR_EGRESS_AUTHORIZED"):
    os.environ.pop(_v, None)
# The shared report contract travels in the irpt-common LAYER (/opt/python/irpt_contracts on the runtime); here its extracted copy.
for _layer in sys.argv[7:]:
    if (Path(_layer) / "irpt_contracts" / "PerformanceReport.schema.json").is_file():
        os.environ["IRPT_CONTRACTS_DIR"] = str(Path(_layer) / "irpt_contracts")

import authorization  # noqa: E402  (the zip's own)
import retained  # noqa: E402
import repository  # noqa: E402
import retention  # noqa: E402
import bd_selected  # noqa: E402
import orion_selected  # noqa: E402
import tenants  # noqa: E402
import normalize  # noqa: E402

TREE = str(Path(zip_dir).resolve())
for _m in (authorization, retained, repository, retention, bd_selected, orion_selected, tenants, normalize):
    assert str(Path(_m.__file__).resolve()).startswith(TREE), _m.__file__

# Fakes: the repo's own test helpers (data/fakes only), imported AFTER the zip's modules so they resolve to the zip's.
sys.path.append(wt_tests)
import test_retention as _tr  # noqa: E402
from repository import digest  # noqa: E402

FACTORY = getattr(authorization, "VendorUseTransportFactory", None) or getattr(authorization, "OneUseTransportFactory")
NOW = 1_800_000_000


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def make_factory(table, builder_arg_count, transport):
    """The zip's own factory with an injected fake transport; the live class wants builder(token), the built one builder()."""
    if FACTORY.__name__ == "OneUseTransportFactory":
        return FACTORY(table, environment={}, clock=lambda: NOW, transport_builder=lambda token: transport)
    return FACTORY(table, clock=lambda: NOW, transport_builder=lambda: transport)


class RecordingTransport:
    def __init__(self):
        self.sent = []

    def request(self, route, url, body, label=None):
        self.sent.append((route, sha(body)))
        return SimpleNamespace(ok=True, status=200)


class UseTable:
    def __init__(self):
        self.puts = []

    def put_item(self, **kw):
        self.puts.append(copy.deepcopy(kw))


def cot_case():
    account = "acc_" + "a" * 24
    mapping = {"firm_id": tenants._CANONICAL_COT, "canonical_account_id": account, "vendor_account_id": 900000001,
               "vendor_external_id": "SCRUBBED-EXTERNALID-003", "source_revision": "synthetic-crosswalk", "currency": "USD"}
    request = {"firm_id": tenants._CANONICAL_COT, "account_ids": [account], "start": "2026-06-10", "end": "2026-09-09"}
    return request, mapping, bd_selected.requests_for


def inf_case():
    account = "acc_" + "c" * 24
    mapping = {"firm_id": tenants._CANONICAL_INF, "canonical_account_id": account, "vendor_account_id": 900000002,
               "vendor_household_id": 381, "source_revision": "synthetic-accounts-v2", "currency": "USD"}
    request = {"firm_id": tenants._CANONICAL_INF, "account_ids": [account], "start": "2026-01-01", "end": "2026-09-24"}
    return request, mapping, orion_selected.requests_for


def fresh(name, case):
    request, mapping, requests_for = case
    expected = requests_for(mapping, request["account_ids"][0], request["start"], request["end"])
    table, transport = UseTable(), RecordingTransport()
    out = {"factory_class": FACTORY.__name__, "expected_requests_sha256": sha(expected)}
    try:
        bound = make_factory(table, 0, transport)(copy.deepcopy(request), copy.deepcopy(mapping))
    except Exception as exc:  # noqa: BLE001 -- recorded, not hidden
        out.update(outcome="refused", exception=type(exc).__name__, transport_produced=False)
    else:
        sent = {}
        for route in expected:
            bound.request(route, "https://synthetic.invalid/" + route, copy.deepcopy(expected[route]))
        for route, digest_ in transport.sent:
            sent[route] = digest_
        altered_refused = False
        try:
            bound.request(next(iter(expected)), "https://synthetic.invalid/x", {"altered": True})
        except Exception as exc:  # noqa: BLE001
            altered_refused = type(exc).__name__ == "VendorEgressRefused"
        out.update(outcome="transport", transport_produced=True, sent_routes=sorted(sent),
                   sent_matches_built_requests=all(sent.get(r) == sha(expected[r]) for r in expected) and len(sent) == len(expected),
                   bound_requests_match=sha(bound.requests) == sha(expected), altered_body_refused=altered_refused)
    out["use_rows_written"] = len(table.puts)
    out["use_row_unconditional"] = all("ConditionExpression" not in p for p in table.puts) if table.puts else None
    return out


def reopen():
    request, mapping, _ = cot_case()
    account = request["account_ids"][0]
    data = {n: json.loads((Path(fixtures_dir) / f).read_text(encoding="utf-8"))
            for n, f in (("performancePeriod", "bd_period.json"), ("performanceSeries", "bd_series.json"))}

    class Fixture:
        def request(self, route, url, body, label=None):
            raw = json.dumps(data[route]).encode()
            return SimpleNamespace(ok=True, status=200, body=copy.deepcopy(data[route]), raw_body=raw,
                                   source_response_sha256=hashlib.sha256(raw).hexdigest(), response_bytes=len(raw))

    class S3:
        def __init__(self):
            self.objects, self.put_count = {}, 0

        def put_object(self, Bucket, Key, Body, ContentType, IfNoneMatch):
            assert IfNoneMatch == "*"
            if (Bucket, Key) in self.objects:
                raise RuntimeError("PreconditionFailed")
            self.put_count += 1
            self.objects[Bucket, Key] = (bytes(Body), "version-%d" % self.put_count)
            return {"VersionId": self.objects[Bucket, Key][1]}

        def head_object(self, Bucket, Key):
            return {"VersionId": self.objects[Bucket, Key][1]}

        def get_object(self, Bucket, Key, VersionId):
            body, version = self.objects[Bucket, Key]
            assert VersionId == version
            return {"Body": io.BytesIO(body)}

    table, s3 = _tr.Table(), S3()
    if side == "live":
        saved = pickle.loads(Path(state_path).read_bytes())
        table.rows, s3.objects, s3.put_count = saved["rows"], saved["objects"], saved["put_count"]
    registered = {"state": "ACTIVE", "policy_revision": "irpt-x10-v1", "enforcement_ref": "1" * 40,
                  "retention_policy_id": "irpt-retention-v1", "register_id": "X10", "register_commit": "705dae3202",
                  "firms": ["49financial", "cottonwood", "inflection"],
                  "families": {name: {"unreferenced_days": days, "accepted_ceiling_days": ceiling}
                               for name, days, ceiling in [("ORIGINAL_CSV", 30, 2555), ("PERFORMANCE_SOURCE_EVIDENCE", 30, 2555),
                                                           ("PERFORMANCE", None, 2555), ("SELECTED_ACCOUNTS", 30, 30), ("EXPORT_PDF", 7, 2555)]}}
    policy = retention.RetentionPolicy(retention.DynamoRetentionIndex(table),
        lambda revision: {**copy.deepcopy(registered), "policy_sha256": digest(registered)},
        lambda p, o: p["principal_id"] == o["principal_id"], clock=lambda: NOW)
    principal = {"firm_id": tenants._CANONICAL_COT, "principal_id": "test-viewer"}
    owner = {**principal, "account_ids": [account]}
    scope = {"verified_request_firm_id": tenants._LEGACY_SHORT_ID["COT"], "permitted_account_set": [account],
             "resolved_scope": {"scope_ids": [account]}}
    use_table = UseTable()
    real = make_factory(use_table, 0, Fixture())
    counter = {"constructions": 0}

    def counted(req, mp):
        counter["constructions"] += 1
        return real(req, mp)
    service = retained.RetainedPerformance(table=table, s3=s3, reporting_policy=policy.reporting_policy,
        reporting_destination=lambda firm, kind, identity, sha_, **kw: ("offline-private", "/".join((firm, kind, identity, sha_))),
        load_mapping=lambda firm, acct: copy.deepcopy(mapping), transport_factory=counted, clock=lambda: NOW)

    def compute():
        return service.compute(scope, request["start"], request["end"], principal=principal, owner=owner, authorize=policy.authorize)

    seed = {"attempted": False}
    if side == "built":
        seed["attempted"] = True
        try:
            first = compute()
            seed.update(outcome="accepted", retained=bool(first["retained_ref"]["immutable"]), constructions=counter["constructions"],
                        use_rows=len(use_table.puts))
            Path(state_path).write_bytes(pickle.dumps({"rows": table.rows, "objects": s3.objects, "put_count": s3.put_count}))
        except Exception as exc:  # noqa: BLE001
            seed.update(outcome="refused", exception=type(exc).__name__)
    before = counter["constructions"], len(use_table.puts), s3.put_count
    try:
        compute()
        outcome, exc_name = "served", None
    except Exception as exc:  # noqa: BLE001
        outcome, exc_name = "refused", type(exc).__name__
    return {"seed": seed, "reopen_outcome": outcome, "reopen_exception": exc_name,
            "reopen_transport_constructions": counter["constructions"] - before[0],
            "reopen_use_rows_written": len(use_table.puts) - before[1], "reopen_s3_puts": s3.put_count - before[2],
            "reopen_vendor_requests_sent": 0}


result = {"label": side, "factory_class": FACTORY.__name__,
          "cases": {"fresh_cottonwood": fresh("cot", cot_case()), "fresh_inflection": fresh("inf", inf_case()), "reopen": reopen()}}
outside = sorted({n for n, m in sys.modules.items() if getattr(m, "__file__", None)
                  and str(Path(m.__file__).resolve()).replace("\\", "/").find("/investor-reporting/") >= 0
                  and not str(Path(m.__file__).resolve()).startswith(TREE)})
result["modules_loaded_from_the_worktree_not_the_zip"] = outside
Path(out_path).write_text(json.dumps(result, indent=1, sort_keys=True), encoding="utf-8")
print("OK: %s %s" % (side, {k: (v.get("outcome") or v.get("reopen_outcome")) for k, v in result["cases"].items()}))
