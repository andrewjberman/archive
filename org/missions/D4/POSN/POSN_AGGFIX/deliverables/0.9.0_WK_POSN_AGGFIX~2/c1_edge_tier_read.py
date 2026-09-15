#!/usr/bin/env python3
"""EDGE_TIER_READ_C1 -- POSN_AGGFIX.TO-C1-1, criterion C1-AC2 (cell AF1-s-4).

For shared-advisor-router, auth-validator-edge and public-data-router AT HEAD (read from git objects,
never the working tree): every tier / role / firm / userType branch with its line range and the URI
prefixes it applies to, and one line per function stating whether any such branch applies to
/api/general/positioning/.

METHOD (a structural read of the committed source, printed so it can be checked):
  1. The source is MASKED (comments blanked; string, template and regex literal bodies blanked) so braces
     and parentheses are matched on code only; regex literals are recovered from the scanner's spans.
  2. An IDENTITY BRANCH is an `if` clause whose condition names an identifier containing tier / role /
     firm / usertype / admin, or a variable holding such an expression or the result of a helper whose own
     conditions do; every `if` inside a helper whose NAME carries one of those words is listed too.
  3. Its URI SCOPE is the conjunction of URI guards on (a) every enclosing `if`, (b) its own condition,
     (c) early-return guards earlier in the same function (`if (!x.startsWith(P)) return`), and (d) for a
     branch inside a helper, the guards at the helper's call sites. A guard is a string literal of the
     form '/<letter>...', a regex literal, or a const / variable / helper resolved to those.
  4. A branch APPLIES to a URI when the function is associated with the behaviour CloudFront selects for
     that URI (TF parse, shared with c1_edge_route_census.py), the URI satisfies every scope level, and at
     least one non-pass EFFECT in its body (a return other than null / request / L0, or an assignment) is
     reachable under its own nested guards. A regex that cannot be compiled is UNRESOLVED, never a match,
     and an UNRESOLVED branch makes the function's verdict UNRESOLVED rather than NONE.
  5. POSITIVE CONTROLS: a URI on which each function's branches are known to run is scored the same way,
     so a NONE is shown to come from the scope and not from a reader that sees nothing.
Exit 0 when the read completes (the verdict is the output); 2 on a read failure.
"""
from __future__ import annotations

import bisect
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("c1_edge_route_census", HERE / "c1_edge_route_census.py")
census = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(census)
ROOT = census.ROOT

FUNCS = [
    ("shared-advisor-router", "infra/aws/lambda-edge/shared-advisor-router", ["index.mjs", "tier_policy.mjs"]),
    ("auth-validator-edge", "infra/aws/lambda-edge/auth-validator-edge", ["index.mjs", "tier_policy.mjs"]),
    ("public-data-router", "infra/aws/lambda-edge/public-data-router", ["index.mjs"]),
]
TARGETS = [
    "/api/general/positioning/opal_aggregate.json",
    "/api/general/positioning/positioning_data.json",
    "/api/general/positioning/model.json",
]
POSITIVE = {
    "shared-advisor-router": "/api/scoped/advisor-intelligence/artifacts/timeseries_chart.json",
    "auth-validator-edge": "/api/scoped/advisor-intelligence/clients/abc/detail",
    "public-data-router": "/api/general/json/positioning/positioning_data.json",
}
IDENT_RE = re.compile(r"tier|role|firm|usertype|admin", re.I)
PASS_RETURN = re.compile(r"^return\s*(null|request|true|false|'L0'|\"L0\")?\s*;?$")
URI_LIT = re.compile(r"^/[A-Za-z]")
UNRESOLVED: set = set()


def git_show(rel: str) -> str:
    p = subprocess.run(["git", "show", f"HEAD:{rel}"], capture_output=True, cwd=str(ROOT))
    if p.returncode != 0 or not p.stdout:
        print(f"ERROR: git show HEAD:{rel} rc={p.returncode} bytes={len(p.stdout)}")
        sys.exit(2)
    return p.stdout.decode("utf-8")


