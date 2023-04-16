create database: 
```
pg_ctl -D C:\Programme\PostgreSQL\15\data start
psql -U postgres
CREATE DATABASE foodplanner;
CREATE USER <user> WITH ENCRYPTED PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE foodplanner to <user>;
GRANT ALL ON SCHEMA public TO <user>;
```

.flaskenv:
```
FLASK_APP = flaskr
FLASK_ENV = DEVELOPMENT
```