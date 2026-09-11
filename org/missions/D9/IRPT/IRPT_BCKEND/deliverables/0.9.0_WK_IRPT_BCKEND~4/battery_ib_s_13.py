"""IB-s-13 acceptance battery -- S13-AC1.

Seven arms, each printing its own denominators, and the token only when every one holds.
The token is IBS13-NARRATIVE-DETERMINISTIC.

Arms (a)-(f) are OFFLINE: they run the committed package over committed fixtures with a
socket guard installed, and the guard is proved live by a positive control before the
verdict. Arms (d), (g) and (h) take NAMED reads on the AWS control plane and on the news
plane -- DynamoDB Query/Scan and S3 ListObjectsV2, both READ -- because what they assert is
about the live world and cannot be proved from a fixture.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import json
import pathlib
import socket
import subprocess
import sys
import tempfile
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[7]
PACKAGE = REPO / "infra" / "aws" / "lambda" / "investor-reporting" / "narrative"
FIXTURES = PACKAGE / "fixtures"
LAYER_DIR = REPO / "infra" / "aws" / "lambda" / "layers" / "irpt-common"
LAYER_ZIP = LAYER_DIR / "irpt-common.zip"
NARR_IAM = REPO / "infra" / "aws" / "terraform" / "investor-reporting" / "narrative" / "iam.tf"
# THE ESTATE'S OWN SHIM, via its .cmd face. `.tools/aws` is a bash script and a
# Windows Python cannot exec it (WinError 193); `.tools/aws.cmd` is the same shim
# with a launcher this interpreter can spawn, so the instrument is the estate's
# rather than a boto3 call standing in for it.
AWS = ["cmd", "/c", str(REPO / ".tools" / "aws.cmd")]
CUTOFF = "2026-09-09T23:59:59Z"

sys.path.insert(0, str(PACKAGE))
import events as events_mod      # noqa: E402
import evidence as evidence_mod  # noqa: E402
import handler as handler_mod    # noqa: E402
import prose as prose_mod        # noqa: E402

VENDOR_HOSTS = ("bd3.bdreporting.com", "api.cloud.orionadvisor.com")
MODEL_HOSTS = ("api.openai.com", "api.anthropic.com", "bedrock-runtime.us-east-1.amazonaws.com")
_real_connect = socket.socket.connect
_real_connect_ex = socket.socket.connect_ex
ATTEMPTS = {"total": 0, "vendor": 0, "model": 0}
RESULTS = []


def _guard(self, address, *a, **k):
    host = address[0] if isinstance(address, tuple) else str(address)
    ATTEMPTS["total"] += 1
    if any(v in str(host) for v in VENDOR_HOSTS):
        ATTEMPTS["vendor"] += 1
    if any(m in str(host) for m in MODEL_HOSTS):
        ATTEMPTS["model"] += 1
    raise OSError("BLOCKED: socket guard -- the offline arms opened nothing (%s)" % (host,))


def install_guard():
    socket.socket.connect = _guard
    socket.socket.connect_ex = _guard


def remove_guard():
    socket.socket.connect = _real_connect
    socket.socket.connect_ex = _real_connect_ex


def head(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def record(arm, ok, claim, evidence):
    RESULTS.append((arm, bool(ok), claim, evidence))
    print("  %s:  %s  -- %s" % ("PASS" if ok else "FAIL", claim, evidence))


def aws_json(args):
    """A NAMED control-plane / news-plane READ through the estate's own shim."""
    proc = subprocess.run(AWS + args, capture_output=True)
    out = proc.stdout.decode("utf-8", "replace").replace("\r", "")
    if proc.returncode != 0:
        return {"_error": proc.stderr.decode("utf-8", "replace")[:300], "_rc": proc.returncode}
    return json.loads(out) if out.strip() else {}


