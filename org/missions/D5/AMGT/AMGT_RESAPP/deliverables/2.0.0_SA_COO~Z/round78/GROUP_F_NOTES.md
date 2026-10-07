# AMGT_RESAPP round 78 -- GROUP F: one drafted cell (bb-23, the CTO's ruling in msg 31206)

Drafted for `2.0.0_SA_COO~Z` on 2026-10-07. Nothing is committed. Two repo files were written: this file and
`round78/checks/r78_bb23.py` (passes `bash .tools/commit-gate.sh`: "pre-commit gate clean for 1 of 1 file(s)"). The build
script was not edited and not run, the helper was not created, no pip command ran, nothing was fetched, no AWS write was
made. AWS reads: `lambda get_function_configuration` on `opal-amgt-scoped-api`, once per run of AC1 and AC2.

**The ruling served (CTO msg 31206).** "One LOCAL cell edits build-and-upload-scoped-amgt.sh before bb-18. Term 1: the
script takes the two folders only from a zip whose sha256 equals the live function's CodeSha256 read at build time, and
stops if it does not; it never falls back to a download on this box. Term 2: the cell's check is as proposed, the two
folders in the new zip equal the deployed zip's byte for byte, with a negative control (one changed byte fails). pyarrow
stays the pruned 138 files; the prune step must leave it unchanged, which the equality check shows. This covers these two
versions only: a version bump goes back through the laptop's intake."

**The base.** The shared tree on `CLOUD`; HEAD read `12fdfae38d` at the first dry-run and `9c759c41fe` at the last. The
build script is clean in the shared tree. Python 3.14.7.

---

## F1 -- `AMGT-bb-23` -- THE BUILD TAKES PYARROW AND RPDS-PY FROM THE DEPLOYED PACKAGE, NEVER FROM A DOWNLOAD

### 1. MEASURED AT THE BASE

**The deployed package on this box.** `C:/tmp/ba20-r77-14a36147bd.zip`: 41,981,131 bytes, 380 entries, 0 directory
entries, every entry deflated. Its sha256 in base64 is `MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=`; the live
function's CodeSha256, read by the check, is the same string.

**The four folders in it (147 files, 129,318,685 bytes unpacked).**

| folder | files | bytes unpacked |
|---|---|---|
| `pyarrow/` | 132 | 128,118,395 |
| `pyarrow-16.1.0.dist-info/` | 6 (LICENSE.txt, METADATA, NOTICE.txt, RECORD, WHEEL, top_level.txt) | 187,735 |
| `rpds/` | 4 (`__init__.py`, `__init__.pyi`, `py.typed`, `rpds.cpython-311-x86_64-linux-gnu.so`) | 985,869 |
| `rpds_py-2026.6.3.dist-info/` | 5 (METADATA, RECORD, WHEEL, licenses/LICENSE, sboms/rpds-py.cyclonedx.json) | 26,686 |

- pyarrow: 138 files in all (132 + 6); its RECORD lists 745. rpds-py: 9 files in all (4 + 5); its RECORD lists 9.
  The issuer's "rpds 4 files + dist-info 9 of 9" reads as 4 + 5 = 9, not 4 + 9.
- 31 `.so` names among the 147. The largest member is `pyarrow/libarrow.so.1601`, 69,200,512 bytes.
- 0 of the 147 names collide when case is ignored (a Windows folder can hold them all).
- The package's dist-info folders are 7: attrs-26.1.0, jsonschema-4.26.0, jsonschema_specifications-2025.9.1,
  pyarrow-16.1.0, referencing-0.37.0, rpds_py-2026.6.3, typing_extensions-4.16.0.

**The prune.** The script's prune list is `VENDOR_PRUNE = ("pyarrow/include/", "pyarrow/src/", "/tests/", "/testing/")`
(line 247), applied to each wheel member at line 440. Applied to the 147 deployed names it removes 0. So the deployed copy
is a fixed point of the prune: even a prune run over the copied folders would not change them. The draft still routes the
copied files around the prune.

**The build script, `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh` (741 lines, `bash -n` exits 0).**

