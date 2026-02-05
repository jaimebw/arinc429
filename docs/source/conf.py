import os
import sys

sys.path.insert(0, os.path.abspath("../.."))

project = "PyArinc429"
author = "Jaime Bowen Varela"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True
autodoc_member_order = "bysource"

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
