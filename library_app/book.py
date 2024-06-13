import sqlite3

class Book:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create books table
        cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                            book_id INTEGER PRIMARY KEY,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            genre TEXT,
                            available INTEGER DEFAULT 1
                        )''')

        conn.commit()
        conn.close()

    def add_book(self, title, author, genre):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO books (title, author, genre) 
                          VALUES (?, ?, ?)''', (title, author, genre))
        conn.commit()
        conn.close()

    def issue_book(self, book_id, member_id, issue_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if the book is available
        cursor.execute('''SELECT available FROM books WHERE book_id = ?''', (book_id,))
        available = cursor.fetchone()[0]
        if available:
            cursor.execute('''INSERT INTO transactions (book_id, member_id, issue_date) 
                              VALUES (?, ?, ?)''', (book_id, member_id, issue_date))
            cursor.execute('''UPDATE books SET available = 0 WHERE book_id = ?''', (book_id,))
            conn.commit()
            print("Book issued successfully.")
        else:
            print("Book is not available.")
        
        conn.close()

    def return_book(self, book_id, return_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''UPDATE transactions SET return_date = ? 
                          WHERE book_id = ? AND return_date IS NULL''', (return_date, book_id))
        cursor.execute('''UPDATE books SET available = 1 WHERE book_id = ?''', (book_id,))
        conn.commit()
        conn.close()

    def view_books(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM books''')
        books = cursor.fetchall()
        conn.close()

        if not books:
            print("No books available.")
        else:
            print("Books in the library:")
            for book in books:
                print("Book ID:", book[0])
                print("Title:", book[1])
                print("Author:", book[2])
                print("Genre:", book[3])
                print("Available:", "Yes" if book[4] else "No")
                print()
