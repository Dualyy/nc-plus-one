# nc-plus-one
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
host = '[YOUR HOST ADDRESS]'
port = '[PORT]'
dbname = '[DBNAME]'
user = '[USER]'
password = '[PASSWORD]'

```

Once this is all setup you simply need to run
```python main.py```
from within the project directory and the database will be seeded.

## Running the backend

To run the required backend server please run ```uvicorn main:app --reload```. After running the server, the API documentation can be found at ```http://[HOSTNAME][?Port]/docs#/```
