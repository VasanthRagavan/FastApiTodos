from fastapi import FastAPI,Body,Path,Query,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating : int
    published_date :int
    
    def __init__(self,id,title,author,description,rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
        
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed on create",default= None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3,max_length=100)
    rating : int = Field(gt=0,lt=6)
    published_date : int = Field(gt=1900)
    
    
    #This is used to set example shown in the swagger view of post 
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "Example",
                "author": "coding with Roby",
                "description": "good book",
                "rating": "5",
                "published_date": 2021
            }
        }
    }
    
    
    
    
Books=[
    Book(1,'Messi the Goat','vasanth','A book on greatest player',5,2000),
    Book(2,'Better At APi','roby','A book on fast api',5,2004),
    Book(3, 'Python Crash Course', 'Eric Matthes', 'A hands-on, project-based introduction to programming', 5,2021),
    Book(4, 'Automate the Boring Stuff with Python', 'Al Sweigart', 'Practical programming for total beginners', 4,2000),
    Book(5, 'Fluent Python', 'Luciano Ramalho', 'Clear, concise, and effective programming', 3,2000),
    Book(6, 'Learning Python', 'vasanth ', '59 specific ways to write better Python', 4,2020),
    Book(7, 'Effective Python', 'Brett Slatkin', '59 specific ways to write better Python', 2,2015)
]

@app.get('/books',status_code=status.HTTP_200_OK)


def read_all_books():
    return Books




@app.post("/create_books,status_code=status.HTTP_201_CREATED")
def create_books(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    Books.append(find_book_id(new_book))
    

  
#TO AUTOMATICALLY ADD BOOK ID 
def find_book_id(book : Book):
    if len(Books)>0:
        book.id =Books[-1].id+1
    else:
        book.id = 1
        
    return book

@app.get("/books/")
def get_book_by_rating(rating: int=Query(gt=0, lt=6)):
    books_to_return=[]
    for book in Books:
        if book.rating == rating:
            books_to_return.append(book)
            
    return books_to_return

@app.get("/books/year")
def get_book_by_year(publised_date: int):
    books_to_return=[]
    for book in Books:
        if book.published_date == publised_date:
            books_to_return.append(book)
            
    return books_to_return



@app.get("/books/{book_id}")
def get_book(book_id: int=Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail="Book not found")
    
        
        
        

        
@app.delete("/books/delete/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int=Path(gt=0) ):
    book_changed=False
    for i in range(len(Books)):
        if Books[i].id == book_id:
            Books.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")
        
        
        


@app.put("/books/update_book/",status_code=status.HTTP_202_ACCEPTED)
def update_book(book_request: BookRequest):
    book_changed = False
    for i in range(len(Books)):
        if Books[i].id == book_request.id:
            Books[i] = book_request
            book_changed = True
            
    if not book_changed:
        raise HTTPException(status_code=404,detail="Book not found")
        
            


        
