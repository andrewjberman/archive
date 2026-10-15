"""IRPT_DASHBD round 111, the label rule (issuer 2.0.0_SA_COO~D2) -- the CVO's round-110 FAIL on the account labels (ADJUDICATION_v70) and the CTO's ruling (round 111 analysis,
@5d2241be16): "ending" prints only before a real digit run of at least 4 digits from a field measured to be the custodian account number; otherwise the label is
"Account <n> of <N>" (household order). No Inflection field is measured to be that number yet (DB-b-226 reads it), so every Inflection account takes the fallback.

  DB-b-225 (~180)  the relabelled sample (last4 null for every account, every value as in the round-110 sample), the render rule, a test that "ending" never precedes a
                   fragment, every page read.                                                                                                      DB111-2-AC1 (+ J1, the CVO's)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P10 = load_mod("p110", "r110/p110_inflection.py")
P9 = P10.P9
P7, P6, P5, P3, P = P9.P7, P9.P6, P9.P5, P9.P3, P9.P
need, nes, is_int, sha = P.need, P.nes, P.is_int, P.sha
D, PRIV, Fail = P.D, P.PRIV, P.Fail
accounts_of, whole_document_scan = P6.accounts_of, P6.whole_document_scan
SAMPLE_DIR11 = PRIV + "IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~180/"
V051_SHA = "0b515243b310bb95de8d9bebdb0f2725b70626307adcc9f4fb80298883692df4"  # the contract 0.5.1 bytes this round built against; a later contract keeps the record valid through the lineage
OUT_R11 = PRIV + "fwd21_sample_r111/"
W180 = D + "0.9.0_WK_IRPT_DASHBD~180/"
NEEDS_MORE = P10.NEEDS_MORE


def canon(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def label_of(account, position, total, measured_digits=False):
    """THE RULE (pure): 'Account ending NNNN' only when the account carries a real digit run of at least 4 digits as its last4; otherwise 'Account <n> of <N>'."""
    l4 = account.get("last4")
    if measured_digits and isinstance(l4, str) and re.fullmatch(r"[0-9]{4,}", l4):
        return "Account ending %s" % l4
    return "Account %d of %d" % (position, total)


# ---------------------------------------------------------------- DB111-2-AC1, the sample half
def check_sample(root):
    r = P.load(root, W180 + "BUILD_R111.json")
    c = P.contract(root)
    ver = tuple(int(x) for x in str(c.get("contract_version") or "0.0.0").split("."))
    need(ver >= (0, 5, 1), "the contract must be 0.5.1 or later")
    s = r.get("sample") or {}
    sp = str(s.get("path") or "").replace("\\", "/")
    need(sp.startswith(SAMPLE_DIR11) and sp.endswith("HOUSEHOLD_SAMPLE.json") and Path(sp).is_file(), "sample.path must be the private HOUSEHOLD_SAMPLE.json under %s" % SAMPLE_DIR11)
    need(not sp.startswith(str(root.resolve()).replace("\\", "/").rstrip("/") + "/"), "the sample is inside the repo: client data never goes there")
    need(s.get("sha256") == sha(sp) and s.get("contract_sha256") in (sha(root / P10.CONTRACT_REL), V051_SHA), "sample.sha256 and sample.contract_sha256 must equal the sample bytes and the contract bytes (current, or the 0.5.1 bytes this round built against)")
    sm = P.sample_json(sp)
    P5.check_sample_shape_k(sm, c, "inflection")
    prob = P5.kind_problems(sm["values"], c, "inflection")
    need(not prob, "kind carrier: %s" % "; ".join(prob[:3]))
    acc = accounts_of(sm)
    conf, dis, st = whole_document_scan(sm["values"], acc)
    need(st["unmapped"] == 0 and not conf and not dis, "whole-document rule: unmapped %d, %s" % (st["unmapped"], "; ".join((conf + dis)[:3])))
    ec = P10.equivalence_conflicts(sm["values"], c, acc)
    need(not ec, "equivalence rule: %s" % "; ".join(ec[:3]))
    # the only change against the round-110 sample is the label: every value, every window, every date is the same
    prev = P.load(root, D + "0.9.0_WK_IRPT_DASHBD~175/BUILD_R110.json")
    pp = str((prev.get("sample") or {}).get("path") or "")
    need(Path(pp).is_file(), "the round-110 sample is missing")
    old = P.sample_json(pp)
    need(canon(sm["values"]) == canon(old["values"]) and r.get("values_sha256_equal_to_r110") is True, "every value must equal the round-110 sample's (only the label changes)")
    need(sm["household"]["as_of"] == old["household"]["as_of"] and sm["household"]["first_data_date"] == old["household"]["first_data_date"] and sm["household"]["household_ref"] == old["household"]["household_ref"], "the household ref, as_of and first_data_date equal the round-110 sample's")
    need([a["account_id"] for a in sm["household"]["accounts"]] == [a["account_id"] for a in old["household"]["accounts"]], "the accounts and their order equal the round-110 sample's")
    for a, b in zip(sm["household"]["accounts"], old["household"]["accounts"]):
        need(a["first_data_date"] == b["first_data_date"] and a["window_status"] == b["window_status"], "an account's first_data_date and window_status equal the round-110 sample's")
        need(a["last4"] is None, "every account's last4 is null: no field is measured to be the custodian account number, so no account takes the 'ending' label")
    need(r.get("accounts") == len(acc) and nes(r.get("label_basis")) and "measured" in r["label_basis"].lower(), "accounts must equal %d and label_basis must say in words that no field is measured to be the custodian account number" % len(acc))
    ar = json.loads((root / P9.ALIEN_REC).read_bytes().decode("utf-8"))
    need(r.get("orion_guard") == ar["result"]["guard_state_for_render_record"], "orion_guard must equal the issuer's read-gate state")
    need(r.get("files_in_repo") is False and r.get("served_values_changed") is False and r.get("pushed") is False and r.get("deployed") is False, "files_in_repo, served_values_changed, pushed and deployed must be false")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("secret_reads") == 0 and is_int(rd.get("s3_reads")), "reads: zero writes, vendor calls and secret reads; s3_reads an integer")
    need(not P.long_digit_runs({k: v for k, v in r.items() if k != "sample"}), "the record holds a run of 8 or more digits")
    return sm


# ---------------------------------------------------------------- DB111-2-AC1, the render half
def render_extras11(html, sm):
    """the round-110 render clauses without the last-four clause, plus the label rule: no 'Account ending' label, every account labelled 'Account <n> of <N>' in household order."""
    fails = []
    acc = {a["account_id"]: a for a in sm["household"]["accounts"]}
    gl = {e: t for m, e, t in P10.cell_texts(html) if m == "glr.ending_value" and e}
    for a in acc:
        t = gl.get(a)
        if t is None or "not available" in t.lower() or not re.search(r"\$\s*[\d,]+", t):
            fails.append("the gain/loss Ending Value of an account does not print a figure")
    by_key = {}
    for n in [n for n in P7.parse_notes(html) if n["kind"] == "absent"]:
        for mem, ent in n["keys"]:
            by_key.setdefault((mem, ent), set()).add(re.sub(r"\s+", " ", n["text"]).strip().lower())
            m = re.match(r"avs\.(qtd|ytd|last_12_months)\.", mem)
            a = acc.get(ent)
            if m and a and a["window_status"][m.group(1)] == "NOT_SPANNED" and NEEDS_MORE in n["text"].lower():
                fails.append("a note says 'needs more history' for an account window that is not spanned (%s)" % m.group(1))
    two = sorted(k for k, v in by_key.items() if len(v) > 1)
    if two:
        fails.append("%d cell(s) carry two different reasons in two notes" % len(two))
    vt = P3.visible_text(html)
    if re.search(r"Account ending", vt):
        fails.append("a label says 'Account ending' while no field is measured to be the custodian account number (%d times)" % len(re.findall(r"Account ending", vt)))
    n_acc = len(acc)
    for i in range(1, n_acc + 1):
        if not re.search(r"Account %d of %d\b" % (i, n_acc), vt):
            fails.append("the label 'Account %d of %d' is not printed" % (i, n_acc))
    return fails


def extra_inflection11(root, r, k, vals, tab, exp):
    P9.extra_inflection(root, r, k, vals, tab, exp)
    sm = P.sample_json(str((k.get("sample") or {}).get("path") or ""))
    for name, text in (("tab_html", tab), ("export_html", exp)):
        f = render_extras11(text, sm)
        need(not f, "%s: %s" % (name, "; ".join(f[:3])))


def build_check_render():
    src = inspect.getsource(P9.check_render)
    for a, b in (("0.9.0_WK_IRPT_DASHBD~173/RENDER_R109.json", "0.9.0_WK_IRPT_DASHBD~180/RENDER_R111.json"),
                 ("0.9.0_WK_IRPT_DASHBD~173/BUILD_R109.json", "0.9.0_WK_IRPT_DASHBD~180/BUILD_R111.json"),
                 ("wk-IRPT_DASHBD-173-portal", "wk-IRPT_DASHBD-180-portal"),
                 ("extra_inflection(root, r, k, vals, tab, exp)", "extra_inflection11(root, r, k, vals, tab, exp)"),
                 ("OUT_R9", "OUT_R11")):
        need(a in src, "check_render generation: %r not in the round-109 source" % a)
        src = src.replace(a, b)
    nl = chr(10)
    lines = [ln for ln in src.split(nl) if "each account's last4 label must be four digits" not in ln]
    need(len(lines) == len(src.split(nl)) - 1, "check_render generation: the round-109 last4 clause was not found exactly once")
    ns = dict(vars(P9))
    ns.update(OUT_R11=OUT_R11, extra_inflection11=extra_inflection11, FIRM_TITLE9=P9.firm_title())
    exec(compile(nl.join(lines), "p111_check_render", "exec"), ns)
    return ns["check_render"]


def check_all(root):
    check_sample(root)
    build_check_render()(root)
    r = P.load(root, W180 + "RENDER_R111.json")
    lb = r.get("labels") or {}
    need(is_int(lb.get("position_labels")) and lb.get("ending_labels") == 0 and lb["position_labels"] >= 2, "RENDER_R111.json labels must be {position_labels (one per account), ending_labels 0}")
    t = r.get("tests") or {}
    need(nes(t.get("fragment_test")) and t.get("fragment_cases") and all(isinstance(x, str) for x in t["fragment_cases"]), "tests.fragment_test (the test name) and tests.fragment_cases (the kinds of fragment the test feeds: words, letters and digits mixed, a digit run under 4) must be recorded")
    print("OK: the sample is the round-110 sample with every last4 null; the render prints 'Account <n> of <N>' for %d accounts and no 'Account ending' label; the CVO's counts hold; a test feeds fragments and the label never says ending" % lb["position_labels"])


# ---------------------------------------------------------------- self-test
def selftest(root):
    arms = []

    def arm(name, ok):
        arms.append(name)
        if not ok:
            raise Fail("self-test arm failed: " + name)
    arm("a null last4 takes the position label", label_of({"last4": None}, 2, 5) == "Account 2 of 5")
    arm("a fragment never takes ending", label_of({"last4": "tion"}, 1, 3, True) == "Account 1 of 3")
    arm("a mixed fragment never takes ending", label_of({"last4": "4INT"}, 1, 3, True) == "Account 1 of 3")
    arm("a measured digit run takes ending", label_of({"last4": "1234"}, 1, 3, True) == "Account ending 1234")
    arm("a digit run under 4 never takes ending", label_of({"last4": "123"}, 1, 3, True) == "Account 1 of 3")
    sm = {"household": {"accounts": [{"account_id": "1111", "last4": None, "window_status": {"qtd": "MEASURED", "ytd": "MEASURED", "last_12_months": "MEASURED", "since_inception": "MEASURED"}},
                                    {"account_id": "2222", "last4": None, "window_status": {"qtd": "MEASURED", "ytd": "MEASURED", "last_12_months": "MEASURED", "since_inception": "MEASURED"}}]}}
    good = ('<td data-member="glr.ending_value" data-entity="1111">$5</td><td data-member="glr.ending_value" data-entity="2222">$6</td><h2>Account 1 of 2</h2><h3>Account 2 of 2</h3>')
    arm("the clean render is quiet", render_extras11(good, sm) == [])
    arm("an 'Account ending' label is found", len(render_extras11(good + "<p>Account ending tion</p>", sm)) == 1)
    arm("a missing position label is found", any("Account 2 of 2" in x for x in render_extras11(good.replace("Account 2 of 2", "Account B"), sm)))
    print("SELFTEST OK: %d arms: %s" % (len(arms), "; ".join(arms)))


CHECKS = {"DB111-2-AC1": check_all}


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        selftest(Path(argv[2] if len(argv) > 2 else ".").resolve())
        return 0
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p111_labels.py <repo_root> <%s>" % "|".join(CHECKS))
        return 2
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        CHECKS[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
