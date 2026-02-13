#!/usr/bin/env python3
"""
Enhanced Free Web Search for OpenClaw
Sources: Wikipedia, GitHub, HN, Reddit, Stack Overflow, DuckDuckGo
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from typing import List, Dict

class FreeWebSearch:
    def __init__(self):
        self.user_agent = "OpenClaw/1.0 (Terminal AI Assistant)"
    
    def search_wikipedia(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Wikipedia API"""
        try:
            url = f"https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "utf8": 1,
                "srlimit": max_results
            }
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("query", {}).get("search", []):
                results.append({
                    "source": "Wikipedia",
                    "title": item.get("title", ""),
                    "snippet": item.get("snippet", ""),
                    "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item.get('title', ''))}"
                })
            return results
        except Exception as e:
            return [{"error": f"Wikipedia search failed: {str(e)}"}]
    
    def search_github(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search GitHub API"""
        try:
            url = f"https://api.github.com/search/code"
            params = {"q": query, "per_page": max_results}
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("items", []):
                results.append({
                    "source": "GitHub",
                    "title": item.get("full_name", ""),
                    "snippet": item.get("path", ""),
                    "url": item.get("html_url", "")
                })
            return results
        except Exception as e:
            return [{"error": f"GitHub search failed: {str(e)}"}]
    
    def search_hn(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Hacker News"""
        try:
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                story_ids = json.loads(response.read().decode())[:30]
            
            results = []
            for story_id in story_ids[:30]:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                req = urllib.request.Request(story_url, headers={"User-Agent": self.user_agent})
                with urllib.request.urlopen(req, timeout=10) as response:
                    story = json.loads(response.read().decode())
                
                if story and query.lower() in (story.get("title", "") + story.get("text", "")).lower():
                    results.append({
                        "source": "Hacker News",
                        "title": story.get("title", ""),
                        "url": f"https://news.ycombinator.com/item?id={story_id}",
                        "score": story.get("score", 0)
                    })
                    if len(results) >= max_results:
                        break
            return results
        except Exception as e:
            return [{"error": f"HN search failed: {str(e)}"}]
    
    def search_reddit(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Reddit (via pushshift API)"""
        try:
            url = "https://api.pushshift.io/reddit/search/submission"
            params = {"q": query, "size": max_results, "sort": "desc", "sort_type": "created_utc"}
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("data", []):
                results.append({
                    "source": "Reddit",
                    "title": item.get("title", ""),
                    "subreddit": f"r/{item.get('subreddit', '')}",
                    "url": f"https://reddit.com{item.get('permalink', '')}",
                    "score": item.get("score", 0)
                })
            return results
        except Exception as e:
            return [{"error": f"Reddit search failed: {str(e)}"}]
    
    def search_stackoverflow(self, query: str, max_results: int = 3) -> List[Dict]:
        """Search Stack Overflow"""
        try:
            url = "https://api.stackexchange.com/2.3/search/advanced"
            params = {
                "order": "desc",
                "sort": "activity",
                "q": query,
                "site": "stackoverflow",
                "pagesize": max_results
            }
            url += "?" + urllib.parse.urlencode(params)
            
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                
            results = []
            for item in data.get("items", []):
                results.append({
                    "source": "Stack Overflow",
                    "title": item.get("title", ""),
                    "tags": item.get("tags", []),
                    "url": item.get("link", ""),
                    "score": item.get("score", 0)
                })
            return results
        except Exception as e:
            return [{"error": f"Stack Overflow search failed: {str(e)}"}]
    
    def search_duckduckgo(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search DuckDuckGo (HTML scraping)"""
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}&kl=us-en"
            req = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode()
            
            import re
            results = []
            pattern = r'<a class="result__a" href="([^"]*)"[^>]*>([^<]*)</a>'
            matches = re.findall(pattern, html)
            
            for url, title in matches[:max_results]:
                results.append({
                    "source": "DuckDuckGo",
                    "title": title.strip(),
                    "snippet": "",
                    "url": url
                })
            return results
        except Exception as e:
            return [{"error": f"DuckDuckGo search failed: {str(e)}"}]
    
    def search_all(self, query: str, sources: List[str] = None) -> Dict[str, List[Dict]]:
        """Search all sources"""
        if sources is None:
            sources = ["wikipedia", "github", "hn", "reddit", "stackoverflow", "duckduckgo"]
        
        all_results = {}
        for source in sources:
            source = source.lower()
            if source == "wikipedia":
                all_results["Wikipedia"] = self.search_wikipedia(query)
            elif source == "github":
                all_results["GitHub"] = self.search_github(query)
            elif source == "hn":
                all_results["Hacker News"] = self.search_hn(query)
            elif source == "reddit":
                all_results["Reddit"] = self.search_reddit(query)
            elif source == "stackoverflow":
                all_results["Stack Overflow"] = self.search_stackoverflow(query)
            elif source == "duckduckgo":
                all_results["DuckDuckGo"] = self.search_duckduckgo(query)
        
        return all_results

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: web-search-enhanced.py <query> [--source <source>]")
        print("Sources: wikipedia, github, hn, reddit, stackoverflow, duckduckgo (default: all)")
        sys.exit(1)
    
    query = sys.argv[1]
    sources = None
    
    if "--source" in sys.argv:
        idx = sys.argv.index("--source")
        if idx + 1 < len(sys.argv):
            sources = sys.argv[idx + 1].split(",")
    
    search = FreeWebSearch()
    results = search.search_all(query, sources)
    
    print(f"\n{'='*60}")
    print(f"Search Results for: {query}")
    print(f"{'='*60}\n")
    
    for source, items in results.items():
        print(f"\n### {source}")
        if not items or "error" in items[0]:
            print(f"  Error or no results")
            continue
            
        for i, item in enumerate(items, 1):
            print(f"\n{i}. {item.get('title', 'N/A')}")
            print(f"   URL: {item.get('url', 'N/A')}")
            if item.get('snippet'):
                snippet = item['snippet'][:150] + "..." if len(item.get('snippet', '')) > 150 else item['snippet']
                print(f"   Snippet: {snippet}")
            if item.get('score'):
                print(f"   Score: {item.get('score', 0)}")

if __name__ == "__main__":
    main()
