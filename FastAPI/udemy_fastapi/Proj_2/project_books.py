from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    book_id: int
    author: str
    title: str
    description: str
    rating: int
    year: int

    def __init__(self, book_id, author, description, title, rating, year):
        self.book_id = book_id
        self.author = author
        self.description = description
        self.title = title
        self.rating = rating
        self.year = year


class BookRequest(BaseModel):

    book_id: Optional[int] = Field(description="ID is auto increment in the BOOKS", default=None)
    author: str = Field(description="Author field atleast of one character", min_length=1)
    description: str = Field(description="Not more than 100 characters", min_length=1, max_length=100)
    title: str = Field(min_length=4)
    rating: int = Field(description="Rating of book should be between 0 to 5",ge=0, le=5)
    year: int = Field(gt=2000, lt=2030)


    model_config = {
        "json_schema_extra":{
            "example": {
                "author": "A new noob author",
                "description": "This is the description of the noob author book",
                "title": "Life of a Married Man",
                "rating": 5,
                "year": 2025
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]


@app.get("/read_all_books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.post("/create_book", status_code=201)
async def create_book_item(book_req: BookRequest):
    new_book = Book(**book_req.model_dump)
    BOOKS.append(find_book_id(new_book))
    return "Books List updated"

def find_book_id(book: Book):

    book.book_id = 1 if len(BOOKS) == 0 else len(BOOKS)
    return book

@app.get("/books/{book_id}", status_code=200)
async def get_book_id(book_id: int = Path(gt=0, lt=60)):
    for each in BOOKS:
        if each.book_id == book_id:
            return each
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No book with provided {book_id} id")

# @app.get("/books/rating/{rating}") # use this url to avoid fastapi order pick in case of path parameter
@app.get("/books/", status_code=200) # use this for query parameter of rating
async def get_books_rating(rating: int = Query(ge=0, lt=6)):
    result = []
    for each in BOOKS:
        if each.rating == rating:
            result.append(each)
    if result:
        return result
    raise HTTPException(status_code=400, detail= "Please provide a valid rating [0, 5]")

@app.get("/books/publish/", status_code=200)
async def get_books_publish(year: int = Query(gt=2000, lt=2030)):
    result = []
    for each in BOOKS:
        if each.year == year:
            result.append(each)
    if result:
        return result 
    raise(HTTPException(status_code=404,detail = f"No book published in {year}"))