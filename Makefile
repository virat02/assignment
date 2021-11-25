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
	docker-compose down -v && docker-compose build && docker-compose up -d

run_tcp:
	docker-compose up -d redis && docker-compose up -d tcp_server

run_http:
	docker-compose up -d redis && docker-compose up -d web

remove_orphans:
	docker-compose down --remove-orphans