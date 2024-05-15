from flask import Flask, redirect, url_for, render_template, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class Anime(Base):
    __tablename__ = 'anime'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    author = Column(String(40), nullable=False)
    price = Column(Float, nullable=False)

    def __str__(self):
        return f'Anime title: {self.title}; Author: {self.author}; Price: {self.price}'
    
engine = create_engine('sqlite:///anime.db', echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user')
def user():
    if 'user' in flask_session:
        subjects = ['Howl\'s moving castle', 'Hayao miyazaki', 'DB']
        return render_template('user.html', subjects=subjects)
    return redirect(url_for('login'))

@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    flask_session.pop('user', None)
    return 'You are logged out'

@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        if title and author and price:
            try:
                price = float(price)
                new_anime = Anime(title=title, author=author, price=price)
                db_session.add(new_anime)
                db_session.commit()
                return 'Data added successfully'
            except ValueError:
                return 'Invalid input for price'
    return render_template('anime.html')

if __name__ == "__main__":
    app.run(debug=True)

anime1 = Anime(title='Howl\'s moving castle', author='Hayao miyazaki', price=999999.0)
db_session.add(anime1)
db_session.commit()

anime2 = Anime(title='My neighbor Totoro', author='Hayao miyazaki', price=999999.9)
db_session.add(anime2)
db_session.commit()

result = db_session.query(Anime).all()
for row in result:
    print(row)