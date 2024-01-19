

# import the Flask library
from flask import Flask, render_template, request,redirect,url_for,jsonify
import json
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['dburl']

db.init_app(app)

class dim_user(db.Model):
    userid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)

@app.route('/', methods=['GET','POST'])
def homepage():

    if request.method == 'GET':
        if request.args.get('btnnum') != None:
            return redirect(url_for("homepage"))
        else:
            return render_template("homepage.html")
    else:
        if request.form['num'] != '' and request.form['num2'] != '' and request.form['btnnum2'] != '':
            user = dim_user(
                name=request.form["num"],
                username=request.form["num2"],
                password=request.form["num3"]
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_detail", id=user.userid))
        else:
            return render_template("homepage.html")  
 


@app.route('/api1', methods=['GET'])
def  get_current_json():

    if request.method == 'GET':
        r = db.session.execute(db.select(User.id,User.email))
        temp = []
        for row in r:
            temp.append({'id':row[0],'email':row[1]})
        return jsonify(temp)

@app.route('/login', methods=['GET'])
def  login():

    if request.method == 'GET':
        r = db.session.execute(db.select(User.id,User.email))
        temp = []
        for row in r:
            temp.append({'id':row[0],'email':row[1]})
        return jsonify(temp)
    

# @app.route('/register', methods=['GET','POST'])
# def  insert_data():
#     # If method is GET, check if  number is entered
#     # or user has just requested the page.
#     # Calculate the square of number and pass it to
#     # answermaths method
#     if request.method == "POST":
#         if request.form['num'] != '' and request.form['num2'] != '' and request.form['btnnum2'] != '':
#             user = User(
#                 id=request.form["num"],
#                 email=request.form["num2"],
#             )
#             db.session.add(user)
#             db.session.commit()
#             return redirect(url_for("user_detail", id=user.id))
#         else:
#             return render_template("squarenum.html")
        
#     else:    
#         return render_template("squarenum.html")

@app.route("/user/<int:id>")
def user_detail(id):
    return render_template("user/detail.html")

if(__name__ == "__main__"):
    app.run(debug=True)