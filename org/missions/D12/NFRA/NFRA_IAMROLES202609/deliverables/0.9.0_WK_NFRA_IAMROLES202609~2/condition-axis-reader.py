#!/usr/bin/env python3
"""
condition-axis-reader.py -- NFRA_IAMROLES202609 task order TO-IAM-s-4, cell IAM-s-4.

THE ASK (FWD-3, verbatim from the ratified endpoint): "For any policy, a reviewer can see
what it REQUIRES of the caller, not only what it lets them touch."

Every existing IAM instrument in this estate (comp-iam included) answers "what resources
does this statement scope" -- the (action, resource) axis. NONE of them answer "what does
this statement demand of whoever invokes it": MFA, source address, principal tags, session
age, or any other Condition-block requirement. A statement can be immaculately scoped to one
ARN and still ask nothing of its caller, and today that reads as CLEAN. This reader makes
that absence VISIBLE instead of silent, by printing the literal token REQUIRES-NOTHING for
every statement that carries no Condition block at all.

BOUND -- C-DESIRED-UNTIL-EXERCISED (task order BOUNDS, G-15 + acceptance property 3):
Everything this reader reports is read from POLICY TEXT. That is DESIRED, never APPLIED and
never EXERCISED, until a real `aws iam simulate-principal-policy` battery runs against the
live role (that battery is cell IAM-s-8, not this one). A document read is not an applied
state and never an exercised one -- every finding below carries that label explicitly.

DISCIPLINE INHERITED FROM comp-iam's OWN Rule-22a limit (c), stated in this task order's
BATTERY FINDINGS: "Condition-block false-deny -> FIXED/CARRIED: --context-entries when
given; A CONDITIONED STATEMENT WITH NO CONTEXT IS UNKNOWN, NEVER A (FALSE) DENY." This
reader's mirror of that discipline: a Condition block this parser CANNOT resolve is reported
UNKNOWN, never REQUIRES-NOTHING. The two are opposite claims -- conflating "we could not
parse it" with "there is nothing there" would manufacture the very finding this cell exists
to surface honestly.

POPULATION BOUND (task order BOUNDS, PRD section 8 row S4 / brief Part VII item 5): this
reader reports what it read, for the one file named on its --policy argument, WITH a printed
denominator of statements examined in THAT file. It never aggregates across a run into an
estate-wide population claim, and it prints no sentence of the form "the estate is silent on
this axis" / "no policy requires MFA" / "all policies are silent" -- that inference is not
licensed by reading one file, or several, one at a time.

Usage: python condition-axis-reader.py --policy <path-to-a-terraform-iam-file>

Scope, deliberately: this cell READS. It does not modify any policy (narrowing is cell
IAM-s-8's question) and it mints no alert/alarm/monitor/schedule/notification.
"""
import argparse
import re
import sys


# ------------------------------------------------------------------------------------------
# Advisory-only pattern hints for well-known AWS condition keys. This is narrative colour
# printed for a human reviewer, NOT a ratified value-enum any downstream process consumes as
# a coded field -- so it does not carry Rule 24's MECE/census bar, which governs schemas an
# agent AUTHORS OR ADOPTS for consumption. It is not claimed exhaustive; an unrecognised key
# is printed with its raw operator/key/value and no hint, never suppressed.
# ------------------------------------------------------------------------------------------
KNOWN_KEY_HINTS = [
    ("aws:MultiFactorAuthPresent", "MFA"),
    ("aws:MultiFactorAuthAge", "MFA / session age"),
    ("aws:SourceIp", "source address"),
    ("aws:SourceVpc", "source network"),
    ("aws:SourceVpce", "source network (VPC endpoint)"),
    ("aws:VpcSourceIp", "source address"),
    ("aws:TokenIssueTime", "session age"),
    ("sts:RoleSessionName", "caller session identity"),
    ("sts:ExternalId", "caller identity (external id)"),
    ("aws:PrincipalTag", "principal tag"),
    ("aws:RequestTag", "request tag"),
    ("aws:userid", "caller identity"),
    ("aws:PrincipalArn", "caller identity"),
    ("aws:CalledViaFirst", "caller identity (call chain)"),
    ("aws:ResourceTag", "resource tag -- scopes the TARGET, not the caller"),
    ("ec2:ResourceTag", "resource tag -- scopes the TARGET, not the caller"),
    ("s3:prefix", "call parameter -- scopes the LIST call, not the caller"),
    ("cloudwatch:namespace", "call parameter -- scopes the request, not the caller"),
]


