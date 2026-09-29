#!/usr/bin/env bash
# OA-e-4 AC1 (built, I-5 / FWD-2): the serve skill at opal_ai ${OA_NESTED_REF:-HEAD},
# opal/agent/skills/bbg-teams-assist/SKILL.md, names the served image reader `read_chat_message_images` for a message
# with pasted content (hostedContents) and carries the plain decline sentence, verbatim:
#   I could not read the image you pasted
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
txt=$(git -C opal_ai show "$REF:opal/agent/skills/bbg-teams-assist/SKILL.md" 2>/dev/null | tr -d '\r')
if [ -z "$txt" ]; then echo "SKILL.md absent at opal_ai $REF"; echo "RESULT: FAIL"; exit 1; fi
r=$(printf '%s\n' "$txt" | grep -c 'read_chat_message_images')
h=$(printf '%s\n' "$txt" | grep -ci 'hostedContents\|pasted')
d=$(printf '%s\n' "$txt" | grep -c 'I could not read the image you pasted')
echo "opal_ai $REF SKILL.md: read_chat_message_images=$r; hostedContents/pasted lines=$h; decline sentence=$d"
if [ "$r" -ge 1 ] && [ "$h" -ge 1 ] && [ "$d" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
