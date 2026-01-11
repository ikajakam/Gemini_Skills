#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

BASE_OUT = "nuclei_output"

def ensure_out(target):
    base = target.replace("https://", "").replace("http://", "").strip("/")
    out = os.path.join(BASE_OUT, base)
    os.makedirs(out, exist_ok=True)
    return out

def build_template_set(context):
    templates = set()

    tech = context.get("tech", [])
    paths = context.get("paths", [])
    aggression = context.get("aggression", "low")

    # Tech-based selection
    for t in tech:
        templates.add(f"cves/{t.lower()}")
        templates.add(f"misconfiguration/{t.lower()}")

    # Path-based logic
    if paths:
        templates.update([
            "exposures/",
            "misconfiguration/",
            "auth/",
            "api/"
        ])

    # Cold target
    if not tech and not paths:
        templates.update([
            "exposed-panels/",
            "default-logins/",
            "misconfiguration/"
        ])

    # Aggression
    if aggression == "high":
        templates.add("cves/")

    return list(templates)

def run_nuclei(target, context):
    out = ensure_out(target)
    raw = os.path.join(out, "nuclei_raw.txt")

    templates = build_template_set(context)

    cmd = [
        "nuclei",
        "-u", target,
        "-silent",
        "-no-color",
        "-o", raw
    ]

    for t in templates:
        cmd.extend(["-t", t])

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return raw

def run(target, context):
    """
    context example:
    {
        "tech": ["wordpress", "apache"],
        "paths": ["/admin", "/api/v1/users"],
        "aggression": "low"
    }
    """
    return run_nuclei(target, context)
