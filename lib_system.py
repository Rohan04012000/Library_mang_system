from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.exc import IntegrityError

#In this task, we are connecting to a SQLite database.
DATABASE_URL = "sqlite:///./library_data.db"

# SQLAlchemy setup
#Creating a SQLAlchemy engine. connect_args = {"check_same_thread":False} is needed only for SQLite. Not needed for other databases.
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = engine))
Base = declarative_base()

# Association table for many-to-many relationship between Students and Books
student_books = Table('student_books', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)

#We are using Base class to create the SQLAlchemy models.
#Creating Classes and these Classes are SQLAlchemy models.
class BOOK(Base):
    #The __tablename__ = "books" tells the name of the table to use in the database for Book model.
    __tablename__ = "Books"
    #Now creating attributes which represents Columns in table Books.
    #id is set to primary_key, therefore by default it supports auto-increment.
    id = Column(Integer, primary_key = True, index = True)
    #Title of book and Name of Author to be entered as Text/String.
    title_of_book = Column(String, index = True)
    author_of_book = Column(String, index = True)

#Student model for registering Students.
class STUDENT(Base):
    #For models STUDENT, creating table Students, which will register the details of students.
    __tablename__ = 'Students'
    id = Column(Integer, primary_key = True, index = True)
    name_of_student = Column(String, index = True)
    email_of_student = Column(String, index = True)

    Books = relationship("Books", secondary = student_books, back_populates = "Students")

#Inventory model for keep the check on books.
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer)
    book = relationship("Book")

Book.students = relationship("Student", secondary=student_books, back_populates="books")

# Pydantic models
class BookCreate(BaseModel):
    title: str
    author: str

class StudentCreate(BaseModel):
    name: str

class InventoryUpdate(BaseModel):
    book_id: int
    quantity: int

class IssueBook(BaseModel):
    student_id: int
    book_id: int

class ReturnBook(BaseModel):
    student_id: int
    book_id: int

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI instance
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: sessionmaker = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.post("/students/", response_model=StudentCreate)
def create_student(student: StudentCreate, db: sessionmaker = Depends(get_db)):
    db_student = Student(name=student.name)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.post("/inventory/", response_model=InventoryUpdate)
def update_inventory(inventory: InventoryUpdate, db: sessionmaker = Depends(get_db)):
    db_inventory = db.query(Inventory).filter(Inventory.book_id == inventory.book_id).first()
    if db_inventory:
        db_inventory.quantity = inventory.quantity
    else:
        db_inventory = Inventory(book_id=inventory.book_id, quantity=inventory.quantity)
        db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@app.post("/issue/", response_model=IssueBook)
def issue_book(issue: IssueBook, db: sessionmaker = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == issue.student_id).first()
    db_book = db.query(Book).filter(Book.id == issue.book_id).first()
    db_inventory = db.query(Inventory).filter(Inventory.book_id == issue.book_id).first()

    if not db_student:
        raise HTTPException(status_code=400, detail="Student not found")
    if not db_book:
        raise HTTPException(status_code=400, detail="Book not found")
    if not db_inventory or db_inventory.quantity == 0:
        raise HTTPException(status_code=400, detail="Book out of stock")
    if len(db_student.books) >= 3:
        raise HTTPException(status_code=400, detail="Student cannot hold more than 3 books")

    db_student.books.append(db_book)
    db_inventory.quantity -= 1
    db.commit()
    return issue

@app.post("/return/", response_model=ReturnBook)
def return_book(return_: ReturnBook, db: sessionmaker = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == return_.student_id).first()
    db_book = db.query(Book).filter(Book.id == return_.book_id).first()
    db_inventory = db.query(Inventory).filter(Inventory.book_id == return_.book_id).first()

    if not db_student:
        raise HTTPException(status_code=400, detail="Student not found")
    if not db_book:
        raise HTTPException(status_code=400, detail="Book not found")
    if db_book not in db_student.books:
        raise HTTPException(status_code=400, detail="This book is not issued to the student")

    db_student.books.remove(db_book)
    db_inventory.quantity += 1
    db.commit()
    return return_

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
