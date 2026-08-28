#!/usr/bin/env python
"""WP-3b -- THE DECLARATION PASS. Writes `part.identity` from the RULED mapping, or refuses and says why.

Ruled by 2.0.0_SA_COO~X @7abc9544a2 (option (b)) after the translator errored 42 of 42 parts on the
same five ISCK identity fields; the VALUES were then ruled as DATA by the design lane
(L0_PART_IDENTITY_MAPPING.json @f553dd2b00) so that no emitter decides identity on its own authority,
and the SLOT by the L0 `identity` receiver @8607debb64 so that membership is enforced by a schema
rather than merely checked by this file.

THIS PASS DECIDES NOTHING. It applies a ruled table and cites it. Every value carries basis 'held'
with the mapping's path @commit as evidence and the mapping blob as `mapping_digest`. The one thing
it will not do is proceed when its input cannot support the ruling.

NOTE: THE PRECONDITION IS A CONTROL, NOT A COMMENT. The ruled mapping keys `plane` and
`identity_policy` BY `home_space`. Measured at the TO's pinned population @2feca185e7: 0 of 42 parts
carry that field; in the working tree, 42 of 42 do (repo_path 25 | s3_uri 14 | none 3). A mapping
keyed on a field the population lacks is unapplicable, and the failure mode is quiet -- my own
pre-ruling pass inferred the plane from the SHAPE of `home` and produced 25 / 14 / 3, matching the
ruled census exactly, which is precisely what would have let this run against the pin, agree with
every expected number, and never notice the key was absent. So `require_home_space()` refuses first
and names the count. Agreement on values is not applicability.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
MAPPING_PATH = "org/standards/isck/ledger/translation/L0_PART_IDENTITY_MAPPING.json"
MAPPING_COMMIT = "b3aeaf7b4f"   # v0.1 -- carries the applicability clause
L1_COMMIT = "16cd74c870"
MANIFEST_PATH = ("org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/"
                 "graph_object_manifest.json")
# THE POPULATION (issuer ruling 152829Z): the committed immutable PRESERVATION COPY -- the
# generator's last RATIFIED output at the vintage the L0 ratification pinned (d86a59514ec3). The
# generator is neither invoked nor bypassed: it REFUSES because the candidate set has moved since
# ratification, and that refusal is the vintage caveat this slice carries rather than works around.
PRESERVED_PATH = ("org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/preserved/"
                  "graph_object_manifest.PRESERVED_47f583e6.json")
DECLARED_PATH = ("org/tier2_senior/0.4.0_DT_ClientPlatform/deliverables/D11_MANIFEST/"
                 "graph_object_manifest.declared.json")
RATIFIED_VINTAGE = "d86a59514ec3"
MOVED_CANDIDATE_SET = "87528e2a6d89"
SCHEMA_PATH = "org/standards/L0_GRAPH_SUBSTRATE_MANIFEST.schema.json"


def _blob(commit, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (commit, path)], cwd=ROOT)


def load_mapping(commit=MAPPING_COMMIT):
    raw = _blob(commit, MAPPING_PATH)
    return json.loads(raw), hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


def require_home_space(parts):
    """THE PRECONDITION. The ruled mapping keys on home_space; refuse if the population lacks it."""
    have = [p for p in parts if p.get("home_space") is not None]
    if len(have) != len(parts):
        raise SystemExit(
            "REFUSING: the ruled mapping keys `plane` and `identity_policy` by `home_space`, and "
            "only %d of %d parts carry it. A mapping keyed on an absent field is unapplicable, and "
            "inferring the key from `home` instead would agree with the ruled census (25/14/3) "
            "while silently substituting a parse for a declared field -- the substitution this "
            "ruling exists to refuse. Re-pin the population to a commit whose parts carry "
            "home_space, or have the design lane re-key the mapping." % (len(have), len(parts)))
    return True


def declare(part, mapping, mapping_digest, emitter_seat):
    """`part.identity` in the receiver's shape, values from the ruled table only."""
    rules = mapping["rules"]
    space = part["home_space"]
    plane = rules["plane"]["table"].get(space)
    policy = rules["identity_policy"]["table"].get(space)
    if plane is None or policy is None:
        return {"claim_status": "unknown", "entity_class": None, "plane": None,
                "entity_grain": None, "identity_scope": None, "identity_policy": None,
                "basis": None, "evidence": "home_space %r is not in the ruled table" % space,
                "owner": None, "mapping_digest": None}
    return {
        "claim_status": "declared",
        "entity_class": rules["entity_class"]["value"],
        "plane": plane,
        "entity_grain": rules["entity_grain"]["value"],
        "identity_scope": rules["identity_scope"]["value"],
        "identity_policy": policy,
        "basis": "held",
        "evidence": ("%s @%s (ruled mapping v%s); plane cited to L1 @%s"
                     % (MAPPING_PATH, MAPPING_COMMIT, mapping["mapping_version"], L1_COMMIT)),
        "owner": "1.0.0_SA_CTO~X (mapping) / %s (pass)" % emitter_seat,
        "mapping_digest": mapping_digest,
    }