class Src:
    """One JS module: original text, masked text, regex literal spans."""

    def __init__(self, text: str, name: str):
        self.text, self.name = text, name
        self.mask, self.regex_spans = self._mask(text)
        self.nl = [i for i, c in enumerate(text) if c == "\n"]

    def line(self, off: int) -> int:
        return bisect.bisect_left(self.nl, off) + 1

    @staticmethod
    def _mask(s: str):
        out = list(s)
        n, i = len(s), 0
        prev_sig, word, prev_word = "", "", ""
        regex_spans = []
        while i < n:
            c = s[i]
            nx = s[i + 1] if i + 1 < n else ""
            if c == "/" and nx == "/":
                j = s.find("\n", i)
                j = n if j == -1 else j
                for k in range(i, j):
                    out[k] = " "
                i = j
                continue
            if c == "/" and nx == "*":
                j = s.find("*/", i + 2)
                j = n if j == -1 else j + 2
                for k in range(i, j):
                    if s[k] != "\n":
                        out[k] = " "
                i = j
                continue
            if c in "\"'":
                j = i + 1
                while j < n and s[j] != c:
                    j += 2 if s[j] == "\\" else 1
                for k in range(i + 1, min(j, n)):
                    if s[k] != "\n":
                        out[k] = "_"
                i, prev_sig, word = j + 1, c, ""
                continue
            if c == "`":
                j, depth = i + 1, 0
                while j < n:
                    if s[j] == "\\":
                        j += 2
                        continue
                    if s[j] == "`" and depth == 0:
                        break
                    if s.startswith("${", j):
                        depth += 1
                        j += 2
                        continue
                    if s[j] == "}" and depth:
                        depth -= 1
                    j += 1
                for k in range(i + 1, min(j, n)):
                    if s[k] != "\n":
                        out[k] = "_"
                i, prev_sig, word = j + 1, "`", ""
                continue
            if c == "/" and (prev_sig == "" or prev_sig in "(,=:[!&|?{};+-*%<>~^" or prev_word in ("return", "typeof")):
                j, in_class = i + 1, False
                while j < n and s[j] != "\n":
                    if s[j] == "\\":
                        j += 2
                        continue
                    if s[j] == "[":
                        in_class = True
                    elif s[j] == "]":
                        in_class = False
                    elif s[j] == "/" and not in_class:
                        break
                    j += 1
                end = j
                j += 1
                while j < n and s[j].isalpha():
                    j += 1
                for k in range(i + 1, end):
                    out[k] = "_"
                regex_spans.append((i, end))
                i, prev_sig, word = j, "/", ""
                continue
            if c.isalnum() or c in "_$":
                word += c
                prev_sig = "w"
            else:
                if word:
                    prev_word, word = word, ""
                if not c.isspace():
                    prev_sig = c
                    if c != ")":
                        prev_word = ""
            i += 1
        return "".join(out), regex_spans


def match_close(mask: str, open_idx: int) -> int:
    pair = {"(": ")", "{": "}", "[": "]"}
    o = mask[open_idx]
    depth = 0
    for k in range(open_idx, len(mask)):
        if mask[k] == o:
            depth += 1
        elif mask[k] == pair[o]:
            depth -= 1
            if depth == 0:
                return k
    return len(mask) - 1


def statement_end(mask: str, start: int) -> int:
    depth = 0
    for k in range(start, len(mask)):
        ch = mask[k]
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth -= 1
            if depth < 0:
                return k - 1
        elif ch == ";" and depth == 0:
            return k
    return len(mask) - 1


def parse(src: Src) -> dict:
    m = src.mask
    ifs = []
    for mo in re.finditer(r"\b(else\s+)?if\s*\(", m):
        p_open = mo.end() - 1
        p_close = match_close(m, p_open)
        k = p_close + 1
        while k < len(m) and m[k].isspace():
            k += 1
        if k < len(m) and m[k] == "{":
            b_start, b_end = k, match_close(m, k)
        else:
            b_start, b_end = k, statement_end(m, k)
        ifs.append({"kw": mo.start(), "cond": (p_open + 1, p_close), "body": (b_start, b_end),
                    "else": bool(mo.group(1))})
    funcs = []
    for mo in re.finditer(r"\bfunction\s+([A-Za-z_$][\w$]*)\s*\(", m):
        p_close = match_close(m, mo.end() - 1)
        b = m.find("{", p_close)
        funcs.append({"name": mo.group(1), "body": (b, match_close(m, b))})
    for mo in re.finditer(r"\bconst\s+([A-Za-z_$][\w$]*)\s*=\s*(async\s*)?\([^)]*\)\s*=>\s*\{", m):
        b = mo.end() - 1
        funcs.append({"name": mo.group(1), "body": (b, match_close(m, b))})
    decls: dict = {}
    for mo in re.finditer(r"\b(const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*", m):
        e_end = statement_end(m, mo.end())
        decls.setdefault(mo.group(2), []).append((mo.start(), mo.end(), e_end))
    assigns = []
    for mo in re.finditer(r"(?<![\w$.\]=!<>+\-*/%&|^])([A-Za-z_$][\w$]*(?:\.[\w$]+|\[[^\]]*\])*)\s*=(?![=>])", m):
        before = m[max(0, mo.start() - 6):mo.start()]
        if re.search(r"\b(const|let|var)\s*$", before):
            continue
        assigns.append((mo.start(), mo.group(1)))
    return {"ifs": ifs, "funcs": funcs, "decls": decls, "assigns": assigns}


