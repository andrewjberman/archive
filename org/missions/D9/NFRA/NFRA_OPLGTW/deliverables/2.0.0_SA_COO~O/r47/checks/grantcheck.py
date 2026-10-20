"""Round-47 grant checks (OG-gv-1: Andrew's Schwab grant moves to the master-wide scope; OG-gm-1: Menachem's Schwab grant, master-wide).

usage: python3 -I grantcheck.py <phaseA|phaseB> <andrew|menachem> <W-directory>
Prints labelled lines and a last line OK or NO. Counts and hashes only; no account number is read into any printed line.

PHASE A reads W/<P>_BEFORE.json, W/<P>_DIFF.json, W/<P>_PREFLIGHT_DECIDE.json, W/<P>_DENY.json and W/NEVER_WIDEN_ASK_OG-<o>.md (P = GV1 or GM1, o = gv-1 or gm-1).
PHASE B re-reads the LIVE policy partitions (strong reads) and W/<P>_READBACK.json.
"""
import hashlib
import json
import os
import re
import sys

phase, who, W = sys.argv[1], sys.argv[2], sys.argv[3]
P = {"andrew": "GV1", "menachem": "GM1"}[who]
ORDER = {"andrew": "og-gv-1", "menachem": "og-gm-1"}[who]
ASK = "NEVER_WIDEN_ASK_OG-%s.md" % {"andrew": "gv-1", "menachem": "gm-1"}[who]
MASTERS = {"andrew": ("08242234", "08335338"), "menachem": ("08242234", "08335338")}[who]
TOOLS = ("schwab_get_access", "schwab_list_files", "schwab_describe_dataset", "schwab_query")


def Y(x):
    return "yes" if x else "no"


if who == "andrew":
    DL_TEXT = "leaves schwab_prepare_download as his stored operations say"
    DL_TEXT_B = "leaves prepare_download as his stored operations say"
else:
    DL_TEXT = "refuses schwab_prepare_download"
    DL_TEXT_B = "refuses prepare_download"


def download_ok(dec):
    """Andrew: prepare_download is UNCHANGED (admitted iff his stored operations include download_filtered; the two booleans are equal). Menachem: refused (Alyssa's template has no download)."""
    if who == "andrew":
        dl = dec.get("download") or {}
        a, b = dl.get("stored_operations_include_download_filtered"), dl.get("prepare_download_admitted")
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    return (dec.get("refuse") or {}).get("schwab_prepare_download") is True


def load(name):
    try:
        return json.load(open(os.path.join(W, name), encoding="utf-8"))
    except Exception:
        return None


