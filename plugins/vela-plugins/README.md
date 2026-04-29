# Vela Plugins

This plugin is a test to build some useful Claude skills for the vela advisory team.

## Purpose

1. Download meeting transcripts from Google Drive and store in a folder called `transcripts` (downloading via MCP so make sure that is connected)
2. Summarize transcripts and place in a `summaries` folder
3. Maintain and update an INDEX.md file containing an index of which summaries belong to which transcripts (tracking purposes for the LLM)

## Use cases

1. Track decisions made for the technical solutions of the proposal generation and market intelligence systems being designed
2. Flag inconsistencies between what was said in meetings vs the system design

## How to use this plugin

You should be able to trigger these skills via chatting normally with Claude in **Cowork**. Try saying `Can you download the latest meeting transcripts`. It will by default only give you meeting transcripts from the last 3 days.

This behaviour can be changed by editing the `sync-transcript` skill.
