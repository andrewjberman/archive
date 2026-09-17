#!/usr/bin/env python
"""NFRA_OPLGTW OG-i-3 probe -- the ALB's explicit browser paths, one function per acceptance criterion.

Usage: og_i3.py <AC-short-id>   e.g. og_i3.py AC1

Prints its measurement with vintage and denominator, then exactly one line:
  VERDICT: PASS-OGI3-AC<n>
  VERDICT: FAIL-OGI3-AC<n> <reason>

The HTTP arm (AC4) makes unauthenticated GETs to https://mcp.opalinvest.dev without following
redirects and records status and Location only -- Opal infrastructure, no vendor egress.
"""
from __future__ import annotations

import http.client
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
DELIV = HERE.parent
EVID = DELIV / "evidence" / "og_i3"

LISTENER_ARN = "arn:aws:elasticloadbalancing:us-east-1:313476888478:listener/app/opal-gateway/89166a68f337e5a4/2904a0140214f982"
HTTP_LISTENER_ARN = "arn:aws:elasticloadbalancing:us-east-1:313476888478:listener/app/opal-gateway/89166a68f337e5a4/a72b21be9d935e5c"
ALB_ARN = "arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4"
HOST = "mcp.opalinvest.dev"


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def say(*a):
    print(*a)


def _ws() -> Path:
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, cwd=str(HERE))
    return Path(r.stdout.strip())


WS = _ws()


