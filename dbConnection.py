import pyodbc
import hashlib, uuid

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-3DIB104;'
                      'Database=PPP;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

def hashing(pswd):
    salt = uuid.uuid4().hex
    hashed = hashlib.sha512(str(pswd).encode('utf-8') + str(salt).encode('utf-8')).hexdigest()
    return hashed, salt

def register(username, password, mail):
    hashed, salt = hashing(password)
    cursor.execute("INSERT INTO PPP.dbo.Users(username, password, salt, email) values ('"+username+"','"+hashed+"','"+salt+"','"+mail+"')")
    conn.commit()

def login(username, password):
    cursor.execute("SELECT salt FROM PPP.dbo.Users WHERE username='"+username+"'")
    salt = cursor.fetchone()
    hashed = hashlib.sha512(str(password).encode('utf-8') + str(salt[0]).encode('utf-8')).hexdigest()
    cursor.execute("SELECT * FROM PPP.dbo.Users WHERE username='"+username+"' AND password='"+hashed+"'")
    logCheck = cursor.fetchone()
    if logCheck != None:
        print(logCheck[0])
    else:
        print("Wrong login or password!")
        logCheck = -1

# register("testowy", "tester", "tester@test.com")
# login("testowy", "tester")
