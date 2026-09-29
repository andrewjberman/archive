"""HVST-w-2 AMENDMENT 1 -- the in-process guards, installed by the RUNNER'S OWN PROCESS before it calls the
producer's CLI entry point in that same process. Never delivered through PYTHONPATH/sitecustomize into a child
(that is what failed at 00:21Z, row AMGT_HARVST-Z-W37-S3).

Entry points neutralised (each raises GuardStop, a BaseException, so the producer's own `except Exception`
handlers cannot swallow the stop and carry on to the next job):
  auth.SessionManager.refresh            the credentialed browser login          (auth.py:54)
  auth.SessionManager._refresh           the body refresh() delegates to          (belt)
  auth.SessionManager.get                its no-envelope fallback -> refresh      (auth.py:22)
  auth.SessionManager.repair_verification headed Chrome press-and-hold            (worker.py:282 calls it)
  verification.repair                    what repair_verification delegates to    (belt)
  verification.sync_playwright           the browser launch the repair path uses  (belt; import alone starts nothing)
  verification_locator.locate            the Moonshot POST                        (verification_locator.py:19)
  requests.sessions.Session.request      any request to a moonshot host           (belt, the wire level)
No file under lib/ is changed: the replacement is an in-memory attribute swap in this process only.

install_guards() takes the modules as parameters so a development test can hand it STUB modules whose real bodies
raise AssertionError -- the real SessionManager.refresh is never called unguarded, even to test.
"""
import collections
import sys


class GuardStop(BaseException):
    """A hard stop. BaseException on purpose: the producer's `except Exception` must not absorb it."""

    def __init__(self, entry, detail=""):
        super().__init__("GUARD STOP at %s %s" % (entry, detail))
        self.entry, self.detail = entry, detail


TRIPS = []                                   # every refusal, in order, this process
REQUEST_HOSTS = collections.Counter()        # hosts seen by requests.sessions.Session.request (the vision path)


def _mark(fn, name):
    fn._hvst_guard = name
    return fn


def install_guards(auth_mod=None, verification_mod=None, locator_mod=None, requests_mod=None):
    """Swap the entry points. Returns {entry_name: original_object} (kept only so a test can prove the swap)."""
    if auth_mod is None:
        import lib.opal_data_harvest.auth as auth_mod
    if verification_mod is None:
        import lib.opal_data_harvest.verification as verification_mod
    if locator_mod is None:
        import lib.opal_data_harvest.verification_locator as locator_mod
    if requests_mod is None:
        import requests as requests_mod
    SM = auth_mod.SessionManager
    originals = {"SessionManager.refresh": SM.refresh, "SessionManager._refresh": SM._refresh,
                 "SessionManager.get": SM.get, "SessionManager.repair_verification": SM.repair_verification,
                 "verification.repair": verification_mod.repair, "verification_locator.locate": locator_mod.locate,
                 "requests.Session.request": requests_mod.sessions.Session.request,
                 "verification.sync_playwright": getattr(verification_mod, "sync_playwright", None)}

    def stop(entry, detail=""):
        TRIPS.append({"entry": entry, "detail": detail})
        raise GuardStop(entry, detail)

    def refresh(self, publisher, *a, **k):
        stop("SessionManager.refresh", "publisher=%s" % publisher)

    def _refresh(self, publisher, *a, **k):
        stop("SessionManager._refresh", "publisher=%s" % publisher)

    def get(self, publisher):
        saved = self.vault.load(publisher)          # the producer's designed session read, unchanged
        if not saved:                                # ... but the no-envelope fallback (-> refresh) is a stop
            stop("SessionManager.get(no envelope)", "publisher=%s" % publisher)
        return saved

    def repair_verification(self, publisher, envelope, target_url=None):
        stop("SessionManager.repair_verification", "publisher=%s" % publisher)

    def repair(*a, **k):
        stop("verification.repair")

    def locate(*a, **k):
        stop("verification_locator.locate", "the Moonshot POST")

    def sync_playwright(*a, **k):
        stop("verification.sync_playwright", "a browser launch")

    real_request = originals["requests.Session.request"]

    def request(self, method, url, *a, **k):
        REQUEST_HOSTS[str(url).split("/")[2] if "//" in str(url) else str(url)] += 1
        if "moonshot" in str(url).lower():
            stop("requests.Session.request", "moonshot host")
        return real_request(self, method, url, *a, **k)

    SM.refresh = _mark(refresh, "SessionManager.refresh")
    SM._refresh = _mark(_refresh, "SessionManager._refresh")
    SM.get = _mark(get, "SessionManager.get")
    SM.repair_verification = _mark(repair_verification, "SessionManager.repair_verification")
    verification_mod.repair = _mark(repair, "verification.repair")
    locator_mod.locate = _mark(locate, "verification_locator.locate")
    requests_mod.sessions.Session.request = _mark(request, "requests.Session.request")
    if hasattr(verification_mod, "sync_playwright"):
        verification_mod.sync_playwright = _mark(sync_playwright, "verification.sync_playwright")
    # any module that bound `locate` / `repair` by name at import time keeps the ORIGINAL unless swapped too
    for mod in list(sys.modules.values()):
        if mod is None or mod is locator_mod or mod is verification_mod:
            continue
        try:
            if getattr(mod, "locate", None) is originals["verification_locator.locate"]:
                mod.locate = locator_mod.locate
            if getattr(mod, "repair", None) is originals["verification.repair"]:
                mod.repair = verification_mod.repair
        except Exception:  # noqa: S110 -- a module with a hostile __getattr__ is skipped, never fatal
            continue
    return originals


