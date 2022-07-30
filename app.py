from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import os
import click


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    group = db.Column(db.Integer)
    server = db.Column(db.Integer)
    lv1 = db.Column(db.Integer)
    gold = db.Column(db.Integer)
    lv2 = db.Column(db.Integer)
    lv3 = db.Column(db.String(100))

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
    d = {column: search for column in columns}
    raw = [
        Account.query.filter(getattr(Account, col).ilike(f"{val}%")).all()
        for col, val in d.items()
    ]
    # [item for item in raw if item]
    return ''.join(raw)
    # return render_template("log.html", content=content)
#========================================================================
app.cli.add_command(create_table)


if __name__ == '__main__':
    app.run()