def hint_for(key):
    for prefix, label in KNOWN_KEY_HINTS:
        if key == prefix or key.startswith(prefix + "/"):
            return label
    return None


def strip_comments(text):
    """Quote-aware: blank out an unquoted '#' to end of line. Preserves line count so a
    reported location still lines up with the source file."""
    out_lines = []
    for line in text.split("\n"):
        in_str = False
        cut = None
        i = 0
        n = len(line)
        while i < n:
            ch = line[i]
            if in_str:
                if ch == "\\":
                    i += 1
                elif ch == '"':
                    in_str = False
            else:
                if ch == '"':
                    in_str = True
                elif ch == "#":
                    cut = i
                    break
            i += 1
        out_lines.append(line if cut is None else line[:cut])
    return "\n".join(out_lines)


def find_matching_close(text, open_idx):
    """text[open_idx] is '{' or '['. Return the index of its matching close bracket,
    quote-aware. Returns -1 if the text is unbalanced from that point on."""
    depth = 1
    in_str = False
    i = open_idx + 1
    n = len(text)
    while i < n:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def depth_map(text):
    """Bracket depth AT each index (before consuming that char), quote-aware, for `text`
    treated as a standalone span starting at depth 0. HCL/JSON-like content only: `{`/`[`
    push, `}`/`]` pop, quoted-string content is opaque (its interpolation `${...}` never
    changes depth)."""
    n = len(text)
    depths = [0] * (n + 1)
    depth = 0
    in_str = False
    i = 0
    while i < n:
        depths[i] = depth
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
                if i < n:
                    depths[i] = depth
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch in "{[":
                depth += 1
            elif ch in "}]":
                depth -= 1
        i += 1
    depths[n] = depth
    return depths


# A depth-0 ATTRIBUTE KEY: a bare HCL identifier or a quoted map key, immediately followed
# by '=' (not '==') once whitespace is skipped. HCL object-constructor syntax separates
# attributes by a newline OR a comma (both, redundantly, are also legal) -- so an attribute's
# value is bounded by the START of the NEXT depth-0 key, never by a comma alone. Comma-based
# splitting silently swallows an entire newline-separated object into one giant "value",
# which is exactly the trap this reader must not fall into on THIS estate's actual policy
# files (verified: this file's statement objects use newline separation with NO commas
# between Sid/Effect/Action/Resource).
_ATTR_KEY_RE = re.compile(r'(?:"([^"]+)"|([A-Za-z_][A-Za-z0-9_]*))\s*=(?!=)')


def find_top_level_attrs(inner):
    """Return an ordered list of (key_str, match_start, value_start) for every depth-0
    `key =` boundary in `inner` (depth computed relative to inner's own start, i.e. inner is
    the content strictly BETWEEN an object's outer braces)."""
    depths = depth_map(inner)
    attrs = []
    for m in _ATTR_KEY_RE.finditer(inner):
        if depths[m.start()] != 0:
            continue
        key_str = m.group(1) if m.group(1) is not None else m.group(2)
        attrs.append((key_str, m.start(), m.end()))
    return attrs


def parse_object(obj_text):
    """obj_text spans a full `{...}` INCLUDING its braces. Returns an ordered list of
    (key, value_str) pairs for its immediate (depth-1) children, delimited by the HCL
    attribute-boundary rule above (newline- or comma-separated, either legal). Raises
    ValueError if obj_text does not look like a brace-delimited object."""
    t = obj_text.strip()
    if not (t.startswith("{") and t.endswith("}")):
        raise ValueError("not a brace-delimited object: %r" % t[:60])
    inner = t[1:-1]
    attrs = find_top_level_attrs(inner)
    out = []
    for idx, (key_str, key_start, value_start) in enumerate(attrs):
        value_end = attrs[idx + 1][1] if idx + 1 < len(attrs) else len(inner)
        value = inner[value_start:value_end].strip()
        if value.endswith(","):
            value = value[:-1].rstrip()
        out.append((key_str, value))
    return out


def iter_top_level_objects(text, start, end):
    """Yield (obj_start, obj_end) absolute indices (obj_end is the index of the closing
    '}', inclusive) of each top-level `{...}` object inside text[start:end], where
    'top-level' means depth 0 relative to `start`."""
    depth = 0
    in_str = False
    i = start
    while i < end:
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 1
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            i += 1
            continue
        if ch == "{" and depth == 0:
            close = find_matching_close(text, i)
            if close == -1 or close > end:
                return
            yield (i, close)
            i = close + 1
            continue
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        i += 1


