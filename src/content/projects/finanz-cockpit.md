---
title: Finance cockpit
oneLiner: Several banks and several currencies, normalised into one schema — and the masking rules that make it safe to look at.
short: 'Several banks and currencies, in one picture.'
tag: Money
why: >-
  My accounts sit in different banks and different currencies. Adding them up by hand gave me a number I could not check. I wanted one picture I can reproduce next month.
role: sole author
period: '2026'
stack:
  - Python
  - PSD2 / open banking
  - CSV parsers
  - JSONL normalised layer
repoStatus: architecture-only
status: published
order: 4
metrics:
  - label: Currencies
    value: '3'
    note: one base currency, the others converted at the correct date per row
  - label: Ingestion paths
    value: '2'
    note: an open-banking API, and CSV for banks without one
  - label: Pipeline
    value: 1,595 LOC
    note: nine scripts, one shared schema module every parser must satisfy
sanitized: true
reviewed: 2026-11-10
---

## The problem is not the maths

Money spread across several banks and currencies does not produce a hard arithmetic problem. It produces a **reconciliation** problem: each bank describes a transaction differently, in different currencies, with different date semantics, and none of them will ever agree to a common format.

The naive approach — open every app, read every balance, add them up — fails in a specific way. It gives you a number you cannot check, cannot reproduce next month, and cannot decompose when it looks wrong.

## One normalised layer, two ways in

Everything lands in a single normalised schema. What differs is only how it gets there.

| Source | Method | Automation |
|---|---|---|
| Banks with an open-banking API | PSD2 account-information API | Fully automated; consent must be re-authorised every ≤180 days |
| Banks without one | CSV or Excel export → parser | Manual export, automated parsing |

The rule that keeps this from decaying: **analysis only ever runs on the normalised layer, never on a raw export.** Raw responses are kept, but they are inputs, not sources of truth. Adding a new EU bank requires no code at all — it is one authorisation command, because PSD2 is a standard. Adding a CSV-only bank means writing one parser function that maps columns onto the shared schema. That asymmetry is the whole reason the schema module exists as a separate file every parser must satisfy.

## Currency conversion is a date problem

The mistake that makes cross-currency numbers meaningless is converting everything at today's rate.

**Flows convert at the transaction date. Stocks convert at the snapshot date.** A payment received in March is a March-rate event forever; a balance sitting in an account is worth what it is worth on the day you are asking. Rates come from a central-bank reference series and are cached locally, so a recomputation of last year's figures produces last year's answer rather than a new one.

This sounds pedantic until you need a figure that must still be defensible two years later.

## Privacy as a schema property, not a habit

This pipeline touches the most sensitive data I have, and it exists to be read in conversation with an AI assistant. So the protections are structural rather than behavioural:

- **Raw API responses and raw exports are git-ignored.** They never enter version control.
- **The normalised layer masks account identifiers at write time** — only the last four characters survive. Not at display time, at *write* time, so no downstream consumer can leak what it never received.
- **Credentials live in a git-ignored config file**, with a committed example template carrying the shape but no values.
- **Analysis output shows aggregates and masked counterparties.** Full account numbers and tokens are never printed, including into a chat transcript.

The distinction I care about here: masking at write time means the safety property holds for code I have not written yet. Masking at display time means every future feature is one forgotten call away from a leak.

## Boundaries between systems

Other workflows read from this pipeline. It would have been easy to let it also *interpret* the rows for them.

It doesn't. Interpretation lives in the workflow that needs it, and this pipeline only hands over rows. Two systems computing the same figure from different assumptions is the failure mode that makes both untrustworthy, and personal finance offers no shortage of figures that are almost the same.

The same reasoning governs the manual layer: values and obligations that no API will ever report live in a hand-maintained file with explicit `skip_if_actual` markers. When real synced data eventually covers a period, the estimate yields to it automatically rather than being silently double-counted. Estimates are labelled as estimates in the schema, so nothing downstream has to remember which is which.
