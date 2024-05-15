from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Float, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Anime(Base):
    __tablename__ = 'anime'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    author = Column(String(40), nullable=False)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f'Anime title:{self.title}; Author: {self.author}; Price: {self.price}'
    
engine = create_engine('sqlite:///anime.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()





anime1 = Anime(title='Howl\'s moving castle', author='Hayao miyazaki', price=999999.9)
session.add(anime1)
session.commit()

anime2 = Anime(title='My neighbor Totoro', author='Hayao miyazaki', price=999999.9)
session.add(anime2)
session.commit()

result = session.query(Anime).all()
for row in result:
    print(row)