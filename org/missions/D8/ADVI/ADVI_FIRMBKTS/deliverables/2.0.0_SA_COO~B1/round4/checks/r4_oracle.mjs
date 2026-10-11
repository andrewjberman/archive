// ADVI_FIRMBKTS round 4: the ROUTER ORACLE for act 4's pre-flip read (the CTO's act-4 ADDENDUM 3), issuer 2.0.0_SA_COO~B1.
// Runs the router's OWN handler on one origin-request event per served class and prints the rewritten origin bucket and key.
// No AWS call, no network. Run with bun from the repository root:
//   bun org/missions/D8/ADVI/ADVI_FIRMBKTS/deliverables/2.0.0_SA_COO~B1/round4/checks/r4_oracle.mjs [--firm <id>] [--simulate-flip]
// --simulate-flip passes the registry's map with the firm's own bucket and the canonical list [that bucket], so the oracle can
// be rehearsed BEFORE the registry value moves; without it the router runs exactly as built from the tree (the act's read).
import { handleWithMap, handler, CANONICAL_PLATINUM_CLASSES } from "../../../../../../../../../infra/aws/lambda-edge/shared-advisor-router/index.mjs";
import { FIRM_BUCKET_MAP } from "../../../../../../../../../infra/aws/lambda-edge/_shared/firm-config.mjs";

const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const FIRM = opt("--firm", "49financial");
const SIM = args.includes("--simulate-flip");
const A = "/api/scoped/advisor-intelligence/";
const PLAT = CANONICAL_PLATINUM_CLASSES[0][0].replace(/^\//, ""); // "platinum/", read from the router's own table
const own = "opal-data-" + FIRM;
const domain = (b) => `${b}.s3.us-east-1.amazonaws.com`;
const ev = (suffix) => ({ Records: [{ cf: { request: {
  method: "GET", uri: A + suffix, querystring: "",
  headers: { "x-firm-id": [{ key: "X-Firm-Id", value: FIRM }], "x-user-tier": [{ key: "X-User-Tier", value: "internal" }] },
  origin: { s3: { domainName: domain(FIRM_BUCKET_MAP[FIRM] || own), region: "us-east-1",
    authMethod: "origin-access-identity", customHeaders: {} } },
} } }] });

// the nine served classes, each as the request suffix a viewer sends (the router's own table gives the rest)
const SUFFIXES = [
  PLAT + "accounts/", PLAT + "advisors/", PLAT + "clients/", PLAT + "firm/",
  "entities/accounts/", "entities/advisors/", "entities/clients/", "views/", "artifacts/",
];
const quiet = async (fn) => { const l = console.log, w = console.warn; console.log = () => {}; console.warn = () => {};
  try { return await fn(); } finally { console.log = l; console.warn = w; } };

const rows = [];
for (const s of SUFFIXES) {
  const e = ev(s + "t1/x.json");
  const r = await quiet(() => (SIM
    ? handleWithMap(e, { ...FIRM_BUCKET_MAP, [FIRM]: own }, [own])
    : handler(e)));
  const bucket = r && r.origin && r.origin.s3 ? r.origin.s3.domainName.replace(/\.s3\..*$/, "") : null;
  rows.push({ suffix: s, status: r && r.status ? String(r.status) : "pass", bucket, key: r && r.uri ? r.uri.replace(/^\//, "") : null });
}
console.log(JSON.stringify({ firm: FIRM, simulate_flip: SIM, classes_in_router_table: CANONICAL_PLATINUM_CLASSES.length, rows }));
