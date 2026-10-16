set -u
# IRPT_ANLREQ TO-READ-HOSTLIB step 1 (READ ONLY): the resident host's platform. Sent through Systems Manager; every command runs as ec2-user.
# It imports no package of the project, installs nothing and writes nothing; `python3.12 -m pip --version` only reports pip's own version.
U="sudo -u ec2-user HOME=/home/ec2-user"
run() {
  label="$1"; shift
  out=$("$@" 2>&1); rc=$?
  echo "CMD $label"
  printf '%s\n' "$out" | sed 's/^/OUT /'
  echo "RC $rc"
}
run "uname -m" $U uname -m
run "PRETTY_NAME of /etc/os-release" $U grep '^PRETTY_NAME' /etc/os-release
run "python3.12 platform strings" $U /usr/bin/python3.12 -c "import sys, sysconfig, platform; print(sys.version.split()[0], sysconfig.get_platform(), platform.libc_ver())"
run "getconf GNU_LIBC_VERSION" $U getconf GNU_LIBC_VERSION
run "python3.12 -m pip --version" $U /usr/bin/python3.12 -m pip --version
run "df -Pk /opt/investor-reporting-ycharts" $U df -Pk /opt/investor-reporting-ycharts
