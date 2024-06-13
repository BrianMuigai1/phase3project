import sqlite3

class Borrowing:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create transactions table
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
        conn.close()

    def borrow_book(self, book_id, member_id, issue_date):
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
            print("Book borrowed successfully.")
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

    def view_borrowed_books(self, member_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT b.title, b.author, t.issue_date FROM transactions t
                          INNER JOIN books b ON b.book_id = t.book_id
                          WHERE t.member_id = ? AND t.return_date IS NULL''', (member_id,))
        borrowed_books = cursor.fetchall()
        conn.close()

        if not borrowed_books:
            print("No books borrowed.")
        else:
            print("Borrowed books:")
            for book in borrowed_books:
                print("Title:", book[0])
                print("Author:", book[1])
                print("Issue Date:", book[2])
                print()