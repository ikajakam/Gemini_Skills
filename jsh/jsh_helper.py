#!/usr/bin/env python3

import os
import re
import requests
import argparse
import hashlib
import jsbeautifier
from urllib.parse import urlparse
from subprocess import Popen, PIPE
from datetime import datetime
import json
import csv

LINKFINDER_BIN = "linkfinder"

# === OUTPUT DIR SETUP ===
def prepare_output_dir(domain):
    base_name = domain.strip().replace("https://", "").replace("http://", "").strip("/")
    output_base = os.path.join("jshunt_output", base_name)
    count = 1
    final_path = output_base
    while os.path.exists(final_path):
        count += 1
        final_path = f"{output_base}{count}"
    os.makedirs(os.path.join(final_path, "js_files"), exist_ok=True)
    return final_path

# === COLLECT JS URLS ===
def get_domains_from_target(domain):
    js_urls = set()
    commands = [
        {"desc": "📡 Subfinder + Waybackurls", "cmd": f"echo {domain} | subfinder -silent | waybackurls | grep '\\.js$'"},
        {"desc": "🌐 Waybackurls (main domain)", "cmd": f"echo {domain} | waybackurls | grep '\\.js$'"}
    ]

    for task in commands:
        print(f"\n{task['desc']}")
        try:
            p = Popen(task["cmd"], stdout=PIPE, shell=True)
            output = p.stdout.read().decode().splitlines()
            found = [url.strip() for url in output if url.strip()]
            print(f"👉 Found {len(found)} JS URLs.")
            js_urls.update(found)
        except Exception as e:
            print(f"⚠️ Error: {e}")

    return list(js_urls)

# === DOWNLOAD JS FILES ===
def download_js_files(js_urls, output_dir, proxy=None):
    downloaded = []
    
    # Limit to unique filenames to avoid duplicates
    seen_hashes = set()

    for idx, url in enumerate(js_urls, 1):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            proxies = {"http": proxy, "https": proxy} if proxy else {}
            resp = requests.get(url, headers=headers, proxies=proxies, timeout=5, verify=True)

            if resp.status_code == 200 and len(resp.text) > 50:
                # Deduplicate by content hash
                content_hash = hashlib.md5(resp.text.encode()).hexdigest()
                if content_hash in seen_hashes:
                    continue
                seen_hashes.add(content_hash)

                fname = urlparse(url).path.split("/")[-1].split("?")[0] or "index.js"
                filename = f"{fname}_{content_hash[:6]}.js"
                path = os.path.join(output_dir, "js_files", filename)
                
                with open(path, "w", encoding="utf-8") as f:
                    f.write(resp.text)
                downloaded.append(path)
                print(f"  ├─ Saved: {filename}")
        except Exception:
            pass
    return downloaded

# === EXTRACT SECRETS (REGEX) ===
def find_secrets(js_file, output_dir):
    with open(js_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # High-confidence patterns only
    patterns = {
        "API Key": r"(?i)(apikey|api_key|token|secret)[\"'\s:=]+[\"']?([A-Za-z0-9\-_]{20,})[\"']?",
        "JWT": r"eyJ[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,}\.[a-zA-Z0-9-_]{10,}",
        "Google Key": r"AIza[0-9A-Za-z\-_]{35}",
        "AWS Access": r"AKIA[0-9A-Z]{16}"
    }
    
    findings = []
    for label, pattern in patterns.items():
        for match in re.findall(pattern, content):
            val = match if isinstance(match, str) else match[-1]
            findings.append(f"[{label}] {val[:10]}... ({os.path.basename(js_file)})")
    
    return findings

# === PREPARE FOR AI (The Magic Step) ===
def prepare_for_ai(downloaded_files, output_dir):
    """Bundles relevant JS code into one context file for Gemini CLI"""
    context_file = os.path.join(output_dir, "summary_for_ai.txt")
    
    print(f"\n📦 Bundling code for Gemini Analysis...")
    
    with open(context_file, "w", encoding="utf-8") as out:
        out.write("# JAVASCRIPT RECONNAISSANCE SUMMARY\n")
        out.write(f"Generated: {datetime.now()}\n\n")

        for js_file in downloaded_files:
            # 1. Regex check first
            secrets = find_secrets(js_file, output_dir)
            
            with open(js_file, "r", encoding="utf-8") as f:
                raw_code = f.read()
            
            # 2. Filter boring files (e.g. jquery, minified bundles without keywords)
            keywords = ["api", "key", "token", "auth", "user", "admin", "config", "fetch", "http"]
            if not any(k in raw_code.lower() for k in keywords) and len(secrets) == 0:
                continue

            # 3. Clean Code (Simple extraction of interesting lines to save tokens)
            # We take lines with interesting keywords + 2 lines context
            lines = raw_code.splitlines()
            interesting_lines = []
            for i, line in enumerate(lines):
                if any(k in line.lower() for k in keywords) or len(line) > 200: # Long lines often contain data
                    interesting_lines.append(f"{i+1}: {line.strip()[:500]}") # Truncate massive lines
            
            if interesting_lines or secrets:
                out.write(f"\n\n--- FILE: {os.path.basename(js_file)} ---\n")
                if secrets:
                    out.write(f"POTENTIAL SECRETS: {json.dumps(secrets)}\n")
                out.write("\n".join(interesting_lines))
                out.write("\n----------------------------------------\n")
    
    print(f"✅ AI Context Ready: {context_file}")
    print(f"   (Size: {os.path.getsize(context_file)} bytes)")
    return context_file

# === MAIN ===
def main():
    parser = argparse.ArgumentParser(description="JS Recon Helper for Gemini")
    parser.add_argument("--domain", required=True, help="Target domain")
    parser.add_argument("--proxy", help="Proxy URL")
    args = parser.parse_args()

    output_dir = prepare_output_dir(args.domain)
    print(f"☢  Starting scan for {args.domain}")
    
    js_urls = get_domains_from_target(args.domain)
    downloaded = download_js_files(js_urls, output_dir, args.proxy)
    
    if downloaded:
        prepare_for_ai(downloaded, output_dir)
        print("\n🚀 DONE! Now ask Gemini:")
        print(f'   "Analyze the JS summary file at {output_dir}/summary_for_ai.txt"')
    else:
        print("❌ No JS files found.")

if __name__ == "__main__":
    main()
