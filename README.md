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
### Administration
| Request type | API Endpoint                             | Description                                                                                 | Permission      |
|--------------|------------------------------------------|---------------------------------------------------------------------------------------------|-----------------|
| `POST`       | `/admin/setrole/administrator/`          | Allows user to promote himself to an Administrator if no other Administrator is defined yet | Has key         |
| `POST`       | `/admin/setrole/<int:id>/administrator/` | Allows users with Administrator role to change selected user's role to an Administrator     | IsAdministrator |
| `POST`       | `/admin/setrole/<int:id>/librarian/`     | Allows users with Administrator role to change selected user's role to Distributor          | IsAdministrator |
| `POST`       | `/admin/setrole/<int:id>/distributor/`   | Allows users with Administrator role to change selected user's role to Librarian            | IsAdministrator |
| `POST`       | `/admin/setrole/<int:id>/registred/`     | Allows users with Administrator role to change selected user's role to Registered User      | IsAdministrator |
### Authorization
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|
| `POST`       	| `/auth/login/`                     	| Allow user to login - creates login Token                                                                                                     	| AllowAny                                            	|
| `POST`       	| `/auth/logout/`                    	| Allow user to logout - invalidates current login Token                                                                                        	| IsAuthenticated                                     	|
| `POST`       	| `/auth/logoutall/`                 	| Allow user to logout from all devices - invalidates all login Tokens associated with the user                                                 	| IsAuthenticated                                     	|
| `POST`       	| `/auth/register/`                  	| Allow unregistered user to create user account                                                                                                 	| AllowAny                                            	|
### User
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|
| `GET`        	| `/user/`                           	| Returns information about user (logged in user)                                                                                               	| IsAuthenticated                                     	|
| `GET`        	| `/user/<int:id>/`                  	| Returns information about user specified by `<int:id>`                                                                                        	| IsAdministrator \|\| IsLibrarian                    	|
| `GET`        	| `/users/`                          	| Returns list of all users                                                                                                                     	| IsAdministrator \|\| IsLibrarian                    	|
| `PUT`      	| `/user/edit/`                      	| Allow user to change his details (address, phone, etc..)                                                                                      	| IsAuthenticated                                     	|
| `PUT`      	| `/user/edit/<int:id>/`             	| Change user information for user specified by `<int:id>`, this also allows administrator to promote user to Librarian, etc...                 	| IsAdministrator                                     	|
| `DELETE`     	| `/user/delete/`                    	| Deactivates user account                                                                                                                      	| IsAuthenticated                                     	|
| `DELETE`     	| `/user/delete/<int:id>/`           	| Deactivates user account for user specified by `<int:id>`                                                                                     	| IsAdministrator                                     	|
### Library
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|
| `GET`        	| `/library/`                        	| Returns list of all libraries                                                                                                                 	| AllowAny                                            	|
| `GET`        	| `/library/<int:id>/`               	| Returns library specified by `<int:id>`                                                                                                       	| AllowAny                                            	|
| `GET`         | `/library/<int:id>/open/`             | Returns opening hours of the library specified by `<int:id>`                                                                                      | AllowAny                                              |
| `POST`       	| `/library/create/`                 	| Allows creation of new library                                                                                                                 	| IsAdministrator                                     	|
| `POST`      	| `/library/<int:id>/associate/<int:uid>`     	| Adds Librarian to the Library                                                                                                           	| IsAdministrator                                       |
| `POST`        | `/library/<int:id>/update/openinghours/` | Set opening hours for the library specified by `<int:id>`                                                                                      | IsAdministrator\|\| IsLibrarian                       |
| `PUT`         | `/library/<int:id>/update/`           | Allows user with Administration or Librarian role to update information about library specified by `<int:id>`                                     | IsAdministrator\|\| IsLibrarian                       |
### Publication
| Request type 	| API Endpoint                       	| Description                                                                                                                                   	| Permission                                          	|
|--------------	|------------------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------	|-----------------------------------------------------	|
| `GET`        	| `/publication/`                    	| Returns list of all publications in the system                                                                                                	| AllowAny                                            	|
| `GET`        	| `/publication/<int:id>/`           	| Returns publication specified by `<int:id>`                                                                                                   	| AllowAny                                            	|
| `GET`         | `/publication/<int:id>/library/<int:lid>/`    | Allows users what publications are availiable at specified library                                                                        | AllowAny                                              |
| `GET`         | `/publication/library/<int:lid>/`             | Returns publication in the library specified by `<int:id>` |                                                                               AllowAny                                              |
| `POST`        | `/publication/<int:id>/rate/<int:rate>/`  | Allows users to rate publication |                                                                                                             IsAuthenticated                                       |
| `POST`      	| `/publication/<int:id>/associate/<int:lid>/` 	| Adds Publication specified by `<int:id>` to the Library (Library is taken from user object if user is Librarian, else it has to be specified) 	| IsAdministrator \|\| IsLibrarian            	|
| `POST`       	| `/publication/create/`             	| Creates new publication                                                                                                                       	| IsAdministrator \|\| IsLibrarian \|\| IsDistributor 	|
| `PUT`      	| `/publication/<int:id>/update/`      	| Update Publication - for fixing information or supplying new                                                                                  	| IsAdministrator \|\| IsLibrarian \|\| IsDistributor 	|
### Order
| Request type | API Endpoint                                         | Description                                                                                                     | Permission                                          |
|--------------|------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| `GET`        | `/order/`                                            | Returns list of all orders in the system                                                                        | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `GET`        | `/order/<int:id>/`                                   | Returns order specified by `<int:id>`                                                                           | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `GET`        | `/order/library/<int:id>/`                           | Returns list of all orders from the library specified by `<int:id>`                                             | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `GET`        | `/order/user/<int:id>/`                              | Returns list of all orders made by the user specified by `<int:id>`                                             | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `GET`        | `/order/delivered/<int:delivered>/`                  | Returns list of all orders that have been delivered/undelivered                                                 | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `GET`        | `/order/delivered/<int:delivered>/library/<int:id>/` | Returns list of all orders made by the user specified by `<int:id>`, that have been delivered/undelivered       | IsAdministrator \|\| IsLibrarian \|\| IsDistributor |
| `POST`       | `/order/create/`                                     | Creates a new order                                                                                             | IsAdministrator \|\| IsLibrarian                    |
| `PUT`        | `/order/<int:id>/deliver/`                           | Update order - for marking the order specified by `<int:id>` as delivered, also creates new instances of book   | IsAdministrator \|\| IsDistributor                  |
### Book
| Request type | API Endpoint             | Description                                                                                                  | Permission                       |
|--------------|--------------------------|--------------------------------------------------------------------------------------------------------------|----------------------------------|
| `GET`        | `/book/`                 | Returns list of all books in the system                                                                      | AllowAny                         |
| `GET`        | `/book/<int:id>/`        | Returns book specified by `<int:id>`                                                                         | AllowAny                         |
| `GET`        | `/book/library/<int:id>/`| Returns list of all books from the library specified by `<int:id>`                                           | AllowAny                         |
| `PUT`        | `/book/update/<int:id>/` | Update book - updating information of the book specified by `<int:id>`                                       | IsAdministrator \|\| IsLibrarian |
### Book Loan
| Request type | API Endpoint                         | Description                                                                            | Permission                       |
|--------------|--------------------------------------|----------------------------------------------------------------------------------------|----------------------------------|
| `GET`        | `/book_loan/`                        | Returns list of all book loans in the system                                           | IsAdministrator \|\| IsLibrarian |
| `GET`        | `/book_loan/<int:id>/`               | Returns book loan specified by `<int:id>`                                              | IsAdministrator \|\| IsLibrarian |
| `GET`        | `/book_loan/library/<int:id>/`       | Returns list of all book loans from the library specified by `<int:id>`                | IsAdministrator \|\| IsLibrarian |
| `GET`        | `/bookloan/user/`                    | Returns list of loans that logged in user made                                         | IsAuthenticated                  |
| `GET`        | `/book_loan/user/<int:id>/`          | Returns list of all book loans made by a user specified by `<int:id>`                  | IsAdministrator \|\| IsLibrarian |
| `POST`       | `/book_loan/create/`                 | Registered user or an employee creates a new book loan                                 | IsAuthenticated                  |
| `POST`       | `/book_loan/<int:id>/loan/`          | Librarian loans book/s in book loan specified by `<int:id>`                            | IsAdministrator \|\| IsLibrarian |
| `POST`       | `/book_loan/<int:id>/receive/`       | Librarian receives book/s in book loan specified by `<int:id>`                         | IsAdministrator \|\| IsLibrarian |
| `PUT`        | `bookloan/<int:id>/fine/<int:fine>/` | Update book loan - for adding fine to a book loan specified by `<int:id>`              | IsAdministrator \|\| IsLibrarian |
### Voting
| Request type | API Endpoint               | Description                                                     | Permission                                          |
|--------------|----------------------------|-----------------------------------------------------------------|-----------------------------------------------------|
| `GET`        | `/voting/`                 | Returns list of all voting in the system                        | AllowAny                                            |
| `GET`        | `/voting/<int:id>`         | Returns voting specified by `<int:id>`                          | AllowAny                                            |
| `GET`        | `/voting/library/<int:id>` | Returns list of all voting in library specified by `<int:id>`   | AllowAny                                            |
| `POST`       | `/voting/create/`          | Manually creates a new voting                                   | IsAdministrator \|\| IsLibrarian                    |
| `PUT`        | `/voting/vote/<int:id>`    | Adds vote to the voting specified by `<int:id>`                 | IsAuthenticated                                     |
| `PUT`        | `/voting/end/<int:id>/`    | Allows user to end voting, also automatically creates a new one | IsAdministrator \|\| IsLibrarian                    |
| `DELETE`     | `/voting/delete/<int:id>/` | Allows administrator to end voting                              | IsAdministrator                                     |
