from fastapi import FastAPI
from schema import BooksBody
from constant import BOOKS

app = FastAPI(title="Books Project")

@app.get("/books")
async def get_all_books():
    return {
        "data": BOOKS,
        "message": "Welcome to FastApi"
        }

@app.get("/get_book/{category}")
async def get_title_book(book_author: str, category: str):
    """
    API to get book based on author and category
    """
    for each_book in BOOKS:
        if each_book.get("author").lower() == book_author.lower() and each_book.get("category") == category:
            return each_book
    return "No book for provided author and category"

@app.get("/books/{book_num}")
async def get_one_books(book_num: str):
    for each in BOOKS:
        if each.get('sr') and each['sr'] == int(book_num):
            return{
                "data": each,
                "message": "Book data extracted"
            }
    return{
        "data": [],
        "message": "No data"
    }


@app.post("/books/create_book")
async def create_book(new_book: BooksBody):
    newbook = new_book.model_dump()
    newbook['sr'] = len(BOOKS) + 1
    BOOKS.append(newbook)
    return "New Book Added"


@app.put("/books/update_book")
async def update_book(book_id: int, update_data: BooksBody):
    book_data = update_data.model_dump()
    for each in BOOKS:
        if each['sr'] == book_id:
            each['title'] = book_data['title']
            each['author'] = book_data['author']
            each['category'] = book_data['category']
            return each
    return "Please enter a valid ID"


@app.delete("/books/remove_book/{book_title}")
async def remove_book(book_title: str):
    for each in BOOKS:
        if each.get('title', "").lower() == book_title.lower():
            BOOKS.pop(BOOKS.index(each))
            return f"{book_title} is deleted"
    return "Please enter a valid title present in the BOOKS list"

""" Get all the books for a specific author """

@app.get("/fetch/books/{author}")
async def fetch_author_book(author: str):

    result = []
    for each in BOOKS:
        if each.get('author', '').lower() == author.lower():
            result.append(each)
    return result