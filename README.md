# Library_mang_system
This project was developed using PyCharm, Python, FastAPI, Pydantic, and Poetry. For Database SQLAlchemy is used. PyCharm provides a virtual environment.

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

http://0.0.0.0:8000 this part is the url which server provides, http://0.0.0.0:8000/books/  This endpoint should be entered in Postman with the method set to POST. Navigate to the body tab, select raw and choose json from the dropdown menu.
Enter the following JSON object into the body section: {
    "title":"A Boy at Seven",
    "author":"John",
    "publisher":"Pearson Publication",
    "published_year": 1893,
    "isbn":"1-86092-022-5"
}
The keys of the JSON should be fixed, whereas the values can change. This will upload the Book if it already does not exist.
And returns the details of book with an additional column as book_id, which is unique for every book ranging from 1 to N.

# Endpoint for Registering a Student.
http://0.0.0.0:8000/students/

Enter this endpoint in Postman with the method set to POST, Navigate to the body tab, select raw and choose json from the dropdown menu.
Enter the following JSON object into the body section: {
    "first_name": "Aarohan",
    "last_name": "Iyer",
    "class_name": "8th B",
    "email": "iyer@gmail.com",
    "phone": "7723658712"
}
The keys should be fixed, and the values can change. This will register the student if the student does not already exist. 
It will return the details of the student with an additional column as student_id, which will be unique for every student ranging from 1 to N.

# Endpoint for updating Inventory.
http://0.0.0.0:8000/inventory/

Enter the above endpoint and set the HTTP method to POST. Navigate to the body tab, select raw and choose json from the dropdown menu.
Enter the following JSON object into the body section: {
    "book_id": 5,
    "total_copies": 200,
    "available_copies": 200
}
The book_id is the ID generated when a new book was added to the system. You need to specify the book ID for the book you want to update. While the keys in this JSON object are fixed, the values can be changed as needed.

# Endpoint for issuing and returning a book.
http://0.0.0.0:8000/transactions/

Enter the above endpoint and set the HTTP method to POST. Navigate to the body tab, select raw and choose json from the dropdown menu.
<center>Note 1:</center> 
<u>Enter the following JSON object into the body section for issuing a book: </u>
{
    "student_id":5,
    "book_id":12,
    "issue_date":"2021-06-09"
}
The student_id is the ID generated for a student when they registered with the system. Entering the student_id indicates which student is issuing the book, and entering the book_id indicates which book is being issued. Since the student is issuing the book, only the issue_date needs to be entered.
<center>Note 2:</center>
<u>Enter the following JSON object into the body section for issuing a book:</u>
{
    "student_id":5,
    "book_id":12,
    "return_date":"2021-06-28"
}
 Since the student is returning the book, only the return_date needs to be entered.

 <u>Important:</u>Both requests will automatically update the inventory, either increasing or decreasing the available copies of the book that is being issued or returned.

 <u>When both issue_date and return_date are entered, it will raise an HTTPException.</u>

 # Endpoint for finding top five popular books.
 http://0.0.0.0:8000/five_popular_books/

Set the method to GET and send the request to the above URL. It will return the top 5 popular books with their book_id, book_title, and no_of_times_issued.

#Additional endpoint which should be sent with method set to GET.
1. For listing first 10 updated books:  http://0.0.0.0:8000/books_records/
2. For listing first 10 registered students: http://0.0.0.0:8000/students_records/
3. For listing the first 10 records of Inventory table: http://0.0.0.0:8000/inventory_records/
4. For listing the first 10 records of Transaction table, which holds the details about issue and return of a book: http://0.0.0.0:8000/transactions_records/

#Information about the tables used:
1. <u>Details of table_name "books":</u>
   book_id = Column(Integer, primary_key = True, index = True)  --> This is set to primary Key and it will auto-increment, and it should be noted whenever a book is registed/updated into library system.
   title = Column(String, index = True)
   author = Column(String, index = True)
   publisher = Column(String, index = True)
   published_year = Column(Integer, index = True)
   isbn = Column(String, index = True)

2. <u>Details of table_name "students":</u>
   student_id = Column(Integer, primary_key = True, index = True)
   first_name = Column(String, index = True)
   last_name = Column(String, index = True)
   class_name = Column(String, index = True)
   email = Column(String, index = True)
   phone = Column(String, index = True)

3. <u>Details of table_name "inventory":</u>
   inventory_id = Column(Integer, primary_key = True, index = True)
   book_id = Column(Integer, ForeignKey('books.book_id')) --> In inventory table, a column which is linked to books.book_id column. And it is one-to-one relation.
   total_copies = Column(Integer, index = True)
   available_copies = Column(Integer, index = True)
   book = relationship("Book") -->  Making a relationship in Inventory model with Book model.

4. <u>Details of table_name "transactions":</u>
   transaction_id = Column(Integer, primary_key = True, index = True)
   student_id = Column(Integer, ForeignKey('students.student_id'))
   book_id = Column(Integer, ForeignKey('books.book_id'))
   issue_date = Column(String)
   return_date = Column(String, nullable = True)
   student = relationship("Student") -->This table has relationship with Student.
   book = relationship("Book") -->Also has relationship with Book.








 















