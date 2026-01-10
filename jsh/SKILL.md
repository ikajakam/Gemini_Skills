---
name: jsh
description: JavaScript security auditor using jsh_helper for reconnaissance
---

# JavaScript Security Auditor Skill

## Overview
This skill assists in auditing JavaScript files found during reconnaissance. It works in tandem with the `jsh_helper.py` script.

## Workflow
1.  **Gather Data**: The user runs `python3 jsh_helper.py --domain <target>`.
2.  **Analyze**: The script generates a `summary_for_ai.txt` file.
3.  **Audit**: Gemini reads this file and identifies vulnerabilities.

## How to Analyze
When the user provides a `summary_for_ai.txt` file content or path, perform the following checks:

### 1. Hardcoded Secrets
Scan for:
- API Keys (Google, AWS, Stripe, etc.)
- Bearer Tokens / JWTs
- Basic Auth credentials
- Encryption keys or salts

### 2. Vulnerable Code Patterns
- **DOM XSS**: Look for `location.search` or `location.hash` feeding into `innerHTML` or `document.write`.
- **Open Redirects**: Look for `window.location = user_input`.
- **Debug Logic**: Look for `isAdmin`, `debug: true`, or exposed source maps.

### 3. Hidden Endpoints
Extract any API routes (e.g., `/api/v1/admin/users`) that look interesting for IDOR or unauthorized access.

## Reporting Format
For each finding, provide:
- **[SEVERITY] Title**
- **File**: (Filename from the summary)
- **Evidence**: The specific line of code.
- **Why it matters**: Brief exploitation scenario.

## Helper Script Usage
If the user asks "How do I scan a domain?", tell them:
```bash
python3 ~/.gemini/skills/jsh/jsh_helper.py --domain target.com
