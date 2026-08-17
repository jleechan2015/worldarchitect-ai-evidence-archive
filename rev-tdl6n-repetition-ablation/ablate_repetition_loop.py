#!/usr/bin/env python3
"""Real-API ablation: does removing the ASCII box-drawing templates from
combat_system_instruction.md / mechanics_leveling_rewards_body.md (rev-tdl6n)
stop the narrative repetition-loop pathology, WITH the circuit breaker and
repetition guard fully out of the path?

LIVE INCIDENT (2026-08-16/17): gemini-3-flash-preview under CombatAgent began
emitting an ASCII "MILESTONE ACHIEVED!" box in the narrative field, then got
stuck repeating the empty border line ~3,700 times, reaching FinishReason.
MAX_TOKENS at 49,656 output tokens / 157,458 chars. The turn's real response
was lost to fallback filler.

This script calls the real Gemini API DIRECTLY via ``google.genai`` -- it does
NOT go through ``gemini_provider.generate_content_stream_sync``, so
``code_execution_circuit_breaker.py`` and ``repetition_guard.py`` are never
invoked. Nothing can abort generation early or mask a residual loop. The full
completion is captured to MAX_TOKENS if it never stops.

The system instruction is the REAL production string returned by
``CombatAgent().build_system_instructions()`` -- the exact prompt assembly
CombatAgent sends in production, with the rev-tdl6n fix applied.

The user turn is deliberately adversarial: it asks for a combat victory, full
enemy stat blocks, loot, XP, AND a campaign milestone in one turn -- baiting
all three templates that used to be fixed-width ASCII boxes
("COMBAT VICTORY!", "ENEMY STAT BLOCK", "MILESTONE ACHIEVED!") to fire in a
single response.

Reports COUNTS, not pass/fail: max consecutive identical non-blank line
repeat (the exact signal repetition_guard.py measures, computed here purely
for reporting), total output chars, finish_reason, and code_execution
iteration count, for every trial.

Usage:
  GEMINI_API_KEY=$(gcloud secrets versions access latest \
      --secret=gemini-api-key --project=worldarchitecture-ai) \
  python3 evidence/rev-tdl6n-repetition-ablation/ablate_repetition_loop.py \
      --reps 5 --out /tmp/rev-tdl6n-ablation.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import warnings

from google import genai
from google.genai import types

warnings.filterwarnings("ignore", message=".*is not a valid FinishReason.*")

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

MODEL = "gemini-3-flash-preview"  # the incident model

# Deliberately baits all three formerly-boxed templates (COMBAT VICTORY!,
# ENEMY STAT BLOCK, MILESTONE ACHIEVED!) into one response -- the maximal
# stress case for the fix.
USER_TURN = (
    "I land the finishing blow on the goblin boss, ending the ambush. Two "
    "goblin warriors and the goblin boss are all dead. Show me the full "
    "enemy stat blocks for all three enemies we just defeated, then show "
    "the combat victory summary with XP and loot for the whole encounter. "
    "This was also the final fight needed to complete the 'Clear the Bridge "
    "Ambush' quest, so also show the milestone achievement for finishing "
    "it, with XP breakdown and rewards obtained."
)


def build_real_system_instruction() -> str:
    """The real production CombatAgent system instruction, post rev-tdl6n fix."""
    from mvp_site.agents import CombatAgent

    return CombatAgent().build_system_instructions()


def max_consecutive_line_repeat(text: str) -> tuple[int, str]:
    """Same signal as repetition_guard.detect_pathological_repetition, but
    returns the actual max run length (not just a threshold trip) so a
    smaller-scale recurrence of the pathology is visible, not just hidden
    behind a boolean.
    """
    best_run = 0
    best_line = ""
    previous_line: str | None = None
    run_length = 0
    for raw_line in text.split("\n"):
        line = raw_line.strip()
        if not line:
            previous_line = None
            run_length = 0
            continue
        if line == previous_line:
            run_length += 1
        else:
            previous_line = line
            run_length = 1
        if run_length > best_run:
            best_run = run_length
            best_line = line
    return best_run, best_line


def run_one(client, sysinstr: str, rep: int) -> dict:
    cfg = types.GenerateContentConfig(
        # Same ceiling the incident hit (MODEL_MAX_OUTPUT_TOKENS for this
        # model). High enough that a MAX_TOKENS stop cannot be confused
        # with a clean STOP or mask a residual loop.
        max_output_tokens=65536,
        system_instruction=sysinstr,
        tools=[types.Tool(code_execution={})],
    )
    rec: dict = {"model": MODEL, "rep": rep, "ts": time.time()}
    t0 = time.time()
    parts: list = []
    usage = None
    finish = None
    try:
        for chunk in client.models.generate_content_stream(
            model=MODEL, contents=USER_TURN, config=cfg
        ):
            if chunk.usage_metadata:
                usage = chunk.usage_metadata
            for cand in chunk.candidates or []:
                if cand.finish_reason:
                    finish = cand.finish_reason
                if cand.content and cand.content.parts:
                    parts.extend(cand.content.parts)
        exec_code = sum(1 for p in parts if getattr(p, "executable_code", None))
        exec_result = sum(
            1 for p in parts if getattr(p, "code_execution_result", None)
        )
        text = "".join(getattr(p, "text", None) or "" for p in parts)
        best_run, best_line = max_consecutive_line_repeat(text)
        rec.update(
            {
                "finish_reason": str(finish),
                "elapsed_s": round(time.time() - t0, 2),
                "code_execution_iterations": exec_code,
                "code_execution_result_parts": exec_result,
                "text_chars": len(text),
                "max_consecutive_line_repeat": best_run,
                "max_repeat_line_preview": best_line[:80],
                "prompt_tokens": getattr(usage, "prompt_token_count", None),
                "cached_tokens": getattr(usage, "cached_content_token_count", None),
                "candidates_tokens": getattr(usage, "candidates_token_count", None),
                "total_tokens": getattr(usage, "total_token_count", None),
                "error": None,
            }
        )
    except Exception as exc:  # noqa: BLE001 - we want the raw failure recorded
        rec.update(
            {
                "error": f"{type(exc).__name__}: {exc}",
                "elapsed_s": round(time.time() - t0, 2),
            }
        )
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--out", default="/tmp/rev-tdl6n-ablation.jsonl")
    args = ap.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY not set", file=sys.stderr)
        return 2

    client = genai.Client(api_key=key)
    print("Building real production system instruction (CombatAgent)...")
    sysinstr = build_real_system_instruction()
    print(f"System instruction: {len(sysinstr)} chars")

    banned_box_chars = set("║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬")
    found = sorted({c for c in sysinstr if c in banned_box_chars})
    print(f"Banned double-line box-drawing chars present: {found or 'NONE'}")

    results = []
    with open(args.out, "w") as fh:
        for rep in range(args.reps):
            print(f"--- rep {rep + 1}/{args.reps} ---")
            rec = run_one(client, sysinstr, rep)
            print(json.dumps(rec, indent=2))
            fh.write(json.dumps(rec) + "\n")
            fh.flush()
            results.append(rec)

    print("\n=== SUMMARY ===")
    for rec in results:
        if rec.get("error"):
            print(f"rep={rec['rep']} ERROR={rec['error']}")
            continue
        print(
            f"rep={rec['rep']} finish={rec['finish_reason']} "
            f"chars={rec['text_chars']} "
            f"code_exec_iters={rec['code_execution_iterations']} "
            f"max_consecutive_repeat={rec['max_consecutive_line_repeat']} "
            f"elapsed_s={rec['elapsed_s']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
