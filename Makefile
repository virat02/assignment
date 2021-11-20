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