def resolve_entries(auth_mod=None, verification_mod=None, locator_mod=None, requests_mod=None, worker_mod=None):
    """(entry name, object as the PRODUCER resolves it, guard tag) for every entry point. `worker_mod` is
    included because the producer reaches SessionManager through lib.opal_data_harvest.worker."""
    if auth_mod is None:
        import lib.opal_data_harvest.auth as auth_mod
    if verification_mod is None:
        import lib.opal_data_harvest.verification as verification_mod
    if locator_mod is None:
        import lib.opal_data_harvest.verification_locator as locator_mod
    if requests_mod is None:
        import requests as requests_mod
    if worker_mod is None:
        import lib.opal_data_harvest.worker as worker_mod
    rows = [
        ("SessionManager.refresh", auth_mod.SessionManager.refresh),
        ("SessionManager._refresh", auth_mod.SessionManager._refresh),
        ("SessionManager.get", auth_mod.SessionManager.get),
        ("SessionManager.repair_verification", auth_mod.SessionManager.repair_verification),
        ("verification.repair", verification_mod.repair),
        ("verification_locator.locate", locator_mod.locate),
        ("requests.Session.request", requests_mod.sessions.Session.request),
        ("verification.sync_playwright", getattr(verification_mod, "sync_playwright", None)),
        ("worker.SessionManager.refresh (producer's route)", worker_mod.SessionManager.refresh),
        ("worker.SessionManager.get (producer's route)", worker_mod.SessionManager.get),
        ("worker.SessionManager.repair_verification (producer's route)", worker_mod.SessionManager.repair_verification),
    ]
    out = []
    for name, obj in rows:
        tag = getattr(obj, "_hvst_guard", None)
        want = name.split(" (")[0].replace("worker.", "")
        out.append((name, obj, tag, tag == want))
    return out


def print_identity(rows):
    print("guard identity, resolved INSIDE this process (pid %d):" % __import__("os").getpid())
    for name, obj, tag, ok in rows:
        print("  %-62s id=0x%x qualname=%s tag=%r IS_GUARD=%s" % (
            name, id(obj), getattr(obj, "__qualname__", "?"), tag, ok))
    return all(r[3] for r in rows)
