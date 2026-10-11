import hashlib
import os
os.chdir("/opt/opal-gateway")
MD5 = """d41d8cd98f00b204e9800998ecf8427e  app/__init__.py
9604aa77bda0ae8e9a36a57498eb97e8  app/access_state.py
3c1ae7a2c409c1c5111c93cbb89f863f  app/account_ref.py
012e661390c27ab902d6d19d6b061af3  app/admin_api.py
cbcb35cad0514c8bd41c73823cbd902d  app/admin_fabric.py
9aaa782a1e9dd315cd1e2a173cba9c26  app/admin_fabric_calls.py
09b8631aed0c6ed97fb93984fb6cb5ce  app/admin_fabric_gitstate.py
6e0d547dc7272f620cc5f5ac63195232  app/admin_fabric_overlap.py
b8dca6e9b8345a148e632aab9f8d304d  app/admin_grants.py
e01e882df6cc5f915202cba51f1f54b6  app/admin_refusals.py
35ed4a1565e4b1b278c3e0a6dd228285  app/admin_tenants.py
74535f62ca6c51a51a2bf5ad532748c7  app/asker_scope.py
fbba53361a4018b460c6825828cec374  app/audit.py
f3f086d89146aae4d840aec71dea25dd  app/blast_cap.py
bf22fd17169b3e20816862cf7938c871  app/blocklist.py
0f608bb14ed47423a36b36206ca94669  app/browser_oidc.py
00b73d4ca1a7afe9473c7623daeefd58  app/config.py
f4949e7d72d695fd917ac6ac8034454f  app/context.py
784fe5031dc4d3d68c25c76bdac22466  app/data_entitlement.py
feb0cf868acc33fe1ba5a88ac9bcfe78  app/destructive_ops.py
74f8843ea829b520ddf7db436f9fe52d  app/download_routes.py
ae689b825d6ae3722cf183862c0603c2  app/entitlements.py
0eee173a240340455e8e93017aa04f17  app/entity_resolution/SCAFFOLD.md
a803154a45725ded61164ea84ff1bcd5  app/entity_resolution/disposition_contract.py
a3402e3973e3360466a33f9c5420d016  app/entity_resolution/exercise_disposition_contract.py
64a7434537323ac6621b4ca1db35b2f7  app/entity_resolution/resolver_skeleton.py
b20b12a07f31355ea38e6912d0e5fffe  app/firm_role.py
3cfaf4d58ddf0d4f1d855c6a7d83745d  app/gen_rivalfunds_location.py
6e2fb9c51806cee05b003657d384cec5  app/graph.py
6b583540336c13d03095b9262c1d78ac  app/graph_read.py
303cff4df963ff9713ce727cfcd9a884  app/graph_scope_map.py
18a9df3652978c9f970f467d1dbd814f  app/graphql_plumbing/DESIGN.md
2d671de665769a24ca47ea90edf62d66  app/graphql_plumbing/__init__.py
bcfb89a944ee4607d596dab2f7a23053  app/graphql_plumbing/catalog_gate.py
0fc6bb1cf64633bc64441fd2c8f18def  app/graphql_plumbing/exercise_catalog_gate.py
332b288fd6c84c1e93572de093662759  app/guard.py
78d355fd5e0a5c1fe99f45a3f1296c66  app/identity.py
314d8430b23f2ec90b46d909123b245d  app/identity_scope.py
f8925a03de84c8362052a5badaa69a8a  app/integrations/__init__.py
69bc81984f5d23192e89fa94c1db881f  app/integrations/base.py
b364446918f5245a8d525c5474a8f5a7  app/integrations/blackdiamond/__init__.py
9e3e90d32cf92395650e2e1760e804b7  app/integrations/blackdiamond/integration.py
e975c500999959cf81ae8591823e760e  app/integrations/globgrph/__init__.py
35d9d2853de3117ef7e80dd30f940fc2  app/integrations/globgrph/integration.py
e422142acb024e6f72d0d8eeb5d2f8bf  app/integrations/opal_discover/__init__.py
34f36796d6b19eebe17d715c7ae7c041  app/integrations/opal_discover/integration.py
35d0e9f933bd92ed048e2b2f13bec44e  app/integrations/opal_portal/__init__.py
d28d856b74cf4d60cb9d2e149cec7967  app/integrations/opal_portal/integration.py
8803d0c142171e48522a596fe6b337ba  app/integrations/portal_index/__init__.py
ffac4cbf24e44469e639defbad9514c9  app/integrations/portal_index/integration.py
6499690c3bfca49becf3811ca7b05403  app/integrations/registry.py
3554bd462adde2000bde4003930e0a2d  app/integrations/schwab/__init__.py
38d2e87af341443a68f80f458a8b4b95  app/integrations/schwab/aws_roles.py
7944327d0bba500b9498b9767301748e  app/integrations/schwab/catalog.py
17d254b5ad4b77c9ba61ef0d6e732020  app/integrations/schwab/cursor.py
91ace8a27e64a00b4f0ed8c5d8b047d0  app/integrations/schwab/datasets.json
efcc3ebdfa2fe64d1649c2f89cf963d1  app/integrations/schwab/engine.py
e16e540eb4bb2a4d1d5b59d68b46f46c  app/integrations/schwab/envelope.py
c9943e7840e2e1ea2cb97df75feccf90  app/integrations/schwab/export.py
e79398bc0c21b17e94467fd6ba108207  app/integrations/schwab/integration.py
f9ba1d084cc5b3ede117203685e6aeee  app/integrations/schwab/query.py
7ecdf64b8f7f12a4f41f328025009b0a  app/integrations/schwab/semantics.py
13e40f1d2a9d5e09aa6a0910c27d6459  app/integrations/ycharts/__init__.py
d984f11b6367d9b409565e3bb27fdd4e  app/integrations/ycharts/client.py
a239bd493f50e63fe1e807835b20e8bb  app/integrations/ycharts/integration.py
653fbc8a664c0066b3035d5548fc5382  app/internal_role.py
1be54a93cbe66ba4d772d775d741110e  app/mail_route.py
1814b3703dc38e99b6b5845b44d5ff58  app/mock_graph.py
903cf0134b567f49f1c163575db58338  app/ms_ingest.py
f5234e8ebaa4897cbb5d56c23e851319  app/oauth_as.py
72a721d585f9e6f3bd10002fcf90d5d7  app/org/mcp/agent_telemetry/0.7.0_AE_CloudOps.jsonl
8704a7d3f14bc423a1f386cb4b302e5f  app/otp.py
a9c2ac2ba17e5e3a5d3b465e8420e1f0  app/owner_gate.py
4a1d8ec3cbe672cf490adfcf1b875404  app/query_v0.py
dcc62bf05fb1f53289121e035e834187  app/ratelimit.py
7e9e40bb185f266aa293a7d29ad67e6d  app/refs/DATA_CATALOG.yaml
09d6d8196f2b8bb645d2cef42a4baa5c  app/refs/fabric_boxes.json
ccc3efbca9e9ef3c1f08bb6d52f26800  app/refs/overlap_rules.json
0c1381a28ee860808556152b1be5e2c2  app/revocation.py
4e570ca9a8423a1e5885574c20f3889f  app/rivalfunds_location.json
148edfdbefb75406937fb9ebb51927ca  app/rivalfunds_view.py
31c9395469b10f30beeecc9c05c4bbf5  app/schwab_audit.py
bd6c349f9faa62e2a5e6781e6147d03d  app/sender_gate.py
037fd3a8f9bb657a8ba63aa8d859496f  app/server.py
2ffba4cd8d79d1c66240c86fe14c76f3  app/sprint_view.py
465f9fcb3550a499507686d7bfe73734  app/ssavail_contract.py
8a6208d3fd56b9838dd204a3bf0b0200  app/static/schwab_download/index.html
1869ef212742171be3cf8f837514b1c9  app/static/yearinreview/index.html
52753763e8c433efb8a72da9f8c1f752  app/taxsma_workbook.py
a3e14f8d20a04ae9fbbe252ef91930c8  app/teams_format.py
51784fbeb4de304e8e531d7b82a061e3  app/teams_route.py
52c6c73fdb5717212dfa71efac8f1c86  app/tenant_registry.py
c1f6390f916c2fbe6c1c21ee986a959a  app/tests/test_rivalfunds_view.py
5626d65c04b74a505f57d95b24ba4d5c  app/tier.py
a99942f02a4898cfa296b50f23324b3e  app/token_broker.py
fe0556c3b6caa623f68d118d52d3f959  app/tools.py
a7e5e68be5132158923e104eca216e57  app/transcript_route.py
0d26f064cb41c83f63f9bcb8bd5907a8  app/yearinreview_view.py
46b7c391f04ad09c91db2b7c15c6b086  deploy/NFRA_OPLGTW_CONTRACT.json
f4fed5cfd2a62a9471846d73fcf58823  deploy/mail_sender_domain_table.txt
3074d36bb77962c8c831448c696f9acb  deploy/mail_sender_table.txt
0c5f4d11ed95b3b8ce49467a827ea4bf  deploy/opal-gateway.service
fbe94252f6ef5bbf4524892af1fe0267  identity_tool_allowlist.txt
bc854942debf056b3c7d38342c036f29  requirements.txt
"""
want = [ln.split("  ", 1) for ln in MD5.strip().split("\n") if ln.strip()]
bad = []
for h, f in want:
    try:
        got = hashlib.md5(open(f, "rb").read()).hexdigest()
    except OSError:
        got = "ABSENT"
    if got != h:
        bad.append(f)
print("MD5 listed %d identical %d mismatch %d %s" % (len(want), len(want) - len(bad), len(bad), bad))
extra = []
names = set(x[1] for x in want)
for root, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if d not in (".venv", "__pycache__", "node_modules")]
    for f in fs:
        p = os.path.join(root, f)[2:].replace(os.sep, '/')
        if not (p.startswith("app/") or p.startswith("deploy/") or p.startswith("dashboard/")
                or p in ("requirements.txt", "identity_tool_allowlist.txt")):
            continue
        if p.endswith(".pyc") or "__pycache__" in p:
            continue
        if p not in names:
            extra.append(p)
print("HOST_ONLY_FILES %d %s" % (len(extra), sorted(extra)))
