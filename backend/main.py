from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy
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


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    srfid = db.column(db.String(20),unique_key=True)
    email = db.Column(db.String(20))
    dob = db.Column(db.String(20))

# Adding route
    
@app.route('/signup',methods = ['POST','GET'])
def signup ():
    if request.method=="POST":



@app.route("/")
def home(): 
   return render_template("index.html") 



@app.route('/signup', methods=['POST', 'GET'])
def signup(request):
    if request.method=="POST":
        srfid = request.form.get('srfid')
        email = request.form.get('email')
        dob = request.form.get('dob')
        #print(srfid,email,dob)
        encpassword= generate_password_hash(dob) #encrypting password
        new_user = db.engine.execute(f"INSERT INTO 'user' ('srfid', 'email', 'dob') VALUES ('{srfid}', '{email}', '{encpassword}') " )
        return ' USER ADDED'

    return render_template("usersignup.html")


@app.route('/login', methods=['POST', 'GET'])
def login(request):
    if request.method=="POST":
        srfid = request.form.get('srfid')
        dob = request.form.get('dob')
        user = User.query.filter_by(srfid = srfid).first 
        #filtering email address

        if user and check_password_hash(user.dob,dob):
            login_user(user)
            return 'Login success'
        else:
            return 'Login fail'

    return render_template("userlogin.html")

    
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
