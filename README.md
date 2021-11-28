# redis-proxy

A simple redis proxy on:
- HTTP server using a Flask app served through Gunicorn and simple read-through caching for redis GET commands. 
- TCP server using a simple python socket server and read-through caching for redis GET commands.

**Project overview:**
- `HTTP web service` - Clients interface to the Redis proxy through HTTP, with the
  Redis “GET” command mapped to the HTTP “GET” method.
- `TCP Client` - Clients interface to the Redis proxy over TCP socket, through a subset of Redis Protocol (RESP GET command)
- `Single backing instance` - Each instance of the proxy service is associated with a single
  Redis service instance called the “backing Redis”. The address of the backing Redis is configured 
  at proxy startup.
- `Cached GET` - A GET request, directed at the proxy, returns the value of the
  specified key from the proxy’s local cache if the local cache
  contains a value for that key. If the local cache does not contain
  a value for the specified key, it fetches the value from the
  backing Redis instance, using the Redis GET command, and
  stores it in the local cache, associated with the specified key.
- `Global expiry` - Values added to the local cache are expired after being in the
  cache for a time duration that is globally configured per
  instance. After a value expires, a GET request to it will act as if
  the value associated with the key has never been stored in the
  cache.
- `LRU eviction` - Once the cache fills to capacity, the least recently used (i.e.
  read) key is evicted each time a new key needs to be added to
  the cache.
- `Fixed key size` - The cache capacity is configured in terms of the number of
  keys it retains.

**HTTP Proxy specific additional features:**
- `Parallel concurrent processing` - Multiple clients are able to concurrently
  connect to the proxy (up to some configurable maximum limit). When
  multiple clients make concurrent requests to the proxy, it would execute a 
  number of these requests (up to some configurable limit) in parallel.
- `Concurrent client limit` - The maximum number of clients that can
  concurrently be served by the proxy is configured at proxy startup.

## Architecture Overview

A GET request, directed at the proxy, returns the value of the specified key from the proxy’s local 
cache if the local cache contains a value for that key. If the local cache does not contain
a value for the specified key, it fetches the value from the backing Redis instance, and
stores it in the local cache, associated with the specified key.

### cache

  The cache is implemented as an LRU cache. `CACHE_GLOBAL_EXPIRY` and `CACHE_CAPACITY` can be configured at proxy startup.
  Any different cache implementation can be switched easily.

### redis

The backing redis instance for the proxy is configurable using:
- For HTTP proxy: 
  - BACKING_REDIS_HOST_HTTP
  - BACKING_REDIS_PORT_HTTP

- For TCP proxy:
  - BACKING_REDIS_HOST_TCP
  - BACKING_REDIS_PORT_TCP

These are made available to the respective proxy service at proxy startup.
If there is any error in fetching the value from backing redis, or unable to connect to backing redis, returns `Error getting key: {key}`

### HTTP server

The HTTP server handling `GET` requests. 
- A `GET` request to the endpoint `/get/{key}` first attempts to fetch a value from the cache, if unavailable, fetches the value from backing redis. 
- If value is not available in the backing redis either, displays `{key} not found!`. 

