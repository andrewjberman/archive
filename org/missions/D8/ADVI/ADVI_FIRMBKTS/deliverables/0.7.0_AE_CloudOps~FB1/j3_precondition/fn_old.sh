emit_chain_complete() {
    local exit_code="${1:-0}"
    local entries_file
    entries_file=$(mktemp "/tmp/gold_emit.XXXXXX")
    cat > "$entries_file" <<EOF
[
  {
    "Source": "bd-pipeline.gold-chain",
    "DetailType": "chain-complete",
    "Detail": "{\"chain_label\":\"$CHAIN_LABEL\",\"completed_at\":\"$(log_ts)\",\"scripts\":\"$SCRIPT_IDS\",\"mode\":\"$MODE\",\"exit_code\":$exit_code}",
    "EventBusName": "default"
  }
]
EOF
    if aws events put-events --entries "file://$entries_file" 2>&1 | grep -q '"FailedEntryCount": 0'; then
        echo "  EventBridge chain-complete emitted (chain_label=$CHAIN_LABEL, mode=$MODE, exit=$exit_code)"
    else
        echo "  WARN: EventBridge chain-complete put-events failed (non-fatal to chain close)"
    fi
    rm -f "$entries_file"
    return 0
}
