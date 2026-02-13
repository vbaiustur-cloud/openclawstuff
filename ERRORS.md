# ERRORS.md - Known Errors

## Resolved Today

### Twitter API - NOW WORKING!
- **Status**: RESOLVED
- **What happened**: Cron job automatically posted tweet at 15:35
- **Command**: `python3 ~/.openclaw/scripts/staratlas_tv_check.py --daily`
- **Schedule**: Daily at 9 AM (cron: `0 9 * * *`)

### Audio Transcription - KNOWN COMMAND
- **Script**: `python3 /home/vbai/openclaw-dashboard/transcribe.py <audio_file>`

## Still Issues

### Fleet Alerts - API Spam
- **Status**: SPAMMING
- **Cause**: Cannot connect to api.staratlas.com:443
- **Impact**: Log spam every 60 seconds
- **Fix**: Disable cron until fixed

## DO NOT
- Reinstall tools
- Recreate credentials
- Reconfigure Gmail (working)

## Check Before Acting
1. Read PROJECT_STATE.md
2. Read TASKS.md
3. Read ERRORS.md
4. Continue from last task
