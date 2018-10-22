# Baires Dev

## Requirements

The main requirements are:

- Python 3.6+
- Django 2.1
- Django Rest Framework 3.8

You can see the other requirements inside the requirements files.

## Installing

First you need to activate the environment.

On windows:
```bash
virtualenv env
env\Scripts\activate
```

On linux:
```bash
virtualenv env
source env/bin/activate
```

To install this project you can use `pip` or download individually which library from PyPI.

Using `pip`, you can run the following commands for each environment you want.

```bash
pip install -r requirements.txt
```

## Setting Up

The environment is using SQLite by default, to make easier to run and test the project. 

After setup the DB, you need to run the following commands to have the data scheme right.

```bash
python manage.py makemigrations api
python manage.py migrate
python manage.py createsuperuser
```

There you will be prompted to enter the superuser credentials: username, email(optional)
and password.

## Loading initial data

To load some data into the database you must run the following commands. Being located in the root of the project

```bash
python manage.py loaddata company.json
python manage.py loaddata users.json
python manage.py loaddata reviewers.json
python manage.py loaddata reviews.json
```

## Running

To run this project, you can just run the following command:

```bash
python manage.py runserver
```

This command will run the project in `development` mode.

You can access the admin page by `http://localhost:8000/admin` and using the previous created superuser. 
Then, you can manage the users and their access tokens.

## Testing


To run all the tests, you run the following command:

```bash
python manage.py test
```

## Code coverage


To run all the tests, you run the following commands:

```bash
coverage run --source='api' manage.py test
coverage report
```

## Modeling Design

1)I have decided that the submissionDate attribute could be some date that was significant
for the review. So that was the reason for no to generate it when the review is created like a timestamp.

2)I have decided that the reviewerIp is taken from the request object.

## API documentation

To take a look at the api endpoints visit: http://localhost:8000/swagger/