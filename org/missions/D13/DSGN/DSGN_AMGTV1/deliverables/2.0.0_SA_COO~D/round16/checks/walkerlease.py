#!/usr/bin/env python3
"""THE WALKER ACCOUNT IS LEASED: k of 3 arms  (DSGN_AMGTV1 round 16 cell 1; row DSGN_AMGTV1-Z-S10).

Run from the repo root of the checkout under test:
    cd "$(git rev-parse --show-toplevel)" && python org/missions/D13/DSGN/DSGN_AMGTV1/deliverables/2.0.0_SA_COO~D/round16/checks/walkerlease.py

It loads .claude/skills/ui-walk/ui_walker_account.py from that checkout against an IN-MEMORY fake of DynamoDB and
SSM (a fake `boto3` module is installed in sys.modules BEFORE the module loads, and urllib.request.urlopen is replaced
by a 401 answer), so no call can reach live AWS or the network. The fake EVALUATES ConditionExpression and applies
UpdateExpression, and refuses an expression attribute name/value that is unused or undefined (as DynamoDB does).

CONTRACT under test (the ruled fix, CTO~Z msg 27598):
  arm()            -> one conditional UpdateItem (armedBy + armedAt + ConditionExpression) BEFORE any SSM write;
                      a held lease raises/prints "HELD by <armedBy> since <armedAt>" and mints nothing;
                      the holder id comes back to the caller (in arm's return value or stdout).
  disarm(holder)   -> conditional on armedBy == holder; removes armedBy/armedAt with the disable; deletes SSM;
                      a non-holder refuses and changes nothing.
  walk.mjs         -> the disarm invocation carries the holder id the arm returned (static read).

Arms:
  1 GREEN    -- sub-clauses (a)-(f) all PASS on the checkout.
  2 NEGATIVE -- every sub-clause FAILS on the pre-fix bytes (git show <BASE_PIN>:<file>, resolved by content).
  3 CONTROL  -- planted mutants: disarm with its conditions stripped is rejected by (e); SSM-before-DynamoDB is
               rejected by (a); and the unmutated checkout passes (a) and (e) (else the control is vacuous).
Exit 0 only at 3 of 3. Override the base pin with WALKERLEASE_BASE=<commit>.
"""
from __future__ import annotations

import contextlib
import copy
import datetime as dt
import importlib.util
import inspect
import io
import os
import re
import socket
import subprocess
import sys
import tempfile
import types
import urllib.error
import urllib.request

from botocore.exceptions import ClientError

TITLE = "THE WALKER ACCOUNT IS LEASED"
BASE_PIN = os.environ.get("WALKERLEASE_BASE", "8e874400712bcf60df5d4bce24b2c5b8e4faf3f3")
MOD_REL = ".claude/skills/ui-walk/ui_walker_account.py"
WALK_REL = ".claude/skills/ui-walk/walk.mjs"
OTHER = "other-host:4242:cafe0001"
INTRUDER = "intruder-host:77:beef0002"
FMT = "%Y-%m-%dT%H:%M:%S.%fZ"


def _iso(minutes_ago):
    return (dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=minutes_ago)).strftime(FMT)


# ---- the fake AWS plane --------------------------------------------------------------------------------------------
def _cerr(code, op, extra=None):
    resp = {"Error": {"Code": code, "Message": code}}
    resp.update(extra or {})
    return ClientError(resp, op)


