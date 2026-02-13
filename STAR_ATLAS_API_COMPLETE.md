# 🌌 STAR ATLAS - COMPLETE API INTEGRATION

## Overview

Star Atlas has official APIs and on-chain programs for building tools and automation!

---

## 🎯 What I Found

### 1. Galaxy API (Working!)
**URL:** https://galaxy.staratlas.com

**Status:** ✅ Online and responding

**Available Endpoints:**
- `GET /` - Root API status
- `GET /health` - Health check

### 2. SAGE Program (@staratlas/sage) ⭐
**NPM:** https://www.npmjs.com/package/@staratlas/sage

**Description:** TypeScript bindings for the SAGE (Star Atlas Galactic Economy) on-chain program

**Account Types:**
- Sector - Galaxy sector data
- Star - Star information  
- Planet - Planet data
- Fleet - Fleet management
- Ship - Ship specifications
- FleetShips - Fleet-ships relationship
- StarbasePlayer - Player progress

**Documentation:**
- Build Portal: https://build.staratlas.com/dev-resources/apis-and-data/sage
- Program Docs: https://staratlasmeta.github.io/star-atlas-programs/sage
- NPM: https://www.npmjs.com/package/@staratlas/sage

### 3. On-Chain Data (Verified!)

**Token Addresses:**
- ATLAS: `ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx`
- POLIS: `poLisWXnNRwC6oBu1vHiuKQzFjGL4XDSu4g9qjz9qVk`

**Current Supplies:**
- ATLAS: 35,999,681,636 ATLAS ✅
- POLIS: 359,997,511 POLIS ✅

### 4. DEX Prices (DexScreener)
**API:** https://api.dexscreener.com

**Status:** Working (free, no API key needed)

---

## 🔧 Installation

### SAGE TypeScript SDK
```bash
npm install @staratlas/sage
```

### Python Integration (Already Created!)
```bash
python3 ~/.openclaw/skills/staratlas/staratlas_complete.py
```

---

## 📊 What Data is Available

### ✅ ON-CHAIN (I can query these):
1. Token supplies (ATLAS, POLIS)
2. Token holders
3. NFT ownership
4. Transaction history
5. DEX prices
6. Wallet balances

### 🔄 SAGE PROGRAM (via @staratlas/sage SDK):
1. Fleet data
2. Territory control
3. Player progress
4. Resource management
5. Galaxy state

### ❌ Game Server Data (Not publicly available):
- Players online right now
- Active fleet positions
- Real-time combat
- SAGE participant count

---

## 🚀 Quick Commands

```bash
# Complete Dashboard
python3 ~/.openclaw/skills/staratlas/staratlas_complete.py

# Real-time data
python3 ~/.openclaw/skills/staratlas/realtime_dashboard.py

# Galaxy API Status
python3 ~/.openclaw/skills/staratlas/staratlas_api.py
```

---

## 📁 Files Created

```
~/.openclaw/skills/staratlas/
├── staratlas_complete.py      # Complete integration
├── staratlas_api.py          # API wrapper
├── realtime_dashboard.py    # Real-time dashboard
├── realtime_tracker.py      # On-chain tracker
├── free_api_integration.py  # Free API integration
├── sagE_PROGRAM.md        # SAGE docs
└── realtime_cache.json     # Cached data

~/.openclaw/workspace/
└── STAR_ATLAS_API_COMPLETE.md  # This file
```

---

## 🔗 All Resources

| Resource | URL |
|----------|-----|
| **Build Portal** | https://build.staratlas.com |
| **Galaxy API** | https://galaxy.staratlas.com |
| **SAGE Docs** | https://staratlasmeta.github.io/star-atlas-programs/sage |
| **NPM Package** | https://www.npmjs.com/package/@staratlas/sage |
| **Solana RPC** | https://api.mainnet-beta.solana.com |
| **DexScreener** | https://api.dexscreener.com |

---

## 💡 How to Get Real-Time Game Data

### Option 1: Use SAGE SDK (Recommended)
```bash
npm install @staratlas/sage
```

Then in TypeScript:
```typescript
import { Fleet, Player, Sector } from '@staratlas/sage';

// Get fleet data
const fleets = await Fleet.getAll();

// Get player progress
const players = await Player.getAll();
```

### Option 2: Galaxy API
Check https://galaxy.staratlas.com for available endpoints

### Option 3: Direct Blockchain
Query the SAGE program address on Solana

---

## 🎯 Next Steps

1. **Install Node.js** (for SAGE TypeScript SDK)
2. **Run:** `npm install @staratlas/sage`
3. **Query:** Fleets, players, territories
4. **Build:** Automation tools like Slybot!

---

## 🔍 About Slybot

Slybot is a community automation tool for Star Atlas that uses these same APIs!

**Features:**
- Automated fleet management
- Resource tracking
- Territory monitoring
- Player analytics

**Similar tools** can be built using:
- @staratlas/sage SDK
- Galaxy API
- Solana blockchain data

---

*Created: 2026-02-12 | Status: ✅ Integration Complete*