| lines | what is there |
|---|---|
| 108-111 | the only flag: `--build-only <out.zip>`, read as `$1` and `$2`; there is no other flag parser |
| 113-117 | `AWS` is `.tools/aws` when present |
| 123 | `gen_harvest_prefixes.py --check` (imports no boto3, urllib, subprocess or requests) |
| 126, 132, 133 | `RPDS_PIN`, `PYARROW_PIN`, `VENDOR_PINS` (seven pins) |
| 135-137 | pip download 1: the seven pins for cp311 manylinux2014_x86_64 into `$WHEELS` |
| 141-147 | prints the sha256 of each downloaded wheel |
| 149-542 | one Python block (`python - "$ROOT" "$ZIP" "$WHEELS"`): closure, data members, the wheel unpack with the prune (427-448), the two-native-wheels refusal (449-455), the zip (458-482: entries sorted by name, fixed date, deflated), the verify |
| 243-244 | `NATIVE_WHEEL_PREFIXES`, `NATIVE_WHEEL_TAGS`: the two compiled wheels admitted |
| 514-515, 537 | the build stops unless `pyarrow/__init__.py`, `rpds/__init__.py` and an `rpds/` member named for cpython-311 x86_64 linux are packaged |
| 545-723 | the isolated runtime check; pip download 2 at 560-561 fetches the rpds-py wheel of the BUILD interpreter (no `--platform`) into `$LOCAL_WHEELS`, used in a scratch folder only |
| 729 | `content_diff.py --zip "$ZIP"`, in both modes |
| 731-735 | `--build-only` copies the zip out and exits 0 |
| 738-740 | the upload (`upload_verified.sh`), reached only without `--build-only` |

**AWS and network use of a `--build-only` run today.** No AWS write. Two fetch routes: the two pip downloads, and
`content_diff.py`, which calls `lambda get_function` (boto3) and then downloads the whole deployed package from the
function's code location (`urllib.request.urlopen`, lines 46-52 of that file) to print a content diff. See section 8.

**A base64 hash handed from Git Bash to Python is rewritten when it begins with a slash.** Measured:
`python -c ... --expect-sha256 "/kM9Kf..."` arrives as `C:/Program Files/Git/kM9Kf...`; the same happens to
`--expect-sha256=/kM9Kf...` and to an environment variable. With `MSYS2_ARG_CONV_EXCL='--expect-sha256='` set on the
command, `--expect-sha256=/kM9Kf...` arrives unchanged while `--zip /tmp/x.zip` and `--dest /tmp/d` are still converted
to Windows paths (which the build needs, because `$TMP` is a Git Bash path). One CodeSha256 in 64 begins with a slash;
without the exclusion that build would stop on a false mismatch. The draft's call line carries the exclusion.

**The check's passing arm was exercised.** A prototype helper written OUTSIDE the repo (the session scratch folder) and a
scratch copy of the script carrying edits S1, S3 and S5 below: AC1, AC2 and AC3 (the six clauses it had then) all read
YES against them. The prototype and the patched copy are not in the repo and are not handed to the worker.

**The comparer on two built zips (not a criterion).** `r78_bb23.py --compare-zip <zip>` compares a built zip's four
folders with the deployed zip's. The deployed zip against itself: 147 of 147 equal. The older kept build
`C:/tmp/az5-build-r76.zip`: 147 of 147 equal, so two builds a day apart packaged the same bytes for these folders.

### 2. THE ACT (worker face text)

The build of the `opal-amgt-scoped-api` package downloads seven Python packages from the internet. That is no longer
allowed on this machine. Five of them will arrive as files and are not your concern. The other two, pyarrow 16.1.0 and
rpds-py 2026.6.3, must be taken from the package that is running now: the build copies their files out of a local copy
of that package, and only after proving the local copy IS the running package. You write a small helper that does the
proof and the copy, and you edit the build script to use it.

Words used below.
- "The build script" is `infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh`. Line numbers are the file's
  lines before your edit.
- "The helper" is a new file, `infra/aws/terraform/harvest/vendor_from_deployed.py`.
- "The deployed zip" is a local file holding the package the function runs now. On this machine it is
  `C:/tmp/ba20-r77-14a36147bd.zip`. You never type that path into the build script or the helper.
