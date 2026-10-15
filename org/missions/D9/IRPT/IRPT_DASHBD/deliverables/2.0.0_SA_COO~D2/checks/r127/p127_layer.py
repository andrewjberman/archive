"""IRPT_DASHBD round 127, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-259, the COTTONWOOD LANDING ROOT GAINS ITS PYARROW LAYER. The merged root builds the function
`irpt-cot-account-return-daily-lambda` with NO layer, while the adapter it packages imports pyarrow at module level and the python3.12 runtime does not carry pyarrow: the first event
would fail on import. The sibling Cottonwood function (account-dim) takes pandas/pyarrow from the EXISTING `irpt-performance-native-layer` through a read-only data source; this cell does
the same for the landing root and nothing else. A data source adds no resource, so the expected plan stays 7 add / 0 change / 0 destroy. LOCAL: nothing is planned, applied or deployed.

  DB-b-259 (~212)   lambda.tf: the read-only layer data source and `layers = [...]` on the module call; a facts record
                    DB127-1-AC1 (the HCL: only the data source and the layers line are new, nothing else in the root moves),
                    DB127-1-AC2 (FRESH live read: the layer's latest version, its runtime, the sibling function's use, and the record equals them),
                    DB127-1-AC3 (the layer's zip holds pyarrow; the bundle's import-time third-party imports (module level, not inside try, function or class bodies) are exactly pyarrow plus the runtime's boto3/botocore)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms
"""
import ast
import json
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~212/RD_COT_LAYER_FACTS_R127.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-259.cottonwood-landing-root-pyarrow-layer-from-the-existing-native-layer.md"
ROOT_DIR = "infra/aws/terraform/investor-reporting/account-return-daily/"
LAMBDA_TF = ROOT_DIR + "lambda.tf"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
ENTRY_KEY = "irpt-cot-account-return-daily-lambda"
LAYER_NAME = "irpt-performance-native-layer"
DATA_NAME = "irpt_performance_native"
SIBLING = "irpt-cot-account-dim-lambda"
RUNTIME_PROVIDED = {"boto3", "botocore"}
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "layer_arn", "sibling_layer_arn")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout.decode("utf-8", "replace"), r.returncode


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.split()[-1]


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


DATA_BLOCK = re.compile(r'data\s+"aws_lambda_layer_version"\s+"%s"\s*\{\s*layer_name\s*=\s*"%s"\s*\}' % (DATA_NAME, re.escape(LAYER_NAME)))
LAYERS_LINE = re.compile(r"^\s*layers\s*=\s*\[\s*data\.aws_lambda_layer_version\.%s\.arn\s*\]\s*$" % DATA_NAME)


