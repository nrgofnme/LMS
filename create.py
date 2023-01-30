from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, and_
from model import Author, Publisher, Book, Customer, Librarian, Loan, engine
import datetime
import os

Session = sessionmaker(bind=engine)
session = Session()

def user_choice_menu():
    print("------ [ Library Admin Menu ] -------")
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

def clear():
    os.system("cls")

def add_book(book_name, book_isbn, authors, publishers):
    book = Book(book_name, book_isbn, authors, publishers)
    session.add(book)
    session.commit()
    return book

def add_book_from_input():
    clear()
    authors_list = []
    publishers_list = []
    while True:
        book_name = input("Name of the book: ")
        clear()
        while True:
            try:
                book_isbn = input("Books ISBN code: ")
                book_isbn = int(book_isbn)
                clear()
                break
            except ValueError:
                print("Error: Books ISBN must be a number!")
        while True:
            try:
                author_list = session.query(Author)
                for tries in author_list:
                    print(f"{tries.author_id} | {tries}") 
                    authors_list.append(tries.author_id)   
                authors = input("Authors ID: ")
                authors = int(authors)
                clear()
                if authors not in authors_list:
                    clear()
                    print("Error: Author with that ID was not found")
                    continue
                break
            except ValueError:
                print("Error: Authors ID must be a number!")
        while True:
            try:
                publisher_list = session.query(Publisher)
                for tries in publisher_list:
                    print(f"{tries.publisher_id} | {tries.publisher_name}")
                    publishers_list.append(tries.publisher_id)
                publishers = input("Publishers ID: ")
                publishers = int(publishers)
                clear()
                if publishers not in publishers_list:
                    clear()
                    print("Error: Publisher with that ID was not found")
                    continue
                break
            except ValueError:
                print("Error: Publishers ID must be a number!")
        add_book(book_name, book_isbn, authors, publishers)
        user_choice = input("Do you want to add another book? (yes/no): ")
        if user_choice.lower() == "no":
            break
        elif user_choice.lower() == "yes":
            continue
        else:
            print("This input wasn't an option... I'll take it as a 'no' then")
            break
def add_author(author_name, author_surname):
    authors = Author(author_name, author_surname)
    session.add(authors)
    session.commit()
    return authors

def add_author_from_input():
    clear()
    while True:
        author_name = input("Name of the author: ")
        if author_name == "":
            print("This field can't be empty!")
            continue
        clear()
        break
    while True:
        author_surname = input("Surname of the author: ")
        if author_surname == "":
            print("This field can't be empty!")
            continue
        clear()
        add_author(author_name, author_surname)
        print("Author was added successfully")
        break
    while True:
        user_choice = input("Do you want to add another author? (yes/no): ")
        if user_choice.lower() == "no":
            break
        elif user_choice.lower() == "yes":
            add_author_from_input()
        else:
            print("Your input wasn't an option... I'll take it as a 'no' then")
        

def register_customer(customer_name, customer_surname, customer_address):
    customers = Customer(customer_name, customer_surname, customer_address)
    session.add(customers)
    session.commit()
    return customers

def register_customer_from_input():
    clear()
    while True:
        customer_name = input("Customers name: ")
        if customer_name == "":
            clear()
            print("This field can't be empty!")
            continue
        clear()
        break
    while True:
        customer_surname = input("Customers surname: ")
        if customer_surname == "":
            clear()
            print("This field can't be empty!")
            continue
        clear()
        break
    while True:
        customer_address = input("Customers address: ")
        if customer_address == "":
            clear()
            print("This field can't be empty!")
            continue
        clear()
        print("Customer was added successfully")
        return register_customer(customer_name, customer_surname, customer_address)

def new_librarian(librarian_name, librarian_surname):
    librarians = Librarian(librarian_name, librarian_surname)
    session.add(librarians)
    session.commit()
    return librarians

def new_librarian_from_input():
    clear()
    while True:
        librarian_name = input("Librarians name: ")
        if librarian_name == "":
            print("This field can't be empty!")
            continue
        clear()
        break
    while True:
        librarian_surname = input("Librarians surname: ")
        if librarian_surname == "":
            print("This field can't be empty!")
            continue
        clear()
        break
    print("Librarian was added successfully")
    return new_librarian(librarian_name, librarian_surname)

