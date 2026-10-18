"""AMGT_RESAPP round 116 (AMGT-bw-1 / bw-5 grade): every money line of the LIVE printed pack against the page's served figure.

  [R116_LOCAL=1] PYTHONPATH=<repo root> python r116_pack_money_vs_page.py [KEY ...]      (R116_LOCAL=1: the pack comes from this checkout's own Lambda handler, the page from the live function)
       (default: ICT_PM_Equity RIO_LN_Equity GOOGL_US_Equity)

Read-only (Lambda invokes of GET /thesis and GET /print?format=pdf on opal-amgt-scoped-api). For each name it reads the page's `header_figures`
(the figures the page shows: value, unit, OWN `currency`) and the pack's text, and for each header figure whose unit is money (MILLIONS,
ABSOLUTE (full currency units), PRICE, PER SHARE) it finds the pack lines that carry that figure's printed label, parses the printed currency
word and amount, and compares with the page:
  OK            the printed currency equals the figure's OWN currency and the magnitude equals the page's (to the printed rounding);
  OK-UNCONFIRMED  the figure carries NO own currency and the line says so in the page's words ("does not confirm this figure's currency") and prints no currency code;
  WRONG-CURRENCY  the printed code differs from the figure's own (or a code is printed for a figure with none);
  WRONG-MAGNITUDE the amount differs.
Prints one line per figure and `MONEY VS PAGE: YES|NO (<ok> of <n> money lines)`. It grades NOTHING by itself: the verdict is the issuer's read of the lines.
"""
import base64
import json
import os
import re
import sys

import boto3

os.environ.setdefault("AMGT_AIFILL_ROOT", "/var/empty/aifill-hold")
sys.path.insert(0, ".")
import fitz  # noqa: E402

from lib.research.print import render_pack as rp  # noqa: E402

FN = "opal-amgt-scoped-api"
WITHHELD_WORDS = "Bloomberg does not confirm this figure's currency"  # the page's CURRENCY_UNCONFIRMED_WORDS, StatTile.tsx
UNCONFIRMED_WORDS = ("currency not stated", "does not confirm this figure's currency")  # the page's two wordings: a valued amount with no currency, and an unmeasured basis
LAM = boto3.client("lambda", region_name="us-east-1")


