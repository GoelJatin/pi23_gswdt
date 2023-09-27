################
# build commands
################

django-build:
	docker-compose -f local.yml build django

django-run:
	docker-compose -f local.yml up --remove-orphans

backend-build:
	docker-compose -f local.yml build --pull

build: backend-build stop

run: django-run

stop:
	docker-compose -f local.yml stop

destroy:
	docker-compose -f local.yml rm -svf postgres
	docker-compose -f local.yml rm -svf django
	docker-compose -f local.yml rm -svf celeryworker
	docker-compose -f local.yml rm -svf celerybeat
	docker volume prune -f
	rm -f localstack/data/recorded_api_calls.json localstack/data/startup_info.json

destroy-save-data:
	docker-compose -f local.yml rm -svf django
	docker-compose -f local.yml rm -svf celeryworker
	docker-compose -f local.yml rm -svf celerybeat
	docker volume prune -f

rebuild-save-data: destroy-save-data build

destroy-hard: stop destroy
	docker-compose -f local.yml down -v --rmi all

rebuild: destroy build
r: rebuild

rebuild-with-init-data: destroy build m core-data
rbwid: rebuild-with-init-data

armageddon:
	docker-compose -f local.yml stop
	docker-compose -f local.yml down -v --rmi all
	docker volume prune -f
	rm -f localstack/data/recorded_api_calls.json localstack/data/startup_info.json

clean: destroy stop
	docker system prune -f

cbr: clean build run

destroy-postgres:
	docker-compose -f local.yml rm -svf postgres


####################
# migration commands
####################
python-makemigrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations
mm: python-makemigrations

python-makemigrations-empty:
	docker-compose -f local.yml run --rm django python manage.py makemigrations ${app_label} --empty --name data_migration_${migration_name}
mme: python-makemigrations-empty

python-makemigrations-merge:
	docker-compose -f local.yml run --rm django python manage.py makemigrations --merge
merge: python-makemigrations-merge

python-migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate_schemas
m: python-migrate


###########################
# bash, shell, cli commands
###########################
python-bash:
	docker-compose -f local.yml run --rm django bash
b: python-bash
bash: python-bash

python-bash-root:
	docker-compose -f local.yml run --rm --user root django bash
b-root: python-bash-root

python-shell-plus:
	docker-compose -f local.yml run --rm django python manage.py shell_plus
sp: python-shell-plus

python-tenant-shell-plus:
	docker-compose -f local.yml run --rm django python manage.py tenant_command shell_plus
tsp: python-tenant-shell-plus

python-db-shell:
	docker-compose -f local.yml run --rm django python manage.py dbshell
db: python-db-shell

redis-cli:
	docker-compose -f local.yml run --rm redis redis-cli -h redis -p 6379

redis-cli-cacheops:
	docker-compose -f local.yml run --rm redis redis-cli -n 1 -h redis -p 6379
cacheops: redis-cli-cacheops

#################################
# scripts and management commands
#################################
python-pip-install:
	docker-compose -f local.yml run --rm --user root django pip install -r requirements/base.txt -r requirements/local.txt
	docker-compose -f local.yml run --rm --user root celeryworker pip install -r requirements/base.txt -r requirements/local.txt
	docker-compose -f local.yml run --rm --user root celerybeat pip install -r requirements/base.txt -r requirements/local.txt
pip: python-pip-install

postman-push:
	docker-compose -f local.yml run --rm django /bin/bash -c "cd scripts && chmod 755 postman-push.sh && ./postman-push.sh"
pp: postman-push

build-openapi-schema:
	docker-compose -f local.yml run --rm django python manage.py tenant_command spectacular --file openapi-schema.yml --urlconf config.urls
bos: build-openapi-schema

rules-engine-ecr:
	echo "Downloading Rules Engine from ECR.  Make sure your AWS profile is called 'los'."
	aws ecr get-login-password --profile los | docker login --username AWS --password-stdin 813755454003.dkr.ecr.us-east-2.amazonaws.com
re-ecr: rules-engine-ecr

python-makemessages:
	docker-compose -f local.yml run --rm django python manage.py makemessages -a
messages: python-makemessages

python-compilemessages:
	docker-compose -f local.yml run --rm django python manage.py compilemessages
cm: python-compilemessages


###############
# test commands
###############
DIR ?= tests/
python-test:
	docker-compose -f local.yml run --rm django python -m pytest ${DIR}
t: python-test
test: python-test

####################
# reporting commands
####################
pylint:
	docker-compose -f local.yml run --rm django bash ./run_pylint.sh

coverage:
	docker-compose -f local.yml run --rm django bash -c "pytest --cov tests/"
# docker-compose -f local.yml run --rm django bash -c "coverage run -m pytest && coverage report"

# config in pyproject.toml
vulture:
	docker-compose -f local.yml run --rm django vulture

qc: pylint coverage vulture
