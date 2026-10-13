"""Writes the SSM params file for z6.AC1: argv[1] = output path, argv[2..3] = window t0 t1 (ISO Z). One command: the
counts, in the gateway's own access log inside the window, of GET /api/admin/gateway/breakdown answered 200 and of a
direct GET /control-plane answered 200 (only the verified owner reaches 200 on either)."""
import json
import sys

since = sys.argv[2].replace("T", " ").rstrip("Z")
until = sys.argv[3].replace("T", " ").rstrip("Z")
log = ("TZ=UTC journalctl -u opal-gateway --no-pager -o cat --utc --since \"%s\" --until \"%s\"") % (since, until)
cmd = (log + " > /tmp/mp_z6_log.txt; "
       "echo \"breakdown_200=$(grep -cE '\"GET /api/admin/gateway/breakdown HTTP/1.1\" 200' /tmp/mp_z6_log.txt)\"; "
       "echo \"control_plane_200=$(grep -cE '\"GET /control-plane HTTP/1.1\" 200' /tmp/mp_z6_log.txt)\"; "
       "rm -f /tmp/mp_z6_log.txt")
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