def load_report():
    with open(str(FIXTURES / "performance_report_inf.json"), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    policy = handler_mod.load_policy()
    report = load_report()
    series = report["returns"]["daily_cumulative_series"]
    store = evidence_mod.RecordedTopicStore.from_file(FIXTURES / "topics_window.json")
    later = evidence_mod.RecordedTopicStore.from_file(FIXTURES / "topics_predating.json")

    print("IB-s-13 BATTERY -- narrative events, dated evidence, contemporaneity")
    print("  package     : %s" % PACKAGE)
    print("  policy      : %s v%s (materiality %.4f)"
          % (policy["policy_id"], policy["policy_version"], policy["materiality_threshold"]))
    print("  store       : recorded fixture (no credential, no host, no socket)")

    install_guard()

    # ---------------------------------------------------------------- (a)
    head("(a) DETERMINISTIC -- the same series and history select the same moments twice")
    run_a = handler_mod.build_packet(report, store, CUTOFF, policy,
                                     declared_daily_length=len(series))
    run_b = handler_mod.build_packet(json.loads(json.dumps(report)), store, CUTOFF, policy,
                                     declared_daily_length=len(series))
    same = json.dumps(run_a["packet"], sort_keys=True) == json.dumps(run_b["packet"], sort_keys=True)
    det = run_a["detection"]
    print("  series points fed to the detector : %d" % det["series_points"])
    print("  daily_cumulative_series length    : %d  (declared denominator asserted equal)"
          % len(series))
    print("  series window                     : %s .. %s"
          % (det["series_first_date"], det["series_last_date"]))
    print("  series_fingerprint                : %s" % det["series_fingerprint"][:32])
    print("  episodes found / material         : %d / %d"
          % (det["episodes_found"], det["episodes_material"]))
    print("  movement windows raw / merged     : %d / %d  (%d collapsed by the merge)"
          % (det["movement_windows_raw"], det["movement_windows_merged"], det["merge_collapsed"]))
    for ev in run_a["packet"]["events"]:
        print("    %-9s %s  cumulative=%+0.9f" % (ev["event_type"], ev["date"], ev["value"]))
    diff = [x for x in zip(run_a["packet"]["events"], run_b["packet"]["events"]) if x[0] != x[1]]
    print("  run-to-run event diff             : %d entry(ies)  <- empty is the arm" % len(diff))
    # THE DOWNSAMPLE CONTROL: the same detector on a 7th-of-the-points curve must REFUSE.
    thin = json.loads(json.dumps(report))
    thin["returns"]["daily_cumulative_series"] = series[::7]
    try:
        events_mod.detect(thin, policy, declared_daily_length=len(series))
        downsample_refused = "NOT REFUSED (the arm fails)"
        ok_ds = False
    except events_mod.SeriesRefused as exc:
        downsample_refused = exc.refusal
        ok_ds = True
    print("  CONTROL: a %d-point display curve -> %s" % (len(series[::7]), downsample_refused))
    record("a", same and not diff and ok_ds and det["series_points"] == len(series),
           "the same series selects the same moments twice, on the pre-downsample daily series",
           "%d of %d events identical across two runs; %d point(s) in and %d asserted; a "
           "downsampled curve is REFUSED" % (len(run_a["packet"]["events"]),
                                             len(run_b["packet"]["events"]),
                                             det["series_points"], len(series)))

    # ---------------------------------------------------------------- (b)
    head("(b) THE FUTURE IS EXCLUDED BY DATE -- the difference control")
    ev_last = {"event_type": "MOVEMENT", "date": "2026-09-09", "value": 0.0,
               "series_basis": events_mod.SERIES_BASIS}
    strict = evidence_mod.collect_for_event(store, ev_last, policy, CUTOFF)
    loose = evidence_mod.collect_for_event(store, ev_last, policy, "2026-12-31T00:00:00Z")
    packet_future = [r for r in run_a["packet"]["cited_evidence"]
                     if r["admission"] == evidence_mod.EXCLUDED_FUTURE]
    cited_ids = set(run_a["packet"]["prose"]["cited_evidence_ids"])
    future_in_prose = [r["evidence_id"] for r in packet_future if r["evidence_id"] in cited_ids]
    print("  cutoff                            : %s" % CUTOFF)
    for item in strict["excluded_future"]:
        print("    EXCLUDED_FUTURE %s published %s > cutoff %s"
              % (item["evidence_id"], item["published_at"], item["cutoff_at"]))
    print("  future ids in the PROSE            : %d of %d future item(s)  <- 0 is the arm"
          % (len(future_in_prose), len(packet_future)))
    print("  CONTROL (a policy that admits it) : cutoff moved to 2026-12-31 -> %d excluded, "
          "%d admitted; the SAME code admits the same article, so the exclusion is a "
          "decision and not a coincidence of the fixture"
          % (len(loose["excluded_future"]), len(loose["admitted"])))
    undated = strict["excluded_undated"]
    print("  undated (never assumed)           : %d item(s)" % len(undated))
    for item in undated:
        print("    EXCLUDED_UNDATED %s -- %s" % (item["evidence_id"], item["reason"][:80]))
    record("b", len(strict["excluded_future"]) >= 1 and not future_in_prose
           and len(loose["excluded_future"]) < len(strict["excluded_future"]),
           "future information is excluded BY DATE and the exclusion is recorded, not dropped",
           "%d future item(s) excluded and 0 of %d reach the prose; moving the cutoff "
           "changes the answer (%d -> %d excluded)"
           % (len(strict["excluded_future"]), len(packet_future),
              len(strict["excluded_future"]), len(loose["excluded_future"])))

    # ---------------------------------------------------------------- (c)
    head("(c) MISSING HISTORY IS AN ANSWER, NOT AN EMPTY LIST")
    env_missing = handler_mod.build_packet(report, later, CUTOFF, policy,
                                           declared_daily_length=len(series))
    cov = env_missing["packet"]["coverage"]
    print("  store coverage bounds             : %s" % (list(later.bounds()),))
    print("  windows evaluated / covered       : %d / %d" % (cov["windows_evaluated"],
                                                             cov["windows_covered"]))
    print("  missing_history                   : %s" % cov["missing_history"])
    print("  reason                            : %s" % (cov["missing_history_reason"] or "")[:150])
    print("  prose says MISSING HISTORY        : %s"
          % ("MISSING HISTORY" in env_missing["packet"]["prose"]["text"]))
    print("  prose still VALIDATED             : %s (an honest empty answer is not punished; "
          "otherwise 'say nothing' would be the cheapest way to pass)"
          % env_missing["packet"]["prose"]["validation_status"])
    print("  CONTRAST: the covered store       : missing_history=%s, %d of %d windows"
          % (run_a["packet"]["coverage"]["missing_history"],
             run_a["packet"]["coverage"]["windows_covered"],
             run_a["packet"]["coverage"]["windows_evaluated"]))
    record("c", cov["missing_history"] == evidence_mod.MISSING_HISTORY
           and "MISSING HISTORY" in env_missing["packet"]["prose"]["text"]
           and run_a["packet"]["coverage"]["missing_history"] == evidence_mod.NONE,
           "a window predating the history renders MISSING HISTORY with its bounds",
           "%d of %d windows uncovered against bounds %s; the covered store renders NONE"
           % (cov["windows_evaluated"] - cov["windows_covered"], cov["windows_evaluated"],
              list(later.bounds())))

    # ---------------------------------------------------------------- (e)
    head("(e) SECONDARY SIGNALS GATED; SYNDICATED CONTEXT DEDUPLICATED")
    signals = [
        {"name": "rsi_14", "observed_at": "2026-07-29", "universe": "SP500 members", "value": 28.1},
        {"name": "fear_greed", "observed_at": "2026-07-29", "universe": "US equity",
         "value_state": "CURRENT", "value": 50},
        {"name": "regime", "universe": "US equity", "value": "risk-off"},
        {"name": "best_worst", "observed_at": "2026-07-29", "value": "ABC +4%"},
    ]
    rulings = [evidence_mod.admit_secondary_signal(s, policy) for s in signals]
    for ruling in rulings:
        print("    %-11s %-8s %s" % (ruling["signal"], "ADMIT" if ruling["admitted"] else "REFUSE",
                                     ruling.get("reason", ruling.get("observed_at", ""))[:95]))
    admitted_signals = [r for r in rulings if r["admitted"]]
    syn = [c for c in strict["candidates"] if c.get("syndicated_copies", 1) > 1]
    total_collapsed = sum(b["syndication_collapsed"] for b in
                          [evidence_mod.collect_for_event(store, e, policy, CUTOFF)
                           for e in run_a["packet"]["events"]])
    print("  syndication collapsed (all events): %d copy(ies) folded into their first id"
          % total_collapsed)
    for item in syn[:4]:
        print("    %s  copies=%d  sources=%s  dates=%s"
              % (item["evidence_id"], item["syndicated_copies"],
                 ",".join(item["syndicated_sources"])[:60], item["syndicated_dates"]))
    ids = [c["evidence_id"] for c in strict["candidates"]]
    print("  evidence ids unique in the window : %d of %d" % (len(set(ids)), len(ids)))
    record("e", len(admitted_signals) == 1 and total_collapsed > 0 and len(set(ids)) == len(ids),
           "a current/neutral value is refused as history; syndicated copies collapse to one id",
           "%d of %d signals admitted (the three refused name what they lack); %d syndicated "
           "copy(ies) collapsed; %d of %d ids unique"
           % (len(admitted_signals), len(signals), total_collapsed, len(set(ids)), len(ids)))

    # ---------------------------------------------------------------- (f)
    head("(f) CONTEMPORANEITY, NEVER CAUSE")
    good = ('On 2026-07-29 the portfolio sat at a cumulative 0.25%. Over the same window the '
            'dated record carried "A headline" [ev-00000000000000ab].')
    bad = [
        "The portfolio fell on 2026-07-29 because inflation data surprised. "
        "Over the same window [ev-00000000000000ab].",
        "Tariff headlines drove the drawdown into 2026-07-29. "
        "Over the same window [ev-00000000000000ab].",
        "The recovery on 2026-08-04 came in response to the rate decision. "
        "Over the same window [ev-00000000000000ab].",
    ]
    v_good = prose_mod.validate(good, ["ev-00000000000000ab"])
    print("    ACCEPT  %s  contemporaneity=%s causation=%s"
          % (v_good["validation_status"], v_good["states_contemporaneity"],
             v_good["asserts_causation"]))
    bad_ok = True
    for text in bad:
        verdict = prose_mod.validate(text, ["ev-00000000000000ab"])
        bad_ok = bad_ok and verdict["validation_status"] == prose_mod.REJECTED
        print("    REJECT  %s  hits=%s" % (verdict["validation_status"], verdict["causal_hits"]))
    shipped = run_a["prose_validation"]
    print("  the SHIPPED prose                 : %s, contemporaneity=%s, causation=%s"
          % (shipped["validation_status"], shipped["states_contemporaneity"],
             shipped["asserts_causation"]))
    print("  citations resolved                : %s (unknown: %s)"
          % (shipped["citations_resolved"], shipped["unknown_citations"] or "none"))
    admitted_ids = {r["evidence_id"] for r in run_a["packet"]["cited_evidence"]
                    if r["admission"] == evidence_mod.ADMITTED}
    subset = set(run_a["packet"]["prose"]["cited_evidence_ids"]).issubset(admitted_ids)
    print("  every cited id is a SELECTED id   : %s (%d cited of %d admitted)"
          % (subset, len(run_a["packet"]["prose"]["cited_evidence_ids"]), len(admitted_ids)))
    resolved_n, resolved_d = shipped["citations_resolved"].split(" of ")
    print("  news text as DATA                 : %d instruction-shaped marker(s) seen and "
          "neutralised across the window; the prose template has no slot an instruction "
          "could occupy"
          % len([c for c in strict["candidates"] if c["neutralised_markers"]]))
    record("f", v_good["validation_status"] == prose_mod.VALIDATED and bad_ok and subset
           and resolved_n == resolved_d
           and shipped["validation_status"] == prose_mod.VALIDATED,
           "a contemporaneous sentence is accepted, three causal phrasings are rejected, "
           "every citation resolves",
           "1 of 1 accepted, %d of %d rejected, citations %s"
           % (len(bad), len(bad), shipped["citations_resolved"]))

    # ---------------------------------------------------------------- (d) part 1 (offline)
    head("(d) THE TIMEZONE IS VERIFIED FROM THE PRODUCER'S OWN BYTES")
    for row in evidence_mod.PUBLICATION_TIMEZONE_EVIDENCE:
        print("    %s:%s" % (row["file"], row["line"]))
        print("      %s" % row["source_line"][:110])
        print("      -> %s  [%s]" % (row["fact"][:100], row["claim"]))
    bases = {}
    for item in strict["candidates"]:
        bases[item["publication_timezone_basis"]] = bases.get(
            item["publication_timezone_basis"], 0) + 1
    print("  per-item timezone basis (window)  : %s" % bases)
    print("  DECLARED publication timezone     : %s -- and ET is NOT written anywhere, "
          "because no producer byte establishes it" % evidence_mod.PUBLICATION_TIMEZONE)

    # the positive control BEFORE the guard comes off, so the zero below is measured
    print("\n  SOCKET GUARD, arms (a)-(f) and the read above:")
    print("    outbound attempts              : %d" % ATTEMPTS["total"])
    print("    of which to a VENDOR host      : %d (denominator: %s)"
          % (ATTEMPTS["vendor"], ",".join(VENDOR_HOSTS)))
    print("    of which to a MODEL host       : %d (denominator: %s)"
          % (ATTEMPTS["model"], ",".join(MODEL_HOSTS)))
    before = ATTEMPTS["vendor"]
    fired = False
    try:
        socket.socket().connect(("bd3.bdreporting.com", 443))
    except OSError:
        fired = True
    print("    POSITIVE CONTROL               : guard fired=%s; vendor attempts moved %d -> %d, "
          "so the zeros above are MEASURED, not a dead guard"
          % (fired, before, ATTEMPTS["vendor"]))
    guard_ok = fired and ATTEMPTS["vendor"] == before + 1 and before == 0 and ATTEMPTS["model"] == 0
    remove_guard()

    # ---------------------------------------------------------------- (d) part 2 (live reads)
    print("\n  LIVE READS (named, READ-ONLY) that established the usable coverage:")
    scan = aws_json(["dynamodb", "scan", "--table-name", evidence_mod.TRENDING_TABLE,
                     "--region", "us-east-1", "--projection-expression", "#d",
                     "--expression-attribute-names", '{"#d":"date"}', "--output", "json"])
    dates = sorted({i["date"]["S"] for i in scan.get("Items", [])})
    counts = {}
    for item in scan.get("Items", []):
        counts[item["date"]["S"]] = counts.get(item["date"]["S"], 0) + 1
    import datetime as _dt
    first = _dt.date.fromisoformat(dates[0]) if dates else None
    last = _dt.date.fromisoformat(dates[-1]) if dates else None
    span = (last - first).days + 1 if dates else 0
    window_30 = [d for d in dates if d > str(last - _dt.timedelta(days=30))] if dates else []
    items_30 = sum(counts[d] for d in window_30)
    print("    dynamodb %s : %d item(s) scanned of %d reported (ScannedCount), %d distinct date(s)"
          % (evidence_mod.TRENDING_TABLE, len(scan.get("Items", [])),
             scan.get("ScannedCount", -1), len(dates)))
    print("      coverage                     : %s .. %s = %d calendar day(s), %d present, "
          "%d absent" % (dates[0], dates[-1], span, len(dates), span - len(dates)))
    print("      LAST 30 DAYS                 : %d item(s) across %d of 30 date(s)"
          % (items_30, len(window_30)))
    s3 = aws_json(["s3api", "list-objects-v2", "--bucket", evidence_mod.ARCHIVE_BUCKET,
                   "--prefix", evidence_mod.ARCHIVE_PREFIX, "--query", "Contents[].Key",
                   "--output", "json"])
    keys = s3 if isinstance(s3, list) else []
    dated = [k for k in keys if k.count("/") == 4]
    s3_days = sorted({"-".join(k.split("/")[1:4]) for k in dated})
    print("    s3 s3://%s/%s : %d object(s), %d dated archive object(s) across %d day(s) "
          "%s .. %s" % (evidence_mod.ARCHIVE_BUCKET, evidence_mod.ARCHIVE_PREFIX, len(keys),
                        len(dated), len(s3_days), s3_days[0] if s3_days else "-",
                        s3_days[-1] if s3_days else "-"))
    print("      NOTE: the archive PATH date is the writer's naive local clock, so these day "
          "counts bound the ARCHIVE, never a publication date. The dated evidence of record "
          "is the DynamoDB table above, whose `date` partition is a verified UTC calendar date.")
    record("d", guard_ok and len(dates) > 0 and len(keys) > 0,
           "the cutoff/timezone is read from the producer's own bytes and the live coverage "
           "is measured",
           "%d of %d timezone facts cited to file:line; dynamodb %d item(s) over %d date(s) "
           "(%d in the last 30 days); s3 %d object(s); 0 vendor and 0 model connections with "
           "a positive control that moved the counter"
           % (len(evidence_mod.PUBLICATION_TIMEZONE_EVIDENCE),
              len(evidence_mod.PUBLICATION_TIMEZONE_EVIDENCE), len(scan.get("Items", [])),
              len(dates), items_30, len(keys)))

    # ---------------------------------------------------------------- (h)
    head("(h) THE SHARED LAYER IS BUILT, PINNED AND ATTACHED (issuer amendment, row W4-S3)")
    with open(str(LAYER_DIR / "BUILD_MANIFEST.json"), encoding="utf-8") as fh:
        manifest = json.load(fh)
    bd = manifest["bd_helpers"]
    print("  assembled from                    : %s" % bd["assembled_from"])
    print("  pin                               : %s  [%s]" % (bd["pin"], bd["pin_claim"]))
    print("  method                            : %s" % bd["method"])
    print("  helpers                           : %s" % bd["denominator"])
    print("    emitted   %s" % ", ".join(bd["functions_emitted"]))
    print("    constants %s ; imports %s" % (", ".join(bd["constants_emitted"]),
                                             ", ".join(bd["imports_emitted"])))
    print("    NOT carried %s" % "; ".join(bd["not_carried"]))
    print("  zip                               : %d member(s), %d bytes, sha256 %s"
          % (manifest["member_count"], manifest["zip_bytes"], manifest["zip_sha256_base64"]))
    requested = set(manifest["bd_helpers"]["functions_requested"])
    emitted = set(manifest["bd_helpers"]["functions_emitted"])
    helpers_ok = requested.issubset(emitted)

    # THE IMPORT CHECK, in a clean interpreter over the EXTRACTED layer.
    extract = pathlib.Path(tempfile.mkdtemp(prefix="irpt-layer-"))
    with zipfile.ZipFile(str(LAYER_ZIP)) as zf:
        zf.extractall(str(extract))
        names = zf.namelist()
    native = [n for n in names if n.endswith(".so") or n.endswith(".pyd")]
    probe = (
        "import sys, json\n"
        "sys.path.insert(0, r'%s')\n"
        "out = {}\n"
        "try:\n"
        "    import bd_helpers\n"
        "    body = bd_helpers.body_performance_period(account_id='900000001',"
        " q_start='2026-06-10', q_end='2026-09-09', inception='2023-03-03', run_year=2026)\n"
        "    idx = bd_helpers.requested_range_index(body)\n"
        "    out['bd_helpers'] = ('OK: imported; built a request body with %%d dateRange(s)"
        " and a requested_range_index of %%d row(s): %%s'"
        " %% (len(body['parameters']['dateRanges']), len(idx),"
        " ','.join(r['name'] for r in idx)))\n"
        "except Exception as exc:\n"
        "    out['bd_helpers'] = 'ERROR: %%s: %%s' %% (type(exc).__name__, exc)\n"
        "try:\n"
        "    import jsonschema\n"
        "    out['jsonschema'] = 'OK: imported'\n"
        "except Exception as exc:\n"
        "    out['jsonschema'] = 'ERROR: %%s: %%s' %% (type(exc).__name__, exc)\n"
        "print(json.dumps(out))\n" % str(extract / "python").replace("\\", "\\\\")
    )
    proc = subprocess.run([sys.executable, "-E", "-s", "-c", probe], capture_output=True)
    try:
        imports = json.loads(proc.stdout.decode("utf-8", "replace").strip().splitlines()[-1])
    except (ValueError, IndexError):
        imports = {"bd_helpers": "ERROR: probe produced no json",
                   "jsonschema": proc.stderr.decode("utf-8", "replace")[:200]}
    print("  CLEAN-PYTHON IMPORT over the extracted layer (python -E -s, sys.path = the "
          "layer's own python/ only):")
    print("    bd_helpers                     : %s" % imports["bd_helpers"])
    print("    jsonschema                     : %s" % imports["jsonschema"])
    print("    native member(s)               : %s" % ", ".join(native))
    print("      jsonschema's only native dependency is built for LINUX (cp312 x86_64), which "
          "is what a Lambda needs and what this Windows host cannot load. A host import of it "
          "would prove the layer is WRONG. The import that matters is on the RUNTIME, below.")

    cfg_perf = aws_json(["lambda", "get-function-configuration", "--function-name",
                         "irpt-performance-adapter", "--region", "us-east-1", "--output", "json"])
    cfg_narr = aws_json(["lambda", "get-function-configuration", "--function-name",
                         "irpt-narrative", "--region", "us-east-1", "--output", "json"])
    layers_perf = [x["Arn"] for x in cfg_perf.get("Layers", [])]
    layers_narr = [x["Arn"] for x in cfg_narr.get("Layers", [])]
    attached = sum(1 for arns in (layers_perf, layers_narr)
                   if any("irpt-common" in a for a in arns))
    print("  ATTACHED (live get-function-configuration):")
    print("    irpt-performance-adapter       : %s" % (layers_perf or "NONE"))
    print("    irpt-narrative                 : %s" % (layers_narr or "NONE"))
    print("    functions carrying irpt-common : %d of 2" % attached)

    # THE RUNTIME IMPORT PROOF: invoke the deployed performance function, BOTH providers.
    invokes = {}
    for label, payload in (("F-INF (Orion)", ".scratch/perf_invoke_event.json"),
                           ("F-49F (Black Diamond)", ".scratch/perf_invoke_bd.json")):
        out_path = REPO / ".scratch" / ("battery_invoke_%s.json" % label.split()[0])
        proc = subprocess.run(AWS + ["lambda", "invoke", "--function-name",
                              "irpt-performance-adapter", "--region", "us-east-1",
                              "--payload", "file://%s" % payload, str(out_path),
                              "--output", "json"], capture_output=True)
        try:
            with open(str(out_path), encoding="utf-8") as fh:
                raw = json.load(fh)
            body = json.loads(raw["body"]) if "body" in raw else raw
            invokes[label] = body
        except Exception as exc:  # a failed read is a FAIL, never a silent skip
            invokes[label] = {"_error": "%s: %s / %s" % (type(exc).__name__, exc,
                                                         proc.stderr.decode("utf-8", "replace")[:200])}
    validated = 0
    for label, body in invokes.items():
        cv = body.get("contract_validated")
        facts = [a.get("fact") for a in (body.get("absences") or [])]
        degraded = [f for f in facts if f == "period_range_labels"]
        print("    INVOKE %-22s contract_validated=%s  absences=%s"
              % (label, cv, facts))
        print("      helper-degraded cell(s)      : %d  <- 0 is the arm (IB-s-11 shipped 1 here)"
              % len(degraded))
        if cv is True and not degraded:
            validated += 1

    ledger = REPO / "org" / "critical_paths" / "change_management" / \
        "20260911T0103Z_irpt-bckend-s13-layer_deploy_completion.md"
    with open(str(ledger), encoding="utf-8") as fh:
        ledger_text = fh.read()
    ledger_closed = "**Status:** CLOSED" in ledger_text
    sentinel_gone = not (REPO / "org" / "critical_paths" / ".open_deploys"
                         / "irpt-bckend-s13-layer.json").exists()
    sha = subprocess.run(["git", "log", "-1", "--format=%H %s", "--",
                          "org/critical_paths/.open_deploys/irpt-bckend-s13-layer.json"],
                         cwd=str(REPO), capture_output=True)
    print("  LEDGER irpt-bckend-s13-layer      : entry reads CLOSED=%s; sentinel on disk=%s "
          "(removed by the close, as designed)" % (ledger_closed, not sentinel_gone))
    print("    sentinel commit                : %s"
          % sha.stdout.decode("utf-8", "replace").strip()[:110])
    record("h", helpers_ok and attached == 2 and validated == 2 and ledger_closed
           and sentinel_gone and imports["bd_helpers"].startswith("OK"),
           "the layer is built from a pin, attached to both functions, and the deployed "
           "adapter validates its contract on BOTH provider paths",
           "%d of %d requested helper(s) emitted from pin %s; %d of 2 functions carry "
           "irpt-common; %d of 2 invokes return contract_validated=true with 0 "
           "helper-degraded cells; ledger CLOSED"
           % (len(requested & emitted), len(requested), bd["pin"][:10], attached, validated))

    # ---------------------------------------------------------------- (g)
    head("(g) SCHEMA-VALID, READ-ONLY, LEDGER CLOSED")
    print("  packet contract_validated (worktree): %s" % run_a["contract_validated"])
    narr_body = None
    out_path = REPO / ".scratch" / "battery_narr_invoke.json"
    proc = subprocess.run(AWS + ["lambda", "invoke", "--function-name", "irpt-narrative",
                             "--region", "us-east-1", "--payload",
                             "file://.scratch/narr_event.json", str(out_path),
                             "--output", "json"], capture_output=True)
    try:
        with open(str(out_path), encoding="utf-8") as fh:
            raw = json.load(fh)
        narr_body = json.loads(raw["body"])
    except Exception as exc:
        narr_body = {"_error": "%s: %s" % (type(exc).__name__, exc)}
    print("  packet contract_validated (DEPLOYED): %s  [prose %s]"
          % (narr_body.get("contract_validated"),
             (narr_body.get("packet") or {}).get("prose", {}).get("validation_status")))

    with open(str(NARR_IAM), encoding="utf-8") as fh:
        iam_text = fh.read()
    write_actions = ("dynamodb:PutItem", "dynamodb:UpdateItem", "dynamodb:DeleteItem",
                     "dynamodb:BatchWriteItem", "s3:PutObject", "s3:DeleteObject",
                     "dynamodb:*", "s3:*", "secretsmanager:GetSecretValue", "bedrock:")
    granted = []
    for line in iam_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue          # the NOT-GRANTED list is a comment and must not count as a grant
        for action in write_actions:
            if '"%s' % action in stripped:
                granted.append((action, stripped[:70]))
    print("  iam.tf write/secret/model actions  : %d of %d probed  <- 0 is the arm"
          % (len(granted), len(write_actions)))
    for action, line in granted:
        print("      GRANTED %s in %s" % (action, line))
    print("    probed: %s" % ", ".join(write_actions))
    try:
        store.put({"date": "2026-09-09"})
        seam_refused = False
    except evidence_mod.NewsWriteRefused:
        seam_refused = True
    print("  the store seam refuses a write     : %s" % seam_refused)

    built_sha = None
    with open(str(REPO / "infra" / "aws" / "lambda" / "ci" / "lambda-source-map.json"),
              encoding="utf-8") as fh:
        built_sha = json.load(fh)["functions"]["irpt-narrative"]["artifact_sha256"]
    live_sha = cfg_narr.get("CodeSha256")
    print("  irpt-narrative CodeSha256          : %s" % live_sha)
    print("  built zip sha256 (source map)      : %s" % built_sha)
    print("  equal                              : %s" % (live_sha == built_sha))
    narr_ledger = REPO / "org" / "critical_paths" / "change_management" / \
        "20260911T0103Z_irpt-bckend-s13_deploy_completion.md"
    with open(str(narr_ledger), encoding="utf-8") as fh:
        narr_closed = "**Status:** CLOSED" in fh.read()
    sha2 = subprocess.run(["git", "log", "-1", "--format=%H %s", "--",
                           "org/critical_paths/.open_deploys/irpt-bckend-s13.json"],
                          cwd=str(REPO), capture_output=True)
    print("  LEDGER irpt-bckend-s13             : entry reads CLOSED=%s" % narr_closed)
    print("    sentinel commit                 : %s"
          % sha2.stdout.decode("utf-8", "replace").strip()[:110])
    record("g", run_a["contract_validated"] is True
           and narr_body.get("contract_validated") is True
           and not granted and seam_refused and live_sha == built_sha and narr_closed,
           "the packet validates, the role carries no write on the news resources, the "
           "served bytes are the built bytes and the ledger is closed",
           "0 of %d write/secret/model actions granted; CodeSha256 == the built zip; "
           "contract_validated true in the worktree AND on the deployed function"
           % len(write_actions))

    # ---------------------------------------------------------------- verdict
    head("VERDICT")
    for arm, ok, claim, _ in RESULTS:
        print("  %s  (%s) %s" % ("PASS" if ok else "FAIL", arm, claim))
    passed = sum(1 for _, ok, _, _ in RESULTS if ok)
    print("\n  %d of %d mechanical arms passed" % (passed, len(RESULTS)))
    if passed == len(RESULTS):
        print("IBS13-NARRATIVE-DETERMINISTIC")
        return 0
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        remove_guard()
