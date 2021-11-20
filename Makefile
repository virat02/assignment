## Build the container. 
build: 
	docker-compose build

## Run docker container.
run: 
	docker-compose up -d

## Stop docker container
stop: 
	docker-compose down -v