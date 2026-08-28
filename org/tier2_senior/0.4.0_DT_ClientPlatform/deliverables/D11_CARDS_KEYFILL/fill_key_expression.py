#!/usr/bin/env python
"""KEYFILL-DTX -- fill `trust.key.key_expression` for the 18 cards carded by 0.4.0_DT_ClientPlatform~X.

THE RULE THIS FILL OBEYS (SUBSTRATE_CARD.v3, trust.key.key_expression): the expression is stated so a
consumer can COMPUTE the key, "not merely name its space". NULL is STRUCTURAL PAYLOAD ABSENCE, legal
only when basis_by_field.key_expression == 'absent' -- and then the row cannot read 'measured'. A
card whose key row is measured with a null expression is the contradiction v3 exists to make
unrepresentable, and AC3 requires that fixture be refused.

BASIS, per the certifier's arm 2 and this TO's AC2:
    measured   ONLY when the expression was EXERCISED on a real member in THIS fill
    held       the expression is stated but was not exercised here (subject unreachable)
    inferred   PROHIBITED in this fill -- it is what every row carries now, and it is the thing
               the fill exists to replace with something a consumer can check
    absent     no expression can be stated; null payload, reason recorded

⛔ THE EXPRESSIONS ARE AUTHORED AGAINST EACH CARD'S DECLARED identity_space, NOT AGAINST WHATEVER
COLLECTION IS BIGGEST. My first reachability probe picked `$.edges[*]` for the motif cards because
edges outnumber nodes 36 to 7 -- while their declared space is "motif node_id strings", which lives
on `$.nodes[*]`. A plausible answer about the wrong population is the failure mode this whole
carding round is about, so the member collection is chosen from the SPACE and the triple is printed
for a reader to check.
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
CARDS = os.path.join(ROOT, "org", "tier2_senior", "0.4.0_DT_ClientPlatform", "deliverables")


def jload(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# -- space predicates: what a key in this space must LOOK like -------------------------------------
def p_repo_path(k):
    return isinstance(k, str) and not k.startswith("/") and "\\" not in k and len(k) > 1


def p_exists(k):
    return p_repo_path(k) and os.path.exists(os.path.join(ROOT, k))


def p_typed_id(k):
    return bool(re.match(r"^[a-z_]+:[^\s]+$", k or ""))


def p_symbol(k):
    return bool(re.match(r"^[a-z]+:[A-Za-z0-9_.\-]+(:[A-Za-z0-9_.\-]+)?$", k or ""))


def p_prefixed_path(k):
    """The observed key form for the risk-edge store: `file:` + a repo-relative path. Named
    separately because p_repo_path accepted it while the card's space said 'repo-relative file
    paths' -- the predicate was weak enough to hide a prefix a consumer must not strip."""
    return isinstance(k, str) and k.startswith("file:") and p_repo_path(k[5:])


def p_nonempty(k):
    return isinstance(k, str) and bool(k.strip())


def p_arn(k):
    return bool(re.match(r"^arn:aws:[a-z0-9\-]+:", k or ""))


# -- the fill table: one row per card, expression authored against ITS declared space --------------
# (card prefix, expression, exerciser, space predicate, predicate name)
def ex_json_nodes(subject):
    d = jload(os.path.join(ROOT, subject))
    return d["nodes"][0]["node_id"], "$.nodes[0].node_id"


def ex_graph_nodes(subject):
    d = jload(os.path.join(ROOT, subject))
    k = next(iter(d["nodes"]))
    return k, "first key of $.nodes (the mapping IS keyed by the symbol id)"


def ex_firms(subject):
    d = jload(os.path.join(ROOT, subject))
    return d["firms"][0]["firm_id"], "$.firms[0].firm_id"


def ex_edges_field(field):
    def go(subject):
        d = jload(os.path.join(ROOT, subject))
        return d["edges"][0][field], "$.edges[0].%s" % field
    return go


def ex_dir(subject):
    names = sorted(n for n in os.listdir(os.path.join(ROOT, subject)) if not n.startswith("__"))
    return subject.rstrip("/") + "/" + names[0], "first non-dunder entry of the directory"


def ex_tool(_subject):
    return ".tools/comp-heat", "the shim's repo-root-relative path"


def ex_yaml_entries(subject):
    txt = open(os.path.join(ROOT, subject), encoding="utf-8").read()
    m = re.search(r'^\s*-\s*resource_id:\s*"([^"]+)"', txt, re.M)
    return m.group(1), "first $.entries[*].resource_id"


def ex_yaml_terms(subject):
    txt = open(os.path.join(ROOT, subject), encoding="utf-8").read()
    m = re.search(r"^terms:\s*$", txt, re.M)
    tail = txt[m.end():]
    t = re.search(r"^  ([A-Za-z][A-Za-z0-9_ \-]*):\s*$", tail, re.M)
    return t.group(1), "first key under $.terms"


