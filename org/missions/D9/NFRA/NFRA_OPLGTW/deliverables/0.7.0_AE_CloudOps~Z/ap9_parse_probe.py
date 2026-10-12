"""OG-ap-9 step 5 -- the SESSION-FREE parse read-back (COO half condition B).

Loads ONE package's own app/data_entitlement.py and asks its OWN parse_scope to parse a grant
scope whose `dates` dimension is {"mode": "rolling_complete_window", "calendar_months": 13}.
No session, no live invoke, no AWS call, no grant written: this reads the code that is deployed.

Run once per package, in its own process, so neither package's modules can bleed into the
other's import cache:
    python -I ap9_parse_probe.py <extracted-package-dir>

It prints one JSON line: AP9PARSE {"accepts_13": bool, "accepts_plain_rolling": bool, ...}

WHY THE SECOND SCOPE IS HERE. `parse_scope` refuses a scope for MANY reasons -- a master outside
the contract, an empty dimension, a bad account pattern. A refusal of the 13-month scope alone
would therefore not show that calendar_months is the cause; a wrong shape against a real parser
returns a real-looking refusal. So the probe also parses the SAME scope with a plain
{"mode": "rolling_complete_window"} and no calendar_months. If a package accepts the plain one and
refuses the 13-month one, the refusal is specifically about calendar_months. If it refuses both,
the scope itself is wrong and the result says nothing about the defect.
"""
import importlib.util
import json
import os
import sys
import types

pkg = sys.argv[1]
mod_path = os.path.join(pkg, "infra", "aws", "ec2", "opal-gateway", "app", "data_entitlement.py")

R = {"package_dir": pkg, "module_path_exists": os.path.isfile(mod_path)}

# data_entitlement.py uses RELATIVE imports, so loading it by path as a standalone module fails
# with "attempted relative import with no known parent package" -- and it fails IDENTICALLY for
# both packages, which would have made a careless reading ("the prior refuses!") completely wrong.
# It must be imported as app.data_entitlement, with the directory CONTAINING app/ on sys.path, so
# every sibling it imports comes from the SAME package rather than from this checkout.
pkg_root = os.path.join(pkg, "infra", "aws", "ec2", "opal-gateway")
sys.path.insert(0, pkg_root)
R["pkg_root"] = pkg_root

# The module imports boto3 at module scope, which is not installed in this interpreter, so the
# import failed IDENTICALLY for both packages -- measuring nothing about either. boto3 is stubbed
# so the module can load. This CANNOT change the verdict: parse_scope is pure dict validation
# (it reads the scope's own keys and the module's own constants, and makes no AWS call), and the
# SAME stub is applied to both packages, so the comparison stays symmetric. Recorded in the
# output so a reader can see the probe's own scaffolding.


class _Permissive(Exception):
    """Stands in for any boto3/botocore attribute. Module-scope code constructs things like
    Config(max_pool_connections=...), so it must accept arbitrary args; it subclasses Exception so
    that `except botocore.exceptions.ClientError` clauses remain valid except-expressions."""

    def __init__(self, *a, **k):
        super().__init__()

    def __call__(self, *a, **k):
        return self

    def __getattr__(self, item):
        if item.startswith("__"):
            raise AttributeError(item)
        return _Permissive()


class _AnyAttr(types.ModuleType):
    """A stub that is also a PACKAGE and yields a harmless class for any attribute, so a
    module-scope `from boto3.dynamodb.conditions import Key` resolves without boto3 installed."""

    __path__ = []  # makes it a package, so submodule imports resolve

    def __getattr__(self, item):
        if item.startswith("__"):
            raise AttributeError(item)
        return _Permissive


class _StubFinder:
    """Fabricates ANY boto3.* / botocore.* module on demand.

    Hand-listing submodules cascaded three times (boto3 -> boto3.dynamodb ->
    boto3.dynamodb.conditions -> boto3.dynamodb.types), each round failing IDENTICALLY for both
    packages and so measuring nothing. A finder ends the cascade in one move.
    """

    ROOTS = ("boto3", "botocore")

    # find_spec / create_module / exec_module is the MODERN finder API. The legacy
    # find_module/load_module pair was REMOVED in Python 3.12, and this interpreter is 3.14, so a
    # legacy finder is silently ignored -- which produced the same "No module named 'boto3'" for
    # both packages and again measured nothing.
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] not in self.ROOTS:
            return None
        return importlib.util.spec_from_loader(name, self, is_package=True)

    def create_module(self, spec):
        return _AnyAttr(spec.name)

    def exec_module(self, module):
        if "." in module.__name__:
            parent, _, child = module.__name__.rpartition(".")
            if parent in sys.modules:
                setattr(sys.modules[parent], child, module)


sys.meta_path.insert(0, _StubFinder())
R["stub_strategy"] = ("meta_path find_spec finder fabricating any boto3.*/botocore.* module on "
                      "demand (python %d.%d)" % sys.version_info[:2])

try:
    import app.data_entitlement as de
    R["loaded_from"] = getattr(de, "__file__", "?")
except Exception as e:
    R["load_error"] = type(e).__name__ + ": " + str(e)[:300]
    print("AP9PARSE " + json.dumps(R, sort_keys=True))
    raise SystemExit(0)

# Guard against loading THIS checkout's copy instead of the package's.
if os.path.abspath(pkg_root) not in os.path.abspath(R["loaded_from"]):
    R["load_error"] = "WRONG MODULE: loaded %s, which is not under %s" % (R["loaded_from"], pkg_root)
    print("AP9PARSE " + json.dumps(R, sort_keys=True))
    raise SystemExit(0)

R["has_parse_rolling_window"] = hasattr(de, "parse_rolling_window")
R["mentions_calendar_months_in_source"] = "calendar_months" in open(mod_path, encoding="utf-8").read()

# `accounts` is a DICT keyed by EXACTLY the granted masters (parse_scope: "scope.accounts must
# name the accounts of every granted master and no other"), not a flat list. The first attempt
# passed a list, and BOTH packages then refused on that field -- which the plain-rolling control
# caught, since it refused too. Without that control the prior's refusal would have read as the
# negative arm satisfied when it was really a malformed probe.
BASE = {
    "masters": ["08242234"],
    "datasets": ["dim_position"],
    "accounts": {"08242234": ["ACC1"]},
    # `columns` is likewise a DICT, keyed by exactly the granted datasets.
    "columns": {"dim_position": ["col1"]},
    "operations": ["list"],
}
scope_13 = dict(BASE, dates={"mode": "rolling_complete_window", "calendar_months": 13})
scope_plain = dict(BASE, dates={"mode": "rolling_complete_window"})


def attempt(scope, label):
    try:
        s = de.parse_scope(scope)
        out = {"accepted": True}
        cm = getattr(s, "calendar_months", "ATTR_ABSENT")
        out["calendar_months_on_result"] = cm if cm != "ATTR_ABSENT" else "ATTR_ABSENT"
        return out
    except Exception as e:
        return {"accepted": False, "error_type": type(e).__name__, "error": str(e)[:200]}


a13 = attempt(scope_13, "13")
apl = attempt(scope_plain, "plain")
R["result_13_months"] = a13
R["result_plain_rolling"] = apl
R["accepts_13"] = bool(a13.get("accepted"))
R["accepts_plain_rolling"] = bool(apl.get("accepted"))
R["refusal_is_specific_to_calendar_months"] = bool(apl.get("accepted")) and not bool(a13.get("accepted"))

print("AP9PARSE " + json.dumps(R, sort_keys=True))
