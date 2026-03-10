/**
 * Lambda@Edge: Auth Validator
 * Purpose: Validate JWT tokens for ALL routes except /auth/* and OPTIONS preflight
 * Trigger: viewer-request on CloudFront distribution EVTSA9VEHNZVH (opalinvest.dev)
 *
 * This is the SINGLE centralized auth gate — universal blacklist model.
 * Downstream Lambdas never parse JWTs — they read the injected X-User-* headers.
 *
 * JWT claims (from portal_authorizer): sub, name, tier, role, firmId, officeId, regionId, userType
 * Injected headers: X-User-Email, X-User-Name, X-User-Tier, X-User-Role, X-Firm-Id, X-User-Type, X-Origin-Verify
 *
 * Pass-through (no auth):
 *   /auth/*   - Login, signup, token refresh endpoints
 *   OPTIONS   - CORS preflight
 *
 * v6: whitelist -> blacklist universal gate (API path restructure 2026-02-25)
 * v7: stop stripping Authorization header — API Gateway authorizer needs it for enrichment (2026-03-01)
 */
import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";
import jwt from "jsonwebtoken";

// Cache JWT public key for 5 minutes (avoid Secrets Manager call on every request)
let cachedPublicKey = null;
let cacheExpiry = 0;

export const handler = async (event) => {
  const request = event.Records[0].cf.request;
  const uri = request.uri;

  // Pass through: auth endpoints (login/signup/refresh) and CORS preflight
  if (uri.startsWith("/auth/") || request.method === "OPTIONS") {
    return request;
  }

  try {
    // Extract JWT from Authorization header
    const authHeader = request.headers.authorization?.[0]?.value;
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
      return unauthorized("Missing or invalid Authorization header");
    }

    const token = authHeader.substring(7);

    // Get public key from Secrets Manager (cached)
    if (!cachedPublicKey || Date.now() > cacheExpiry) {
      const client = new SecretsManagerClient({ region: "us-east-1" });
      const response = await client.send(
        new GetSecretValueCommand({ SecretId: "opal/auth/jwt-public-key" })
      );
      cachedPublicKey = response.SecretString;
      cacheExpiry = Date.now() + 300000; // 5 min
    }

    // Verify JWT signature and expiration
    const payload = jwt.verify(token, cachedPublicKey, { algorithms: ["RS256"] });

    // Inject user context headers for downstream Lambdas.
    // Claim names match portal_authorizer JWT payload.
    request.headers["x-user-email"] = [{ key: "X-User-Email", value: payload.sub || "" }];
    request.headers["x-user-name"]  = [{ key: "X-User-Name",  value: payload.name || "" }];
    request.headers["x-user-tier"]  = [{ key: "X-User-Tier",  value: payload.tier || "unknown" }];
    request.headers["x-user-role"]  = [{ key: "X-User-Role",  value: payload.role || "user" }];
    request.headers["x-firm-id"]    = [{ key: "X-Firm-Id",    value: payload.firmId || "" }];
    request.headers["x-user-type"]  = [{ key: "X-User-Type",  value: payload.userType || "" }];
    request.headers["x-origin-verify"] = [{ key: "X-Origin-Verify", value: "cloudfront" }];

    console.log(`Auth OK: user=${payload.sub} tier=${payload.tier} path=${uri}`);
    return request;

  } catch (error) {
    console.error(`Auth FAILED: path=${uri} error=${error.message}`);
    return unauthorized("Invalid or expired token");
  }
};

function unauthorized(message) {
  return {
    status: "401",
    statusDescription: "Unauthorized",
    headers: {
      "content-type": [{ key: "Content-Type", value: "application/json" }],
      "access-control-allow-origin": [{ key: "Access-Control-Allow-Origin", value: "*" }],
      "www-authenticate": [{ key: "WWW-Authenticate", value: "Bearer" }]
    },
    body: JSON.stringify({ error: message })
  };
}