class _Expr:
    """A minimal DynamoDB ConditionExpression evaluator: OR/AND/NOT, parens, attribute_exists/_not_exists,
    begins_with, = <> < <= > >=, BETWEEN. Values compare as S strings or N numbers."""
    TOK = re.compile(r"\s*(<>|<=|>=|=|<|>|\(|\)|,|#[A-Za-z0-9_]+|:[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_.]*)")

    def __init__(self, text, names, values, row):
        self.toks, pos = [], 0
        text = text.strip()
        while pos < len(text):
            m = self.TOK.match(text, pos)
            if not m:
                raise ValueError("fake: cannot tokenise condition at %r" % text[pos:])
            self.toks.append(m.group(1))
            pos = m.end()
        self.i, self.names, self.values, self.row = 0, names, values, row

    def peek(self):
        return self.toks[self.i] if self.i < len(self.toks) else None

    def take(self, want=None):
        t = self.peek()
        if want is not None and (t or "").upper() != want:
            raise ValueError("fake: expected %s got %s" % (want, t))
        self.i += 1
        return t

    def run(self):
        v = self.p_or()
        if self.peek() is not None:
            raise ValueError("fake: trailing tokens %r" % self.toks[self.i:])
        return v

    def p_or(self):
        v = self.p_and()
        while (self.peek() or "").upper() == "OR":
            self.take()
            r = self.p_and()
            v = v or r
        return v

    def p_and(self):
        v = self.p_not()
        while (self.peek() or "").upper() == "AND":
            self.take()
            r = self.p_not()
            v = v and r
        return v

    def p_not(self):
        if (self.peek() or "").upper() == "NOT":
            self.take()
            return not self.p_not()
        return self.p_prim()

    def path(self, tok):
        if tok.startswith("#"):
            if tok not in self.names:
                raise ValueError("fake: undefined name %s" % tok)
            return self.names[tok]
        return tok

    def operand(self):
        t = self.take()
        if t.startswith(":"):
            if t not in self.values:
                raise ValueError("fake: undefined value %s" % t)
            return _scalar(self.values[t])
        v = self.row.get(self.path(t))
        return None if v is None else _scalar(v)

    def p_prim(self):
        t = self.peek()
        if t == "(":
            self.take()
            v = self.p_or()
            self.take(")")
            return v
        low = (t or "").lower()
        if low in ("attribute_exists", "attribute_not_exists", "begins_with"):
            self.take()
            self.take("(")
            p = self.path(self.take())
            if low == "begins_with":
                self.take(",")
                pre = self.operand()
                self.take(")")
                cur = self.row.get(p)
                return cur is not None and isinstance(_scalar(cur), str) and _scalar(cur).startswith(pre)
            self.take(")")
            return (p in self.row) == (low == "attribute_exists")
        left = self.operand()
        op = self.take()
        if op.upper() == "BETWEEN":
            lo = self.operand()
            self.take("AND")
            hi = self.operand()
            return left is not None and lo is not None and hi is not None and lo <= left <= hi
        right = self.operand()
        if left is None or right is None or type(left) is not type(right):
            return False if op != "<>" else (left != right)
        return {"=": left == right, "<>": left != right, "<": left < right, "<=": left <= right,
                ">": left > right, ">=": left >= right}[op]


def _scalar(av):
    if "S" in av:
        return av["S"]
    if "N" in av:
        return float(av["N"])
    if "BOOL" in av:
        return av["BOOL"]
    return repr(av)


def _referenced(*exprs):
    out = set()
    for e in exprs:
        out |= set(re.findall(r"[#:][A-Za-z0-9_]+", e or ""))
    return out


def _apply_update(row, expr, names, values):
    parts = re.split(r"\b(SET|REMOVE)\b", expr.strip(), flags=re.I)
    if parts[0].strip():
        raise ValueError("fake: unsupported update expression %r" % expr)
    for kw, body in zip(parts[1::2], parts[2::2]):
        for clause in [c.strip() for c in body.split(",") if c.strip()]:
            if kw.upper() == "SET":
                lhs, rhs = [s.strip() for s in clause.split("=", 1)]
                key = names[lhs] if lhs.startswith("#") else lhs
                if rhs.startswith(":"):
                    row[key] = copy.deepcopy(values[rhs])
                else:
                    raise ValueError("fake: unsupported SET rhs %r" % rhs)
            else:
                key = names[clause] if clause.startswith("#") else clause
                row.pop(key, None)


class World:
    def __init__(self, row=None, param=None):
        self.row = copy.deepcopy(row)
        self.param = param
        self.calls = []  # (service, op, kwargs, ok, row_after)

    def rec(self, svc, op, kw, ok):
        self.calls.append((svc, op, copy.deepcopy(kw), ok, copy.deepcopy(self.row)))

    def writes(self):
        return [c for c in self.calls if c[1] in ("update_item", "put_item", "delete_item", "put_parameter",
                                                    "delete_parameter")]


WORLD = World()


