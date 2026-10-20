"""Does a resident package's own schema set admit a request composition? (READ ONLY, offline.)

usage: python -I check_schema_admits.py <package.tar.gz> <composition.json>

Builds a jsonschema registry from the tarball's members docs/contracts/investor-reporting/v1/*.schema.json (direct
children only; the leading "./" of a tar member name is ignored), validates the composition against
RequestComposition.schema.json and prints exactly one line:
  SCHEMA-ADMITS errors=0                       rc 0 when the composition validates
  SCHEMA-REFUSES errors=<n> <validator>@<path> rc 1 with the first error (closed words and key path, no value)
  SCHEMA-CHECK-BAD <why>                        rc 2 when the tarball or the composition cannot be read
ASCII only.
"""
import json
import sys
import tarfile

import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

PREFIX = "docs/contracts/investor-reporting/v1/"
ROOT_SCHEMA = PREFIX + "RequestComposition.schema.json"


def bad(why):
    print("SCHEMA-CHECK-BAD %s" % why)
    return 2


def normal(name):
    return name[2:] if name.startswith("./") else name


def package_schemas(tar_path):
    """Return {member name: parsed JSON} for the direct children of the v1 schema directory."""
    out = {}
    with tarfile.open(tar_path, "r:*") as tar:
        for member in tar.getmembers():
            name = normal(member.name)
            if not member.isfile() or not name.startswith(PREFIX):
                continue
            rest = name[len(PREFIX):]
            if "/" in rest or not rest.endswith(".schema.json"):
                continue
            out[name] = json.load(tar.extractfile(member))
    return out


def build_registry(schemas):
    pairs = []
    for name, doc in schemas.items():
        uri = doc.get("$id") or "opal://irpt/contracts/v1/" + name[len(PREFIX):]
        pairs.append((uri, Resource.from_contents(doc, default_specification=DRAFT202012)))
    return Registry().with_resources(pairs)


def main(argv):
    if len(argv) != 2:
        return bad("usage: check_schema_admits.py <package.tar.gz> <composition.json>")
    try:
        schemas = package_schemas(argv[0])
    except (OSError, tarfile.TarError, ValueError) as exc:
        return bad("tarball unreadable: %s" % type(exc).__name__)
    if ROOT_SCHEMA not in schemas:
        return bad("tarball has no %s" % ROOT_SCHEMA)
    try:
        with open(argv[1], encoding="utf-8") as fh:
            composition = json.load(fh)
    except (OSError, ValueError) as exc:
        return bad("composition unreadable: %s" % type(exc).__name__)
    validator = jsonschema.Draft202012Validator(schemas[ROOT_SCHEMA], registry=build_registry(schemas))
    errors = sorted(validator.iter_errors(composition), key=lambda err: ("/".join(str(p) for p in err.absolute_path), err.validator))
    if not errors:
        print("SCHEMA-ADMITS errors=0")
        return 0
    first = errors[0]
    where = "/".join(str(p) for p in first.absolute_path) or "$"
    print("SCHEMA-REFUSES errors=%d %s@%s" % (len(errors), first.validator, where))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
