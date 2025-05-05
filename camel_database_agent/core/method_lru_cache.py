# Copyright 2025 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
