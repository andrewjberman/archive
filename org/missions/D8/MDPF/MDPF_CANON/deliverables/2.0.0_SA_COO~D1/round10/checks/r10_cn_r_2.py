#!/usr/bin/env python3
"""MDPF_CANON round 10, cell CN-r-2 -- the publisher role may READ the served MDPF prefix (the latest.json pointer and the served keys).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r10_cn_r_2.py statement   the ONE added policy: one statement, one action, one resource, builder-named, not gated, ASCII (5 arms)
  python r10_cn_r_2.py rest        nothing else moved: the rest of mdpf_egress_publisher.tf equals the base, the block inventory is the
                                   base plus the two added, the 22 neighbouring Terraform files are byte-equal, terraform fmt parses it (4 arms)
  python r10_cn_r_2.py eval        the role's policy documents EVALUATED: GetObject on latest.json and the served keys allowed; the
                                   negative controls (json/mdpf, etfs, staging, another bucket, DeleteObject) still denied; the write set unchanged (5 arms)
  python r10_cn_r_2.py selftest    base red/green as expected, the reference tree green, one planted mutant per arm; issuer only

Target: `<git toplevel>/infra/aws/terraform/opal-assets/`, or `--root <dir>` (selftest and dry-runs; a dir shaped like the repo root).
The statements are PARSED from the real Terraform source (a small reader of the restricted `jsonencode({...})` shape the file uses) and
the policy documents are evaluated with S3 object-level matching: nothing is granted by text presence alone.
Output: `CN-R-2 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import fnmatch
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

TF_REL = "infra/aws/terraform/opal-assets/mdpf_egress_publisher.tf"
TF_DIR_REL = "infra/aws/terraform/opal-assets"
ROLE_REF = "aws_iam_role.mdpf_egress_publisher"
NEW_RES = "mdpf_egress_publisher_live_serve_read"
NEW_MOD = "mdpf_publisher_live_serve_read_policy_name"
PLAT = "opal-data-portal-v2"
LIVE_PREFIX = "platinum/mdpf/*"
WANT_RES = "arn:aws:s3:::%s/%s" % (PLAT, LIVE_PREFIX)
# LF-normalised (blank and `#` lines dropped, trailing blanks stripped) sha256 of the base file, measured at box/dell1 @21caa664be.
BASE_NORM_SHA = "dd0ed236596c377d21f24690a9a11bf6bb9a248d00afb726149ca2006adaa238"
BASE_NONASCII = 3   # the file's pre-existing non-ASCII characters (comments); an edit must keep them and add none
BASE_OTHERS_SHA = "1fc14ba918c1265490c51f15a2031ede93deb3e0da65efeb6c152510f8de231c"   # 22 neighbouring files at box/dell1 @21caa664be
BASE_INVENTORY = {
    ("variable", "mdpf_egress_live_serve_write_cosigned"), ("resource", "aws_iam_role.mdpf_egress_publisher"),
    ("resource", "aws_iam_role_policy_attachment.mdpf_egress_publisher_basic"),
    ("resource", "aws_iam_role_policy.mdpf_egress_publisher_scoped"),
    ("resource", "aws_iam_role_policy.mdpf_egress_publisher_live_serve"),
    ("resource", "aws_iam_role_policy.mdpf_egress_publisher_taxsma_control"),
    ("module", "mdpf_publisher_taxsma_control_policy_name"),
    ("output", "mdpf_egress_publisher_role_arn"), ("output", "mdpf_egress_publisher_live_serve_cosigned"),
    ("locals", "#1"), ("locals", "#2"),
}
ADDED_INVENTORY = {("resource", "aws_iam_role_policy." + NEW_RES), ("module", NEW_MOD)}
GOLD_READ = "arn:aws:s3:::opal-data-assets/portal/gold/mdpf/global/aggregate-aua-timeseries/2026-10-14.json"
TAX_CONTROL = "arn:aws:s3:::opal-data-mdpf/mdpf/global/state/taxsma_control/current.json"
LATEST = "arn:aws:s3:::%s/platinum/mdpf/_manifests/latest.json" % PLAT
SERVED = ["arn:aws:s3:::%s/platinum/mdpf/%s/%s.json" % (PLAT, s, t)
          for s in ("global", "49financial", "inflection", "cottonwood") for t in ("category-views", "aggregate-aua-timeseries")]
MUST_DENY = [
    "arn:aws:s3:::%s/json/mdpf/global/aggregate_aua_timeseries.json" % PLAT,      # the UNSIGNED prefix of the NEVER#3 record
    "arn:aws:s3:::%s/platinum/etfs/global/anything.json" % PLAT,                  # another served product
    "arn:aws:s3:::%s/platinum/_staging/mdpf/global/anything.json" % PLAT,         # staging: written, never read by this grant
    "arn:aws:s3:::opal-data-mdpf/mdpf/global/gold/aum_metrics/anything.parquet",  # another bucket
    "arn:aws:s3:::opal-data-bd/anything",
]


# ------------------------------------------------------------------ a tiny reader for the file's restricted HCL
class Reader:
    def __init__(self, text):
        self.s, self.i = text, 0

    def skip(self):
        s = self.s
        while self.i < len(s):
            c = s[self.i]
            if c in " \t\r\n,":
                self.i += 1
            elif c == "#" or s.startswith("//", self.i):
                while self.i < len(s) and s[self.i] != "\n":
                    self.i += 1
            elif s.startswith("/*", self.i):
                j = s.find("*/", self.i + 2)
                self.i = len(s) if j < 0 else j + 2
            else:
                break

    def string(self):
        s = self.s
        assert s[self.i] == '"'
        self.i += 1
        out = []
        while self.i < len(s):
            c = s[self.i]
            if c == "\\":
                out.append(s[self.i:self.i + 2])
                self.i += 2
            elif s.startswith("${", self.i):
                depth, j = 1, self.i + 2
                while j < len(s) and depth:
                    depth += (s[j] == "{") - (s[j] == "}")
                    j += 1
                out.append(s[self.i:j])
                self.i = j
            elif c == '"':
                self.i += 1
                return "".join(out)
            else:
                out.append(c)
                self.i += 1
        raise ValueError("unterminated string")

    def value(self):
        self.skip()
        c = self.s[self.i]
        if c == '"':
            return self.string()
        if c == "[":
            self.i += 1
            items = []
            while True:
                self.skip()
                if self.s[self.i] == "]":
                    self.i += 1
                    return items
                items.append(self.value())
        if c == "{":
            self.i += 1
            obj = {}
            while True:
                self.skip()
                if self.s[self.i] == "}":
                    self.i += 1
                    return obj
                m = re.compile(r'[A-Za-z_][A-Za-z0-9_\-]*|"[^"]*"').match(self.s, self.i)
                key = m.group(0).strip('"')
                self.i = m.end()
                self.skip()
                assert self.s[self.i] in "=:", self.s[self.i - 20:self.i + 20]
                self.i += 1
                obj[key] = self.value()
        m = re.compile(r"[A-Za-z0-9_.\-]+").match(self.s, self.i)
        if not m:
            raise ValueError("bad token near %r" % self.s[self.i:self.i + 30])
        self.i = m.end()
        return ("ref", m.group(0))


def block_span(text, open_idx):
    """Index just past the brace block opening at text[open_idx] == '{', string and comment aware."""
    depth, i, n = 0, open_idx, len(text)
    while i < n:
        c = text[i]
        if c == '"':
            r = Reader(text)
            r.i = i
            r.string()
            i = r.i
            continue
        if c == "#" or text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced block")


HEAD_RE = re.compile(r'^(resource|module|variable|output)\s+"([^"]+)"(?:\s+"([^"]+)")?\s*\{', re.M)
LOCALS_RE = re.compile(r"^locals\s*\{", re.M)


def blocks(text):
    """[(kind, name, start, end, body)] for every top-level block of interest, plus the locals blocks."""
    out, nloc = [], 0
    for m in HEAD_RE.finditer(text):
        end = block_span(text, m.end() - 1)
        kind, a, b = m.group(1), m.group(2), m.group(3)
        name = ("%s.%s" % (a, b)) if kind == "resource" else a
        out.append((kind, name, m.start(), end, text[m.end():end - 1]))
    for m in LOCALS_RE.finditer(text):
        end = block_span(text, m.end() - 1)
        nloc += 1
        out.append(("locals", "#%d" % nloc, m.start(), end, text[m.end():end - 1]))
    return sorted(out, key=lambda b: b[2])


def read_locals(tf_dir):
    loc = {}
    for fn in sorted(os.listdir(tf_dir)):
        if not fn.endswith(".tf"):
            continue
        t = open(os.path.join(tf_dir, fn), encoding="utf-8").read()
        for kind, _n, _s, _e, body in blocks(t):
            if kind == "locals":
                for m in re.finditer(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"([^"\n]*)"\s*$', body, re.M):
                    loc.setdefault(m.group(1), m.group(2))
    return loc


def subst(s, loc):
    if isinstance(s, tuple) and s[0] == "ref" and s[1].startswith("local."):
        s = loc.get(s[1][len("local."):], s)
    return re.sub(r"\$\{local\.([A-Za-z0-9_]+)\}", lambda m: loc.get(m.group(1), m.group(0)), s) if isinstance(s, str) else s


def policy_docs(text, loc):
    """{resource name: {'role': ref, 'name': value, 'doc': evaluated policy dict, 'attrs': set of top-level attribute names}}"""
    out = {}
    for kind, name, _s, _e, body in blocks(text):
        if kind != "resource" or not name.startswith("aws_iam_role_policy."):
            continue
        attrs = {}
        top = set()
        depth = 0
        for ln in body.split("\n"):
            if depth == 0:
                m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", ln)
                if m:
                    top.add(m.group(1))
            depth += ln.count("{") + ln.count("[") + ln.count("(") - ln.count("}") - ln.count("]") - ln.count(")")
        m = re.search(r"policy\s*=\s*jsonencode\(", body)
        if not m:
            continue
        r = Reader(body)
        r.i = m.end()
        doc = r.value()
        for k in ("name", "role"):
            mm = re.search(r"^\s*%s\s*=\s*(\"[^\n]*\"|[A-Za-z0-9_.\-]+)\s*$" % k, body, re.M)
            attrs[k] = mm.group(1).strip('"') if mm else None
        stm = doc.get("Statement", []) if isinstance(doc, dict) else []
        stm = stm if isinstance(stm, list) else [stm]
        for st in stm:
            for k in ("Resource", "Action"):
                if k in st:
                    st[k] = [subst(x, loc) for x in st[k]] if isinstance(st[k], list) else subst(st[k], loc)
        out[name.split(".", 1)[1]] = {"role": attrs["role"], "name": attrs["name"], "doc": doc, "attrs": top, "statements": stm}
    return out


def as_list(x):
    return x if isinstance(x, list) else [x]


def allowed(docs, action, arn):
    """S3 object-level evaluation over every policy attached to the publisher role: Allow statements only (no Deny exists)."""
    for name, p in docs.items():
        if p["role"] != ROLE_REF + ".id":
            continue
        for st in p["statements"]:
            if st.get("Effect") != "Allow" or "Condition" in st or "NotAction" in st or "NotResource" in st:
                continue
            if any(fnmatch.fnmatchcase(action, a) for a in as_list(st.get("Action", []))) and \
               any(fnmatch.fnmatchcase(arn, r) for r in as_list(st.get("Resource", []))):
                return True
    return False


OTHER_DIRS = ("infra/aws/terraform/opal-assets", "infra/aws/terraform/modules/opal_name")


def others_digest(root):
    h, n, h_items = hashlib.sha256(), 0, []
    for d in OTHER_DIRS:
        for dp, dn, fn in os.walk(os.path.join(root, d)):
            dn[:] = [x for x in dn if x != ".terraform"]
            for f in fn:
                full = os.path.join(dp, f)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                if rel == TF_REL or f == "CHANGELOG.json" or ".tfstate" in f:
                    continue
                body = open(full, "rb").read().replace(b"\r\n", b"\n")
                h_items.append((rel, hashlib.sha256(body).hexdigest()))
    for rel, s in sorted(h_items):
        h.update(rel.encode() + b"\0" + s.encode() + b"\n")
        n += 1
    return h.hexdigest(), n


def norm(text):
    out = []
    for ln in text.replace("\r\n", "\n").split("\n"):
        x = ln.rstrip()
        if x.strip() and not x.strip().startswith("#"):
            out.append(x)
    return "\n".join(out) + "\n"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class Arms:
    def __init__(self, name):
        self.name, self.ok, self.n = name, 0, 0

    def arm(self, aid, passed, detail):
        self.n += 1
        self.ok += 1 if passed else 0
        print("  %-3s %s %s" % (aid, "PASS" if passed else "FAIL", detail))

    def done(self):
        print("CN-R-2 %s: %d of %d arms" % (self.name.upper(), self.ok, self.n))
        return 0 if self.ok == self.n else 1


def load(root):
    tf = os.path.join(root, TF_REL)
    text = open(tf, "rb").read().decode("utf-8").replace("\r\n", "\n")
    loc = read_locals(os.path.join(root, TF_DIR_REL))
    return tf, text, loc, policy_docs(text, loc)


# ------------------------------------------------------------------ the modes
def statement(root):
    a = Arms("statement")
    _tf, text, loc, docs = load(root)
    p = docs.get(NEW_RES)
    sts = (p or {}).get("statements") or []
    a.arm("S1", p is not None and p["role"] == ROLE_REF + ".id" and len(sts) == 1,
          "the policy resource aws_iam_role_policy.%s exists, is attached to %s, and holds exactly ONE statement (found %s, role %s, %d statement(s))"
          % (NEW_RES, ROLE_REF, p is not None, (p or {}).get("role"), len(sts)))
    st = sts[0] if len(sts) == 1 else {}
    ok2 = (st.get("Effect") == "Allow" and as_list(st.get("Action", [])) == ["s3:GetObject"]
           and as_list(st.get("Resource", [])) == [WANT_RES]
           and not ({"Condition", "NotAction", "NotResource", "Principal"} & set(st)))
    a.arm("S2", ok2, "the statement is Allow, s3:GetObject ONLY, on exactly %s, with no Condition, NotAction, NotResource or Principal (got Effect %s, Action %s, Resource %s)"
          % (WANT_RES, st.get("Effect"), st.get("Action"), st.get("Resource")))
    mods = {n: b for k, n, _s, _e, b in blocks(text) if k == "module"}
    mb = mods.get(NEW_MOD, "")
    mod_ok = (NEW_MOD in mods and re.search(r'source\s*=\s*"\.\./modules/opal_name"', mb) and re.search(r'system\s*=\s*"mdpf"', mb)
              and re.search(r'function\s*=\s*"publisher-live-serve-read"', mb) and re.search(r'kind\s*=\s*"policy"', mb))
    name_ok = bool(p) and p["name"] == "module.%s.name" % NEW_MOD
    a.arm("S3", bool(mod_ok) and name_ok, "the policy name comes from the opal_name builder module %s (system mdpf, function publisher-live-serve-read, kind policy) "
          "and is never a typed literal (name = %s)" % (NEW_MOD, (p or {}).get("name")))
    gated = bool(p) and ({"count", "for_each", "depends_on", "provider", "lifecycle"} & p["attrs"])
    a.arm("S4", bool(p) and not gated and p["attrs"] == {"name", "role", "policy"},
          "the resource carries only name, role and policy: not gated by count or for_each, so the plan adds it unconditionally (attributes %s)" % sorted((p or {}).get("attrs", [])))
    added = "".join(text[s:e] for k, n, s, e, _b in blocks(text) if (k, n) in ADDED_INVENTORY)
    nonascii_all = sum(1 for c in text if ord(c) > 127)
    a.arm("S5", bool(added) and all(ord(c) < 128 for c in added) and nonascii_all == BASE_NONASCII,
          "the added blocks are ASCII only and the file still carries exactly its %d pre-existing non-ASCII characters (found %d in the file, %d bytes added)"
          % (BASE_NONASCII, nonascii_all, len(added)))
    return a.done()


def rest(root):
    a = Arms("rest")
    tf = os.path.join(root, TF_REL)
    try:
        text = open(tf, "rb").read().decode("utf-8").replace(chr(13) + chr(10), chr(10))
        bl = blocks(text)
    except Exception as exc:  # an unparseable file is a red arm, never a crash
        text, bl = None, None
        print("      (the file could not be read as blocks: %s: %s)" % (type(exc).__name__, exc))
    if bl is None:
        a.arm("R1", False, "the file does not read as balanced blocks")
        a.arm("R2", False, "the block inventory cannot be read")
    else:
        keep = text
        for kind, name, s, e, _b in sorted(bl, key=lambda b: -b[2]):
            if (kind, name) in ADDED_INVENTORY:
                keep = keep[:s] + keep[e:]
        a.arm("R1", sha(norm(keep)) == BASE_NORM_SHA,
              "the file minus its two added blocks (comments and blank lines ignored) equals the base: sha256 %s (want %s...); a changed or removed existing line fails"
              % (sha(norm(keep))[:12], BASE_NORM_SHA[:12]))
        inv = {(k, n) for k, n, _s, _e, _b in bl}
        extra = inv - BASE_INVENTORY - ADDED_INVENTORY
        miss = BASE_INVENTORY - inv
        a.arm("R2", not extra and not miss, "the block inventory is the base plus at most the two added (unexpected %s, missing %s)" % (sorted(extra), sorted(miss)))
    d_now, n_now = others_digest(root)
    a.arm("R3", d_now == BASE_OTHERS_SHA,
          "the %d neighbouring files (every other file of infra/aws/terraform/opal-assets and of modules/opal_name, the generated CHANGELOG.json aside) are byte-equal to the base: digest %s (want %s...)"
          % (n_now, d_now[:12], BASE_OTHERS_SHA[:12]))
    tfx = None
    for cand in (os.path.join(root, ".tools", "terraform.exe"), os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "..", "..", ".tools", "terraform.exe")):
        if os.path.exists(cand):
            tfx = cand
            break
    tfx = tfx or shutil.which("terraform")
    if tfx is None:
        a.arm("F", False, "no terraform binary found for the format and parse check")
    else:
        r = subprocess.run([tfx, "fmt", "-check", "-diff", tf], capture_output=True, text=True, timeout=60)
        a.arm("F", r.returncode == 0, "terraform fmt -check on the file: rc %d (the real HCL parser reads it; a formatting or syntax defect fails)%s"
              % (r.returncode, "" if r.returncode == 0 else " " + (r.stdout or r.stderr)[:160].replace("\n", " ")))
    return a.done()


def evaluate(root):
    a = Arms("eval")
    _tf, text, loc, docs = load(root)
    a.arm("E1", allowed(docs, "s3:GetObject", LATEST), "the role may s3:GetObject the pointer %s (the publisher's prior-rows read)" % LATEST)
    served_ok = [s for s in SERVED if allowed(docs, "s3:GetObject", s)]
    a.arm("E2", len(served_ok) == len(SERVED),
          "the role may s3:GetObject every served key it re-hashes in the unchanged branch (%d of %d probed: category-views and aggregate-aua-timeseries of four scopes)"
          % (len(served_ok), len(SERVED)))
    denied = [r for r in MUST_DENY if not allowed(docs, "s3:GetObject", r)]
    a.arm("E3", len(denied) == len(MUST_DENY), "NEGATIVE CONTROL: GetObject stays DENIED where it must be (%d of %d: json/mdpf, platinum/etfs, platinum/_staging/mdpf, opal-data-mdpf, opal-data-bd)"
          % (len(denied), len(MUST_DENY)))
    ctl = [allowed(docs, "s3:GetObject", GOLD_READ), allowed(docs, "s3:GetObject", TAX_CONTROL)]
    a.arm("E4", all(ctl), "CONTROL: the existing reads still hold (the gold read %s, the Tax control read %s)" % (ctl[0], ctl[1]))
    put_ok = [allowed(docs, "s3:PutObject", x) for x in ("arn:aws:s3:::%s/platinum/mdpf/global/x.json" % PLAT, "arn:aws:s3:::%s/platinum/_staging/mdpf/x.json" % PLAT)]
    put_no = [allowed(docs, "s3:PutObject", x) for x in ("arn:aws:s3:::%s/json/mdpf/x.json" % PLAT, "arn:aws:s3:::opal-data-assets/portal/gold/mdpf/x.json")]
    gone = [allowed(docs, "s3:DeleteObject", x) for x in ("arn:aws:s3:::%s/platinum/mdpf/global/x.json" % PLAT, GOLD_READ)]
    a.arm("E5", all(put_ok) and not any(put_no) and not any(gone),
          "CONTROL: the write set is unchanged (PutObject on platinum/mdpf and staging allowed %s; PutObject on json/mdpf and the gold tree denied %s; DeleteObject denied %s)"
          % (all(put_ok), not any(put_no), not any(gone)))
    return a.done()


# ------------------------------------------------------------------ selftest: base, reference, one mutant per arm
REFERENCE_BLOCK = '''
module "mdpf_publisher_live_serve_read_policy_name" {
  source   = "../modules/opal_name"
  system   = "mdpf"
  function = "publisher-live-serve-read"
  kind     = "policy"
}

resource "aws_iam_role_policy" "mdpf_egress_publisher_live_serve_read" {
  name = module.mdpf_publisher_live_serve_read_policy_name.name
  role = aws_iam_role.mdpf_egress_publisher.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "ReadLiveServedMdpf"
      Effect   = "Allow"
      Action   = ["s3:GetObject"]
      Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"
    }]
  })
}
'''

MUTANTS = {
    # name: (transform on the reference file text, the arms that must turn red)
    "action-star": (lambda t: t.replace('Action   = ["s3:GetObject"]\n      Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]\n  })\n}\n',
                    'Action   = ["s3:*"]\n      Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]\n  })\n}\n'), {"S2", "E5"}),
    "plus-put": (lambda t: t.replace('Action   = ["s3:GetObject"]\n      Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]',
                                     'Action   = ["s3:GetObject", "s3:PutObject"]\n      Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]'), {"S2"}),
    "bucket-wide": (lambda t: t.replace('Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]\n  })\n}\n',
                                        'Resource = "arn:aws:s3:::${local.platinum_bucket}/*"\n    }]\n  })\n}\n'), {"S2", "E3"}),
    "json-prefix": (lambda t: t.replace('Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]\n  })\n}\n',
                                        'Resource = "arn:aws:s3:::${local.platinum_bucket}/json/mdpf/*"\n    }]\n  })\n}\n'), {"S2", "E1", "E2", "E3"}),
    "latest-only": (lambda t: t.replace('Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"\n    }]\n  })\n}\n',
                                        'Resource = "arn:aws:s3:::${local.platinum_bucket}/platinum/mdpf/_manifests/latest.json"\n    }]\n  })\n}\n'), {"S2", "E2"}),
    "deny-effect": (lambda t: t.replace('Effect   = "Allow"\n      Action   = ["s3:GetObject"]', 'Effect   = "Deny"\n      Action   = ["s3:GetObject"]'), {"S2", "E1", "E2"}),
    "count-off": (lambda t: t.replace('resource "aws_iam_role_policy" "mdpf_egress_publisher_live_serve_read" {\n',
                                      'resource "aws_iam_role_policy" "mdpf_egress_publisher_live_serve_read" {\n  count = var.mdpf_egress_live_serve_write_cosigned ? 1 : 0\n\n'), {"S4"}),
    "typed-name": (lambda t: t.replace("name = module.mdpf_publisher_live_serve_read_policy_name.name", 'name = "mdpf-publisher-live-serve-read-policy"'), {"S3"}),
    "wrong-role": (lambda t: t.replace('role = aws_iam_role.mdpf_egress_publisher.id\n\n  policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n      Sid      = "ReadLiveServedMdpf"',
                                       'role = aws_iam_role.mdpf_egress_publisher_other.id\n\n  policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n      Sid      = "ReadLiveServedMdpf"'), {"S1", "E1", "E2"}),
    "edit-existing": (lambda t: t.replace('Action   = ["s3:PutObject"]\n        Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"',
                                          'Action   = ["s3:PutObject", "s3:DeleteObject"]\n        Resource = "arn:aws:s3:::${local.platinum_bucket}/${local.mdpf_egress_live_write_prefix}"'), {"R1", "E5"}),
    "extra-resource": (lambda t: t + '\nresource "aws_iam_role_policy" "mdpf_egress_publisher_extra" {\n  name = "x"\n  role = aws_iam_role.mdpf_egress_publisher.id\n  policy = jsonencode({\n    Version = "2012-10-17"\n    Statement = [{\n      Effect   = "Allow"\n      Action   = ["s3:ListAllMyBuckets"]\n      Resource = "*"\n    }]\n  })\n}\n', {"R2"}),
    "bad-hcl": (lambda t: t + '\nresource "aws_iam_role_policy" "oops" {\n', {"F"}),
    "nonascii-add": (lambda t: t.replace('Sid      = "ReadLiveServedMdpf"', 'Sid      = "ReadLiveServedMdpf\u00e9"'), {"S5"}),
}


def selftest():
    root_real = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    base_tf = subprocess.check_output(["git", "-C", root_real, "show", "HEAD:" + TF_REL])
    assert sha(norm(base_tf.decode("utf-8").replace("\r\n", "\n"))) == BASE_NORM_SHA, "selftest needs the BASE file at HEAD (run it on a tree whose HEAD carries the base)"
    ok_all = True
    tmp = tempfile.mkdtemp(prefix="r10cnr2_")

    def build(name, text):
        d = os.path.join(tmp, name)
        for rel in (TF_DIR_REL, "infra/aws/terraform/modules/opal_name"):
            shutil.copytree(os.path.join(root_real, rel), os.path.join(d, rel), ignore=shutil.ignore_patterns(".terraform", "*.tfstate*"))
        os.makedirs(os.path.join(d, ".tools"), exist_ok=True)
        for tfx in (os.path.join(root_real, ".tools", "terraform.exe"),):
            if os.path.exists(tfx):
                shutil.copy(tfx, os.path.join(d, ".tools", "terraform.exe"))
        with open(os.path.join(d, TF_REL), "wb") as fh:
            fh.write(base_tf)
        subprocess.run(["git", "init", "-q", d], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.email=a@b", "-c", "user.name=x", "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.email=a@b", "-c", "user.name=x", "commit", "-q", "-m", "base"], check=True)
        with open(os.path.join(d, TF_REL), "wb") as fh:
            fh.write(text.encode("utf-8"))
        return d

    def run(mode, d):
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = {"statement": statement, "rest": rest, "eval": evaluate}[mode](d)
        return rc, buf.getvalue()

    def red_arms(out):
        return {ln.split()[0] for ln in out.splitlines() if ln.startswith("  ") and " FAIL " in ln}

    base_text = base_tf.decode("utf-8")
    ref_text = base_text.rstrip("\n") + "\n" + REFERENCE_BLOCK
    expect_base = {"statement": {"S1", "S2", "S3", "S4", "S5"}, "rest": set(), "eval": {"E1", "E2"}}
    print("-- base (must be red where it is a build arm, green where it is a control)")
    dbase = build("base", base_text)
    for mode, want in expect_base.items():
        _rc, out = run(mode, dbase)
        got = red_arms(out)
        print("   base %-9s red %s (expected %s) -> %s" % (mode, sorted(got), sorted(want), "OK" if got == want else "WRONG"))
        ok_all &= (got == want)
    print("-- reference tree (must read green on every arm)")
    dref = build("ref", ref_text)
    for mode in ("statement", "rest", "eval"):
        rc, out = run(mode, dref)
        print("   reference %-9s rc=%d%s" % (mode, rc, "" if rc == 0 else " RED " + str(sorted(red_arms(out)))))
        ok_all &= (rc == 0)
    print("-- planted mutants (each must turn the named arms red)")
    for mname, (fn, want) in MUTANTS.items():
        text = fn(ref_text)
        if text == ref_text and mname != "extra-resource":
            print("   mutant %-14s TRANSFORM DID NOT CHANGE THE TEXT -> WRONG" % mname)
            ok_all = False
            continue
        d = build("m_" + mname, text)
        got = set()
        for mode in ("statement", "rest", "eval"):
            try:
                _rc, out = run(mode, d)
                got |= red_arms(out)
            except Exception as exc:  # a mutant that breaks the reader is a caught mutant only if the arm set names it
                got |= {"PARSE:" + type(exc).__name__}
        hit = want <= got
        print("   mutant %-14s red %s (needs %s) -> %s" % (mname, sorted(got), sorted(want), "caught" if hit else "MISSED"))
        ok_all &= hit
    shutil.rmtree(tmp, ignore_errors=True)
    print("CN-R-2 SELFTEST: %s" % ("OK" if ok_all else "FAILED"))
    return 0 if ok_all else 1


def main(argv):
    if len(argv) < 2 or argv[1] not in ("statement", "rest", "eval", "selftest"):
        print(__doc__)
        return 2
    if argv[1] == "selftest":
        return selftest()
    root = argv[argv.index("--root") + 1] if "--root" in argv else subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    try:
        return {"statement": statement, "rest": rest, "eval": evaluate}[argv[1]](root)
    except Exception as exc:  # an unreadable file is a red result, never a traceback
        print("CN-R-2 %s: 0 arms (the file could not be read: %s: %s)" % (argv[1].upper(), type(exc).__name__, exc))
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
