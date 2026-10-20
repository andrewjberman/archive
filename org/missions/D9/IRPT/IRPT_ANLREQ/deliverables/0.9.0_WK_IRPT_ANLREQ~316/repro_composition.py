"""AR-y-436 (IRPT_ANLREQ-D2-W316): which step of CompositionAdmission.validate refuses a request composition whose
frozen portfolio holds kept rows. Offline: no AWS, no network, no push.

The baseline is the accepted composition the product's own test world builds (the one
ycharts/generate/tests/test_composition_refusal_cause.py starts from). The frozen portfolios are produced by
intake/portfolio.py freeze_template_portfolio from synthetic checks that come from the product's SecurityResolver
with a synthetic checker and an empty provider. Prints exactly three REPRO lines. If a premise does not hold it
prints BLOCKED on stderr and exits 2, never a fake result.
"""
import contextlib
import copy
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[6]
IR = REPO / "infra/aws/lambda/investor-reporting"
SCHEMA_DIR = REPO / "docs/contracts/investor-reporting/v1"
sys.path[:0] = [str(IR / "intake/tests"), str(IR / "ycharts/generate"), str(IR / "reports/tests"),
                str(IR / "reports"), str(IR / "intake"), str(IR / "ycharts/generate")]

import portfolio  # noqa: E402
import security_resolution  # noqa: E402
import template_reader  # noqa: E402
import test_retained_uploads as retained  # noqa: E402
import test_retention  # noqa: E402
from composition_admission import CompositionAdmission  # noqa: E402
from submission import SubmissionRefused  # noqa: E402

CSV_KEPT = b"Ticker,Dollars\nSPY,1000\nAGG,2000\nTIMXX,1500\n"
CSV_KEPT_UNRESOLVED = b"Ticker,Dollars\nSPY,1000\nAGG,2000\nTIMXX,1500\nZQXWVK,700\n"
KEPT = {"state": "KEPT", "rows": 20, "last_close": 1.0, "reason": "HISTORY_ROWS"}
NOT_KEPT = {"state": "NOT_KEPT", "rows": 0, "last_close": None, "reason": "NO_ROWS"}
KEEP_UNRESOLVED = [{"finding_code": "TICKER_NOT_FOUND", "from_value": "ZQXWVK", "to_value": "ZQXWVK"}]


def blocked(message):
    print("BLOCKED: " + message, file=sys.stderr)
    raise SystemExit(2)


class SyntheticChecker:
    """The yfinance checker port, answering from a fixed dict (no yfinance import, no network)."""

    def __init__(self, answers):
        self.answers = answers

    def check(self, symbols):
        return {s: dict(self.answers[s]) for s in symbols if s in self.answers}


def empty_provider(requested):
    """The provider port: a complete read with no rows, so every provider-checked symbol is NOT_FOUND."""
    return {"http_status": 200, "complete": True, "final_url_path": "/securities/securities_info",
            "account_id": "fixture-account", "source_revision": "lookup-v1", "requested": list(requested),
            "observed_at": "2026-10-13T12:00:00Z", "json": []}


def resolved_checks(symbols, answers):
    resolver = security_resolution.SecurityResolver(
        provider_check=empty_provider, identity=lambda symbol, kind: None, cache=None,
        clock=lambda: 1000.0, account_id="fixture-account", source_revision="lookup-v1",
        checker=SyntheticChecker(answers))
    return {row["symbol"]: row for row in resolver.check(symbols)["results"]}


def baseline():
    """The product's own accepted composition, built exactly as test_composition_refusal_cause.accepted_document."""
    raw = test_retention.world._get_wrapped_function()()
    world = retained.world._get_wrapped_function()(raw)
    first = world.case.create()
    service, accepted, body, _loaded = retained.submission(world, first)
    service.submit(body, None, {}, {}, None)
    _owner, _unused, ref = accepted.accept.call_args.args
    data = world.stores.artifacts.get(world.case.principal, ref["artifact_id"])["data"]
    return json.loads(data)


