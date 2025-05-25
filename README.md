# Pythonic FP - Pythonic functional programming

Functional programming tools which endeavor to be Pythonic. This project
is part of the [Pythonic FP][1] **pythonic-fp** PyPI namespace projects.

- **Repositories**
  - [pythonic-fp.fptools][2] project on *PyPI*
  - [Source code][3] on *GitHub*
- Detailed documentation for pythonic-fp.fptools
  - [Detailed API documentation][4] on *GH-Pages*

**Warning:** The maintainer intends to break up the pythonic-fp.fptools
repo sometime in the near future.

## Overview

- Benefits of FP
  - improved composability
  - avoid hard to refactor exception driven code paths
  - data sharing becomes trivial when immutability leveraged

The `pythonic_fp.fptools` package consists of 5 modules.
___

### Subclassable Boolean datatype

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

___

### Functions as first class objects

  - *module* `pythonic_fp.fptools.function`
    - utilities to manipulate and partially apply functions

___

### Lazy function evaluation

- *module* `pythonic_fp.fptools.lazy`
  - lazy (non-strict) function evaluation

___

### Singletons

- *module* `pythonic_fp.fptools.singletons`
  - 3 singleton classes representing
    - a missing value (actually missing, not potentially missing)
    - a sentinel value
    - a failed calculation

___

### State monad implementation

- *module* `pythonic_fp.fptools.state`
  - pure FP handling of state (the state monad)

___

[1]: https://github.com/grscheller/pythonic-fp/blob/main/README.md
[2]: https://pypi.org/project/pythonic-fp.fptools/
[3]: https://github.com/grscheller/pythonic-fp-fptools/
[4]: https://grscheller.github.io/pythonic-fp/maintained/fptools/