def analyze_statement(obj_text):
    """obj_text is one IAM statement, `{...}` inclusive. Returns a dict describing what it
    REQUIRES OF THE CALLER."""
    try:
        fields = parse_object(obj_text)
    except ValueError as exc:
        return {"status": "UNKNOWN", "sid": None, "effect": "<unparseable>",
                "detail": "statement object itself did not parse: %s" % exc}

    fmap = {}
    for k, v in fields:
        if k is not None and k not in fmap:
            fmap[k] = v

    sid = fmap.get("Sid")
    if sid:
        sid = sid.strip().strip('"')
    effect = fmap.get("Effect", "").strip().strip('"') or "<unspecified>"

    has_condition_keyword = re.search(r"\bCondition\b", obj_text) is not None

    if "Condition" not in fmap:
        if has_condition_keyword:
            # Rule-22a discipline, inherited: the token exists in the text but our
            # depth-aware key parse did not resolve it as this statement's own top-level
            # key (e.g. it sits nested somewhere unexpected, or the statement is malformed).
            # That is UNKNOWN, never REQUIRES-NOTHING.
            return {"status": "UNKNOWN", "sid": sid, "effect": effect,
                    "detail": "the literal token 'Condition' appears in this statement's "
                              "text but did not resolve as a clean top-level key -- reported "
                              "UNKNOWN per the comp-iam Rule-22a discipline this reader "
                              "inherits, never REQUIRES-NOTHING"}
        return {"status": "REQUIRES-NOTHING", "sid": sid, "effect": effect}

    cond_val = fmap["Condition"].strip()
    try:
        operators = parse_object(cond_val)
    except ValueError as exc:
        return {"status": "UNKNOWN", "sid": sid, "effect": effect,
                "detail": "Condition value did not parse as an object: %s" % exc}

    reqs = []
    parse_clean = True
    for op_name, op_val in operators:
        if op_name is None:
            parse_clean = False
            continue
        op_val_s = op_val.strip()
        try:
            pairs = parse_object(op_val_s)
        except ValueError:
            # Operator present but its value isn't the map shape this reader expects --
            # surface the raw text rather than silently dropping it, and flag the parse as
            # not fully clean (drives UNKNOWN rather than a confident REQUIRES-NOTHING).
            reqs.append((op_name, None, op_val_s))
            parse_clean = False
            continue
        if not pairs:
            parse_clean = False
        for ck, cv in pairs:
            if ck is None:
                parse_clean = False
                continue
            reqs.append((op_name, ck, cv.strip()))

    if not reqs:
        return {"status": "UNKNOWN", "sid": sid, "effect": effect,
                "detail": "a Condition block is present but no operator/key pair could be "
                          "extracted from it -- reported UNKNOWN, never REQUIRES-NOTHING"}

    status = "REQUIRES" if parse_clean else "REQUIRES (partial parse -- see UNPARSED note)"
    return {"status": status, "sid": sid, "effect": effect, "requirements": reqs,
            "clean": parse_clean}


