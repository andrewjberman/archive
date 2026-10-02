"""Shared fixture for the RIV-sa-1 and RIV-pv-1 checks (issuer-written, 2.0.0_SA_COO~RV): the 2026-10-02 state that
hid C-S24, rebuilt offline. The round-5 page fixture (test_p2: TXUE and BASG on 2026-09-25, 09-28 and 09-29, G5
replayed as batch `g`); then, for page day 2026-09-30, a batch marker for every upstream stage of the sweep's chain
(what the 07:00 marker chain leaves); then, with `morning=True`, the gateless morning publish (the publish-page Lambda
carries no AI gate: batch `g`, RIVALFUNDS_AI_ENABLE unset), which writes the publish-page marker that makes
`sweep.py:469` skip.

The sweep runs through `sweep.handler_entry` with the EventBridge Scheduler input of the sweep schedule, read from the
graded tree's infra/aws/terraform/etfs-rivalfunds/generated.auto.tfvars.json (the schedule whose target is the daily
Lambda, `homes.DAILY_LAMBDA`). Its placeholders are filled (`<aws.scheduler.scheduled-time>` = <day>T13:00:00Z, which
is 09:00 America/New_York) and ONE field is changed: `sink` "s3" becomes the local sink. A Lambda-like context reports
900 s remaining at the start.

Offline: `_common.offline_guards()` refuses boto3 and requests.post. `sweep._real_runners` returns the real
publish-page; every other stage is a stub that records the call and runs nothing (no collector, no fetch).
`market_context.read_context` returns the fixture readings, and `ai_client.default_client` returns the current stub
client (no vendor call)."""
from __future__ import annotations

import hashlib
import io
import json
import os
import pathlib
import time

import _common as c

DAY = "2026-09-30"  # page day (a Wednesday, a trading day)
BATCH = "g"  # the G5 batch: the marker chain's batch id, and the morning publish's
UPSTREAM = ("build-peer-group-map", "fetch-holdings", "build-silver", "build-canonical-shape", "build-coverage",
            "build-trade-schedule")
STATE = {"client": None, "built": 0, "unexpected": [], "installed": False}
REPLY = "TXUE added to S1 in the window."


class Client(c.StubClient):
    """The stub transport: instant canned replies, or the FIRST reply delayed by `slow_s` seconds (a slow vendor)."""

    def __init__(self, slow_s: float = 0.0, n: int = 60):
        super().__init__([c.ai2_reply(REPLY, [])] * n)
        self.slow_s, self.t_first = float(slow_s), None

    def chat(self, messages, model):
        if self.t_first is None:
            self.t_first = time.monotonic()
            if self.slow_s:
                time.sleep(self.slow_s)
        return super().chat(messages, model)


class Context:
    """A Lambda-like context: 900 s at the start, counting down."""
    aws_request_id = "offline-check"

    def __init__(self, total_ms: int = 900_000):
        self.t0, self.total = time.monotonic(), total_ms

    def get_remaining_time_in_millis(self) -> int:
        return int(self.total - (time.monotonic() - self.t0) * 1000)


def install() -> None:
    """The offline guards and stubs (idempotent)."""
    c.setup_path()
    c.offline_guards()
    if STATE["installed"]:
        return
    from rivalfunds import ai_client, market_context, publish_page, sweep

    market_context.read_context = lambda day, *a, **k: c.ai2_readings()

    def _client():
        STATE["built"] += 1
        if STATE["client"] is None:
            raise PermissionError("offline check: no stub client set")
        return STATE["client"]

    ai_client.default_client = _client

    def _stub(stage):
        def run(ev):
            STATE["unexpected"].append(stage)
            return {"status": "FAILED", "batch_id": ev.get("batch_id"), "outputs": [], "marker": None,
                    "detail": "offline check: stage %s not run" % stage}
        return run

    def _runners():
        r = {st: _stub(st) for st in sweep.ALL_STAGES}
        r["publish-page"] = lambda ev: publish_page.handler_entry(ev)
        return r

    sweep._real_runners = _runners
    STATE["installed"] = True


def set_client(stub) -> None:
    STATE["client"], STATE["built"] = stub, 0


