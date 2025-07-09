..
   Pythonic FP - FPTools documentation master file. To regenerate the sphinx
   documentation do: "$ make html" from the "docs/" directory.

Pythonic FP - FPTools
=====================

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

Part of of the
`pythonic-fp namespace projects <https://github.com/grscheller/pythonic-fp/blob/main/README.md>`_.

Documentation
-------------

:doc:`Current Development API <api>`
    Development environment API documentation.

:doc:`CHANGELOG <changelog>`
    For the current and predecessor projects.

.. toctree::
   :caption: Documentation
   :maxdepth: 2
   :hidden:

   installing
   api_pypi
   api

.. toctree::
   :caption: Development
   :maxdepth: 1
   :hidden:

   changelog

.. toctree::
   :caption: Back to start
   :maxdepth: 1
   :hidden:

   self
