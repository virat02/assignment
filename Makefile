## Build the container. 
build: 
	docker-compose build

## Run docker container.
run: 
	docker-compose up -d

## Stop docker container
stop: 
	docker-compose down -v

rebuild:
	make stop && make build && make run

remove_orphans:
	docker-compose down --remove-orphans

build_redis:
	docker-compose build redis

run_redis:
	docker-compose up -d redis

build_http_server:
	docker-compose build web

run_http_server:
	docker-compose up -d web

build_tcp_server:
	docker-compose build tcp_server

run_tcp_server:
	docker-compose up -d tcp_server

run_tcp:
	make run_redis && make run_tcp_server

run_http:
	make run_redis && make run_http_server

test_http:
	docker-compose exec web pytest "tests"

test_tcp:
	docker-compose exec tcp_server pytest "tests"

stop_redis:
	docker-compose down -v redis

stop_http: 
	make stop_redis && docker-compose down -v web

stop_tcp: 
	make stop_redis && docker-compose down -v tcp_server

test:
	make build && make run && make test_http && make test_tcp