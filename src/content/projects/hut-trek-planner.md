---
title: Hut-trek planner
oneLiner: A constraint solver for alpine hut bookings, and a single-file planner that still works when the signal doesn't.
short: 'Books a week of alpine huts as one chain. Works with no signal.'
tag: Outdoors
why: >-
  Popular alpine routes sell out hut by hut. One full hut can break a whole week. I wanted a plan that closes the chain of bookings first, and a map I can open on the mountain without a signal.
role: sole author
period: 2025 – 2026
stack:
  - Constraint propagation
  - SVG (WGS84 projection, Catmull-Rom)
  - Vanilla JS, zero dependencies
  - Prose-as-spec
repoStatus: architecture-only
status: published
order: 1
metrics:
  - label: Nights chained
    value: '7'
    note: 6 huts, one booked twice, across 8 stages
  - label: Distance
    value: 85 km
    note: '+6,850 m ascent, 7 walking days plus a rest day'
  - label: Full re-solves
    value: '1'
    note: one zero-availability cell invalidated the plan in both directions
  - label: Network calls while walking
    value: '0'
    note: one file, opened from local storage in a valley with no coverage
artifact:
  path: /artifacts/berliner-hoehenweg/planner.html
  title: 'Berliner Höhenweg planner (published template)'
  allow: geolocation
  caption: >-
    The real artifact, with the reservation numbers and membership details
    blanked so it works as a template for your own booking chain. The map is
    hand-drawn SVG; the topo layer behind the toggle is the only thing that
    ever touches the network.
sanitized: true
reviewed: 2026-11-10
---

## The problem is a chain, not a list

On a trail with valley towns you can absorb a bad night: walk further, stop earlier, drop into a village. On an alpine high route you cannot. The huts are a day apart, they are the only legal accommodation, and the terrain between them offers nothing.

That makes an itinerary a **chain of fixed links**. Fix any one night and every other night is determined. In peak season a single popular hut with zero beds does not fail locally — it propagates in both directions and can invalidate an otherwise perfect plan.

The obvious approach fails badly: start from your preferred departure date and walk forwards, and you discover a wall four steps in and restart from scratch.

## Anchor on scarcity, then propagate

The method that works inverts it.

1. **Find the binding constraint** — the hut with the fewest viable dates. Usually the smallest, the most photogenic, or the one nearest a road head.
2. **Anchor the chain on one of its open dates.**
3. **Propagate outwards**, one day per stage, forwards and backwards, checking each night against an availability matrix.
4. **A link landing on zero kills the anchor date.** Try the constraint's next open date; exhaust its options before touching anything else.
5. **If every anchor date fails, the constraint is structural** — the route as designed cannot be booked in this window, and you move to release valves: shift the whole chain, reverse direction, substitute a valley guesthouse, merge two stages, or drop the opening stages.

Two details matter more than they look:

**Record bed counts, not free/full.** A cell with one bed is a different risk from a cell with twelve, and single beds vanish during the conversation in which you are discussing them.

**Classify every link as hard or soft before anything goes wrong.** A hard link is the only accommodation within a day's walk with no road access — losing it breaks the trip. A soft link has transport or an alternative nearby — losing it costs a stage. This is what turns *"the hut is full, everything is ruined"* into *"that night has three fallbacks, keep going"*, and it tells you when it is safe to buy a non-refundable rail ticket.

## What actually happened

Berliner Höhenweg (Zillertaler Runde), 8 stages, 7 nights, a fixed return deadline.

The first plan was clean until **Berliner Hütte showed zero beds on 1 August**. That single cell killed the rest day and, because the chain propagates, both neighbouring nights with it.

The re-solve:

- Combined stages 3 and 4 into one 8.5–9 h day with +1,415 m over the Schönbichler Horn (3,134 m).
- Moved the rest day earlier by booking Berliner Hütte for two consecutive nights — the only dates with two beds each.
- **Cancelled an already-confirmed hut booking and paid the €10 fee**, downgrading Furtschaglhaus from a night to a mid-morning break stop.

The result is better than the original: the rest day now sits directly after the two hardest days and immediately before three consecutive *schwarz* stages, instead of the awkward 2.5-hour half day it replaced.

A second constraint had nothing to do with beds. The outbound rail connection is an **8-minute platform change in München**, Gl 15 to Gl 12. Missing it lifts the Zugbindung automatically, so the recovery path — next RJ/EC, or regional via Rosenheim–Kufstein — is written into the plan alongside the hut's phone number and the latest arrival time that still works.

## Why the artifact is one offline file

Somewhere above 2,000 m, with a forecast that has changed and a cancellation window closing at 18:00 that evening, you need the plan. There is no signal.

So the planner is a single HTML file with no build step, no framework, and no runtime dependency. Everything is inlined. It is opened from local storage on the phone, and it works.

The consequences of that constraint shaped the design:

- **The map is hand-drawn SVG**, projected from WGS84 with Catmull-Rom smoothing, carrying a graticule, a scale bar computed from the projection itself, a north arrow and a legend. A tile layer would have needed the network. The optional topo overlay behind a toggle is the one exception, and it degrades silently when it cannot load.
- **Dates are the only variable.** Everything else — stages, grades, ascent, escape routes, hut phone numbers — is constant, so shifting the start date by a day re-renders the whole plan without re-deriving anything.
- **Go/no-go rules are in the document, not in my head.** Stage 2 and stage 3 are weather-gated with 06:00 and 07:00 starts; each has a valley Plan B that lands on the same bed. Stage 7 is the Königsetappe with no escape mid-route and no water, so the decision is made at the previous hut the evening before.
- **The booking tracker uses real `<textarea>` elements and patches in place** rather than re-rendering, because losing what you typed while standing in a hut doorway is unacceptable.

## The reusable part

The route data is one trek; the method is not. Both the chain-solving procedure and the planner's build spec are written as prose specifications rather than code — which is what lets them be re-applied to a different range, a different hut system, and a different set of membership economics without porting anything.

The reporting rule is the piece I would keep above all others: every round of solving ends with a numbered action list in **scarcity order, not route order**. Route order is what you will walk. Scarcity order is what you should click, right now, before the two remaining beds are gone.
