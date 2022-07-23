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
	b_lines = [row for row in reversed(list(open("account.txt")))]
	return render_template('log.html', b_lines=b_lines)
#========================================================================

if __name__ == '__main__':
	app.run(debug=True, use_reloader=True)

