# GSTHEALTH Official Repository

Welcome to Django-Tabler Boilerplate by Letstream®

## Features

- Email Based Authentication with Email Confirmation and ready-to-use module with UI.
- Two way access to all modules, i.e. Subscriber or Admin
- Inbuilt Methods for common tasks
- Celery Support
- AWS S3 Support
- Support for Read-Replica Database
- .env based configuration for DEBUG Mode, Celery, AWS, Database, Upload/Static Root and more.
- Seperate Config Files for Production and Testing. 
- Dynamic Email Credentials (Not embedded in settings.py)
- Celery Support for Emails
- Options Support for Dynamic Website Settings
- Admin Dashboard with Sidebar and Pre-Built User Module to add, edit, delete, suspend, login as, change password, change profile, listing with filter and much more.
- TableData class to programitcally create tables using Django without writing single line of HTML!
- Pre-Built UI using Tabler (https://tabler.github.io)

## Dependecies
- PostgreSQL 10+
- Python 3.6.x
- Celery (Optional)
- python3-dev (Linux)
- build-essential (Linux)
- Visual Studio SDK Tools (Windows)

## Basic Steps
- Clone the project and replace `PROJECT_NAME_HERE` with your project name everywhere.
- Create a `.env` file in `PROJECT_NAME_HERE/settings/`. You can refer to sample.env at same place for supported settings.
- Install Dependecies and then install requirements using `pip install requirements/local.txt`
- Create Migrations using `python manage.py makemigrations` and migrate them using `python manage.py migrate`.
- Initialize Options Table using `python manage.py initializedb`
- Create SuperUser using `python manage.py createsuperuser`
- Run Server using `python manage.py runserver`
- Head to http://localhost:8000/dashboard and login with superuser credentials.
- Now goto http://localhost:8000/dashboard/profile and and in the Roles Section, select Admin and Click on Save.
- All Set. The application is ready to start.
