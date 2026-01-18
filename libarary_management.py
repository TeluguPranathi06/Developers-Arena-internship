import json
import os
from datetime import datetime, timedelta


class Book:
    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.due_date = None

    def check_out(self):
        self.available = False
        self.due_date = datetime.now() + timedelta(days=14)

    def return_book(self):
        self.available = True
        self.due_date = None

    def __str__(self):
        if self.available:
            status = "Available"
        else:
            status = f"Due on {self.due_date.date()}"
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | {status}"



class Member:
    MAX_BORROW = 5

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, isbn):
        if len(self.borrowed_books) >= Member.MAX_BORROW:
            raise Exception("Borrow limit reached (Max 5 books)")
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        self.borrowed_books.remove(isbn)

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) | Borrowed: {len(self.borrowed_books)}"


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.load_data()

    def add_book(self, book):
        if book.isbn in self.books:
            raise Exception("Book already exists")
        self.books[book.isbn] = book

    def find_book(self, keyword):
        results = []
        for book in self.books.values():
            if (keyword.lower() in book.title.lower() or
                keyword.lower() in book.author.lower() or
                keyword == book.isbn):
                results.append(book)
        return results

    def register_member(self, member):
        if member.member_id in self.members:
            raise Exception("Member already exists")
        self.members[member.member_id] = member

    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            raise Exception("Member not found")
        if isbn not in self.books:
            raise Exception("Book not found")

        book = self.books[isbn]
        member = self.members[member_id]

        if not book.available:
            raise Exception("Book not available")

        member.borrow_book(isbn)
        book.check_out()

    def return_book(self, member_id, isbn):
        if member_id not in self.members:
            raise Exception("Member not found")
        if isbn not in self.books:
            raise Exception("Book not found")

        book = self.books[isbn]
        member = self.members[member_id]

        if isbn not in member.borrowed_books:
            raise Exception("Book not borrowed by this member")

        overdue_days = 0
        if book.due_date and datetime.now() > book.due_date:
            overdue_days = (datetime.now() - book.due_date).days

        member.return_book(isbn)
        book.return_book()
        return overdue_days

    def statistics(self):
        total_books = len(self.books)
        available_books = sum(book.available for book in self.books.values())
        return total_books, available_books

    def save_data(self):
        with open("books.json", "w") as f:
            json.dump(
                {isbn: {
                    "title": b.title,
                    "author": b.author,
                    "year": b.year,
                    "available": b.available,
                    "due_date": b.due_date.isoformat() if b.due_date else None
                } for isbn, b in self.books.items()}, f, indent=4
            )

        with open("members.json", "w") as f:
            json.dump(
                {mid: {
                    "name": m.name,
                    "borrowed_books": m.borrowed_books
                } for mid, m in self.members.items()}, f, indent=4
            )

    def load_data(self):
        if os.path.exists("books.json"):
            with open("books.json") as f:
                data = json.load(f)
                for isbn, b in data.items():
                    book = Book(b["title"], b["author"], isbn, b["year"])
                    book.available = b["available"]
                    book.due_date = datetime.fromisoformat(b["due_date"]) if b["due_date"] else None
                    self.books[isbn] = book

        if os.path.exists("members.json"):
            with open("members.json") as f:
                data = json.load(f)
                for mid, m in data.items():
                    member = Member(m["name"], mid)
                    member.borrowed_books = m["borrowed_books"]
                    self.members[mid] = member


def menu():
    library = Library()

    while True:
        print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Search Book")
        print("6. View Statistics")
        print("7. Exit")

        choice = input("Enter choice: ")

        try:
            if choice == "1":
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                year = input("Year: ")
                library.add_book(Book(title, author, isbn, year))
                print("✅ Book added successfully")

            elif choice == "2":
                name = input("Member Name: ")
                member_id = input("Member ID: ")
                library.register_member(Member(name, member_id))
                print("✅ Member registered successfully")

            elif choice == "3":
                member_id = input("Member ID: ")
                isbn = input("ISBN: ")
                library.borrow_book(member_id, isbn)
                print("✅ Book borrowed successfully")

            elif choice == "4":
                member_id = input("Member ID: ")
                isbn = input("ISBN: ")
                overdue = library.return_book(member_id, isbn)
                print(f"✅ Book returned | Overdue days: {overdue}")

            elif choice == "5":
                keyword = input("Enter title / author / ISBN: ")
                results = library.find_book(keyword)
                if results:
                    for book in results:
                        print(book)
                else:
                    print("❌ No books found")

            elif choice == "6":
                total, available = library.statistics()
                print(f"📊 Total Books: {total}")
                print(f"📊 Available Books: {available}")

            elif choice == "7":
                library.save_data()
                print("💾 Data saved. Exiting system.")
                break

            else:
                print("❌ Invalid choice")

        except Exception as e:
            print("⚠ Error:", e)


menu()
