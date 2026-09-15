from pydantic import BaseModel
from typing import Optional

class BooksBody(BaseModel):

    # sr: Optional[int]
    title: str
    author: str
    category: str