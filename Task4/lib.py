import datetime

class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        
    def __repr__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
class User:
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role
        
    def __repr__(self):
        return f"{self.name} ({self.role})"
    
class Loan:
    def __init__(self, book, user, due_date):
        self.book = book
        self.user = user
        self.due_date = due_date
        
    def __repr__(self):
        return f"{self.book} loaned by {self.user} (due on {self.due_date.strftime('%Y-%m-%d')})"
    
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