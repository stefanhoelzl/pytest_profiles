"""utilities to define pytest configuration profiles."""
import functools
from collections import OrderedDict
from typing import Callable, MutableMapping, NamedTuple, Optional, Union, overload

from _pytest.config import Config  # pylint: disable=protected-access

RegisteredProfiles: MutableMapping[str, "Profile"] = OrderedDict()


_AutoUseDefault = False


class Profile(NamedTuple):
    """pytest configuration profile."""

    apply: Callable[[Config], None]
    autouse: bool = _AutoUseDefault


@overload
def profile(apply: Callable[[Config], None]) -> Profile:
    ...


@overload
def profile(
    *, name: Optional[str] = None, autouse: bool = _AutoUseDefault
) -> Callable[[Callable[[Config], None]], Profile]:
    ...


def profile(
    apply: Optional[Callable[[Config], None]] = None,
    *,
    name: Optional[str] = None,
    autouse: bool = _AutoUseDefault
) -> Union[Profile, Callable[[Callable[[Config], None]], Profile]]:
    """decorator to create pytest configuration profiles."""
    if apply is None:
        return functools.partial(profile, name=name, autouse=autouse)

    name = name or apply.__name__
    RegisteredProfiles[name] = Profile(apply=apply, autouse=autouse)
    return RegisteredProfiles[name]
