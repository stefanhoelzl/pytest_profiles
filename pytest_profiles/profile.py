"""utilities to define pytest configuration profiles."""
import functools
import itertools
from collections import OrderedDict
from typing import (
    Callable,
    Generator,
    Iterable,
    List,
    MutableMapping,
    NamedTuple,
    Optional,
    Union,
    overload,
)

from _pytest.config import Config  # pylint: disable=protected-access


class PytestProfilesException(Exception):
    """Base for pytest profiles exceptions."""


class UnknownProfiles(PytestProfilesException):
    """Exception for using a unknown profile."""

    def __init__(self, unkonwn_profiles: Iterable[str]) -> None:
        super().__init__(f"unregistered profiles used: {', '.join(unkonwn_profiles)}")


class ProfileCycleDetected(PytestProfilesException):
    """Exception when an cycle in the profile definitions is detected."""

    def __init__(self, cycle: Iterable[str]) -> None:
        super().__init__(f"profile cycle detected: {' -> '.join(cycle)}")


RegisteredProfiles: MutableMapping[str, "Profile"] = OrderedDict()


_AutoUseDefault = False


class Profile(NamedTuple):
    """pytest configuration profile."""

    apply: Callable[[Config], None]
    autouse: bool = _AutoUseDefault
    uses: Optional[List[str]] = None


@overload
def profile(apply: Callable[[Config], None]) -> Profile:
    ...


@overload
def profile(
    *,
    name: Optional[str] = None,
    autouse: bool = _AutoUseDefault,
    uses: Optional[Union[str, List[str]]] = None,
) -> Callable[[Callable[[Config], None]], Profile]:
    ...


def profile(
    apply: Optional[Callable[[Config], None]] = None,
    *,
    name: Optional[str] = None,
    autouse: bool = _AutoUseDefault,
    uses: Optional[Union[str, List[str]]] = None,
) -> Union[Profile, Callable[[Callable[[Config], None]], Profile]]:
    """decorator to create pytest configuration profiles."""
    if isinstance(uses, str):
        uses = [uses]

    if apply is None:
        return functools.partial(profile, name=name, autouse=autouse, uses=uses)

    name = name or apply.__name__
    RegisteredProfiles[name] = Profile(apply=apply, autouse=autouse, uses=uses)
    return RegisteredProfiles[name]


def resolve_profiles(
    profiles: Optional[List[str]] = None,
) -> Generator[Profile, None, None]:
    """
    resolves a list of profile names and yields Profiles.

    It also yields the autouse profiles and all dependencies of the resolved profiles.
    """
    candidates = [n for n, p in RegisteredProfiles.items() if p.autouse]
    if profiles:
        candidates.extend(profiles)

    with_dependecies = itertools.chain.from_iterable(
        _with_dependencies(name) for name in candidates
    )

    deduplicated = OrderedDict((n, None) for n in with_dependecies).keys()
    _check_for_unknown_profiles(deduplicated)
    for profile_name in deduplicated:
        yield RegisteredProfiles[profile_name]


def _with_dependencies(
    profile_name: str, chain: Optional[List[str]] = None
) -> Generator[str, None, None]:
    if profile_name in RegisteredProfiles:
        chain = chain or []
        if profile_name in chain:
            raise ProfileCycleDetected([*chain, profile_name])
        for dependency in RegisteredProfiles[profile_name].uses or []:
            yield from _with_dependencies(dependency, chain=[*chain, profile_name])
    yield profile_name


def _check_for_unknown_profiles(profile_names: Iterable[str]) -> None:
    unknown = [n for n in profile_names if n not in RegisteredProfiles]
    if unknown:
        raise UnknownProfiles(unknown)