def phase_a():
    b, d, p, dn = load(P + "_BEFORE.json"), load(P + "_DIFF.json"), load(P + "_PREFLIGHT_DECIDE.json"), load(P + "_DENY.json")
    pr = (b or {}).get("principal") or {}
    first = pr.get("first_grant") is True
    ok_b = (bool(b) and pr.get("role") == who and bool(pr.get("pk_hash")) and isinstance(pr.get("scope_sans_accounts_sha256"), str)
            and bool((b.get("denominator") or {}).get("policy_items_scanned")) and (first or isinstance(pr.get("accounts_before_counts"), dict)))
    df = (d or {}).get(who) or {}
    want_keys = ["accounts"] if (who == "andrew") else ["accounts", "masters"]
    ok_d = (df.get("changed_keys") == want_keys and sorted(df.get("masters_after") or []) == sorted(MASTERS)
            and all((df.get("accounts_after") or {}).get(m) == ["*"] for m in MASTERS) and df.get("rest_of_scope_matches_template") is True)
    dec = (p or {}).get(who) or {}
    ok_p = bool(p) and all((dec.get("admit") or {}).get(t) is True for t in TOOLS) and download_ok(dec) and dec.get("master_wide_parsed") is True
    de = dn or {}
    ok_dn = (isinstance(de.get("deny_record_present_before"), bool) and isinstance(de.get("activate_writes_deny"), bool) and isinstance(de.get("options"), list) and len(de["options"]) >= 2
             and isinstance(de.get("effect"), str) and len(de["effect"]) >= 40 and de.get("delete_proposed") is False)
    try:
        ask = open(os.path.join(W, ASK), encoding="utf-8").read()
    except Exception:
        ask = ""
    halves = all(re.search(r"(?mi)^#{2,4}\s.*\b%s\b" % h, ask) for h in ("CTO", "COO", "CVO"))
    pws = "process-wide state this change touches" in ask
    order_sentence = bool(re.search(r"(?i)OG-rl-18.{0,120}(CLOSED|live)", ask))
    emails = len(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", ask))
    digits = len(re.findall(r"\d{9,}", ask))
    print("before-record: %s with pk_hash, scope hash and a printed denominator%s: %s" % (who, " (a first grant)" if first else ", per-master counts", Y(ok_b)))
    print("diff keys %s, masters after == the two original masters, every master's accounts == ['*'], the rest of the scope equals its template: %s" % (want_keys, Y(ok_d)))
    print("decide() pre-flight on the candidate (master-wide parser) admits the 4 read tools and %s: %s" % (DL_TEXT, Y(ok_p)))
    print("email_deny finding: present before %s, activation writes it %s, options named %s, effect stated, no delete proposed: %s" % (
        de.get("deny_record_present_before"), de.get("activate_writes_deny"), len(de.get("options") or []), Y(ok_dn)))
    print("ask: three halves %s; process-wide state line %s; states OG-rl-18 live before the activation %s; e-mail-shaped strings %d (want 0); runs of 9+ digits %d (want 0)" % (Y(halves), Y(pws), Y(order_sentence), emails, digits))
    ok = ok_b and ok_d and ok_p and ok_dn and halves and pws and order_sentence and emails == 0 and digits == 0
    print("OK" if ok else "NO")


def phase_b():
    try:
        import boto3
        from boto3.dynamodb.types import TypeDeserializer
        td = TypeDeserializer()
        c = boto3.client("dynamodb", region_name="us-east-1")
        kw = {"TableName": "gateway-access-state-table", "ConsistentRead": True,
              "FilterExpression": "begins_with(pk,:p)", "ExpressionAttributeValues": {":p": {"S": "POLICY#"}}}
        items = []
        while True:
            r = c.scan(**kw)
            items += r["Items"]
            if "LastEvaluatedKey" not in r:
                break
            kw["ExclusiveStartKey"] = r["LastEvaluatedKey"]
    except Exception as e:
        print("live read FAILED %s" % type(e).__name__)
        print("NO")
        return
    def val(i, k):
        return list(i[k].values())[0] if k in i else None
    prof = {}
    for i in items:
        if val(i, "record_type") == "principal_profile" and val(i, "email") and val(i, "status") == "active":
            em = val(i, "email").lower()
            for role in ("andrew", "menachem", "alyssa"):
                if em.startswith(role):
                    prof[role] = i

    def grant(role):
        pf = prof.get(role)
        if not pf:
            return None, None
        pk, gr = val(pf, "pk"), str(val(pf, "grant_revision"))
        for i in items:
            if val(i, "pk") == pk and val(i, "record_type") == "data_entitlement" and str(val(i, "revision")) == gr:
                s = td.deserialize(i["scope"]) if "scope" in i else None
                return int(gr), (json.loads(s) if isinstance(s, str) else s)
        return None, None

    before = load(P + "_BEFORE.json") or {}
    pr = before.get("principal") or {}
    rev, sc = grant(who)
    sc = sc or {}
    acc = sc.get("accounts") or {}
    first = pr.get("first_grant") is True
    newer = rev is not None and (first or (pr.get("grant_revision") is not None and rev > int(pr["grant_revision"])))
    masters_ok = sorted(sc.get("masters") or []) == sorted(MASTERS)
    wide_ok = all(acc.get(m) == ["*"] for m in MASTERS) and set(acc) == set(MASTERS)
    def num(o):
        return int(o) if o == int(o) else float(o)

    rest = {k: v for k, v in sc.items() if k not in ("accounts", "masters")}
    resth = hashlib.sha256(json.dumps(rest, sort_keys=True, separators=(",", ":"), default=num).encode()).hexdigest()
    rest_ok = resth == (load(P + "_DIFF.json") or {}).get(who, {}).get("rest_sha256_after_expected")
    other = "alyssa"
    orev, _ = grant(other)
    ob = (load("MG2_BEFORE.json") or {}).get("principals", [])
    omap = {r.get("role"): r for r in ob}
    other_ok = orev is not None and (omap.get(other) or {}).get("grant_revision") is not None and orev >= int(omap[other]["grant_revision"])
    rb = load(P + "_READBACK.json") or {}
    mk = (load("rl18_release.json") or {}).get("release_sha", "")
    dec = rb.get("decide") or {}
    dec_ok = (all((dec.get("admit") or {}).get(t) is True for t in TOOLS) and download_ok(dec)
              and rb.get("tree") == "deployed" and bool(mk) and rb.get("code_sha") == mk)
    sv = rb.get("served") or {}
    served_ok = sv.get("account_count_all_masters") == "all" and isinstance(sv.get("query_rows"), int) and sv["query_rows"] >= 1 and sv.get("as_principal") == who
    print("%s: active %s; newer grant revision %s; masters equal the two originals %s; accounts == ['*'] for every master %s; rest of scope unchanged %s" % (
        who, Y(who in prof), Y(newer), Y(masters_ok), Y(wide_ok), Y(rest_ok)))
    print("%s's grant revision as before: %s" % (other, Y(other_ok)))
    print("decide() on the LIVE grant against the DEPLOYED tree at the batch17 release: admits 4 read tools and %s: %s" % (DL_TEXT_B, Y(dec_ok)))
    print("served read as %s through the gateway: schwab_get_access account_count 'all' for every master and one bounded schwab_query answered %s row(s): %s" % (who, sv.get("query_rows"), Y(served_ok)))
    print("OK" if all((who in prof, newer, masters_ok, wide_ok, rest_ok, other_ok, dec_ok, served_ok)) else "NO")


phase_a() if phase == "phaseA" else phase_b()
