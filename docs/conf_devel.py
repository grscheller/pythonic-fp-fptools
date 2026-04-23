# Configuration file for the Sphinx documentation builder.
#
# https://www.sphinx-doc.org/en/master/usage/index.html
#
# Must match what is in pyproject.toml, also delete "Proposed"
# in the release string in source/index.rst when generating
# the docs for an actual, not proposed, release.

from typing import Any
from sphinx.application import Sphinx

project = 'Pythonic FP - Functional Programming Tools'
copyright = '2023-2026, Geoffrey R. Scheller'
author = 'Geoffrey R. Scheller'
release = '5.2.1'


def skip_abc_methods(
    app: Any, what: str, name: str, obj: Any, skip: bool, options: Any
) -> bool:
    if name in [
        '__init_subclass__',
        '__subclasshook__',
        '__class_getitem__',
        '__weakref__',
    ]:
        return True  # Skip these members
    return skip


def setup(app: Sphinx) -> None:
    app.connect('autodoc-skip-member', skip_abc_methods)


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.graphviz',
]

autodoc_default_options = {
    'members': True,
    'private-members': True,
    'special-members': True,
    'inherited-members': True,
    'show-inheritance': True,
}
autodoc_member_order = 'bysource'
autoclass_content = 'both'
autodoc_class_signature = 'separated'
autodoc_typehints_format = 'short'
autodoc_use_type_comments = True
autodoc_docstring_signature = False
autodoc_preserve_defaults = True
autodoc_warningiserror = False

templates_path = ['_templates']
exclude_patterns: list[str] = []

html_theme_options = {
    'light_css_variables': {
        'color-link--visited': 'var(--color-link)',
    },
    'dark_css_variables': {
        'color-link--visited': 'var(--color-link)',
    },
}
html_theme = 'furo'
html_static_path = ['_static']
