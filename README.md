# pytest_profiles
[![Build Status](https://github.com/stefanhoelzl/pytest_profiles/workflows/push/badge.svg)](https://github.com/stefanhoelzl/pytest_profiles/actions)
[![Coverage](https://img.shields.io/badge/coverage-100%25-success?style=flat)](https://stefanhoelzl.github.io/pytest_profiles)
[![PyPI](https://img.shields.io/pypi/v/pytest_profiles.svg)](https://pypi.org/project/pytest_profiles/)
[![Downloads](https://img.shields.io/pypi/dm/pytest_profiles?color=blue&logo=pypi&logoColor=yellow)](https://pypistats.org/packages/pytest_profiles)
[![License](https://img.shields.io/pypi/l/pytest_profiles.svg)](LICENSE)

pytest plugin to create configuration profiles.

## Installation
```bash
$ pip install pytest_profiles
```

## Usage
Define your pytest configurations in a `conftest.py`.
```python
# conftest.py
from pytest_profiles import profile
from _pytest.config import Config


@profile(autouse=True)
def default(config: Config) -> None:
    """
    sets pytest configuration options 
    which are always applied (autouse=True)
    """
    config.option.verbose = 1


@profile
def custom(config: Config) -> None:
    """
    sets pytest configuration options 
    only when `--profile custom` argument is applied.
    """
    config.option.newfirst = True
    config.option.failedfirst = True
```

activate profiles by passing command line arguments to pytest
```bash
# pytest runs with verbosity=1 by default
$ pytest

# pytest runs new and failed tests first
$ pytest --profile custom  
```

It is also possible to define dependencies between profiles
```python
# conftest.py
from pytest_profiles import profile
from _pytest.config import Config


@profile
def base(config: Config) -> None:
    config.option.newfirst = True
    config.option.failedfirst = True


@profile(uses=["base"])
def sub(config: Config) -> None:
    """the sub profile also includes the configuration of the base profile."""
    config.option.verbose = 1
```

see [conftest.py](conftest.py) for more examples.
