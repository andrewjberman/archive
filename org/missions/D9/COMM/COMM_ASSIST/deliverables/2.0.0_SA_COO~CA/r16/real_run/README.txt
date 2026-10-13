MUSE READER FOLDER -- what is waiting on Andrew
=================================================

This folder is refreshed from AWS by a scheduled job on dell2. Read it as plain files.

FILES (four sources, one file each, plus the index and this note)
  open_calls.json     the open calls of every box (the cluster copies in the cloud)
  drafts.json         every Teams chat draft waiting for Andrew's 1 or 0
  eod_today.json      today's End of Day draft, if one is waiting
  sprint_today.json   the objects listed for today's sprint report (names and sizes, no bodies)
  INDEX.json          one entry per source: status, read_at, last_good_at
  README.txt          this note

KEYS IN EACH SOURCE FILE (six)
  source        the source's name, the file name without .json
  read_at       when this run read the source (UTC, ends in Z)
  status        ok, absent or unreadable (see below)
  last_good_at  the last time this source was read ok (UTC, ends in Z); carried forward when a later read fails
  error         null, or the first 200 characters of the reason the read did not succeed
  items         the list of what was found; null unless status is ok

THE THREE STATUSES
  ok          the source was read. items is the complete list. An empty list is a true empty, said at read_at.
  absent      the source was reached, but the thing is not there yet today (for example, no End of Day draft yet).
              items is null.
  unreadable  the source could not be read. items is null; last_good_at says when it was last read ok.

absent and unreadable are never an empty list.

INSIDE open_calls.json a row whose state is ABSENT names a box that has no cluster copy of its open calls yet.
Rows whose state is OPEN are open calls. Closed calls are not listed.

Email addresses are shown as [address withheld]. No key, token or password is ever written here.
