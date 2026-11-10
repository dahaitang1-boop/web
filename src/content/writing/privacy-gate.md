---
title: A privacy gate for a public site
blurb: How this site is published from a machine that also holds private records.
date: 2026-11-08
sanitized: true
reviewed: 2026-11-10
---

This website is built on the same laptop that holds my private paperwork. The systems I write about here read that paperwork every day.

So the risk is simple. One careless copy and a private detail is on the public internet.

I did not want to rely on being careful. I wanted a gate.

## The rule: deny by default

Before every build, a scanner reads every file in the site. If it finds something that looks private, the build stops. Nothing is published.

It looks for patterns, such as long digit runs, phone numbers, bank account formats, and a list of folder names that must never appear. It also has a short list of topics that are never allowed, whatever the context.

The default answer is no. To publish something that looks sensitive, I have to add that exact value to an allowlist and write down the reason. A mountain hut's public phone number is a good example. It is on the hut's own website, so it is allowed, and the file says why.

## Patterns in public, values in private

The site's code is public. That creates a small trap. A list of "things that must not be published" is itself a list of private things.

So the rules are split. The public file holds only general patterns. The exact values live in a second file that never leaves my machine. The scanner reads both.

## Three places where the gate sits

A check that can be skipped will be skipped. So the gate is in three places.

1. **In the build command.** The scanner runs first. If it fails, there is no build.
2. **In the content format.** Every page must carry a line saying it was reviewed. A page without that line is a build error.
3. **Before each commit.** This one is a convenience. The first two are the real gate.

## One rule I do not break

When the scanner flags something harmless, the tempting fix is to loosen the pattern. I never do that. I allow the one specific value instead.

A loose pattern fails silently, months later, on a value I have not seen yet. A long allowlist is only a little ugly.

## What it does not do

The scanner cannot read meaning. It will not notice a sentence that reveals too much in ordinary words. So every page also gets read by me before it goes out.

The gate handles the mistakes a machine can catch. That leaves me free to look for the ones it cannot.
