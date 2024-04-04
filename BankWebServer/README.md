# Python Validata CRUD Application Task

## Tech Used

 - SQL Server Management Studio 20.0.70.0
 - PyCharm 2023.3.2
 - Python 3.12.0
 - Postman v10.24

## Environment Setup
For environment setup, I used Anaconda to create a new environment with Python 3.12.0.
```
conda create -n ValidataEnv python=3.12
```

And added the following packages:

You can combine them in one command, or declare a requirements file and install them all at once.

I installed them one by one, and kept track of them in the list below:
```
conda install flask
conda install flask-wtf
conda install pyodbc
conda install pytest pytest-flask
```

For completeness, a `requirements.txt` file is also provided. It was generated with ` pip freeze > requirements.txt`

## Microsoft SQL Server Management Studio Login
![SQL_Server_Credentials.PNG](Files%2FSQL_Server_Credentials.PNG)

## Data Setup

### Create the Database
```
CREATE DATABASE ValidataBank;
```
### Create the Table

```
CREATE TABLE Banks (
    id INT PRIMARY KEY IDENTITY,
    name NVARCHAR(100),
    location NVARCHAR(100)
);
```

Run the `app.py` to start the Flask server. The add bank form can be accessed at `http://localhost:5000/add_bank`.

The API supports the following endpoints, which can be tested using Postman, curl, or any other API testing tool:


- `POST /create` - Create a bank with name and location (id auto-incremented)
- `GET /read` - Read all banks
- `PUT /update/<id>` - Update a bank by id (both name and location can be updated, and both need to be present in the request body)
- `DELETE /delete/<id>` - Delete a bank by id
- `GET /read/<id>` - Get a bank by id
- `GET /find/<name>` - Find a bank by name (returns the first occurrence of the bank with the specified name). If the bank name has spaces, the api endpoint works with URL encoding, so the spaces should be replaced with `%20` (if not automatically replaced by any tool that is in use, like POSTMAN).


For quick proof of concept, you can run the `API.py` which will:
 - Create 5 predefined banks using the `/create` POST endpoint
 - Read all the banks using the `/read` GET endpoint
 - Read a specified bank using the `/find/<name>` endpoint from which we will get a bank's id given its name (for example, we search for `Viva`)
 - Update `Viva` to `Viva Wallet` using the `/update/<id>` endpoint
 - Delete `Viva Wallet` bank using the `/delete/<id>` endpoint

To run the tests, you can use the following command:
(The flask server should be running)
```
pytest ValidataBankTests.py
```

For proof of concept, I have 2 tests, one for creating a bank,
and one for reading a bank by name.

Curl requests copied below, as-is from Postman which I heavily used for testing the API, in conjunction with the `API.py` script:

Create a bank with name and location (id auto-incremented)
```
curl --location 'http://localhost:5000/create' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Viva",
    "location": "Athens"
}'
```

Read all banks
```
curl --location 'http://localhost:5000/read'
```

Update a bank by id
```
curl --location --request PUT 'http://localhost:5000/update/4' \
--header 'Content-Type: application/json' \
--data '{
    "location": "Athens",
    "name": "Piraeus Bank"
}'
```

Delete a bank by id
```
curl --location 'http://localhost:5000/delete/1'
```

Find a bank by id
```
curl --location 'http://localhost:5000/read/4'
```

Find a bank by name (returns the first occurrence of the bank with the specified name)
```
curl --location 'http://localhost:5000/find/Alpha Bank'
```

