#!/usr/bin/env python3

import json
import re

# Wraps text blocks in <p> tags, ignoring blocks that look like HTML.
# A block is any text separated by one or more blank lines (2+ \n).  
def AutoParagraph(text: str) -> str:
	if not text:
		return ""
	paragraphs = []
	blocks = re.split(r'\n\s*\n', text.strip())
	for block in blocks:
		stripped_block = block.strip()
		if stripped_block.startswith('<') or stripped_block.endswith('>'):
			paragraphs.append(stripped_block)
		else:
			paragraphs.append(f"<p>{stripped_block}</p>")
	return "\n\n".join(paragraphs)

# Removes HTML tags and comments from a string using regular expressions.
# Will remove items similar to <b> <div> </div> and &rarr;
def StripHTML(HTML_Text: str) -> str:	
	cleaner = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	clean_text = re.sub(cleaner, '', HTML_Text)
	return clean_text

# Removes non-base64 characters from text
def toJSONStr(raw_text: str) -> str:
	raw_text = raw_text.strip()
	if not raw_text:
		return ""
	return json.dumps(raw_text)[1:-1]