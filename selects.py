from sqlalchemy.orm import sessionmaker
from main import Author, Book, engine

Session = sessionmaker(bind=engine)
session = Session()

# Получаем всех авторов
authors = session.query(Author).all()
print(authors)
for author in authors:
    print(author.name)
