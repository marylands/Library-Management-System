import sqlite3
import os

# Create Library Database
def create_database():
    # Remove existing database file if it exists(i was getting an error before this)
    try:
        os.remove("library.db")
    except FileNotFoundError:
        pass

    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    # Create Books table
    cursor.execute('''CREATE TABLE Books (
                      id INTEGER PRIMARY KEY,
                      title TEXT,
                      author TEXT,
                      category TEXT,
                      price REAL,
                      status TEXT)''')

    # Create Transactions table
    cursor.execute('''CREATE TABLE Transactions (
                      id INTEGER PRIMARY KEY,
                      book_id INTEGER,
                      customer_name TEXT,
                      issue_date TEXT,
                      return_date TEXT,
                      FOREIGN KEY (book_id) REFERENCES Books(id))''')

    connection.commit()
    connection.close()


# Adding a book to the database
def add_book(title, author, category, price):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO Books (title, author, category, price, status) VALUES (?, ?, ?, ?, ?)",
                   (title, author, category, price, "Available"))

    connection.commit()
    connection.close()

# Issue a book to a customer
def issue_book(book_id, customer_name, issue_date, return_date):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE Books SET status='Issued' WHERE id=?", (book_id,))
    cursor.execute("INSERT INTO Transactions (book_id, customer_name, issue_date, return_date) VALUES (?, ?, ?, ?)",
                   (book_id, customer_name, issue_date, return_date))

    connection.commit()
    connection.close()

# Display available books
def display_available_books():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Books WHERE status='Available'")
    available_books = cursor.fetchall()

    for book in available_books:
        print("ID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("Category:", book[3])
        print("Price:", book[4])
        print("Status:", book[5])
        print("-------------------------")

    connection.close()

# Function to display books that are not available (issued)
def display_issued_books():
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Books WHERE status='Issued'")
    issued_books = cursor.fetchall()

    if len(issued_books) == 0:
        print("No books are currently issued.")
    else:
        print("Issued Books:")
        for book in issued_books:
            print("ID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("Category:", book[3])
            print("Price:", book[4])
            print("-------------------------")

    connection.close()

create_database()

# Add more books
add_book("To Kill a Mockingbird", "Harper Lee", "Classic", "12.99")
add_book("1984", "George Orwell", "Science Fiction", "9.99")
add_book("Rich Dad, Poor Dad", "Robert T. Kiyosaki", "Investing", "11.50")
add_book("The Cat in The Hat", "Dr.Seuss", "Childrens Literature", "7.99")

# Issue a book
issue_book(2, "Joshua Eckroth", "2024-04-25", "2024-05-09")
issue_book(3, "Daniel Plante", "2024-04-23", "2024-05-07")


# Function to display who has checked out a specific book
def display_checked_out_by(book_id):
    connection = sqlite3.connect("library.db")
    cursor = connection.cursor()

    cursor.execute("SELECT customer_name, issue_date, return_date FROM Transactions WHERE book_id=?", (book_id,))
    transactions = cursor.fetchall()

    if len(transactions) == 0:
        print("This book is not currently checked out.")
    else:
        print("Checked Out Information for Book ID", book_id)
        for transaction in transactions:
            print("Checked Out By:", transaction[0])
            print("Issue Date:", transaction[1])
            print("Return Date:", transaction[2])
            print("-------------------------")

    connection.close()

# Function to display the menu
def display_menu():
    print("\nLibrary Management System Menu:")
    print("1. Add a Book")
    print("2. Issue a Book")
    print("3. Display Available Books")
    print("4. Display Issued Books")
    print("5. View who has checked out a book")
    print("6. Exit Library Management System")

# Function to interact with the user and perform selected action
def interact_with_user():
    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            category = input("Enter the category of the book: ")
            price = float(input("Enter the price of the book: "))
            add_book(title, author, category, price)
            print("Book added successfully!")

        elif choice == "2":
            # Add functionality to issue a book
            pass

        elif choice == "3":
            print("Available Books:")
            display_available_books()

        elif choice == "4":
            print("Issued Books:")
            display_issued_books()

        elif choice == "5":
            book_id = int(input("Enter the ID of the book: "))
            display_checked_out_by(book_id)

        elif choice == "6":
            print("Exiting...Thank You for using Library Management System")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

# Interact with the user
interact_with_user()



