#!/usr/bin/env python3
"""Check Star Atlas TV YouTube channel for latest uploads and generate tweet drafts.

- Uses the channel RSS feed (no API key).
- Tracks last seen video id in workspace/state/staratlas_tv.json.
- Attempts to fetch English auto-captions via yt-dlp for better summaries.

Outputs:
- human-readable text to stdout (for the main agent to paste/send)

Modes:
- default: if there is a new video since lastSeen, prints multiple tweet options and updates state.
- --daily: always prints exactly ONE tweet body (<=280 chars). If no new video, uses the last-seen video as source and does NOT advance lastSeen.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

CHANNEL_URL = "https://www.youtube.com/@staratlastv"
RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCElCan0ISZn68l7b341yxLA"  # Star Atlas TV
STATE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "state", "staratlas_tv.json")

# Always tag the source accounts + hashtag per user preference.
TAG_SUFFIX = " @staratlastv @staratlas #staratlas"


def _load_state() -> dict:
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _save_state(state: dict) -> None:
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    tmp = STATE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_PATH)


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OpenClaw)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _parse_rss(xml_text: str) -> list[dict]:
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    root = ET.fromstring(xml_text)
    out = []
    for entry in root.findall("atom:entry", ns):
        vid = entry.findtext("yt:videoId", default="", namespaces=ns)
        title = entry.findtext("atom:title", default="", namespaces=ns)
        published = entry.findtext("atom:published", default="", namespaces=ns)
        link_el = entry.find("atom:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        author = entry.findtext("atom:author/atom:name", default="", namespaces=ns)
        out.append({
            "videoId": vid,
            "title": title,
            "published": published,
            "link": link,
            "author": author,
        })
    return out


def _published_dt(published: str) -> datetime:
    # example: 2026-01-31T12:34:56+00:00
    try:
        return datetime.fromisoformat(published.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def _get_captions_text(video_url: str, max_chars: int = 8000) -> str:
    """Best-effort: fetch English auto captions via yt-dlp. Returns plain text."""
    # We use --write-auto-subs and --skip-download; yt-dlp writes .vtt to a temp dir.
    import tempfile

    with tempfile.TemporaryDirectory(prefix="openclaw-yt-") as td:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-subs",
            "--sub-langs",
            "en.*",
            "--sub-format",
            "vtt",
            "-o",
            os.path.join(td, "%(id)s.%(ext)s"),
            video_url,
        ]
        try:
            subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        except Exception:
            return ""

        # find vtt
        vtts = [p for p in os.listdir(td) if p.endswith(".vtt")]
        if not vtts:
            return ""
        path = os.path.join(td, vtts[0])
        try:
            text = open(path, "r", encoding="utf-8", errors="replace").read()
        except Exception:
            return ""

    # crude VTT cleanup
    lines = []
    for line in text.splitlines():
        line = line.strip("\ufeff").strip()
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if "-->" in line:
            continue
        if re.match(r"^\d+$", line):
            continue
        if line.startswith("NOTE"):
            continue
        # remove tags
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            lines.append(line)

    joined = " ".join(lines)
    joined = re.sub(r"\s+", " ", joined).strip()
    if len(joined) > max_chars:
        joined = joined[:max_chars] + "…"
    return joined


def _make_tweets(title: str, link: str, transcript_hint: str | None) -> list[str]:
    # Very lightweight heuristic summarizer from transcript: pick 2–3 salient sentences.
    why = ""
    bullets = []

    if transcript_hint:
        # split into sentences-ish
        sents = re.split(r"(?<=[.!?])\s+", transcript_hint)
        # keep longer-ish sentences
        sents = [s.strip() for s in sents if len(s.strip()) >= 50]
        # dedupe-ish
        seen = set()
        cleaned = []
        for s in sents:
            key = re.sub(r"\W+", "", s.lower())[:80]
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(s)
        sents = cleaned

        bullets = sents[:3]
        if bullets:
            # why it matters from first bullet
            why = bullets[0]

    # Fallback if no transcript
    if not bullets:
        bullets = ["New Star Atlas TV update dropped — quick highlights inside."]
        why = "Worth a look if you’re tracking development progress and upcoming changes."

    # Tighten
    def tighten(s: str, max_len: int) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        if len(s) <= max_len:
            return s
        return s[: max_len - 1].rstrip() + "…"

    headline = f"GM — Star Atlas TV: {title}".strip()

    tweet1 = "\n".join([
        tighten(headline, 120),
        f"Key points: {tighten(bullets[0], 120)}" if bullets else "Key points: (see video)",
        f"Why it matters: {tighten(why, 120)}" if why else "Why it matters: (context)",
        f"{link}",
    ])

    # Alternative: shorter
    tweet2 = "\n".join([
        tighten(f"GM — Star Atlas TV update: {title}", 140),
        f"Why it matters: {tighten(why, 160)}" if why else "Why it matters: Keeping up with the latest dev signals.",
        f"Watch: {link}",
    ])

    tweet1 = _ensure_tags(tweet1)
    tweet2 = _ensure_tags(tweet2)
    return [tweet1, tweet2]


def _compact_tweet(text: str, max_len: int = 280) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_len:
        return text
    # Try trimming at last space
    trimmed = text[: max_len - 1].rstrip()
    trimmed = re.sub(r"\s+", " ", trimmed).strip()
    return trimmed + "…"


def _ensure_tags(text: str) -> str:
    # Avoid duplicating tags/hashtag (match full @/# tokens, not substrings).
    existing = set(re.findall(r"(?:^|\s)([@#][A-Za-z0-9_]+)", text.lower()))
    for token in TAG_SUFFIX.split():
        if token.lower() not in existing:
            text += " " + token
    return text


def _daily_tweet(entries: list[dict], state: dict) -> tuple[str, dict]:
    """Return (tweet_text, new_state). In daily mode we update lastCheckedAt only.

    If a new video exists, we use the newest video and advance lastSeenVideoId.
    If there is no new video, we use the lastSeen video as the source and DO NOT advance lastSeenVideoId.
    """
    # newest first
    entries.sort(key=lambda e: _published_dt(e.get("published", "")), reverse=True)

    newest = entries[0]
    newest_id = newest["videoId"]
    last_seen = state.get("lastSeenVideoId")

    if last_seen and last_seen != newest_id:
        # New video: advance lastSeen
        title = newest["title"]
        link = newest["link"]
        transcript = _get_captions_text(link)
        bullets = []
        if transcript:
            sents = re.split(r"(?<=[.!?])\s+", transcript)
            sents = [s.strip() for s in sents if 50 <= len(s.strip()) <= 180]
            if sents:
                bullets = sents[:2]
        what_new = bullets[0] if bullets else title
        why = bullets[1] if len(bullets) > 1 else "Worth a quick watch if you’re tracking current development progress and near-term changes."
        tweet = f"GM — Star Atlas TV: {title}. {what_new} Why it matters: {why} {link}"
        tweet = _ensure_tags(tweet)
        state["lastSeenVideoId"] = newest_id
        state["lastSeenPublished"] = newest.get("published")
        state["lastCheckedAt"] = datetime.now(timezone.utc).isoformat()
        return _compact_tweet(tweet), state

    # No new video (or no state yet): use lastSeen if present else newest
    chosen = None
    if last_seen:
        for e in entries:
            if e.get("videoId") == last_seen:
                chosen = e
                break
    if chosen is None:
        chosen = newest

    title = chosen["title"]
    link = chosen["link"]
    transcript = _get_captions_text(link)

    takeaways = []
    if transcript:
        sents = re.split(r"(?<=[.!?])\s+", transcript)
        sents = [s.strip() for s in sents if 50 <= len(s.strip()) <= 160]
        takeaways = sents[:3]

    if not takeaways:
        takeaways = [
            "Quick recap from the latest episode.",
            "Key updates are inside.",
        ]

    # NotebookLM-style: 2–3 takeaways + why it matters + link
    takeaways_txt = " | ".join(takeaways[:3])
    why = "Why it matters: it keeps you aligned with the latest dev signals and what’s coming next."
    tweet = f"GM — Star Atlas TV recap: {title}. {takeaways_txt} {why} {link}"
    tweet = _ensure_tags(tweet)

    # daily mode does NOT advance lastSeen when there is no new video
    state["lastCheckedAt"] = datetime.now(timezone.utc).isoformat()
    return _compact_tweet(tweet), state


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--daily", action="store_true", help="Print exactly one tweet body (<=280 chars).")
    args = ap.parse_args()

    xml_text = _fetch(RSS_URL)
    entries = _parse_rss(xml_text)
    if not entries:
        print("No entries found in RSS.")
        return 2

    state = _load_state()

    if args.daily:
        tweet, new_state = _daily_tweet(entries, state)
        print(tweet)
        _save_state(new_state)
        return 0

    # default behavior (drafts only when new)
    entries.sort(key=lambda e: _published_dt(e.get("published", "")), reverse=True)

    last_seen = state.get("lastSeenVideoId")
    newest = entries[0]
    newest_id = newest["videoId"]
    newest_link = newest["link"]

    if last_seen == newest_id:
        print("No new Star Atlas TV video since last check.")
        return 0

    title = newest["title"]
    transcript = _get_captions_text(newest_link)
    tweets = _make_tweets(title=title, link=newest_link, transcript_hint=transcript if transcript else None)

    print(f"Source: {CHANNEL_URL}")
    print(f"Latest video: {title}")
    print(f"Link: {newest_link}\n")

    for i, t in enumerate(tweets, 1):
        print(f"--- Tweet option {i} ---")
        print(t)
        print()

    state["lastSeenVideoId"] = newest_id
    state["lastSeenPublished"] = newest.get("published")
    state["lastCheckedAt"] = datetime.now(timezone.utc).isoformat()
    _save_state(state)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
