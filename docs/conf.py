import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath("../src"))

project = "AlphaPickle"
author = "Matt Arnold"
copyright = f"{datetime.now():%Y}, {author}"

extensions = [
    "sphinx.ext.autodoc",
]

autodoc_mock_imports = []
html_theme = "furo"
