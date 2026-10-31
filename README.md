# MindMex — single-file build

Consolidated, self-contained export of the MindMex AI story factory
(a new original superhero empire generator with HUMAN-in-the-loop approval).

## Files
    mindmex      the whole project in one Python file (run this)
                 ~4000 lines; zero API keys required; runs in mock mode

## Quick start
    python3 mindmex --help
    cd tests && python3 -m unittest discover -s . -v   # 7 tests, run against the single file
    python3 mindmex verify     # built-in self-check -> GREEN
    python3 mindmex doctor     # show the fallback ladder (guaranteed output)
    python3 mindmex serve      # run as an MCP server over stdio (tools for ChatGPT/Claude)
    python3 mindmex new-universe --universe "Aurora Imperium"   # George Stanley drafts, YOU approve
    python3 mindmex approve <id>                                # greenlight a hero/villain
    python3 mindmex run --series the-cosmic-hero --episodes 3
    python3 mindmex export-all --series the-cosmic-hero --youtube --print
    python3 mindmex publish-youtube --series the-cosmic-hero

## Fallback plan (always works)
Every subsystem is a ladder that lands on a free/local/mock producer:
    TEXT  OpenRouter live -> fallback chain -> deterministic mock
    VIDEO Runway -> Pika -> Luma  (live-or-mock each)
    IMAGE Pika -> Runway -> Stability
    VOICE ElevenLabs -> local coqui -> local piper -> mock
    YOUTUBE OAuth real -> mock IDs
    MCP   expose all as tools if CLI ergonomics fail
No API key needed. If an API is down/broken, the pipeline still emits output.
Verified: 10/10 checks, incl. failure-injection with garbage keys + dead API URL.

## Status (Oct 2026)
7 tests green in this folder (run against the single-file build), verify GREEN,
MCP protocol verified, HITL gated, fallback ladder proven under failure-injection.
