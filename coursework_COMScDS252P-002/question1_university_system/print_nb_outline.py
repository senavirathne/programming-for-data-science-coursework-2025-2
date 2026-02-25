import json

with open('university_system_interactive.ipynb', 'r') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        first_line = "empty"
        if len(cell['source']) > 0:
            first_line = cell['source'][0].strip()
        print(f"Code Cell {i} (lines: {len(cell.get('source', []))}): {first_line}")
    elif cell.get('cell_type') == 'markdown':
        first_line = "empty"
        if len(cell.get('source', [])) > 0:
            first_line = cell['source'][0].strip()
        print(f"Markdown Cell {i}: {first_line}")
