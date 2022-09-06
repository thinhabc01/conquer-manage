from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import os
import re
import click
import requests


app = Flask(__name__) 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
url = os.environ.get('LINK_NOTEPAD')

def read_data(url):
    headers = {}
    payload={}
    response = requests.request("GET", url, headers=headers, data=payload)

    txt = response.text
    start = txt.find('<textarea id="content" spellcheck="false" style="font-family:Arial, Helvetica, sans-serif;">')
    end = txt.find('</textarea>')
    if end > start:
        return txt[start+92: end]
    else:
        return None

def write_data(url, text):
    headers = {}

    payload={"text":text}
    response = requests.request("POST", url, headers=headers, data=payload) 
    return response.text


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
                pass

                return "success"
        except Exception as e:
            return "error: "+ e

#===============================get account=====================================
@app.route('/get-account')  
def chat():
    columns = ['name', 'password', 'group', 'server', 'lv1', 'gold', 'lv2', 'lv3']
    try:
        socks = Account.query.filter_by(lv2='15').order_by(Account.id).all()
        sock_text = '<pre>'
        for sock in socks:
            sock_text += sock.name + '|'
            sock_text += sock.password + '|'
            sock_text += sock.group + '|'
            sock_text += sock.server + '|'
            sock_text += sock.lv1 + '|'
            sock_text += sock.gold + '|'
            sock_text += sock.lv2 + '|'
            sock_text += sock.lv3 + '\n'
        sock_text += '</pre>'
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
