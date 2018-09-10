from flask import request, Flask, render_template, flash, redirect, url_for, session
import models as dbHandler
import hashlib
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)
app.secret_key = 'some_secret'

# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
# configure_uploads(app, photos)

#===========================================================================================
@app.route('/',methods=['GET', 'POST'])
def hey():
    if  session.get('logged_in'):
        # if session['posts']:
        render_template('home.html',posts=session['posts'])
        # else:
            # render_template('home.html',posts=None)
    return render_template('index.html')
#===========================================================================================

@app.route('/home',methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "POST":
        book_name = request.form['search']
        return redirect(book_name)
    # if session['posts']:
    posts = dbHandler.getPosts(session['userid'])
    session['posts'] = posts
    print (session['posts'])
    return render_template('home.html', posts=session['posts'])
    # else:
        # return render_template('home.html',posts=None)
#===========================================================================================

@app.route('/<book_name>',methods=['GET','POST'])
def search(book_name):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == "POST":
        book_name = request.form['search']
        return redirect(book_name)

    userid = session['userid']
    details = dbHandler.searchUsers(book_name,userid)
    return render_template("booksearch.html",details=details,book=book_name)
#===========================================================================================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    userid = session['userid']
    if request.method == 'POST':

        Name = request.form['Name']

        if request.form['butt'] == 'addWishlist':
            dbHandler.addToWishlist(userid, Name)

        elif request.form['butt'] == 'deleteWishlist':
            dbHandler.deleteFromWishlist(userid, Name)

        elif request.form['butt'] == 'addBook':
            dbHandler.addToBooklist(userid, Name)

        elif request.form['butt'] == 'deleteBook':
            dbHandler.deleteFromBooklist(userid, Name)

        elif request.form['butt'] == 'addPeople':
            id2 = dbHandler.getUserid(Name)
            if id2 !='User Not Found':
                dbHandler.follow(userid, id2)
            else:
                flash(id2)

        elif request.form['butt'] == 'deletePeople':
            id2 = dbHandler.getUserid(Name)
            dbHandler.unFollow(userid, id2)

    wish_list = dbHandler.getWishlist(userid)
    book_list = dbHandler.getBooklist(userid)
    followers = dbHandler.getFollowers(userid)
    following = dbHandler.getFollowing(userid)

    return render_template('profile.html',books=book_list,wish=wish_list, followers=followers, following=following)
#===================================================================================================================

@app.route('/login',methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = hashlib.sha256(str.encode(password)).hexdigest()
        check = dbHandler.checkUsers(username, password)
        if type(check) == int:
            flash(username)
            session['logged_in'] = True
            session['user'] = username
            session['userid'] = check
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password. Please try again.'

    return render_template('login.html', error=error)
#=================================================================================================================

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify_pass = request.form['verify_pass']
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phoneNum']

        val = verify_signup(name, username, password, address, email, verify_pass, phone)
        if val == True:
            flash(name)
            session['posts'] = [{}]
            session['logged_in'] = True
            session['user'] = username
            session['userid'] = dbHandler.getUserid(username)
            return redirect('home')
        else:
            error = val
    return render_template('signup.html', error = error)
#=============================================================================================================

def verify_signup(name, username, password, address, email, verify_pass, phone):
    password = hashlib.sha256(str.encode(password)).hexdigest()
    verify_pass = hashlib.sha256(str.encode(verify_pass)).hexdigest()

    usernameValidated = dbHandler.verifyUser(username)
    emailValidated = dbHandler.verifyEmail(email)

    if password != verify_pass:
        val = 'Passwords don\'t match'
    elif emailValidated == False:
        val = 'This email ID is already registered. Please click on login to go to the login page.'
    elif usernameValidated == False:
        val = 'This username is already taken. Please use a diffrent one.'
    else:
        dbHandler.insertUser(name, username, password, address, email, phone)
        val = True
    return val
#=================================================================================================

@app.route('/index',methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        arg = request.form['myarg']
        if arg == 'login':
            return render_template('login.html', error=error)
        return render_template('signup.html', error=error)
    return render_template('index.html', error=error)
#=================================================================================================

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['posts'] = None
    session['user'] = None
    session['userid'] = None
    return redirect(url_for('index'))
#=================================================================================================

@app.route('/blog', methods=['GET', 'POST'])
def Myblog():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    username = session['user']
    userid = session['userid']

    if request.method == 'POST':
        title = request.form['title']
        entry = request.form['blog']
        desc = request.form['desc']
        img = photos.save(request.files['image'])
        dbHandler.addPost(title, entry, username, userid, img, desc)

    blogs = dbHandler.getUserPost(userid)
    return render_template('blog.html',blogs=blogs)
#================================================================================================

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0',  ssl_context=('cert.pem', 'key.pem'))
