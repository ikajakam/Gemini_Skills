#!/usr/bin/env python3
import os
import re
import hashlib
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {"User-Agent": "Mozilla/5.0"}

# =========================
# CONFIG (HUNTER TUNED)
# =========================
MIN_INLINE_SIZE = 400          # bytes
MIN_EXTERNAL_SIZE = 800        # bytes
MAX_BLOCKS_PER_FILE = 10

KNOWN_PATHS = [
    "/admin",
    "/app",
    "/dashboard",
    "/login",
]

HUNTER_KEYWORDS = [
    "api", "auth", "token", "admin", "internal", "graphql",
    "ws", "socket", "upload", "client_id", "redirect",
    "scope", "bearer", "jwt", "organization", "user"
]

# =========================
# REGEX PACK
# =========================
REGEX_PACK = {
    "API Path": r"(\/(?:api|internal|admin|staff|private|beta|v\d+)[\/a-zA-Z0-9_\-]+)",
    "OAuth Param": r"(client_id|redirect_uri|scope|audience|issuer)[\"'\s:=]+[\"']([^\"']+)",
    "Bearer Token": r"Authorization[\"'\s:=]+[\"']Bearer\s+([A-Za-z0-9\-._]+)",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "AWS Key": r"AKIA[0-9A-Z]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "S3 Bucket": r"s3\.amazonaws\.com\/[a-zA-Z0-9.\-_]+",
    "GCS Bucket": r"storage\.googleapis\.com\/[a-zA-Z0-9.\-_]+",
    "CloudFront": r"[a-z0-9\-]+\.cloudfront\.net",
    "GraphQL": r"(\/graphql|ApolloClient|gql`)",
    "WebSocket": r"(wss?:\/\/[^\s\"']+)",
    "Feature Flag": r"(featureFlag|isEnabled|killSwitch|experiment)[\"'\s:=]+[\"']([^\"']+)",
    "Debug Mode": r"(debug|devMode|testMode)[\"'\s:=]+true",
}

# =========================
# OUTPUT
# =========================
def prepare_output(domain):
    base = domain.replace("https://", "").replace("http://", "").strip("/")
    out = os.path.join("jshunt_output", base)
    os.makedirs(os.path.join(out, "js"), exist_ok=True)

    analysis_path = os.path.join(out, "analysis.txt")
    if not os.path.exists(analysis_path):
        open(analysis_path, "w").write(
            "Analysis will be written here by the JSH agent.\n"
        )

    return out

# =========================
# TIER 1 — LIVE HTML
# =========================
def discover_js_live(url):
    urls = set()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for s in soup.find_all("script"):
            src = s.get("src")
            if src:
                urls.add(urljoin(url, src))
            elif s.string:
                urls.add(("INLINE", s.string.strip()))
    except Exception:
        pass

    return urls

# =========================
# TIER 2 — WAYBACK
# =========================
def discover_js_wayback(domain):
    urls = set()
    try:
        cmd = f"echo {domain} | waybackurls | grep '\\.js$'"
        for u in os.popen(cmd).read().splitlines():
            urls.add(u.strip())
    except Exception:
        pass
    return urls

# =========================
# TIER 3 — KNOWN PATHS
# =========================
def discover_js_known_paths(domain):
    urls = set()
    for path in KNOWN_PATHS:
        full = domain.rstrip("/") + path
        urls |= discover_js_live(full)
    return urls

# =========================
# FETCH & FILTER
# =========================
def is_interesting_inline(code):
    if len(code) < MIN_INLINE_SIZE:
        return False
    lc = code.lower()
    return any(k in lc for k in HUNTER_KEYWORDS)

def fetch_js(items, out):
    files, seen = [], set()

    for item in items:
        try:
            if isinstance(item, tuple):
                code = item[1]
                if not is_interesting_inline(code):
                    continue
                name = "inline"
            else:
                r = requests.get(item, headers=HEADERS, timeout=8)
                if r.status_code != 200 or len(r.text) < MIN_EXTERNAL_SIZE:
                    continue
                code = r.text
                name = os.path.basename(urlparse(item).path) or "script"

            h = hashlib.md5(code.encode()).hexdigest()
            if h in seen:
                continue
            seen.add(h)

            path = os.path.join(out, "js", f"{name}_{h[:6]}.js")
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(code)
            files.append(path)

        except Exception:
            pass

    return files

# =========================
# EXTRACTION
# =========================
def extract_blocks(code, window=6):
    lines = code.splitlines()
    blocks = []

    for i, line in enumerate(lines):
        if any(k in line.lower() for k in HUNTER_KEYWORDS):
            start = max(0, i - window)
            end = min(len(lines), i + window)
            block = "\n".join(
                f"{j+1}: {lines[j]}" for j in range(start, end)
            )
            blocks.append(block)

    return list(dict.fromkeys(blocks))[:MAX_BLOCKS_PER_FILE]

# =========================
# SUMMARY
# =========================
def build_summary(files, out):
    summary = os.path.join(out, "summary_for_ai.txt")

    with open(summary, "w", encoding="utf-8") as f:
        f.write("# JS HUNT — RAW ATTACK SURFACE\n")
        f.write(f"Generated: {datetime.now()}\n\n")
        f.write("Analyze this file and write findings to analysis.txt\n")

        for js in files:
            code = open(js, encoding="utf-8", errors="ignore").read()
            findings = []

            for label, rx in REGEX_PACK.items():
                for m in re.findall(rx, code):
                    val = m if isinstance(m, str) else m[-1]
                    findings.append(f"[{label}] {val}")

            blocks = extract_blocks(code)

            if not findings and not blocks:
                continue

            f.write(f"\n\n--- FILE: {os.path.basename(js)} ---\n")

            for h in sorted(set(findings)):
                f.write(f"- {h}\n")

            for b in blocks:
                f.write("\n" + b + "\n")

            f.write("\n----------------------------------------\n")

    return summary

# =========================
# ENTRY POINT (AGENT)
# =========================
def run(domain):
    out = prepare_output(domain)

    js_items = set()

    # Tier 1
    js_items |= discover_js_live(domain)

    # Tier 3
    js_items |= discover_js_known_paths(domain)

    # Tier 2 (best effort, non-fatal)
    js_items |= discover_js_wayback(domain)

    files = fetch_js(js_items, out)
    if files:
        return build_summary(files, out)
    return None
