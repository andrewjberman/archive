# KIT_TERRAFORM_PACK_RECORD -- NFRA_CTLPLN.TO-CT-k-2 AMENDMENT 4

Worker `0.9.0_WK_NFRA_CTLPLN~13`, 2026-10-07 (pack cut ~12:0xZ, UTC). Branch `wk-NFRA_CTLPLN-13`. Nothing was sent anywhere, nothing was
downloaded, the pack is outside every git tree and is not committed. Push state of this record: LOCAL on the worker branch.

## The pack

- Path: `C:/tmp/kit-terraform-pack-20261007` (drive prefix derived from the box; `git -C /c/tmp rev-parse` reads "not a git repository").
- Cut with: `python org/devices/kit_terraform_providers.py pack --out C:/tmp/kit-terraform-pack-20261007 --include-unlocked`
- Pack line: `TF-PACK out=kit-terraform-pack-20261007 providers=3 files=6 bytes=1581246835 binary=1.15.8 binary_bytes=119934088 linked=7 copied=0 not_on_box=0 h1_mismatch=0 ok=True`
- Total on disk: 9 files, 1,701,184,015 bytes (6 provider files 1,581,246,835 + binary 119,934,088 + MANIFEST.json + terraform.rc.snippet).
- HARD-LINKED, not copied: link-count histogram over the 9 files is {2 links: 7 files, 1 link: 2 files}; the 7 are the six provider files and the
  binary, the 2 singles are the manifest and the snippet this tool wrote. No extra disk for the 7 (plugin cache and WinGet are on the same C: volume).
  Free space before 41 GB, after 39 GB (the 2 GB movement is other activity on the box; the link counts are the evidence). The 10 GB floor was never in play.

| Provider | Version | Locked by | Binary (bytes) | h1 vs lock |
| --- | --- | --- | --- | --- |
| hashicorp/aws | 5.100.0 | nfra-ctlpln-identity and the other locked roots | 718,820,352 | MATCHES-LOCK |
| hashicorp/aws | 6.67.0 | none (unlocked: nfra-ctlpln-agentbus declares `~> 6.0`, no lock file) | 843,379,848 | no hash to check |
| hashicorp/archive | 2.8.1 | none (unlocked: estate-report declares `~> 2.4`) | 18,996,360 | no hash to check |

## The Terraform binary

- Resolved by `.tools/safe-apply.sh`'s own order: `$SAFE_APPLY_TERRAFORM` (unset here), then the sibling `<base>/.tools/terraform.exe` (ABSENT in the
  base checkout `C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/`, and ABSENT in this worktree's `.tools/`; it is gitignored by `.tools/*.exe`), then PATH.
  Source = PATH (step 3): `C:/Users/AndrewBerman/AppData/Local/Microsoft/WinGet/Packages/Hashicorp.Terraform_Microsoft.Winget.Source_8wekyb3d8bbwe/terraform.exe`.
- Version 1.15.8, platform windows_amd64, 119,934,088 bytes, SHA-256 `6eb0a1cb89344c97ccf2928ddc2d7a6cb71a1837b7ecccfd5991466b6d751e03`.
- A second binary of another version exists on this machine: `C:/Users/AndrewBerman/Desktop/ajb_workspace/.tools/terraform-1.9.8-aside.exe` (91,104,424 bytes,
  version 1.9.8). The wrapper does NOT resolve it (its name is not `terraform.exe`), so it is not carried and the three sources do not disagree.
- Self-check (the pack's binary hashed against the manifest, then executed): `TF-VERIFY from=kit-terraform-pack-20261007 files=6 verified=6/6 mismatched=0 missing=0 unlisted=0 binary=ok run=ok installed=- ok=True`
  (with `BINARY-RUN version=1.15.8 matches the manifest (platform windows_amd64)`).

## Commands another machine runs, in order

`<P>` is where the pack landed on that machine; `<W>` is that machine's workspace (base checkout). Run from `<W>`.

1. Verify the pack (hashes every file against the manifest, then, only if all match, runs the packed binary's `version -json` and compares):
   `python org/devices/kit_terraform_providers.py verify --from <P> --run-binary`
2. Install the binary where the wrapper finds it with no baked path (the sibling is the wrapper's second choice and beats PATH; gitignored):
   `python org/devices/kit_terraform_providers.py verify --from <P> --install-binary <W>/.tools/terraform.exe`
   (it re-verifies the copy's SHA-256 and refuses to overwrite a different file there; the verify output prints this exact path).
3. Write the CLI config that reads the mirror and never the registry (merge by hand if the file exists):
   `python org/devices/kit_terraform_providers.py verify --from <P> --write-config "$APPDATA/terraform.rc"`
4. Read back (version through the wrapper's resolution; then init with the mirror and one no-op plan; needs that machine's AWS identity and the state backend):
   `python org/devices/kit_terraform_providers.py readback --root <W>/infra/aws/terraform/<root> --from <P>`
   Last line `TF-READBACK version=<v> init=<ok|fail> plan_exit=<0|1|2> ok=<True|False>`; plan_exit 2 means changes are present (loud, not a kit failure).

No command above contains a URL; the kit sets `CHECKPOINT_DISABLE=1` for every terraform it runs (row NFRA_CTLPLN-W13-S8).

## What was not done

- `readback` part (b) was never run against a real root (needs a Dell's identity and backend): it ran on temporary local-backend roots only (test case 10).
- The pack was not sent, and nothing was installed on any box.
- A fresh root with only locals and an output reads plan_exit=2, not 0 (row NFRA_CTLPLN-W13-S7); the test seeds the state by hand to read 0.
