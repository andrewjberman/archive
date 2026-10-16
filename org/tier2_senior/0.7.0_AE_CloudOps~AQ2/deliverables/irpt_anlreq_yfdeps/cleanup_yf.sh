set -u
# IRPT_ANLREQ TO-APPLY-YFDEPS: remove ONLY the 17 staged wheels and the staging folder this act made (rm of those 17 names, then rmdir). Runs as ec2-user.
W=/tmp/irpt-yf-pydeps-20261016.wheels
[ -d "$W" ] || { echo "CLEAN staging folder absent: nothing to remove"; exit 0; }
echo "CLEAN before: $(ls -A "$W" | wc -l) entries in $W"
LIST="beautifulsoup4-4.14.3-py3-none-any.whl certifi-2026.1.4-py3-none-any.whl curl_cffi-0.13.0-cp39-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl frozendict-2.4.7-py3-none-any.whl idna-3.11-py3-none-any.whl multitasking-0.0.13-py3-none-any.whl numpy-2.4.2-cp312-cp312-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl pandas-2.3.3-cp312-cp312-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl peewee-4.0.0-py3-none-any.whl platformdirs-4.9.2-py3-none-any.whl protobuf-6.33.5-py3-none-any.whl pytz-2025.2-py2.py3-none-any.whl requests-2.32.5-py3-none-any.whl soupsieve-2.8.3-py3-none-any.whl tzdata-2025.3-py2.py3-none-any.whl websockets-16.0-py3-none-any.whl yfinance-1.2.0-py2.py3-none-any.whl"
n=0; for f in $LIST; do if [ -f "$W/$f" ]; then rm "$W/$f" && n=$((n+1)); fi; done
echo "CLEAN removed $n of 17 named wheels"
left=$(ls -A "$W" | wc -l)
if [ "$left" -eq 0 ]; then rmdir "$W" && echo "CLEAN rmdir done"; else echo "CLEAN left $left other entries, rmdir NOT run: $(ls -A "$W")"; fi
[ -d "$W" ] && echo "CLEAN folder still present" || echo "CLEAN folder absent"
