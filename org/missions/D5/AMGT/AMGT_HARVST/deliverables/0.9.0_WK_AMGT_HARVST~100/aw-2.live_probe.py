"""HVST-aw-2 live probe: sa through the real Publisher._ensure_session (tab, signed-in profile). Prints no cookie/header/token."""
import sys
import time

sys.path.insert(0, ".")
from lib.opal_data_harvest import publishers


def main():
    pub = publishers.Publisher("sa", {"bundle": {}}, lambda row: None, minimum=0, jitter=0)
    ok = []
    try:
        mod, sess = pub.module, pub.session
        try:
            r = mod.check(sess)
            print("account 200" if r.get("authorized") else "account NOT-AUTHORIZED")
            ok.append(bool(r.get("authorized")))
        except Exception as exc:
            print("account FAIL %s" % type(exc).__name__, str(exc)[:80])
            ok.append(False)
            return ok
        time.sleep(16)
        try:
            j = mod.news(sess, "AAPL", limit=5)
            items = j.get("data") or []
            print("listing 200 items=%d" % len(items))
            ok.append(len(items) > 0)
        except Exception as exc:
            print("listing FAIL %s" % type(exc).__name__, str(exc)[:80])
            ok.append(False)
            return ok
        time.sleep(16)
        try:
            a = mod.article(sess, items[0]["id"])
            print("article 200 body_chars=%d" % len(a.get("content") or ""))
            ok.append(True)
        except Exception as exc:
            print("article FAIL %s" % type(exc).__name__, str(exc)[:80])
            ok.append(False)
    finally:
        try:
            pub.session.close()
        except Exception as exc:
            print("close %s" % type(exc).__name__)
    return ok


if __name__ == "__main__":
    res = main()
    if len(res) == 3 and all(res):
        print("ALL 200")