def new_publisher(publisher_name):
    publishers = Publisher(publisher_name)
    session.add(publishers)
    session.commit()
    return publishers

def new_publisher_from_input():
    clear()
    while True:
        publisher_name = input("Publishers name: ")
        if publisher_name == "":
            print("This field can't be empty!")
            continue
        clear()
        break
    print("Publisher was added successfully")
    return new_publisher(publisher_name)

def assign_loan(loan_date, loan_active, customer_id, book_id, librarian_id):
    loans = Loan(loan_date, loan_active, customer_id, book_id, librarian_id)
    session.add(loans)
    session.commit()
    return loans

def assign_loan_from_input():
    clear()
    loan_date = datetime.datetime.now().date()
    loan_active = True
    customer_ids = []
    while True:
        try:
            customer_list = session.query(Customer)
            for tries in customer_list:
                print(f"{tries.customer_id} | {tries.customer_name} {tries.customer_surname}")
                customer_ids.append(tries.customer_id)
            customer_id = input("Enter customers ID: ")
            customer_id = int(customer_id)
            clear()
            if customer_id not in customer_ids:
                clear()
                print("Error: Customer with that ID was not found")
                continue
            break
        except ValueError:
            print("Error: Customer ID must be a number")
    while True:
        books_list = []
        try:
            book_list = session.query(Book).filter(~session.query(Loan).filter(Loan.book_id == Book.book_id).filter(Loan.loan_active == 1).exists()).all()
            for tries in book_list:
                print(f"{tries.book_id} | {tries.book_name}")
                books_list.append(tries.book_id)
            book_id = input("Enter books ID: ")
            book_id = int(book_id)
            clear()
            if book_id not in books_list:
                clear()
                print("Error: Book with that ID was not found")
                continue
            break
        except ValueError:
            print("Error: Book ID must be a number")
    while True:
        librarians_list = []
        try:
            librarian_list = session.query(Librarian)
            for tries in librarian_list:
                print(f"{tries.librarian_id} | {tries.librarian_name} {tries.librarian_surname}")
                librarians_list.append(tries.librarian_id)
            librarian_id = input("Enter librarians ID: ")
            librarian_id = int(librarian_id)
            clear()
            if librarian_list not in librarians_list:
                clear()
                print("Error: Librarian with that ID was not found")
                continue
            break
        except ValueError:
            print("Error: Librarian ID must be a number")
    print("Loan was successful!")
    return assign_loan(loan_date, loan_active, customer_id, book_id, librarian_id)

def check_active_loans(query=session.query(Loan)):
    clear()
    query = session.query(Book, Loan, Customer)\
        .join(Loan, Book.book_id == Loan.book_id)\
        .join(Customer, Loan.customer_id == Customer.customer_id)\
            .filter(Loan.loan_active == True).all()
    if query:
        for x in query:
            print("Loan id: {}, Book id: {}, Book name: {}, Loaned at: {}, Customers name: {} {}".format(
                x.Loan.loan_id,
                x.Book.book_id,
                x.Book.book_name,
                x.Loan.loan_date,
                x.Customer.customer_name,
                x.Customer.customer_surname
            ))
    else:
        print("No books are currently loaned")

def customer_returns(user_input):
    current_date = datetime.datetime.now().date()
    session.query(Loan).filter_by(book_id=user_input).update({Loan.return_date: current_date, Loan.loan_active: False})
    session.commit()

def customer_returns_from_input():
    clear()
    while True:
        try:
            all_loans = session.query(Loan).filter(Loan.loan_active != 0).all()
            for tries in all_loans:
                book = session.query(Book).get(tries.book_id)
                print(f"{tries.book_id} | {book.book_name}")
            user_input = input("Enter book ID which the customer returned: ")
            user_input = int(user_input)
            if not user_input:
                raise ValueError
            else:
                customer_returns(user_input)
                break
        except ValueError:
            print("Error: This field must be a number")
    print("Book was returned successfully")