def ex_source(pattern, note):
    """A source read that finds nothing RAISES. It used to return the string '(pattern not found)',
    which is non-empty and therefore PASSED the p_nonempty predicate -- a failed retrieval returning
    a value that satisfies the check. That is the wrong-ACCEPT class this whole carding round exists
    to remove, and it was in my own fill until the triple was printed."""
    def go(subject):
        txt = open(os.path.join(ROOT, subject), encoding="utf-8", errors="replace").read()
        m = re.search(pattern, txt)
        if not m:
            raise LookupError("pattern %r not found in %s" % (pattern, subject))
        return m.group(0)[:80], note
    return go


FILL = {
 "W2-bcin": ("a member is an element of $.nodes[*]; key = .node_id",
             ex_json_nodes, p_nonempty, "non-empty motif node_id string"),
 "W2-qvzv": ("a member is an element of $.nodes[*]; key = .node_id",
             ex_json_nodes, p_nonempty, "non-empty motif node_id string"),
 "W2-xzjx": ("a member is an element of $.nodes[*]; key = .node_id",
             ex_json_nodes, p_nonempty, "non-empty C3System / graph node id"),
 "W2-jgzc": ("a member is an element of $.firms[*]; key = .firm_id (the second, partial space is "
             ".tree_token on the same member)", ex_firms, p_nonempty, "non-empty firm_id string"),
 "W2-lqzx": ("a member is an entry of the $.nodes MAPPING; key = the mapping key, which equals "
             "the member's .id (form gold:MODULE.function[:inner])",
             ex_graph_nodes, p_symbol, "^[a-z]+:[A-Za-z0-9_.-]+(:[A-Za-z0-9_.-]+)?$"),
 "W2-nthk": ("a member is a file under the harness directory; key = its repo-relative path",
             ex_dir, p_exists, "repo-relative path that resolves on disk"),
 "W2-pcac": ("a member is an element of $.entries[*]; key = .resource_id, of the form <type>:<name>",
             ex_yaml_entries, p_typed_id, "^[a-z_]+:[^ ]+$"),
 "W2-rpcx": ("for the freshness surface a member's key is its repo-root-relative path "
             "(.tools/<tool>); the score surface's key is an unresolved free string and is NOT "
             "expressed here", ex_tool, p_exists, "repo-relative path that resolves on disk"),
 "W2-ukdh": ("a member is an element of $.edges[*]; the key of each endpoint is .src / .dst, a "
             "repo-relative file path", ex_edges_field("src"), p_repo_path, "repo-relative path"),
 "W2-uvcz": ("a member is an element of $.edges[*]; key = .node, which is NOT a bare path: it "
             "carries a `file:` prefix (observed 'file:.tools/deploy_ledger.py'). The declared "
             "space says 'repo-relative file paths'; the KEY is that path with a namespace prefix, "
             "and a consumer that strips it will mis-key",
             ex_edges_field("node"), p_prefixed_path, "^file:<repo-relative path>"),
 "W2-znom": ("a member is an entry of the $.terms MAPPING; key = the term name (the mapping key)",
             ex_yaml_terms, p_nonempty, "non-empty term name"),
}

# Subjects that cannot be exercised in this fill, with the reason. Expression still STATED where the
# card's own evidence supports one -> held. Where no expression can be stated -> null + absent.
HELD = {
 "W3-gkih": ("a member is a CloudNode the loader writes; key = the AWS ARN string, used verbatim as "
             "the CloudNode PRIMARY KEY (kuzu_load.py assigns it from the node's `arn` field)",
             "the loader was NOT RUN in this fill and its output table was not opened, so no real "
             "member was keyed here. Reading the assignment at source STATES the expression; it "
             "does not exercise it, and calling a source citation 'measured' is exactly the "
             "overstatement this fill's basis rule exists to prevent"),
 "W3-mdiu": ("a member is a node the stitch loader writes; key = node_id, the arn when present and "
             "otherwise the node's own id (path/name for portal nodes) -- ONE column carrying TWO "
             "id spaces with no type discriminator",
             "the stitch loader was NOT RUN and its output was not opened; same boundary as its "
             "sibling -- a source citation is not an exercise"),
 "W2-hffm": ("a member is an element of $.nodes[*]; key = .node_id, canonical at the in-file "
             "nodes_snapshot_id 8601547680771488785",
             "subject ABSENT on this device and not at that path at HEAD: the card recorded it as "
             "UNTRACKED-and-not-gitignored at 10,329,963 bytes, and an untracked file that "
             "disappears leaves no git evidence it was ever there"),
 "W2-coth": ("a member is a CloudNode row; key = .node_id -- the ARN where one exists, otherwise a "
             "layer-specific string",
             "the LOCAL kuzu projection was not opened in this fill (no driver invoked; opening it "
             "is a different act from filling a key expression)"),
 "W2-vlov": ("a member is a row of the Iceberg table; key = the node_id column as surfaced in the "
             "projection",
             "S3/Iceberg table not opened in this fill; the card itself records that the table's "
             "own schema was never read, so the column is named from the projection, not from the "
             "table"),
 "W2-xnwo": ("a member is a row of the Iceberg table; key = the node_id column as surfaced in the "
             "projection",
             "S3/Iceberg table not opened in this fill; same unread-schema caveat as its edges "
             "sibling"),
}
ABSENT = {
 "W2-yjky": "the object was never opened -- the card's identity_space is literally UNOBSERVED, so "
            "no expression can be stated without inventing one. NULL payload with basis absent is "
            "the honest row, and it is what v3 legalises for exactly this case.",
}


