#!/usr/bin/env python3
"""EDGE_ROUTE_CENSUS_C1 -- POSN_AGGFIX.TO-C1-1, criterion C1-AC1 (cell AF1-s-4).

Every CloudFront behaviour of distribution EVTSA9VEHNZVH, from TWO sources with both denominators
printed: `comp-routes behaviors` and a direct parse of
infra/aws/terraform/portal-auth/cloudfront-distribution.tf. Per behaviour: path pattern, viewer-request
and origin-request functions, and whether the pattern plus the rewrite can reach the key
opal-data-portal-v2/json/positioning/opal_aggregate.json.

REACH IS DERIVED, NEVER ASSERTED. For each behaviour the key's PREIMAGES are built under that
behaviour's origin-request router (the rules `comp-routes rewrites` parses from router source, first
match honoured), or the key itself when no router runs. A behaviour reaches the key when (i) its origin
can hold the key (an S3 origin in opal-data-portal-v2, or a router that mutates the origin per firm),
(ii) its path pattern matches the preimage, and (iii) first-match precedence over the ordered behaviours
(default last) selects THIS behaviour for that preimage. An API Gateway origin is reported NOT reaching
BY ROUTE, blind stated: a key a backend Lambda computes is invisible to a route census.

A supplementary LIVE read (get-distribution-config) prints which function runs at viewer-request on the
reaching patterns as deployed, because both sources above are the DESIRED plane.
Exit: 0 = both sources parsed and agree; 1 = the sources disagree; 2 = a parse or read failed.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

DIST_ID = "EVTSA9VEHNZVH"
KEY_BUCKET = "opal-data-portal-v2"
KEY = "json/positioning/opal_aggregate.json"
TF_REL = "infra/aws/terraform/portal-auth/cloudfront-distribution.tf"
EDGE_TF_REL = "infra/aws/terraform/portal-auth/lambda-edge.tf"
ROUTER_SRC = {
    "public-data-router": "infra/aws/lambda-edge/public-data-router/index.mjs",
    "shared-advisor-router": "infra/aws/lambda-edge/shared-advisor-router/index.mjs",
}


def _root() -> Path:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return Path(out.stdout.strip())


ROOT = _root()
sys.path.insert(0, str(ROOT / ".tools"))
from git_bash_resolver import git_bash  # noqa: E402


def run_bash(cmd: str, timeout: int = 240) -> tuple[int, str, str]:
    bash = git_bash()
    if not bash:
        print("ERROR: Git Bash not resolved; refusing to fall back to bare bash")
        sys.exit(2)
    p = subprocess.run([bash, "-c", cmd], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, cwd=str(ROOT))
    return p.returncode, p.stdout, p.stderr


def pattern_re(pattern: str) -> re.Pattern:
    body = "".join(".*" if c == "*" else "." if c == "?" else re.escape(c) for c in pattern)
    return re.compile("^" + body + "$")


# ---------------------------------------------------------------- HCL (enough of it for these two files)
def _strip_comment(line: str) -> str:
    out, in_str, i = [], False, 0
    while i < len(line):
        c = line[i]
        if c == '"' and (i == 0 or line[i - 1] != "\\"):
            in_str = not in_str
        if not in_str and (c == "#" or line.startswith("//", i)):
            break
        out.append(c)
        i += 1
    return "".join(out)


def _net_braces(s: str) -> int:
    n, in_str = 0, False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != "\\"):
            in_str = not in_str
        elif not in_str:
            n += (c == "{") - (c == "}")
    return n


def parse_hcl(text: str) -> dict:
    root: dict = {"name": "<root>", "labels": [], "line": 0, "attrs": {}, "children": []}
    stack = [root]
    for n, raw in enumerate(text.split("\n"), 1):
        line = _strip_comment(raw).strip()
        if not line:
            continue
        m_block = re.match(r'^([A-Za-z_][\w-]*)((?:\s+"[^"]*")*)\s*\{$', line)
        if m_block:
            blk = {"name": m_block.group(1), "labels": re.findall(r'"([^"]*)"', m_block.group(2)),
                   "line": n, "attrs": {}, "children": []}
            stack[-1]["children"].append(blk)
            stack.append(blk)
            continue
        m_attr = re.match(r"^([A-Za-z_][\w-]*)\s*=\s*(.*)$", line)
        net = _net_braces(line)
        if m_attr:
            stack[-1]["attrs"].setdefault(m_attr.group(1), (m_attr.group(2).strip(), n))
            if net > 0:
                blk = {"name": m_attr.group(1) + "=", "labels": [], "line": n, "attrs": {}, "children": []}
                stack[-1]["children"].append(blk)
                stack.append(blk)
            continue
        for _ in range(max(0, -net)):
            if len(stack) > 1:
                stack.pop()
    return root


def _unq(v: str) -> str:
    return v.strip().strip('"')


def tf_behaviours() -> tuple[list[dict], dict]:
    tf = parse_hcl((ROOT / TF_REL).read_text(encoding="utf-8"))
    edge = parse_hcl((ROOT / EDGE_TF_REL).read_text(encoding="utf-8"))
    fn_name = {}
    for b in edge["children"]:
        if b["name"] == "resource" and b["labels"][:1] == ["aws_lambda_function"]:
            fn_name[b["labels"][1]] = _unq(b["attrs"]["function_name"][0])
    local_fn = {}
    for b in tf["children"]:
        if b["name"] == "locals":
            for k, (v, _n) in b["attrs"].items():
                m = re.search(r"aws_lambda_function\.(\w+)\[0\]", v)
                if m:
                    local_fn["local." + k] = fn_name.get(m.group(1), m.group(1))
    dist = [b for b in tf["children"]
            if b["name"] == "resource" and b["labels"] == ["aws_cloudfront_distribution", "portal"]]
    if len(dist) != 1:
        print(f"ERROR: expected 1 aws_cloudfront_distribution.portal, parsed {len(dist)}")
        sys.exit(2)
    origins = {}
    for c in dist[0]["children"]:
        if c["name"] == "origin":
            dom = _unq(c["attrs"]["domain_name"][0])
            m = re.match(r"^(.+)\.s3\.[a-z0-9-]+\.amazonaws\.com$", dom)
            origins[_unq(c["attrs"]["origin_id"][0])] = {"domain": dom, "bucket": m.group(1) if m else None}
    ordered, default = [], None
    for c in dist[0]["children"]:
        if c["name"] not in ("default_cache_behavior", "ordered_cache_behavior"):
            continue
        assoc: dict = {}
        for a in c["children"]:
            if a["name"] == "lambda_function_association":
                assoc.setdefault(_unq(a["attrs"]["event_type"][0]), []).append(
                    local_fn.get(a["attrs"]["lambda_arn"][0], a["attrs"]["lambda_arn"][0]))
            elif a["name"] == "function_association":
                fa = a["attrs"]["function_arn"][0]
                m = re.search(r"aws_cloudfront_function\.(\w+)", fa)
                assoc.setdefault(_unq(a["attrs"]["event_type"][0]), []).append(
                    "cf-function:" + (m.group(1) if m else fa))
        beh = {"pattern": _unq(c["attrs"]["path_pattern"][0]) if "path_pattern" in c["attrs"] else "/*",
               "origin": _unq(c["attrs"]["target_origin_id"][0]), "assoc": assoc, "line": c["line"]}
        if c["name"] == "default_cache_behavior":
            beh["default"] = True
            default = beh
        else:
            ordered.append(beh)
    if default is None:
        print("ERROR: no default_cache_behavior parsed")
        sys.exit(2)
    return ordered + [default], origins


# ---------------------------------------------------------------- comp-routes
def comp_routes_behaviours() -> tuple[int, list[dict]]:
    rc, out, err = run_bash("comp-routes behaviors")
    if rc != 0:
        print(f"ERROR: comp-routes behaviors rc={rc}: {err.strip()[:300]}")
        sys.exit(2)
    m = re.search(r"CLOUDFRONT BEHAVIORS \((\d+)\)", out)
    declared = int(m.group(1)) if m else -1
    items: list[dict] = []
    cur = None
    for line in out.split("\n"):
        mi = re.match(r"^\s+(\d+)\.\s+(\S+)\s*$", line)
        if mi:
            cur = {"idx": int(mi.group(1)), "pattern": mi.group(2), "origin": None, "assoc": {}}
            items.append(cur)
            continue
        if cur is None:
            continue
        mo = re.match(r"^\s+->\s+(\S+)\s+\((\w+)\)", line)
        if mo and cur["origin"] is None:
            cur["origin"] = mo.group(1)
            continue
        ma = re.match(r"^\s+(viewer-request|origin-request|origin-response|viewer-response):\s+(\S+)\s*$", line)
        if ma:
            cur["assoc"].setdefault(ma.group(1), []).append(ma.group(2))
    return declared, items


def comp_routes_rewrites() -> tuple[int, list[dict]]:
    rc, out, err = run_bash("comp-routes rewrites")
    if rc != 0:
        print(f"ERROR: comp-routes rewrites rc={rc}: {err.strip()[:300]}")
        sys.exit(2)
    m = re.search(r"URL -> S3 REWRITE RULES \((\d+)\)", out)
    declared = int(m.group(1)) if m else -1
    lines = out.split("\n")
    rules = []
    for i, line in enumerate(lines):
        mp = re.match(r"^  (/\S+)\s*$", line)
        if mp and i + 2 < len(lines):
            mt = re.match(r"^\s+->\s*(\S*)\s*$", lines[i + 1])
            md = re.match(r"^\s+\((.*)\)\s*$", lines[i + 2])
            if mt and md:
                prefix = mp.group(1)
                router = "public-data-router" if prefix.startswith("/api/general/") else "shared-advisor-router"
                rules.append({"prefix": prefix, "target": mt.group(1), "desc": md.group(1), "router": router})
    return declared, rules


def preimages(key_uri: str, rules: list[dict]) -> list[tuple[str, dict]]:
    """URIs that the router's FIRST-MATCH chain rewrites onto key_uri."""
    out = []
    for r in rules:
        if not r["target"]:
            continue
        tgt = "/" + r["target"].lstrip("/")
        if key_uri.startswith(tgt):
            cand = r["prefix"] + key_uri[len(tgt):]
            first = next((x for x in rules if cand.startswith(x["prefix"])), None)
            if first is r:
                out.append((cand, r))
    return out