Flask app served through Gunicorn helps achieve parallel concurrent access, values for MAX_CLIENTS and MAX_REQUESTS configurable from [`.env`](#environment-variables) 

### TCP server

The TCP server handling Redis Protocol `GET` commands.
- A `GET {key}` RESP request first attempts to fetch a value from the cache, if unavailable, fetches the value from backing redis. 
- If value is not available in the backing redis either, displays `{key} not found!`. 

## Code Implementation

Directory structure for client containers:
- [HTTP Proxy](#http-server):
    ```
    - app
      - routes
        - __init__.py
        - routes.py
      - package
        - cache
          - lru_cache.py
        - proxy
          - proxy_service.py
          - resp_parser.py
        - redis
          - client.py
      - tests
        - test_routes
          - __init__.py
          - conftest.py
          - test_routes.py
      - requirements.txt
      - wsgi.py
    ```

- [TCP Proxy](#tcp-server):
    ```
    - tcp_server
      - server.py
      - package
        - cache
          - lru_cache.py
        - proxy
          - proxy_service.py
          - resp_parser.py
        - redis
          - client.py
      - tests
        - test_tcp_server
          - __init__.py
          - conftest.py
          - test_routes.py
        - test_cache
            - __init__.py
            - conftest.py
            - test_cache.py
      - requirements.txt
      - wsgi.py
    ```

**Package module:**

***`cache/lru_cache.py`***

The [cache](#cache) is implemented as an LRU cache.

- `lru_cache.py`

    - `__init__(self, capacity: int = 5, expiry: int = sys.maxsize, debug: bool = False) -> None`
        - Instantiates a LRUCache object.
        - `capacity` is defaulted to `5`. 
        - `expiry` is defaulted to `300000` milliseconds.
        - `debug` is defaulted to `False`. When set to `True`, debugging logs would be seen.

    - `get(self, key: str) -> Union[int, str]`
        - Returns -1 if key not found.
        - Returns -1 if requested key has expired (Treat it as key not found)
        - Returns value if key found and also marks it as most recently used.

    - `put(self, key: str, value: str) -> None`
        - Adds key: (value, expiry_time) to the cache
        - Marks the key as most recently used.
        - If cache is over-capacity, removes the least recently used key.

    - `isExpired(self, expiry_time: int) -> bool`
        Returns True if time now is greater than the cache expiry time set else returns False.

***`redis/client.py`***

The [redis client](#redis) handles talking to the backing redis instance

***`proxy/proxy_service.py`***

Instantiates a proxy object for communicating with the [cache](#cache) and [redis](#redis).
Cache and backing redis is instantiated based on the configurable cache values in [`.env`](#environment-variables)

- `__init__(self, is_tcp: bool = False, debug: bool = False, cache_capacity: int = 5, cache_expiry: int = 60000) -> None`

    - Creates a new instance of `Proxy`, which contains an instance of a redis and cache.
    - `is_tcp` boolean parameter when set to `True`, gives back a Proxy instance usable with TCP server.
        It's default value is `False` (meaning it would be defaulted to only be able to use with a HTTP server)
    - `debug` boolean parameter when set to `True` allows viewing the necessary logs for debugging purpose.
        It is defaulted to `False`. (meaning debugging logs would not be seen by default)
    - cache_capacity is defaulted to `5` if no `CACHE_CAPACITY` is found in `.env` file
    - cache_expiry is defaulted to `60000` milliseconds if no `CACHE_GLOBAL_EXPIRY` is found in `.env` file

- `get(self, key: str) -> str`
    - First attempts to fetch a value from the cache, if unavailable, fetches the value from backing redis. 
    - If value is not available in the backing redis either, displays `{key} not found!`.

**[HTTP server](#http-server) specific files:**

***`wsgi.py`*** 

Runs the flask app on `PROXY_HOST` and `PROXY_PORT` configured via [`.env`](#environment-variables) file.

***`routes.py`***

Provides two end-points for a HTTP client:
- A `GET` request to `/` end-point returns whether the http proxy server is up and running.
- A `GET` request to `/get/{key}` end-point returns the value of the `{key}` requested.

### [TCP server](#tcp-server) specific files:

***`server.py`***

Listens to and accepts connections from clients connecting on `PROXY_HOST` and `PROXY_PORT` configured via [`.env`](#environment-variables) file.

***`resp_parser.py`***

Encodes response to RESP format and decodes a `GET` request RESP command to extract out the requested `key`.

# Prerequisites

`make`, `docker`, `docker-compose`, `bash`

# Environment variables

Configuration options can be set in the `.env` file. Example:

```
# Redis
# -----
BACKING_REDIS_HOST_HTTP=redis-http-container
BACKING_REDIS_PORT_HTTP=6379

BACKING_REDIS_HOST_TCP=redis-tcp-container
BACKING_REDIS_PORT_TCP=6379

# HTTP Proxy server
# -----
PROXY_HOST_HTTP=0.0.0.0
PROXY_PORT_HTTP=5000
MAX_CLIENTS=5
MAX_REQUESTS=1000

# TCP Proxy server
# -----
PROXY_HOST_TCP=0.0.0.0
PROXY_PORT_TCP=4000

# Cache
# -----
CACHE_GLOBAL_EXPIRY=60000
CACHE_CAPACITY=5
```

# Algorithmic Complexity

**[Cache](#cache)**

The cache get and put operations are O(1)

**Proxy**

For [HTTP Proxy](#http-server):
- **Time complexity: O(1)**
  Fetching from cache is O(1), if not, fetching from redis, per redis documentation [here](https://redis.io/commands/get), redis get time complexity is O(1).
  Therefore, overall time complexity for our HTTP proxy `GET` is O(1)

For [TCP Proxy](#tcp-server):
- **Time Complexity: O(n), where n = length of string `key` requested.**
  The RESP Parser would take O(n) time to encode and O(n) time to decode the `key` passed to it. Fetching from either the cache or redis is an O(1) operation.
  Therefore, overall time complexity for a TCP Proxy `GET` request is O(n), where n is the length of the `key` requested.


# How to run

```bash
# clone the repo
git clone git@github.com:virat02/assignment.git

# cd into repo
cd assignment

# build and run tests
make test

# run in docker container
make run

# stop container
make stop
```

# Time spent in implementation

1. `Cache`: ~1 hour
2. `HTTP Proxy service`: ~20 hours (Includes time to setup docker for HTTP Proxy)
3. `TCP Proxy service`: ~20 hours (Includes time to setup docker for TCP Proxy)
4. `Understanding Redis and RESP` : ~3 hours.
5. `Tests` : ~3 hours
