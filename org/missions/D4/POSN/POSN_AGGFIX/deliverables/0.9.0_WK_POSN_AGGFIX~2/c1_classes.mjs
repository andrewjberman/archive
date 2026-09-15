/**
 * c1_classes.mjs -- POSN_AGGFIX.TO-C1-1: the four viewer classes, the URLs, and the claim sets.
 * Shared by GATE_UNIT_HARNESS_C1 (c1_gate_unit_harness.mjs) and LIVE_TIER_ARMS_C1 (c1_live_tier_arms.mjs)
 * so the unit rows and the live rows are driven by ONE definition.
 *
 * CLAIM SHAPE: read from the signer, infra/aws/opalinvest_dev/lambda/auth-handler/src/jwt.ts
 * generateAccessToken (sub, name, role, tier, firmId, userType when set, advisorKey/advisorName/
 * advisorRole/advisorId for a partner identity, firmRole when set, iss 'opal-portal-auth',
 * aud 'opal-portal-api'; RS256; no keyid). The signer derives tier as 'internal' for opal-capital and
 * 'advisor' for everyone else, so it never mints a 'client' tier: the client class below carries
 * tier 'client' deliberately, the value the proxy docstring's "blocks client tier" names, with no
 * advisor identity (a row records that the signer's tier space has no client member).
 */

export const KEY = "json/positioning/opal_aggregate.json";
export const AGG_URLS = [
  "/api/general/positioning/opal_aggregate.json",
  "/api/general/json/positioning/opal_aggregate.json",
];
export const CONTROL_URL = "/api/general/positioning/positioning_data.json";
export const MODEL_URL = "/api/general/positioning/model.json";
export const AMENDMENT_URLS = [
  "/api/general/positioning/opal%5Faggregate.json",
  "/api/general/positioning/opal%5faggregate.json",
  "/api/general/json/positioning/opal%5Faggregate.json",
  "/api/general/positioning/opal_aggregate.json?v=1",
  "/api/general/positioning//opal_aggregate.json",
];
export const ENCODED_URLS = AMENDMENT_URLS.slice(0, 3);

export const ISSUER = "opal-portal-auth";
export const AUDIENCE = "opal-portal-api";

export const CLASSES = {
  opal: { sub: "qa-posn-aggfix-opal", name: "QA POSN_AGGFIX Opal staff", role: "user", tier: "internal",
    firmId: "opal-capital" },
  dev: { sub: "qa-posn-aggfix-dev", name: "QA POSN_AGGFIX Dev", role: "user", tier: "advisor",
    firmId: "49financial", userType: "Dev" },
  advisor: { sub: "qa-posn-aggfix-advisor", name: "QA POSN_AGGFIX advisor", role: "user", tier: "advisor",
    firmId: "49financial", advisorKey: "qa-posn-aggfix-advisor", advisorName: "QA POSN_AGGFIX advisor",
    advisorRole: "implementor", advisorId: "qa-posn-aggfix-advisor" },
  client: { sub: "qa-posn-aggfix-client", name: "QA POSN_AGGFIX client", role: "user", tier: "client",
    firmId: "49financial" },
};
export const CLASS_ORDER = ["opal", "dev", "advisor", "client"];
export const ADMITTED = new Set(["opal", "dev"]);

export function claimsFor(cls, iat) {
  return { ...CLASSES[cls], iss: ISSUER, aud: AUDIENCE, iat, exp: iat + 300 };
}

export function splitUrl(url) {
  const q = url.indexOf("?");
  return q === -1 ? { uri: url, querystring: "" } : { uri: url.slice(0, q), querystring: url.slice(q + 1) };
}
