from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://user:password@172.18.0.2:5432/myblog', echo=True)
Base = declarative_base()


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship("Book", back_populates="author")


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="books")


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

author = Author(name="John Smith")
author2 = Author(name="Korol Lev")

session.add(author)
session.add(author2)
session.commit()

book1 = Book(title="Book 1", author=author)
book2 = Book(title="Book 2", author=author)
book3 = Book(title="Book 3", author=author2)
book4 = Book(title="Book 4", author=author2)
book5 = Book(title="Book 5", author=author2)
session.add_all([book1, book2, book3, book4, book5])
session.commit()
