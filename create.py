from sqlalchemy.orm import sessionmaker
from main import Authors, Publishers, Books, Customers, Librarians, Loans, engine
import datetime

Session = sessionmaker(bind=engine)
session = Session()

def user_choice_menu():
    print("------ [ MENU ] -------")
    print("1| Add a new publisher")
    print("2| Add a new author")
    print("3| Add a new book")
    print("4| Register a new customer")
    print("5| Assign a new loan")
    print("6| Customers returns")
    print("7| Check active loans")
    print("8| Search")
    print("9| Add a new librarian")
    print("0| Exit the program")

    choice = input("What's your choice?: ")
    return choice

def add_book(book_name, book_isbn, author, publisher):
    book = Books(book_name, book_isbn, author, publisher)
    session.add(book)
    session.commit()
    return book

def add_book_from_input():
    book_name = input("Name of the book: ")
    while True:
        try:
            book_isbn = input("Books ISBN code: ")
            book_isbn = int(book_isbn)
            break
        except ValueError:
            print("Error: Books ISBN must be a number!")
    while True:
        try:    
            author = input("Authors ID: ")
            author = int(author)
            break
        except ValueError:
            print("Error: Authors ID must be a number!")
    while True:
        try:
            publisher = input("Publishers ID: ")
            publisher = int(publisher)
            break
        except ValueError:
            print("Error: Publishers ID must be a number!")
    return add_book(book_name, book_isbn, author, publisher)

def add_author(author_name, author_surname):
    author = Authors(author_name, author_surname)
    session.add(author)
    session.commit()
    return author

def add_author_from_input():
    author_name = input("Name of the author: ")
    author_surname = input("Surname of the author: ")
    return add_author(author_name, author_surname)

def register_customer(customer_name, customer_surname, customer_address):
    customer = Customers(customer_name, customer_surname, customer_address)
    session.add(customer)
    session.commit()
    return customer

def register_customer_from_input():
    customer_name = input("Customers name: ")
    customer_surname = input("Customers surname: ")
    customer_address = input("Customers address: ")
    return register_customer(customer_name, customer_surname, customer_address)

def new_librarian(librarian_name, librarian_surname):
    librarian = Librarians(librarian_name, librarian_surname)
    session.add(librarian)
    session.commit()
    return librarian

def new_librarian_from_input():
    librarian_name = input("Librarians name: ")
    librarian_surname = input("Librarians surname: ")
    return new_librarian(librarian_name, librarian_surname)

def new_publisher(publisher_name):
    publisher = Publishers(publisher_name)
    session.add(publisher)
    session.commit()
    return publisher

def new_publisher_from_input():
    publisher_name = input("Publishers name: ")
    return new_publisher(publisher_name)

def assign_loan(loan_date, loan_active, customer_id, book_id, librarian_id):
    loan = Loans(loan_date, loan_active, customer_id, book_id, librarian_id)
    session.add(loan)
    session.commit()
    return loan

def assign_loan_from_input():
    loan_date = datetime.datetime.now().date()
    loan_active = True
    while True:
        try:
            customer_id = input("Enter customers ID: ")
            customer_id = int(customer_id)
            break
        except ValueError:
            print("Error: Customer ID must be a number")
    while True:
        try:
            book_id = input("Enter books ID: ")
            book_id = int(book_id)
            break
        except ValueError:
            print("Error: Book ID must be a number")
    while True:
        try:
            librarian_id = input("Enter librarians ID: ")
            librarian_id = int(librarian_id)
            break
        except ValueError:
            print("Error: Librarian ID must be a number")
    return assign_loan(loan_date, loan_active, customer_id, book_id, librarian_id)

def check_active_loans(query=session.query(Loans)):
    query = session.query(Books, Loans, Customers)\
        .join(Loans, Books.book_id == Loans.book_id)\
        .join(Customers, Loans.customer_id == Customers.customer_id)\
            .filter(Loans.loan_active == True).all()
    if query:
        for x in query:
            print("Loan id: {}, Book id: {}, Book name: {}, Loaned at: {}, Customers name: {} {}".format(
                x.Loans.loan_id,
                x.Books.book_id,
                x.Books.book_name,
                x.Loans.loan_date,
                x.Customers.customer_name,
                x.Customers.customer_surname
            ))
    else:
        print("No books are currently loaned")