def _run(cmd, timeout=90):
    say(f"+ {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def aws(*args, timeout=90):
    # This probe runs under a native-Windows Python (.venv-og), which cannot exec the extensionless
    # bash shim directly (WinError 193 -- no shebang support in CreateProcess); .tools/aws.cmd is the
    # Windows-shell companion that resolves to the same real CLI (CLAUDE.md Git section).
    cmd = [str(WS / ".tools" / "aws.cmd"), *args, "--output", "json"]
    r = _run(cmd, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"aws {' '.join(args)} failed rc={r.returncode}: {r.stderr.strip()[:400]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def _pass(ac):
    say(f"VERDICT: PASS-OGI3-{ac}")
    return 0


def _fail(ac, reason):
    say(f"VERDICT: FAIL-OGI3-{ac} {reason}")
    return 1


# --------------------------------------------------------------------------------------- the inputs
def _browser_paths() -> list:
    """The exact four paths, from the two merged records -- NEVER typed. BLOCKING if either is
    absent at HEAD (order text, THE CELL)."""
    a3 = WS / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~3/BROWSER_PATHS.json"
    x1 = WS / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~5/DOWNLOAD_PATHS.json"
    if not a3.exists() or not x1.exists():
        raise RuntimeError(f"BLOCKING: a path record is absent -- a3.exists()={a3.exists()} x1.exists()={x1.exists()}")
    a3d, x1d = load_json(a3), load_json(x1)
    paths = [p["path"] for p in a3d["paths"]] + [p["path"] for p in x1d["paths"]]
    return sorted(paths)


def _baseline() -> dict:
    return load_json(WS / "org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/BASELINE.json")


def _plan_resource_changes() -> list:
    return load_json(EVID / "plan.json")["resource_changes"]


def _live_rules() -> dict:
    return load_json(EVID / "live_rules.json")


def _live_waf() -> dict:
    return load_json(EVID / "live_waf.json")


# --------------------------------------------------------------------------------------------- AC1
def ac1():
    """The plan changes only listener rules for the exact download/OIDC-callback paths, default
    action unchanged."""
    wanted = _browser_paths()
    rc = _plan_resource_changes()
    say(f"instrument: saved plan JSON (terraform show -json), pre-apply {EVID / 'plan.json'}")
    say(f"vintage: {_utcnow()} (plan taken 2026-09-17, applied same session, unchanged since)")
    non_noop = [r for r in rc if r["change"]["actions"] != ["no-op"]]
    say(f"denominator: {len(rc)} resource_changes total, {len(non_noop)} non-no-op")
    lb_related = [r for r in non_noop if r["type"].startswith("aws_lb")]
    say("non-no-op aws_lb* resources: " + ", ".join(f"{r['address']}={r['change']['actions']}" for r in lb_related))
    if len(lb_related) != 1:
        return _fail("AC1", f"expected exactly 1 non-no-op aws_lb* resource, found {len(lb_related)}")
    r = lb_related[0]
    if r["type"] != "aws_lb_listener_rule" or r["change"]["actions"] != ["create"]:
        return _fail("AC1", f"the one aws_lb* change is {r['address']} {r['type']} {r['change']['actions']}, not a new listener rule")
    after = r["change"]["after"]
    if after.get("listener_arn") != LISTENER_ARN:
        return _fail("AC1", f"new rule's listener_arn {after.get('listener_arn')} != the HTTPS listener")
    values = sorted(after["condition"][0]["path_pattern"][0]["values"])
    say(f"new rule priority={after.get('priority')} path_pattern values={values}")
    if values != wanted:
        return _fail("AC1", f"new rule's path_pattern values {values} != the two merged records' paths {wanted}")
    actions = after.get("action", [])
    if len(actions) != 1 or actions[0].get("type") != "forward":
        return _fail("AC1", f"new rule's action is not a plain forward: {actions}")
    # default action unchanged: no resource_changes entry for aws_lb_listener.https with a non-no-op action.
    https_listener = [r for r in rc if r["address"] == "aws_lb_listener.https"]
    if https_listener and https_listener[0]["change"]["actions"] != ["no-op"]:
        return _fail("AC1", f"aws_lb_listener.https changed: {https_listener[0]['change']['actions']}")
    say("aws_lb_listener.https: no-op (absent from non-no-op set)" if not https_listener else "aws_lb_listener.https: no-op")
    return _pass("AC1")


# --------------------------------------------------------------------------------------------- AC2
def ac2():
    """The apply runs through safe-apply under a ledger entry opened and committed before the act
    and closed before the reads."""
    slug = "nfra-oplgtw-og-i-3-alb-paths"
    md_glob = list((WS / "org/critical_paths/change_management").glob(f"*_{slug}_deploy_completion.md"))
    say(f"instrument: git log + the deploy-completion record; slug={slug}")
    if len(md_glob) != 1:
        return _fail("AC2", f"expected exactly 1 completion record for {slug}, found {len(md_glob)}")
    md = md_glob[0]
    text = md.read_text(encoding="utf-8")
    say(f"record: {md.relative_to(WS)}")
    if "**Status:** CLOSED" not in text:
        return _fail("AC2", f"{md.name} is not CLOSED at read time")
    sentinel = WS / "org/critical_paths/.open_deploys" / f"{slug}.json"
    r = _run(["git", "-C", str(WS), "log", "--format=%H %cI %s", "--follow", "--", str(md.relative_to(WS))])
    commits = [line for line in r.stdout.splitlines() if line.strip()]
    say(f"denominator: {len(commits)} commit(s) touched the completion record")
    for c in commits:
        say(f"  {c}")
    if len(commits) < 2:
        return _fail("AC2", f"expected >=2 commits (open, close) on the completion record, found {len(commits)}")
    r2 = _run(["git", "-C", str(WS), "log", "--format=%cI %s", "--", str(sentinel.relative_to(WS))])
    say(f"sentinel {sentinel.relative_to(WS)} history: {r2.stdout.strip()!r}")
    if sentinel.exists():
        return _fail("AC2", "the open-deploys sentinel is still present (deploy_ledger.py close removes it)")
    if not r2.stdout.strip():
        return _fail("AC2", "the open-deploys sentinel has no commit history at all (never opened)")
    # apply ran through safe-apply.sh: evidence is this session's own apply log naming safe-apply's gates.
    applylog = EVID / "apply.log"
    if not applylog.exists():
        return _fail("AC2", f"no apply.log evidence at {applylog}")
    alog = applylog.read_text(encoding="utf-8", errors="replace")
    markers = ["HALT-GATE:", "naming-apply-gate", "naming-plan-gate", "comp-tagauthz", "tombstone-gate", "Apply complete!"]
    missing = [m for m in markers if m not in alog]
    say(f"apply.log markers present: {[m for m in markers if m not in missing]}; missing: {missing}")
    if missing:
        return _fail("AC2", f"apply.log is missing safe-apply gate marker(s): {missing}")
    return _pass("AC2")


# --------------------------------------------------------------------------------------------- AC3
def _rule_key(rule):
    conds = sorted(
        (c.get("Field"), tuple(sorted(c.get("Values", []))))
        for c in rule.get("Conditions", [])
    )
    actions = sorted((a.get("Type"), a.get("TargetGroupArn")) for a in rule.get("Actions", []))
    return (rule.get("Priority"), tuple(conds), tuple(actions))


def ac3():
    """Every pre-existing rule reads back byte-equal to OG-p-1's baseline."""
    baseline = _baseline()["OGP1-AC3"]["measurement"]
    live = _live_rules()
    say(f"instrument: elbv2 describe-rules (live, {EVID / 'live_rules.json'}) vs OG-p-1 baseline "
        f"(measured_utc {_baseline()['OGP1-AC3']['measured_utc']})")
    base_https = next(lst for lst in baseline["listeners"] if lst["Port"] == 443)
    base_http = next(lst for lst in baseline["listeners"] if lst["Port"] == 80)
    base_rules = {r["RuleArn"]: _rule_key(r) for r in base_https["rules"]}
    live_rules = {r["RuleArn"]: _rule_key(r) for r in live["Rules"]}
    say(f"denominator: {len(base_rules)} baseline rule(s) on the HTTPS listener")
    new_rule_prios = {r["Priority"] for r in live["Rules"]} - {r["Priority"] for r in base_https["rules"]}
    say(f"new priorities in live HTTPS listener vs baseline: {new_rule_prios} (expect exactly {{'34'}})")
    missing = [arn for arn in base_rules if arn not in live_rules]
    changed = [arn for arn in base_rules if arn in live_rules and live_rules[arn] != base_rules[arn]]
    say(f"missing from live: {len(missing)}; changed: {len(changed)}")
    if missing or changed:
        return _fail("AC3", f"missing={missing} changed={changed}")
    if new_rule_prios != {"34"}:
        return _fail("AC3", f"unexpected new priority set {new_rule_prios}, expected only 34")
    # also the HTTP:80 redirect listener's default rule, byte-equal.
    http_live = aws("elbv2", "describe-rules", "--listener-arn", HTTP_LISTENER_ARN)["Rules"]
    say(f"HTTP:80 listener: {len(http_live)} rule(s) (baseline: {len(base_http['rules'])})")
    if len(http_live) != 1 or http_live[0].get("Priority") != "default":
        return _fail("AC3", "HTTP:80 listener's rule set changed shape")
    if _rule_key(http_live[0]) != _rule_key(base_http["rules"][0]):
        return _fail("AC3", "HTTP:80 listener's default rule differs from baseline")
    return _pass("AC3")


# --------------------------------------------------------------------------------------------- AC4
def _get_no_redirect(path: str) -> tuple:
    conn = http.client.HTTPSConnection(HOST, 443, timeout=15)
    try:
        conn.request("GET", path, headers={"Host": HOST})
        resp = conn.getresponse()
        resp.read(200)  # drain so the connection can close cleanly; content is not graded
        return resp.status, resp.getheader("Location"), resp.getheader("server")
    finally:
        conn.close()


def ac4():
    """An unauthenticated GET to an unrelated path still redirects to the ALB login, while the
    same request to an explicit path reaches the application (status and Location recorded)."""
    unrelated = "/og-i-3-unrelated-probe-path"
    explicit = _browser_paths()
    say(f"instrument: unauthenticated HTTPS GET, no redirect follow, https://{HOST}; vintage {_utcnow()}")
    say(f"denominator: 1 unrelated path + {len(explicit)} explicit path(s)")
    u_status, u_loc, u_server = _get_no_redirect(unrelated)
    say(f"unrelated {unrelated}: status={u_status} Location={u_loc} server={u_server}")
    if u_status != 302 or not u_loc or "login.microsoftonline.com" not in u_loc:
        return _fail("AC4", f"unrelated path did not redirect to Entra: status={u_status} Location={u_loc}")
    results = []
    for p in explicit:
        st, loc, server = _get_no_redirect(p)
        say(f"explicit {p}: status={st} Location={loc} server={server}")
        results.append((p, st, loc, server))
    reached_app = [p for p, st, loc, server in results if loc is None and server == "uvicorn"]
    say(f"explicit path(s) that reached the application (no Location, server=uvicorn): {len(reached_app)} of {len(explicit)}")
    if len(reached_app) != len(explicit):
        return _fail("AC4", f"not every explicit path reached the application: {results}")
    return _pass("AC4")


# --------------------------------------------------------------------------------------------- AC5
def ac5():
    """The idle_timeout is read back with its ARN and UTC time."""
    attrs = aws("elbv2", "describe-load-balancer-attributes", "--load-balancer-arn", ALB_ARN)["Attributes"]
    vintage = _utcnow()
    val = next((a["Value"] for a in attrs if a["Key"] == "idle_timeout.timeout_seconds"), None)
    say(f"instrument: elbv2 describe-load-balancer-attributes, resource {ALB_ARN}")
    say(f"idle_timeout.timeout_seconds={val} (read {vintage})")
    baseline_val = _baseline()["OGP1-AC3"]["measurement"]["idle_timeout_seconds"]
    say(f"baseline idle_timeout_seconds={baseline_val}")
    if val is None:
        return _fail("AC5", "idle_timeout.timeout_seconds not present in the read")
    if val != baseline_val:
        return _fail("AC5", f"idle_timeout {val} != baseline {baseline_val}")
    return _pass("AC5")


# --------------------------------------------------------------------------------------------- AC6
def ac6():
    """The WAF association equals OG-p-1's baseline."""
    baseline = _baseline()["OGP1-AC3"]["measurement"]["waf"]["WebACL"]
    live = _live_waf()["WebACL"]
    say(f"instrument: wafv2 get-web-acl-for-resource, resource {ALB_ARN}, vintage {_utcnow()}")
    say(f"live: {live['Name']} {live['ARN']} rules={[r['Name'] for r in live['Rules']]}")
    say(f"baseline: {baseline['Name']} {baseline['ARN']} rules={[r['Name'] for r in baseline['Rules']]}")
    if live["ARN"] != baseline["ARN"] or live["Name"] != baseline["Name"]:
        return _fail("AC6", f"WAF identity differs: live={live['ARN']} baseline={baseline['ARN']}")
    live_rules = sorted((r["Name"], r["Priority"]) for r in live["Rules"])
    base_rules = sorted((r["Name"], r["Priority"]) for r in baseline["Rules"])
    if live_rules != base_rules:
        return _fail("AC6", f"WAF rule set differs: live={live_rules} baseline={base_rules}")
    return _pass("AC6")


FUNCS = {"AC1": ac1, "AC2": ac2, "AC3": ac3, "AC4": ac4, "AC5": ac5, "AC6": ac6}


def main(argv):
    if len(argv) != 2 or argv[1] not in FUNCS:
        say(f"usage: og_i3.py <{'|'.join(FUNCS)}>")
        return 2
    try:
        return FUNCS[argv[1]]()
    except Exception as exc:  # noqa: BLE001 -- a probe that cannot answer prints FAIL, never raises past main
        return _fail(argv[1], f"EXCEPTION {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
