---
name: sync-transcripts
description: Queries the google drive MCP for new meeting transcripts and downloads them to a local folder
---

# Sync Transcripts from Google Drive

Pull any meeting transcripts from Google Drive that aren't already in `transcripts/`, extract the transcript-only portion, and save them as markdown matching the existing format.

Default lookback is **3 days**. If the user gives a date range or different lookback, use that.

## Step 1 — Search Google Drive

Use `mcp__claude_ai_Google_Drive__search_files` with `excludeContentSnippets: true` (snippets blow up the output).

Query template — adjust `modifiedTime` to today minus the lookback window:

```
(title contains 'transcript' or title contains 'Transcript' or title contains 'Meeting' or title contains 'Notes by Gemini' or title contains 'Recording') and modifiedTime > 'YYYY-MM-DDT00:00:00Z'
```

## Step 2 — Cross-reference against `transcripts/`

List the local folder. For each Drive file, check whether a local `.md` already covers that meeting (match on date + topic, not exact title — local names are abbreviated, e.g. Drive's `BD AI System - India Country Partner Session - 2026/04/22 14:23 - Notes by Gemini` → local `2026-04-22_BD_AI_India_Country_Partner.md`).

Report the missing files to the user before downloading. If two Drive files map ambiguously to two local files (same date, same topic), flag it rather than guessing.

## Step 3 — Confirm before downloading

Ask the user which missing transcripts to pull. Do not auto-download all of them.

## Step 4 — Fetch and extract

For each confirmed file, call `mcp__claude_ai_Google_Drive__read_file_content` with the `fileId`.

The Drive file contains both **Notes** and **Transcript** sections. Extract **only** the transcript: everything from the `## <title> - Transcript` heading down to (and including) `### Transcription ended after HH:MM:SS`. Drop the Gemini disclaimer line that follows.

**After the tool call, choose the right path based on what came back:**

### Path A — Content returned inline
The full file content is in the tool result directly. Apply the cleaning rules below, then use the **Write tool** to save the file. Do not write a script.

### Path B — Content saved to a file (too large for inline)
The tool result says the output was saved to a path like:
```
<YOUR_HOME>/.claude/projects/<PROJECT_HASH>/tool-results/mcp-claude_ai_Google_Drive-read_file_content-*.txt
```
Run the extraction script:
```
python3 ".claude/scripts/extract_transcript.py" "<saved_tool_result_path>" "<output_transcript_path>" "<MMM D, YYYY>"
```
The script handles JSON parsing, transcript extraction, and cleaning automatically. See `.claude/scripts/extract_transcript.py` for full details.

## Step 5 — Clean the content

*(Only needed for Path A — Path B handles this automatically via the script.)*

The raw content has JSON escapes and markdown bold that don't match the existing format. Apply these substitutions:

- `**Speaker:**` → `Speaker:` (strip bold from speaker labels)
- `\&` → `&`
- `\*` → `*`
- `\[` → `[`
- `\]` → `]`
- Preserve trailing two-space line breaks (`  ` at line ends) — they render as line breaks in markdown

## Step 6 — Save the file

Filename: `YYYY-MM-DD_Snake_Case_Topic.md` in `transcripts/`. Strip "BD AI System -", "Notes by Gemini", and timestamps from the title; keep it short and topic-focused. Examples:

- Drive: `BD AI System - Director of Technical Services & Projects Session - 2026/04/24 11:00 - Notes by Gemini`
- Local: `2026-04-24_BD_AI_Director_Technical_Services.md`

File structure (match existing files exactly):

```

MMM D, YYYY
## <Original meeting title> - Transcript

### 00:00:00

Speaker: line one  
Speaker: line two  

### 00:01:29

Speaker: ...
```

Note: file starts with a blank line, then the date, then the `##` title.

## Step 7 — Update INDEX.md

For each newly saved transcript, add a row to the matching table in `INDEX.md`. Pick the section by meeting type:

| Section | When to use |
|---|---|
| Stakeholder Interviews — Kerten Team | 1:1 sessions with a Kerten employee (e.g. `BD AI System - <Role>`) |
| Intelligence Hub Sessions | Lead sourcing / market intelligence sessions |
| Kickoff & Progress Meetings | Stream kickoffs, weekly progress reviews |
| Technical Design Sessions | Architecture / workflow / KH Technical sessions |
| Vela Internal Check-ins | `Check-in | Kerten AI Acceleration program` |

Use `—` in the Summary column (the `/summarize-transcripts` command picks up these pending rows). Match the column structure of the target table — they differ between sections. Date format: `MMM D` (e.g. `Apr 24`). Insert the row in date order.

## Step 8 — Report back

Summarize what was added: filename(s), date(s), approximate duration (from the final `### Transcription ended after` timestamp), and which INDEX.md section(s) you updated.