def customer_returns(user_input):
    current_date = datetime.datetime.now().date()
    session.query(Loans).filter_by(book_id=user_input).update({Loans.return_date: current_date, Loans.loan_active: False})
    session.commit()

def customer_returns_from_input():
    while True:
        try:
            user_input = input("Enter book ID which the customer returned: ")
            user_input = int(user_input)
            if not user_input:
                raise ValueError
            else:
                customer_returns(user_input)
                break
        except ValueError:
            print("Error: This field must be a number")

def search(user_selection):
    if user_selection == '1':
        value = input("Searching for: ")
        query1 = session.query(Authors).filter(Authors.author_name.ilike(f"%{value}%")).all()
        query2 = session.query(Authors).filter(Authors.author_surname.ilike(f"%{value}%")).all()
        query3 = session.query(Books).filter(Books.book_name.ilike(f"%{value}%")).filter(~session.query(Loans).filter(Loans.book_id == Books.book_id).exists()).all()
        query4 = session.query(Publishers).filter(Publishers.publisher_name.ilike(f"%{value}%")).all()
        query5 = session.query(Loans).filter(Loans.loan_active==True).all()
        for querys in query1:
            print("Authors name", querys)
        for querys in query2:
            print("Authors surname:", querys)
        for querys in query3:
            print("Available book:", querys)
        for querys in query4:
            print("Publisher:", querys)
        for querys in query5:
            book = session.query(Books).get(querys.book_id)
            customer = session.query(Customers).get(querys.customer_id)
            librarian = session.query(Librarians).get(querys.librarian_id)
            print(f"Loaned book: {book.book_name}, by customer: {customer.customer_name} {customer.customer_surname}, assigned by librarian: {librarian.librarian_name} {librarian.librarian_surname}")
    elif user_selection == '2':
        value = input("Searching for: ")
        query1 = session.query(Authors).filter(Authors.author_name.ilike(f"%{value}%")).all()
        query2 = session.query(Authors).filter(Authors.author_surname.ilike(f"%{value}%")).all()
        for querys in query1:
            print("Authors name", querys)
        for querys in query2:
            print("Authors surname:", querys)
    elif user_selection == '3':
        value = input("Searching for: ")
        query = session.query(Books).filter(Books.book_name.ilike(f"%{value}%")).filter(~session.query(Loans).filter(Loans.book_id == Books.book_id).exists()).all()
        if query:
            for querys in query:
                print(querys)
        else:
            print("Found nothing")
    elif user_selection == '4':
        value = input("Searching for: ")
        query = session.query(Publishers).filter(Publishers.publisher_name.ilike(f"%{value}%")).all()
        if query:
            for querys in query:
                print(querys)
        else:
            print("Found nothing")
    elif user_selection == '5':
        query = session.query(Loans, Books, Customers).\
        join(Books, Loans.book_id == Books.book_id).\
        join(Customers, Loans.customer_id == Customers.customer_id).\
        filter(Loans.loan_active==True).all()
        if query:
            for loan, book, customer in query:
                print("Book `{}` was loaned to {} {} on {} ".format(
                    book.book_name,
                    customer.customer_name,\
                    customer.customer_surname,
                    loan.loan_date
                ))
        else:
                print("Nothing is loaned")
    elif user_selection == '6':
        while True:
            try:
                value = input("Enter librarians ID: ")
                value = int(value)
                if not value:
                    raise ValueError
                query = session.query(Loans, Books, Customers, Librarians).\
                    join(Books, Loans.book_id == Books.book_id).\
                    join(Customers, Loans.customer_id == Customers.customer_id).\
                    join(Librarians, Loans.librarian_id == Librarians.librarian_id).\
                    filter(Loans.librarian_id==value and Loans.loan_active==False).all()
                if query:
                    for loan, book, customer, librarian in query:
                        print("Librarian {} {} loaned a book named `{}` to {} {} on {}".format(
                            librarian.librarian_name,
                            librarian.librarian_surname,
                            book.book_name,
                            customer.customer_name,
                            customer.customer_surname,
                            loan.loan_date
                        ))
                    break
                else:
                    print("Nothing is loaned by this librarian")
                    break
            except ValueError:
                print("Librarian ID must be an integer!")
    
def search_from_input():
    user_selection = input("Search by: \n1|Everything (Excluding loaned books)\n2|Author\n3|Book\n4|Publisher\n5|All loaned books\n6|Loaned books by librarians ID\n")
    return search(user_selection)    
