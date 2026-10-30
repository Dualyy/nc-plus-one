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

Once this is all setup you simply need to run
```python main.py```
from within the project directory and the database will be seeded.

## Running the backend

To run the required backend server please run ```ENV=[ENVIRONMENT_YOU_WANT_TO_RUN] uvicorn main:app --reload```. After running the server, the API documentation can be found at ```http://[HOSTNAME][?Port]/docs#/```