def router_uri_targets(router: str) -> list[tuple[int, str]]:
    """Source-side disclosure: every request.uri assignment in the router, with its literal target prefix."""
    src = (ROOT / ROUTER_SRC[router]).read_text(encoding="utf-8").split("\n")
    consts = dict(re.findall(r'const\s+([A-Z_]+)\s*=\s*"([^"]*)"', "\n".join(src)))
    found = []
    for n, line in enumerate(src, 1):
        m = re.search(r"request\.uri\s*=\s*(.+?);", line)
        if not m:
            continue
        rhs = m.group(1)
        rep = re.search(r'request\.uri\.replace\("([^"]+)",\s*"([^"]*)"\)', rhs)
        if rep:
            found.append((n, rep.group(2)))
            continue
        lit = ""
        for p in [x.strip() for x in rhs.split("+")]:
            if p.startswith('"'):
                lit += p.strip('"')
            elif p in consts:
                lit += consts[p]
            elif p == "suffix" and lit == "/":
                guard = None
                for back in range(n - 1, max(0, n - 14), -1):
                    g = re.search(r'suffix\.startsWith\("([^"]+)"\)', src[back - 1])
                    if g:
                        guard = g.group(1)
                        break
                lit += (guard or "<suffix>")
                break
            elif p == "suffix":
                lit += "<suffix>"
                break
            else:
                lit += "<" + p + ">"
                break
        found.append((n, lit))
    return found


