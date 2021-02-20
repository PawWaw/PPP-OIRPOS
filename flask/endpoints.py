# Dołączanie modułu flask 
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, session
import sqlite3
from flask_session import Session
# Tworzenie aplikacji
app = Flask("Dogopedia")
# Ścieżka do pliku bazy danych w sqlite
DATABASE = 'database.db'
sess = Session()

#Tworzenie baazy danych tylko jesli tabela nie istnieje
@app.route('/create_db', methods=['GET', 'POST'])
def create_db():
    # Połączenie sie z bazą danych
    conn = sqlite3.connect(DATABASE)
    # Stworzenie tabeli w bazie danych za pomocą sqlite3 jesli tabela nie istnieje
    conn.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, isAdmin INTEGER,ID INTEGER PRIMARY KEY AUTOINCREMENT)')
    conn.execute('CREATE TABLE IF NOT EXISTS books (author TEXT, title TEXT, ID INTEGER PRIMARY KEY AUTOINCREMENT)')
    # Zakończenie połączenia z bazą danych
    conn.close()

#Widok główny
@app.route('/', methods=['GET', 'POST'])
def index():
    # if 'user' in session:
    #     con = sqlite3.connect(DATABASE)
        
    #     # Pobranie danych z tabeli
    #     cur = con.cursor()
    #     cur.execute("select * from books ORDER BY author ASC")
    #     books = cur.fetchall()
    #     con.close()
    #     adminView = ""
    #     if 'isAdmin' in session:
    #         if session['isAdmin'] == 1:
    #             adminView = "<a href=/users>Użytkownicy</a>"
    #     return render_template('index.html', books = books, user=session['user']) + adminView
    # else:
    #     print("nie ma user w sesji")
    #     return redirect(url_for('login'))
    return "Welcome to dogopedia!"

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
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username == ? AND password == ?", [login,password])
        users = cur.fetchall()
        print(users)
        if len(users) == 1:
            print("jest uzytkownik")
            session['user'] = users[0][0]
            session['isAdmin'] = users[0][2]
        con.close()
        return redirect(url_for('index'))

#dodanie użytkownika
@app.route('/user/add', methods=['GET', 'POST'])
def userAdd():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        userLogin = request.form['login']
        password = request.form['password']
        administrator = 0
        if request.form.get('administrator'):
            administrator = 1
        # Dodanie użytkownika do bazy danych
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE username ==?",[userLogin])
        users = cur.fetchall()
        print(administrator)
        if len(users) > 0:
            con.close()
            return "Użytkonik istnieje" + render_template('add.html')
        cur.execute("INSERT INTO users (username,password, isAdmin) VALUES (?,?,?)",(userLogin,password,administrator) )
        con.commit()
        con.close()
        return "Dodano użytkownika do bazy danych <br>" + render_template('login.html')

#dodanie ksiazki
@app.route('/book/add', methods=['POST'])
def bookAdd():
    if 'user' in session:
        title = request.form['title']
        author = request.form['author']
        # Dodanie użytkownika do bazy danych
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("INSERT INTO books (title,author) VALUES (?,?)",(title,author) )
        con.commit()
        con.close()

        return "Dodano ksiązkę do bazy danych <br>" + index()
    else:
        return "Co ty tutaj robisz?"

#użytkownicy
@app.route('/users', methods=['GET'])
def users():
    if 'isAdmin' in session:
        if session['isAdmin'] == 1:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            con.close()
            return render_template('users.html', users=users)
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"

#jeden użytkownik
@app.route('/user/<int:get_id>',methods=['GET'])
def get_user_by_id(get_id):
    if 'isAdmin' in session:
        if session['isAdmin'] == 1:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?",[get_id])
            user = cur.fetchone()
            con.close()
            if user is None:
                return "Użytkownik nie został znaleziony. <br><a href='/users'>Powrót</a>"
            else:
                return render_template('user.html',user=user) 
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"
@app.route('/user/<get_name>',methods=['GET'])
def get_user_by_name(get_name):
    if 'isAdmin' in session:
        if session['isAdmin'] == 1:
            con = sqlite3.connect(DATABASE)
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username == ?",[get_name])
            user = cur.fetchone()
            con.close()
            if user is None:
                return "Użytkownik nie został znaleziony. <br><a href='/users'>Powrót</a>"
            else:
                return render_template('user.html',user=user)   
    return "Co ty tutaj robisz? <br> <a href=/>Powrót</a>"

#wylogowanie
@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        session.pop('isAdmin')
    return redirect(url_for('login'))

#Przygotowanie bazy danych jeśli ona nie istnieje (włącznie ze sprawdzeniem tabel)
create_db()
# Uruchomienie applikacji w trybie debug
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.run(debug = True)