#!/usr/bin/env python
# Generate conf.py Sphinx configuration executable

import sys

project_prefix = 'Pythonic FP'
pypi_prefix = 'pythonic-fp'
author = 'Geoffrey R. Scheller'
copyright = f'2023-2026, {author}'

args = sys.argv[1:]
num_args = len(args)

if num_args == 4:
    build_type, version, project_name, pypi_name = args
    project = project_prefix + ' - ' + project_name
    pypi_project_repo = pypi_prefix + '-' + pypi_name
    project_url_rst = f'`{project} <https://pypi.org/project/{pypi_project_repo}/>`_'
    homepage_url_rst = (
        f'`{project_prefix} <https://grscheller.github.io/{pypi_prefix}/>`_'
    )
else:
    sys.exit('Error: gen_conf.py takes exactly 4 arguments')

release = f'{version}'
match build_type:
    case 'curr_release':
        release_string = f'**Current PyPI release {release}**'
    case 'devel':
        release_string = f'**Proposed PyPI release {release}**'
    case 'prev_release':
        release_string = (
            f'**Last PyPI release {release} from previous rolling release**'
        )
    case _:
        sys.exit(f'Error: unknown built_type {build_type} given')

print(f'''# Generated conf.py Sphinx configuration executable

from typing import Any
from sphinx.application import Sphinx

project = '{project}'
author = '{author}'
copyright = '{copyright}'
release = '{release}'
release_string = '{release_string}'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.graphviz',
]

autodoc_default_options = {{
    'members': True,
    'private-members': True,
    'special-members': True,
    'inherited-members': False,
    'show-inheritance': True,
}}
autodoc_member_order = 'bysource'
autoclass_content = 'class'
autodoc_class_signature = 'separated'
autodoc_typehints_format = 'short'
autodoc_use_type_comments = True
autodoc_docstring_signature = False
autodoc_preserve_defaults = True
autodoc_warningiserror = False

templates_path = ['_templates']
exclude_patterns: list[str] = []

html_theme_options = {{
    'light_css_variables': {{
        'color-link--visited': 'var(--color-link)',
    }},
    'dark_css_variables': {{
        'color-link--visited': 'var(--color-link)',
    }},
}}
html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['custom.css']

rst_epilog = """
.. |RELEASE_STRING| replace:: {release_string}

"""
''')
