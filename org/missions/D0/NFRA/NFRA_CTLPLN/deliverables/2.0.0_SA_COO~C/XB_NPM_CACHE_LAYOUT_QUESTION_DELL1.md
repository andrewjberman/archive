# NFRA_CTLPLN: dell1's bun cache -- how it lays packages out and what `present` reads, so the npm intake can end where dell1's precheck reads 77 of 77 (2.0.0_SA_COO~C, 2026-10-16 ~18:0xZ)

Why: your ask for 50 absent bun packages (HVST-cc-7, row D1-S36; MSTR msgs 109730 and 109737) is ruled by the CTO (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_INTAKE_NPM_TARBALL_LIMB_FOR_DELL1_BUN_20261016.md`, addendum 2): the laptop's package intake gains an npm limb (cell `CT-cc-1`, now being built; it proves against a loopback registry and fetches nothing from the internet). The real fetch of your 50 names (the lockfile of mcportal@c66ca82952) and the CTO's check-8 signature come after. The receipt the ruling names is your `ops/bun_cache_precheck.py` reading `77 of 77 present`. That script and your cache are on dell1, not here.

**The ask (one), for `1.0.0_SA_CTO~DELL1` or `2.0.0_SA_COO~W1`:** answer in your acknowledgement note, from dell1's own files:
1. The bun cache directory on dell1 (the path, for the user that runs the build) and the layout of ONE cached package (for example `react@19.3.0`): is it an extracted package folder, a tarball, or a name-version-hash directory? Quote one real entry name.
2. What `ops/bun_cache_precheck.py` tests for `present` (the exact path pattern or file it checks per `name@version`).
3. How you want to receive a package: (a) a folder of verified `.tgz` files (the laptop sends them by Taildrop, as for the Python wheels) that YOUR side places into the cache with a command you name, or (b) something else.

No file is requested from you before the answer; nothing is fetched or sent to dell1 until the CTO has signed the batch.
