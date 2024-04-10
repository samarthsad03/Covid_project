from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy


#my database connection
local_server=True
app = Flask(__name__)
app.secret_key = "samarthsadana"

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/Covid'
db=SQLAlchemy(app)


#creating a module
class Test(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.column(db.String(50))

# Adding route
@app.route("/")
def home(): 
   return render_template("index.html") 


@app.route("/usersignup")
def userSignup():
    return render_template("usersignup.html")

@app.route("/userlogin")
def userlogin():
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
