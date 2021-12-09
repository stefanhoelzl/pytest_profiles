# pylint: disable=missing-module-docstring,missing-function-docstring
import os


def test_compatibility() -> None:
    env_vars_to_check = [
        "PYTEST_PROFILE_AUTOUSE",
        "PYTEST_PROFILE_CUSTOM_NAME",
        "PYTEST_PROFILE_DEPENDENCY",
        "PYTEST_PROFILE_USES",
    ]
    for env_var in env_vars_to_check:
        if env_var in os.environ:
            assert (
                os.environ[env_var] == "done"
            ), f"{env_var} compatibility check failed."