- "The four folders" are the zip entries whose names begin with `pyarrow/`, `pyarrow-16.1.0.dist-info/`, `rpds/` or
  `rpds_py-2026.6.3.dist-info/`. In the deployed zip they hold 132, 6, 4 and 5 files: 147 in all.
- "The live hash" is the text AWS returns as `CodeSha256` for the function `opal-amgt-scoped-api`: the sha256 of the
  running package, written in base64 (44 characters).

**File 1: the helper, `infra/aws/terraform/harvest/vendor_from_deployed.py` (new).** Standard library only. ASCII only.
Python 3.9 syntax. It imports none of: urllib, http, socket, ssl, ftplib, subprocess, boto3, botocore, requests, pip.

1. Command line: `--zip <path>`, `--expect-sha256 <base64 text>`, `--dest <folder>`, all three required. Use argparse,
   so `--expect-sha256=<text>` is accepted too.
2. Read the zip file in pieces and compute its sha256; write it in standard base64. If it is not exactly equal to the
   `--expect-sha256` text: print one line that begins `ERROR: sha256 mismatch` and states both values, write nothing,
   do not create the dest folder, and exit with a non-zero code. There is no other way past this step: no option skips
   it and nothing is fetched.
3. If the dest folder exists and holds anything, print a line beginning `ERROR:` and exit non-zero, writing nothing.
4. List the zip's file entries under the four folders. The four folder names are typed in the helper exactly as above,
   versions included. If any of the four has no entry, print a line beginning `ERROR:` that names the missing folder,
   write nothing and exit non-zero. (A zip holding `pyarrow-17.0.0.dist-info/` and no `pyarrow-16.1.0.dist-info/` is
   refused here. That is intended: this helper serves these two versions only.)
5. Refuse (a line beginning `ERROR:`, nothing written, non-zero exit) if any of those entry names begins with a slash,
   holds a backslash or a colon, or has `..` as a path part.
6. Only then write each entry under the dest folder at its own relative path, in binary mode, the bytes exactly as the
   zip gives them. Write nothing else there. Entries outside the four folders are never written.
7. Print one line per folder with its file count, then one last line beginning `OK:` with the total. Exit 0.

**File 2: the build script.** Eight edits. Do not change any line not named here.

- S1. After line 123 (`python "$SCRIPT_DIR/gen_harvest_prefixes.py" --check`) and before the comment line that begins
  `# ---- VENDOR:`, insert these lines, with a comment line above them naming AMGT-bb-23:

      FUNCTION_NAME="opal-amgt-scoped-api"
      DEPLOYED_ZIP="${AMGT_DEPLOYED_ZIP:?AMGT_DEPLOYED_ZIP must name the deployed package zip on this box}"
      FROM_DEPLOYED="$TMP/from-deployed"
      LIVE_SHA="$("$AWS" lambda get-function-configuration --function-name "$FUNCTION_NAME" --query CodeSha256 --output text | tr -d '\r\n')"
      if [ -z "$LIVE_SHA" ] || [ "$LIVE_SHA" = "None" ]; then echo "ERROR: no live CodeSha256 was read for $FUNCTION_NAME"; exit 1; fi
      echo "DEPLOYED: live CodeSha256 $LIVE_SHA; local zip $DEPLOYED_ZIP"
      MSYS2_ARG_CONV_EXCL='--expect-sha256=' python "$SCRIPT_DIR/vendor_from_deployed.py" \
        --zip "$DEPLOYED_ZIP" "--expect-sha256=$LIVE_SHA" --dest "$FROM_DEPLOYED"

  What they do: the build stops at once when the environment variable `AMGT_DEPLOYED_ZIP` is not set; it reads the live
  hash itself, every run; it calls the helper, and because the script runs under `set -e` a non-zero exit from the
  helper stops the build before any pip command. `MSYS2_ARG_CONV_EXCL` keeps Git Bash from rewriting a hash that begins
  with a slash into a Windows path; keep it and keep the `--expect-sha256=` form with the equals sign.
- S2. Line 126 (`RPDS_PIN="rpds-py==2026.6.3"`) stays. Add a comment line above it saying it is now used only by the
  local-interpreter download near line 560.
