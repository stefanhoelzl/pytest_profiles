"""configures pytest"""
from _pytest.config import Config  # pylint: disable=protected-access

from pytest_profiles import profile

pytest_plugins = ["pytester"]


@profile(autouse=True, uses=["mypy", "mccabe"])
def default(config: Config) -> None:
    """Setup default pytest options."""
    config.option.newfirst = True
    config.option.failedfirst = True
    config.option.tbstyle = "short"
    config.option.durations = 0
    config.option.durations_min = 1

    config.option.black = True
    config.option.isort = True

    if config.option.file_or_dir or config.option.keyword:
        config.option.verbose = 1
    else:
        config.option.pylint = True


@profile
def ci(config: Config) -> None:  # pylint: disable=invalid-name
    """profile to run in CI"""
    config.option.newfirst = False
    config.option.failedfirst = False
    config.option.verbose = 1
    config.option.cacheclear = True


@profile
def quick(config: Config) -> None:
    """profile skipping slow checks."""
    config.option.pylint = False


@profile(uses="ci")
def compatibility(config: Config) -> None:
    """disable quality checks for compatibility checks."""
    config.option.pylint = False
    config.option.black = False
    config.option.isort = False
    config.option.mypy = False
    config.option.mccabe = False
    config.option.pylint = False


@profile
def mypy(config: Config) -> None:
    """profile for mypy."""
    config.option.mypy = True
    config.option.mypy_ignore_missing_imports = True
    try:
        config.pluginmanager.getplugin("mypy").mypy_argv.extend(
            ["--strict", "--implicit-reexport"]
        )
    except AttributeError:
        pass


@profile
def mccabe(config: Config) -> None:
    """profile for mccabe code complexity"""
    config.option.mccabe = True
    try:
        config.addinivalue_line("mccabe-complexity", "4")
    except ValueError:
        pass
