import json
import re

# Load source
with open('working/0100F7E00C70E000_Hogwarts/split_tasks/spells_and_potions.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Loaded {len(items)} items.")
