# Agent: gamedev

## Purpose
Implement features/changes in the Star Atlas games repositories, and produce playable builds for vb.

## Main Project (current)
- **Repo:** `games/staratlas-sidescroller` → GitHub `citb77/aitestsa`
- **Stack:** Vite + TypeScript + Three.js (browser game)
- **Target:** Web build (no desktop wrapper yet)

## Canonical Build Pipeline
From workspace root:

```bash
cd /home/vbai/.openclaw/workspace/games/staratlas-sidescroller
npm ci
npm run build    # runs: tsc && vite build → dist/
```

## Latest Build Location
- Folder: `games/staratlas-sidescroller/dist`
- Entry point: `dist/index.html`

## How Testers Should Use It
- Serve `dist/` as static files and open `index.html`, or
- Run `npm run preview` from the project root and open the printed localhost URL.

## Fallback / Reset Plan
If GPT or config is reset:
1. Re-clone `citb77/aitestsa` into `games/staratlas-sidescroller`.
2. Re-run the canonical build pipeline above.
3. Treat `dist/index.html` as the "latest playable version" for testers.
