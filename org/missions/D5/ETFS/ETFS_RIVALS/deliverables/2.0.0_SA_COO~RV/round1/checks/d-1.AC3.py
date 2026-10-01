"""RIV-d-1 AC3 -- comp-iam instrument + rule 30: the stack's names, prefixes and role policies are GENERATED from
address()/name() (regenerated here, byte-equal to what is committed), and IAM's own simulator confirms each role
writes only inside the builder prefixes: never the bucket's tier-first roots, never opal-data-assets, never a Delete."""
import filecmp
import json
import pathlib
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _common as c  # noqa: E402


def run(v):
    import boto3

    root = c.setup_path()
    stack = root / "infra" / "aws" / "terraform" / "etfs-rivalfunds"
    gen = stack / "gen_policies.py"
    v.check(gen.exists(), "gen_policies.py exists")
    if not gen.exists():
        return
    tmp = pathlib.Path(c.tmpdir("rv_d1d_"))
    r = subprocess.run([sys.executable, str(gen), "--out", str(tmp)], capture_output=True, text=True)
    v.check(r.returncode == 0, f"generator rc={r.returncode} {r.stderr[-300:]}")
    committed = sorted(p.relative_to(stack).as_posix() for p in list((stack / "policies").glob("*.json")) + [stack / "generated.auto.tfvars.json"] if p.exists())
    regen = sorted(p.relative_to(tmp).as_posix() for p in tmp.rglob("*.json"))
    v.check(committed == regen and all(filecmp.cmp(stack / f, tmp / f, shallow=False) for f in committed),
            f"committed generated files equal a fresh regeneration ({len(committed)} file(s))")
    pols = sorted((stack / "policies").glob("*.json"))
    v.check(len(pols) == 5, f"one role policy per Lambda ({len(pols)})")
    iam = boto3.client("iam")
    arn = lambda u: "arn:aws:s3:::" + u[len("s3://"):]  # noqa: E731
    never = ["arn:aws:s3:::opal-data-etfs/bronze/x", "arn:aws:s3:::opal-data-etfs/silver/x", "arn:aws:s3:::opal-data-etfs/gold/x",
             "arn:aws:s3:::opal-data-etfs/daily/x", "arn:aws:s3:::opal-data-etfs/platinum/x", "arn:aws:s3:::opal-data-assets/x"]
    own = [arn(c.address(*a)) for a in [("issuer-site", "etfs", "bronze", "holdings", "date=2026-09-29", "x"),
                                         ("issuer-site", "etfs", "silver", "holdings", "date=2026-09-29", "x"),
                                         ("rivalfunds", "etfs", "gold", "canonical_shape", "date=2026-09-29", "x"),
                                         ("rivalfunds", "etfs", "platinum", "page", "date=2026-09-29", "x")]]
    for p in pols:
        doc = p.read_text(encoding="utf-8")
        ev = lambda act, res: iam.simulate_custom_policy(PolicyInputList=[doc], ActionNames=[act], ResourceArns=res)["EvaluationResults"]  # noqa: E731
        leaks = [e["EvalResourceName"] for e in ev("s3:PutObject", never) if e["EvalDecision"] == "allowed"]
        v.check(not leaks, f"{p.name}: no PutObject outside the builder prefixes ({leaks})")
        dels = [e["EvalResourceName"] for e in ev("s3:DeleteObject", own + never) if e["EvalDecision"] == "allowed"]
        v.check(not dels, f"{p.name}: no DeleteObject anywhere ({dels})")
    fetch = next((p for p in pols if "fetch-holdings" in p.name), None)
    if fetch:
        got = iam.simulate_custom_policy(PolicyInputList=[fetch.read_text(encoding="utf-8")], ActionNames=["s3:PutObject"], ResourceArns=[own[0]])["EvaluationResults"][0]["EvalDecision"]
        v.check(got == "allowed", f"positive arm: the fetch role may PutObject into issuer bronze ({got})")
    tfv = json.loads((stack / "generated.auto.tfvars.json").read_text(encoding="utf-8")) if (stack / "generated.auto.tfvars.json").exists() else {}
    import re
    typed_re = re.compile(r'opal-data-etfs|(function_name|name|role|name_prefix)\s*=\s*"(etfs-rivalfunds|rivalfunds-)')
    typed = [f.name for f in stack.glob("*.tf") if typed_re.search(f.read_text(encoding="utf-8"))]
    v.check(bool(tfv) and not typed, f"the .tf files type no bucket or resource name; they read generated.auto.tfvars.json (typed in: {typed})")


failures = c.guarded("AC3", run)
if failures == 0:
    print("AC3 RESULT: PASS 0 failures")
else:
    print(f"AC3 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
