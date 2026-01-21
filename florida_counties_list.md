# Grok Prompt: Florida Counties Catalog

You are Grok. Search authoritative sources and compile a complete catalog of
all counties in the State of Florida. Return the counties in alphabetical
order and list each county's county seat and population.

Requirements:
- Include all 67 Florida counties.
- Sort alphabetically by county name.
- Provide population figures using the most recent official data available.
- Use consistent units and clarify the population year.
- Cite sources for every population value.
- Cite the total geographical area in square miles
- Cite the total marine shore line in statute miles

Output format:
Return a markdown table with these columns:
1) County
2) County Seat
3) Population (year)
4) Source URL
5) Geographical Area
6) Total Marine Shoreline

If any population value is missing or unclear, note "Unknown" and explain why
in a short footnote below the table.
