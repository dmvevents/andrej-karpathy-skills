# Knowledge Base — CUCo-Compatible Dataset

A structured knowledge base following the CUCo (Compute-Communication Co-Design) evolutionary learning format, adapted for general coding principles from Andrej Karpathy's observations.

## Structure

```
knowledge_base/
├── learned_instincts/
│   └── instincts.json          # 16 instincts (K001-K033) — rules for LLM prompts
├── negative_examples/
│   ├── hidden_assumptions.md   # Silently assuming scope/format/fields
│   ├── silent_interpretation.md # Picking one meaning of "faster"
│   ├── over_abstraction.md     # Strategy pattern for one function
│   ├── speculative_features.md # Adding caching/validation nobody asked for
│   ├── drive_by_refactoring.md # Improving adjacent code during bug fix
│   ├── style_drift.md          # Changing quotes/types while adding feature
│   ├── vague_execution.md      # "Review, identify, improve" without criteria
│   └── fix_without_reproducing.md  # Fixing bug without failing test
├── positive_examples/
│   ├── surface_assumptions.md  # Numbered assumption list before coding
│   ├── minimal_function.md     # One function until complexity needed
│   ├── surgical_bugfix.md      # Only bug-related lines in diff
│   ├── style_matching.md       # Matching existing code style exactly
│   ├── verifiable_plan.md      # [Step] → verify: [check] format
│   └── reproduce_first.md      # Failing test before fix
├── api_contracts/
│   └── karpathy_principles.md  # Ground truth definitions + rubric
└── evaluation/
    ├── eval_prompts.json       # 8 eval prompts with pass/fail signals
    ├── scoring_rubric.md       # L1→L2→L3 cascaded evaluation
    └── run_eval.py             # Evaluation runner (L1 automated, L2 judge prompt)
```

## How CUCo Uses This

### 1. Instinct Injection
Before generating code, load relevant instincts into the LLM prompt:
```python
import json
instincts = json.load(open('knowledge_base/learned_instincts/instincts.json'))

# Filter by trigger
task_instincts = [i for i in instincts if i['trigger'] == 'editing_code']
# → K020 (don't improve adjacent code), K021 (match style), K023 (every line traces to request)

# Inject into prompt
prompt = "RULES:\n" + "\n".join(f"- {i['id']}: {i['rule']}" for i in task_instincts)
prompt += f"\n\nTASK: {user_request}"
```

### 2. Few-Shot Examples
Include positive/negative examples as context:
```python
negative = open('knowledge_base/negative_examples/drive_by_refactoring.md').read()
positive = open('knowledge_base/positive_examples/surgical_bugfix.md').read()

prompt = f"""Here is a WRONG approach:
{negative}

Here is the CORRECT approach:
{positive}

Now apply the same principle to this task: {user_request}"""
```

### 3. Cascaded Evaluation
Test any LLM response against the principles:
```bash
python knowledge_base/evaluation/run_eval.py \
  --eval-id EVAL-003 \
  --model claude-sonnet-4-20250514 \
  --response "$(cat response.txt)"
```

### 4. Model Rankings
Track which LLMs follow which principles:
```bash
python knowledge_base/evaluation/run_eval.py --report
```

## Integration with Claude Code

The knowledge base is bundled with the Claude Code plugin. When installed via:
```
/plugin install andrej-karpathy-skills@karpathy-skills
```

The instincts and examples are available to Claude Code sessions through the skill system.

## Extending the Dataset

To add a new example pair:

1. **Negative example** → `knowledge_base/negative_examples/your_antipattern.md`
   - Title: "NEVER: [description]"
   - Sections: Principle Violated, What Happened, The Wrong Code, Why It's Wrong, Hard Rule

2. **Positive example** → `knowledge_base/positive_examples/your_pattern.md`
   - Title: "Pattern: [description]"
   - Sections: Principle, When to Use, The Pattern, Why It Works, Key Elements

3. **Instinct** → Add entry to `instincts.json`
   - Fields: id, rule, principle, confidence, source, trigger, negative_example/positive_example

4. **Eval prompt** → Add entry to `evaluation/eval_prompts.json`
   - Fields: id, principle, prompt, pass_criteria, fail_signals, pass_signals, difficulty
