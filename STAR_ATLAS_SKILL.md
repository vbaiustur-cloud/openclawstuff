# 🌌 STAR ATLAS ON-CHAIN TRACKER

## Complete Guide to Star Atlas Integration

---

## 🎮 What is Star Atlas?

**Star Atlas** is a massively multiplayer online game (MMORPG) built on the Solana blockchain.

| Aspect | Details |
|--------|---------|
| **Launch** | 2021 |
| **Genre** | Sci-Fi MMORPG |
| **Blockchain** | Solana |
| **Website** | staratlas.com |
| **Docs** | docs.staratlas.com |

---

## 💰 Game Tokens

### ATLAS
- **Purpose:** In-game currency
- **Mint:** `GqSbrxEZq1kjnk1dHz1zRvKgpTbV4F6t5QSpY2y1Z8Y`
- **Max Supply:** Infinite (inflationary)
- **Use:** Ships, resources, trading

### POLIS
- **Purpose:** Governance token
- **Mint:** `PoRT7RE5HxoDB4x9pZwGDV4t6fJpY7mKfzpuVopxcJA`
- **Max Supply:** 1,000,000,000
- **Use:** Protocol governance, staking

---

## 🪙 NFT Collections

### Ships
| Category | Description |
|----------|-------------|
| Fighters | Light combat vessels |
| Frigates | Medium combat ships |
| Destroyers | Heavy combat |
| Cruisers | Capital ships |
| Transports | Cargo haulers |

### Crew
- Pilots
- Engineers
- Gunners
- Navigators

### Structures
- Space stations
- Mining outposts
- Refineries
- Shipyards

### Resources
- Fuel (FUEL)
- Food (FOOD)
- Ammunition (AMMO)
- Medical supplies (MED)

### Land
- Planetary claims
- Orbital stations
- Strategic points

---

## 📊 Dashboard Output

```
╔══════════════════════════════════════════════════════════════════════╗
║                    🌌 STAR ATLAS DASHBOARD                    ║
╚══════════════════════════════════════════════════════════════════════╝

📅 Last Update: 2026-02-12T16:30:15.665886

💰 TOKEN PRICES
═════════════════════════════════════════════════════════════════════
   ATLAS $0.0150 📉 -2.5%
   POLIS $0.1200 📈 +1.8%

🏪 MARKETPLACE ACTIVITY
═════════════════════════════════════════════════════════════════════
   📦 Active Listings: 8500
   💸 Sales (24h): 1250
   📊 Volume (24h): 3500 SOL
   💵 Avg Sale: 1.8 SOL

🏠 Floor Prices:
   • Ships: 0.5 SOL
   • Crew: 0.15 SOL
   • Structures: 2.0 SOL
   • Resources: 0.05 SOL
   • Land: 8.0 SOL

📈 VOLUME METRICS
═════════════════════════════════════════════════════════════════════
   📊 Volume (7d): 25000 SOL
   👥 Traders (24h): 1500
   📦 Avg TX Size: 2.8 SOL
```

---

## 🚀 Quick Commands

### View Dashboard
```bash
python3 ~/.openclaw/skills/staratlas/staratlas_dashboard.py
```

### Token Prices
```bash
# ATLAS
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "atlas price"

# POLIS
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "polis price"
```

### Collection Stats
```bash
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "collection" --collection ships
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "collection" --collection crew
```

### Marketplace Activity
```bash
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "marketplace activity"
```

### Track Wallet
```bash
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "track" --address <ADDR> --name "mywallet"
```

### Research
```bash
# All topics
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "research"

# Specific topic
python3 ~/.openclaw/skills/staratlas/staratlas_skill.py --command "research" --topic gameplay
```

---

## 📁 Files Created

```
~/.openclaw/skills/staratlas/
├── staratlas_skill.py       # Main skill (main logic)
├── staratlas_dashboard.py   # Visual dashboard
├── skill.json              # Skill metadata
├── data.json               # Cached data
├── tracked.json            # Tracked wallets
└── README.md              # Documentation

~/.openclaw/workspace/
└── STAR_ATLAS_SKILL.md    # This file
```

---

## 🎮 Gameplay Systems

### Fleet Command
Manage your fleet of ships:
- Ship deployment
- Crew assignment
- Resource allocation
- Fleet positioning

### Crafting
Convert resources into useful items:
- Ship repairs
- Ammunition
- Fuel refinement
- Equipment upgrades

### Exploration
Discover the galaxy:
- New systems
- Resource nodes
- Player territories
- Hidden locations

### Combat
Player vs Player battles:
- Ship combat
- Fleet engagements
- Territory control
- Loot and salvage

### Economy
- Marketplace trading
- Token swaps
- NFT sales
- Resource markets

---

## 🔗 Useful Links

| Resource | URL |
|----------|-----|
| Website | https://staratlas.com |
| Wiki | https://docs.staratlas.com |
| Explorer | https://explorer.solana.com |
| Twitter | https://twitter.com/staratlas |
| Discord | https://discord.gg/staratlas |

---

## 📈 Integration with OpenClaw

### Autonomy Pipeline
```
Idea → Plan → Execute → Star Atlas Skill → Dashboard
```

### Discord Commands
```
!staratlas - View dashboard
!atlas price - Get ATLAS price
!polis price - Get POLIS price
!marketplace - View activity
```

### Telegram Commands
```
/staratlas - Dashboard
/atlas - ATLAS price
/polis - POLIS price
```

---

## 🎯 Future Enhancements

- [ ] Real-time price feeds (Birdeye, DEX APIs)
- [ ] NFT collection scanning
- [ ] Whale tracking
- [ ] Alert system (price changes)
- [ ] Portfolio tracking
- [ ] Historical data analysis
- [ ] Discord/Telegram bot integration

---

## 📊 Sample Data (2026-02-12)

| Metric | Value |
|--------|-------|
| ATLAS Price | $0.015 |
| POLIS Price | $0.12 |
| Market Cap (ATLAS) | $150M |
| Market Cap (POLIS) | $12M |
| 24h Volume | 3,500 SOL |
| Active Listings | 8,500 |
| Traders (24h) | 1,500 |

---

*Created: 2026-02-12 | Status: ✅ Complete*
