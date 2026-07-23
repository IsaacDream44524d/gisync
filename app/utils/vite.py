import json
from pathlib import Path
from flask import current_app, url_for
from markupsafe import Markup

def vite_assets():
    # 1. Safely build the path to the manifest
    manifest_path = Path(current_app.static_folder) / "dist" / ".vite" / "manifest.json"

    # 2. Read the manifest file
    with open(manifest_path, 'r') as file:
        manifest = json.load(file)
        
    entry = manifest.get("src/main-v4.js", {})
    if not entry:
        return Markup("") # Return empty string if entry doesn't exist
        
    tags = []

    # 3. Generate CSS tags using Python's url_for directly
    for css_file in entry.get('css', []):
        css_url = url_for('static', filename=f"dist/{css_file}")
        tags.append(f"<link rel='stylesheet' href='{css_url}'>")

    # 4. Generate JS tag
    js_file = entry.get('file')
    if js_file:
        js_url = url_for('static', filename=f"dist/{js_file}")
        tags.append(f"<script type='module' src='{js_url}'></script>")

    # 5. Join safely with safe newlines
    return Markup("\n".join(tags))
