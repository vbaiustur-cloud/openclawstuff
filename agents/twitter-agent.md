# Agent: twitter-agent

## Purpose
Automate a daily Star Atlas TV tweet for account `vb0nline` based on the Star Atlas TV YouTube channel.

## Automation Job
- **Cron:** `Daily Star Atlas TV → tweet draft (vbOnline)` – id `96b9a8ab-...`
- **Schedule:** 09:00 Europe/Berlin
- **Model:** `openai/gpt-5.1` (paid)

### Job Steps
1. Run:
   ```bash
   python3 /home/vbai/.openclaw/workspace/scripts/staratlas_tv_check.py --daily
   ```
   - Script prints exactly one tweet body (<= 280 chars) to stdout.
2. Post that text to `https://x.com/home` using the logged-in OpenClaw Chromium session.
3. If posting fails, send vb a Telegram message with:
   - The tweet text
   - The error encountered

### Content Rules
- English only
- Start with `GM`
- Max 1 tweet/day
- Only source: **Star Atlas TV**
- No financial advice / speculation
- Include the YouTube link

## Fallback / Reset Plan
If GPT/config is reset:
1. Ensure the script `scripts/staratlas_tv_check.py` exists and works.
2. Recreate the cron with the steps and rules above.
3. Use `openai/gpt-5.1` or another configured GPT-like model for orchestration.
