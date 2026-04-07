import os
import sys

# Make the src layout importable by autodoc.
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

project = "pcgs_api"
copyright = "2026, Ryan A. Mannion"
author = "Ryan A. Mannion"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Autodoc -----------------------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": False,
    "show-inheritance": True,
    "special-members": "__init__",
}

# Don't repeat the type annotations in both the signature and the description.
autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"

# -- Napoleon (Google-style docstrings) --------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- MyST (Markdown support) -------------------------------------------------

myst_enable_extensions = ["colon_fence"]

# -- HTML output -------------------------------------------------------------

html_theme = "alabaster"
html_static_path = ["_static"]

html_theme_options = {
    "description": "Python client for the PCGS Public API",
    "fixed_sidebar": True,
}
