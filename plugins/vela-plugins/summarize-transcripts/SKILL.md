---
name: summarize-transcripts
description: reads the INDEX.md file for any meeting transcripts that do not have a sumamry written, writes the summary for the transcript, places it in a local folder, updates the index and provides suggestions of any changes to system design
---

# Summarize Transcripts

`INDEX.md` is the single source of truth for what needs summarising. Each transcript that needs a summary already has a row there with `—` in the Summary column (added by `/sync-transcripts`). Do not scan `transcripts/` or `summaries/` to find work — the index has it.

For each pending row, write a structured summary file, replace the `—` in INDEX.md with a WikiLink to the new summary, then scan for design decisions and suggest updates to the relevant `CLAUDE.md` files in the codebase if applicable.


## Step 1 — Identify what needs summarising

Open `INDEX.md`. Any row whose Summary column shows `—` is a pending summary. From that row, read:
- The transcript filename (Transcript column) — this is the file to read in Step 2
- The session type (the table the row appears in — this determines the summary structure)

Session types and their tables:
| Table in INDEX.md | Session type |
|---|---|
| Stakeholder Interviews — Kerten Team | `stakeholder-interview` |
| Intelligence Hub Sessions | `stakeholder-interview` (intelligence hub focus) |
| Kickoff & Progress Meetings | `kickoff` or `progress-review` |
| Technical Design Sessions | `technical-session` |
| Vela Internal Check-ins | `internal-checkin` |

## Step 2 — Read the transcript(s)

Read the full new transcript file(s) from `transcripts/`. Key things to extract:

### Check-in Meetings/Weekly progress meetings:
These are 30min quick check-in calls where we go over quick progress updates. We will be discussing ongoing work for different streams but I am mainly concerned with the proposal generation and intelligence hub.
- **Key Decisions Made** - Any decisions we have made in the meetings regarding the streams we are working on for the client broken down by the different streams. Particular focus on proposal generation and intelligence hub. Anything else, group in others.
- **Key Topics** - Over all key topics discussed and short bullets for each topic.
- **Contradictions and Flags** - Anything contradicting previously made assumptions or things said before.
- **Action Items** - Specific action items as a result of this meeting and who they are assigned to.

### Proposal Generation or Intelligence Hub Meetings
- **Who is speaking** — name, role, any background they give about themselves
- **Their current process** — how they actually do their job today, step by step
- **Tools and sources** — what platforms, databases, documents they use
- **Pain points** — what is broken, slow, manual, unreliable
- **Decisions and system implications** — anything said that has a direct consequence for how the proposal generation system or intelligence hub should be built; these must be captured explicitly
- **Contradictions** — anything that conflicts with what other stakeholders have said

Transcripts are noisy (filler words, cross-talk, tangents). Focus on substance. Discard small talk at the start and end of sessions.

---

## Step 3 — Write the summary file

### File naming
YYYY-MM-DD_Meeting_Type_Name.md

Examples:
- `2026-04-23_Intelligence_Hub_Shivali.md`
- `2026-04-23_Proposal_Generation_Ramine.md`
- `2026-04-23_Vela_Checkin.md`

### File location

Place all summary files directly in `summaries/`. Do not create sub-directories.

---

## Step 4 — Summary structure by session type

Every summary starts with a YAML frontmatter block, then uses the sections described below for its type.

### Frontmatter (all types)

```yaml
---
transcript: "[[<TranscriptFilenameWithoutExtension>]]"
date: YYYY-MM-DD
person: Full Name (or team list for check-ins)
role: Role Title
type: <session type>
tags: [tag1, tag2, ...]
related: ["[[SummaryA]]", "[[SummaryB]]"]
---
```

- `transcript` is an Obsidian WikiLink to the source transcript (no path, no extension) — this is what links the summary back to the transcript in the graph view
- `type` values: `stakeholder-interview`, `internal-checkin`, `kickoff`, `progress-review`, `technical-session`
- `related` should link to summaries that are directly relevant to the content (same person in a different session; sessions that share a topic; summaries referenced within the body)
- Use Obsidian `[[WikiLink]]` syntax throughout the body for all cross-references to other summaries and transcripts

---

### Stakeholder Interview

```
# <Role> — <Name> — <Date>

## Person
- Name, role, background, key context about their position in the workflow

## Inputs
- What information or materials arrive at this person's desk / triggers their involvement

## Their Process
Step-by-step description of how they actually work today.
Use named steps (Step 1 — ..., Step 2 — ...) for clarity.

## Tools Used
- List each tool, with a one-line note on what it is used for

## Outputs & Handoffs
- What they produce and who receives it next

## Approvals & Back-and-Forths
- What requires sign-off, negotiation, or iteration

## Time & Volume
- How long things take, how many per week/month

## Pain Points & Frustrations
- What is broken, manual, slow, or unreliable

## Decisions & System Implications

### Proposal Generation System
- Bullet list of specific decisions or design constraints that follow from this session
- If nothing was discussed, write: Not discussed in this session

### Intelligence Hub
- Bullet list of specific decisions or design constraints
- If nothing was discussed, write: Not discussed in this session

## Observations
- 4–8 bullet points
- Each starts with **bolded key point** — then 1–2 sentences of analysis
- These are analytical, not just descriptive — draw connections to other sessions, flag risks, note what this means for the build
```

---

### Intelligence Hub Session

