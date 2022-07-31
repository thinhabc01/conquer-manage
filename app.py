from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import os
import re
import click


app = Flask(__name__)

uri = os.environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
    
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    password = db.Column(db.String(200))
    group = db.Column(db.String(50))
    server = db.Column(db.String(50))
    lv1 = db.Column(db.String(50))
    gold = db.Column(db.String(50))
    lv2 = db.Column(db.String(50))
    lv3 = db.Column(db.String(50))

    def __init__(self, name, password, group, server, lv1, gold, lv2, lv3):
        self.name = name
        self.password = password
        self.group = group
        self.server = server
        self.lv1 = lv1
        self.gold = gold
        self.lv2 = lv2
        self.lv3 = lv3


#=================================create table=============================
@click.command(name='create_table')
@with_appcontext
def create_table():
    db.create_all()

#================================home page=================================
@app.route('/')
def homepage():
    return """
        <h1>Server OK</h1
        """
#========================upload account=====================================
 
@app.route('/upload', methods = ['POST'])  
def success():
    if request.method == 'POST':
        try:
            account = request.form.get('account')
            a = account.split("|")
            if len(a) == 8:
                data = Account(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7])
                db.session.add(data)
                db.session.commit()

                return "success"
        except Exception as e:
            return "error: "+ e

#===============================get account=====================================
@app.route('/get-account')  
def chat():
    columns = ['name', 'password', 'group', 'server', 'lv1', 'gold', 'lv2', 'lv3']
    try:
        socks = Account.query.filter_by(lv2='15').order_by(Account.id).all()
        sock_text = '<ul>'
        for sock in socks:
            sock_text += '<li>'
            sock_text += sock.name + '|'
            sock_text += sock.password + '|'
            sock_text += sock.group + '|'
            sock_text += sock.server + '|'
            sock_text += sock.lv1 + '|'
            sock_text += sock.gold + '|'
            sock_text += sock.lv2 + '|'
            sock_text += sock.lv3
            sock_text += '</li>'
        sock_text += '</ul>'
        return sock_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    # return render_template("log.html", content=content)
#========================================================================
app.cli.add_command(create_table)


if __name__ == '__main__':
    app.run()
