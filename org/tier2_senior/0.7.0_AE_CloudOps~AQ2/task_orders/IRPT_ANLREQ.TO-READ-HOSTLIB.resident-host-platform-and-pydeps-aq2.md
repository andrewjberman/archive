<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-READ-HOSTLIB.resident-host-platform-and-pydeps-aq2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-16</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- a READ ONLY order on the resident host through the channel you used for releases 32 and 34 (Systems Manager): read-only commands (uname, the interpreter's own platform strings, the C library's version, a directory listing of the pydeps folder, a free-space read). No write, no install, no restart, no network call, no secret read, no queue message.
comp-routes: DECLARED-NOT-APPLICABLE -- no route is called. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM change; your principal already sends commands to this host for releases 32 and 34.
comp-adversary: RUN -- by reading AQ2's V2 probe (msg 9066: yfinance, pandas, numpy and requests are absent; pydeps holds 52 entries) and the CTO's ruling (msg 9075) against this cell; the lens: a platform read from the wrong interpreter (the order requires /usr/bin/python3.12, the resident's own, as ec2-user), a glibc version read from a container image instead of the host, a pydeps listing taken as complete when it was a page of a long directory (the order requires the count and the listing whole), a version taken from a directory name that lies (the order also prints each dist-info METADATA Name and Version line), a read that installs or imports a package (it does neither). NOT seen (blind): the host's real architecture and glibc until step 1; denominator: one host, one interpreter, one pydeps folder.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R31_G.md</decomp_doc> round 31, workstream ~G: the platform facts the yfinance library delivery is built for (cell AR-g-114).
<owned_cells>AR-g-114</owned_cells>
</decomp_ref>

  <objective>
    READ the resident host's CPU architecture, interpreter, platform tag, C library version, pip availability, free space and the pydeps folder's contents, write them to two small files, commit, and report ONCE to 2.0.0_SA_COO~G2. Change NOTHING on the host or in AWS.
  </objective>

  <context>
    Load /cloud-ops first. CTO msg 9075 (ruling 2): the library delivery (yfinance==1.2.0 and its closure) is built for the host's exact platform, so the laptop COO `2.0.0_SA_COO~C` can compute a Linux closure and not a Windows one. The resident runs under `/usr/bin/python3.12` as ec2-user with the pydeps appended (`/opt/investor-reporting-ycharts/pydeps`). This order may be run before or after the r34 rollback leg (step 9 of TO-APPLY-R34B); it does not depend on which root is running. The two files you write carry no secret and no customer value.
  </context>

  <the_act>
    GO. Start at step 1; stop on any step that reads wrong and tell 2.0.0_SA_COO~G2.
    1. THE PLATFORM, one read-only script sent through Systems Manager as ec2-user, printing exactly: `uname -m`; the PRETTY_NAME line of /etc/os-release; `/usr/bin/python3.12 -c "import sys, sysconfig, platform; print(sys.version.split()[0], sysconfig.get_platform(), platform.libc_ver())"`; `getconf GNU_LIBC_VERSION`; `/usr/bin/python3.12 -m pip --version` (print its rc; the answer may be a failure, that is a result); `df -Pk /opt/investor-reporting-ycharts | tail -1`. Print every command's rc.
    2. THE PYDEPS, one read-only script: list the folder /opt/investor-reporting-ycharts/pydeps whole (`ls -1A`), print the count and that the listing was not cut; then for each directory ending in .dist-info print the `Name:` and `Version:` lines of its METADATA file (`grep -m2 -E '^(Name|Version):'`); no import, no pip command that writes. Also print whether the folder is writable by ec2-user (`test -w`) and its owner.
    3. WRITE org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/HOST_PLATFORM.txt with ONE line each, exactly: `ARCH <uname -m>`, `PYTHON <x.y.z>`, `PLATFORM_TAG <sysconfig platform>`, `GLIBC <x.y>`, `PIP <present|absent>`, `PYDEPS_ENTRIES <n>`, `PYDEPS_WRITABLE <yes|no>`, `DISK_FREE_KB <n>`. And org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/PYDEPS_INVENTORY.txt with one line per installed distribution, `<Name> <Version>`, sorted, and a first line `COUNT <n>`. Commit both in one commit and report ONCE to 2.0.0_SA_COO~G2 with the lines and the commit.
  </the_act>

  <bounds>
    One host, read-only. No install, no pip write, no import of any package, no restart, no queue message, no network call, no secret read. Not in this order: the library delivery itself, the r34 rollback (TO-APPLY-R34B step 9), the Lambdas.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/IRPT_ANLREQ.TO-READ-HOSTLIB.resident-host-platform-and-pydeps-aq2.proof_of_spec.json`.
    <criterion id="HOSTLIB-AC1" cell_refs="AR-g-114">The platform file carries the eight lines.<invocation>grep -c -E '^(ARCH [A-Za-z0-9_]+|PYTHON [0-9]+\.[0-9]+\.[0-9]+|PLATFORM_TAG [A-Za-z0-9_.-]+|GLIBC [0-9]+\.[0-9]+|PIP (present|absent)|PYDEPS_ENTRIES [0-9]+|PYDEPS_WRITABLE (yes|no)|DISK_FREE_KB [0-9]+)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/HOST_PLATFORM.txt</invocation><expect>^8$</expect></criterion>
    <criterion id="HOSTLIB-AC2" cell_refs="AR-g-114">The inventory starts with its count.<invocation>grep -c -E '^COUNT [0-9]+$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r34/PYDEPS_INVENTORY.txt</invocation><expect>^1$</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: a READ order to a tier-2 applier (not a worker cell); the cell AR-g-114 is the issuer's, as for TO-READ-R34POOL.
