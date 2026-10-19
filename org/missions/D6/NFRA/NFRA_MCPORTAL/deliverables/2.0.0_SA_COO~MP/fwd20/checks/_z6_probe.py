"""Writes the SSM params file for z6.AC1: argv[1] = output path, argv[2..3] = window t0 t1 (ISO Z). One command: the
counts, in the gateway's own access log inside the window, of GET /api/admin/gateway/breakdown answered 200 and of a
count of the Control Plane page's four data routes (fabric boxes, overlap, gitstate, calls) each answered 200 at least once (0..4; only the verified owner reaches 200)."""
import json
import sys

since = sys.argv[2].replace("T", " ").rstrip("Z")
until = sys.argv[3].replace("T", " ").rstrip("Z")
log = ("TZ=UTC journalctl -u opal-gateway --no-pager -o cat --utc --since \"%s\" --until \"%s\"") % (since, until)
cmd = (log + " > /tmp/mp_z6_log.txt; "
       "echo \"breakdown_200=$(grep -cE '\"GET /api/admin/gateway/breakdown HTTP/1.1\" 200' /tmp/mp_z6_log.txt)\"; "
       "n=0; for r in boxes overlap gitstate calls; do grep -qE \"GET /api/admin/fabric/$r[ ?][^\\\"]*HTTP/1.1\\\" 200\" /tmp/mp_z6_log.txt && n=$((n+1)); done; echo \"control_plane_200=$n\"; "
       "rm -f /tmp/mp_z6_log.txt")
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
