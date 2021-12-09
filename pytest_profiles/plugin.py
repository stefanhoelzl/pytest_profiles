"""pytest plugin to define config profiles."""
# pylint: disable=protected-access
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from .profile import RegisteredProfiles, resolve_profiles


def pytest_addoption(parser: Parser) -> None:
    """Adds a profile option to pytest"""
    parser.addoption("--profile", action="append", choices=RegisteredProfiles.keys())


@pytest.mark.tryfirst
def pytest_configure(config: Config) -> None:
    """configures pytest according to the given profiles."""
    for profile in resolve_profiles(config.option.profile):
        profile.apply(config)