def norm_code(text):
    return [" ".join(ln.split()) for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


# ------------------------------------------------------------------------------------------------ pure clauses
def check_hcl(base_text, new_text):
    need(len(DATA_BLOCK.findall(new_text)) == 1, "lambda.tf must hold exactly one read-only data source for %s" % LAYER_NAME)
    stripped = DATA_BLOCK.sub("", new_text)
    lines = stripped.splitlines()
    hits = [i for i, ln in enumerate(lines) if LAYERS_LINE.match(ln)]
    need(len(hits) == 1, "the module call must carry exactly one `layers = [data.aws_lambda_layer_version.%s.arn]` line" % DATA_NAME)
    del lines[hits[0]]
    need(norm_code("\n".join(lines)) == norm_code(base_text), "anything beyond the data source and the layers line changed in the code (comments excluded, spacing normalised)")
    comments = "\n".join(ln for ln in new_text.splitlines() if ln.lstrip().startswith("#"))
    need("pyarrow" in comments and LAYER_NAME in comments, "a comment must say pyarrow comes from %s" % LAYER_NAME)
    need(re.search(r"memory_size\s*=\s*1024", new_text) and re.search(r"timeout\s*=\s*900", new_text), "memory 1024 and timeout 900 must stay")
    return True


def import_time_names(body):
    """Top-level names imported when the module is IMPORTED: module-level statements, descending into if/with blocks, never into function or class bodies and never into a try
    block (a guarded import is a fallback, not a requirement)."""
    out = set()
    for node in body:
        if isinstance(node, ast.Import):
            out |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            out.add(node.module.split(".")[0])
        elif isinstance(node, (ast.If, ast.With)):
            out |= import_time_names(node.body)
            if isinstance(node, ast.If):
                out |= import_time_names(node.orelse)
    return out


def third_party(sources, bundle_modules):
    """sources: {name: source text} of the bundle's python files; returns the sorted set of import-time top-level imports that are neither stdlib nor bundle modules."""
    std = set(sys.stdlib_module_names)
    found = set()
    for name, src in sources.items():
        found |= import_time_names(ast.parse(src, filename=name).body)
    return sorted(m for m in found if m not in std and m not in bundle_modules and m != "__future__")


def check_imports(tp, layer_has):
    need(set(tp) - RUNTIME_PROVIDED == {"pyarrow"}, "the bundle's third-party imports besides boto3/botocore must be exactly pyarrow, read %s" % sorted(set(tp) - RUNTIME_PROVIDED))
    need(layer_has("python/pyarrow/__init__.py"), "the layer zip does not hold python/pyarrow/__init__.py")
    return True


def check_facts(rec, live):
    exp = {"layer_name", "layer_version", "compatible_runtimes", "sibling_function", "sibling_layer_arn", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    need(rec["layer_name"] == LAYER_NAME and rec["sibling_function"] == SIBLING, "layer_name or sibling_function")
    need(rec["layer_version"] == live["latest_version"] and rec["compatible_runtimes"] == live["runtimes"] and "python3.12" in live["runtimes"], "layer version or runtimes differ from the live read (%s)" % live)
    need(rec["sibling_layer_arn"] == live["sibling_layer_arn"] and live["sibling_layer_arn"].endswith(":%s:%d" % (LAYER_NAME, live["latest_version"])),
         "the sibling function must use the layer's LATEST version, so the data source resolves to the version the sibling is proven on: %s" % live["sibling_layer_arn"])
    need(isinstance(rec["words"], str) and 80 <= len(rec["words"]) <= 1500, "words must be one paragraph of 80 to 1500 characters")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def live_layer():
    import boto3
    lam = boto3.client("lambda", region_name="us-east-1")
    vs = lam.list_layer_versions(LayerName=LAYER_NAME)["LayerVersions"]
    latest = max(vs, key=lambda v: v["Version"])
    sib = lam.get_function_configuration(FunctionName=SIBLING)
    arns = [x["Arn"] for x in sib.get("Layers", [])]
    return {"latest_version": latest["Version"], "runtimes": latest.get("CompatibleRuntimes", []), "sibling_layer_arn": arns[0] if arns else "", "sibling_runtime": sib["Runtime"]}


def layer_namelist(version):
    import boto3
    lam = boto3.client("lambda", region_name="us-east-1")
    url = lam.get_layer_version(LayerName=LAYER_NAME, VersionNumber=version)["Content"]["Location"]
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "layer.zip"
        urllib.request.urlretrieve(url, str(p))
        with zipfile.ZipFile(p) as z:
            names = set(z.namelist())
    return names


def run(root, cid):
    root = Path(root)
    base = base_commit(root)
    if cid == "DB127-1-AC1":
        bt, rc = git(root, "show", "%s:%s" % (base, LAMBDA_TF))
        need(rc == 0, "cannot read the base lambda.tf")
        check_hcl(bt, (root / LAMBDA_TF).read_text(encoding="utf-8"))
        others, _ = git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", ROOT_DIR)
        n = 0
        for f in others.split():
            if f != LAMBDA_TF:
                need(git(root, "show", "HEAD:" + f)[0] == git(root, "show", "%s:%s" % (base, f))[0], "another root file changed: %s" % f)
                n += 1
        print("OK: lambda.tf gains one read-only data source for %s and one layers line on the module call; no other code line moves; %d other root files byte-equal to the base" % (LAYER_NAME, n))
        return True
    lv = live_layer()
    if cid == "DB127-1-AC2":
        rec = json.loads((root / REC_REL).read_text(encoding="utf-8"))
        check_facts(rec, lv)
        print("OK: layer %s latest version %d, runtimes %s, the sibling %s runs python3.12 on that version; the record equals the live read" % (LAYER_NAME, lv["latest_version"], lv["runtimes"], SIBLING))
        return True
    if cid == "DB127-1-AC3":
        tf = (root / LAMBDA_TF).read_text(encoding="utf-8")
        need(DATA_BLOCK.search(tf) is not None and any(LAYERS_LINE.match(ln) for ln in tf.splitlines()), "the root does not attach the layer yet (no data source or no layers line in lambda.tf)")
        sm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))["functions"][ENTRY_KEY]
        sources = {}
        for f in sm["files"]:
            if f.endswith(".py"):
                rel = sm["source_dir"] + "/" + f if f == "handler.py" else f
                sources[f] = (root / rel).read_text(encoding="utf-8")
        mods = {Path(f).stem for f in sources}
        tp = third_party(sources, mods)
        names = layer_namelist(lv["latest_version"])
        check_imports(tp, lambda n: n in names)
        print("OK: the bundle's third-party imports are %s; the layer zip (version %d, %d entries) holds python/pyarrow/__init__.py" % (tp, lv["latest_version"], len(names)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    base = '# top\nmodule "m" {\n  timeout     = 900\n  memory_size = 1024\n  reserved_concurrent_executions = 1\n}\n'
    good = ('# pyarrow comes from the existing %s\ndata "aws_lambda_layer_version" "%s" {\n  layer_name = "%s"\n}\n\nmodule "m" {\n  timeout     = 900\n  memory_size = 1024\n'
            '  layers      = [data.aws_lambda_layer_version.%s.arn]\n  reserved_concurrent_executions = 1\n}\n') % (LAYER_NAME, DATA_NAME, LAYER_NAME, DATA_NAME)
    assert check_hcl(base, good)
    red(lambda: check_hcl(base, base), "no layer")
    red(lambda: check_hcl(base, good.replace("= 1024", "= 2048")), "memory changed")
    red(lambda: check_hcl(base, good.replace("= 900", "= 600")), "timeout changed")
    red(lambda: check_hcl(base, good.replace(LAYER_NAME, "other-layer", 1).replace('"%s"' % LAYER_NAME, '"other-layer"')), "wrong layer")
    red(lambda: check_hcl(base, good + 'resource "x" "y" {}\n'), "extra code")
    red(lambda: check_hcl(base, good.replace("# pyarrow comes from the existing %s" % LAYER_NAME, "# layer")), "no comment")
    red(lambda: check_hcl(base, good.replace("  layers      = [data.aws_lambda_layer_version.%s.arn]\n" % DATA_NAME, "  layers      = []\n")), "layers line wrong")
    src = {"handler.py": "import json\nfrom pathlib import Path\nimport opal_naming\n", "adapter.py": "from __future__ import annotations\nimport pyarrow as pa\nimport pyarrow.parquet as pq\nimport boto3\n"}
    tp = third_party(src, {"opal_naming", "handler", "adapter"})
    assert tp == ["boto3", "pyarrow"], tp
    lazy = {"a.py": "import json\ntry:\n    import pandas_market_calendars\nexcept ImportError:\n    pass\ndef f():\n    import psutil\nclass C:\n    import numpy\nif True:\n    import requests\n"}
    assert third_party(lazy, set()) == ["requests"], third_party(lazy, set())
    assert check_imports(tp, lambda n: True)
    red(lambda: check_imports(tp, lambda n: False), "layer lacks pyarrow")
    red(lambda: check_imports(["boto3", "pyarrow", "pandas"], lambda n: True), "extra third party")
    red(lambda: check_imports(["boto3"], lambda n: True), "no pyarrow")
    live = {"latest_version": 1, "runtimes": ["python3.12"], "sibling_layer_arn": "arn:x:layer:%s:1" % LAYER_NAME}
    rec = {"layer_name": LAYER_NAME, "layer_version": 1, "compatible_runtimes": ["python3.12"], "sibling_function": SIBLING, "sibling_layer_arn": "arn:x:layer:%s:1" % LAYER_NAME, "words": "w" * 100}
    assert check_facts(rec, live)
    for label, fn in (("version", lambda r: r.update(layer_version=2)), ("runtimes", lambda r: r.update(compatible_runtimes=[])), ("sibling", lambda r: r.update(sibling_function="x")),
                      ("arn", lambda r: r.update(sibling_layer_arn="arn:x:layer:%s:2" % LAYER_NAME)), ("words", lambda r: r.update(words="short")), ("extra", lambda r: r.update(z=1)),
                      ("digits", lambda r: r.update(words="w" * 100 + " 123456789"))):
        r2 = dict(rec)
        fn(r2)
        red(lambda: check_facts(r2, live), label)
    red(lambda: check_facts(rec, dict(live, latest_version=2)), "live moved on")
    print("selftest: hcl (7 red arms), imports (3 red arms) and facts (8 red arms) clauses behave")
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except (Fail, OSError, ValueError, KeyError, TypeError, IndexError) as e:
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
