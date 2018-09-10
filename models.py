import sqlite3 as sql
import datetime
import coordinates
import distance


def insertUser(name, username, password, address, email, phone):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (name, username, password, address, email, phone) VALUES (?, ?, ?, ?, ?, ?)", (name, username, password, address, email, phone))
    con.commit()
    con.close()
#==============================================================================================================================

def checkUsers(username, password):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password, user_id FROM users")
    users = cur.fetchall()
    con.close()
    for row in users:
        if username == row[0] and password == row[1]:
            return row[2]
    return False
#==============================================================================================================================

def verifyUser(input_username):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM users WHERE username = ?", (input_username,))
    matches = cur.fetchall()[0][0]
    con.close()
    if matches > 0:
        return False
    return True
#==============================================================================================================================

def verifyEmail(input_email):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("SELECT count(*) FROM users WHERE email = ?", (input_email,))
    matches = cur.fetchall()[0][0]
    con.close()
    if matches > 0:
        return False
    return True
#==============================================================================================================================

def getPosts(user_id):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("SELECT user_id_B FROM followers WHERE user_id_A = ?", (user_id,))
    follow_list = cur.fetchall()
    posts = []
    for row in follow_list:
        idB = row[0]
        cur.execute("SELECT username, post_time, post_content, img, description, title FROM blogPosts WHERE user_id = ?", (idB,))
        x = cur.fetchall()
        if x == []:
            continue
        x = x[len(x)-1]
        x = {'username' : x[0], 'post_time' : x[1], 'content' : x[2], 'image' : x[3], 'desc' : x[4], 'title' : x[5]}
        posts.append(x)
    con.close()
    posts = [posts]
    return posts
#==============================================================================================================================

def getUserPost(user_id):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    cur.execute("SELECT post_time, post_content, description, img, title FROM blogPosts WHERE user_id=?",(user_id,))
    x = cur.fetchall()
    ret = []
    for item in x:
	    ret.append({ 'post_time' : item[0], 'content' : item[1], 'desc' : item[2], 'img' : item[3], 'title' : item[4] })
    con.close
    return ret
#==============================================================================================================================

