# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name
import pytest
from _pytest.config import Config  # pylint: disable=protected-access

from pytest_profiles.profile import RegisteredProfiles, profile


def test_create_and_apply(pytester: pytest.Pytester) -> None:
    @profile
    def test_profile(config: Config) -> None:
        config.option.verbose = 0

    config = pytester.parseconfig("-v")
    assert config.option.verbose == 1

    RegisteredProfiles["test_profile"].apply(config)
    assert config.option.verbose == 0


def test_register_custom_name() -> None:
    profile(name="custom")(lambda c: None)
    assert "custom" in RegisteredProfiles


def test_autouse() -> None:
    assert not profile(name="custom")(lambda c: None).autouse
    assert profile(name="custom", autouse=True)(lambda c: None).autouse
