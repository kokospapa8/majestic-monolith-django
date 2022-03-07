# environment setup 
## prereq
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
### Poetry
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

To install or add packages,
```
cd <project_dir>/config/app/
poetry install
poetry add <packages> --dev # use --dev only for dev
```
