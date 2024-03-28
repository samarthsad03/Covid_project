from flask import Flask,redirect,render_template
from flask_sqlalchemy import SQLAlchemy


#my database connection
local_server=True
app = Flask(__name__)
app.secret_key = "samarthsadana"

app.config['SQLAICHEMY_DATABASE_URI'] ='mysql://username:password@localhost/databasename'

@app.route('/')
def home():
    return render_template("index.html") 
#here 2 dots means to go backwards to backend directory


app.run(debug=True)
