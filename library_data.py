from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import sessionmaker, relationship, Session, declarative_base


#In this task, we are connecting to a SQLite database.
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy setup
#Creating a SQLAlchemy engine. connect_args = {"check_same_thread":False} is needed only for SQLite. Not needed for other databases.
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

#We are using Base class to create the SQLAlchemy models.
#Creating Classes and these Classes are SQLAlchemy models.
class Book(Base):
    # The __tablename__ = "books" tells the name of the table to use in the database for Book model.
    __tablename__ = "books"
    # Now creating attributes which represents Columns in table books.
    # book_id is set to primary_key, therefore by default it supports auto-increment.
    book_id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True)
    author = Column(String, index = True)
    publisher = Column(String, index = True)
    published_year = Column(Integer, index = True)
    isbn = Column(String, index = True)


#Student model for registering Students.
class Student(Base):
    __tablename__ = "students"
    # For model Student, creating table students, which will register the details of students.
    student_id = Column(Integer, primary_key = True, index = True)
    first_name = Column(String, index = True)
    last_name = Column(String, index = True)
    class_name = Column(String, index = True)
    email = Column(String, index = True)
    phone = Column(String, index = True)


#Inventory model for keeping inventory of books.
class Inventory(Base):
    # For model Inventory, creating table inventory, which will keep the records of book and it's quantity.
    __tablename__ = "inventory"
    inventory_id = Column(Integer, primary_key = True, index = True)
    #In inventory table, a column which is linked to books.book_id column. And it is one-to-one relation.
    book_id = Column(Integer, ForeignKey('books.book_id'))
    total_copies = Column(Integer, index = True)
    available_copies = Column(Integer, index = True)
    #Making a relationship in Inventory model with Book model.
    book = relationship("Book")

#An additional table which defines the relationship between Student and Book table.
class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key = True, index = True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    book_id = Column(Integer, ForeignKey('books.book_id'))
    issue_date = Column(String)
    return_date = Column(String, nullable = True)
    student = relationship("Student") #This table has relationship with Student.
    book = relationship("Book") #Also has relationship with Book.


# Create the tables
Base.metadata.create_all(bind = engine)


# Define Pydantic models
#BookCreate model is used to validate the type of data entered through json request.
class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    published_year: int
    isbn: str
#StudentCreate model is used to validate thee type of data entered through json request.
class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    class_name: str
    email: str
    phone: str

#InventoryCreate model is used to validate the type of data entered through json request.
class InventoryCreate(BaseModel):
    book_id: int
    total_copies: int
    available_copies: int

#This model is used to validate the type of request in /transaction endpoint.
class TransactionCreate(BaseModel):
    student_id: int
    book_id: int
    issue_date: Optional[str] = None  #Is None because when returning book, no need to specify issue_date.
    return_date: Optional[str] = None #Is None because when issuing book, no need to specify return_date.

#This is used to return the response and validate the types from '/books/'  endpoint.
class BookResponse(BaseModel):
    book_id: int
    title: str
    author: str
    publisher: str
    published_year: int
    isbn: str

