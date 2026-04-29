---
name: build-index
description: Creates an INDEX.md knowledge base for a meeting-heavy engagement, with typed tables, markdown links, a contradictions tracker, and a key people reference
---

# Build Index

`INDEX.md` is the central knowledge base for a meeting-heavy engagement. It organises meetings into typed tables, links summaries and transcripts via standard markdown links, tracks cross-session contradictions, and maintains a reference table of key people.

It is also the dependency for `/sync-transcripts` (which writes `—` placeholder rows when new transcripts land) and `/summarize-transcripts` (which replaces `—` with links to completed summaries). Build this file before running either of those skills.

---

## Step 1 — Define your meeting categories

Before writing anything, identify the types of meetings in your engagement. Common patterns:

| Category | Description |
|---|---|
| Stakeholder Interviews | 1:1 sessions with client team members |
| Kickoff & Progress Meetings | Stream kickoffs, weekly reviews |
| Technical Design Sessions | Architecture, workflow, or system design sessions |
| Internal Check-ins | Your own team's internal calls |

Add, rename, or remove categories to match your engagement. Each becomes its own `##` section with its own table. One hard constraint: `Summary` must be the first column in every table — `/sync-transcripts` writes `—` there and `/summarize-transcripts` reads from it.

---

## Step 2 — Write the file header

```markdown
# <Engagement Name> — Knowledge Base Index

> <One-sentence description of the engagement and what this index covers>. Summaries are in `summaries/`; source transcripts are in `transcripts/`.
```

---

## Step 3 — Build each section's table

For each category from Step 1, add a `##` section with a horizontal rule above it and a table below. Use the column patterns for the relevant type.

### Stakeholder Interviews

```markdown
---

## Stakeholder Interviews

| Summary | Role | Date | Transcript |
|---|---|---|---|
| [Name — Role](summaries/YYYY-MM-DD_Name_Role.md) | Role Title | Mon DD | YYYY-MM-DD_Topic.md |
```

### Internal Check-ins

```markdown
---

## Internal Check-ins

| Summary | Date | Key Topics |
|---|---|---|
| [Team Check-in](summaries/YYYY-MM-DD_Checkin.md) | Mon DD | Topic 1, topic 2 |
```

### Kickoff & Progress Meetings

```markdown
---

## Kickoff & Progress Meetings

| Summary | Type | Date | Participants |
|---|---|---|---|
| [Stream 1 Kickoff](summaries/YYYY-MM-DD_Stream1_Kickoff.md) | Stream 1 Kickoff | Mon DD | Person A + Person B |
```

### Technical Design Sessions

```markdown
---

## Technical Design Sessions

| Summary | Type | Date | Participants | Transcript |
|---|---|---|---|---|
| [Architecture Session](summaries/YYYY-MM-DD_Architecture.md) | Architecture Session | Mon DD | Person A + Person B | YYYY-MM-DD_Topic.md |
```

### Custom categories

For any category not listed above, choose columns that are meaningful for that meeting type:
- `Summary` is always first
- `Date` is always present
- Add `Transcript` if transcripts exist for those meetings
- Keep column count consistent within a section — mixed counts break `/summarize-transcripts`

---

## Step 4 — Add Contradictions & Flags

Always include this section, even if empty at first. It captures cross-session conflicts that need resolution before system design is finalised.

```markdown
---

## Contradictions & Flags

> Cross-session contradictions that need resolution before system design is finalised.

1. **Short label — Person A vs. Person B:** One sentence describing the conflict. [Summary A](summaries/YYYY-MM-DD_A.md) says X; [Summary B](summaries/YYYY-MM-DD_B.md) says Y. → *Status: unresolved.*
```

If no contradictions exist yet, leave a placeholder rather than omitting the section:

```markdown
## Contradictions & Flags

> Cross-session contradictions that need resolution before system design is finalised.

*None identified yet.*
```

---

## Step 5 — Add Key People Reference

Always the last section. One row per person, one key note — what matters most about them for the project.

```markdown
---

## Key People Reference

| Name | Role | Key Note |
|---|---|---|
| Full Name | Role Title | One-line note about their most important characteristic for the project |
```

Populate this as you add meeting rows. Keep it deduplicated — the same person may appear under a nickname or short name elsewhere in the index.

---

## Populating the index over time

Once the file exists, the other skills maintain it:

- `/sync-transcripts` — adds `—` placeholder rows as new transcripts are downloaded; leave these as-is
- `/summarize-transcripts` — replaces `—` with markdown links to completed summary files

Do not write summary links directly into the index — let `/summarize-transcripts` do it so the file naming convention stays consistent.
