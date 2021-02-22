import os, sys
#Użycie parentdir
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
# Dołączanie modułu flask 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
from flask_session import Session
import dbConnection
# Tworzenie aplikacji - w tym momencie rootem jest ścieżka Dogopedia więc trzeba zrobić flask/templates
app = Flask("Dogopedia", template_folder='flask/templates')
sess = Session()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Widok główny
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in session:        
        # Pobranie danych z tabeli
        posts = dbConnection.getUserPosts(session['user'])
        return render_template('index.html', posts = posts, user=session['user'])
    else:
        #Nie ma użytkownika w sesji
        return redirect(url_for('login'))

#widok logowanie
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('index'))
        else: 
            return render_template('login.html')
    else:
        login = request.form['login']
        password = request.form['password']
        id = login(login, password)
        if id != -1:
            #Poprawny użytkownik
            session['user'] = id
        return redirect(url_for('index'))

#dodanie użytkownika
@app.route('/user/add', methods=['GET', 'POST'])
def userAdd():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        userLogin = request.form['login']
        password = request.form['password']
        email = request.form['email']
        if userLogin == '' or password == '':
            return "<p class='error'>Nazwa użytkownika i hasło muszą być wypełnione</p>" + render_template('add.html')
        # Dodanie użytkownika do bazy danych
        dbConnection.register(userLogin, password, email)
        return "Dodano użytkownika do bazy danych <br>" + render_template('login.html')

#dodanie ksiazki
@app.route('/book/add', methods=['POST'])
def bookAdd():
    if 'user' in session:
        title = request.form['title']
        author = request.form['author']
        
        return "Dodano ksiązkę do bazy danych <br>" + index()
    else:
        return "Co ty tutaj robisz?"

#użytkownicy
@app.route('/users', methods=['GET'])
def users():
    if 'isAdmin' in session:
        if session['isAdmin'] == 1:
            
            return render_template('users.html', users=users)
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"

#jeden użytkownik
@app.route('/user/<int:get_id>',methods=['GET'])
def get_user_by_id(get_id):
        
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"
@app.route('/user/<get_name>',methods=['GET'])
def get_user_by_name(get_name):
        
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"

#wylogowanie
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
app.run(debug = True)