class FakeDDB:
    def get_item(self, **kw):
        WORLD.rec("ddb", "get_item", kw, True)
        return {"Item": copy.deepcopy(WORLD.row)} if WORLD.row is not None else {}

    def put_item(self, **kw):
        raise AssertionError("fake: put_item is out of this check's scope")

    def update_item(self, **kw):
        names = kw.get("ExpressionAttributeNames") or {}
        values = kw.get("ExpressionAttributeValues") or {}
        used = _referenced(kw.get("UpdateExpression"), kw.get("ConditionExpression"))
        unused = (set(names) | set(values)) - used
        if unused:
            WORLD.rec("ddb", "update_item", kw, False)
            raise _cerr("ValidationException", "UpdateItem", {"Error": {"Code": "ValidationException",
                        "Message": "unused in expressions: %s" % sorted(unused)}})
        cur = WORLD.row if WORLD.row is not None else {}
        cond = kw.get("ConditionExpression")
        if cond and not _Expr(cond, names, values, cur).run():
            WORLD.rec("ddb", "update_item", kw, False)
            extra = {"Item": copy.deepcopy(cur)} if kw.get("ReturnValuesOnConditionCheckFailure") == "ALL_OLD" else {}
            raise _cerr("ConditionalCheckFailedException", "UpdateItem", extra)
        new = copy.deepcopy(cur)
        new.update(kw["Key"])
        _apply_update(new, kw["UpdateExpression"], names, values)
        WORLD.row = new
        WORLD.rec("ddb", "update_item", kw, True)
        return {}


class FakeSSM:
    def put_parameter(self, **kw):
        WORLD.param = kw["Value"]
        WORLD.rec("ssm", "put_parameter", {k: v for k, v in kw.items() if k != "Value"}, True)
        return {"Version": 1}

    def get_parameter(self, **kw):
        WORLD.rec("ssm", "get_parameter", kw, WORLD.param is not None)
        if WORLD.param is None:
            raise _cerr("ParameterNotFound", "GetParameter")
        return {"Parameter": {"Name": kw["Name"], "Value": WORLD.param}}

    def delete_parameter(self, **kw):
        ok = WORLD.param is not None
        WORLD.rec("ssm", "delete_parameter", kw, ok)
        if not ok:
            raise _cerr("ParameterNotFound", "DeleteParameter")
        WORLD.param = None
        return {}


MUTANT = {"strip_disarm_conditions": False}


class StripDDB(FakeDDB):
    def update_item(self, **kw):
        if MUTANT["strip_disarm_conditions"]:
            kw = dict(kw)
            cond = kw.pop("ConditionExpression", None)
            kw.pop("ReturnValuesOnConditionCheckFailure", None)
            # drop the names/values only the condition used, so the fake does not refuse them as unused
            keep = _referenced(kw.get("UpdateExpression"))
            if cond:
                for k in ("ExpressionAttributeNames", "ExpressionAttributeValues"):
                    if k in kw:
                        kw[k] = {n: v for n, v in kw[k].items() if n in keep}
                        if not kw[k]:
                            kw.pop(k)
        return FakeDDB.update_item(self, **kw)


def _fake_client(name, *a, **k):
    if name == "dynamodb":
        return StripDDB()
    if name == "ssm":
        return FakeSSM()
    raise AssertionError("fake boto3: client %r is not offered (no live AWS in this check)" % name)


def _install_fakes():
    fake = types.ModuleType("boto3")
    fake.client = _fake_client
    fake.Session = lambda *a, **k: (_ for _ in ()).throw(AssertionError("fake boto3: Session refused"))
    sys.modules["boto3"] = fake

    def _urlopen(req, *a, **k):
        url = getattr(req, "full_url", str(req))
        raise urllib.error.HTTPError(url, 401, "Unauthorized", {}, io.BytesIO(b'{"error":"stub refused"}'))
    urllib.request.urlopen = _urlopen


