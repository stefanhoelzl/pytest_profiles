# pylint: disable=missing-module-docstring,missing-function-docstring
import pytest

from pytest_profiles.profile import RegisteredProfiles


@pytest.fixture(autouse=True)
def clear_registered_profiles() -> None:
    RegisteredProfiles.clear()
