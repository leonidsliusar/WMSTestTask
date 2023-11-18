runDB:
	cd app && docker compose up -d

migrate:
	cd app && python manage.py migrate

uploadData:
	cd app && python manage.py shell < main.py

test:
	cd app && pytest -v

run:
	cd app && python manage.py runserver

stopDB:
	cd app && docker compose down -v

shell:
	cd app && python manage.py shell_plus --print-sql
