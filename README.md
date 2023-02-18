https://github.com/gufin/Auth_sprint_1
# 🛠 Educational project
Authorization service by roles based on JWT tokens

The following tools were used in the backend part of the project:
-Flask 2.2
-SQLAlchemy 2.0
-Alembic 1.9
-Gevent 1.9

The infrastructure part used:
- PostgreSQL
- Docker
- Redis
- Gunicorn

# 🚀 Project installation
Install Docker and docker-compose:
```sh
sudo apt-get update
sudo apt install docker.io
sudo apt-get install docker-compose-plugin
```
Clone repository:
```sh
git clone git@github.com:gufin/Auth_sprint_1.git
```
When deploying to a server, you need to create a file with the values of the .env variables in the docker_compose folder.
```sh
sudo docker-compose  up -d --build
```
Then you need to apply the migrations
```sh
sudo docker-compose exec auth_service flask db upgrade
```
To create a superuser, you need to move to the [src](flask-solution%2Fsrc) directory and run the command
```sh
flask superuser create <login> <password>
```

[Api documentation](http://127.0.0.1:5500/apidocs/)

 # :dependabot: Project Tests
To run functional tests, you need to move to the [functional](tests%2Ffunctional)tests directory and run the command. You need to create a file with the values of the .env variables before that
```sh
sudo docker-compose  up -d --build
```
Test results will be available in the test container console output

# :smirk_cat: Authors
Drobyshev Ivan

[Agatanov Madihan](https://github.com/agatma/)