def find_label(cleaned, match_start):
    """Best-effort label for the enclosing resource + policy-document kind of a Statement
    array found at match_start. Advisory only -- used for readability, never for scoring."""
    window_start = max(0, match_start - 4000)
    window = cleaned[window_start:match_start]

    resource_matches = list(re.finditer(r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{', window))
    if resource_matches:
        m = resource_matches[-1]
        resource_label = "%s.%s" % (m.group(1), m.group(2))
    else:
        resource_matches2 = list(re.finditer(r'\bresource\s+"([^"]+)"\s+"([^"]+)"', window))
        resource_label = "%s.%s" % resource_matches2[-1].groups() if resource_matches2 else "<unknown resource>"

    kind_matches = list(re.finditer(r"\b(assume_role_policy|policy)\s*=\s*jsonencode\s*\(", window))
    if kind_matches:
        kind_kw = kind_matches[-1].group(1)
        kind_label = "assume_role_policy / trust" if kind_kw == "assume_role_policy" else "policy"
    else:
        kind_label = "<unlabelled policy document>"

    return "%s (%s)" % (resource_label, kind_label)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--policy", required=True, help="path to a Terraform file containing IAM policy documents")
    args = ap.parse_args()

    try:
        with open(args.policy, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as exc:
        print("ERROR: could not read --policy %r: %s" % (args.policy, exc), file=sys.stderr)
        return 2

    cleaned = strip_comments(raw)

    print("=" * 100)
    print("CONDITION AXIS READER -- IAM-s-4 (NFRA_IAMROLES202609)")
    print("policy file: %s" % args.policy)
    print("-" * 100)
    print("BOUND (C-DESIRED-UNTIL-EXERCISED): every finding below is DESIRED -- read from")
    print("policy TEXT, not an APPLIED state and not an EXERCISED one. Only a real")
    print("`aws iam simulate-principal-policy` battery (cell IAM-s-8) moves a claim past DESIRED.")
    print("=" * 100)

    n_requires_nothing = 0
    n_requires = 0
    n_unknown = 0
    n_statements = 0
    n_documents = 0
    n_skipped_arrays = 0

    for m in re.finditer(r"\bStatement\s*=\s*(\[)", cleaned):
        open_idx = m.start(1)
        close_idx = find_matching_close(cleaned, open_idx)
        if close_idx == -1:
            print("\n[PARSE-ERROR] Statement array starting at offset %d in %s is unbalanced "
                  "and was skipped -- not counted toward the denominator." % (open_idx, args.policy))
            continue

        objects = list(iter_top_level_objects(cleaned, open_idx + 1, close_idx))

        # Sanity gate: a real IAM Statement array's members all carry "Effect". If none do,
        # this match is very likely a false positive (e.g. the literal text "Statement ="
        # inside an unrelated value) rather than an IAM statement list -- skip it rather than
        # report fabricated findings against something that is not a policy statement.
        looks_like_iam = False
        for (os_, oe_) in objects:
            if re.search(r"\bEffect\s*=", cleaned[os_:oe_ + 1]):
                looks_like_iam = True
                break
        if objects and not looks_like_iam:
            n_skipped_arrays += 1
            print("\n[SKIPPED] array at offset %d does not look like an IAM Statement list "
                  "(no member carries 'Effect') -- not counted toward the denominator." % open_idx)
            continue

        n_documents += 1
        label = find_label(cleaned, m.start())
        total_here = len(objects)
        for idx, (os_, oe_) in enumerate(objects, start=1):
            obj_text = cleaned[os_:oe_ + 1]
            n_statements += 1
            result = analyze_statement(obj_text)
            sid = result.get("sid") or "<unnamed>"
            effect = result.get("effect", "<unspecified>")
            print("\n[%s] statement %d/%d -- Sid=%s Effect=%s" % (label, idx, total_here, sid, effect))
            status = result["status"]
            if status == "REQUIRES-NOTHING":
                n_requires_nothing += 1
                print("    REQUIRES-NOTHING")
            elif status == "UNKNOWN":
                n_unknown += 1
                print("    UNKNOWN (DESIRED-axis unresolved): %s" % result.get("detail", ""))
            else:
                n_requires += 1
                print("    REQUIRES (DESIRED, read from policy text -- NOT yet EXERCISED):")
                for op_name, ck, cv in result["requirements"]:
                    if ck is None:
                        print("      - %s = %s   [UNPARSED value shape]" % (op_name, cv))
                        continue
                    hint = hint_for(ck)
                    hint_txt = "   [%s]" % hint if hint else ""
                    print("      - %s  %s = %s%s" % (op_name, ck, cv, hint_txt))
                if not result.get("clean", True):
                    print("      NOTE: this Condition block only partially parsed -- some "
                          "operator/value shape was not recognised; treat as UNKNOWN for "
                          "whatever this reader could not extract, not as a clean REQUIRES.")

    print("\n" + "=" * 100)
    print("DENOMINATOR: %d statement(s) examined across %d policy document(s) (Statement "
          "arrays) read from %s" % (n_statements, n_documents, args.policy))
    if n_skipped_arrays:
        print("  (%d array(s) matched the text 'Statement =' but did not look like an IAM "
              "statement list and were excluded from the denominator above)" % n_skipped_arrays)
    print("  REQUIRES-NOTHING : %d" % n_requires_nothing)
    print("  REQUIRES         : %d" % n_requires)
    print("  UNKNOWN          : %d" % n_unknown)
    print("=" * 100)
    print("POPULATION BOUND: this run covers ONLY the file named above. It is not, and does")
    print("not claim to be, a statement about any other policy or about the estate as a whole.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
