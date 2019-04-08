############################# Makefile ##########################
up:
	sudo docker-compose up

down:
	sudo docker-compose down --volume

test:
	sudo docker-compose up -d
	sudo docker-compose exec hubcareapi python manage.py test

coverage:
	sudo docker-compose up -d
	docker-compose exec hubcareapi coverage run --source='.' --omit=*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	docker-compose exec hubcareapi coverage report
	
style:
	sudo docker-compose up -d
	docker-compose exec hubcareapi pycodestyle .