def consts_of(src: Src) -> dict:
    out = {}
    for mo in re.finditer(r"\bconst\s+([A-Z_][A-Z0-9_]*)\s*=\s*", src.mask):
        k = mo.end()
        ch = src.text[k] if k < len(src.text) else ""
        if ch in "\"'":
            j = src.text.find(ch, k + 1)
            out[mo.group(1)] = ("str", src.text[k + 1:j])
        elif ch == "/":
            span = next(((a, b) for a, b in src.regex_spans if a == k), None)
            if span:
                out[mo.group(1)] = ("re", [src.text[span[0]:span[1] + 1]])
        elif ch == "[":
            end = match_close(src.mask, k)
            regs = [src.text[a:b + 1] for a, b in src.regex_spans if k < a and b <= end]
            if regs:
                out[mo.group(1)] = ("re", regs)
    return out


def js_regex(lit: str):
    body = lit[1:lit.rfind("/")]
    try:
        return re.compile(body.replace("\\/", "/"))
    except re.error:
        UNRESOLVED.add(lit)
        return None


class Module:
    def __init__(self, fn: str, srcs: list[Src]):
        self.fn = fn
        self.srcs = srcs
        self.p = {s.name: parse(s) for s in srcs}
        self.consts: dict = {}
        for s in srcs:
            self.consts.update(consts_of(s))
        self.names = self._tainted()

    def enclosing_func(self, s: Src, off: int):
        best = None
        for f in self.p[s.name]["funcs"]:
            if f["body"][0] <= off <= f["body"][1] and (best is None or f["body"][0] > best["body"][0]):
                best = f
        return best

    def func_by_name(self, name: str):
        for s in self.srcs:
            for f in self.p[s.name]["funcs"]:
                if f["name"] == name:
                    return s, f
        return None

    def literals_in_span(self, s: Src, a: int, b: int, depth: int = 0) -> list[tuple[str, str]]:
        lits: list[tuple[str, str]] = []
        seg = s.text[a:b + 1]
        for mo in re.finditer(r'"([^"]*)"|\'([^\']*)\'', seg):
            val = mo.group(1) if mo.group(1) is not None else mo.group(2)
            if URI_LIT.match(val):
                lits.append(("prefix", val))
        for ra, rb in s.regex_spans:
            if a <= ra and rb <= b:
                lits.append(("regex", s.text[ra:rb + 1]))
        if depth > 3:
            return lits
        for ident in sorted(set(re.findall(r"[A-Za-z_$][\w$]*", s.mask[a:b + 1]))):
            if ident in self.consts:
                kind, val = self.consts[ident]
                if kind == "str" and URI_LIT.match(val):
                    lits.append(("prefix", val))
                elif kind == "re":
                    lits.extend(("regex", r) for r in val)
                continue
            for _d_start, d_end, e_end in self.p[s.name]["decls"].get(ident, []):
                expr = s.mask[d_end:e_end + 1]
                call = re.match(r"\s*(?:await\s+)?([A-Za-z_$][\w$]*)\s*\(", expr)
                if call and self.func_by_name(call.group(1)):
                    fs, f = self.func_by_name(call.group(1))
                    lits.extend(self.literals_in_span(fs, f["body"][0], f["body"][1], depth + 1))
                elif re.match(r"^\s*null\s*;?\s*$", expr):
                    for off, name in self.p[s.name]["assigns"]:
                        if name == ident:
                            for lv in self.scope_levels(s, off, depth + 1):
                                lits.extend(lv)
        return lits

    def scope_levels(self, s: Src, off: int, depth: int = 0) -> list[list[tuple[str, str]]]:
        levels = []
        for c in self.p[s.name]["ifs"]:
            if c["body"][0] <= off <= c["body"][1] and not (c["kw"] <= off <= c["cond"][1]):
                lv = self.literals_in_span(s, c["cond"][0], c["cond"][1], depth)
                if lv:
                    levels.append(lv)
        f = self.enclosing_func(s, off)
        if f:
            fb = f["body"]
            early = re.compile(r"if\s*\(\s*!\s*[\w$.]+\.startsWith\(\s*[^)]*\)\s*\)\s*return")
            for mo in early.finditer(s.mask, fb[0], off):
                lv = self.literals_in_span(s, mo.start(), mo.end(), depth)
                if lv:
                    levels.append(lv)
            if f["name"] != "handler" and depth < 3:
                sites = []
                for s2 in self.srcs:
                    for mo in re.finditer(r"\b" + re.escape(f["name"]) + r"\s*\(", s2.mask):
                        if s2 is s and fb[0] <= mo.start() <= fb[1]:
                            continue
                        if re.search(r"function\s+$", s2.mask[max(0, mo.start() - 9):mo.start()]):
                            continue
                        sites.append(self.scope_levels(s2, mo.start(), depth + 1))
                if len(sites) == 1:
                    levels.extend(sites[0])
                elif len(sites) > 1 and all(sites):
                    levels.append([x for site in sites for lv in site for x in lv])
        return levels

    def _cond_ids(self, s: Src, c: dict) -> list[str]:
        return re.findall(r"[A-Za-z_$][\w$]*", s.mask[c["cond"][0]:c["cond"][1] + 1])

    def _tainted(self) -> set:
        names: set = set()
        for s in self.srcs:
            for ident, ds in self.p[s.name]["decls"].items():
                for _a, d_end, e_end in ds:
                    if any(IDENT_RE.search(x) for x in re.findall(r"[A-Za-z_$][\w$]*", s.mask[d_end:e_end + 1])):
                        names.add(ident)
        changed = True
        while changed:
            changed = False
            for s in self.srcs:
                pp = self.p[s.name]
                for f in pp["funcs"]:
                    if f["name"] in names or f["name"] == "handler":
                        continue
                    inner = [c for c in pp["ifs"] if f["body"][0] < c["kw"] < f["body"][1]]
                    if any(any(IDENT_RE.search(x) or x in names for x in self._cond_ids(s, c)) for c in inner):
                        names.add(f["name"])
                        changed = True
                for ident, ds in pp["decls"].items():
                    if ident in names:
                        continue
                    for _a, d_end, e_end in ds:
                        call = re.match(r"\s*(?:await\s+)?([A-Za-z_$][\w$]*)\s*\(", s.mask[d_end:e_end + 1])
                        if call and call.group(1) in names:
                            names.add(ident)
                            changed = True
                            break
        return names

    def branches(self) -> list[dict]:
        out = []
        for s in self.srcs:
            for c in self.p[s.name]["ifs"]:
                ident = any(IDENT_RE.search(x) or x in self.names for x in self._cond_ids(s, c))
                f = self.enclosing_func(s, c["kw"])
                in_named_helper = bool(f and f["name"] != "handler" and IDENT_RE.search(f["name"]))
                if ident or in_named_helper:
                    out.append({"src": s, "if": c})
        return out

    def effects(self, s: Src, c: dict) -> list[int]:
        a, b = c["body"]
        effs = []
        for mo in re.finditer(r"\breturn\b", s.mask[a:b + 1]):
            st = a + mo.start()
            en = statement_end(s.mask, st)
            stmt = re.sub(r"\s+", " ", s.text[st:en + 1]).strip()
            if not PASS_RETURN.match(stmt):
                effs.append(st)
        for off, _name in self.p[s.name]["assigns"]:
            if a <= off <= b:
                effs.append(off)
        return effs

    def applies(self, s: Src, c: dict, uri: str, assoc: bool) -> tuple[bool, str]:
        if not assoc:
            return False, "function not associated with the behaviour CloudFront selects"
        levels = self.scope_levels(s, c["kw"] + 1)
        own = self.literals_in_span(s, c["cond"][0], c["cond"][1])
        if own:
            levels = levels + [own]
        for lv in levels:
            if not satisfies(uri, lv):
                return False, "URI outside scope " + fmt_level(lv)
        effs = self.effects(s, c)
        if not effs:
            return False, "no non-pass effect in the body"
        for off in effs:
            inner = [self.literals_in_span(s, x["cond"][0], x["cond"][1]) for x in self.p[s.name]["ifs"]
                     if c["body"][0] < x["kw"] and x["body"][0] <= off <= x["body"][1]]
            if all(satisfies(uri, lv) for lv in inner if lv):
                return True, "a non-pass effect is reachable"
        return False, "every non-pass effect sits under a URI guard the URI fails"