#This is used to return the response and validate the types from '/students/'  endpoint.
class StudentResponse(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    class_name: str
    email: str
    phone: str

#This is used to return the response from '/inventory/'  endpoint.
class InventoryResponse(BaseModel):
    inventory_id: int
    book_id: int
    total_copies: int
    available_copies: int

#Model for validating the response from /transaction endpoint.
class TransactionResponse(BaseModel):
    transaction_id: int
    student_id: int
    book_id: int
    issue_date: Optional[str]
    return_date: Optional[str]

#Model for validating the response from endpoint /five_popular_books.
class PopularBookResponse(BaseModel):
    book_id: int
    title: str
    times_issued: int


# Create the FastAPI app
app = FastAPI()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoint for adding books.
#response_model = BookResponse, will return the details mentioned under BookResponse, which is defined under Pydantic.
#inside create_book, book represents the data which was passed through postman in json and which is also validated based on BookCreate.
@app.post("/books/", response_model = BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Check if the book already exists.
    existing_book = db.query(Book).filter(Book.title == book.title,
                                          Book.author == book.author,
                                          Book.publisher == book.publisher,
                                          Book.published_year == book.published_year,
                                          Book.isbn == book.isbn
                                          ).first()
    #If exist, then raise an Exception.
    if existing_book:
        raise HTTPException(status_code = 409, detail = "Book already exists")
    try:
        #Otherwise, update the entered details into books table.
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        return {"message": "Error occurred while creating the book"}

# Endpoint for Registering students.
#response_model = StudentResponse, will return the details mentioned under StudentResponse, which is defined under Pydantic.
#inside create_student, student represents the data which was passed through postman in json and which is also validated based on StudentCreate.
@app.post("/students/", response_model = StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # Check if the student already exists.
    existing_student = db.query(Student).filter(Student.first_name == student.first_name,
                                          Student.last_name == student.last_name,
                                          Student.class_name == student.class_name,
                                          Student.email == student.email,
                                          Student.phone == student.phone
                                          ).first()
    #If student exist, then raise an Exception.
    if existing_student:
        raise HTTPException(status_code = 409, detail = "Student already exists.")
    try:
        #Otherwise, update the student table after reading the json data.
        db_book = Student(**student.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    except IntegrityError:
        return {"message": "Error occurred while creating the book"}

#Inventory endpoint.
#Updating the inventory for new arrivals, whether they are new books or additional copies of existing books.
@app.post("/inventory/", response_model = InventoryResponse)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    # Check if entered inventory already exists.
    existing_inventory = db.query(Inventory).filter(Inventory.book_id == inventory.book_id,
                                                Inventory.total_copies == inventory.total_copies,
                                                Inventory.available_copies == inventory.available_copies
                                                ).first()
    # If inventory exist, then raise an Exception.
    if existing_inventory:
        raise HTTPException(status_code = 409, detail = "Inventory already exists.")


    # Check if the inventory record for the given book_id already exists.
    existing_inventory_1 = db.query(Inventory).filter(Inventory.book_id == inventory.book_id).first()

    # If the inventory exists, update the total_copies and available_copies.
    if existing_inventory_1:
        existing_inventory_1.total_copies = inventory.total_copies
        existing_inventory_1.available_copies = inventory.available_copies
        db.commit()
        db.refresh(existing_inventory_1)
        return existing_inventory_1

    # Validating that the requested book_id exists in books table or not.
    book = db.query(Book).filter(Book.book_id == inventory.book_id).first()
    # If book is not found, raise an error.
    if book is None:
        raise HTTPException(status_code = 400, detail = "Book not found")

    # Otherwise, insert a new record into the inventory table.
    db_inventory = Inventory(**inventory.dict())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

#Endpoint to handle the request of issue and return a book.
@app.post("/transactions/", response_model = TransactionResponse)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Validating if the student exists.
    student = db.query(Student).filter(Student.student_id == transaction.student_id).first()
    #If no record is found, raise an exception.
    if student is None:
        raise HTTPException(status_code = 400, detail = "Student not found")

    # Validating if the book exists.
    book = db.query(Book).filter(Book.book_id == transaction.book_id).first()
    #If no record is found.
    if book is None:
        raise HTTPException(status_code = 400, detail = "Book not found.")
    print("we are in-----")
    #Now, this is for when a student is issuing a book and have not entered anything for return_date.
    if transaction.issue_date and not transaction.return_date:
        # Before issuing, Checking if the student has already issued 3 books.
        issued_books_count = db.query(Transaction).filter(
                                    Transaction.student_id == transaction.student_id,
                                            Transaction.return_date == None
                                            ).count()
        #If count for student_id in transction table is more than 3, raise an exception.
        if issued_books_count >= 3:
            raise HTTPException(status_code = 400, detail = "Student has already issued 3 books.")

        # Check if there is an inventory record for the requested book.
        inventory = db.query(Inventory).filter(Inventory.book_id == transaction.book_id).first()
        #If inventory is not updated for book, which is about to issued, raise an exception.
        if inventory is None:
            raise HTTPException(status_code = 400, detail = "Inventory record not found.")
        #Also check if there is available copies for requested book.
        if inventory.available_copies < 1:
            raise HTTPException(status_code = 400, detail = "No copies available to issue.")

        # Decreasing the count of available_copies by 1 on issuing a book.
        inventory.available_copies -= 1

        # Creating the transaction record for issuing the book in transactions table.
        db_transaction = Transaction(
                                    student_id = transaction.student_id,
                                    book_id = transaction.book_id,
                                    issue_date = transaction.issue_date,
                                    return_date = None  # Return date is None when issuing
                                    )
        db.add(db_transaction)
    elif transaction.return_date and not transaction.issue_date: #When returning a book.
        # Finding the transaction record of student_id and book_id where return_date is None.
        db_transaction = db.query(Transaction).filter(
                                            Transaction.student_id == transaction.student_id,
                                                    Transaction.book_id == transaction.book_id,
                                                    Transaction.return_date == None
                                                    ).first()
        #If there is no record found in transaction.
        if db_transaction is None:
            raise HTTPException(status_code = 400, detail = "No active transaction found for this student and book.")

        # Updating the return date in the transactions table.
        db_transaction.return_date = transaction.return_date

        # Increase the count of available_copies by 1 on returning a book.
        inventory = db.query(Inventory).filter(Inventory.book_id == transaction.book_id).first()
        if inventory is None:
            raise HTTPException(status_code = 400, detail = "Inventory record not found.")
        #Increasing the count of available_copies, when a book is returned.
        inventory.available_copies += 1
    else: #When user passes both issue date and return date.
        print("when both are entered!.")
        raise HTTPException(status_code = 400, detail = "Invalid request. Provide either issue date or return date, not both.")

    db.commit()
    db.refresh(db_transaction)
    db.refresh(inventory)  # Refresh the inventory record to reflect changes.
    return db_transaction

#Endpoint to find the 5 most popular books along with their id, title and times of issued.
@app.get("/five_popular_books/", response_model = List[PopularBookResponse])
def get_popular_books(db: Session = Depends(get_db)):
    #Join the Transaction and Book tables based on book_id, group by the book ID,
    # count the number of transactions for each book, and return the top 5 results by ordering them by descending order.
    popular_books = db.query(
        Transaction.book_id,
        Book.title,
        func.count(Transaction.transaction_id).label('No_of_times_issued')
    ).join(Book).group_by(Transaction.book_id).order_by(func.count(Transaction.transaction_id).desc()).limit(5).all()

    #From the above query, we are appendind all the result into response.
    response = []
    for book in popular_books:
        popular_book = PopularBookResponse(
                                            book_id = book.book_id,
                                            title = book.title,
                                            times_issued = book.No_of_times_issued
                                            )
        response.append(popular_book)

    return response


# Endpoint to clear records of all tables.
@app.delete("/clear-all-tables/")
def clear_all_tables(db: Session = Depends(get_db)):
    try:
        db.query(Transaction).delete()
        db.query(Inventory).delete()
        db.query(Student).delete()
        db.query(Book).delete()
        db.commit()
        return {"message": "All tables cleared successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear tables: {str(e)}")


#For displaying records of books, students, inventory and transactions tables.
@app.get("/books_records/", response_model = List[BookResponse])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books_all = db.query(Book).offset(skip).limit(limit).all()
    return books_all

@app.get("/students_records/", response_model = List[StudentResponse])
def read_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students_all = db.query(Student).offset(skip).limit(limit).all()
    return students_all

@app.get("/inventory_records/", response_model = List[InventoryResponse])
def read_inventory(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    inventory_all = db.query(Inventory).offset(skip).limit(limit).all()
    return inventory_all

@app.get("/transactions_records/", response_model=List[TransactionResponse])
def read_transactions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    transaction_all = db.query(Transaction).offset(skip).limit(limit).all()
    return transaction_all


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)