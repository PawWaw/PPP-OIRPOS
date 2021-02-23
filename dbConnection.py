import pyodbc
import hashlib, uuid

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=blackblood-pc;'
                      'Database=PPP;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def hashing(pswd):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha512(str(pswd).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()
    return hashed, salt

def register(username, password, mail):
    hashed, salt = hashing(password)
    cursor.execute("SELECT username FROM PPP.dbo.Users WHERE username='"+username+"'")
    if cursor.fetchone() != None:
        print("User with that login already exists!")
        return -1
    else:
        cursor.execute("INSERT INTO PPP.dbo.Users(username, password, salt, email) values ('"+username+"','"+hashed+"','"+salt+"','"+mail+"')")
        conn.commit()

def login(username, password):
    cursor.execute("SELECT salt FROM PPP.dbo.Users WHERE username='"+username+"'")
    salt = cursor.fetchone()
    if salt is not None:
        hashed = hashlib.sha512(str(password).encode('utf-8') + str(salt[0]).encode('utf-8')).hexdigest()
        cursor.execute("SELECT * FROM PPP.dbo.Users WHERE username='"+username+"' AND password='"+hashed+"'")
        logCheck = cursor.fetchone()
        if logCheck != None:
            print(logCheck[0])
            return logCheck[0]
        else:
            print("Wrong login or password!")
            logCheck = -1
            return logCheck
    return -1

def addPost(userId, message, file):
    cursor.execute("INSERT INTO PPP.dbo.Messages(userId, message, [file]) VALUES('"+str(userId)+"','"+message+"','"+file+"')")
    conn.commit()

def getUserPosts(userId):
    cursor.execute("Select * FROM PPP.dbo.Messages WHERE userId='"+str(userId)+"'")
    posts = cursor.fetchall()    
    username = getUserName(userId)
    return posts, username

def addArticle(userId, topic, article, file):
    cursor.execute("INSERT INTO PPP.dbo.Articles(userId, topic, informations, [file]) VALUES('"+str(userId)+"','"+topic+"', '"+article+"','"+file+"')")
    conn.commit()

def getArticleTopics():
    cursor.execute("Select id, userId, topic FROM PPP.dbo.Articles")
    articles = cursor.fetchall()
    return articles

def getArticle(id):
    cursor.execute("Select * FROM PPP.dbo.Articles WHERE id='"+str(id)+"'")
    article = cursor.fetchone()
    username = getUserName(article.userId)
    return article, username

def getPost(id):
    cursor.execute("Select * FROM PPP.dbo.Messages WHERE id='"+str(id)+"'")
    post = cursor.fetchone()
    username = None
    if post != None:
        username = getUserName(post.userId)
    return post, username

def getUserName(userId):
    cursor.execute("Select username FROM PPP.dbo.Users WHERE id='"+str(userId)+"'")
    username = cursor.fetchone()
    return username[0]
# register("testowy", "tester", "tester@test.com")
#userId = login("testowy", "tester")
# addPost(userId, 'Testowa wiadomość aplikacji, Lorem Ipsum', 'C:/Users/pawel/Desktop/border.jpg')
#getUserPosts(userId)
# addArticle(userId, 'Border Collie 2', 'Testowy artykuł dotyczący pieska 2!', 'C:/Users/pawel/Desktop/border.jpg')
# getArticleTopics()
# getArticle(1)

