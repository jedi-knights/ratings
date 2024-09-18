# SQL Model Example

This example demonstrates how to use the `SQLModel` class to create a simple SQL model.

```python
from typing import Optional, List
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship

engine = create_engine('sqlite:///orm.db')

class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=50)
    
    books: List['Book'] = Relationship(back_populates='author')

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=100)
    content: str
    author_id: int = Field(foreign_key='author.id')

    author: Author = Relationship(back_populates='books')


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    author1 = Author(name='Alice', email='alice.example.com')
    author2 = Author(name='Bob', email='bob.example.com')
    book1 = Book(title='Book1', content='Content1', author=author1)
    book2 = Book(title='Book2', content='Content2', author=author2)
    book3 = Book(title='Book3', content='Content3', author=author1)

    session.add_all([author1, author2, book1, book2, book3])
    session.commit()


with Session(engine) as session:
    statement = select(Book)
    results = session.exec(statement)
    for book in results:
        print(book)
```
