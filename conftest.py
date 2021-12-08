"""configures pytest"""
from _pytest.config import Config  # pylint: disable=protected-access

from pytest_profiles import profile

pytest_plugins = ["pytester"]


@profile(autouse=True)
def default(config: Config) -> None:
    """Setup default pytest options."""
    config.option.newfirst = True
    config.option.failedfirst = True
    config.option.tbstyle = "short"
    config.option.durations = 0
    config.option.durations_min = 1

    config.option.pylint = True
    config.option.black = True
    config.option.isort = True

    config.option.mypy = True
    config.option.mypy_ignore_missing_imports = True
    config.pluginmanager.getplugin("mypy").mypy_argv.extend(
        ["--strict", "--implicit-reexport"]
    )

    config.option.mccabe = True
    config.addinivalue_line("mccabe-complexity", "3")
