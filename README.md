# nc-plus-one
This API allows users to register, browse events, RSVP, and manage their attendance. Organisers are be able to create and manage events, and view statistics about their audience.


### Requirements
Python

PostgreSQL

uvicorn

## Installation
Clone the repository onto your local machine using:

`git clone https://github.com/Dualyy/nc-plus-one.git`

## Setup
First you need to install all the required packages. This can be done with the following command:

`pip install -r requirements.txt`

### Creating the Database
After installing the required packages, you are going to need to create the Database. This can be done with the provided setup.sql file by running:

`psql -f db/setup.sql`

### Configuring the environment
This project requires you to setup different credentials for different environments. For this you will need seperate files named like this, according to your need and use case:

`.env.test`
`.env.development`
`.env.production`

An example file is provided within the repo but generally it should look something like this:

```python
HOST = "[YOUR HOST ADDRESS]"
PORT = "[PORT]"
DBNAME = "[DBNAME]"
USER = "[USER]"
PASSWORD = "[PASSWORD]"


JWT_SECRET = "[YOUR SECRET]"
```

## Seeding

To seed the database simply run `python src/seed.py`. This is not necessary when running tests with pytest, as pytest calls the function itself

## Running the backend

To run the required backend server please run ```ENV=[ENVIRONMENT_YOU_WANT_TO_RUN] uvicorn main:app --reload```. After running the server, the API documentation can be found at ```http://[HOSTNAME][?Port]/docs#/```


## General Info

### Endpoints table
| Method 	|Path    	|Auth   |
|--------|---------|--------|
|POST|	/auth/register, /auth/login	|public
|GET|	/events, /events/{id}	|public
|POST|	/events	|user
|PATCH|	/events/{id}	|organiser
|POST / DELETE	|/events/{id}/rsvp, /events/{id}/rsvp/me	|user
|GET|	/events/{id}/attendees	|organiser
|GET|	/user/me/events	|user
|GET|	/organisers/{id}/stats	|public -> CURRENTLY WORK IN PROGRESS


### Tree structure

```
└── nc_plus_one/
    ├── db/
    │   ├── data/
    │   │   ├── events.json
    │   │   ├── rsvps.json
    │   │   ├── users.json
    │   │   └── venues.json
    │   ├── data_test/
    │   │   ├── events.json
    │   │   ├── rsvps.json
    │   │   ├── users.json
    │   │   └── venues.json
    │   └── setup.sql
    ├── src/
    │   ├── auth/
    │   │   ├── passwords.py
    │   │   └── security.py
    │   ├── models/
    │   │   ├── auth.py
    │   │   ├── events.py
    │   │   └── user.py
    │   ├── routes/
    │   │   ├── auth_routes.py
    │   │   ├── event_route.py
    │   │   ├── organisers_route.py
    │   │   └── user_route.py
    │   ├── table_utils/
    │   │   ├── events_table_util.py
    │   │   ├── rsvps_table_util.py
    │   │   ├── user_table_util.py
    │   │   └── venues_table_util.py
    │   ├── connection.py
    │   ├── exceptions.py
    │   ├── seed.py
    │   └── util.py
    ├── tests/
    │   ├── routes/
    │   │   ├── conftest_routes.py
    │   │   ├── test_auth_routes.py
    │   │   ├── test_event_route.py
    │   │   ├── test_organisers_route.py
    │   │   └── test_user_routes.py
    │   ├── test_connection.py
    │   ├── test_seed.py
    │   └── test_util.py
    ├── .env.*
    ├── main.py
    ├── pytest.toml
    ├── README.md
    └── requirements.txt```

courtesy of [https://tree.nathanfriend.com/](https://tree.nathanfriend.com/?s=(%27opUJs!(%27fancyI~fullPath!falN~trailingSlashI~rootDotI)~Q(%27Q%27nc_plus_Je6db-dataT8393data_7T8393Ntup.sql6src-HTpasswordXNcurity2modelzHF8XC24zHOX8OFBCO25z8YFZvpYFC_5FkY2GexcepUJs2Ned2L7s-4zcJfK4XKHOXK8OFKBKCOs2KGKNed2KL.Vv.*6mainW6py7.toml6README.md6requiremVts.txt-%27)~veZiJ!%271%27)-600%20%202W-3s.jsJ-4route5table_uUl6%5Cn07test8evVt90Zvp30C30kBorganiNZOFCuNrF20GcJnecUJ2HauthI!trueJonK7_LuUlW6NseO_4Qsource!T-0UtiVenW.pyXsFYs_5ZrskvVuezsT%01zkZYXWVUTQONLKJIHGFCB987654320-)