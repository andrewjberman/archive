"""BF-e-6: which generic_noun words are AWS service words, and what moving them to purpose_word would change.

Reads infra/logic/registry/systems.json refused_keys.generic_noun. A word is AWS-SERVICE when (a) it is the name or
IAM API prefix of an AWS service (the SERVICE_PREFIXES table below: the judgment half) AND (b) the repository's .tf or
policy JSON carries an IAM action with it as the service prefix (a double-quote, the word, a colon, an action name:
the mechanical half, first file and line printed). Else OTHER.

Then, on a temporary COPY of the registry folder with the AWS-SERVICE words moved generic_noun -> purpose_word, the
grader is pointed at the copy (opal_naming.REGISTRY_DIR, the key of both the registry cache and the vocabulary cache),
census_repo()'s items are re-graded, and the verdict changes are counted. The real registry files are hashed before
and after. Python 3.9, ASCII only, stdlib only.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
sys.path.insert(0, os.path.join(REPO, "lib"))
import opal_naming as on  # noqa: E402

REG = on.REGISTRY_DIR  # the real registry; never written

# Judgment half: the generic_noun words that ARE the name or the IAM API prefix of an AWS service. A word absent from
# this table is OTHER whatever the repo says (verbs, vendors, tiers, nouns). Prefix per the AWS Service Authorization
# Reference; the second field is the service name.
SERVICE_PREFIXES = {
    "cloudfront": "Amazon CloudFront",
    "codebuild": "AWS CodeBuild",
    "ec2": "Amazon EC2",
    "ecr": "Amazon ECR",
    "ecs": "Amazon ECS",
    "events": "Amazon EventBridge (IAM prefix events)",
    "rds": "Amazon RDS",
    "ses": "Amazon SES",
    "sms": "AWS Server Migration Service (IAM prefix sms)",
    "sns": "Amazon SNS",
    "sqs": "Amazon SQS",
    "ssm": "AWS Systems Manager",
    "dynamo": "Amazon DynamoDB (IAM prefix dynamodb)",
    "ddb": "Amazon DynamoDB (IAM prefix dynamodb)",
    "fargate": "AWS Fargate (part of ECS, no IAM prefix of its own)",
    "ai": "(not a service)",
}
SERVICE_PREFIXES = {k: v for k, v in SERVICE_PREFIXES.items() if not v.startswith("(")}


def hash_registry():
    out = {}
    for n in sorted(os.listdir(REG)):
        with open(os.path.join(REG, n), "rb") as fh:
            out[n] = hashlib.sha256(fh.read()).hexdigest()
    return out


def scan_files():
    p = subprocess.run(["git", "ls-files", "--", "*.tf", "*.json"], cwd=REPO, capture_output=True)
    if p.returncode != 0:
        raise SystemExit("SERVICE-WORDS ok=False git ls-files rc=%d" % p.returncode)
    files = sorted(f for f in p.stdout.decode("utf-8").split("\n") if f)

    # .tf files first (the policy text itself), then policy JSON outside docs/, then the rest: the evidence
    # printed for a word is the strongest first occurrence, never a brief's census dump when a .tf has the action.
    def rank(f):
        return (0 if f.endswith(".tf") else (2 if f.startswith("docs/") else 1), f)
    return sorted(files, key=rank)


def first_iam_occurrence(words, files):
    """word -> (file, line number, line text) of the first IAM-action-shaped use, else None."""
    pats = {w: re.compile(r"\"%s:[A-Za-z*][A-Za-z0-9*]*\"" % re.escape(w)) for w in words}
    found = {}
    for f in files:
        path = os.path.join(REPO, *f.split("/"))
        try:
            if os.path.getsize(path) > 8 * 1024 * 1024:
                continue
            with open(path, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        except OSError:
            continue
        if ":" not in text:
            continue
        for n, line in enumerate(text.split("\n"), 1):
            for w, rx in pats.items():
                if w not in found and rx.search(line):
                    found[w] = (f, n, line.strip()[:110])
        if len(found) == len(pats):
            break
    return found


def lead(name):
    return re.split(r"[-_]", name.lower())[0]


def main():
    before = hash_registry()
    real_sys = on._read_json(os.path.join(REG, "systems.json"))
    generic = list(real_sys["refused_keys"]["generic_noun"])
    files = scan_files()
    print("SCAN tf+json files=%d" % len(files))
    cand = [w for w in generic if w in SERVICE_PREFIXES]
    occ = first_iam_occurrence(cand, files)
    classes = {}
    for w in generic:
        if w in occ:
            classes[w] = "AWS-SERVICE"
        else:
            classes[w] = "OTHER"
        if w in occ:
            f, n, txt = occ[w]
            print("AWS-SERVICE %-10s %s | evidence %s:%d  %s" % (w, SERVICE_PREFIXES[w], f, n, txt))
        elif w in SERVICE_PREFIXES:
            print("OTHER       %-10s %s | named a service but NO IAM action in repo" % (w, SERVICE_PREFIXES[w]))
    aws = sorted(w for w, c in classes.items() if c == "AWS-SERVICE")
    print("OTHER words (not a service name, or no IAM evidence): %d" % (len(generic) - len(aws)))

    # baseline grades on the real registry
    items, stats = on.census_repo()
    seen = {}
    for it in items:
        seen.setdefault((it["type"], it["current"]), []).append(it["where"])
    old = {}
    for (t, n) in seen:
        try:
            old[(t, n)] = on.grade(n, t)[0]
        except on.RaiseDefect:
            old[(t, n)] = "RAISE"
    print("CENSUS items=%d unique_names=%d" % (len(items), len(seen)))

    tmp = tempfile.mkdtemp(prefix="bf_e6_reg_")
    cp = os.path.join(tmp, "registry")
    shutil.copytree(REG, cp)
    try:
        sp = os.path.join(cp, "systems.json")
        d = on._read_json(sp)
        rk = d["refused_keys"]
        rk["generic_noun"] = [w for w in rk["generic_noun"] if w not in aws]
        rk["purpose_word"] = list(rk["purpose_word"]) + [w for w in aws if w not in rk["purpose_word"]]
        with open(sp, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, indent=2)
            fh.write("\n")
        refusals, warns = on.validate(cp)
        for r in refusals:
            print("VALIDATE REFUSAL %s" % (r,))
        # point the grader at the copy: fresh registry and vocabulary, keyed by the copy's own path
        saved = on.REGISTRY_DIR
        on.REGISTRY_DIR = cp
        on._CACHE.clear()
        on._VOCAB_CACHE.clear()
        try:
            assert aws == [w for w in aws if w in on._vocab().purpose], "copy vocabulary lacks the moved words"
            new = {}
            for (t, n) in seen:
                try:
                    new[(t, n)] = on.grade(n, t)[0]
                except on.RaiseDefect:
                    new[(t, n)] = "RAISE"
        finally:
            on.REGISTRY_DIR = saved
            on._CACHE.clear()
            on._VOCAB_CACHE.clear()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    changed = sorted(k for k in seen if old[k] != new[k])
    trans = {}
    for k in changed:
        trans[(old[k], new[k])] = trans.get((old[k], new[k]), 0) + 1
    to_nsa = sum(c for (o, n), c in trans.items() if o == "OUT-OF-PATTERN" and n == "NO-SYSTEM-ASKED")
    other = len(changed) - to_nsa
    print("TRANSITIONS " + "; ".join("%s -> %s: %d" % (o, n, c) for (o, n), c in sorted(trans.items())))
    for k in changed:
        print("MOVES %s %s | %s -> %s | %s" % (k[0], k[1], old[k], new[k], seen[k][0]))
    for k in sorted(seen):
        if lead(k[1]) in aws and k not in changed:
            print("STAYS %s %s | %s | %s" % (k[0], k[1], old[k], seen[k][0]))

    after = hash_registry()
    untouched = before == after
    print("REGISTRY real files=%d byte-identical-before-after=%s" % (len(before), untouched))
    ok = (other == 0 and len(refusals) == 0 and untouched and len(changed) > 0)
    print("SERVICE-WORDS ok=%s generic_noun=%d aws_service=%d moved_names=%d to_no_system_asked=%d other_changes=%d "
          "validate_refusals=%d" % (ok, len(generic), len(aws), len(changed), to_nsa, other, len(refusals)))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
