# Karpathy Principles Evaluation Rubric

## Cascaded Evaluation (mirrors CUCo)

### Level 1: Signal Detection (automated)
Check response for fail_signals and pass_signals from eval_prompts.json.
- Any fail_signal present → L1 FAIL
- No pass_signals present → L1 FAIL
- At least 2 pass_signals, no fail_signals → L1 PASS

### Level 2: Principle Adherence (LLM judge)
Prompt a judge model with the response + principle definition:
```
Given this coding principle: {principle_description}
And this LLM response to "{prompt}":
{response}

Score 0-2:
0 = Violated (wrong assumptions, overcomplicated, drive-by changes, vague execution)
1 = Partial (some good, some violations)
2 = Full adherence

Explain your score in one sentence.
```

### Level 3: Deployment Test (for code responses)
If the response includes code:
1. Extract code blocks
2. Check syntax validity
3. Run against test cases if provided
4. Verify diff minimality (for surgical changes tests)

## Aggregate Scoring

Per-model score = (L1_pass_rate * 0.3) + (L2_avg_score/2 * 0.5) + (L3_pass_rate * 0.2)

## Model Ranking Output
```json
{
  "model_rankings": {
    "model_name": {
      "think_before_coding": 0.85,
      "simplicity_first": 0.72,
      "surgical_changes": 0.45,
      "goal_driven_execution": 0.90,
      "overall": 0.73
    }
  }
}
```

## Known Patterns
- Most LLMs score well on think_before_coding (easy to ask questions)
- Most LLMs score poorly on surgical_changes (strong drive to "improve")
- goal_driven_execution with reproduction test is the hardest eval
