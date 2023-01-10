first-start: docker-build-up makemigrations migrate createsuperuser add-10-fake-forms

start: docker-up

# --- Docker section ----------------------
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-build-up:
	docker-compose up -d --build

docker-down:
	docker-compose down --remove-orphans

docker-down-remove-volumes:
	docker-compose down -v --remove-orphans

docker-logs:
	docker-compose -f docker-compose.yml logs -f

docker-logs-web-app:
	docker-compose -f docker-compose.yml logs web-app -f

docker-logs-mongo:
	docker-compose -f docker-compose.yml logs mongo -f

docker-logs-mongo-express:
	docker-compose -f docker-compose.yml logs mongo-express -f

web-app-cli:
	docker exec -ti web-app sh
# --------------------------------------------

# --- Django section ----------------------
migrate:
	 docker-compose run --rm web-app sh -c "python manage.py migrate"

makemigrations:
	 docker-compose run --rm web-app sh -c "python manage.py makemigrations"

createsuperuser:
	docker-compose run --rm web-app sh -c "python manage.py createsuperuser --no-input"

test:
	docker-compose run --rm web-app sh -c "python manage.py test"

add-10-fake-forms:
	docker-compose run --rm web-app sh -c "python manage.py add_fake_forms 10"
# --------------------------------------------

# --- Code section ----------------------
check-code:
	docker-compose run --rm web-app sh -c "isort form_checker/ service/"
	docker-compose run --rm web-app sh -c "flake8 --extend-ignore E501,F401,W605 form_checker/ service/"
# --------------------------------------------