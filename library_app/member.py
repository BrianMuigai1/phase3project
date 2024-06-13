import sqlite3

class Member:
    def __init__(self, db_name='library.db'):
        self.db_name = db_name

    def _create_tables(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create members table
        cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                            member_id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            email TEXT
                        )''')

        conn.commit()
        conn.close()

    def add_member(self, name, email):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO members (name, email) 
                          VALUES (?, ?)''', (name, email))
        conn.commit()
        conn.close()

    def view_members(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM members''')
        members = cursor.fetchall()
        conn.close()

        if not members:
            print("No members registered.")
        else:
            print("Library members:")
            for member in members:
                print("Member ID:", member[0])
                print("Name:", member[1])
                print("Email:", member[2])
                print()