def run(manifest, mapping, mapping_digest, emitter_seat="0.4.0_DT_ClientPlatform~X", out_path=None):
    parts = manifest["parts"]
    require_home_space(parts)
    out_parts, by_plane, by_policy, declared, unknown = [], {}, {}, 0, 0
    for part in parts:
        ident = declare(part, mapping, mapping_digest, emitter_seat)
        p = dict(part)
        p["identity"] = ident
        out_parts.append(p)
        if ident["claim_status"] == "declared":
            declared += 1
            by_plane[ident["plane"]] = by_plane.get(ident["plane"], 0) + 1
            by_policy[ident["identity_policy"]] = by_policy.get(ident["identity_policy"], 0) + 1
        else:
            unknown += 1
    out = dict(manifest)
    out["parts"] = out_parts
    print("DECLARATION PASS -- every number COUNTED from the parts processed")
    print("   parts       %d" % len(parts))
    print("   declared    %d   unknown %d" % (declared, unknown))
    print("   by plane    %s" % json.dumps(by_plane, sort_keys=True))
    print("   by policy   %s" % json.dumps(by_policy, sort_keys=True))
    print("   mapping     %s @%s blob %s" % (MAPPING_PATH, MAPPING_COMMIT, mapping_digest[:12]))
    if out_path:
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print("   re-emitted  %s" % out_path)
    return out, {"parts": len(parts), "declared": declared, "unknown": unknown,
                 "by_plane": by_plane, "by_policy": by_policy}


def validate(manifest_doc, schema_commit="8607debb64"):
    """The SLOT's own gate: the re-emitted manifest must validate against the receiver's schema."""
    import jsonschema
    schema = json.loads(_blob(schema_commit, SCHEMA_PATH))
    jsonschema.validate(manifest_doc, schema)
    return True


def main():
    pop_commit = sys.argv[1] if len(sys.argv) > 1 else "2feca185e7"
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    if pop_commit == "--preserved":
        pin = subprocess.check_output(["git", "log", "-1", "--format=%h", "--", PRESERVED_PATH],
                                      cwd=ROOT).decode().strip()
        with open(os.path.join(ROOT, PRESERVED_PATH), "rb") as fh:
            raw = fh.read()
        manifest = json.loads(raw)
        print("   POPULATION  the committed immutable preservation copy")
        print("     path      %s" % PRESERVED_PATH)
        print("     pin       %s   sha256 %s" % (pin, hashlib.sha256(raw).hexdigest()))
        print("     vintage   the generator's last RATIFIED output at %s" % RATIFIED_VINTAGE)
        print("     CAVEAT    the candidate set has since MOVED to %s; l0_compile_w3.py refuses to "
              "re-emit until the ratification is re-read (4.0.0_SA_CRO~X). This slice admits the "
              "RATIFIED set at its ratified vintage; the moved set is the NEXT vintage's "
              "population." % MOVED_CANDIDATE_SET)
    elif pop_commit == "--worktree":
        with open(os.path.join(ROOT, MANIFEST_PATH), "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
        print("   population  WORKING TREE (uncommitted) -- NOT the TO's pinned population")
    else:
        manifest = json.loads(_blob(pop_commit, MANIFEST_PATH))
        print("   population  %s @%s (object database)" % (MANIFEST_PATH, pop_commit))
    mapping, digest = load_mapping()
    doc, _counts = run(manifest, mapping, digest, out_path=out_path)
    try:
        validate(doc)
        print("   SCHEMA      re-emitted manifest VALIDATES against the identity receiver "
              "@8607debb64")
    except Exception as exc:                                            # noqa: BLE001
        print("   SCHEMA      REFUSED by the receiver: %s" % str(exc).splitlines()[0][:120])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
