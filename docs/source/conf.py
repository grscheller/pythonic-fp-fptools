"""Sphinx configuration shared by all Pythonic FP projects.

This file is identical in every pythonic-fp-* repo. What differs between
projects and between builds arrives through the environment, exported by
``docs/Makefile``:

- ``PROJECT_NAME``  display name, for example ``Gadgets``
- ``PYPI_NAME``     PyPI suffix, for example ``gadgets``
- ``DOCS_TYPE``     ``devel``, ``curr_release`` or ``prev_release``

The version is not passed in. It is read from whichever distribution is
installed in the environment running Sphinx, so the docs are always
labeled with the version of the code they were generated from.
"""

import os
from importlib.metadata import version as installed_version

from sphinx.application import Sphinx
from sphinx.errors import ConfigError

try:
    project_name = os.environ['PROJECT_NAME']
    pypi_name = os.environ['PYPI_NAME']
except KeyError as missing:
    msg = f'{missing} is not set, build with: uv run make -C docs devel'
    raise ConfigError(msg) from None

docs_type = os.environ.get('DOCS_TYPE', 'devel')
release_labels = {
    'devel': 'Proposed PyPI release',
    'curr_release': 'Current PyPI release',
    'prev_release': 'Previous PyPI release',
}
if docs_type not in release_labels:
    msg = f"unknown DOCS_TYPE '{docs_type}'"
    raise ConfigError(msg)

# -- Project information -----------------------------------------------------

project = f'Pythonic FP - {project_name}'
author = 'Geoffrey R. Scheller'
copyright = f'2023-2026, {author}'
release = installed_version(f'pythonic-fp-{pypi_name}')

rst_epilog = f"""
.. |RELEASE_STRING| replace:: **{release_labels[docs_type]} {release}**
"""

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# -- Autodoc -----------------------------------------------------------------

autodoc_default_options = {
    'members': True,
    'special-members': True,
    'show-inheritance': True,
}
autodoc_member_order = 'bysource'
autodoc_class_signature = 'separated'
autodoc_docstring_signature = False
autodoc_preserve_defaults = True

# Dunders Python creates on its own. A docstring never belongs on these, but
# some inherit one and would otherwise show up as API.
IMPLEMENTATION_DUNDERS = frozenset(
    {
        '__annotate_func__',
        '__annotations_cache__',
        '__dict__',
        '__module__',
        '__weakref__',
    }
)


def skip_implementation_dunders(
    app: Sphinx, what: str, name: str, obj: object, skip: bool, options: object
) -> bool | None:
    """Return True to skip a member, None to leave the decision to autodoc."""
    return True if name in IMPLEMENTATION_DUNDERS else None


def setup(app: Sphinx) -> None:
    app.connect('autodoc-skip-member', skip_implementation_dunders)


# -- HTML output -------------------------------------------------------------

html_theme = 'furo'
html_theme_options = {
    'light_css_variables': {'color-link--visited': 'var(--color-link)'},
    'dark_css_variables': {'color-link--visited': 'var(--color-link)'},
}
html_static_path = ['_static']
html_css_files = ['custom.css']
