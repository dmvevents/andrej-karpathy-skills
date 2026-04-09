#!/usr/bin/env python3
"""
Karpathy Principles Evaluator — CUCo-compatible cascaded eval.

Usage:
    python run_eval.py --model claude-sonnet-4-20250514 --eval-id EVAL-003
    python run_eval.py --model gpt-4o --all
    python run_eval.py --report  # show model rankings
"""
import json
import sys
import re
from pathlib import Path
from datetime import datetime, timezone

EVAL_DIR = Path(__file__).parent
KB_DIR = EVAL_DIR.parent
PROMPTS_FILE = EVAL_DIR / "eval_prompts.json"
RESULTS_FILE = EVAL_DIR / "eval_results.jsonl"
RANKINGS_FILE = KB_DIR / "model_rankings.json"


def load_prompts():
    with open(PROMPTS_FILE) as f:
        return json.load(f)


def l1_evaluate(response: str, eval_entry: dict) -> dict:
    """Level 1: Automated signal detection."""
    fail_signals = eval_entry.get("fail_signals", [])
    pass_signals = eval_entry.get("pass_signals", [])

    found_fail = [s for s in fail_signals if s.lower() in response.lower()]
    found_pass = [s for s in pass_signals if s.lower() in response.lower()]

    passed = len(found_fail) == 0 and len(found_pass) >= 2
    return {
        "level": "L1",
        "passed": passed,
        "fail_signals_found": found_fail,
        "pass_signals_found": found_pass,
        "score": 1.0 if passed else 0.0,
    }


def l2_judge_prompt(response: str, eval_entry: dict) -> str:
    """Generate the L2 judge prompt (to be sent to a judge model)."""
    principles = {
        "think_before_coding": "Think Before Coding: Don't assume. Surface tradeoffs. Present multiple interpretations.",
        "simplicity_first": "Simplicity First: Minimum code that solves the problem. No speculative features.",
        "surgical_changes": "Surgical Changes: Touch only what you must. Match existing style.",
        "goal_driven_execution": "Goal-Driven Execution: Define verifiable success criteria. Reproduce before fixing.",
    }
    principle_desc = principles.get(eval_entry["principle"], eval_entry["principle"])

    return f"""Given this coding principle: {principle_desc}
And this LLM response to "{eval_entry['prompt'][:200]}":

{response[:2000]}

Score 0-2:
0 = Violated the principle
1 = Partially followed
2 = Fully followed

Reply with ONLY a JSON object: {{"score": N, "reason": "one sentence"}}"""


def record_result(model: str, eval_id: str, l1_result: dict, l2_score: float = None):
    """Append result to JSONL log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "eval_id": eval_id,
        "l1": l1_result,
    }
    if l2_score is not None:
        entry["l2_score"] = l2_score
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def generate_rankings():
    """Generate model rankings from results log."""
    if not RESULTS_FILE.exists():
        print("No results yet. Run evaluations first.")
        return

    results = []
    with open(RESULTS_FILE) as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))

    # Group by model
    by_model = {}
    for r in results:
        model = r["model"]
        if model not in by_model:
            by_model[model] = []
        by_model[model].append(r)

    # Load prompts for principle mapping
    prompts = {p["id"]: p for p in load_prompts()}

    rankings = {}
    for model, model_results in by_model.items():
        by_principle = {}
        for r in model_results:
            eval_entry = prompts.get(r["eval_id"], {})
            principle = eval_entry.get("principle", "unknown")
            if principle not in by_principle:
                by_principle[principle] = []
            by_principle[principle].append(r["l1"]["score"])

        scores = {}
        for principle, principle_scores in by_principle.items():
            scores[principle] = sum(principle_scores) / len(principle_scores)
        if scores:
            scores["overall"] = sum(scores.values()) / len(scores)
        rankings[model] = scores

    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_evaluations": len(results),
        "model_rankings": rankings,
    }
    with open(RANKINGS_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(json.dumps(output, indent=2))


def main():
    if "--report" in sys.argv:
        generate_rankings()
        return

    if "--list" in sys.argv:
        for p in load_prompts():
            print(f"  {p['id']:10s} [{p['principle']:25s}] {p['prompt'][:60]}")
        return

    # Manual evaluation mode: paste a response and get L1 score
    if "--response" in sys.argv:
        idx = sys.argv.index("--response")
        eval_id = sys.argv[sys.argv.index("--eval-id") + 1] if "--eval-id" in sys.argv else None
        model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "unknown"

        if not eval_id:
            print("Usage: python run_eval.py --eval-id EVAL-001 --model model-name --response 'paste response'")
            sys.exit(1)

        response = sys.argv[idx + 1]
        prompts = {p["id"]: p for p in load_prompts()}
        if eval_id not in prompts:
            print(f"Unknown eval_id: {eval_id}")
            sys.exit(1)

        eval_entry = prompts[eval_id]
        l1 = l1_evaluate(response, eval_entry)
        record_result(model, eval_id, l1)

        print(f"L1: {'PASS' if l1['passed'] else 'FAIL'}")
        print(f"  Fail signals found: {l1['fail_signals_found']}")
        print(f"  Pass signals found: {l1['pass_signals_found']}")
        print(f"\nL2 judge prompt (send to judge model):")
        print(l2_judge_prompt(response, eval_entry))
        return

    print("Karpathy Principles Evaluator")
    print("  --list                  List all eval prompts")
    print("  --report                Generate model rankings from results")
    print("  --eval-id ID --model M --response 'text'   Evaluate a response")


if __name__ == "__main__":
    main()
