# majestic-monolith-django

[!image]()

## Introduction
This is a starter repo for django project aiming to achieve majestic monolith architecture.
I have complied useful techniques and libraries to help build backend API server.

Inspired by [Majestic monolith](https://m.signalvnoise.com/the-majestic-monolith/) and 
[Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x), this starter code will help you 
build scalable application for a small team of developers.


## Why majestic modular monolith?
MicroService is everywhere and no doubt that they are the next big thing,
for a company with many developers and in need for concurrent feature releases.

However, if you are the only developer in the team or dealing with a relatively small to medium scale architecture, 
MSA needs a lot of coordination and preparation compare to monolith.

You can reduce cognitive load by following DDD practice. 
With code isolation, data isolation and some cloud architecture aid, majestic monolith django can prepare for the scale and bigger team coordination.


## Sample app
This repo provides sample user and auth app. 
also another app another comment app to illustrate modular monolith architecture.

[!image]()


## Features
- cache : REDIS
- authentication : JWT
- 

## Infra
- CDK
-- eventbridege 
- SAM
-- lambda

## Deployment
- CI 
-- precommit 
-- dockerfile
- ECS support

## Libraries
uses poetry for dependency management
- Django 3.2 
- djangorestframework
- django-storages
- django-request-logging
- djangorestframework-simplejwt
- drf-yasg
- django-guid
- easy-thumbnails
- django-daterangefilter
- boto3
and many more...
refer to [pyproject.toml](/config/app/pyproject.toml)

## pytest

# setup 
[setup](setup.md) 

# convention
[convention](conventions.md)



# Howto
## run docker-compose
## run pytest
```python -m pytest --ds=settings.test```

## TODO
[Projects](https://github.com/users/kokospapa8/projects/1/views/1)

## Reference
- [Majestic monolith](https://m.signalvnoise.com/the-majestic-monolith/)
- [Majestic Modular Monoliths](https://lukashajdu.com/post/majestic-modular-monolith/)
- [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [cookie-cutter-django](https://github.com/cookiecutter/cookiecutter-django)

# Release
## version
- 0.0.1 initial scaffolding
## release plan
- 0.1.0 initial application update with api
- 0.1.1 service layer 
- 0.2.0 cookie cutter
- 0.3.0 async support
- 