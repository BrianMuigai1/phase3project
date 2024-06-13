from library_app.book import Book
from library_app.loan import Borrowing
from library_app.member import Member


def main():
    # Add books
    books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "Fiction"),
        ("1984", "George Orwell", "Dystopian")
    ]
    for title, author, genre in books:
        Book(title, author, genre).add_to_library()

    # Add members
    members = [
        ("Jackson Nyangwenya", "jackson.nyangwenya123@yahoo.com"),
        ("Milicent Opipo", "milicentopipo99@gmail.com"),
        ("James Wikido ", "Jwikido@gmail.com")
    ]
    for name, email in members:
        Member(name, email).register()

    # View books
    print("Books in the library:")
    Book.view_books()

    # View members
    print("Library members:")
    Member.view_members()

    # Issue a book
    Borrowing(1, 1, "2024-06-12").issue()

    # Return a book
    Borrowing(1).return_book("2024-06-19")

    # View books again to see changes
    print("Books in the library after issuing and returning:")
    Book.view_books()

if __name__ == "__main__":
    main()
