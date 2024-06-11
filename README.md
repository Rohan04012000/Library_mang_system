# Library_mang_system
This project was developed using PyCharm, Python, and FastAPI. PyCharm provides a virtual environment.

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
