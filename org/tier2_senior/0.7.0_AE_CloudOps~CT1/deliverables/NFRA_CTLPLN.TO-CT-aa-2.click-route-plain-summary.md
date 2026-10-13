# Click route, plain words

## What was set up
On 12 October 2026, a checked package for a small software library called click reached the dell1 computer. It went only into a throwaway workspace, since deleted. The computer's own copy was untouched. A setting, PIP_NO_INDEX set to 1, was saved for the user account. It makes pip, the tool that installs Python add-on software, refuse to consult any online catalogue.

## What was shown
All seven delivered files matched the sender's fingerprints, and the receiving tool's checks passed. Click ran and reported its version. A deliberate download from the public catalogue was refused: pip found no versions and saved nothing. Later that day, a new process built from saved settings, not inherited, saw the setting, and the download was refused again.

## What was not shown
That new process was not a real sign-in session; it lacked two standard settings, and a first attempt crashed for that reason. One setting was supplied inside the test only. The download command ran twice, not once. Requests were not counted directly. The install log held four lines. No real task needing click was found, so only a version check ran. The refusal did not tell anyone to ask the laptop. Nothing on the network stops a download: the setting governs pip only, so another program, another Python install, or a browser can still download, and programs already running are not covered.
