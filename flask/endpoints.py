import io
import base64
from flask_session import Session
from flask import render_template, request, redirect, url_for, flash, session, Response, abort
from flask import Flask
from werkzeug.utils import secure_filename
from matplotlib import pyplot as plt
import os
import sys
# Użycie parentdir
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir) 
import dbConnection
from scriptRunner import runScripts
from UIMethods import getDataForGraph, getDataForText
# Dołączanie modułu flask
# Tworzenie aplikacji - w tym momencie rootem jest ścieżka Dogopedia więc trzeba zrobić flask/templates
app = Flask("Dogopedia", template_folder='flask/templates', static_folder="flask/static")
sess = Session()

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def rawPngToBase64(binaryFile):
    return "data:image/png;base64," + base64.b64encode(binaryFile).decode('utf8')

def Base64ToRawPNG(pngImage):
    return base64.decodebytes(pngImage.split('base64,')[1].encode('utf8'))

#404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', img="/static/404-najman.jpg"), 404   
# Widok główny
@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        # Pobranie danych z tabeli
        articles = dbConnection.getArticleTopics()
        username = dbConnection.getUserName(session['user'])
        return render_template('index.html', articles=articles, user=username)
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
        userLogin = request.form['login']
        password = request.form['password']
        if userLogin == '' or password == '':
            return "<p class='error'>Nazwa użytkownika i hasło muszą być wypełnione</p>" + render_template('login.html')
        id = dbConnection.login(userLogin, password)
        if id != -1:
            # Poprawny użytkownik
            session['user'] = id
            flash("Zostałeś pomyślnie zalogowany!")
        else:
            flash("Wpisałeś złe hasło lub nazwę użytkownika")
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
        if dbConnection.register(userLogin, password, email) != -1:
            return "Dodano użytkownika<br>" + render_template('login.html')
        else:
            return render_template('registration.html')

# dodanie posta użytkownika
@app.route('/post', methods=['POST'])
def post():
    if 'user' in session:
        content = request.form['content']
        image = None
        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                image = image.read()
                preImg = io.BytesIO(image)
                img = rawPngToBase64(preImg.getvalue())
        dbConnection.addPost(session['user'], content, img)
        flash("Dodano posta z sukcesem!")
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
            if image and allowed_file(image.filename):
                image = request.files['image'].read()
                preImg = io.BytesIO(image)
                img = rawPngToBase64(preImg.getvalue())
        dbConnection.addArticle(session['user'], title, content, img)
        return index()
    else:
        return "Co ty tutaj robisz?"

#wszystkie posty użytkownika
@app.route('/posts', methods=['GET'])
def userPosts():
    if 'user' in session:
        # Pobranie danych z tabeli
        posts, username = dbConnection.getUserPosts(session['user'])
        return render_template('posts.html', posts=posts, userName=username)
    else:
        # Nie ma użytkownika w sesji
        return redirect(url_for('login'))

#Konkretny post
@app.route('/post/<int:post_id>', methods=['GET'])
def aPost(post_id):
    if 'user' in session:
        # Pobranie danych z tabeli
        post, username = dbConnection.getPost(post_id)
        if post == None:
            abort(404)
        return render_template('post.html', post=post, userName=username)
    else:
        # Nie ma użytkownika w sesji
        return redirect(url_for('login'))

#wszystkie artykuły użytkownika
@app.route('/articles', methods=['GET'])
def allArticles():
    articleTopics = dbConnection.getArticleTopics()
    return render_template('articles.html', articles=articleTopics)

#Konkretny artykuł
@app.route('/article/<int:article_id>', methods=['GET'])
def getArticle(article_id):
    article,username = dbConnection.getArticle(article_id)
    return render_template('article.html', article = article, author = username)

#obrazek dla artykułu
@app.route('/img/article/<int:article_id>', methods=['GET'])
def imgArticle(article_id):
    article, username= dbConnection.getArticle(article_id)
    if article == None:
        abort(404)
    binaryImg = article.file
    return Response(Base64ToRawPNG(binaryImg), mimetype='image/png')

#obrazek dla posta
@app.route('/img/post/<int:post_id>', methods=['GET'])
def imgPost(post_id):
    if 'user' in session:
        post, username= dbConnection.getPost(post_id)
        if post == None:
            abort(404)
        binaryImg = post.file
        return Response(Base64ToRawPNG(binaryImg), mimetype='image/png')
    else:
        abort(404)

#Obrazek wygenerowany przez sieć
@app.route('/guess', methods=['GET','POST'])
def guesserr():
    if 'user' in session:
        if request.method == 'POST':
            image = None
            if 'image' in request.files:
                image = request.files['image']
                if image and allowed_file(image.filename):
                    image = request.files['image']
                    diractory = os.path.join(app.static_folder, secure_filename(image.filename))
                    image.save(diractory)
                    tab = runScripts(diractory)
                    os.remove(diractory)
                    networkInfo = getDataForGraph(tab)
                    title = getDataForText(tab)
                    fig = plt.figure(figsize=(16, 9))
                    plt.bar(networkInfo[0],networkInfo[1], color='orange', align='center')
                    plt.title(title)
                    img = io.BytesIO()
                    fig.savefig(img,bbox_inches='tight',dpi=100, aspect='auto')
                    return Response(img.getvalue(), mimetype='image/png')
            return render_template('guess.html', error=True)
        else:
            return render_template('guess.html', error=False)
    else:
        abort(404)
# wylogowanie
@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash("Zostałeś pomyślnie wylogowany!")
    return redirect(url_for('login'))

# Uruchomienie applikacji w trybie debug
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)
app.config.from_object(__name__)
app.run(debug=True)
