---
name: jsh
description: JavaScript security auditor using jsh_helper for reconnaissance
---

# JavaScript Security Auditor Skill

## Overview
This skill assists in auditing JavaScript files found during reconnaissance. It works in tandem with the `jsh_helper.py` script.

## Workflow

You ALWAYS analyze that file after execution.

---

## How You Must Analyze JavaScript (Hunter Doctrine)

### 1 API & ROUTE EXTRACTION (PRIMARY OBJECTIVE)
Extract and classify:
- `/api/*`, `/internal/*`, `/admin/*`, `/staff/*`
- Versioned routes (`/v1`, `/v2`, `/beta`)
- Relative & dynamically built paths
- Mobile-only endpoints

For each endpoint:
- Guess auth level
- Suggest IDOR / auth-bypass / mass-assignment testing
- Suggest ffuf wordlists or parameters

---

### 2 AUTH / OAUTH / TOKEN LOGIC
Hunt for:
- OAuth metadata (`client_id`, `redirect_uri`, `scope`, `audience`)
- Token handling in JS
- JWT parsing / trust decisions
- `localStorage` / `sessionStorage` auth

Flag:
- Frontend-trusted claims
- Missing scope / audience validation
- Static OAuth config

---

### 3 SECRETS & CONFIGURATION
Identify:
- Hardcoded API keys
- Contextual secrets (non-random but privileged)
- Feature flags
- Debug / dev toggles
- Kill-switches

Contextual secrets ARE valid findings.

---

### 4 ROLE & ACCESS CONTROL
Look for:
- `isAdmin`, `isStaff`, `hasPermission`
- UI-only enforcement
- Feature gating in JS
- Role checks before API calls

Assume backend may not re-check.

---

### 5 GRAPHQL & WEBSOCKETS
Detect:
- `/graphql` endpoints
- Apollo / Relay usage
- Operation names
- Subscriptions / WebSockets

Suggest introspection and operation abuse.

---

### 6 STORAGE & INFRASTRUCTURE
Extract:
- S3 / GCS buckets
- CloudFront / CDN URLs
- Upload endpoints
- Media paths

Consider IDOR, overwrite, or public access.

---

## Reporting Rules (STRICT)

For EACH finding:
- **[SEVERITY] Title**
- **Category** (API / Auth / Secret / Logic)
- **Evidence** (exact JS code block)
- **Attack Idea** (clear next step)

No generic advice. No theory. Only exploitable surface.

## JavaScript Discovery Coverage

JavaScript discovery includes:
- Live HTML script sources (primary)
- Historical JavaScript via Wayback (secondary)
- Known application entry paths such as:
  /admin, /app, /dashboard, /login

These are used to surface hidden or privileged attack surface.


## Inline JavaScript Handling (STRICT)

Inline JavaScript files (files prefixed with `inline_`) are considered
**low-signal context only**.

### Rules:
- DO NOT create primary findings from inline JS
- DO NOT assign severity based solely on inline JS
- DO NOT use inline JS as standalone evidence in `analysis.txt`

### Allowed use:
- Inline JS may be referenced ONLY to:
  - Corroborate findings found in external JS files
  - Provide configuration context (e.g. storefront IDs, feature flags)

### Enforcement:
- All findings written to `analysis.txt` MUST be supported by
  non-inline JavaScript files unless explicitly stated otherwise.

Inline JS findings should default to INFO severity unless
confirmed exploitable through backend interaction.