def satisfies(uri: str, level: list[tuple[str, str]]) -> bool:
    for kind, val in level:
        if kind == "prefix" and uri.startswith(val):
            return True
        if kind == "regex":
            rx = js_regex(val)
            if rx is not None and rx.search(uri):
                return True
    return False


def fmt_level(level: list[tuple[str, str]]) -> str:
    return "{" + " | ".join(dict.fromkeys(v for _k, v in level)) + "}"


def main() -> int:
    head = subprocess.run(["git", "rev-parse", "--short=10", "HEAD"], capture_output=True, text=True,
                          cwd=str(ROOT)).stdout.strip()
    print(f"C1-AC2 EDGE_TIER_READ_C1 -- vintage: git objects at HEAD {head} (working tree NOT read)")
    tf_list, _origins = census.tf_behaviours()

    def assoc_for(fn: str, uri: str) -> tuple[bool, str]:
        for b in tf_list:
            if census.pattern_re(b["pattern"]).match(uri):
                evs = [ev for ev, fns in b["assoc"].items() if fn in fns]
                return bool(evs), f"behaviour {b['pattern']} ({','.join(evs) or 'not associated'})"
        return False, "no behaviour"

    for fn, rel_dir, files in FUNCS:
        UNRESOLVED.clear()
        srcs = [Src(git_show(f"{rel_dir}/{f}"), f) for f in files]
        mod = Module(fn, srcs)
        brs = mod.branches()
        total_ifs = sum(len(mod.p[s.name]["ifs"]) for s in srcs)
        print("")
        print(f"== {fn} (" + ", ".join(f"{rel_dir}/{f} {len(s.text.splitlines())} lines" for f, s in zip(files, srcs)) + ")")
        print(f"   if-clauses parsed {total_ifs}; tier/role/firm/userType branches {len(brs)}; "
              f"URI consts resolved {sorted(k for k, v in mod.consts.items() if v[0] == 're' or URI_LIT.match(str(v[1])))}")
        applies_t: list[str] = []
        for br in brs:
            s, c = br["src"], br["if"]
            l1, l2 = s.line(c["kw"]), s.line(c["body"][1])
            cond = re.sub(r"\s+", " ", s.text[c["cond"][0]:c["cond"][1]]).strip()
            own = mod.literals_in_span(s, c["cond"][0], c["cond"][1])
            all_levels = mod.scope_levels(s, c["kw"] + 1) + ([own] if own else [])
            scope = " AND ".join(fmt_level(lv) for lv in all_levels) if all_levels else "ALL URIs the function sees"
            results = [(t,) + mod.applies(s, c, t, assoc_for(fn, t)[0]) for t in TARGETS]
            hit = any(r[1] for r in results)
            if hit:
                applies_t.append(f"{s.name}:{l1}-{l2}")
            print(f"   {s.name}:L{l1}-{l2} {'else if' if c['else'] else 'if'} ({cond[:110]})")
            print(f"      URI scope: {scope}")
            print(f"      /api/general/positioning/: {'APPLIES' if hit else 'does not apply'} -- {results[0][2]}")
        _assoc, why = assoc_for(fn, TARGETS[0])
        print(f"   association for {TARGETS[0]}: {why}")
        pos = POSITIVE[fn]
        passoc, pwhy = assoc_for(fn, pos)
        pos_hits = [f"{br['src'].name}:{br['src'].line(br['if']['kw'])}" for br in brs
                    if mod.applies(br["src"], br["if"], pos, passoc)[0]]
        print(f"   POSITIVE CONTROL {pos}: {pwhy}; branches applying {len(pos_hits)} of {len(brs)}"
              + (f" ({', '.join(pos_hits)})" if pos_hits else ""))
        if UNRESOLVED:
            print(f"   UNRESOLVED regex literals: {sorted(UNRESOLVED)}")
            verdict = "UNRESOLVED"
        else:
            verdict = "NONE" if not applies_t else f"{len(applies_t)} BRANCH(ES): " + ", ".join(applies_t)
        print(f"{fn}: ANY TIER/ROLE/FIRM/USERTYPE BRANCH APPLIES TO /api/general/positioning/: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