def _load(path, tag):
    spec = importlib.util.spec_from_file_location("walkerlease_target_%s" % tag, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _call(fn, *args):
    out, err = io.StringIO(), io.StringIO()
    exc = None
    ret = None
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            ret = fn(*args)
        except BaseException as e:  # SystemExit is the module's refusal channel
            exc = e
    return ret, exc, out.getvalue() + err.getvalue()


def _ok_exit(exc):
    return exc is None or (isinstance(exc, SystemExit) and exc.code in (None, 0))


def _seed_row(**extra):
    row = {"PK": {"S": "USER#usr_opal_ui_walker"}, "SK": {"S": "PROFILE"}, "email": {"S": "opal-ui-walker@opal.test"},
           "passwordHash": {"S": "$2b$12$seedseedseedseedseedse"}, "role": {"S": "admin"},
           "firmId": {"S": "opal-capital"}, "userType": {"S": "Dev"}, "status": {"S": "disabled"}}
    for k, v in extra.items():
        row[k] = {"S": v}
    return row


def _reset(row=None, param=None):
    global WORLD
    WORLD = World(row, param)
    return WORLD


def _holder_accepted(mod):
    try:
        inspect.signature(mod.disarm).bind("x")
        return True
    except (TypeError, ValueError):
        return False


# ---- sub-clauses: each returns (ok, reason) -------------------------------------------------------------------------
def p_a(mod, arm_fn=None):
    arm_fn = arm_fn or mod.arm
    holders = []
    for n in (1, 2):
        w = _reset(_seed_row(), None)
        ret, exc, text = _call(arm_fn)
        if not _ok_exit(exc):
            return False, "arm on a free row raised %r" % (exc,)
        puts = [i for i, c in enumerate(w.calls) if c[1] == "put_parameter"]
        if not puts:
            return False, "arm wrote no SSM PutParameter"
        before = [c for c in w.writes() if w.calls.index(c) < puts[0]]
        ddb_before = [c for c in before if c[0] == "ddb"]
        if any(c[0] == "ssm" for c in before):
            return False, "an SSM write precedes the first PutParameter"
        if len(ddb_before) != 1:
            return False, "%d DynamoDB write(s) before the first SSM PutParameter (want exactly 1)" % len(ddb_before)
        c = ddb_before[0]
        if not (c[2].get("ConditionExpression") and c[3]):
            return False, "the DynamoDB write before PutParameter is not a successful CONDITIONAL UpdateItem"
        after = c[4] or {}
        if "armedBy" not in after or "armedAt" not in after:
            return False, "the conditional UpdateItem did not set armedBy+armedAt"
        h = after["armedBy"]["S"]
        if not h or h not in (str(ret) + text):
            return False, "holder id %r is not passed back to the caller (return value or stdout)" % h
        if socket.gethostname() not in h:
            return False, "holder id %r does not carry the device hostname" % h
        if (w.row.get("status") or {}).get("S") != "active":
            return False, "row not active after arm"
        holders.append(h)
    if holders[0] == holders[1]:
        return False, "two arms minted the same holder id %r (not unique per walk)" % holders[0]
    return True, "one conditional UpdateItem (armedBy/armedAt) precedes PutParameter; holder %s" % holders[0]


def p_b(mod):
    seed = _seed_row(status="active", armedBy=OTHER, armedAt=_iso(5))
    w = _reset(seed, "other-walk-password")
    ret, exc, text = _call(mod.arm)
    blob = text + ("" if exc is None else str(exc))
    if _ok_exit(exc) and "HELD" not in blob:
        return False, "arm on a row held by %s (5 min ago) did not refuse" % OTHER
    if "HELD" not in blob or OTHER not in blob:
        return False, "refusal text lacks 'HELD by %s'" % OTHER
    if any(c[0] == "ssm" and c[1] in ("put_parameter", "delete_parameter") for c in w.calls):
        return False, "an SSM write happened on a held row"
    if any(c[3] for c in w.writes()):
        return False, "a successful write happened on a held row"
    if w.row != seed or w.param != "other-walk-password":
        return False, "row or SSM changed on a held row"
    return True, "HELD refusal, no SSM call, nothing written"


def p_c(mod):
    seed = _seed_row(status="active", armedBy=OTHER, armedAt=_iso(120))
    w = _reset(seed, None)
    ret, exc, text = _call(mod.arm)
    if not _ok_exit(exc):
        return False, "arm on a stale lease (120 min) raised %r" % (exc,)
    h = (w.row.get("armedBy") or {}).get("S")
    if not h or h == OTHER:
        return False, "stale lease not taken over (armedBy=%r)" % h
    if (w.row.get("armedAt") or {}).get("S", "") < _iso(5):
        return False, "armedAt not refreshed"
    if not any(c[1] == "put_parameter" for c in w.calls):
        return False, "no SSM PutParameter after the takeover"
    return True, "stale lease taken over by %s" % h


def p_d(mod):
    if not _holder_accepted(mod):
        return False, "disarm takes no holder argument"
    holder = "site-z:1234:0a0b0c0d"
    seed = _seed_row(status="active", armedBy=holder, armedAt=_iso(5))
    w = _reset(seed, "the-walk-password")
    ret, exc, text = _call(mod.disarm, holder)
    if not _ok_exit(exc):
        return False, "holder disarm raised %r" % (exc,)
    conds = [c for c in w.calls if c[1] == "update_item" and c[3] and c[2].get("ConditionExpression")]
    if not conds:
        return False, "no successful CONDITIONAL UpdateItem"
    kw = conds[0][2]
    counter = dict(seed)
    counter["armedBy"] = {"S": INTRUDER}
    if _Expr(kw["ConditionExpression"], kw.get("ExpressionAttributeNames") or {},
             kw.get("ExpressionAttributeValues") or {}, counter).run():
        return False, "the condition also admits a row held by another holder (not armedBy = holder)"
    r = w.row
    if (r.get("status") or {}).get("S") != "disabled" or "armedBy" in r or "armedAt" in r:
        return False, "row after disarm: status=%s armedBy=%s armedAt=%s" % (
            (r.get("status") or {}).get("S"), "armedBy" in r, "armedAt" in r)
    if not any(c[1] == "delete_parameter" for c in w.calls) or w.param is not None:
        return False, "SSM DeleteParameter not sent"
    return True, "conditional UpdateItem (armedBy = holder) + DeleteParameter; armedBy/armedAt removed"


def p_e(mod):
    if not _holder_accepted(mod):
        return False, "disarm takes no holder argument"
    seed = _seed_row(status="active", armedBy=OTHER, armedAt=_iso(5))
    w = _reset(seed, "other-walk-password")
    ret, exc, text = _call(mod.disarm, INTRUDER)
    if _ok_exit(exc):
        return False, "non-holder disarm did not refuse"
    if any(c[1] == "delete_parameter" for c in w.calls):
        return False, "non-holder disarm sent DeleteParameter"
    if w.row != seed or w.param != "other-walk-password":
        return False, "non-holder disarm changed the row or SSM"
    return True, "non-holder refused, nothing changed"


_JS_SKIP = {"null", "true", "false", "undefined", "await", "new", "String", "this"}


def p_f(walk_text):
    lines = walk_text.splitlines()
    arm_lines = [ln for ln in lines if re.search(r"""['"]arm['"]""", ln) and not ln.lstrip().startswith("//")]
    if not arm_lines:
        return False, "no arm invocation found"
    assign = re.compile(r"([A-Za-z_$][\w$.]*)\s*(?<![=!<>])=(?![=>])")
    got = set()
    for ln in arm_lines:
        got |= {m.split(".")[0] for m in assign.findall(ln)}
    for _ in range(2):  # one hop: a name assigned from a name the arm line assigned
        for ln in lines:
            for m in assign.finditer(ln):
                rhs = ln[m.end():]
                if any(re.search(r"\b%s\b" % re.escape(g), rhs) for g in got):
                    got.add(m.group(1).split(".")[0])
    calls = re.findall(r"""['"]disarm['"]\s*,([^)\n]*)\)""", walk_text)
    if not calls:
        return False, "the disarm invocation passes no argument"
    for args in calls:
        ids = set(re.findall(r"[A-Za-z_$][\w$]*", args)) - _JS_SKIP
        hit = sorted(ids & got)
        for h in hit:
            if re.search(r"^(?:let|var|const)\b[^\n;]*\b%s\b" % re.escape(h), walk_text, flags=re.M):
                return True, "disarm carries %s, assigned from the arm output, declared at module scope" % h
        if hit:
            return False, "disarm carries %s but it is not declared at module scope (finally cannot see it)" % hit
    return False, "no disarm argument traces back to the arm output"


CLAUSES = "abcdef"


def run_all(mod, walk_text):
    res = {}
    for k, fn in zip("abcde", (p_a, p_b, p_c, p_d, p_e)):
        try:
            res[k] = fn(mod)
        except Exception as e:  # a crash in the predicate is a FAIL with its cause named
            res[k] = (False, "predicate crashed: %s: %s" % (type(e).__name__, e))
    res["f"] = p_f(walk_text)
    return res


def legacy_probe(mod):
    """ADVISORY, not scored: a row armed by the PRE-FIX code (armedAt fresh, no armedBy) -- does arm respect it?"""
    seed = _seed_row(status="active", armedAt=_iso(5))
    w = _reset(seed, "legacy-walk-password")
    ret, exc, text = _call(mod.arm)
    return "REFUSED" if (w.row == seed and w.param == "legacy-walk-password") else "ADMITTED (would kill the legacy walk)"


def main():
    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
    _install_fakes()
    mod_path = os.path.join(root, MOD_REL)
    walk_text = open(os.path.join(root, WALK_REL), encoding="utf-8").read()
    green = _load(mod_path, "checkout")
    passed = 0

    # ARM 1
    r1 = run_all(green, walk_text)
    ok1 = all(v[0] for v in r1.values())
    passed += ok1
    print("ARM 1 GREEN    %s -- %d of 6 sub-clauses PASS on %s" % ("PASS" if ok1 else "FAIL", sum(v[0] for v in r1.values()), MOD_REL))
    for k in CLAUSES:
        print("   (%s) %s: %s" % (k, "PASS" if r1[k][0] else "FAIL", r1[k][1]))
    print("   INFO (advisory, unscored): a legacy-armed row (armedAt fresh, no armedBy) -> arm %s" % legacy_probe(green))

    # ARM 2
    tmp = tempfile.mkdtemp(prefix="walkerlease-base-")
    blobs = {}
    for rel in (MOD_REL, WALK_REL):
        p = subprocess.run(["git", "show", "%s:%s" % (BASE_PIN, rel)], capture_output=True, cwd=root)
        if p.returncode != 0 or not p.stdout:
            print("ARM 2 NEGATIVE FAIL -- git show %s:%s rc=%d (%d bytes)" % (BASE_PIN[:10], rel, p.returncode, len(p.stdout)))
            blobs = None
            break
        dst = os.path.join(tmp, os.path.basename(rel))
        with open(dst, "wb") as fh:
            fh.write(p.stdout)
        blobs[rel] = dst
    if blobs is not None:
        base = _load(blobs[MOD_REL], "base")
        r2 = run_all(base, open(blobs[WALK_REL], encoding="utf-8").read())
        failing = [k for k in CLAUSES if not r2[k][0]]
        ok2 = len(failing) == len(CLAUSES)
        passed += ok2
        print("ARM 2 NEGATIVE %s -- base %s fails %d of 6 sub-clauses: %s" % (
            "PASS" if ok2 else "FAIL", BASE_PIN[:10], len(failing), ",".join(failing) or "none"))
        for k in CLAUSES:
            print("   (%s) base %s: %s" % (k, "FAIL" if not r2[k][0] else "PASS (predicate does not discriminate)", r2[k][1]))

    # ARM 3
    mutant_mod = _load(mod_path, "mutant")
    MUTANT["strip_disarm_conditions"] = True
    try:
        m1 = p_e(mutant_mod)
    finally:
        MUTANT["strip_disarm_conditions"] = False

    def ssm_first():
        _fake_client("ssm").put_parameter(Name=mutant_mod.PARAM, Value="mutant-first", Type="SecureString", Overwrite=True)
        return mutant_mod.arm()
    m2 = p_a(mutant_mod, ssm_first)
    live_a, live_e = r1["a"][0], r1["e"][0]
    ok3 = (not m1[0]) and (not m2[0]) and live_a and live_e
    passed += ok3
    print("ARM 3 CONTROL  %s -- M1 disarm-without-conditions %s by (e) [%s]; M2 SSM-before-DynamoDB %s by (a) [%s]; unmutated (a)=%s (e)=%s" % (
        "PASS" if ok3 else "FAIL", "REJECTED" if not m1[0] else "ADMITTED", m1[1], "REJECTED" if not m2[0] else "ADMITTED",
        m2[1], "PASS" if live_a else "FAIL", "PASS" if live_e else "FAIL"))
    if not (live_a and live_e):
        print("   control is VACUOUS: the unmutated checkout fails (a)/(e), so a rejection proves nothing")

    print("%s: %d of 3 arms" % (TITLE, passed))
    return 0 if passed == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
