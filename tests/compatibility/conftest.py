"""configures the compatibility tests"""
# pylint: disable=missing-function-docstring,unused-argument
import os

from _pytest.config import Config  # pylint: disable=protected-access

from pytest_profiles import profile


@profile(autouse=True)
def autouse(config: Config) -> None:
    os.environ["PYTEST_PROFILE_AUTOUSE"] = "done"


@profile(name="custom")
def custom_name(config: Config) -> None:
    os.environ["PYTEST_PROFILE_CUSTOM_NAME"] = "done"


@profile
def dependency(config: Config) -> None:
    os.environ["PYTEST_PROFILE_DEPENDENCY"] = "done"


@profile(uses="dependency")
def uses(config: Config) -> None:
    os.environ["PYTEST_PROFILE_USES"] = "done"
