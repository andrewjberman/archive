"""Stream-count data rows in the data worksheet XML of an xlsx. Read-only; nothing extracted to disk.
usage: python -I count_rows.py <xlsx> [<xlsx> ...]
One JSON line per file: name, data sheet entry (largest worksheet part), row_open, row_empty,
nonempty_rows, data_rows (= nonempty rows minus the header row), dimension ref.
Matches are counted by ABSOLUTE start offset so a token straddling a read boundary is neither lost nor doubled."""
import json
import os
import re
import sys
import zipfile

OPEN = re.compile(rb'<(?:[A-Za-z0-9_]+:)?row[ >/]')
EMPTY = re.compile(rb'<(?:[A-Za-z0-9_]+:)?row\b[^>]*/>')
DIM = re.compile(rb'<(?:[A-Za-z0-9_]+:)?dimension\s+ref="([^"]+)"')
SHEET = re.compile(r'^xl/worksheets/sheet[0-9]*\.xml$')
OVERLAP = 64  # longest row token we need to see whole


def count_sheet(zf, entry):
    opens = 0
    empties = 0
    dim = None
    tail = b''
    base = 0
    counted_upto = 0
    with zf.open(entry) as fh:
        while True:
            chunk = fh.read(1 << 20)
            eof = not chunk
            buf = tail + chunk
            limit_abs = base + len(buf) if eof else base + len(buf) - OVERLAP
            if dim is None:
                m = DIM.search(buf)
                if m:
                    dim = m.group(1).decode()
            for m in OPEN.finditer(buf):
                a = base + m.start()
                if counted_upto <= a < limit_abs:
                    opens += 1
            for m in EMPTY.finditer(buf):
                a = base + m.start()
                if counted_upto <= a < limit_abs:
                    empties += 1
            if eof:
                break
            counted_upto = limit_abs
            cut = limit_abs - base
            tail = buf[cut:]
            base = limit_abs
    return opens, empties, dim


def main(paths):
    for p in paths:
        with zipfile.ZipFile(p) as zf:
            parts = [i for i in zf.infolist() if SHEET.match(i.filename)]
            parts.sort(key=lambda i: i.file_size, reverse=True)
            entry = parts[0].filename
            opens, empties, dim = count_sheet(zf, entry)
        nonempty = opens - empties
        rec = {"name": os.path.basename(p), "data_sheet": entry,
               "worksheet_parts": [i.filename for i in parts],
               "row_open": opens, "row_empty": empties, "nonempty_rows": nonempty,
               "data_rows": nonempty - 1, "dimension": dim}
        print(json.dumps(rec))


if __name__ == "__main__":
    main(sys.argv[1:])
