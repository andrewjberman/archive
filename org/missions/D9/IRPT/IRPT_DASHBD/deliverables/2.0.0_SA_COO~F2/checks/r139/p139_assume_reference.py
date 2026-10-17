"""Reference implementation of cell DB-f-2705 (positive control for p139_assume.py ONLY; applied to the trunk launcher, graded, then the file is restored with git checkout).
Usage: python p139_assume_reference.py <repo_root>"""
import sys
from pathlib import Path

L = Path(sys.argv[1], "data/inf/scripts/gold/INF_G_01.account_transaction_gold.py")
s = L.read_text(encoding="utf-8")


def sub(old, new):
    global s
    if s.count(old) != 1:
        raise SystemExit("reference: anchor not found exactly once: %r" % old[:60])
    s = s.replace(old, new)


sub('''DEFAULT_CAP = 25
''', '''DEFAULT_CAP = 25
# The role this launcher assumes for its reads and writes (the narrow account-transaction role), and the fixed session name its trust names.
SESSION_NAME = "inf-g-01-account-transaction"
''')
sub('''    root = _repo_root()
    if root is None:
        raise SystemExit("REFUSED: the naming registry is read from the repo layout only (no repo root beside this launcher)")
    lib = str(root / "lib")''', '''    root = _repo_root()
    if root is None:
        root = bootstrap()
    lib = str(root / "lib")''')
sub('''def orion_prefix():''', '''def role_name():
    """The builder-made name of the account-transaction role (never typed)."""
    _firm_row()
    import opal_naming
    return opal_naming.name("orion", "inflection", "account-transaction", "role")


def assumed_s3_client(sts=None, client_factory=None):
    """An S3 client built from temporary credentials of the account-transaction role (fixed session name). A failed assume REFUSES naming the role."""
    if sts is None or client_factory is None:
        import boto3
        sts = sts or boto3.client("sts")
        client_factory = client_factory or boto3.client
    role = role_name()
    account = sts.get_caller_identity()["Account"]
    try:
        cred = sts.assume_role(RoleArn="arn:aws:iam::%s:role/%s" % (account, role), RoleSessionName=SESSION_NAME)["Credentials"]
    except Exception as exc:  # noqa: BLE001
        raise SystemExit("REFUSED: could not assume role %s as session %s (%s)" % (role, SESSION_NAME, type(exc).__name__))
    return client_factory("s3", aws_access_key_id=cred["AccessKeyId"], aws_secret_access_key=cred["SecretAccessKey"],
                          aws_session_token=cred["SessionToken"])


def orion_prefix():''')
sub('''        import boto3
        s3 = boto3.client("s3")
''', '''        s3 = assumed_s3_client()
        print("INF_G_01 assumed role %s session %s" % (role_name(), SESSION_NAME))
''')
L.write_text(s, encoding="utf-8", newline="")
print("reference applied")
