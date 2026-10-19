# AMGT-cf-1 receipt -- the filings entry reads the model key in-process from Secrets Manager

**Worker:** `0.9.0_WK_AMGT_RESAPP~527` **Order:** `AMGT_RESAPP.TO-AMGT-cf-1` **Base:** `5dae2841dd` (issuance commit)
**Branch:** `wk-AMGT_RESAPP-527` (LOCAL; not pushed, not merged).

## What changed

- `lib/research/llm_batch/run.py`: 227 lines (was 176; 52 insertions, 1 deletion). The one deletion is the
  `runner=default_runner` argument in `main()`, now `runner=keyed_runner(args.task)`. `default_runner` is unchanged.
  Added: the constants `ANTHROPIC_SECRET_ID` and `KEY_TASKS`, the class `KeyReadError`, and the functions
  `read_anthropic_key` and `keyed_runner`.
- `lib/research/llm_batch/tests/test_key_read.py`: 134 lines, new. Tests T1 to T8.

No other path was touched. `lib/research/filings/`, `run_filings.cmd`, `tasks.py`, `inputs.py`, `portal/` and
`org/devices/` are unchanged. No AWS, model, SEC, vendor or Bloomberg call was made; no push; no deploy.

### Final text of the functions added (`lib/research/llm_batch/run.py`)

```python
ANTHROPIC_SECRET_ID = "anthropic-api-key"  # the estate's Secrets id for the Anthropic key (comp-secrets list, firm shared)
KEY_TASKS = frozenset({"filings"})  # the tasks whose real command calls the model and so needs ANTHROPIC_API_KEY


class KeyReadError(Exception):
    """The Anthropic key could not be read from Secrets. Its text names the secret id and the exception TYPE only."""


def read_anthropic_key(secrets=None) -> str:
    """The Anthropic key: the raw SecretString of ANTHROPIC_SECRET_ID, stripped. `secrets` is a callable(secret_id) ->
    SecretString (the seam tests use); the default reads Secrets Manager in us-east-1 (the ocilar_hcaptcha pattern)."""
    if secrets is None:
        def secrets(secret_id):
            import boto3
            return boto3.client("secretsmanager", region_name="us-east-1").get_secret_value(SecretId=secret_id)["SecretString"]
    try:
        raw = secrets(ANTHROPIC_SECRET_ID)
    except Exception as exc:
        raise KeyReadError("could not read %s from Secrets (%s)" % (ANTHROPIC_SECRET_ID, type(exc).__name__)) from None
    if not isinstance(raw, str) or not raw.strip():
        raise KeyReadError("secret %s has no usable value" % ANTHROPIC_SECRET_ID)
    return raw.strip()


def keyed_runner(task_key: str, *, secrets=None, run=subprocess.run, environ=None) -> Runner:
    """The runner main() uses. For a KEY_TASKS task's real command it reads the key once (cached for this runner's life)
    and gives it to the child's environment only (env=). A plan-only argv, a task outside KEY_TASKS, or an environment
    that already holds a non-empty ANTHROPIC_API_KEY runs exactly as default_runner does. The key is never printed, never
    put in argv, never written to a file and never set in this process; child output has the key replaced by ***."""
    env_source = os.environ if environ is None else environ
    cache = {}

    def runner(argv: Tuple[str, ...]) -> Tuple[int, str]:
        if task_key not in KEY_TASKS or "--plan-only" in argv or env_source.get("ANTHROPIC_API_KEY"):
            proc = run(list(argv), cwd=ROOT, stdout=subprocess.PIPE, universal_newlines=True,
                       encoding="utf-8", errors="replace")
            return proc.returncode, proc.stdout or ""
        if "key" not in cache:
            try:
                cache["key"] = read_anthropic_key(secrets)
            except KeyReadError as exc:
                sys.stderr.write("LLM-BATCH task=%s key read FAILED: %s\n" % (task_key, exc))
                return 1, ""
        key = cache["key"]
        proc = run(list(argv), cwd=ROOT, env=dict(env_source, ANTHROPIC_API_KEY=key), stdout=subprocess.PIPE,
                   universal_newlines=True, encoding="utf-8", errors="replace")
        return proc.returncode, (proc.stdout or "").replace(key, "***")

    return runner
```

## Tests

`lib/research/llm_batch/tests/test_key_read.py`, hand-written expectations, stub `run` and stub `secrets`, the fake
value `sk-test-FAKEKEY-0123456789` only.

- T1 filings real command, no `--plan-only`, no variable in `environ`: the secret is read once (`anthropic-api-key`);
  the child's `env` carries the fake value; argv unchanged; `cwd`, `universal_newlines`, `encoding`, `errors` as
  specified; the process's own `os.environ` is unchanged; a second call reads nothing (cache).
- T2 a key already in `environ`: no secret read, no `env=` keyword.
- T3 a `--plan-only` argv: no secret read, no `env=` keyword.
- T4 task `scores`: no secret read, no `env=` keyword.
- T5 `secrets` raises `RuntimeError("deny-PAYLOAD-xyz")`: returns `(1, "")`, the child never runs, stderr names
  `anthropic-api-key` and `RuntimeError`, and does not contain `deny-PAYLOAD-xyz`.
- T6 `secrets` returns `""` and `"   "`: returns `(1, "")`, the child never runs, stderr names the secret and `no usable value`.
- T7 the child's stdout contains the fake value: the returned output has `***` and not the value; stderr never has it.
- T8 control: `run.main(["filings", "--print-command"])` returns 0 and prints the `command=` line with
  `read_anthropic_key` replaced by a function that fails the test if called.

### Counts

Base (`5dae2841dd`, `run.py` unedited, test file written first):
- `lib/research/llm_batch/tests/test_key_read.py`: `7 failed, 1 passed` (T1 to T7 fail with
  `AttributeError: ... has no attribute 'keyed_runner'`; T8 passes as the control).
- `lib/research/llm_batch/tests` (whole directory, before the new file was added to the run): `60 passed in 3.88s`.

After the build:
- `test_key_read.py` (AC1 literal): `8 passed in 0.67s`, `exit=0`.
- `lib/research/llm_batch/tests` (AC2 literal): `68 passed in 3.89s`, rc 0.
- `python -m ruff check --target-version py39` on both files: `All checks passed!`.
- ASCII check on both files: no non-ASCII bytes.

## Not verified

- The real Secrets Manager call is never made here. The issuer's `AMGT-cf-5` runs the scheduled task
  `OpalResearch-FilingsAnalyzer` once on demand after the merge and reads rc, the objects and a grep for the key's
  prefix. Whether the task's Windows user holds AWS credentials is read there.
- The secret id `anthropic-api-key` was not re-read from `comp-secrets list` at this cut (an AWS read, forbidden by
  the order's bounds); it is taken from the order's premise.
- The keyed runner has not been exercised against a real child process or a real model call.
- The mechanism that makes the key visible to `lib/research/filings/analyze.py` is the child's environment only;
  that package is unchanged, and its read of `ANTHROPIC_API_KEY` is not re-checked here.
