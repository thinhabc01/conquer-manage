from flask import *

import os
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
                sAccount = read_data(url)
                tAccount = sAccount+account+"\n"
                write_data(url, tAccount)
                return "success"
        except Exception as e:
            return "error: "+ e

#===============================get account=====================================
@app.route('/get-account')  
def get_account():
    sAccount = read_data(url)
    txt = '<pre>'+sAccount+'</pre>'
    return txt
#===============================================================================

if __name__ == '__main__':
    app.run()
