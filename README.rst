====================================
Pythonic FP - Functional programming
====================================

Functional programming tools which endeavor to be Pythonic, part of the
`PyPI pythonic-fp Namespace Projects <https://github.com/grscheller/pythonic-fp/blob/main/README.rst>`_.

Detailed API documentation
`documentation <https://grscheller.github.io/pythonic-fp/maintained/fptools>`_
on *GH-Pages*.

Features:
---------

- Benefits of FP

  - improved composability
  - avoid hard to refactor exception driven code paths
  - data sharing becomes trivial when immutability leveraged

The `pythonic_fp.fptools` package currently consists of 5 modules.

**Warning:** The maintainer intends to break out some of the pythonic-fp.fptools
submodules sometime in the near future.

Subclassable Boolean datatype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- *module* `pythonic_fp.fptools.bool`

  - Python bool cannot be Subclassed
  - this version can

    - *class* `Bool` is subclassable

      - *class* `Truth` instantiates "truthy" objects 
      - *class* `Lie` instantiates "falsy" objects 

  - can have different "flavors" of truths and lies

    - each being a singleton
    - compare with

      - `==` and `!=` for purely boolean comparisons
      - `is` and `is not` if the type of truth matters

Functions as first class objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - *module* `pythonic_fp.fptools.function`

    - utilities to manipulate and partially apply functions

Lazy function evaluation
^^^^^^^^^^^^^^^^^^^^^^^^

- *module* `pythonic_fp.fptools.lazy`

  - lazy (non-strict) function evaluation

Singletons
^^^^^^^^^^

- *module* `pythonic_fp.fptools.singletons`

  - 3 singleton classes representing

    - a missing value (actually missing, not potentially missing)
    - a sentinel value
    - a failed calculation

State monad implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^

- *module* `pythonic_fp.fptools.state`

  - pure FP handling of state (the state monad)
  - Classic FP implementation

    - the monad encapsulates a state transformation, not a "state"

Installation:
-------------

| $ pip install pythonic-fp.fptools

Contribute:
-----------

- Project on PyPI: https://pypi.org/project/pythonic-fp.fptools
- Source Code: https://github.com/grscheller/pythonic-fp-fptools
- Issue Tracker: https://github.com/grscheller/pythonic-fp-fptools/issues
- Pull Requests: https://github.com/grscheller/pythonic-fp-fptools/pulls
- CHANGELOG: https://github.com/grscheller/pythonic-fp-fptools/blob/main/CHANGELOG.rst

+------------------------------------------------+----------------------+--------------------+
| Contributors                                   | Name                 | Role               |
+================================================+======================+====================+
| `@grscheller <https://github.com/grscheller>`_ | Geoffrey R. Scheller | author, maintainer |
+------------------------------------------------+----------------------+--------------------+

License Information
^^^^^^^^^^^^^^^^^^^

This project is licensed under the Apache License Version 2.0, January 2004.

See the `LICENCE file <https://github.com/grscheller/pythonic-fp-fptools/blob/main/LICENSE>`_
for details.
