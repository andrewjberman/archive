"""OG-rl-4 PHASE B guard P1 (CVO half @82708ab726): are MAIL_BEARER and TRANSCRIPT_BEARER distinct from every other route bearer?
Runs ON THE HOST via rl4_ssm.py (base64-shipped). Values come from /proc/<opal-gateway MainPID>/environ -- .env is never sourced or read.
Prints only "<A> vs <B>: EQUAL|DIFFER" per pair (plus token COUNTS per key). Never prints a value or a hash of one.
Split 1 = whitespace (the order's text); split 2 = the routes' own _split, re.split(r"[\\s,]+") (what _shared_elsewhere compares).
A pair is EQUAL when ANY token of A equals ANY token of B; every token pair is compared with hmac.compare_digest, no short-circuit."""
import hmac
import re
import subprocess

pid = subprocess.check_output(["systemctl", "show", "opal-gateway", "-p", "MainPID", "--value"]).decode().strip()
env = {}
for kv in open("/proc/%s/environ" % pid, "rb").read().split(bytes([0])):
    if b"=" in kv:
        k, v = kv.split(b"=", 1)
        env[k.decode()] = v
A_KEYS = ("MAIL_BEARER", "TRANSCRIPT_BEARER")
OTHERS = ("OTP_BEARER", "MS_INGEST_BEARER", "GRAPH_READ_BEARER", "TEAMS_BEARER", "TAXSMA_WORKBOOK_BEARER")


def toks(name, mode):
    raw = env.get(name, b"").decode("utf-8", "replace")
    if mode == "ws":
        return [t for t in raw.split() if t]
    return [t for t in re.split(r"[\s,]+", raw.strip()) if t]


def equal(a, b, mode):
    hit = False
    for x in toks(a, mode):
        for y in toks(b, mode):
            if hmac.compare_digest(x.encode("utf-8"), y.encode("utf-8")):
                hit = True
    return hit


pairs = [(a, b) for a in A_KEYS for b in OTHERS] + [("MAIL_BEARER", "TRANSCRIPT_BEARER")]
print("P1 MainPID-read ok=%s keys_in_process_env=%d" % (bool(pid) and pid != "0", len(env)))
for k in A_KEYS + OTHERS:
    print("TOKENS %s ws=%d app=%d present=%s" % (k, len(toks(k, "ws")), len(toks(k, "app")), k in env))
n_eq = 0
for mode in ("ws", "app"):
    print("-- split=%s (%d pairs)" % (mode, len(pairs)))
    for a, b in pairs:
        e = equal(a, b, mode)
        n_eq += 1 if e else 0
        print("%s vs %s: %s" % (a, b, "EQUAL" if e else "DIFFER"))
print("P1 RESULT: %s (EQUAL pairs %d of %d)" % ("STOP" if n_eq else "ALL DIFFER", n_eq, 2 * len(pairs)))
# Positive control (not a P1 pair): the same compare on a key against itself must read EQUAL, so an all-DIFFER is not a broken compare.
for k in A_KEYS:
    print("CONTROL %s vs %s (self): %s" % (k, k, "EQUAL" if equal(k, k, "app") else "DIFFER"))
