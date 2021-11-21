# IIS - Backend solution for Library Information System
Database design & implemntation of API for working with the database
## Usage
### Requirements
To run this project you will need `docker`.
### Run
To setup this API & database you first have to prepare `.env.prod` file.  
Example of `.env` file (without comments - text after #)
```bash
DEBUG=1                                             # Django that we want to display detailed errors (dev env)
SECRET_KEY=foo                                      # Secret key
DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"    # Accept connection from
SQL_ENGINE="django.db.backends.postgresql"          
SQL_DATABASE="iis_library"                          # Database name
SQL_USER="iis_backend"                              # Database user
SQL_PASSWORD="iis_backend"                          # Database password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```
Modify `docker-compose.yml` with your `.env` file, change POSTGRES enviroment variables, if needed change ports that are used and setup mount points for `static_volume` & `media_volume`.
  
After this you can use
#### Build image and start it 
```bash
$ docker-compose up -d --build
``` 
#### Prepare database models (should not be necessary, check `backend/api_app/migrations`) 
```bash
$ docker-compose exec python manage.py makemigrations
```
#### Apply prepared models to database
```bash
$ docker-compsoe exec python manage.py migrate
```
### Use
Now you can check `localhost:<port>/api` to see if the API is up and running. You should see Swagger documentation.
