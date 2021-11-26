from typing import Union
import pytest
from package.cache.lru_cache import LRUCache
from freezegun import freeze_time

@pytest.mark.parametrize(
    "key, val", [
        ("color", -1),
        ("a", -1),
        ("b", -1),
        ("c", -1),
        ("d", "d"),
        ("e", "e"),
        ("f", "f"),
    ]
)
@freeze_time("2021-01-01 12:01")
def test_get_key_cap_3(cache_cap_3: LRUCache, key: str, val: str) -> Union[int, str]:
    resp = cache_cap_3.get(f'{key}')
    assert resp == val


@pytest.mark.parametrize(
    "key, val", [
        ("x", -1),
        ("a", -1),
        ("b", "b"),
        ("c", "c"),
        ("d", "d"),
        ("e", "e"),
        ("f", "f"),
    ]
)
@freeze_time("2021-01-01 12:02")
def test_get_key_cap_5(cache_cap_5: LRUCache, key: str, val: str) -> Union[int, str]:
    resp = cache_cap_5.get(f'{key}')
    assert resp == val


@pytest.mark.parametrize(
    "key, val", [
        ("d", -1),
        ("e", -1),
        ("f", -1),
    ]
)
@freeze_time("2021-01-01 12:10")
def test_expired_cache_key(cache_cap_3: LRUCache, key: str, val: str) -> Union[int, str]:
    resp = cache_cap_3.get(f'{key}')
    assert resp == val
