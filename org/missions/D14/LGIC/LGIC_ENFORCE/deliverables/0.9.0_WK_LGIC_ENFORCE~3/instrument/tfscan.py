"""tfscan.py -- stdlib scanner for Terraform resource blocks. Scratch instrument of 0.9.0_WK_LGIC_ENFORCE~3 (EN-t-1).

scan(text) -> list of blocks: {kind, labels, line, attrs: [(key, line, raw_value)]} where attrs are the TOP-LEVEL
attributes of the block body (depth 1), raw_value the exact source text of the expression (single or multi line).
Handles # // /* */ comments, "strings" with ${...} / %{...} template nesting, and <<EOF / <<-EOF heredocs.
"""
import re


class Scanner:
    def __init__(self, text):
        self.t = text
        self.n = len(text)

    def line_of(self, i):
        return self.t.count("\n", 0, i) + 1

    def skip_string(self, i):
        """i at the opening quote; returns index after the closing quote."""
        t, n = self.t, self.n
        i += 1
        while i < n:
            c = t[i]
            if c == "\\":
                i += 2
                continue
            if c == '"':
                return i + 1
            if c in "$%" and i + 1 < n and t[i + 1] == "{":
                if i + 2 < n and t[i + 2] == "{":  # escaped? no: $${ is the escape; ${{ is not special
                    pass
                if i > 0 and t[i - 1] == c:  # $${ or %%{ escape
                    i += 1
                    continue
                i = self.skip_expr_braces(i + 1)
                continue
            i += 1
        return n

    def skip_heredoc(self, i):
        """i at '<<'; returns index after the terminator line, or None if not a heredoc."""
        m = re.match(r"<<(-?)([A-Za-z_][A-Za-z0-9_]*)[ \t]*\r?\n", self.t[i:])
        if not m:
            return None
        tag = m.group(2)
        j = i + m.end()
        pat = re.compile(r"^[ \t]*" + re.escape(tag) + r"[ \t]*\r?$", re.M)
        mm = pat.search(self.t, j)
        if not mm:
            return self.n
        return mm.end()

    def skip_comment(self, i):
        t = self.t
        if t[i] == "#" or t.startswith("//", i):
            j = t.find("\n", i)
            return self.n if j < 0 else j
        if t.startswith("/*", i):
            j = t.find("*/", i + 2)
            return self.n if j < 0 else j + 2
        return None

    def skip_expr_braces(self, i):
        """i at '{'; returns index after the matching '}' (expression context)."""
        t, n = self.t, self.n
        depth = 0
        while i < n:
            c = t[i]
            s = self.skip_comment(i) if c in "#/" else None
            if s is not None:
                i = s
                continue
            if c == '"':
                i = self.skip_string(i)
                continue
            if c == "<" and t.startswith("<<", i):
                h = self.skip_heredoc(i)
                if h is not None:
                    i = h
                    continue
            if c in "{[(":
                depth += 1
            elif c in "}])":
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return n


def _value_end(sc, i):
    """i at the first char of an attribute's expression; returns the index where the expression ends (a newline
    at bracket depth 0, not inside a string/heredoc/comment)."""
    t, n = sc.t, sc.n
    depth = 0
    while i < n:
        c = t[i]
        if c in "#/":
            s = sc.skip_comment(i)
            if s is not None:
                if t[i] == "/" and t.startswith("/*", i):
                    i = s
                    continue
                return i  # a line comment ends the expression at depth 0 (content before it)
                # (inside brackets a line comment is skipped below)
        if c == '"':
            i = sc.skip_string(i)
            continue
        if c == "<" and t.startswith("<<", i):
            h = sc.skip_heredoc(i)
            if h is not None:
                i = h
                continue
        if c in "{[(":
            depth += 1
        elif c in "}])":
            if depth == 0:
                return i
            depth -= 1
        elif c == "\n" and depth == 0:
            # an expression may continue on the next line after a trailing operator; HCL allows that only inside
            # brackets, so depth 0 newline ends it
            return i
        i += 1
    return n


def _value_end_full(sc, i):
    """Like _value_end but skips line comments that sit INSIDE brackets."""
    t, n = sc.t, sc.n
    depth = 0
    while i < n:
        c = t[i]
        if c in "#/":
            s = sc.skip_comment(i)
            if s is not None:
                if depth == 0 and not t.startswith("/*", i):
                    return i
                i = s
                continue
        if c == '"':
            i = sc.skip_string(i)
            continue
        if c == "<" and t.startswith("<<", i):
            h = sc.skip_heredoc(i)
            if h is not None:
                i = h
                continue
        if c in "{[(":
            depth += 1
        elif c in "}])":
            if depth == 0:
                return i
            depth -= 1
        elif c == "\n" and depth == 0:
            return i
        i += 1
    return n


BLOCK_HEAD = re.compile(r'([A-Za-z_][A-Za-z0-9_-]*)((?:[ \t]+(?:"(?:[^"\\\n]|\\.)*"|[A-Za-z_][A-Za-z0-9_-]*))*)[ \t]*\{')
ATTR_HEAD = re.compile(r"([A-Za-z_][A-Za-z0-9_-]*)[ \t]*=(?!=)[ \t]*")
LABEL = re.compile(r'"((?:[^"\\\n]|\\.)*)"|([A-Za-z_][A-Za-z0-9_-]*)')


def parse_body(sc, i, end, depth_limit_attrs=True):
    """Parse items in [i, end): returns (attrs, blocks). attrs: (key, line, raw); blocks: (kind, labels, line, start, end)."""
    t = sc.t
    attrs, blocks = [], []
    while i < end:
        c = t[i]
        if c in " \t\r\n;,":
            i += 1
            continue
        s = sc.skip_comment(i) if c in "#/" else None
        if s is not None:
            i = s
            continue
        m = ATTR_HEAD.match(t, i)
        if m:
            vstart = m.end()
            vend = _value_end_full(sc, vstart)
            attrs.append((m.group(1), sc.line_of(i), t[vstart:vend].strip()))
            i = vend
            continue
        m = BLOCK_HEAD.match(t, i)
        if m:
            labels = [a or b for a, b in LABEL.findall(m.group(2))]
            bstart = m.end() - 1
            bend = sc.skip_expr_braces(bstart)
            blocks.append((m.group(1), labels, sc.line_of(i), bstart + 1, bend - 1))
            i = bend
            continue
        # unrecognised: advance to next line
        j = t.find("\n", i)
        i = end if j < 0 else j + 1
    return attrs, blocks


def scan(text):
    text = text.replace("\r\n", "\n")
    sc = Scanner(text)
    _, top = parse_body(sc, 0, len(text))
    out = []
    for kind, labels, line, bs, be in top:
        attrs, sub = parse_body(sc, bs, be)
        out.append({"kind": kind, "labels": labels, "line": line, "attrs": attrs,
                    "subblocks": [(k, lb, ln) for k, lb, ln, _, _ in sub]})
    return out
