# pylint: disable=missing-module-docstring,missing-function-docstring,redefined-outer-name
import pytest
from _pytest.config import Config  # pylint: disable=protected-access

from pytest_profiles.profile import RegisteredProfiles, profile, resolve_profiles


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
    assert not profile(lambda c: None).autouse
    assert not profile()(lambda c: None).autouse
    assert profile(autouse=True)(lambda c: None).autouse


def test_uses() -> None:
    profile(name="single")(lambda c: None)
    profile(name="first")(lambda c: None)
    profile(name="second")(lambda c: None)

    assert profile(lambda c: None).uses is None
    assert profile()(lambda c: None).uses is None
    assert profile(uses="single")(lambda c: None).uses == ["single"]
    assert profile(uses=["first", "second"])(lambda c: None).uses == ["first", "second"]


def test_resolve_profiles_arguments() -> None:
    _profile = profile(name="profile")(lambda c: None)
    assert list(resolve_profiles(profiles=["profile"])) == [_profile]


def test_resolve_profiles_autouse() -> None:
    first = profile(name="first", autouse=True)(lambda c: None)
    second = profile(name="second")(lambda c: None)
    assert list(resolve_profiles(profiles=["second"])) == [first, second]


def test_resolve_profiles_no_duplicates() -> None:
    single = profile(name="single", autouse=True)(lambda c: None)
    assert list(resolve_profiles(profiles=["single"])) == [single]


def test_resolve_profiles_dependencies() -> None:
    first = profile(name="first")(lambda c: None)
    second = profile(name="second", autouse=True, uses="first")(lambda c: None)
    assert list(resolve_profiles()) == [first, second]


def test_resolve_profiles_keep_order() -> None:
    first = profile(name="first", autouse=True)(lambda c: None)
    second = profile(name="second", autouse=True)(lambda c: None)
    assert list(resolve_profiles(profiles=["first"])) == [first, second]


def test_resolve_profiles_value_error_on_unregistered_profile() -> None:
    with pytest.raises(ValueError):
        list(resolve_profiles(profiles=["first"]))
