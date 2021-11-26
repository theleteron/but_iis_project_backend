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

## API Endpoints
All endpoints are prefixed by `/api` -> full endpoint address is then `<your_domain>/api/<api_endpoint>`.
### Auth
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	| Implemented        	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|--------------------	|
| `POST`       	| `/auth/login/`                     	| Allow user to login - creates login Token                                                                                                     	| AllowAny                                            	| :heavy_check_mark: 	|
| `POST`       	| `/auth/logout/`                    	| Allow user to logout - invalidates current login Token                                                                                        	| IsAuthenticated                                     	| :heavy_check_mark: 	|
| `POST`       	| `/auth/logoutall/`                 	| Allow user to logout from all devices - invalidates all login Tokens associated with the user                                                 	| IsAuthenticated                                     	| :heavy_check_mark: 	|
| `POST`       	| `/auth/register/`                  	| Allow unregistered user to create user account                                                                                                 	| AllowAny                                            	| :heavy_check_mark: 	|
### User
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	| Implemented        	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|--------------------	|
| `GET`        	| `/user/`                           	| Returns information about user (logged in user)                                                                                               	| IsAuthenticated                                     	| :heavy_check_mark:   	|
| `GET`        	| `/user/<int:id>/`                  	| Returns information about user specified by `<int:id>`                                                                                        	| IsAdministrator \|\| IsLibrarian                    	| :heavy_check_mark:  	|
| `PUT`      	| `/user/edit/`                      	| Allow user to change his details (address, phone, etc..)                                                                                      	| IsAuthenticated                                     	| :heavy_check_mark:  	|
| `PUT`      	| `/user/edit/<int:id>/`             	| Change user information for user specified by `<int:id>`, this also allows administrator to promote user to Librarian, etc...                 	| IsAdministrator                                     	| :heavy_check_mark:  	|
| `POST`       	| `/user/delete/`                    	| Deactivates user account                                                                                                                      	| IsAuthenticated                                     	| :heavy_check_mark:   	|
| `POST`       	| `/user/delete/<int:id>/`           	| Deactivates user account for user specified by `<int:id>`                                                                                     	| IsAdministrator                                     	| :heavy_check_mark:  	|
| `GET`        	| `/users/`                          	| Returns list of all users                                                                                                                     	| IsAdministrator \|\| IsLibrarian                    	| :heavy_check_mark:    |
### Library
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	| Implemented        	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|--------------------	|
| `GET`        	| `/library/`                        	| Returns list of all libraries                                                                                                                 	| AllowAny                                            	| :heavy_check_mark:    |
| `GET`        	| `/library/<int:id>/`               	| Returns library specified by `<int:id>`                                                                                                       	| AllowAny                                            	| :heavy_check_mark:    |
| `POST`       	| `/library/create/`                 	| Allow creation of new library                                                                                                                 	| IsAdministrator                                     	| :heavy_check_mark:    |
| `PUT`      	| `/library/<int:id>/associate/`     	| Adds Librarian to the Library                                                                                                                 	| IsAdministrator                                     	| :heavy_check_mark:    |
### Publication
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	| Implemented        	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|--------------------	|
| `GET`        	| `/publication/`                    	| Returns list of all publications in the system                                                                                                	| AllowAny                                            	| :heavy_check_mark:    |
| `GET`        	| `/publication/<int:id>/`           	| Returns publication specified by `<int:id>`                                                                                                   	| AllowAny                                            	| :heavy_check_mark:    |
| `POST`       	| `/publication/create/`             	| Creates new publication                                                                                                                       	| IsAdministrator \|\| IsLibrarian \|\| IsDistributor 	| :heavy_check_mark:    |
| `PUT`      	| `/publication/update/<int:id>/`      	| Update Publication - for fixing information or supplying new                                                                                  	| IsAdministrator \|\| IsLibrarian \|\| IsDistributor 	|                    	|
| `PUT`      	| `/publication/<int:id>/associate/` 	| Adds Publication specified by `<int:id>` to the Library (Library is taken from user object if user is Librarian, else it has to be specified) 	| IsAdministrator \|\| IsLibrarian                    	|                    	|
### Order
| Request type | API Endpoint                                         | Description                                                                                               | Permission                                          | Implemented |
|--------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|-----------------------------------------------------|-------------|
| `GET`        | `/order/`                                            | Returns list of all orders in the system                                                                  | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `GET`        | `/order/<int:id>/`                                   | Returns order specified by `<int:id>`                                                                     | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `GET`        | `/order/library/<int:id>/`                           | Returns list of all orders from the library specified by `<int:id>`                                       | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `GET`        | `/order/user/<int:id>/`                              | Returns list of all orders made by the user specified by `<int:id>`                                       | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `GET`        | `/order/delivered/<bool:delivered>/`                 | Returns list of all orders that have been delivered/undelivered                                           | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `GET`        | `/order/delivered/<bool:delivered>/library/<int:id>/`| Returns list of all orders made by the user specified by `<int:id>`, that have been delivered/undelivered | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |             |
| `POST`       | `/order/create/`                                     | Creates a new order                                                                                       | IsAdministrator \|\| IsLibrarian                    |             |
| `PUT`        | `/order/update/<int:id>/`                            | Update order - for marking the order specified by `<int:id>` as delivered                                                                   | IsAdministrator \|\| IsDistributor                  |             |
### Book
| Request type | API Endpoint             | Description                                                                                                  | Permission                       | Implemented |
|--------------|--------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------|-------------|
| `GET`        | `/book/`                 | Returns list of all books in the system                                                                      | IsAdministrator \|\| IsLibrarian |             |
| `GET`        | `/book/<int:id>/`        | Returns book specified by `<int:id>`                                                                         | IsAdministrator \|\| IsLibrarian |             |
| `GET`        | `/book/library/<int:id>/`| Returns list of all books from the library specified by `<int:id>`                                           | IsAdministrator \|\| IsLibrarian |             |
| `POST`       | `/book/create/`          | Adds a new book                                                                                              | IsAdministrator \|\| IsLibrarian |             |
| `PUT`        | `/book/update/<int:id>/` | Update book - for changing condition, loaned status or fixing information of the book specified by <int:id>  | IsAdministrator \|\| IsLibrarian |             |
### Book Loan
| Request type | API Endpoint                     | Description                                                                            | Permission                       | Implemented |
|--------------|----------------------------------|----------------------------------------------------------------------------------------|----------------------------------|-------------|
| `GET`        | `/book_loan/`                    | Returns list of all book loans in the system                                           | IsAdministrator \|\| IsLibrarian |             |
| `GET`        | `/book_loan/<int:id>/`           | Returns book loan specified by `<int:id>`                                              | IsAdministrator \|\| IsLibrarian |             |
| `GET`        | `/book_loan/library/<int:id>/`   | Returns list of all book loans from the library specified by `<int:id>`                | IsAdministrator \|\| IsLibrarian |             |
| `POST`       | `/book_loan/create/`             | Registered user or an employee creates a new book loan                                 | IsAuthenticated                  |             |
| `POST`       | `/book_loan/create/unregistered/`| Unregistered user creates a new book loan                                              | AllowAny                         |             |
| `PUT`        | `/book_loan/update/<int:id>/`    | Update book loan - for updating information about the book loan specified by <int:id>  | IsAdministrator \|\| IsLibrarian |             |
