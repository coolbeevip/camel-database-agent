from functools import lru_cache
from typing import Any, Callable, TypeVar, cast

R = TypeVar('R')


def method_lru_cache(maxsize: int = 128):
    """A decorator that applies lru_cache to a method safely."""

    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        cache = lru_cache(maxsize=maxsize)(func)

        def wrapper(self, *args: Any, **kwargs: Any) -> R:
            return cast(R, cache(self, *args, **kwargs))

        wrapper.cache_clear = cache.cache_clear  # type: ignore[attr-defined]
        wrapper.cache_info = cache.cache_info  # type: ignore[attr-defined]
        return wrapper

    return decorator
