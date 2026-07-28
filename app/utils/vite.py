from pathlib import Path
import json
from flask import current_app, url_for
from markupsafe import Markup


class ViteAssets:
    def __init__(self):
        self.manifest_path = (
            Path(current_app.static_folder)
            / "dist"
            / ".vite"
            / "manifest.json"
        )

    def loadFile(self):
        with open(self.manifest_path, "r") as file:
            manifest = json.load(file)

        return manifest.get("src/main-v4.js", {})

    @property
    def cssAsset(self):
        entry = self.loadFile()

        for css_file in entry.get("css", []):
            css_url = url_for(
                "static",
                filename=f"dist/{css_file}"
            )
           
        return Markup(
            f"<link rel='stylesheet' href='{css_url}'>"
        )

    @property
    def jsAsset(self):
        entry = self.loadFile()

        js_file = entry.get("file")

        if not js_file:
            return Markup("")

        js_url = url_for(
            "static",
            filename=f"dist/{js_file}"
        )

        return Markup(
            f"<script type='module' src='{js_url}'></script>"
        )