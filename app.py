from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
# from pathlib import Path

# Init app
app = Flask(__name__)

# ENV = "dev"
ENV = "prod"

if ENV == "dev":
    # Development Mode
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/pgcb"
else:
    # Production Mode
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "heroku_postgres_uri"
    
# TO DO Comment
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
 
class Pgcb_Db(db.Model):
    __tablename__ = "feedback"
    uid = db.Column(db.Integer, primary_key = True)
    # id = db.column(db.Integer)
    customer = db.Column(db.String(200))
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Run server
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods = ["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        # print(customer, dealer, rating, comments)
        if customer == "" or dealer == "":
            return render_template("index.html", message = "Please enter required fields.")
        if db.session.query(Pgcb_Db).filter(Pgcb_Db.customer == customer).count() == 0:
            data = Pgcb_Db(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            return render_template("success.html")
        return render_template("index.html", message = "You have already submitted feedback")

# Run server
if __name__ == "__main__":
    app.debug = True
    app.run()