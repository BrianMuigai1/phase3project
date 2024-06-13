import sqlite3
import cmd

class Book:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                book_id INTEGER PRIMARY KEY,
                                title TEXT NOT NULL,
                                author TEXT NOT NULL,
                                genre TEXT,
                                available INTEGER DEFAULT 1
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating books table: {e}")
        finally:
            conn.close()

    def add_book(self, title, author, genre):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO books (title, author, genre) 
                              VALUES (?, ?, ?)''', (title, author, genre))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding book: {e}")
        finally:
            conn.close()

    def view_books(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM books''')
            books = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing books: {e}")
            books = []
        finally:
            conn.close()

        return books

class Member:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                                member_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                email TEXT
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating members table: {e}")
        finally:
            conn.close()

    def add_member(self, name, email):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO members (name, email) 
                              VALUES (?, ?)''', (name, email))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding member: {e}")
        finally:
            conn.close()

    def view_members(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM members''')
            members = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing members: {e}")
            members = []
        finally:
            conn.close()

        return members

class Borrowing:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                transaction_id INTEGER PRIMARY KEY,
                                book_id INTEGER,
                                member_id INTEGER,
                                issue_date TEXT,
                                return_date TEXT,
                                FOREIGN KEY (book_id) REFERENCES books (book_id),
                                FOREIGN KEY (member_id) REFERENCES members (member_id)
                            )''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating transactions table: {e}")
        finally:
            conn.close()

    def borrow_book(self, book_id, member_id, issue_date):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''SELECT available FROM books WHERE book_id = ?''', (book_id,))
            available = cursor.fetchone()[0]
            if available:
                cursor.execute('''INSERT INTO transactions (book_id, member_id, issue_date) 
                                  VALUES (?, ?, ?)''', (book_id, member_id, issue_date))
                cursor.execute('''UPDATE books SET available = 0 WHERE book_id = ?''', (book_id,))
                conn.commit()
                print("Book borrowed successfully.")
            else:
                print("Book is not available.")
        except sqlite3.Error as e:
            print(f"Error borrowing book: {e}")
        finally:
            conn.close()

    def return_book(self, book_id, return_date):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''UPDATE transactions SET return_date = ? 
                              WHERE book_id = ? AND return_date IS NULL''', (return_date, book_id))
            cursor.execute('''UPDATE books SET available = 1 WHERE book_id = ?''', (book_id,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error returning book: {e}")
        finally:
            conn.close()

    def view_borrowed_books(self, member_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''SELECT b.title, b.author, t.issue_date FROM transactions t
                              INNER JOIN books b ON b.book_id = t.book_id
                              WHERE t.member_id = ? AND t.return_date IS NULL''', (member_id,))
            borrowed_books = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error viewing borrowed books: {e}")
            borrowed_books = []
        finally:
            conn.close()

        return borrowed_books

class LibraryCLI(cmd.Cmd):
    intro = 'Welcome to the library management system. Type help or ? to list commands.\n'
    prompt = '(library) '
    db_name = 'library.db'
    
    def __init__(self):
        super().__init__()
        self.book_manager = Book(self.db_name)
        self.member_manager = Member(self.db_name)
        self.borrowing_manager = Borrowing(self.db_name)
        self._initialize_tables()

    def _initialize_tables(self):
        self.book_manager._create_tables()
        self.member_manager._create_tables()
        self.borrowing_manager._create_tables()

    def enumerate_and_select(self, options, prompt):
        if not options:
            print("No options available.")
            return None
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print(f"Invalid choice. Please select a number between 1 and {len(options)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def do_add_book(self, arg):
        'Add a new book: add_book'
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        genre = input("Enter book genre: ")
        self.book_manager.add_book(title, author, genre)
        print(f'Book "{title}" by {author} added to the library.')

    def do_add_member(self, arg):
        'Add a new member: add_member'
        name = input("Enter member name: ")
        email = input("Enter member email: ")
        self.member_manager.add_member(name, email)
        print(f'Member "{name}" added to the library.')

    def do_view_books(self, arg):
        'View all books in the library: view_books'
        books = self.book_manager.view_books()
        if not books:
            print("No books available.")
        else:
            print("Books in the library:")
            for book in books:
                print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Genre: {book[3]}, Available: {'Yes' if book[4] else 'No'}")

    def do_view_members(self, arg):
        'View all members in the library: view_members'
        members = self.member_manager.view_members()
        if not members:
            print("No members registered.")
        else:
            print("Library members:")
            for member in members:
                print(f"Member ID: {member[0]}, Name: {member[1]}, Email: {member[2]}")

    def do_borrow_book(self, arg):
        'Borrow a book: borrow_book'
        books = self.book_manager.view_books()
        if not books:
            print("No books available to borrow.")
            return
        book_options = [f"{book[1]} by {book[2]}" for book in books if book[4] == 1]
        selected_book = self.enumerate_and_select(book_options, "Select a book to borrow: ")
        if selected_book:
            book_id = books[book_options.index(selected_book)][0]
            members = self.member_manager.view_members()
            if not members:
                print("No members registered.")
                return
            member_options = [f"{member[1]}" for member in members]
            selected_member = self.enumerate_and_select(member_options, "Select a member: ")
            if selected_member:
                member_id = members[member_options.index(selected_member)][0]
                issue_date = input("Enter issue date (YYYY-MM-DD): ")
                self.borrowing_manager.borrow_book(book_id, member_id, issue_date)

    def do_return_book(self, arg):
        'Return a book: return_book'
        books = self.book_manager.view_books()
        if not books:
            print("No books available to return.")
            return
        book_options = [f"{book[1]} by {book[2]}" for book in books if book[4] == 0]
        selected_book = self.enumerate_and_select(book_options, "Select a book to return: ")
        if selected_book:
            book_id = books[book_options.index(selected_book)][0]
            return_date = input("Enter return date (YYYY-MM-DD): ")
            self.borrowing_manager.return_book(book_id, return_date)

    def do_view_borrowed_books(self, arg):
        'View borrowed books by member ID: view_borrowed_books'
        members = self.member_manager.view_members()
        if not members:
            print("No members registered.")
            return
        member_options = [f"{member[1]}" for member in members]
        selected_member = self.enumerate_and_select(member_options, "Select a member: ")
        if selected_member:
            member_id = members[member_options.index(selected_member)][0]
            borrowed_books = self.borrowing_manager.view_borrowed_books(member_id)
            if not borrowed_books:
                print("No books borrowed.")
            else:
                print("Borrowed books:")
                for book in borrowed_books:
                    print(f"Title: {book[0]}, Author: {book[1]}, Issue Date: {book[2]}")

    def do_exit(self, arg):
        'Exit the library management system: exit'
        print('Exiting the library management system.')
        return True

if __name__ == '__main__':
    LibraryCLI().cmdloop()
