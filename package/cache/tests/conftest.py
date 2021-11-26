import pytest
from package.cache.lru_cache import LRUCache
from freezegun import freeze_time

@pytest.fixture(scope="session", autouse=True)
def cache_cap_3():
    return LRUCache(capacity=3)


@pytest.fixture(scope="session", autouse=True)
def cache_cap_5():
    return LRUCache(capacity=5)


@pytest.fixture(scope="session", autouse=True)
@freeze_time("2021-01-01 12:00")
def setup_cache_cap_3(cache_cap_3) -> None:
    """
    Set-up test cache data 
    """
    cache_cap_3.put('a', 'a')
    cache_cap_3.put('b', 'b')
    cache_cap_3.put('c', 'c')
    cache_cap_3.put('d', 'd')
    cache_cap_3.put('e', 'e')
    cache_cap_3.put('f', 'f')


@pytest.fixture(scope="session", autouse=True)
@freeze_time("2021-01-01 12:00")
def setup_cache_cap_5(cache_cap_5) -> None:
    """
    Set-up test cache data 
    """
    cache_cap_5.put('a', 'a')
    cache_cap_5.put('b', 'b')
    cache_cap_5.put('c', 'c')
    cache_cap_5.put('d', 'd')
    cache_cap_5.put('e', 'e')
    cache_cap_5.put('f', 'f')