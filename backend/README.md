# Trivia API Documentation

## 👋🏻 Introduction 
Trivia API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, Our API retrieves, deletes, adds questions and get questions based on categories and returns them as JSON responses.
## 🎬 Getting Started

### Base URL 
This API only runs locally so the base URL is ```http://127.0.0.1:5000/```
### Installing Dependencies

##### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#####  PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#####   Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend micro-services framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## ⚙️ Database Setup

With Postgres running, restore a database using the ```trivia.psql``` file provided. From the backend folder in terminal run:
###### Development Mode
```bash
dropdb trivia && createdb trivia
psql trivia < trivia.psql
```
###### Testing Mode
```bash
dropdb trivia_test && createdb trivia_tes
psql trivia_test < trivia.psql
python test_flaskr.py
```

## 🚀 Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
## ❌ Error Types
| Status Code | Description                                                                                        |
| ----------- | -------------------------------------------------------------------------------------------------- |
| 200         | OK - The request has succeeded                                                                     |
| 400         | Bad Request - The request could not be understood by the server                                    |
| 404         | Not Found - No resources found for the given request                                               |
| 405         | Not Allowed - The request is not allowed for the given URL                                         |
| 422         | Unprocessable   - The request can't be processed due to maybe lack of information or syntax errors |

> Here is an example of a failing request if the client needs to get the questions of an invalid page
```bash
$ curl -X GET 'http://127.0.0.1:5000/questions?page=10000'

{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

## 🛣 Methods and Resource Endpoints


Make sure that all endpoints starts with ```127.0.0.1:5000/{endpoint}```

| METHOD | ENDPOINT                            | ARGUMENTS   & PARAMETERS         | USAGE                                      |
| ------ | ----------------------------------- | -------------------------------- | ------------------------------------------ |
| GET    | /categories                         | None                             | Retrieve all categories                    |
| GET    | /questions                          | None                             | Retrieve all questions                     |
| POST   | /questions                          | None                             | Add new question                           |
| POST   | /questions                          | searchTerm                       | Search for questions based on their titles |
| DELETE | /questions/{question_id}            | None                             | Delete question with id question_id        |
| GET    | /categories/{category_id}/questions | None                             | Get questions based on category to answer  |
| POST   | /quizzes                            | previous_questions,quiz_category | Get new question for the client to answer  |
            
            
                    
### 🦵🏻 Responses Body

 ###### Get Categories Endpoint
  ```bash
    $ curl http://127.0.0.1:5000/categories


    {
    "categories": [
        {
        "id": 1,
        "type": "Science"
        },
        {
        "id": 2,
        "type": "Art"
        },
        {
        "id": 3,
        "type": "Geography"
        },
        {
        "id": 4,
        "type": "History"
        },
        {
        "id": 5,
        "type": "Entertainment"
        },
        {
        "id": 6,
        "type": "Sports"
        }
    ],
    "success": true,
    "total_categories": 6
}
  ```
  ###### Get Questions Endpoint 
```bash
$ curl http://127.0.0.1:5000/questions

{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "current_category": null,
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    .
    .
    .
}
```
###### Add New Question
```bash
$ curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the greatest API?","answer":"Trivia-API","difficulty":"1","category":"1"}' http://127.0.0.1:5000/questions

{
    REST OF THE QUESTIONS AGAIN , 
    "success": true,
    "total_questions": 10
    "created": 50,
}
```