- S3. Delete line 132 (`PYARROW_PIN="pyarrow==16.1.0"`). Replace the comment at lines 127-131 with a comment saying
  pyarrow 16.1.0 and rpds-py 2026.6.3 are copied from the deployed package by `vendor_from_deployed.py` and are never
  downloaded. Change line 133 to exactly:

      VENDOR_PINS="jsonschema==4.26.0 attrs==26.1.0 jsonschema-specifications==2025.9.1 referencing==0.37.0 typing_extensions==4.16.0"

  Lines 134-147 (the pip download of `$VENDOR_PINS` and the wheel hash print) stay as they are.
- S4. Line 149: add a fourth argument, so it reads `python - "$ROOT" "$ZIP" "$WHEELS" "$FROM_DEPLOYED" <<'PYEOF'`.
  Line 155: read it, `root, out, wheels, from_deployed = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]`.
- S5. Lines 240-244: replace the two constants `NATIVE_WHEEL_PREFIXES` and `NATIVE_WHEEL_TAGS` and their comment with
  one constant, `DEPLOYED_FOLDERS = ("pyarrow/", "pyarrow-16.1.0.dist-info/", "rpds/", "rpds_py-2026.6.3.dist-info/")`,
  and a comment saying these come from the deployed package. Leave lines 245-247 (`VENDOR_PRUNE`) exactly as they are.
