from flask import Flask
app = Flask('CodeChallenge')

@app.route('/')
def home():
        return 'Welcome to the Capsher Code Challenge!'

@app.route('/challenge/<name>', methods=['GET', 'POST'])
def show_challenge(name):
	if request.method == 'POST':
		return 'Submited challenge %s' % name
	else:
		return 'Enter your email and select an upload file to submit \
			the %s challege' % name


if __name__ == '__main__':
	app.debug = True
        app.run(host='0.0.0.0')

