# HVST-aj-6 -- NopeCHA browser extension: source record (stage 1)

Authorization: whitelist row VEW-1 (`org/ref/VENDOR_EGRESS_WHITELIST.yaml`; Andrew-direct 2026-10-02 ~13:08Z "nopeCHA is
permanently whitelisted for egress"). Downloaded 2026-10-02 ~17:1xZ from NopeCHA's own official release only.

| Field | Value |
|---|---|
| Official release page | https://github.com/NopeCHALLC/nopecha-extension/releases (reached from NopeCHA's documented link https://nopecha.com/github/release, HTTP 302) |
| Documentation | https://developers.nopecha.com/guides/extension_advanced/ ("Automation build": settings are the `nopecha` object at the bottom of `manifest.json`; key in `nopecha.key`) |
| Release / version | tag `0.6.1` (stable, published 2026-06-11T13:19:39Z); manifest `version` 0.6.1, manifest_version 3 |
| Asset | `chromium_automation.zip`, 657104 bytes |
| URL | https://github.com/NopeCHALLC/nopecha-extension/releases/download/0.6.1/chromium_automation.zip |
| sha256 | `92ebe154bd34433b4a36e6b2df33006fa6acb19a1b81031a0acb5b72be5e025a` |
| sha256 check | computed locally with `sha256sum` = the digest GitHub's release API lists for the asset (`sha256:92ebe154...e025a`) |
| Not taken | 0.6.2-rc.2 (prerelease, 2026-08-20); the graphical `chromium.zip`; any non-NopeCHA source |

## Cache (the one main-tree write)

`C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest/extensions/nopecha/` (gitignored by `.gitignore:288 .runtime/`):

- `pristine/` -- the zip unpacked as shipped (29 entries: `manifest.json`, `assets/`, `icon/`); `nopecha.key` is the empty string.
  Unpacked by `lib/opal_data_harvest/nopecha_extension.install_pristine`, which refuses any zip whose sha256 is not the one above.
- `prepared/` -- written by `nopecha_extension.prepare` at run time: a copy of `pristine/` whose `manifest.json` carries the key
  (`nopecha.key`, from Secrets `nopecha/api-key`, the secret the CRO's `ft_harvest_session.py` reads) with
  `hcaptcha_auto_open` and `hcaptcha_auto_solve` true. The key therefore lives only in this gitignored directory.

The zip itself is not in the repo or the cache (held only in the worker's untracked `.scratch/`). No binary is committed.

## Loading (measured, row AMGT_HARVST-Z-W90-S18)

Installed Chrome is 154.0.8037.97. `--load-extension` loads nothing there, and `--disable-extensions-except` makes the extension
answer ERR_BLOCKED_BY_CLIENT. The prepared directory loads through CDP `Extensions.loadUnpacked` under
`--enable-unsafe-extension-debugging` (extension id `dknlfmjaanfblgfdfebhijalfmhmjjjo`, service worker running).
