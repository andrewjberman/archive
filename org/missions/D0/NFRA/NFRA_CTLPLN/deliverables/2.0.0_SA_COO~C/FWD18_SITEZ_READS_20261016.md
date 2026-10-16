# NFRA_CTLPLN round 27 -- FWD-18, site Z: the reads from git (issuer 2.0.0_SA_COO~C, 2026-10-16 ~06:5xZ)

Call `XB-20261016T051708Z-662b` (laptop to `1.0.0_SA_CTO~Z`): receive the tabulate pack on a scratch target, read it from the scratch only, commit on `box/sitez`. Site Z's evidence is commit `7d969d9aa6` (author `1.0.0_SA_CTO~Z`, 2026-10-16T01:27:33-04:00 = 05:27:33Z), an ancestor of `origin/box/sitez` (read with `git merge-base --is-ancestor` after a fetch at 06:45Z; an earlier fetch at 06:15Z, before site Z's 06:20Z push per MSTR msg 109634, did not carry it). Folder `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/1.0.0_SA_CTO~Z/xb_r27_sitez_scratch_receive/`. Every line below is read from that commit.

| step | read |
|---|---|
| verify | `INTAKE-VERIFY pack=PACK3 wheels=1 verified=1 checked=1 stray=0 ok=True`, rc 0 |
| prove | `INTAKE-PROVE device=sitez python=3.14.8 wheels=1 installed=1 imported=1 import_missing_dep=0 failed=0 refused=0 ok=True`, rc 0 |
| install | `INTAKE-INSTALL device=sitez python=3.14.8 wheels=1 installed=1 refused=0 target_form=target dry_run=False ok=True`, rc 0; `received_sha256` `024ca478df22e9340661486f85298cff5f6dcdba14f3813e8830015b9ed1948f`, EQUAL to the laptop's wheel |
| pip logs | the install log (657 bytes) and the prove log (676 bytes) each hash to the SHA-256 their receipt's `pip_log` names (`9b39364f...2bd84` and `168853da...6016b`; the issuer hashed both committed files); both carry `--no-index --no-deps` and the three pins; `inherited_pip_vars_removed=` is empty on site Z (dell1's carried `PIP_NO_INDEX`) |
| the read from scratch | a fresh process from a folder outside the workspace, `PYTHONPATH` = `SCRATCH_TARGET_Z` only, `python -s`: `tabulate.__file__ = C:\Users\Opal Bloomberg\opal_intake_r27\SCRATCH_TARGET_Z\tabulate\__init__.py`, `tabulate.__version__ = 0.9.0`, a 2-row table (install and prove receipts, rc 0, `024ca478df22`); `sys.path[0:3]` lists the script folder, then `SCRATCH_TARGET_Z`, then the interpreter's zip |

**Pass (the call's step 4):** the table prints and `__file__` sits under `SCRATCH_TARGET_Z`: both hold.

**The departure, stated:** `tailscale file get` returned "moved 0/0 files", because the Windows Tailscale client had already saved the four Taildrop files to `Downloads` at 05:05-05:06Z, the minutes of the laptop's four sends (`TAILDROP_RECORD_SITEZ.md`). Site Z COPIED them into `PACK3` and states their SHA-256 values equal `MANIFEST.json`'s. This seat cross-checked two of them against the laptop's own send record: the check record `8178cfa9b614...` and the delivery file `bc45f2c1d7df...` equal the hashes the laptop recorded before it sent; the wheel's `024ca478df22...` equals the laptop's. The delivery of the four files is therefore evidenced by content, not by a Taildrop receipt.

**Not read by this seat:** site Z's live filesystem (the scratch folders still exist; nothing was deleted, as the call asked: the recursive delete is Andrew's word); the site Z shell (the `python -s` and `PYTHONPATH` facts rest on the committed `output/4_read_from_scratch.txt`, which prints `PYTHONPATH` and `sys.path`, and the script).
