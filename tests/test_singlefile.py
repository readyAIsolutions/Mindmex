#!/usr/bin/env python3
"""Test the CONSOLIDATED single-file MindMex build (mindmex) end-to-end.

These tests exercise the single file directly (subprocess), so they work in this
folder with no separate modules. They mirror the most important behaviors of the
multi-file project's test suites.

Note: the project's original suites (test_mindmex/test_empire/test_media) target the
multi-file layout in /home/nova/Downloads/MindMex. This suite is the one that runs
against this single-file folder.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MFILE = HERE.parent / "mindmex"          # the single consolidated file


def run(*args, env_extra=None, timeout=120):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(MFILE), *args],
        capture_output=True, text=True, env=env,
        cwd=str(HERE.parent), timeout=timeout,
    )


class TestSingleFile(unittest.TestCase):
    def test_single_file_exists_and_compiles(self):
        self.assertTrue(MFILE.exists())
        self.assertGreater(MFILE.stat().st_size, 150_000, "single file should be large")
        r = subprocess.run([sys.executable, "-m", "py_compile", str(MFILE)], capture_output=True)
        self.assertEqual(r.returncode, 0, "must compile")

    def test_help_lists_all_verbs(self):
        h = run("--help")
        for verb in ["new-universe", "publish-youtube", "verify", "doctor", "serve",
                     "approve", "reject", "voice-pick", "run", "export-all", "validate"]:
            self.assertIn(verb, h.stdout)

    def test_verify_returns_green(self):
        r = run("verify")
        self.assertIn("GREEN", r.stdout)

    def test_doctor_shows_fallback_ladder_and_always_works(self):
        r = run("doctor")
        self.assertIn("ALWAYS-WORKS", r.stdout)
        self.assertIn("ladder", r.stdout)

    def test_mcp_serve_handshake_and_7_tools(self):
        msgs = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        ]
        payload = "\n".join(json.dumps(m) for m in msgs) + "\n"
        p = subprocess.run([sys.executable, str(MFILE), "serve"], input=payload,
                           capture_output=True, text=True, cwd=str(HERE.parent), timeout=60)
        lines = [json.loads(l) for l in p.stdout.splitlines() if l.strip()]
        init = [l for l in lines if l.get("id") == 1]
        tools = [l for l in lines if l.get("id") == 2]
        self.assertTrue(init and "result" in init[0], "initialize must respond")
        self.assertEqual(len(tools[0]["result"]), 7, "must expose 7 tools")

    def test_failure_injection_still_produces_output(self):
        bad = {"OPENROUTER_API_KEY": "bad", "ELEVENLABS_API_KEY": "bad",
               "RUNWAY_API_KEY": "bad", "LUMA_API_KEY": "bad", "PIKA_API_KEY": "bad",
               "HEYGEN_API_KEY": "bad", "OPENROUTER_BASE_URL": "http://127.0.0.1:1"}
        r = run("run", "--series", "the-cosmic-hero", "--episodes", "1", env_extra=bad)
        self.assertIn("complete", r.stdout, "pipeline must complete even with broken keys")

    def test_pipeline_and_publish_mock(self):
        r = run("run", "--series", "the-cosmic-hero", "--episodes", "1")
        self.assertIn("complete", r.stdout)
        p = run("publish-youtube", "--series", "the-cosmic-hero")
        self.assertEqual(p.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)