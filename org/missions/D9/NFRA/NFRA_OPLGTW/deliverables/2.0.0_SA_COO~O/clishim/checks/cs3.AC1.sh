#!/usr/bin/env bash
# OPLGTW OG-cs-3 AC1 (cli-shim workstream, wave 2): app/folder_engine.py, the pure half: the five sensitive column classes dropped BY NAME, and the caller's request mapped to the engine's closed-grammar plan. One fresh process, no AWS, no child process.
#  (a) drop_sensitive(names) -> (kept, dropped): of 24 probe names, EXACTLY the 17 sensitive ones are dropped (tax identifier, mailing address, email, phone, date of birth; snake_case and CamelCase) and the 7 look-alikes (tax_lot_id, tax_amount, taxable_amount, mail_flag, account_id, trade_date, quantity) are KEPT; kept and dropped keep the input order;
#  (b) sensitive_class(name) names the class ("tax_identifier", "mailing_address", "email", "phone", "date_of_birth") or None;
#  (c) plan_from_request(request, allowed_columns): a rows request becomes a QueryPlan of mode "rows" with the columns, filters (eq, gte, in), order_by and limit; an aggregate request (group_by plus aggregates) becomes mode "aggregate"; an omitted limit is 100; a limit above 500 is clamped to 500;
#  (d) refusals raise engine.EngineError with code INVALID_REQUEST: a column not in allowed_columns (a dropped sensitive column is never in them), an unknown filter operator, a limit below 1, a rows request with no columns, an unknown top-level key in the request.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
import warnings
warnings.simplefilter("ignore")
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    from app import folder_engine as fe
    from app.integrations.schwab import engine as eng
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)
SENS = ["tax_id", "TaxID", "taxpayer_id", "ssn", "tin", "mailing_address_1", "MailingAddress", "address_line1", "street", "zip_code", "postal_code",
        "email", "EmailAddress", "phone_number", "mobile", "date_of_birth", "dob"]
KEEP = ["tax_lot_id", "tax_amount", "taxable_amount", "mail_flag", "account_id", "trade_date", "quantity"]
names = [x for pair in zip(SENS[:7], KEEP) for x in pair] + SENS[7:]
kept, dropped = fe.drop_sensitive(names)
say("exactly the %d sensitive probe names are dropped and the %d look-alikes kept (dropped %d, kept %d)" % (len(SENS), len(KEEP), len(dropped), len(kept)),
    sorted(dropped) == sorted(SENS) and sorted(kept) == sorted(KEEP))
say("kept and dropped keep the input order", kept == [n for n in names if n in KEEP] and dropped == [n for n in names if n in SENS])
cls = {n: fe.sensitive_class(n) for n in ("ssn", "TaxID", "MailingAddress", "email", "phone_number", "dob", "account_id")}
say("sensitive_class names the class or None", cls == {"ssn": "tax_identifier", "TaxID": "tax_identifier", "MailingAddress": "mailing_address", "email": "email", "phone_number": "phone", "dob": "date_of_birth", "account_id": None})
A = ("a", "b", "c")
p1 = fe.plan_from_request({"columns": ["a", "b"], "filters": [{"field": "a", "op": "eq", "value": 1}, {"field": "b", "op": "gte", "value": "x"}, {"field": "c", "op": "in", "value": [1, 2]}],
                           "order_by": [{"field": "a", "direction": "asc"}], "limit": 50}, A)
p2 = fe.plan_from_request({"group_by": ["a"], "aggregates": [{"function": "sum", "field": "b", "alias": "tb"}]}, A)
p3 = fe.plan_from_request({"columns": ["a"], "limit": 9999}, A)
p4 = fe.plan_from_request({"columns": ["a"]}, A)
say("a rows request becomes a rows plan with its parts", p1.mode == "rows" and tuple(p1.columns) == ("a", "b") and len(p1.filters) == 3 and p1.filters[0].op == "eq" and p1.limit == 50 and p1.order_by[0].field == "a")
say("an aggregate request becomes an aggregate plan", p2.mode == "aggregate" and tuple(p2.group_by) == ("a",) and p2.aggregates[0].alias == "tb")
say("limit: omitted is 100, 9999 is clamped to 500", p4.limit == 100 and p3.limit == 500)


def refused(req, allowed=A):
    try:
        fe.plan_from_request(req, allowed)
        return None
    except eng.EngineError as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__


bad = {"a dropped sensitive column": refused({"columns": ["email"]}), "a column outside allowed": refused({"columns": ["zzz"]}),
       "an unknown operator": refused({"columns": ["a"], "filters": [{"field": "a", "op": "like", "value": "x"}]}),
       "a limit of 0": refused({"columns": ["a"], "limit": 0}), "a rows request with no columns": refused({"filters": []}),
       "an unknown top-level key": refused({"columns": ["a"], "sql": "select 1"})}
say("refusals raise EngineError INVALID_REQUEST (%s)" % ", ".join("%s: %s" % (k, v) for k, v in bad.items()), all(v == eng.ERROR_INVALID_REQUEST for v in bad.values()))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
