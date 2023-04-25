<center>

# LIBRARY - PYTHON

**Nahuel Ivan Troisi** <br> **2º ASIR**

## STEPS

This is a Python program that defines several classes to model a library system. Here's how the code works:

Import the datetime module. This is used to work with dates and times.

```python
import datetime
```

Define a Book class with an init() method that takes four parameters: title, author, isbn, and quantity. These parameters are used to initialize instance variables of the same names. The class also defines a repr() method that returns a string representation of the book object.

```python
class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        
    def __repr__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
```

Define a User class with an init() method that takes three parameters: name, email, and role. These parameters are used to initialize instance variables of the same names. The class also defines a repr() method that returns a string representation of the user object.

```python
class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        
    def __repr__(self):
        return f"{self.name} ({self.role})"
    
```

Define a Loan class with an init() method that takes three parameters: book, user, and due_date. These parameters are used to initialize instance variables of the same names. The class also defines a repr() method that returns a string representation of the loan object.

```python
class Loan:
    def __init__(self, book, user, due_date):
        self.book = book
        self.user = user
        self.due_date = due_date
        
    def __repr__(self):
        return f"{self.book} loaned by {self.user} (due on {self.due_date.strftime('%Y-%m-%d')})"
```

Define a Library class with an init() method that initializes three instance variables: books, users, and loans. These variables are empty lists. <br>

The Library class defines several methods to interact with the library system:

A. ***add_book(book):*** This method takes a Book object as a parameter and adds it to the books list.

B. ***remove_book(book):*** This method takes a Book object as a parameter and removes it from the books list.

C. ***search_book_by_title(title):*** This method takes a string parameter and returns a list of Book objects whose title contains the given string (case-insensitive).

D. ***search_book_by_author(author):*** This method takes a string parameter and returns a list of Book objects whose author name contains the given string (case-insensitive).

E. ***add_user(user):*** This method takes a User object as a parameter and adds it to the users list.

F. ***remove_user(user):*** This method takes a User object as a parameter and removes it from the users list.

G. ***search_user_by_name(name):*** This method takes a string parameter and returns a list of User objects whose name contains the given string (case-insensitive).

H. ***search_user_by_email(email):*** This method takes a string parameter and returns a list of User objects whose email contains the given string (case-insensitive).

I. ***loan_book(book, user, due_date):*** This method takes a Book object, a User object, and a datetime.date object as parameters. It creates a Loan object with these parameters and adds it to the loans list. It also decrements the quantity of the book by 1. If the quantity is already 0, an exception is raised.

J. ***return_book(loan):*** This method takes a Loan object as a parameter and removes it from the loans list. It also increments the quantity of the book associated with the loan by 1.

K. ***get_loans_for_user(user):*** This method takes a User object as a parameter and returns a list of Loan objects associated with that user.

L. ***save_to_file(filename):*** This method takes a string parameter representing the filename, and saves the state of the Library object to a file with that name. It writes the books, users, and loans lists to the file in the following format: each list is preceded by a section header ("Books:", "Users:", or "Loans:"). Each item in the list is written to a separate line, with the attributes separated by commas.

M. ***load_from_file(filename):*** This method takes a string parameter representing the filename, and loads the state of the Library object from a file with that name. It reads the file and populates the books, users, and loans lists with the data in the file. The method assumes that the file is in the format created by the save_to_file() method. It uses the Book, User, and Loan classes' constructors to create objects from the data read from the file.

```python
class Library:
    def __init__(self):
        self.books = []
        self.users = []
        self.loans = []
        
    def add_book(self, book):
        self.books.append(book)
        
    def remove_book(self, book):
        self.books.remove(book)
        
    def search_book_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]
    
    def search_book_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]
    
    def add_user(self, user):
        self.users.append(user)
        
    def remove_user(self, user):
        self.users.remove(user)
        
    def search_user_by_name(self, name):
        return [user for user in self.users if name.lower() in user.name.lower()]
    
    def search_user_by_email(self, email):
        return [user for user in self.users if email.lower() in user.email.lower()]
    
    def loan_book(self, book, user, due_date):
        if book.quantity == 0:
            raise Exception("Book not available")
        loan = Loan(book, user, due_date)
        self.loans.append(loan)
        book.quantity -= 1
        
    def return_book(self, loan):
        self.loans.remove(loan)
        loan.book.quantity += 1
        
    def get_loans_for_user(self, user):
        return [loan for loan in self.loans if loan.user == user]
        
    def save_to_file(self, filename):
        with open(filename, "w") as f:
            f.write("Books:\n")
            for book in self.books:
                f.write(f"{book.title},{book.author},{book.isbn},{book.quantity}\n")
                
            f.write("\nUsers:\n")
            for user in self.users:
                f.write(f"{user.name},{user.email},{user.role}\n")
                
            f.write("\nLoans:\n")
            for loan in self.loans:
                f.write(f"{loan.book.isbn},{loan.user.email},{loan.due_date.strftime('%Y-%m-%d')}\n")
                
    def load_from_file(self, filename):
        with open(filename, "r") as f:
            section = None
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == "Books:":
                    section = "books"
                elif line == "Users:":
                    section = "users"
                elif line == "Loans:":
                    section= "loans"
                else:
                    if section == "books":
                        title, author, isbn, quantity = line.split(",")
                        book = Book(title, author, isbn, int(quantity))
                        self.add_book(book)
                    elif section == "users":
                        name, email, role = line.split(",")
                        user = User(name, email, role)
                        self.add_user(user)
                    elif section == "loans":
                        isbn, email, due_date_str = line.split(",")
                        book = next((book for book in self.books if book.isbn == isbn), None)
                        user = next((user for user in self.users if user.email == email), None)
                        due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
                        loan = Loan(book, user, due_date)
                        self.loans.append(loan)
```
