# Ollama Integration Research & Testing Plan

## Problem
OpenClaw repeatedly fails to use Ollama local models as primary/fallback for agents.

## Current State
- ✅ Ollama server: Running on http://localhost:11434
- ✅ Models available: qwen2.5:1.5b, llama3.1:8b, lfm2.5-thinking, qwen2.5:7b
- ❌ OpenClaw agent integration: Failing repeatedly

## Known Issues from History
1. "phi3:mini does not support tools" - model limitation
2. Unknown model errors when switching
3. Gateway needs restart after config changes

## Test Strategy

### Test 1: Direct Ollama API Test
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:1.5b","prompt":"Hello","stream":false}'
```

### Test 2: Create Isolated Ollama-Only Agent
```bash
openclaw agents add --id ollama-test --model ollama/qwen2.5:1.5b
```

### Test 3: Spawn Subagent with Ollama
```bash
openclaw agent --agent ollama-test --message "Test"
```

## OpenClaw Ollama Requirements
1. Ollama server must be running before gateway starts
2. Model must be fully pulled before use
3. `OLLAMA_HOST` env var may be needed
4. Gateway restart may be required after Ollama changes

## Troubleshooting Checklist
- [ ] Verify Ollama is running: `curl http://localhost:11434/api/tags`
- [ ] Test model directly with curl
- [ ] Check gateway logs for Ollama connection errors
- [ ] Ensure model name matches exactly (case-sensitive)
- [ ] Try isolated agent first before main agent

## Next Steps
1. Create isolated agent with Ollama only
2. Test with simple prompts
3. If isolated works, clone main agent with Ollama as secondary
4. Document working configuration

---
Created: 2026-02-11
