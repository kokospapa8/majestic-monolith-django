# environment setup
## Runtime
- python 3.8.10
- [pyenv](https://github.com/pyenv/pyenv)
```
#after setup
pyenv install 3.8.10
```
- [virtualenv](https://github.com/pyenv/pyenv-virtualenv)
```
#after setup
pyenv virtualenv 3.8.10 majestic-monolith-django
pyenv activate majestic-monolith-django

```
### M1 MAC
if you are using M1 mac, 3.8.10 might not work use 3.8.13 
```
pyenv install 3.8.13
pyenv virtualenv 3.8.13 majestic-monolith-django
pyenv activate majestic-monolith-django
```

## Poetry
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

To install or add packages,
```
cd <project_dir>/config/app/
poetry install
poetry add <packages> --dev # use --dev only for dev
```

## install precommit hook
```
pre-commit install
```

## Environment setting
```bash
export SECRET_KEY=""
export DB_USERNAME="" #only if needed
export DB_PASSWORD="" #only if needed
export DB_HOST="" #only if needed
export REDIS_HOST="" #only if needed
export S3_BUCKET="" #
export SLACK_TOKEN="" #refer to https://django-slack.readthedocs.io/ for token config

```
## Run server
### local
access via `http://localhost:8000/api/v1/shipping/shippingitems/`
```bash
python majestic-monolith-django/manage.py runserver_plus
```
### docker-compose
access via `http://localhost/api/v1/shipping/shippingitems/`

```
- docker-compose -f compose/docker-compose-local.yml up --build
```
