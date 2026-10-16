RUN=$(systemctl show -p WorkingDirectory --value irpt-analysis-resident.service)
echo "R0e running root: $RUN"
echo "R0e producer list: $(grep -m1 '^OPAL_PRODUCER_PRINCIPALS' $RUN/ycharts/generate/resident_worker.py)"
ls -d /opt/irpt-resident/*r34g* | head -2
