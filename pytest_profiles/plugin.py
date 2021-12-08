"""pytest plugin to define config profiles."""
# pylint: disable=protected-access
import pytest
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from .profile import RegisteredProfiles


def pytest_addoption(parser: Parser) -> None:
    """Adds a profile option to pytest"""
    parser.addoption("--profile", action="append", choices=RegisteredProfiles.keys())


@pytest.mark.tryfirst
def pytest_configure(config: Config) -> None:  # pylint: disable=unused-argument
    """configures pytest according to the given profiles."""
    profiles = [profile for profile in RegisteredProfiles.values() if profile.autouse]
    if config.option.profile is not None:
        profiles.extend(
            [RegisteredProfiles[profile] for profile in config.option.profile]
        )
    for profile in profiles:
        profile.apply(config)
