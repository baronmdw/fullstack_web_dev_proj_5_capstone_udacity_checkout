# Foodplanner Backend
Welcome to the documentation of the backend for the foodplanner app.

## Technologies
The backend uses a Postgres Database and runs on Python Flask. In order to be able to replicate it on your local machine, you will need to have PostgreSQL and Python 3.11.1 installed. The dockerfile is used for production only, please use shell commands to set up your local server otherwise you will need to make some settings in your Postgres to allow a Docker Container to access the database.

## Set-Up the Database
To set up the database, I assume you have PostgreSQL installed, if not, plese do so from [here](https://www.postgresql.org/).
After installation and starting up postgres, please login to your psql via terminal and create the databases for dev and testing with following commands:

create databases: 
```
psql -U postgres
CREATE DATABASE <db_name>;
CREATE USER <user> WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE <db_name> to <user>;
GRANT ALL ON SCHEMA public TO <user>;
CREATE DATABASE <db_test_name>;
CREATE USER <user> WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE <db_test_name> to <user>;
GRANT ALL ON SCHEMA public TO <user>;
```
The variables you enter to <db_name>, <db_test_name>, <user> and <password> need to be put to the .env file so make sure you either can replicate them from memory or put them to the .env file directly. The .env file needs to be included in the src folder.

## Set-Up the backend
Having set up the backend you will need to create a virtual environment, I recommend doing this in the backend folder. This project runs on Python 3.11.1, so please make sure you use this to replicate the project. Having initialized and activated the virtual environment you will need to install the dependencies with 

```console
pip install -r requirements.txt
```

Afterwards cd in the src folder. In this folder (the src folder) you will need to have two files with environment variables: .env and .flaskenv.
This is the necessary content of the .env file, four of them should be familiar from creating the database tables and user, the auth0 secrets will be posted to the udacity submission details:

.env-File:
```
DB_HOST=<e.g.127.0.0.1>
DB_USER=<user>
DB_PASSWORD=<password>
DB_PORT=<your_postgresql_port>
DB_NAME=<db_name>
DB_TEST_NAME=<db_test_name>
AUTH0_DOMAIN=
ALGORITHMS=
API_AUDIENCE=
CLIENT_ID=
CLIENT_SECRET=
WRITE_JWT=<jwt of the full-access user>
READ_JWT=<jwt of the read-access user>
``

.flaskenv-File:
```
FLASK_APP=flaskr
FLASK_DEBUG=1
```

Having set all this you will be able to start the backend by prompting flask run while being cd-ed in the backend/src folder.

## Running the tests