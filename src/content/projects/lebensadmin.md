---
title: Lebensadmin cockpit
oneLiner: A dashboard with no backend — one standard-library generator reads four unrelated systems and writes a single static file.
role: sole author
period: 2025 – 2026
stack:
  - Python (standard library only)
  - TSV as a registry
  - Static HTML
repoStatus: architecture-only
status: published
order: 3
metrics:
  - label: Data sources
    value: '4'
    note: document archive, job funnel, finance, mail — none of which know about each other
  - label: Third-party dependencies
    value: '0'
    note: 504 lines, standard library only, no venv to rot
  - label: Long-running processes
    value: '0'
    note: no server, no database, no sync daemon, no cron requirement
sanitized: true
reviewed: 2026-07-27
---

## Why a dashboard at all

Life admin in a second country generates deadlines that are invisible until they are late. A tax filing date buried in a letter. A residence-permit appointment that must be booked months out. An insurance window that closes on a date nobody states plainly. Miss one and the cost is measured in months, not minutes.

The information already existed on my own disk — in an archive of scanned documents, a job-application tracker, a finance pipeline, a mail scanner. What did not exist was a single place that answered *what is on fire this week*.

## The obvious build, and why I didn't do it

The default shape for this is a small web app: a database, a server, a scheduler pulling from each source, a login. That design has a failure mode I have watched kill every personal tool I have ever built — **it needs maintenance to keep being true**. A container that stops, a certificate that expires, a dependency that breaks on the next OS upgrade. Six months later you are debugging your own dashboard instead of reading it, and the deadlines it was supposed to surface have quietly gone unwatched.

So the constraint I set was: **no process may need to be running for this to work.**

## The architecture

One Python script. It reads four local sources, computes everything at generation time, and writes one self-contained HTML file.

| Source | What it reads | How it stays current |
|---|---|---|
| Document archive | a deadline registry, git log, inbox file count, cloud-folder diff | computed live at each run |
| Job search | the application tracker CSV | computed live at each run |
| Finance | the most recent net-worth snapshot | dropped there by the finance pipeline |
| Mail | a small JSON status file | pushed by the mail scanner after each scan |

Two of the four are **pulled** — read directly and derived on the spot. Two are **pushed** — the owning system writes a small file when it has something to say. That split is deliberate: pull where the source is cheap and local, push where the source needs credentials or network access that the dashboard has no business holding.

The generator has **zero third-party imports**. 504 lines of standard library. There is no virtual environment to rot and nothing to reinstall — it will run on any machine with a Python interpreter, including one restored from a backup in three years.

## Three rules that keep it honest

**A missing source is a state, not an error.** If a system has never been set up, or its file is absent, the panel renders "not configured" and the rest of the dashboard builds normally. A monitoring tool whose own failure blanks the screen teaches you to stop opening it.

**The generator performs no arithmetic on money or dates.** Figures are quoted from source files verbatim. The moment a dashboard starts deriving a number, that number needs its own tests and its own trust, and you have accidentally built a second source of truth that can be wrong in a way you cannot see.

**The dashboard is read-only.** It surfaces the red items; the action happens elsewhere. Making a status page also an action surface is how it acquires state, and state is how it acquires a backend.

## The registry is the real asset

The dashboard is a rendering. The thing worth protecting is the deadline registry underneath it — a tab-separated file with six columns: due date, category, action, source document, status, date added.

TSV, not a database, because the operations that actually matter are *append a row* and *read the whole thing*, both of which a text file does perfectly while remaining diffable, greppable, and readable by a human with no tooling at all. It is version-controlled alongside the documents it references, so every deadline can be traced back to the letter it came from.

The maintenance rule is one line, and it is the entire discipline: **any deadline discovered in any context — opening mail, filing a document, a passing remark in conversation — gets appended immediately.** Completed items are marked done and kept, never deleted, because the record of having handled something on time is occasionally worth as much as the deadline was.

Recurring items bump their due date forward on completion rather than spawning a new row, which keeps the file the size of your actual obligations rather than the size of your history.

## What I would keep

The pull/push split and the zero-dependency rule are the two decisions I would repeat unchanged. Together they mean the tool has no operational surface: nothing to deploy, nothing to monitor, nothing that can be down. The generator either runs and produces a current file, or it does not run and the old file is still sitting there — visibly stale, which is its own useful signal.
