# LLM routing demo: model accuracy vs cost

50 labelled support tickets (`data/tickets.jsonl`: billing, bug, account, feature_request, other; 10 each, generic
made-up text). The built-in step "LLM: Cheapest passing model" scores candidate models on these tickets and shows,
per model, the accuracy and the projected cost per 1,000 tickets (measured tokens per ticket x 1,000 x list price from
MLGear > Provider Prices > LLM API prices; estimates, check the vendor page).

Two modes:
- **Stop at first pass** (default): models run cheapest first; the first one that reaches the threshold is used and the
  bigger ones are never called. Fewest calls.
- **Compare all models**: every candidate runs on the same tickets (call cap per model), and the cheapest model that
  meets the threshold is marked. Use it to decide which model to run in production.

Demo pipelines (project "LLM routing demo"):
1. Rehearsal, provider "mock": simulated answers, no API calls, no cost (the card says "simulated").
2. Threshold 0.85: the small model passes, the bigger one is never called.
3. Threshold 0.98: the small model falls short, the step falls back to the next model.
4. Model comparison (all models): Haiku, Sonnet and Opus on all 50 tickets (~150 calls, a few cents).

Misclassified tickets (id, expected, got) are listed in the step log and in the score tooltip on the job page.
50 tickets is a small sample: one wrong ticket moves the score by 2 points, so small gaps between models are not
significant. Use a larger eval set of your own before switching models in production.
