# Cooking recipe web page

Development of a cooking recipe web page.

## Project

Install [Django](https://docs.djangoproject.com/en/4.2/intro/install/), version 4.2, Python 3.11.5. Create a virtual environment with [venv](https://docs.python.org/3/tutorial/venv.html).

## Database SQLite

[Database SQLite](https://docs.djangoproject.com/en/4.2/intro/tutorial02/). Create the database with command line `python manage.py migrate`. Create table in database with command lines `python manage.py makemigrations recipe` then `python manage.py migrate`.

## Run application

Run application with command line `python manage.py runserver`.
Open browser and search for `http://localhost:8000/recipe`.

## Run tests

Run tests with command line `python manage.py test recipe`.