def addPost(title, content, username, user_id, img, desc):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    now = datetime.datetime.now()
    day = now.strftime("%Y-%m-%d %H:%M")

    cur.execute("INSERT INTO blogPosts (title, post_content, post_time, username, img, description, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (title, content, day, username, img, desc, user_id))
    con.commit()
    con.close()
    return
#==============================================================================================================================

def addToWishlist(userId, bookName):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    bookId = getBookid(bookName)

    cur.execute("SELECT count(*) FROM wishlist WHERE user_id = (?) and book_id = (?)", (userId, bookId,))
    x = cur.fetchall()[0][0]

    if x == 0:
        cur.execute("INSERT INTO wishlist (user_id, book_id) VALUES (?, ?)", (userId, bookId))
        con.commit()
        con.close()
        return 'Done!'

    con.close()
    return 'The book already exists in the database.'
#==============================================================================================================================

def deleteFromWishlist(userId, bookName):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    bookId = getBookid(bookName)

    cur.execute("SELECT count(*) FROM wishlist WHERE user_id = (?) and book_id = (?)", (userId, bookId,))
    x = cur.fetchall()[0][0]

    if x == 0:
        con.close()
        return 'The book does not exist in the database.'

    cur.execute("DELETE FROM wishlist WHERE user_id = ? AND book_id = ?", (userId, bookId))
    con.commit()
    con.close()
    return 'Done!'
#==============================================================================================================================

def getWishlist(userId): # returns a list of books
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT book_id FROM wishlist WHERE user_id = (?)", (userId,))
    x = cur.fetchall()
    books = []

    for row in x:
        cur.execute("SELECT book_name FROM bookList WHERE book_id = (?)", (row[0],))
        z = cur.fetchall()[0][0]
        books.append(z)
    con.close()
    return books
#==============================================================================================================================

def addToBooklist(userId, bookName):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    bookId = getBookid(bookName)

    cur.execute("SELECT count(*) FROM userBookList WHERE user_id = (?) and book_id = (?)", (userId, bookId,))
    x = cur.fetchall()[0][0]

    if x == 0:
        cur.execute("INSERT INTO userBookList (user_id, book_id) VALUES (?, ?)", (userId, bookId))
        con.commit()
        con.close()
        return 'Done!'

    con.close()
    return 'The book already exists in the database.'
#==============================================================================================================================

def deleteFromBooklist(userId, bookName):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    bookId = getBookid(bookName)

    cur.execute("SELECT count(*) FROM userBookList WHERE user_id = (?) and book_id = (?)", (userId, bookId,))
    x = cur.fetchall()[0][0]

    if x == 0:
        con.close()
        return 'The book does not exist in the database.'

    cur.execute("DELETE FROM userBookList WHERE user_id = ? AND book_id = ?", (userId, bookId,))
    con.commit()
    con.close()
    return 'Done!'
#==============================================================================================================================

def getBooklist(userId): # returns a list of books
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT book_id FROM userBookList WHERE user_id = (?)", (userId,))
    x = cur.fetchall()
    books = []

    for row in x:
        cur.execute("SELECT book_name FROM bookList WHERE book_id = (?)", (row[0],))
        z = cur.fetchall()[0][0]
        books.append(z)
    con.close()
    return books
#==============================================================================================================================

def follow(a, b):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("INSERT INTO followers (user_id_A, user_id_B) VALUES (?, ?)", (a, b,))
    con.commit()
    con.close()
#==============================================================================================================================

def unFollow(a, b):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("DELETE FROM followers WHERE user_id_A = ? AND user_id_B = ?", (a, b,))
    con.commit()
    con.close()
#==============================================================================================================================

def getFollowing(userId):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT user_id_B FROM followers WHERE user_id_A = ?", (userId,))
    follow_list = cur.fetchall()
    following = []
    for row in follow_list:
        if row[0] != 'User Not Found':
            following.append(getUsername(row[0]))
    con.close()
    return following
#==============================================================================================================================

def getFollowers(userId):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT user_id_A FROM followers WHERE user_id_B = ?", (userId,))
    follow_list = cur.fetchall()
    following = []
    for row in follow_list:
        following.append(getUsername(row[0]))
    con.close()
    return following
#==============================================================================================================================

def getUserid(username):
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        userId = cur.fetchall()[0][0]
        con.close()
        return userId
    except:
        return 'User Not Found'
#==============================================================================================================================

def getBookid(bookName):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT book_id FROM bookList WHERE book_name = ?", (bookName,))
    bookId = cur.fetchall()
    if bookId == []:
        cur.execute("INSERT INTO bookList (book_name) VALUES (?)", (bookName,))
        con.commit()
        cur.execute("SELECT book_id FROM bookList WHERE book_name = ?", (bookName,))
        bookId = cur.fetchall()
    bookId = bookId[0][0]
    con.close()

    return bookId
#==============================================================================================================================

def getUsername(userId):
    con = sql.connect("templates/database.db")
    cur = con.cursor()

    cur.execute("SELECT username FROM users WHERE user_id = ?", (userId,))
    x = cur.fetchall()[0][0]
    con.close()
    return x
#==============================================================================================================================

# basic template for searchusers
def searchUsers(bookName, userId):
    pass
    con = sql.connect("templates/database.db")
    cur = con.cursor()
    bookId = getBookid(bookName)

    userAddress = cur.execute("SELECT address FROM users WHERE user_id = ? ", (userId,)).fetchall()[0][0]
    userCoordinates = coordinates.getCoordinates(userAddress)
    userCoordinates = ','.join(str(x) for x in userCoordinates)

    cur.execute("SELECT user_id FROM userBookList WHERE book_id=? ", (bookId,))
    userIdList = cur.fetchall()
    if userIdList == []:
        return 'Sorry! No one around you seems to have this book :('
    coordinateList = []
    nameList = []
    emailList = []
    addressList = []
    phoneList = []

    for id in userIdList:
        id = id[0]
        cur.execute("SELECT name, email, address, phone FROM users WHERE user_id = ? ", (id,))
        x = cur.fetchall()[0]
        nameList.append(x[0])
        emailList.append(x[1])
        addressList.append(x[2])
        phoneList.append(x[3])
        coordinate = coordinates.getCoordinates(x[2])
        if coordinate[1] != 'error':
            coordinate = ','.join(str(x) for x in coordinate)
            coordinateList.append(coordinate)
        else:
            coordinateList.append('error')

    coordinateList = '|'.join(coordinateList)
    distanceList = distance.getDistance(userCoordinates, coordinateList)
    ret = []
    i = 0

    for item in distanceList:
        ret.append({'distance' : item['dist'], 'tim' : item['tim'], 'name' : nameList[i], 'email' : emailList[i], 'phone' : phoneList[i], 'address' : addressList[i]})
        i += 1
        ret = sorted(ret, key=lambda k: k['distance'])
    return ret
#==============================================================================================================================

if __name__ == '__main__':
    searchUsers('sapiens', '1')
