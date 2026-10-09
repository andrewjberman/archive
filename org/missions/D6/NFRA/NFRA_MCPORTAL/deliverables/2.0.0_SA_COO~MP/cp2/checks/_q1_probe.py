"""Writes the SSM params file for q1.AC1: argv[1] = output path, argv[2..3] = window t0 t1 (ISO Z). One command: the count
of POST /api/admin/fabric/calls/close answered 202 in the gateway's own access log inside the window."""
import json
import sys

since = sys.argv[2].replace("T", " ").rstrip("Z")
until = sys.argv[3].replace("T", " ").rstrip("Z")
cmd = ("TZ=UTC journalctl -u opal-gateway --no-pager -o cat --utc --since \"%s\" --until \"%s\" "
       "| grep -cE '\"POST /api/admin/fabric/calls/close HTTP/1.1\" 202'") % (since, until)
with open(sys.argv[1], "w", encoding="utf-8") as fh:
    json.dump({"commands": [cmd]}, fh)