def freeze(csv, owner, upload_id, checks, corrections=None):
    template = template_reader.read_template(csv, "csv")
    source = {"lane": "TEMPLATE_UPLOAD", "upload_id": upload_id, "file_type": "csv",
              "content_sha256": template["content_sha256"]}
    options = {"corrections": corrections} if corrections else {}
    result = portfolio.freeze_template_portfolio(template, owner, source, copy.deepcopy(checks), **options)
    if result["state"] != "NORMALIZED":
        codes = sorted({f.get("code", "?") for f in result["findings"] if f.get("severity") == "ERROR"})
        blocked("freeze_template_portfolio state=%s error_codes=%s" % (result["state"], ",".join(codes)))
    return result["frozen"]


def composition_with(base, frozen):
    """The baseline with its frozen portfolio replaced; the digest fields that bind it are re-derived."""
    doc = copy.deepcopy(base)
    artifact = dict(doc["resolved"]["input_ref"]["artifact_ref"], sha256=frozen["content_sha256"],
                    byte_length=len(portfolio.canonical_bytes(frozen["document"])))
    doc["resolved"]["input_ref"] = {"input_id": frozen["input_id"],
                                    "content_sha256": frozen["content_sha256"], "artifact_ref": artifact}
    doc["resolved"]["document"] = copy.deepcopy(frozen["document"])
    doc["browser"]["input_id"] = frozen["input_id"]
    return doc


def admit(admission, doc):
    """Run validate; return (step, error_class, cause). The step and class come from validate's own log line."""
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            admission.validate(doc)
    except SubmissionRefused as error:
        match = re.search(r"^COMPOSITION-REFUSED step=([1-5]) error_class=(\S+)$", out.getvalue(), re.M)
        if match is None:
            blocked("validate refused without its COMPOSITION-REFUSED line")
        return match.group(1), match.group(2), error.__cause__
    return "none", "none", None


def detail(step, cause):
    """Schema step: the jsonschema keyword and the path. Bindings or portfolio step: the check name. Else '-'."""
    if step == "2":
        path = "/".join(str(part) for part in cause.absolute_path)
        return "%s@/%s" % (cause.validator, path)
    if step in ("4", "5"):
        return re.sub(r"\s+", "_", str(getattr(cause, "code", None) or cause)) or "-"
    return "-"


def main():
    if not (REPO / "org").is_dir() or not SCHEMA_DIR.is_dir():
        blocked("repository paths not found from %s" % HERE)
    admission = CompositionAdmission(SCHEMA_DIR)
    base = baseline()
    step, error_class, _cause = admit(admission, base)
    if step != "none":
        blocked("the baseline accepted composition was refused at step %s class %s" % (step, error_class))
    owner = {k: v for k, v in base["resolved"]["owner"].items() if k not in ("account_ids", "prospect_input_id")}
    upload_id = base["resolved"]["owner"]["prospect_input_id"]

    answers = {"SPY": KEPT, "AGG": KEPT, "TIMXX": KEPT}
    frozen_a = freeze(CSV_KEPT, owner, upload_id, resolved_checks(["SPY", "AGG", "TIMXX"], answers))
    frozen_b = freeze(CSV_KEPT_UNRESOLVED, owner, upload_id,
                      resolved_checks(["SPY", "AGG", "TIMXX", "ZQXWVK"], dict(answers, ZQXWVK=NOT_KEPT)),
                      corrections=KEEP_UNRESOLVED)
    doc_a = composition_with(base, frozen_a)
    doc_b = composition_with(base, frozen_b)
    doc_c = copy.deepcopy(base)
    del doc_c["recipe_version"]

    step_a, class_a, _ = admit(admission, doc_a)
    print("REPRO-A step=%s class=%s" % (step_a, class_a))
    step_b, class_b, cause_b = admit(admission, doc_b)
    print("REPRO-B step=%s class=%s detail=%s" % (step_b, class_b, detail(step_b, cause_b)))
    step_c, class_c, _ = admit(admission, doc_c)
    print("REPRO-C step=%s class=%s" % (step_c, class_c))


if __name__ == "__main__":
    main()
