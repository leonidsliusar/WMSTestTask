start:
	docker compose up -d
	@sleep 5
	@echo Check App http://localhost:81

stop:
	docker compose down -v

test:
	docker compose -f app/tests/docker-compose.yml up -d
	@sleep 5
	cd app && pytest -v
	docker compose -f app/tests/docker-compose.yml down




migrate:
	cd app && python manage.py migrate

uploadData:
	cd app && python manage.py shell < main.py

run:
	cd app && python manage.py runserver

shell:
	cd app && python manage.py shell_plus --print-sql