def main() -> int:
    key_uri = "/" + KEY
    head = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], capture_output=True, text=True,
                          cwd=str(ROOT)).stdout.strip()
    print(f"C1-AC1 EDGE_ROUTE_CENSUS_C1 -- distribution {DIST_ID}; key s3://{KEY_BUCKET}/{KEY}")
    print(f"vintage: repo HEAD {head} (DESIRED plane: TF + router source); a live read closes the output")

    tf_list, origins = tf_behaviours()
    cr_declared, cr_list = comp_routes_behaviours()
    rw_declared, rules = comp_routes_rewrites()
    print(f"DENOMINATOR comp-routes behaviors: header {cr_declared}, parsed {len(cr_list)}")
    print(f"DENOMINATOR {TF_REL}: parsed {len(tf_list)} (ordered {len(tf_list) - 1} + default 1); "
          f"origins {len(origins)}")
    print(f"DENOMINATOR comp-routes rewrites: header {rw_declared}, parsed {len(rules)}")

    # comp-routes numbers the default 0 and the ordered behaviours from 1; CloudFront evaluates the default last.
    cr_seq = [x for x in cr_list if x["idx"] != 0] + [x for x in cr_list if x["idx"] == 0]
    agree, disagreements = 0, []
    for i in range(max(len(tf_list), len(cr_seq))):
        t = tf_list[i] if i < len(tf_list) else None
        c = cr_seq[i] if i < len(cr_seq) else None
        tf_assoc = ({k: v for k, v in t["assoc"].items() if not any(s.startswith("cf-function:") for s in v)}
                    if t else {})
        if t and c and t["pattern"] == c["pattern"] and t["origin"] == c["origin"] and tf_assoc == c["assoc"]:
            agree += 1
        else:
            disagreements.append((i, t and t["pattern"], c and c["pattern"]))
    print(f"SOURCES AGREE (pattern, origin, lambda associations, precedence position): {agree} of {len(tf_list)}")
    for d in disagreements:
        print(f"  DISAGREE at position {d[0]}: tf={d[1]} comp-routes={d[2]}")

    for router, rel in ROUTER_SRC.items():
        src_text = (ROOT / rel).read_text(encoding="utf-8")
        rr = [r for r in rules if r["router"] == router]
        present = sum(1 for r in rr if r["prefix"] in src_text
                      or r["prefix"].split("/api/scoped/advisor-intelligence/")[-1] in src_text)
        print(f"REWRITE RULES {router}: {len(rr)} parsed by comp-routes; prefix literal in router source "
              f"{present} of {len(rr)}")
        for n, lit in router_uri_targets(router):
            flag = "   <-- /json/ TARGET" if lit.startswith("/json/") else ""
            print(f"  source {rel}:{n} request.uri -> {lit!r}{flag}")

    def first_match(uri: str) -> int:
        for i, b in enumerate(tf_list):
            if pattern_re(b["pattern"]).match(uri):
                return i
        return -1

    print("")
    print("BEHAVIOURS (CloudFront precedence order; the default is evaluated last)")
    print(f"{'pos':>3}  {'path pattern':<50} {'origin':<28} {'viewer-request':<34} {'origin-request':<22} reach")
    reaching = []
    for i, b in enumerate(tf_list):
        o = origins.get(b["origin"], {})
        vr = ",".join(b["assoc"].get("viewer-request", [])) or "-"
        orq = ",".join(b["assoc"].get("origin-request", [])) or "-"
        routers = [f for f in b["assoc"].get("origin-request", []) if f in ROUTER_SRC]
        forms: list[tuple[str, str]] = []
        if o.get("bucket") is None:
            verdict = "NO (API Gateway origin: no S3 key by route; a backend-computed key is invisible here)"
        elif o.get("bucket") != KEY_BUCKET and "shared-advisor-router" not in routers:
            verdict = f"NO (origin bucket {o.get('bucket')} cannot hold the key)"
        else:
            if routers:
                cands = [(u, r["desc"]) for rt in routers
                         for (u, r) in preimages(key_uri, [x for x in rules if x["router"] == rt])]
            else:
                cands = [(key_uri, "no router: the URI is the key")]
            notes = []
            for u, why in cands:
                if not pattern_re(b["pattern"]).match(u):
                    notes.append(f"{u} does not match the pattern")
                elif first_match(u) != i:
                    notes.append(f"{u} is taken first by {tf_list[first_match(u)]['pattern']}")
                else:
                    forms.append((u, why))
            if forms:
                verdict = "YES"
            elif not cands:
                verdict = "NO (no rewrite rule of this router targets /json/)"
            else:
                verdict = "NO (" + "; ".join(notes) + ")"
        tag = " [default]" if b.get("default") else ""
        print(f"{i:>3}  {(b['pattern'] + tag):<50} {b['origin']:<28} {vr:<34} {orq:<22} {verdict}")
        if forms:
            reaching.append((i, b, forms))

    print("")
    guarded = 0
    for i, b, forms in reaching:
        has = "auth-validator-edge" in b["assoc"].get("viewer-request", [])
        guarded += int(has)
        print(f"REACHING BEHAVIOUR pos {i} pattern {b['pattern']} (cloudfront-distribution.tf:{b['line']}) "
              f"viewer-request auth-validator-edge: {'YES' if has else 'NO'}")
        for u, why in forms:
            print(f"  URL form {u}   via rule: {why}")
    print(f"REACHING {len(reaching)} -- AUTH-VALIDATOR AT VIEWER-REQUEST {guarded} of {len(reaching)}")

    rc, out, err = run_bash(f"aws cloudfront get-distribution-config --id {DIST_ID} --output json")
    if rc != 0:
        print(f"LIVE: get-distribution-config rc={rc} ({err.strip()[:200]}) -- live supplementary NOT read")
    else:
        live = json.loads(out)
        cfg = live["DistributionConfig"]
        lb = [(x["PathPattern"], x) for x in cfg["CacheBehaviors"].get("Items", [])]
        print(f"LIVE (get-distribution-config, ETag {live.get('ETag')}): behaviours {len(lb) + 1} "
              f"(ordered {len(lb)} + default 1)")
        for _i, b, _forms in reaching:
            hits = [x for p, x in lb if p == b["pattern"]]
            for x in hits:
                vr = [a["LambdaFunctionARN"].split(":function:")[-1]
                      for a in x.get("LambdaFunctionAssociations", {}).get("Items", [])
                      if a["EventType"] == "viewer-request"]
                print(f"  LIVE {b['pattern']}: viewer-request {vr}")
            if not hits:
                print(f"  LIVE {b['pattern']}: ABSENT from the live distribution")
    return 1 if disagreements else 0


if __name__ == "__main__":
    sys.exit(main())
