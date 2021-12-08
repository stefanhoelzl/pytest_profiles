# pylint: disable=missing-module-docstring,missing-function-docstring,unused-argument
from itertools import chain
from typing import List

import pytest
from _pytest.config import Config
from _pytest.config.exceptions import UsageError

from pytest_profiles.profile import Profile, RegisteredProfiles


@pytest.mark.parametrize("profiles", [["single"], ["first", "second"]])
def test_addoption(pytester: pytest.Pytester, profiles: List[str]) -> None:
    for profile in profiles:
        RegisteredProfiles[profile] = Profile(lambda c: None)

    config = pytester.parseconfig(
        *chain.from_iterable(("--profile", profile) for profile in profiles)
    )

    assert config.option.profile == profiles


def test_addoption_usage_error(pytester: pytest.Pytester) -> None:
    with pytest.raises(UsageError):
        pytester.parseconfig("--profile")

    with pytest.raises(UsageError):
        pytester.parseconfig("--profile", "unregistered")


def test_configure(pytester: pytest.Pytester) -> None:
    def set_verbose(config: Config) -> None:
        config.option.verbose = 1

    RegisteredProfiles["profile"] = Profile(apply=set_verbose)

    config = pytester.parseconfigure()
    assert config.option.verbose == 0

    config = pytester.parseconfigure("--profile", "profile")
    assert config.option.verbose == 1


def test_configure_autouse(pytester: pytest.Pytester) -> None:
    def set_verbose(config: Config) -> None:
        config.option.verbose = 1

    RegisteredProfiles["profile"] = Profile(apply=set_verbose, autouse=True)

    config = pytester.parseconfigure()

    assert config.option.verbose == 1
