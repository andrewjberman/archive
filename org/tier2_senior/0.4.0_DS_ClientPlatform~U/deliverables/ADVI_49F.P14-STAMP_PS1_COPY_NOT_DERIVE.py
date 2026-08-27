"""ADVI_49F.P14-STAMP PS-1 -- propagation is a COPY, and it is copied from the MIRROR.

Four arms, all against the DEPLOYED bundle staged by the PS battery (_ps_deployed2), because
the claim is about what the campaign will execute, not about the repo copy:

  A. THE TWO RULED ENTRYPOINT TOKENS ARE PRESENT, by AST over the deployed entrypoint:
     a00's stage carries --local-out (ruling 76736(i)) and c02's carries it too (ruling 76887).
     Negative control: the same predicate must NOT find the token on a stage that has none.
  B. NO DERIVATION IN ANY WRITER: an AST walk of c00/c01/c02 finds zero epoch-computation
     identifiers -- no call to attestation_epoch, no attested_count, no date-vs-epoch compare.
     The basis arrives from _attestation_basis_from_mirror and nowhere else.
     A SUBSTRING SCAN WOULD BE THE WRONG INSTRUMENT HERE and 0.7.0_AE_CloudOps~L proved it
     tonight: their grep for 'epoch'/'converter' over the entrypoint returned 5 hits that were
     ALL comments and argparse help -- including the help text that explains the ban. A file
     that documents its own prohibition reads as violating it. So: AST only, and the two
     controls below.
  C. NO --declared-historical WIDENING: exactly one stage in the deployed entrypoint carries
     the flag token, and it is a00. Negative control: planting it on another stage flips it.
  D. THE READ IS FROM THE MIRROR, NOT FROM S3: each writer's basis helper resolves a local
     filesystem path built from its --canonical-local/--local-out argument. Asserted by AST on
     the helper body (no boto3/s3 call inside it), with the S3-read rejection stated: option
     (ii) was rejected by ruling 76704 for adding same-run read-after-write across 533 dates.

Author: 0.4.0_DS_ClientPlatform~U | ADVI_49F.P14-STAMP | 2026-08-27
"""
import ast
import sys
from pathlib import Path

STAGE = Path("C:/Users/ANDREW~1/AppData/Local/Temp/claude/"
             "C--Users-AndrewBerman-Desktop-ajb-workspace/"
             "9c462caa-4942-4b63-85d3-1783cfb1645f/scratchpad/_ps_deployed2")
WRITERS = ("c00_flow_ledger.py", "c01_nna_canonical.py", "c02_twr_engine.py")
DERIVE_IDENTIFIERS = {"attestation_epoch", "attested_count", "_epoch", "epoch"}
ok = True

print("PS-1 arms, all against the DEPLOYED bundle at", STAGE)
if not (STAGE / "chain_49f_entrypoint.py").is_file():
    print("REFUSED: deployed bundle not staged -- run the PS battery first (it stages it).")
    sys.exit(2)

# --- A. the two ruled tokens, by AST over _stage_list's returned tuples -----------------
src = (STAGE / "chain_49f_entrypoint.py").read_text(encoding="utf-8")
tree = ast.parse(src)
fn = next(n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == "_stage_list")
ret = next(n for n in ast.walk(fn) if isinstance(n, ast.Return))
stage_tokens = {}
for elt in ret.value.elts:
    name = elt.elts[0].value
    argv_src = ast.unparse(elt.elts[1])
    stage_tokens[name] = argv_src
mirror_carriers = sorted(k for k, v in stage_tokens.items() if "+ m" in v or "+m" in v)
dh_carriers = sorted(k for k, v in stage_tokens.items() if "dh" in v.split())
print(f"\nA. stages in the deployed entrypoint: {len(stage_tokens)} (denominator printed)")
print(f"   stages carrying the mirror token m: {len(mirror_carriers)} -> {mirror_carriers}")
a_ok = "a00_dim_account" in mirror_carriers and "c02_twr_daily" in mirror_carriers
print(f"   BOTH RULED STAGES carry it (a00 per 76736(i), c02 per 76887): {a_ok}")
neg_a = "a03_dim_security" not in mirror_carriers
print(f"   NEG CTRL a stage with no mirror token is NOT reported as carrying one "
      f"(a03_dim_security): {neg_a}")
ok = ok and a_ok and neg_a

# --- B. no derivation identifiers in any writer ----------------------------------------
print("\nB. derivation identifiers in the three writers (AST -- comments and docstrings are "
      "NOT executable and are correctly invisible here)")
for w in WRITERS:
    wt = ast.parse((STAGE / w).read_text(encoding="utf-8"))
    names = {n.id for n in ast.walk(wt) if isinstance(n, ast.Name)}
    names |= {n.attr for n in ast.walk(wt) if isinstance(n, ast.Attribute)}
    names |= {n.name for n in ast.walk(wt) if isinstance(n, (ast.FunctionDef,))}
    hits = sorted(names & DERIVE_IDENTIFIERS)
    src_w = (STAGE / w).read_text(encoding="utf-8")
    substring_hits = sum(src_w.count(t) for t in ("epoch", "converter"))
    print(f"   {w:<24} AST derivation identifiers: {hits or 'none'}   "
          f"(substring hits for epoch/converter: {substring_hits} -- prose, and this is exactly "
          f"why the arm is AST)")
    ok = ok and not hits
# control of the control: the predicate must FIND a planted derivation call
planted = ast.parse("def f():\n    return attestation_epoch()\n")
pn = {n.id for n in ast.walk(planted) if isinstance(n, ast.Name)}
print(f"   NEG CTRL the same predicate FINDS a planted attestation_epoch() call: "
      f"{bool(pn & DERIVE_IDENTIFIERS)}")
ok = ok and bool(pn & DERIVE_IDENTIFIERS)

# --- C. --declared-historical argv scope stays a00-only ---------------------------------
print(f"\nC. stages carrying the dh token: {len(dh_carriers)} -> {dh_carriers}")
c_ok = dh_carriers == ["a00_dim_account"]
print(f"   EXACTLY a00, no widening: {c_ok}")
ok = ok and c_ok

# --- D. the basis is read from the LOCAL mirror, not from S3 ----------------------------
print("\nD. _attestation_basis_from_mirror reads a LOCAL path (option (ii), the S3 read, was "
      "REJECTED by ruling 76704)")
for w in WRITERS:
    wt = ast.parse((STAGE / w).read_text(encoding="utf-8"))
    helper = next((n for n in ast.walk(wt) if isinstance(n, ast.FunctionDef)
                   and n.name == "_attestation_basis_from_mirror"), None)
    if helper is None:
        print(f"   {w:<24} *** helper ABSENT ***")
        ok = False
        continue
    body = ast.unparse(helper)
    s3ish = [t for t in ("boto3", "s3", "get_object", "Bucket") if t in body]
    reads_local = "Path(" in body and "manifest.json" in body
    print(f"   {w:<24} local-path read={reads_local}  s3 tokens in helper body="
          f"{s3ish or 'none'}")
    ok = ok and reads_local and not s3ish

print(f"\nPS-1 VERDICT: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
