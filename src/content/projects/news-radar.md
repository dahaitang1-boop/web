---
title: News radar
oneLiner: Reworking an open-source news scorer into a three-domain morning briefing — and cutting its running cost by four fifths.
short: 'A morning briefing that scores the news before I read it.'
tag: Information
why: >-
  I was reading too much news and remembering too little. I wanted one short briefing at breakfast, sorted by what matters to me, with the reasons shown.
role: adapted
upstream: https://github.com/Thysrael/Horizon
period: '2026'
stack:
  - Python 3.11
  - uv
  - LLM orchestration
  - RSS / Hacker News ingestion
repoStatus: sanitized-fork
status: published
order: 2
metrics:
  - label: LLM calls per run
    value: 160→35
    note: batch scoring, ~20 items per call, with per-item retry on gaps
  - label: Items recovered per run
    value: '~30'
    note: silently lost to 403s until the fetcher sent a browser User-Agent
  - label: Lines changed
    value: '908'
    note: 908 added / 72 removed across 11 files, on top of a 33-commit upstream
  - label: Scoring rubrics
    value: '4'
    note: tech, securities, politics, general — selected per source
sanitized: true
reviewed: 2026-11-10
---

## Provenance, first

This is **not my project**. [Horizon](https://github.com/Thysrael/Horizon) is an open-source AI news radar by Thysrael, and the great majority of it — the ingestion pipeline, the deduplication, the enrichment stage, the CLI — is theirs. My contribution is a single commit: **908 lines added, 72 removed, across 11 files**, reworking scoring, cost and delivery for a different purpose.

I am writing it up because the changes are the interesting part, not because the codebase is mine.

## Why the scoring had to change

Horizon scores every item against one rubric asking for *relevance to software engineering, AI/ML, and systems research*. That is a coherent choice, and it is the wrong one if you also want to read about interest-rate decisions. A central bank statement or a tariff story lands at 3/10 and gets filtered out before you see it.

The rework replaces the single rubric with **four, selected from the source's category**: tech, securities, politics, general.

The politics rubric is the one worth describing. Political news is unboundedly interesting and almost never actionable, so it caps an item at 4/10 **unless the model can state the mechanism by which it moves an economic variable**. Not "this is important" — the actual chain. That one constraint did more to make the briefing readable than any amount of prompt tuning, because it converts a vague relevance judgement into a claim that can be wrong.

Two supporting changes:

- **The scoring rubric is decoupled from the quota group.** A general-interest source — a newspaper's China desk, say — should not be forced through a single-subject rubric just because its items are counted in a particular bucket.
- **Every item returns a region tag, and a domain×region table prints after scoring.** Geographic preference (China/US over Germany over Canada) lives in a prompt, which means it drifts. A table you see every run is the only way to notice.

## Cost: 160 calls to 35

The original scores one item per LLM call. At the volume this pipeline ingests, that is roughly 160 calls per run and dominates both cost and wall-clock.

Batching to ~20 items per call brings a run down to about **35 calls**. The failure mode of batching is the interesting bit: models drop items from a long response, quietly. So items missing from a batch response are retried individually rather than being treated as unscored, and the throttle now paces *calls* rather than *items*, which is what it was always measuring by accident.

Analysis and enrichment were also split into separate model tiers — the two stages have genuinely different difficulty, and paying the same rate for both was pure waste.

## Two failures worth keeping

**A missing User-Agent cost ~30 items every run.** CNBC and CBC return 403 to a client that does not send a browser User-Agent. Nothing crashed. The fetcher recorded fewer items and the briefing was slightly thinner, every single day, invisibly. This is the failure mode I now look for first in any scraper: not an error, a quiet subtraction.

**A briefing that reads "today was quiet" is the worst possible output.** A broken model name caused every item to score 0. The pipeline completed successfully and produced a calm, confident, empty briefing — which is exactly what you cannot catch when you are reading it half-awake at breakfast. The fix is to warn loudly when scoring largely fails, on the principle that a tool whose failure mode is indistinguishable from a quiet news day is worse than no tool.

## Delivery, and why it isn't hosted

The output is a self-contained HTML page — no CDN, no JavaScript beyond native `<details>`, light and dark — written to a dated file plus a fixed `latest-<lang>.html` so it can be bookmarked once and never again.

The upstream project publishes its output to GitHub Pages. I removed that step. This briefing carries a market snapshot that can include my own positions, so it must not be staged into a publishable directory at all. That is why this page is a write-up rather than a link to a running instance: the thing works, and it is not mine to show you.

Built with [Claude Code](https://claude.com/claude-code).
