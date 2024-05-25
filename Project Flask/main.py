from flask import Flask, redirect, url_for, render_template, request, session as flask_session
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import re

from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

Base = declarative_base()

class Anime(Base):
    __tablename__ = 'anime'
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False)
    director = Column(String(40), nullable=False)
    rating = Column(Float, nullable=False)

    def __str__(self):
        return f'Anime title: {self.title}; Director: {self.director}; Rating: {self.rating}'
    
engine = create_engine('sqlite:///animes.db', echo=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def password_validator(password):
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password_validator(password):
            flask_session['user'] = username
            return redirect(url_for('user'))
        else:
            return 'Password must have at least 8 characters, 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character. Please try again.'
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        flask_session['user'] = username
        return redirect(url_for('user'))
    return render_template('login.html')

@app.route('/user')
def user():
    user_animes = Session.query(Anime).all()
    return render_template('user.html', animes=user_animes)

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
        director = request.form['director']
        rating = request.form['rating']
        if title and director and rating:
            try:
                rating = float(rating)
                new_anime = Anime(title=title, director=director, rating=rating)
                Session.add(new_anime)
                Session.commit()
                return 'Data added successfully'
            except ValueError:
                return 'Invalid input for rating'
    return render_template('anime.html')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

website = requests.get("https://myanimelist.net/anime/genre/39/Detective", headers=headers).text
soup = BeautifulSoup(website, 'lxml')
animes = soup.find_all('div', class_= 'js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-1') + soup.find_all('div', class_= 'js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-2') + soup.find_all('div', class_='js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-3') + soup.find_all('div', class_= 'js-anime-category-producer seasonal-anime js-seasonal-anime js-anime-type-all js-anime-type-5')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        date = request.form['search_date']
        genres = request.form['search_genre']
        animess = []
        if genres != '' and date == '':
            for anime in animes:
                name = anime.find('h2', class_= 'h2_anime_title').text
                name = name.strip()

                info = anime.find('div', class_= 'info').text.split()
                type_year = info[0].split(',')
                type = re.sub(",", "", type_year[0])

                year_status = list(info[1])
                year1 = []
                x = 0
                while x < 4:
                    year1.append(year_status[x])
                    x+=1
                year = ''.join(year1)
                status = []
                for i in year_status:
                    if i not in year1:
                        status.append(i)
                status = ''.join(status)
                episodes = info[2] + info[3] + ' ' + info[4] + info[5]
                genre = anime.find('div', class_= 'genres-inner js-genre-inner').text.split()
                for i in genre:
                    if i == genres:
                        animess.append([name, type, year, status, episodes, genre])
        if genres == '' and date != '':
            for anime in animes:
                name = anime.find('h2', class_= 'h2_anime_title').text
                name = name.strip()

                info = anime.find('div', class_= 'info').text.split()
                type_year = info[0].split(',')
                type = re.sub(",", "", type_year[0])

                year_status = list(info[1])
                year1 = []
                x = 0
                while x < 4:
                    year1.append(year_status[x])
                    x+=1
                year = ''.join(year1)
                status = []
                for i in year_status:
                    if i not in year1:
                        status.append(i)
                status = ''.join(status)
                episodes = info[2] + info[3] + ' ' + info[4] + info[5]
                genre = anime.find('div', class_= 'genres-inner js-genre-inner').text.split()
                if date == year:
                    animess.append([name, type, year, status, episodes, genre])
        if genres != '' and date != '':
            for anime in animes:
                name = anime.find('h2', class_= 'h2_anime_title').text
                name = name.strip()

                info = anime.find('div', class_= 'info').text.split()
                type_year = info[0].split(',')
                type = re.sub(",", "", type_year[0])

                year_status = list(info[1])
                year1 = []
                x = 0
                while x < 4:
                    year1.append(year_status[x])
                    x+=1
                year = ''.join(year1)
                status = []
                for i in year_status:
                    if i not in year1:
                        status.append(i)
                status = ''.join(status)
                episodes = info[2] + info[3] + ' ' + info[4] + info[5]
                genre = anime.find('div', class_= 'genres-inner js-genre-inner').text.split()
                for i in genre:
                    if i == genres and year == date:
                        animess.append([name, type, year, status, episodes, genre])
        return render_template('search.html', response=animess)
    else:
        return render_template('search.html')

    
if __name__ == "__main__":
    app.run(debug=True)

anime1 = Anime(title='Howl\'s moving castle', director='Hayao miyazaki', rating=999999.0)
Session.add(anime1)
Session.commit()

anime2 = Anime(title='My neighbor Totoro', director='Hayao miyazaki', rating=999999.9)
Session.add(anime2)
Session.commit()

result = Session.query(Anime).all()
for row in result:
    print(row)
