docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-build-up:
	docker-compose up -d --build

docker-down:
	docker-compose down --remove-orphans

docker-logs:
	docker-compose -f docker-compose.yml logs

docker-logs-web-app:
	docker-compose -f docker-compose.yml logs web-app

docker-logs-mongo:
	docker-compose -f docker-compose.yml logs mongo -f

docker-logs-mongo-express:
	docker-compose -f docker-compose.yml logs mongo-express -f

web-app-cli:
	docker exec -ti web-app sh