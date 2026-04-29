"""
Extract and clean a transcript from a saved Google Drive tool result file.

Usage:
    python3 extract_transcript.py <tool_result_json> <output_md> [date_str]

Args:
    tool_result_json  Path to the saved tool result file (JSON with {fileContent: string})
    output_md         Path to write the cleaned markdown transcript
    date_str          Optional date string for the file header (e.g. "Apr 27, 2026").
                      If omitted, the script attempts to extract it from the file content.

The script:
  1. Parses the JSON and extracts fileContent
  2. Locates the transcript section (## <title> - Transcript heading)
  3. Extracts to and including the ### Transcription ended after HH:MM:SS line
  4. Cleans formatting: strips **bold** from speaker labels, fixes JSON escapes
  5. Writes the cleaned content with a blank first line, date, then the transcript

Exit codes: 0 = success, 1 = error (message printed to stderr)
"""

import json
import re
import sys


def find_date(content):
    match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}, \d{4}', content)
    return match.group(0) if match else None


def extract_transcript(content):
    # Find the transcript heading: ## <anything> - Transcript
    start_match = re.search(r'## .+? - Transcript\n', content)
    if not start_match:
        # Fallback: find first timestamp heading
        start_match = re.search(r'\n\n### 00:00:00\n', content)
        if not start_match:
            raise ValueError("Could not find transcript section in file content")
        start = start_match.start() + 2  # skip leading \n\n
    else:
        start = start_match.start()

    # Find the end marker
    end_match = re.search(r'### Transcription ended after \d{2}:\d{2}:\d{2}', content[start:])
    if not end_match:
        raise ValueError("Could not find 'Transcription ended after' marker")

    end_pos = start + end_match.end()
    # Include the newline after the end marker
    if end_pos < len(content) and content[end_pos] == '\n':
        end_pos += 1

    return content[start:end_pos]


def clean(text):
    # Strip bold from speaker labels: **Name:** -> Name:
    text = re.sub(r'\*\*([^*\n]+:)\*\*', r'\1', text)
    # Fix JSON/markdown escapes
    text = text.replace(r'\&', '&')
    text = text.replace(r'\*', '*')
    text = text.replace(r'\[', '[')
    text = text.replace(r'\]', ']')
    return text


def main():
    if len(sys.argv) < 3:
        print("Usage: extract_transcript.py <tool_result_json> <output_md> [date_str]", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    date_override = sys.argv[3] if len(sys.argv) > 3 else None

    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    content = data['fileContent']

    date_str = date_override or find_date(content) or 'Unknown date'

    try:
        transcript = extract_transcript(content)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    cleaned = clean(transcript)
    output = f'\n{date_str}\n{cleaned}'

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Written: {output_path} ({len(output)} chars)")


if __name__ == '__main__':
    main()
