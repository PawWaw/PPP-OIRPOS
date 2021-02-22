from flask_session import Session
from flask import render_template, request, redirect, url_for, flash, session
from flask import Flask
import os
import sys
# Użycie parentdir
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import dbConnection
# Dołączanie modułu flask
# Tworzenie aplikacji - w tym momencie rootem jest ścieżka Dogopedia więc trzeba zrobić flask/templates
app = Flask("Dogopedia", template_folder='flask/templates')
sess = Session()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Widok główny
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        # Pobranie danych z tabeli
        posts,username = dbConnection.getUserPosts(session['user'])
        return render_template('index.html', posts=posts, user=username)
    else:
        # Nie ma użytkownika w sesji
        return redirect(url_for('login'))

# widok logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('index'))
        else:
            articles = dbConnection.getArticleTopics()
            return render_template('login.html', articles=articles)
    else:
        login = request.form['login']
        password = request.form['password']
        id = dbConnection.login(login, password)
        if id != -1:
            # Poprawny użytkownik
            session['user'] = id
        return redirect(url_for('index'))

# dodanie użytkownika
@app.route('/user/add', methods=['GET', 'POST'])
def userAdd():
    if request.method == 'GET':
        return render_template('registration.html')
    else:
        userLogin = request.form['login']
        password = request.form['password']
        email = request.form['email']
        if userLogin == '' or password == '':
            return "<p class='error'>Nazwa użytkownika i hasło muszą być wypełnione</p>" + render_template('add.html')
        # Dodanie użytkownika do bazy danych
        dbConnection.register(userLogin, password, email)
        return "Dodano użytkownika do bazy danych <br>" + render_template('login.html')

# dodanie posta użytkownika
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        return redirect(url_for('posts'))
    else:
        if 'user' in session:
            content = request.form['content']
            image = None
            if 'image' in request.files:
                image = request.files['image']
            dbConnection.addPost(session['user'], content, image)
            return index()
        else:
            return "Co ty tutaj robisz?"

# dodanie article użytkownika
@app.route('/article', methods=['POST'])
def article():
    if 'user' in session:
        title = request.form['title']
        content = request.form['content']
        image = None
        if 'image' in request.files:
            image = request.files['image']
        dbConnection.addArticle(session['user'], title, content, image)
        return index()
    else:
        return "Co ty tutaj robisz?"

#wszystkie posty użytkownika
@app.route('/posts', methods=['GET'])
def userPosts():
    if 'user' in session:
        # Pobranie danych z tabeli
        posts,username = dbConnection.getUserPosts(session['user'])
        return render_template('posts.html', posts=posts, userName=username)
    else:
        # Nie ma użytkownika w sesji
        return redirect(url_for('login'))

#wszystkie artykuły użytkownika
@app.route('/articles', methods=['GET'])
def allArticles():
    articles = dbConnection.getArticleTopics()
    return render_template('articles.html', articles=articles)

#Konkretny artykuł
@app.route('/article/<int:get_id>', methods=['GET'])
def getPost(article_id):
    article = dbConnection.getArticle(article_id)
    return render_template('article.html', article = article)

# wylogowanie
@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('isAdmin')
    return redirect(url_for('login'))

# Uruchomienie applikacji w trybie debug
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.run(debug=True)