```
# Intelligence Hub — <Name> — <Date>

## Person
- Name, role, session focus, any relevant context

## Intelligence Sources
Sub-sections for each source (numbered or named).
For each: what it is, how they use it, what they get from it, any limitations.

## [Additional context sections as relevant]
Examples: Lead Disqualification Criteria, Internal CRM Substitute, Contact Tracking, Volume estimates, Market Signal Framework

## Pain Points & Frustrations
- What is missing, manual, or unreliable in their current approach

## Decisions & System Implications

### Proposal Generation System
- Decisions that affect the proposal system (often: shared data sources, none, or an indirect connection)

### Intelligence Hub
- Numbered list of specific decisions — each decision should be actionable and specific enough to inform a build choice
- Include: data sources to use, signals to monitor, filters to apply, geographic priorities, build order, feature requirements

## Observations
- Same format as stakeholder interview observations
```

---

### Vela Internal Check-in

```
# Vela Internal Check-in — <Date>

## Attendees
- Name — Role for each person

## Summary
One short paragraph (3–5 sentences) describing the overall focus and significance of this check-in.

## Decisions Made

## Key Topics
One sub-section per topic discussed.
Each sub-section covers: what was discussed, what was concluded or decided, any open questions.

### Proposal Generation System
- Concrete decisions made in this session

### Intelligence Hub
- Concrete decisions made in this session

## Contradictions & Flags
Numbered list. Each item:
- **Short label:** one-sentence description of the contradiction or flag
- → *Status: resolved / unresolved / needs stakeholder input*

## Observations
- Same format as other session types
```

---

## Step 5 — Update INDEX.md

After writing all summary files, make three types of changes to `INDEX.md`:

### 5a — Replace `—` placeholders with WikiLinks

Find each row that had `—` in the Summary column and replace it with `[[SummaryFilenameWithoutExtension]]`.

Also fill in the Focus / Key Topics column for Intelligence Hub and Vela check-in rows if it was also `—`.

Example — before:
```
| — | Marloes | Apr 23 | — | BD_AI_Intelligence_Hub_Marloes_2026-04-23.md |
```

After:
```
| [[Marloes_Intelligence_Hub_2026-04-23]] | Marloes Knippenberg (CEO) | Apr 23 | Macro market signals, OTA scouting, LinkedIn strategy | BD_AI_Intelligence_Hub_Marloes_2026-04-23.md |
```

### 5b — Add new people to the Key People Reference table

If a summary introduces a person not yet in the Key People table at the bottom of `INDEX.md`, add a row:

```
| Full Name | Role | One-line key note: their most important characteristic for the project |
```

Check for duplicates — the same person may already be listed under a nickname or short name.

### 5c — Add new contradictions if found

If the new summaries surface a cross-session contradiction not already listed in the Contradictions & Flags section, add a numbered entry in that section with the same format as existing entries.

---

## Step 6 — Scan for design impact

After updating `INDEX.md`, re-read the `Decisions & System Implications` sections from every summary just written.

For each decision found, identify which `CLAUDE.md` file it belongs to using this mapping:

| Decision topic | Target CLAUDE.md |
|---|---|
| Concept briefing, direction document, brief structure | `../skills/submit-brief/CLAUDE.md` |
| Market research, data sources, comp set | `../skills/market-research/CLAUDE.md` |
| Outline structure, chapter/slide logic | `../pipeline/agents/CLAUDE.md` |
| Financial model, CoStar, Excel, assumptions | `../pipeline/integrations/CLAUDE.md` or `../pipeline/agents/CLAUDE.md` |
| PowerPoint assembly, brand templates | `../pipeline/assembly/CLAUDE.md` |
| Data schemas, handoff contracts | `../pipeline/models/CLAUDE.md` |
| UI, approval workflow, review interface | `../ui/CLAUDE.md` |
| Intelligence Hub | Note separately — out of scope for this codebase |

Then:

1. Read the current content of each affected `CLAUDE.md` file.

2. Present suggested additions grouped by file, in this format:

   ```
   ../pipeline/integrations/CLAUDE.md
   → Suggested addition under "Open Questions / Blockers":
     "CoStar: [new finding from session]"
   Add this? [y/n]
   ```

3. If a decision **contradicts** something already in a `CLAUDE.md` file, flag it explicitly before suggesting any change:

   ```
   ⚠ Contradiction in ../pipeline/agents/CLAUDE.md:
     Current: "..."
     New session says: "..."
   Which is correct?
   ```

4. For each suggestion the user approves, update the relevant `CLAUDE.md` file.

**Do not update any `CLAUDE.md` file without explicit approval for each change.**

---

## Quality checks before finishing

- Every `—` from the Summary column of the rows being processed has been replaced with a `[[WikiLink]]`
- The `Decisions & System Implications` section is present in every summary, with content under both sub-headers (or an explicit "Not discussed" note)
- Key People table has no duplicate rows

---

## Notes on tone and style

- Write in third person for stakeholder summaries ("Her process…", "Ramine's assessment…")
- Write in plain, direct language — no filler phrases like "it's worth noting that" or "importantly"
- Bold the key phrase at the start of each Observation bullet; the rest of the bullet is analysis
- Do not summarise the transcript chronologically — reorganise into the section structure
- Observations should draw connections to other sessions and flag implications for the build; they are not a list of facts repeated from the sections above
- The Decisions & System Implications section should contain only things that have a direct consequence for how a system is built — not general context
