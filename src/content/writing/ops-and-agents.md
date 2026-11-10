---
title: What an operations manager learns from building with AI agents
blurb: Which habits from running operations carry over, and which lesson cost me seventeen documents.
date: 2026-11-09
sanitized: true
reviewed: 2026-11-10
---

I am not an engineer. My job has always been operations: take a messy process, make it clear, make it repeatable.

When I started building my own tools with AI agents, I thought I was learning a new skill. Mostly I was using the old one.

## An agent is a new colleague who reads everything literally

Working with an agent feels like onboarding a fast, capable hire who has no context. If the brief is vague, the work is vague. If the brief has a gap, the gap gets filled with a confident guess.

So the thing that matters most is the written brief. In one of my workspaces there are about 7,700 lines of plain-language instructions and about 1,600 lines of code. The instructions are the system. The code is small.

That is operations work. It is writing a process down so that someone else can run it.

## Do one. Check it yourself. Then scale.

This is the lesson that cost me the most.

I once asked for a batch of seventeen documents at once. They all came from the same template. The template had a flaw. All seventeen had the flaw. I found it when I opened the first one, after the whole batch was finished.

One document, read by me, would have caught it at one seventeenth of the cost.

Now the rule is fixed. For any batch, make one item first and take it all the way to the end. I read it myself. Only then does the rest run. A checklist run by another agent does not replace my own eyes on the first one.

Every operations person knows this as a pilot. I still had to learn it again.

## Decide which steps need a model at all

The common question is which model to use. The better question is which steps should use a model.

Reading text out of a PDF does not need judgement. Neither does compiling a document, or parsing a response from an API. These steps should be plain scripts. They are cheaper, and they give the same answer every time.

I mark those steps in writing as zero-model. If I do not, the workflow slowly drifts toward asking the model for everything.

## Check fit before you produce anything

One of my workflows drafts documents. The largest quality gain came from a rule that stops it from drafting.

It must first say whether the work is worth doing, and it is allowed to say no. Producing output feels productive. A lot of it should never be produced.

## What carries over

Clear briefs. Pilots before rollouts. Cost limits written down. A second reader with a different brief. None of this is about AI. It is how you run any team.

The tools are new. The job is the same one I already had.