- S6. Lines 430-437, inside the wheel loop: every wheel pip downloads must now be a pure one. Remove the `native` list
  and the admitted-native branch; a wheel whose name does not end `-none-any.whl` stops the build with a `FATAL:` line
  naming it. The rest of the loop (lines 438-448, the prune of each PURE wheel's members) stays.
- S7. Lines 449-455 (the block that demands exactly two native wheels and prints `VENDORED-NATIVE`): delete it. In its
  place, walk the folder `from_deployed`. For every file there: its zip name is its path relative to `from_deployed`
  with forward slashes; if that name does not begin with one of `DEPLOYED_FOLDERS`, or is already in `members`, `data`
  or `vendored`, stop with a `FATAL:` line; otherwise read the file in binary mode and store it, `vendored[name] =
  <its bytes>`. DO NOT pass these names through `VENDOR_PRUNE` or any other filter: every file the helper wrote goes
  into the zip unchanged. If the walk finds no file, stop with a `FATAL:` line. Then print one line beginning
  `VENDORED-FROM-DEPLOYED:` with the file count per folder. The text `expected exactly 2 admitted native wheels` must
  no longer appear anywhere in the script.
- S8. In the header comment, after the paragraph that ends "Any other non-pure wheel is refused." (line 71), add a
  short paragraph: since AMGT-bb-23 pyarrow and rpds-py are copied from the deployed package named by
  `AMGT_DEPLOYED_ZIP`, only when its sha256 equals the live CodeSha256 read at build time; there is no download for
  them; a version change of either goes back through intake.

**Rules.**
1. You do NOT run the build script, with or without `--build-only`. It cannot finish on this machine yet (the five
   other packages are not here) and it must not be tried.
2. You run no `pip download`, no `pip install`, and no command that fetches anything from the internet. You make no
   AWS write. The three check commands make one AWS read each at most; you make no other AWS call.
3. Neither file gains any way to obtain pyarrow or rpds-py other than the copy from the deployed zip: no fallback
   download, no second source, no option that skips the hash comparison.
4. You do not edit lines 544-741 of the build script (the isolated runtime check, the content diff, the upload). The
   pip download near line 560 stays: it is for the build machine's own interpreter and never reaches the zip.
5. You do not edit `content_diff.py`, `upload_verified.sh`, `gen_harvest_prefixes.py`, any `.tf` file, or anything
   under `lib/`.
6. No machine-specific path in either file: the zip's location reaches the script only through `AMGT_DEPLOYED_ZIP`.
7. ASCII only, LF line endings. The helper must pass `bash .tools/commit-gate.sh infra/aws/terraform/harvest/vendor_from_deployed.py`.

Report: the three verdict lines, the file counts the helper printed for the four folders, and the line numbers of the
script at which the zip is required, the live hash is read, the helper is called and the first pip download sits (the
AC3 output prints them).

### 3. THE CRITERIA
- **AC1** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb23.py" --crit AC1; echo "exit=$?"`
  Expect: the helper, handed the deployed zip and the live CodeSha256, exits 0 and fills an empty folder with 147 of 147 files equal to the zip's entries byte for byte (132, 6, 4, 5; pyarrow 138 of 138, rpds 9 of 9) and nothing else; C1-C4 PASS; R78 BB23 AC1 SERVED: YES; and exit=0
- **AC2** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb23.py" --crit AC2; echo "exit=$?"`
  Expect: the helper stops with nothing copied on a wrong expected hash, on a copy of the zip with one byte changed inside a pyarrow member, and on a zip whose pyarrow dist-info is another version, while it exits 0 on the right hash, and the comparer reports the one flipped byte; P0 and N1-N4 PASS; R78 BB23 AC2 SERVED: YES; and exit=0
- **AC3** `cd "$(git rev-parse --show-toplevel)" && PYTHONPATH="$(pwd)" python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb23.py" --crit AC3; echo "exit=$?"`
  Expect: read from the script text, the pip pin list is the five pure pins, no pip download for the Lambda platform names pyarrow or rpds, the script requires the zip, reads the live CodeSha256 and calls the helper before any pip download, there is no other fetch route, the prune list removes 0 of the 147 deployed files, the packaging step is handed the filled folder, and bash -n passes; C1-C7 PASS; R78 BB23 AC3 SERVED: YES; and exit=0

Which clauses are build and which are bound. AC1: C1 is bound (the zip on disk is the running package; PASS at the base),
C2-C4 are build. AC2: N3 is bound (it tests the check's own comparer; PASS at the base), P0, N1, N2, N4 are build.
AC3: C5 and C6 are bound (PASS at the base), C1-C4 and C7 are build. Every criterion as a whole is build: all three read
NO at the base.

**What this cell does NOT prove.** The full build with no network is not this cell's proof: the five pure wheels are not
on this machine, so the script cannot run to a zip. Term 2 in the ruling's own words ("the two folders in the NEW ZIP
equal the deployed zip's") is read at bb-18, on the zip that build makes, by
`python "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round78/checks/r78_bb23.py" --compare-zip <the built zip>`
(expect `R78 BB23 COMPARE-ZIP EQUAL: YES`, 147 of 147). AC1 proves the same equality one step earlier, on the folder the
packaging step reads; AC3 C7 reads from the text that the packaging step takes that folder.

### 4. THE BASE DRY-RUN

AC1 and AC2 were run at HEAD `12fdfae38d`, AC3 (with its seventh clause) at `9c759c41fe`, 2026-10-07 about 17:1xZ. All
three read NO, each for the reason the act removes: the helper does not exist and the script still pins and downloads
the two packages. The four bound clauses PASS. C7 prints before C6.

```
### AC1
   deployed zip C:/tmp/ba20-r77-14a36147bd.zip: 41981131 bytes, sha256 MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=; entries under the four folders 147 [132, 6, 4, 5]
PASS C1 the zip's sha256 equals the live CodeSha256 zip MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg= live MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=
FAIL C2 the helper exists and exits 0 rc=None the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
FAIL C3 the filled folder equals the zip's entries byte for byte 0 of 147 equal; mismatched 0, missing 147, extra 0 ['pyarrow-16.1.0.dist-info/LICENSE.txt', 'pyarrow-16.1.0.dist-info/METADATA', 'pyarrow-16.1.0.dist-info/NOTICE.txt']
FAIL C4 the per-folder counts are the measured ones filled [0, 0, 0, 0] zip [132, 6, 4, 5] measured [132, 6, 4, 5]; pyarrow 0 of 138, rpds 0 of 9
R78 BB23 AC1 SERVED: NO
exit=1
### AC2
   deployed zip sha256 MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=; live CodeSha256 MkM9Kf37nmI+thEmZR+ij8ybbxGrHxqtsonjyI7N5eg=
FAIL P0 the helper exits 0 on the right sha and copies the files rc=None files 0 the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
FAIL N1 a wrong expected sha stops the helper and nothing is copied rc=None files 0 the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
FAIL N2 one changed byte inside a pyarrow member fails the sha gate byte 1560511 of the copy, inside pyarrow/__init__.py; copy sha256 fkdn26kQvDqPbF+0mruqSG2/sZO6CdvVVM9OTCkAgs4=; rc=None files 0 the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
PASS N3 the comparer reports the one flipped byte before the flip 147 of 147 equal, mismatched 0; after it 146 of 147 equal, mismatched ['pyarrow/libarrow.so.1601']
FAIL N4 a zip whose pyarrow dist-info is another version is refused, its sha being right rc=None files 0 the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
R78 BB23 AC2 SERVED: NO
exit=1
### AC3
FAIL C1 VENDOR_PINS expands to exactly the five pure pins 7 pin(s) ['attrs==26.1.0', 'jsonschema-specifications==2025.9.1', 'jsonschema==4.26.0', 'pyarrow==16.1.0', 'referencing==0.37.0', 'rpds-py==2026.6.3', 'typing_extensions==4.16.0']; beyond the five ['pyarrow==16.1.0', 'rpds-py==2026.6.3']; of the five absent []
FAIL C2 no pip download that names --platform names pyarrow or rpds pip download commands 2 at lines [135, 560]; with --platform 1; of those naming one of the two [135]
FAIL C3 the script requires the zip, reads the live CodeSha256 and calls the helper before any pip download AMGT_DEPLOYED_ZIP required at line None; CodeSha256 read at line None; helper called at line None (MSYS2_ARG_CONV_EXCL on the call: False); first pip download at line 135
FAIL C4 no other fetch route in the script or the helper fetch tokens in the script []; the helper infra/aws/terraform/harvest/vendor_from_deployed.py does not exist
PASS C5 the script's prune list removes nothing from the deployed four folders VENDOR_PRUNE ('pyarrow/include/', 'pyarrow/src/', '/tests/', '/testing/'); removed 0 of 147 []
FAIL C7 the packaging step is handed the filled folder and no longer demands two native wheels packaging step at line 149, handed $FROM_DEPLOYED: False; the two-native-wheels refusal still in the text: True
PASS C6 bash -n on the script exits 0 rc=0 
R78 BB23 AC3 SERVED: NO
exit=1
### --compare-zip C:/tmp/ba20-r77-14a36147bd.zip (not a criterion; the deployed zip against itself)
PASS Z1 the four folders of C:/tmp/ba20-r77-14a36147bd.zip equal the deployed zip's byte for byte 147 of 147 equal; mismatched 0, missing 0, extra 0 []
R78 BB23 COMPARE-ZIP EQUAL: YES
exit=0
```

### 5. `<paths>`

```
infra/aws/terraform/harvest/build-and-upload-scoped-amgt.sh
infra/aws/terraform/harvest/vendor_from_deployed.py
org/missions/D5/AMGT/AMGT_RESAPP/deliverables/<worker serial>/
org/missions/D5/AMGT/AMGT_RESAPP/surprise-channel/investigations/INVESTIGATION_v1.md
```

No test file is named: no test file in the repo reads the build script (one search of every `test*.py` for the script's
name, 0 files), the folder `infra/aws/terraform/harvest/` holds no tests folder of its own, and AC2 is the helper's test.

### 6. Risk and class

LOCAL. The cell edits one build script and adds one helper. It builds nothing, uploads nothing and writes nothing to
AWS. The served act is bb-18's build, upload and apply, under its own pair.

Worker class: `worker`. The estimate is about 60 lines for the helper and about 35 changed lines in the script, under the
light class's 100, but the script makes a served package and its Python block cannot be run on this machine before
bb-18, so nothing but careful reading stands between a slip in S6 or S7 and a failed build there.

### 7. Edges

- **After it: bb-18 (the redeploy).** bb-18's build must run with `AMGT_DEPLOYED_ZIP` naming the deployed zip, plus
  `PIP_NO_INDEX=1 PIP_FIND_LINKS=<the wheel folder>`, and reads `--compare-zip` on the zip it makes. bb-18's order
  needs those three variables in its invocation; they are not in this cell.
- **Before it: none.** No file of this cell's write set was seen in another drafted round-78 cell's path block
  (Groups A to E were not re-read for this; the issuer's cut checks the write sets).
- **The check is valid only until bb-18's apply.** After the apply the live CodeSha256 is the new package's, and
  `C:/tmp/ba20-r77-14a36147bd.zip` no longer equals it: AC1 C1 then reads FAIL and the helper refuses that zip, which
  is the ruling working. A re-run after the apply needs `R78_BB23_DEPLOYED_ZIP` set to the zip bb-18 built.
- **Every later build needs the then-deployed zip on disk.** The script deletes its own build folder on exit. The
  `--build-only` output of the build that gets deployed must be KEPT; it is the next build's `AMGT_DEPLOYED_ZIP`. If it
  is lost, the only copy is the function's code location, and taking it from there is a download, which Term 1 forbids
  as a fallback. That is a standing duty on whoever deploys, and it is written nowhere yet.
- **A build between an upload and its apply.** The live hash moves at the apply, not at the upload. A build run after
  an upload and before the apply still wants the OLD zip.
- **The first pip download now holds five pins, all pure.** After S6 any compiled wheel in the download folder stops
  the build, which is stricter than today.

### 8. Not measured, and questions for the issuer

- **Rule `content_diff.py`.** Line 729 of the build script runs it in both modes. It downloads the whole deployed
  package from the function's code location on every build (boto3 `get_function`, then `urllib.request.urlopen`). It
  is not a package index and it is Opal's own object, and it does not feed the two folders, so Term 1 is not broken by
  it. But it is a fetch from the internet on this machine during the build, and the same bytes are already on disk and
  hash-proven by the helper. Whether the new rule reaches it is the CTO's call; a one-line change could hand it the
  local zip. Not in this cell.
- **NOT exercised: the edited Python block of the script (S4-S7).** Nothing in this cell runs it. AC3 C7 reads two
  facts from the text; the first real run is bb-18's build. If S6 or S7 is wrong the build stops there with a `FATAL:`
  line; it cannot package a wrong pyarrow silently, because lines 514-515 and 537 still demand the members and
  `--compare-zip` reads the result.
- NOT measured: whether pip accepts `PIP_NO_INDEX=1 PIP_FIND_LINKS=<folder>` end to end (no pip command was run), and
  whether the five pure wheels or the Windows rpds-py wheel have arrived.
- NOT measured: `upload_verified.sh` was not read. It is sourced only after the `--build-only` exit at line 734, so a
  build-only run does not reach it.
- NOT measured: the `.tools/aws` shim's output for `--output text` (a trailing carriage return is assumed possible and
  S1 strips it). The check read the live hash through boto3, not through the shim.
- NOT measured: the helper on Python 3.9 or on Linux; the layer `opal-amgt-print-deps:1`; whether a module added this
  round imports a pyarrow file outside the 132 (bb-18's deployed route answers that).
- **The function name is typed once in S1** (`FUNCTION_NAME="opal-amgt-scoped-api"`). `content_diff.py` reads it from
  `scoped-amgt-api.tf` instead. The typed form is smaller; if the issuer wants one source, S1's `FUNCTION_NAME` line
  becomes `FUNCTION_NAME="$(python -c "import sys; sys.path.insert(0, sys.argv[1]); import content_diff; print(content_diff.function_name())" "$SCRIPT_DIR")"`.
- **The old pyarrow provenance sentence goes.** The comment at lines 127-131 says the pyarrow wheel's sha256 is
  "recorded on the NEVER-2 entry leg". After this cell no pyarrow wheel is downloaded; the provenance of the pyarrow
  bytes is the CodeSha256 the helper matched, which S1 prints (`DEPLOYED: live CodeSha256 ...`). bb-18's deploy entry
  should record that line in its place.
- The check's default zip path (`C:/tmp/ba20-r77-14a36147bd.zip`) is this machine's. It is in the check only, with the
  override `R78_BB23_DEPLOYED_ZIP`; a worker on this machine needs no override.
- The check expects the names the act gives: `AMGT_DEPLOYED_ZIP`, `FROM_DEPLOYED`, `vendor_from_deployed.py`,
  `--expect-sha256=`, `MSYS2_ARG_CONV_EXCL`, and the read of `CodeSha256` on one line with
  `get-function-configuration`. A worker who renames one fails AC3 C3 or C7; the act types them for that reason.
- AC2 N2 changes one byte in the stored (compressed) bytes of `pyarrow/__init__.py`, at byte 1,560,511 of a temporary
  copy of the zip. The copy is about 42 MB, lives under the system temp folder and is removed when the check ends.