def search(user_selection):
    if user_selection == '1':
        value = input("Searching for: ")
        author_name_search = session.query(Author).filter(Author.author_name.ilike(f"%{value}%")).all()
        author_surname_search = session.query(Author).filter(Author.author_surname.ilike(f"%{value}%")).all()
        book_name_search = session.query(Book).filter(or_(and_(Book.book_name.ilike(f"%{value}%"), 
            ~session.query(Loan).filter(Loan.book_id == Book.book_id).exists()),and_(Book.book_name.ilike(f"%{value}%"), 
                session.query(Loan).filter(Loan.book_id == Book.book_id, Loan.loan_active == 0).exists()))).all()
        publisher_name_search = session.query(Publisher).filter(Publisher.publisher_name.ilike(f"%{value}%")).all()
        loaned_check = session.query(Loan).filter(Loan.loan_active==True).all()
        for tries in author_name_search:
            print("Authors name", tries)
        for tries in author_surname_search:
            print("Authors surname:", tries)
        for tries in book_name_search:
            print(f"Available book: {tries.book_id} {tries}")
        for tries in publisher_name_search:
            print("Publisher:", tries)
        for tries in loaned_check:
            book = session.query(Book).get(tries.book_id)
            customer = session.query(Customer).get(tries.customer_id)
            librarian = session.query(Librarian).get(tries.librarian_id)
            print(f"Loaned book: ID: {book.book_id} {book.book_name}, by customer: {customer.customer_name} {customer.customer_surname}, assigned by librarian: {librarian.librarian_name} {librarian.librarian_surname}")
    elif user_selection == '2':
        value = input("Searching for: ")
        author_name_search = session.query(Author).filter(Author.author_name.ilike(f"%{value}%")).all()
        author_surname_search = session.query(Author).filter(Author.author_surname.ilike(f"%{value}%")).all()
        for tries in author_name_search:
            print(f"Authors name: {tries.author_name}")
        for tries in author_surname_search:
            print(f"Authors surname: {tries.author_surname}")
    elif user_selection == '3':
        value = input("Searching for: ")
        book_search = session.query(Book).filter(or_(and_(Book.book_name.ilike(f"%{value}%"), 
            ~session.query(Loan).filter(Loan.book_id == Book.book_id).exists()),and_(Book.book_name.ilike(f"%{value}%"), 
            session.query(Loan).filter(Loan.book_id == Book.book_id, Loan.loan_active == 0).exists()))).all()
        if book_search:
            for tries in book_search:
                print(f"Book ID: {tries.book_id} {tries}")
        else:
            print("Found nothing")
    elif user_selection == '4':
        value = input("Searching for: ")
        publisher_search = session.query(Publisher).filter(Publisher.publisher_name.ilike(f"%{value}%")).all()
        if publisher_search:
            for tries in publisher_search:
                print(tries)
        else:
            print("Found nothing")
    elif user_selection == '5':
        loan_search = session.query(Loan, Book, Customer).\
        join(Book, Loan.book_id == Book.book_id).\
        join(Customer, Loan.customer_id == Customer.customer_id).\
        filter(Loan.loan_active==True).all()
        if loan_search:
            for loan, book, customer in loan_search:
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
                librarian_list = session.query(Librarian)
                for tries in librarian_list:
                    print(f"{tries.librarian_id} | {tries.librarian_name} {tries.librarian_surname}")
                value = input("Enter librarians ID: ")
                value = int(value)
                if not value:
                    raise ValueError
                book_search = session.query(Loan, Book, Customer, Librarian).\
                    join(Book, Loan.book_id == Book.book_id).\
                    join(Customer, Loan.customer_id == Customer.customer_id).\
                    join(Librarian, Loan.librarian_id == Librarian.librarian_id).\
                    filter(Loan.librarian_id==value and Loan.loan_active==False).all()
                if book_search:
                    for loan, book, customer, librarian in book_search:
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
    clear()
    user_selection = input("Search by: \n1| Everything (Excluding loaned books)\n2| Author\n3| Book\n4| Publisher\n5| All loaned books\n6| Loaned books by librarians ID\nChoice: ")
    return search(user_selection)    

while True:
    choice = user_choice_menu()
    if choice == "0" or choice == "":
        break
    elif choice == "1":
        new_publisher_from_input()
    elif choice == "2":
        add_author_from_input()
    elif choice == "3":
        add_book_from_input()
    elif choice == "4":
        register_customer_from_input()
    elif choice == "5":
        assign_loan_from_input()
    elif choice == "6":
        customer_returns_from_input()
    elif choice == "7":
        check_active_loans()
    elif choice == '8':
        search_from_input()
    elif choice == '9':
        new_librarian_from_input()