def _call(key, route, query=None):
    ev = {"rawPath": "/api/scoped/amgt/security/%s/%s" % (key, route), "queryStringParameters": query,
          "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}
    if os.environ.get("R116_LOCAL") == "1" and route == "print":  # the CANDIDATE: this checkout's own handler over the live pool (the page side stays live)
        return _local_handler()(ev, None)
    return json.loads(LAM.invoke(FunctionName=FN, Payload=json.dumps(ev).encode())["Payload"].read())


_LOCAL = []


def _local_handler():
    if not _LOCAL:
        import importlib.util
        spec = importlib.util.spec_from_file_location("lam", "infra/aws/lambda/research/scoped_amgt_api/lambda_function.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _LOCAL.append(mod.lambda_handler)
    return _LOCAL[0]


def _pack_text(key):
    r = _call(key, "print", {"format": "pdf"})
    raw = base64.b64decode(r["body"]) if r.get("isBase64Encoded") else r["body"].encode("latin-1")
    return "\n".join(p.get_text() for p in fitz.open(stream=raw, filetype="pdf"))


def _lines(text):
    out = []
    for ln in text.splitlines():
        ln = ln.strip()
        if ln:
            out.append(ln)
    return out


AMT = re.compile(r"(?P<cur>[A-Za-z]{2,5}|local currency)?\s*(?P<amt>-?[\d,]+(?:\.\d+)?)\s*(?P<tail>million|billion|per share)?")


def _expected(fig):
    unit = str(fig.get("unit") or "")
    v = fig.get("value")
    if not isinstance(v, (int, float)):
        return None
    if unit.startswith("MILLIONS (share count)") or not (unit.startswith(("MILLIONS", "ABSOLUTE (full", "PRICE", "PER SHARE"))):
        return None
    if unit.startswith("ABSOLUTE (full"):
        return ("million", v / 1e6)
    if unit.startswith("MILLIONS"):
        return ("million", float(v))
    return ("per share", float(v))


def grade(key):
    body = json.loads(_call(key, "thesis")["body"])
    text = _pack_text(key)
    lines = _lines(text)
    # only the HEADER block: the fiscal-year blocks repeat labels such as `Share price (last close)` once per year
    try:
        h0 = next(i for i, ln in enumerate(lines) if ln == "Header")
        h1 = next((i for i in range(h0 + 1, len(lines)) if lines[i].startswith("Fiscal year ")), len(lines))
        lines = lines[h0 + 1:h1]
    except StopIteration:
        pass
    results = []
    for fig in body.get("header_figures") or []:
        exp = _expected(fig)
        if exp is None:
            continue
        label = rp._plain_label(fig)
        own = (fig.get("currency") or "").strip() or None
        labels = [label] + (["Market value, currency-adjusted"] if fig.get("mnemonic") == "CRNCY_ADJ_MKT_CAP" else [])
        cands = [ln for ln in lines if any(ln.lower().startswith(lb.lower()) for lb in labels)]
        seen = set()
        unmeasured = bool(re.match(r"\s*UNMEASURED\b", str(fig.get("currency_basis") or "")))
        if unmeasured:  # round 117: the PAGE withholds an UNMEASURED money figure (StatTile.tsx isUnmeasuredBasis; a dash, the hover words); so does the pack: the page's words, NO amount
            mine = [ln for ln in cands if ":" in ln]
            if not mine:
                alias = fig.get("mnemonic") == "CRNCY_ADJ_MKT_CAP"  # the second market-value line is dropped by the same-value dedup (round 116): its absence is the dedup, not a miss
                results.append((fig.get("mnemonic"), label, own, None, 0.0, exp[1], "OK-DEDUPED" if alias else "MISSING-LINE", "(no pack line%s)" % (": the same-value dedup of the market cap line" if alias else " for a figure the page withholds")))
            for ln in mine:
                val = ln.split(":", 1)[1]
                has_words = WITHHELD_WORDS in val
                has_digit = bool(re.search(r"\d", val.split(" - ")[0]))
                verdict = "OK-WITHHELD" if has_words and not has_digit else ("WRONG-AMOUNT-PRINTED" if has_digit else "NO-WITHHELD-WORDS")
                results.append((fig.get("mnemonic"), label, own, None, 0.0, exp[1], verdict, ln[:110]))
            continue
        for ln in cands:
            if ln in seen or ":" not in ln:
                continue
            seen.add(ln)
            val = ln.split(":", 1)[1]
            m = AMT.search(val)
            if not m:
                continue
            cur = (m.group("cur") or "").strip() or None
            try:
                amt = float(m.group("amt").replace(",", ""))
            except ValueError:
                continue
            kind, want = exp
            mag_ok = abs(amt - want) <= max(0.06, abs(want) * 0.0006) if kind == "million" else abs(amt - want) <= 0.006 + abs(want) * 1e-6
            if own:
                verdict = "OK" if (cur == own and mag_ok) else ("WRONG-CURRENCY" if cur != own else "WRONG-MAGNITUDE")
            else:
                if any(w in ln for w in UNCONFIRMED_WORDS) and (cur in (None, "local currency") or cur.lower() == "currency"):
                    verdict = "OK-UNCONFIRMED" if mag_ok else "WRONG-MAGNITUDE"
                else:
                    verdict = "WRONG-CURRENCY" if cur not in (None, "local currency") else "NO-UNCONFIRMED-WORDS"
            results.append((fig.get("mnemonic"), label, own, cur, amt, want, verdict, ln[:110]))
    return results


def main(argv):
    keys = argv[1:] or ["ICT_PM_Equity", "RIO_LN_Equity", "GOOGL_US_Equity"]
    ok = total = 0
    for key in keys:
        print("==", key)
        for mn, label, own, cur, amt, want, verdict, ln in grade(key):
            total += 1
            ok += 1 if verdict.startswith("OK") else 0
            print("  %-26s own=%-5s printed=%-14s amt=%-18s page=%-18s %s | %s" % (mn, own, cur, "%.2f" % amt, "%.2f" % want, verdict, ln))
    print("MONEY VS PAGE: %s (%d of %d money lines)" % ("YES" if total and ok == total else "NO", ok, total))
    return 0 if total and ok == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
