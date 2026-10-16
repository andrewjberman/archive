set -u
# IRPT_ANLREQ TO-READ-HOSTLIB step 2 (READ ONLY): the pydeps folder, whole. Sent through Systems Manager; runs as ec2-user.
# No import, no pip, no write. Lists the folder whole with its count, then Name and Version of each .dist-info METADATA, then writability and owner.
P=/opt/investor-reporting-ycharts/pydeps
U="sudo -u ec2-user HOME=/home/ec2-user"
echo "PYDEPS folder $P exists: $($U test -d $P && echo yes || echo no)"
LIST=$($U ls -1A $P)
echo "PYDEPS_ENTRIES $(printf '%s\n' "$LIST" | grep -c .) (ls -1A line count: $($U ls -1A $P | wc -l); the listing below is whole, not cut)"
echo "PYDEPS_LISTING_BEGIN"
printf '%s\n' "$LIST"
echo "PYDEPS_LISTING_END"
echo "DISTINFO_BEGIN"
printf '%s\n' "$LIST" | grep -E '\.dist-info$' | while read -r d; do
  echo "DIST $d :: $($U grep -m2 -E '^(Name|Version):' "$P/$d/METADATA" 2>&1 | tr '\n' ' ')"
done
echo "DISTINFO_END"
echo "PYDEPS dist-info directories: $(printf '%s\n' "$LIST" | grep -c -E '\.dist-info$') ; egg-info: $(printf '%s\n' "$LIST" | grep -c -E '\.egg-info$')"
echo "PYDEPS_WRITABLE_BY_EC2_USER $($U test -w $P && echo yes || echo no)"
echo "PYDEPS_OWNER $(stat -c '%U:%G %a' $P)"
