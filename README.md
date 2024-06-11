# Library_mang_system
This project was developed using PyCharm, Python, and FastAPI. For Database SQLAlchemy is used. PyCharm provides a virtual environment.

# Method 1 - How to use the project.
1. Create a virtual environment, load the library_data.py file, the pyproject.toml file, and the poetry.lock file.
2. Then, start the server by typing the following command in the terminal:
   "poetry run uvicorn library_data:app --reload" (without double quote).
3. This will start the server and provide a URL. Use that URL to access all the endpoints through Postman.

# Method 2 - How to use the project.
1. Create virtual environment, load only the library_data.py file.
2. In terminal:  pip install poetry
3. In terminal: poetry init
4. Skip all the entries.
5. The above command will create a "pyproject.toml" file. Now, open that file and replace python = "^3.12" with python = "^3.8" because Pydantic is only compatible with Python versions >= 3.8.  
6. In terminal: poetry install
7. Above command creates "poetry.lock" file.
8. In terminal: poetry add fastapi uvicorn sqlalchemy pydantic
9. Above command will install these dependencies with the updated version.
10. Now, we need to start the server
11. In terminal: poetry run uvicorn library_data:app --reload
12. This starts the server and provides an URL, use that URL to access all Endpoints of project through Postman.

# Endpoint for Adding New Book.
http://0.0.0.0:8000/books/

http://0.0.0.0:8000 this part is the url which server provides, http://0.0.0.0:8000/books/  This endpoint should be entered in Postman with the method set to POST. Then, in the body, enter the details of a book, such as: {
    "title":"A Boy at Seven",
    "author":"John",
    "publisher":"Pearson Publication",
    "published_year": 1893,
    "isbn":"1-86092-022-5"
}
The keys of the JSON should be fixed, whereas the values can change. This will upload the Book if it already does not exist.
And returns the details of book with an additional column as book_id, which is unique for every book.

# Endpoint for Registering a Student.
http://0.0.0.0:8000/students/

Enter this endpoint in Postman with the method set to POST, and in the body, enter the details in JSON format as: {
    "first_name": "Aarohan",
    "last_name": "Iyer",
    "class_name": "8th B",
    "email": "iyer@gmail.com",
    "phone": "7723658712"
}
The keys should be fixed, and the values can change. This will register the student if the student does not already exist. 
It will return the details of the student with an additional column as student_id, which will be unique for every student.

# Endpoint for updating Inventory.














