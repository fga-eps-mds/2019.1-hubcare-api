############################# Makefile ##########################
build:
	sudo docker-compose build

up:
	sudo docker-compose up

down:
	sudo docker-compose down --volume

test:
	sudo docker-compose up -d
	sudo docker-compose exec hubcare_api python manage.py test
	sudo docker-compose exec commit_metrics python manage.py test
	sudo docker-compose exec community_metrics python manage.py test
	sudo docker-compose exec issue_metrics python manage.py test
	sudo docker-compose exec pull_request_metrics python manage.py test

coverage:
	sudo docker-compose up -d
	sudo docker-compose exec hubcare_api coverage run --source='.' --omit=*/tests/*,*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	sudo docker-compose exec hubcare_api coverage report

	sudo docker-compose exec commit_metrics coverage run --source='.' --omit=*/tests/*,*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	sudo docker-compose exec commit_metrics coverage report

	sudo docker-compose exec community_metrics coverage run --source='.' --omit=*/tests/*,*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	sudo docker-compose exec community_metrics coverage report

	sudo docker-compose exec issue_metrics coverage run --source='.' --omit=*/tests/*,*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	sudo docker-compose exec issue_metrics coverage report

	sudo docker-compose exec pull_request_metrics coverage run --source='.' --omit=*/tests/*,*/tests.py,*/migrations/*,*/urls.py,*/settings.py,*/wsgi.py,manage.py manage.py test
	sudo docker-compose exec pull_request_metrics coverage report
	
style:
	sudo docker-compose up -d
	sudo docker-compose exec hubcare_api pycodestyle .

	sudo docker-compose exec commit_metrics pycodestyle .
	sudo docker-compose exec community_metrics pycodestyle .
	sudo docker-compose exec issue_metrics pycodestyle .
	sudo docker-compose exec pull_request_metrics pycodestyle .
