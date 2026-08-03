---
title: Job-search workspace
oneLiner: Three board clients, a drafter/reviewer loop producing typeset applications, and a cost policy for an agent workspace.
role: fork + rework
upstream: https://github.com/MadsLorentzen/ai-job-search
period: '2026'
stack:
  - TypeScript / Bun
  - Public job-board and ATS APIs
  - LaTeX (lualatex, xelatex)
  - Agent workflow definitions
repoStatus: private
status: published
order: 5
metrics:
  - label: Board clients
    value: '3'
    note: a public employment-agency API, four ATS providers, one public job board
  - label: Written in prose
    value: 71 files
    note: 7,700 lines of Markdown workflow definitions against 1,600 of TypeScript
  - label: Model tiers
    value: '3'
    note: pinned per step, so an expensive session cannot silently upgrade the cheap ones
sanitized: true
reviewed: 2026-07-27
---

## Provenance

A fork of [MadsLorentzen/ai-job-search](https://github.com/MadsLorentzen/ai-job-search). The upstream project supplies the shape: an agent workspace where applications are scraped, ranked, drafted and reviewed as a sequence of defined steps rather than a single prompt.

My rework replaced the Danish job portals with German ones, swapped the CV template, added a compliance export, and imposed a cost policy. The repository itself stays private — it holds actual CVs and an application log — so this is a write-up rather than a link.

## The workspace is mostly prose

The most surprising property of this codebase: **71 Markdown files and 7,700 lines of prose against about 1,600 lines of TypeScript.** The programs are small. The specifications are the system.

That is not laziness. The parts that vary — how to judge fit, what makes a cover letter good, when to escalate to a stronger model — are judgements, and judgements written as prose can be edited by the person who holds them. The parts that do not vary — hitting an API, parsing a response, compiling a document — are code. Putting a judgement in code freezes it at the moment you were least informed about it.

## Three board clients, three different problems

**A public employment-agency API.** A genuine documented API with a published key. Boring, reliable, and by far the best data source. Most job-board scraping exists only because employers do not publish anywhere sane; where a public API exists, use it and stop being clever.

**Four ATS providers.** Greenhouse, Lever, Ashby and SmartRecruiters each expose a per-company endpoint returning that company's own live postings as JSON. Point a list of companies at it and you get first-party data — no scraping, no rate limiting, no stale aggregator listings. This turned out to be the highest-signal source in the system, because a posting on a company's own ATS is one that someone is actually reading.

**A public job board.** Kept, used personally, and deliberately never run from any hosted or CI context — the terms permit personal use, and that boundary is worth respecting rather than testing.

The big German aggregators block automated access outright. Rather than fight that, they are handled as search patterns for manual checking. A tool that pretends to cover a source it cannot actually reach is worse than one that admits the gap.

## Evaluate fit before drafting

The single rule that changed output quality most: **the workflow evaluates fit and reports a verdict before it is allowed to draft anything.**

The tempting design is to generate a tailored CV and cover letter for every posting — it feels productive and it is what the tooling makes easy. But an application to a role you are a poor fit for costs the reviewer's time and yours, and produces a rejection that teaches you nothing. Forcing an explicit fit verdict as a separate step, with the option to stop, means drafting only ever runs on applications worth sending.

## The drafter/reviewer loop, and the checks that survive it

Documents are produced by a drafter, then passed to a reviewer working from a different brief, looping until it passes. What makes this more than theatre is that the criteria are mechanical enough to actually fail:

- **The PDF's text layer must extract cleanly.** Applicant tracking systems read the text layer, not the rendering. A beautiful LaTeX document whose text extracts as garbled columns is invisible to the first filter it meets. This is verified by extracting the text and reading it, every time — never assumed.
- **Length is a hard limit**: CV one to two pages, never three; cover letter exactly one page. Typesetting makes overrun easy and invisible until it is printed.
- **No orphaned entries** — a role title stranded at the foot of a page with its content overleaf.
- **No keyword stuffing.** Tempting, detectable, and it reads as desperate to the human who eventually opens it.
- **Every factual claim must trace to the source CV.** A drafting model asked to tailor will embellish if nothing stops it, and an embellishment you did not notice is one you will have to defend in an interview.

There is also a compliance export: the application log renders into a fixed tabular format required as proof of activity. Unremarkable as engineering — structured records into a defined layout — but it is why the log is maintained rigorously rather than when convenient, and that rigour is what makes every other statistic in the system true.

## A cost policy, written down

An agent workspace has a failure mode a normal codebase does not: **opening it with an expensive model silently makes every step in it expensive.** Sub-agents inherit the session's model unless something stops them, so a workspace that is cheap on Monday can cost ten times as much on Tuesday for reasons nobody chose.

So tiers are pinned rather than inherited:

- The repository defaults to the mid-tier model, and sub-agents pin their tier in their own definition — an expensive parent session cannot upgrade them by accident.
- Escalation to the strongest tier is **manual and per-step**, reserved for the few places where judgement quality pays for itself.
- Several steps are marked **zero-model**: extracting a PDF's text layer, compiling LaTeX, parsing an API response. These are deterministic operations a model should never be asked to perform, and naming them explicitly is what stops the workspace drifting into asking anyway.

That last category is the one I would carry into any agent system. The interesting question is rarely *which model* — it is *which steps should involve a model at all*.

## What is honestly broken

The three board clients were written without live network access and have never been smoke-tested against real endpoints. The employment-agency API's version path has probably moved, and several ATS company identifiers are educated guesses that will 404. The design is sound; the integration is unverified — and pretending otherwise would be exactly the kind of claim this project's own review rules exist to catch.

Built with [Claude Code](https://claude.com/claude-code).