def _append(existing, note):
    """Append a keyfill note to the row's existing evidence, never replacing what was there."""
    existing = (existing or "").rstrip()
    return (existing + "  || " + note) if existing else note


def main():
    cards = []
    for f in sorted(glob.glob(os.path.join(CARDS, "D11_CARDS_*", "*.json"))):
        d = jload(f)
        if d.get("carded_by") == "0.4.0_DT_ClientPlatform~X":
            cards.append((f, d))
    print("KEYFILL-DTX -- key_expression fill")
    print("   cards RE-DERIVED at run time: %d (face says 18)" % len(cards))
    print()

    filled = held = absent = refused = 0
    triples = []
    apply = "--apply" in sys.argv
    for f, d in cards:
        pre = os.path.basename(f).split("__")[0]
        key = d.setdefault("trust", {}).setdefault("key", {})
        bbf = key.setdefault("basis_by_field", {})
        subject = (d.get("subject") or {}).get("id", "")
        try:
            if pre in FILL:
                expr, exerciser, pred, predname = FILL[pre]
                k, how = exerciser(subject)
                ok = pred(k)
                if not ok:
                    refused += 1
                    print("REFUSED  %-9s key %r fails the space predicate (%s)" % (pre, k, predname))
                    continue
                key["key_expression"] = expr
                bbf["key_expression"] = "measured"
                filled += 1
                triples.append((pre, subject, how, k, predname))
            elif pre in HELD:
                expr, why = HELD[pre]
                key["key_expression"] = expr
                bbf["key_expression"] = "held"
                # THE REASON GOES IN `evidence`, THE SLOT THE CONTRACT ACTUALLY HAS. My first
                # apply invented `key_expression_unexercised_reason`, and v3's trust.key is
                # additionalProperties:false -- 7 of 18 cards went INVALID. A value needs a whole
                # PATH, not a slot I wish existed; the validator is what caught it.
                key["evidence"] = _append(key.get("evidence"),
                                          "KEY_EXPRESSION NOT EXERCISED IN THE KEYFILL: " + why)
                held += 1
            elif pre in ABSENT:
                key["key_expression"] = None
                bbf["key_expression"] = "absent"
                key["evidence"] = _append(key.get("evidence"),
                                          "KEY_EXPRESSION ABSENT: " + ABSENT[pre])
                absent += 1
            else:
                refused += 1
                print("REFUSED  %-9s no fill rule -- NOT silently skipped" % pre)
                continue
        except Exception as exc:                                          # noqa: BLE001
            refused += 1
            print("REFUSED  %-9s exerciser raised %s: %s" % (pre, type(exc).__name__, str(exc)[:70]))
            continue
        if apply:
            with open(f, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(d, fh, indent=2, ensure_ascii=False)
                fh.write("\n")

    print("=== CERTIFICATION ARM 1: member -> key -> identity_space, validated ===")
    for pre, subj, how, k, predname in triples:
        print("  %-9s %s" % (pre, subj[:64]))
        print("            member: %s" % how)
        print("            key   : %r" % (k[:70] if isinstance(k, str) else k))
        print("            space : VALID against %s" % predname)
    print()
    print("=== CENSUS, every count derived by this run ===")
    print("  filled (measured, exercised here) : %d" % filled)
    print("  held   (stated, not exercised)    : %d" % held)
    print("  absent (null payload + reason)    : %d" % absent)
    print("  refused                           : %d" % refused)
    print("  RECONCILIATION %d + %d + %d + %d = %d of %d"
          % (filled, held, absent, refused, filled + held + absent + refused, len(cards)))
    print()
    print("  inferred used anywhere in this fill: 0 (prohibited by AC2)")
    print("  mode: %s" % ("APPLIED to the cards" if apply else "DRY RUN (pass --apply to write)"))
    # A FILL THAT FOUND NOTHING MUST FAIL. The first run of this script exited 0 having located
    # ZERO cards, because "0 + 0 + 0 + 0 == 0" is vacuously true -- the reconciliation I wrote to
    # prove completeness is satisfied most easily by an empty population. The denominator has to be
    # asserted against the re-derived expectation, not merely balanced against itself.
    if not cards:
        print("  FAIL: zero cards located -- the reconciliation above is vacuous, not a pass")
        return 1
    if len(cards) != 18:
        print("  NAMED DIFFERENCE: re-derived %d cards, the face declares 18 -- not absorbed"
              % len(cards))
    return 0 if (filled + held + absent + refused) == len(cards) and refused == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
