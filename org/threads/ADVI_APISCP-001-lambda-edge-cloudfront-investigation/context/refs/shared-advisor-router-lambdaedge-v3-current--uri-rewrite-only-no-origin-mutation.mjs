/**
 * Lambda@Edge: Shared Advisor Intelligence Router
 * Purpose: Rewrite /api/scoped/advisor-intelligence/* to S3 path
 * Trigger: origin-request
 *
 * Note: Auth is handled by auth-validator-edge on viewer-request
 *
 * v2: renamed /api/shared/ -> /api/scoped/ (API path restructure 2026-02-25)
 * v3: origin migrated from opal-data-portal-v2 to opal-data-bd
 *     rewrite target changed from /json/advisor-intelligence/ to /gold/
 */
export const handler = async (event) => {
  const request = event.Records[0].cf.request;

  // /api/scoped/advisor-intelligence/* -> /gold/*
  if (request.uri.startsWith("/api/scoped/advisor-intelligence/")) {
    const originalUri = request.uri;
    request.uri = request.uri.replace("/api/scoped/advisor-intelligence/", "/gold/");
    console.log(`Scoped advisor rewrite: ${originalUri} -> ${request.uri}`);
  }

  return request;
};
