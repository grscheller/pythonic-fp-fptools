.. Pythonic FP - Circular Array documentation master file, created by
   sphinx-quickstart on Fri Jun 27 11:13:22 2025.
   To regenerate the documentation do: ``$ Sphinx-build -M html docs/source/ docs/build/``
   from the root repo directory.

Pythonic FP - FPTools project
=============================

Part of of the `pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Overview
--------

PyPI project `pythonic.fptools <https://pypi.org/project/pythonic-fp.fptools/>`_
implements functional programming tools which endeavor to be Pythonic.

- Subclassable Boolean datatype (*module* `pythonic_fp.fptools.bool`)
- Functions as first class objects (*module* `pythonic_fp.fptools.function`)
- Lazy (non-strict) function evaluation (*module* `pythonic_fp.fptools.lazy`)
- Singletons (*module* `pythonic_fp.fptools.singletons`)

  - 3 singleton classes representing

    - a missing value (actually missing, not potentially missing)
    - a sentinel values
    - a failed calculation

- State monad implementation (*module* `pythonic_fp.fptools.state`)

  - pure FP handling of state (the state monad)
  - Classic FP implementation

    - the monad encapsulates a state transformation, not a "state"

Documentation
-------------

:doc:`Installation <installing>`
    Installing and importing the module.

:doc:`API docs <api>`
    Detailed API documentation.

Development
-----------

:doc:`changelog`
    CHANGELOG for the current and predecessor projects.

.. Hidden TOCs

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api

.. toctree::
   :caption: Development
   :maxdepth: 2
   :hidden:

   changelog

