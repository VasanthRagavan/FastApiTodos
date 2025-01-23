from fastapi import Body,FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'title 1', 'author': 'author 1', 'category': 'science'},
    {'title': 'title 2', 'author': 'author 2', 'category': 'science'},
    {'title': 'title 3', 'author': 'author 3', 'category': 'history'},
    {'title': 'title 4', 'author': 'author 4', 'category': 'math'},
    {'title': 'title 5', 'author': 'author 5', 'category': 'math'},
    {'title': 'title 6', 'author': 'author 2', 'category': 'math'},
]
# @app.get('/books')
# def read_All_Books():
#     return BOOKS;


# @app.get('/books/')
# def read_Book(category :str):
#     books = []
#     for book in BOOKS:
#         if book['category'] == category:
#             books.append(book)
#     return books


# @app.get('/books/{book_title}/')
# def read_one_book(book_title :str,category :str):
#     for book in BOOKS:
#         if book['title'] == book_title:
#             return book

@app.get('/books')
def read_all_Books():
    return BOOKS;        
@app.get('/books/{author}/')
def read_by_author(author: str):
    # Filter books where both author and category match
    books = [book for book in BOOKS if book['author'] == author ]
    if not books:
        return {"error": "No books found for the given author and category"}
    return books

@app.post('/books/create_book')
def create_book(new_book=Body()):
    BOOKS.append(new_book)
    

@app.put('/books/update_book')
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if  BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            
            
@app.delete('/books/delete/{book_title}')
def delete(book_title: str):
     for i in range(len(BOOKS)):
        if  BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break