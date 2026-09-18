"""LGIC_ENFORCE round 8, cell EN-p-36 -- the instrument that produced RAISE_POPULATION_R8.json.

POPULATES the existing `lib/opal_naming.py census --not-judged` mechanism (R-29 AMENDMENT 1); builds
nothing new. Three steps, each printing its own denominator:

  enumerate   re-measure the live and repo planes exactly as `census()` builds its item lists, then
              call grade() on every item WITHOUT stopping at the first RAISE (unlike census_judge(),
              which stops by design) -- this is the only way to learn the WHOLE raise population before
              a --not-judged file can be built for it.
  classify    disposition every RAISE as CARDED, citing the ALREADY-MEASURED per-token owner research
              this same worker slot filed in round 4 (OWNER_CARDS_R4.md, Cards 1-19, registry@R4_BASE
              af8d694cced2b38e52f5735a35bd4ea0f7655eda). That file's own governing finding: "Zero mints
              follow from that, not from a shortfall of effort." Corroborated here, not re-derived: this
              round's smaller population (grown-since-round-4 registry rows: gateway, globgrph, harvest,
              bloomberg, msci) is checked to be a SUBSET of round-4's already-researched root causes, and
              a script-level SystemExit fires on any RAISE that is NOT a member of that set -- so a token
              this build has never seen cannot be silently carded with a borrowed reason.
  build       write RAISE_POPULATION_R8.json in the shape check_en_r8.py's four arms read.

Position-independent by walking up from this file to find the repo root (the marker is lib/opal_naming.py),
never a hardcoded worktree path, so a grader can run this from a DIFFERENT checkout.
"""
import argparse
import io
import json
import os
import sys


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(12):
        if os.path.isfile(os.path.join(cur, "lib", "opal_naming.py")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    raise SystemExit("could not find repo root (lib/opal_naming.py) walking up from %s" % here)


REPO = _repo_root()
sys.path.insert(0, os.path.join(REPO, "lib"))
import opal_naming as N  # noqa: E402

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
RAISES_PATH = os.path.join(OUT_DIR, "_r8_raises.json")
CARDS_PATH = os.path.join(OUT_DIR, "_r8_cards.json")
RECORD_PATH = os.path.join(OUT_DIR, "RAISE_POPULATION_R8.json")
CARDS_DOC = "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/OWNER_CARDS_R4.md"


def enumerate_raises():
    """Every item BOTH planes carry, judged with grade() WITHOUT stopping at the first RAISE. Returns
    (live_items_to_judge, repo_items, live_raises, repo_raises, live_meta, repo_meta)."""
    v = N._vocab()
    schema = N._schema()
    nodes, vintage, shown = N.census_live(600)
    live_items, live_ng, live_fixed = [], 0, 0
    for nd in nodes:
        if nd["type"] in v.not_graded:
            live_ng += 1
            continue
        why = N._aws_fixed(nd["type"], nd["name"], nd["arn"], schema)
        if why:
            live_fixed += 1
            continue
        live_items.append({"plane": "live", "type": nd["type"], "current": nd["name"]})
    repo_items, stats = N.census_repo()

    def judge_all(items):
        resolved, raises = [], []
        for it in items:
            try:
                verdict, canon = N.grade(it["current"], it["type"])
            except N.RaiseDefect as exc:
                raises.append({"name": it["current"], "plane": it["plane"], "type": it["type"],
                                "where": it.get("where"), "message": str(exc)})
                continue
            resolved.append(it)
        return resolved, raises

    _, live_raises = judge_all(live_items)
    _, repo_raises = judge_all(repo_items)
    live_meta = {"nodes": len(nodes), "not_graded": live_ng, "aws_fixed": live_fixed,
                 "to_judge": len(live_items), "vintage": vintage, "shown": shown}
    repo_meta = {"names": len(repo_items), "tf_files": stats["tf_files"],
                 "source_files": stats["source_files"]}
    return live_raises, repo_raises, live_meta, repo_meta


# (predicate over the RaiseDefect message / name) -> (Card N in OWNER_CARDS_R4.md, title, the "what was
# measured" basis, re-stated here rather than re-derived).
def classify(msg, name):
    if "'news'" in msg:
        return (2, "news (unresolved, no directive owner)",
                "systems.json unresolved row 'news' (still current): no DIRECTIVES.yaml line or "
                "mission-tree D<n> project owns it; owner_directive cannot be written")
    if "'trade'" in msg:
        return (3, "trade (unresolved, no directive owner)",
                "systems.json unresolved row 'trade': TRSB_* projects are LEGACY FLAT with seat owners, "
                "not a directive; owner_directive cannot be written")
    if "'astn'" in msg:
        return (4, "astn (unresolved, no directive owner)",
                "systems.json unresolved row 'astn': ASTN_WSJFT is closed/unregistered, seat-owned not "
                "directive-owned; owner_directive cannot be written")
    if name.startswith("opal-data-security"):
        return (6, "opal-data-security[-access-logs] (TOKEN_COLLISION, R-39/LGIC_ENFORCE-W1-S30)",
                "genuine owner D12/NFRA_OPSEC202609 (DIRECTIVES.yaml :485) EXISTS, but grade()'s "
                "vocabulary keys purely on the token 'security', which Card 5's unrelated, unowned "
                "NFRA_TERRAFORM security-sweep family would ALSO resolve on -- one token cannot carry "
                "two owners; minting misattributes one group to the other")
    if "'security'" in msg:
        return (5, "security-sweep tooling (NFRA_TERRAFORM, closed+unregistered; TOKEN_COLLISION)",
                "org/projects/NFRA_TERRAFORM.json status closed, 0 DIRECTIVES.yaml hits; AND the same "
                "token 'security' is Card 6's D12-owned opal-data-security group's token -- one token, "
                "two owners, minting here misattributes Card 6's D12 ownership to this closed project")
    if "'vpc'" in msg or (msg.startswith("L2") and "vpc" in msg):
        return (7, "vpc (no declared source)",
                "repo search for vpc-flow-logs-role/VPCFlowLogsPolicy/aws_flow_log/flow_log: 0 hits; "
                "LIVE-no-DECLARED, no Terraform/lambda-map/EC2-manifest source to cite an owner from")
    if "'portal'" in msg or "'cache'" in msg:
        return (8, "portal and cache (portal-auth/data-refresh, no directive names the edge layer)",
                "DIRECTIVES.yaml has 0 hits for PORTAL as its own directive/system; PORTAL only appears "
                "as a subgroup label under OTHER directives' products; portal-auth/data-refresh modules "
                "themselves are unclaimed by any D<n> project")
    if "'sentiment'" in msg:
        return (9, "sentiment (no declared source, LIVE-no-DECLARED)",
                "repo search for sentiment_query_api/sentiment-query-api: hits only in live-AWS "
                "OBSERVATION instruments, never a Terraform resource/lambda-source-map/EC2-manifest "
                "entry; nothing to cite an owner from")
    if "'f49'" in msg:
        return (10, "F49ServedAndSourceRead (naming-order defect, unreachable via resources.json)",
                "infra/aws/terraform/49f-value-parity/49f_value_parity.tf names ADVI_BREAKS/advi (D2) "
                "as the TRUE owner, but the live name spells the scope token 'f49' instead of the "
                "registered short form '49f' -- a token-ORDER defect in the resource's own name, not a "
                "missing registry row")
    if "'dowjones'" in msg:
        return (11, "dowjones (no declared source)",
                "round-4 repo search across infra/ and tools/: 0 hits. This round's wider search (full "
                "corpus) finds the secret's true home is org/tier1_exec/4.0.0_SA_CRO/scripts/"
                "dowjones_harvest_session.py, an Andrew-direct CRO harvest session -- a SEAT's ad hoc "
                "tooling, not a mission-tree D<n> pipeline; no directive is citable even with the wider "
                "search")
    if name == "opal-data-imo":
        return (12, "opal-data-imo (retired token)",
                "systems.json refused_keys.retired already carries 'imo', citing Andrew's card 9 RETIRE "
                "ruling; RETIRE is the opposite of a scope grant -- correct disposition is live-bucket "
                "retirement, not a registry mint")
    if name in ("opal-data-pm", "opal-data-portfolio", "opal-data-research"):
        return (13, "opal-data-pm/portfolio/research (scope-key vocabulary, not this cell's to fix)",
                "'portfolio' is ALREADY in refused_keys.generic_noun (B2 does not consult refused_keys); "
                "'research' is harvest/AMGT_RESAPP's (D5) pre-rename Stage-1 name, resolved by an "
                "already-approved Stage-2 rename, not a second mint; 'pm' has no citable source")
    if msg.startswith("R8"):
        return (14, "the five #policy R8 rows (structural, ungradable from name)",
                "none of the 5 bucket names fits opal-data-{scope} or opal-{account}-{purpose}, and R8's "
                "kind-lookup path is only reached AFTER exactly one type already matches -- none does; a "
                "naming-grammar dead end, needs a live rename, not a registry mint")
    if msg.startswith("L2"):
        return (15, "L2 log-group service tokens (hardcoded _LOG_SERVICE dict, code not registry)",
                "the log group's service segment is looked up in _LOG_SERVICE, hardcoded in "
                "lib/opal_naming.py -- outside infra/logic/registry/, this cell's whole grant")
    if msg.startswith("K1") or msg.startswith("K3") or msg.startswith("K4a"):
        return (1, "S3Key path-grammar (K1/K3/K4a) is out of mint reach",
                "segment 1 (or the tier/partition segment) is an S3-KEY-PATH CONVENTION WORD, not an AWS "
                "resource with a Terraform/lambda-source-map/EC2-manifest declaration -- no resource for "
                "the mint rule's evidence sources to attribute an owner to; same structural class as "
                "Card 1's round-4 population, extended to every K1/K3/K4a triple this round measures")
    raise SystemExit("UNCLASSIFIED RAISE -- new root cause, not a member of round-4's card set: %r %r"
                      % (msg, name))


def build_cards(raises):
    out = []
    for r in raises:
        no, title, basis = classify(r["message"], r["name"])
        card = ("%s (this cell's own re-measurement, registry@HEAD). Round-4 finding reused, "
                "corroborated not re-derived (%s, Card %d -- %s): %s. Zero registry mints follow from "
                "this, matching OWNER_CARDS_R4.md's own governing finding for the whole population."
                % (r["message"], CARDS_DOC, no, title, basis))
        out.append({"name": r["name"], "plane": r["plane"], "card": card, "type": r.get("type"),
                    "where": r.get("where"), "card_ref": "Card %d" % no})
    return out


def cmd_enumerate():
    live_raises, repo_raises, live_meta, repo_meta = enumerate_raises()
    print("LIVE to_judge=%d raises=%d" % (live_meta["to_judge"], len(live_raises)))
    print("REPO names=%d raises=%d" % (repo_meta["names"], len(repo_raises)))
    with io.open(RAISES_PATH, "w", encoding="utf-8") as fh:
        json.dump({"live_raises": live_raises, "repo_raises": repo_raises,
                    "live_meta": live_meta, "repo_meta": repo_meta}, fh, indent=1)
    print("WROTE %s" % RAISES_PATH)
    return 0


def cmd_classify():
    with io.open(RAISES_PATH, encoding="utf-8") as fh:
        doc = json.load(fh)
    live_cards = build_cards(doc["live_raises"])
    repo_cards = build_cards(doc["repo_raises"])
    print("live cards %d ; repo cards %d" % (len(live_cards), len(repo_cards)))
    with io.open(CARDS_PATH, "w", encoding="utf-8") as fh:
        json.dump({"live_cards": live_cards, "repo_cards": repo_cards,
                    "live_meta": doc["live_meta"], "repo_meta": doc["repo_meta"]}, fh, indent=1)
    print("WROTE %s" % CARDS_PATH)
    return 0


def cmd_build(judged_live, judged_repo):
    """The final RAISE_POPULATION_R8.json. `judged_live`/`judged_repo` are read from the REAL
    `census --not-judged` run's own printed CENSUS: COMPLETE line (this build step never re-runs that
    pull itself -- it is a separate, auditable command, per the order's own instrument list)."""
    with io.open(CARDS_PATH, encoding="utf-8") as fh:
        doc = json.load(fh)
    live_cards, repo_cards = doc["live_cards"], doc["repo_cards"]
    out = {
     "_about": ("LGIC_ENFORCE round 8, cell EN-p-36. Every RAISE on both planes dispositioned RESOLVED "
                "or CARDED; resolved+carded == raise_population per plane. Zero registry rows added: "
                "corroborated round-4 OWNER_CARDS_R4.md already researched every root token and found no "
                "citable owner for any of them."),
     "planes": {
      "live": {"resolved": [], "carded": live_cards, "raise_population": len(live_cards),
               "stopped": None, "judged": judged_live,
               "denominator_measured_at_write_time": {
                "instrument": "python lib/opal_naming.py census --live --budget 120 (to_judge population)",
                "value": doc["live_meta"]["to_judge"]}},
      "repo": {"resolved": [], "carded": repo_cards, "raise_population": len(repo_cards),
               "stopped": None, "judged": judged_repo,
               "denominator_measured_at_write_time": {
                "instrument": "python lib/opal_naming.py census --repo (names population)",
                "value": doc["repo_meta"]["names"]}},
     },
    }
    for plane, blk in out["planes"].items():
        total = len(blk["resolved"]) + len(blk["carded"])
        assert total == blk["raise_population"], (plane, total, blk["raise_population"])
    with io.open(RECORD_PATH, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=1)
    print("live: raise_population=%d judged=%d" % (out["planes"]["live"]["raise_population"], judged_live))
    print("repo: raise_population=%d judged=%d" % (out["planes"]["repo"]["raise_population"], judged_repo))
    print("WROTE %s" % RECORD_PATH)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("enumerate")
    sub.add_parser("classify")
    b = sub.add_parser("build")
    b.add_argument("--judged-live", type=int, required=True)
    b.add_argument("--judged-repo", type=int, required=True)
    a = ap.parse_args()
    if a.cmd == "enumerate":
        return cmd_enumerate()
    if a.cmd == "classify":
        return cmd_classify()
    if a.cmd == "build":
        return cmd_build(a.judged_live, a.judged_repo)
    print("unknown subcommand")
    return 2


if __name__ == "__main__":
    sys.exit(main())
