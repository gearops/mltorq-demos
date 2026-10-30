#!/usr/bin/env python3
# SPDX-License-Identifier: BUSL-1.1
# Copyright (c) 2026 GearOps. Original demo code, no third-party dependencies.
"""Support-ticket router: a tiny, deterministic, offline stand-in for a prompt-driven AI app.

The behaviour lives in a prompt file (routing rules); "changing the AI" means editing the prompt.
Reads a ticket on stdin (or --text) and prints exactly one label.

    echo "I was charged twice" | python3 app.py --prompt prompts/v2_improved.txt     ->  billing
"""
import argparse
import re
import sys


def load_prompt(path):
    rules, default = [], "other"
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or ":" not in line:
                continue
            label, rest = line.split(":", 1)
            label = label.strip().lower()
            if label == "default":
                default = rest.strip().lower()
                continue
            words = [w.strip().lower() for w in rest.split(",") if w.strip()]
            rules.append((label, words))
    return rules, default


def route(text, rules, default):
    t = " " + re.sub(r"[^a-z0-9' ]", " ", text.lower()) + " "
    t = re.sub(r" +", " ", t)
    best, best_hits = default, 0
    for label, words in rules:  # first rule wins ties
        hits = sum(1 for w in words if " " + w + " " in t)
        if hits > best_hits:
            best, best_hits = label, hits
    return best


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--prompt", required=True, help="prompt file with the routing rules")
    ap.add_argument("--text", help="ticket text (default: read stdin)")
    a = ap.parse_args(argv)
    rules, default = load_prompt(a.prompt)
    text = a.text if a.text is not None else sys.stdin.read()
    print(route(text, rules, default))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))