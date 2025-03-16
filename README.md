# Voting-System

Web app to encode the session evaluation

# Sources

```
git clone https://github.com/IDUG-EMEA-CPC/voting-system.git
```

# Local installation

.env file must be provided

python 3.9 should be installed

pip should be installed

`cd VOTE`

`pip install -r requirements`

Edit your VOTE\vote_app\vote_app\.env to point to the correct database, etc.

`python VOTE\vote_app\manage.py runserver --noreload`


Notes:
* prefer the use of a venv


# Server deployment

## Setup env file

Go to source directory

`cd VOTE`

.env file must be provided. Edit VOTE/.env and fill with valid values

the directory should look like

```
root@P14S:/home/ldb/SynologyDrive/IDUG/voting-system/VOTE# ls -la
total 40
-rw-r--r-- 1 ldb ldb  467 Mar  5 09:25 docker-compose.yml
-rw-r--r-- 1 ldb ldb  490 Mar  5 09:01 Dockerfile
-rw-rw-r-- 1 ldb ldb  415 Mar  5 15:40 .env
-rw-r--r-- 1 ldb ldb    0 Mar 17  2022 __init__.py
-rw-r--r-- 1 ldb ldb  239 Dec  8  2023 requirements.txt
drwxr-xr-x 6 ldb ldb 4096 Mar  5 20:30 vote_app
-rwxr-xr-x 1 ldb ldb   32 Nov  5  2023 vote_start
-rwxr-xr-x 1 ldb ldb   42 Dec  8  2023 vote_stop
```

## Docker compose

 
Build images for all services (webapp, nginx)

`docker-compose -f docker-compose.yml build`

View created images

`docker image ls`

You should see something like
```
vote-web-img               latest          fcc89f216b12   23 seconds ago   540MB
vote-nginx-img             latest          a9e9434231ed   10 days ago      21.3MB
```

Run the docker compose

`vote_start`

OR

`docker-compose up -d -f docker-compose.yml`

See the log

`docker logs -f voteweb`

`docker logs -f votenginx`

# Configuration (.env)

Configuration is defined in the .env file. It should contain database connection, secret key.

The file should contain something like:

```
SECRET_KEY=

DATABASE_SERVER_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
DATABASE_NAME=

ALLOWED_HOSTS=
ADMIN_INTERFACE=

ASSETS_ROOT=

DEBUG=
```

# Additional configuration (admin)

## Database initialisation

* Create a new database
* Specify the server and database name in .env
* Initialise database tables

    `python VOTE\vote_app\manage.py migrate`


    /!\ Only if database is not already populated.


* Add superuser 

    `python VOTE\vote_app\manage.py createsuperuser`

    Superuser has access to admin page. Should not be necessary

## Access to the admin page

http://HOST_IP:8000/admin/login


## Access to the vote app

http://HOST_IP:8000/login

