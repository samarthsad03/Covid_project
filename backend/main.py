from flask import Flask,redirect,render_template,request,flash, url_for
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_login import UserMixin
from flask_login import login_required, login_user,logout_user,login_manager,current_user,LoginManager
from werkzeug.security import generate_password_hash, check_password_hash



#my database connection
local_server=True
app = Flask(__name__)
app.secret_key = "samarthsadana"


#this is for getting the unique user access 
login_manager = LoginManager(app)
login_manager.login_view='login'

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/Covid'
db=SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#This will return user id so that i can keep record of every user


#creating a module
class Test(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.column(db.String(50))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    srfid = db.Column(db.String(20),unique_key=True)
    email = db.Column(db.String(50))
    dob = db.Column(db.String(1000))

# Adding routes
    
@app.route("/")
def home(): 
   return render_template("index.html") 



@app.route('/signup', methods=['POST', 'GET'])
def signup():
    #taking the input data
    if request.method=="POST":
        srfid = request.form.get('srfid')
        email = request.form.get('email')
        dob = request.form.get('dob')
        encpassword= generate_password_hash(dob) #encrypting password
        user = User.query.filter_by(srfid=srfid).first()
        emailUser = User.query.filter_by(email=email).first()
        #putting into the database
        if user or emailUser:
            flash("Email or srfid is already taken", " warning")
            return render_template("usersignup.html")

        with db.engine.connect() as conn:
            query = text(f"INSERT INTO user (srfid, email, dob) VALUES('{srfid}', '{email}', '{encpassword}')")
            new_user =  conn.execute(query)
            conn.commit()
        # new_user = db.engine.execute(f"INSERT INTO 'user' ('srfid', 'email', 'dob') VALUES ('{srfid}', '{email}', '{encpassword}') " )
        user1 = User.query.filter_by(srfid = srfid).first()
        #giving the login access from here
        flash("Signup Success Please Login", "success")
        return render_template("userlogin.html")

    return render_template("usersignup.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=="POST":
        srfid = request.form.get('srfid')
        dob = request.form.get('dob')
        print("[LOGIN]: Logging in with- ", srfid, " ", dob)
        user = User.query.filter_by(srfid = srfid).first()
        #filtering email address

        if user and check_password_hash(user.dob,dob):
            print("[LOGIN]: password validated")

            login_user(user)
            flash(" Login success" , "info")
            return render_template("index.html")
        else:
            print("[LOGIN]: password validatedn't")

            flash("Invalid Credentials","danger") #danger is the colour
            return render_template("userlogin.html") #redirect to this template
    elif request.method =="GET":
        print("[LOGIN]: serving login page")
        return render_template("userlogin.html")
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful", "warning")
    return redirect(url_for('login'))

    
#checking whether database is connected or not
@app.route("/test")
def test():
    try:
        a = Test.query.all()
        print(a)
        return 'my database is connected'
    except Exception as e:
        print(e)
        return f'not connected{e}'
    
    

app.run(debug=True)
