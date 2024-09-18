from typing import Optional, List
from sqlmodel import SQLModel, create_engine, Session, Field, Relationship, select

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

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)

    # with Session(engine) as session:
    #     author1 = Author(name='Alice', email='alice.example.com')
    #     author2 = Author(name='Bob', email='bob.example.com')
    #     book1 = Book(title='Book1', content='Content1', author=author1)
    #     book2 = Book(title='Book2', content='Content2', author=author2)
    #     book3 = Book(title='Book3', content='Content3', author=author1)
    #
    #     session.add_all([author1, author2, book1, book2, book3])
    #     session.commit()

    with Session(engine) as session:
        # statement = select(Book)
        # results = session.exec(statement).all()
        # print(results)

        # statement = select(Book).where(Book.title == "Book3")
        # books = session.exec(statement).all()
        # for book in books:
        #     print(book)

        # statement = select(Book, Author).join(Author)
        # books_with_authors = session.exec(statement).all()
        #
        # for book, author in books_with_authors:
        #     print(f"Book: {book.title}, Author: {author.name}")


        # Update a Book
        # book_to_update = session.exec(select(Book).where(Book.title == "Book3")).first()
        # if book_to_update:
        #     book_to_update.title = "Updated Book3"
        #     session.add(book_to_update)
        #     session.commit()
        #     session.refresh(book_to_update)
        #     print(f"Updated book: {book_to_update.title}")


        # Delete a Book
        book_to_delete = session.exec(select(Book).where(Book.title == "Updated Book3")).first()
        if book_to_delete:
            session.delete(book_to_delete)
            session.commit()