def gate(on: bool) -> None:
    if on:
        os.environ["RIVALFUNDS_AI_ENABLE"] = "1"
        os.environ["RIVALFUNDS_OPENAI_SECRET"] = "fixture/openai"
    else:
        os.environ.pop("RIVALFUNDS_AI_ENABLE", None)
        os.environ.pop("RIVALFUNDS_OPENAI_SECRET", None)


def start(morning: bool = True):
    """The fixture for page day DAY. Returns (spec, sink, tmp_dir, morning publish result or None)."""
    install()
    from rivalfunds import markers, publish_page

    gate(False)
    os.environ.pop(publish_page.PRODUCE_ENV, None)
    STATE["unexpected"].clear()
    spec, s, tmp = c.page_fixture()
    for st in UPSTREAM:
        bid = "g0" if st == "build-peer-group-map" else BATCH
        markers.write_marker(st, DAY, bid, spec, {"status": "OK", "outputs": []})
    r = publish_page.handler_entry({"date": DAY, "mode": "daily", "batch_id": BATCH, "sink": spec}) if morning else None
    return spec, s, tmp, r


def schedule_input() -> dict:
    """The sweep schedule's input as the graded tree declares it (the schedule targeting the daily Lambda)."""
    from rivalfunds import homes

    root = c.setup_path()
    tf = json.loads((root / "infra" / "aws" / "terraform" / "etfs-rivalfunds" / "generated.auto.tfvars.json")
                    .read_text(encoding="utf-8"))
    hits = [v for v in (tf.get("schedules") or {}).values() if v.get("target") == homes.DAILY_LAMBDA]
    if len(hits) != 1:
        raise RuntimeError("expected ONE schedule targeting %s, found %d" % (homes.DAILY_LAMBDA, len(hits)))
    return json.loads(hits[0]["input"])


def schedule_payload(spec: str, day: str = DAY, **extra) -> dict:
    """The schedule's input with its placeholders filled and `sink` set to the local sink (the one changed field)."""
    fill = {"<aws.scheduler.scheduled-time>": f"{day}T13:00:00Z",
            "<aws.scheduler.execution-id>": "offline-execution-id"}
    ev = {k: (fill.get(v, v) if isinstance(v, str) else v) for k, v in schedule_input().items()}
    ev["sink"] = spec
    ev.update(extra)
    return ev


def sweep(event: dict) -> dict:
    from rivalfunds import sweep as sw

    return sw.handler_entry(event, Context())


def accounts(s) -> list[str]:
    from rivalfunds import homes

    prefix = homes.address("rivalfunds", "etfs", "gold", "research_hypotheses", f"date={DAY}") + "/"
    return sorted(u for u in s.list(prefix) if u.endswith(".parquet"))


def page_markers(s) -> list[dict]:
    from rivalfunds import markers

    return markers.read_markers("publish-page", DAY, s)


def manifest(s) -> dict:
    from rivalfunds import homes

    uri = homes.page(DAY, "manifest.json")
    return json.loads(s.get(uri).decode("utf-8")) if s.exists(uri) else {}


def index(s) -> str:
    from rivalfunds import homes

    uri = homes.page(DAY, "index.html")
    return s.get(uri).decode("utf-8") if s.exists(uri) else ""


def ai_run(man: dict) -> dict:
    return (man.get("a1_produced") or {}).get("research_hypotheses_run") or {}


def run_paths(s, uri: str) -> list:
    """The `run_path` of every row's input_manifest in one account object (the account's provenance)."""
    import pyarrow.parquet as pq

    rows = pq.read_table(io.BytesIO(s.get(uri))).to_pandas().to_dict("records")
    return sorted({str(json.loads(r.get("input_manifest") or "{}").get("run_path")) for r in rows})


def run_id_of(uri: str) -> str:
    return uri.rsplit("/", 1)[-1][len("research_hypotheses-"):-len(".parquet")]


def snapshot(tmp) -> dict:
    """{relative path: sha256} of every file under the local sink."""
    base = pathlib.Path(tmp)
    return {p.relative_to(base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(base.rglob("*")) if p.is_file()}
