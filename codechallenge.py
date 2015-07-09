from flask import Flask, request, render_template, redirect
from werkzeug import secure_filename
import os
from random import randint
import uuid
from problem import Problem, ProblemManager


########## Initialization ###########

app = Flask('CodeChallenge')

probmgr = ProblemManager() 


########## Routes ###########


@app.route('/')
def home():
	return render_template('home.html', problems=probmgr.problems)

@app.route('/problem/<prob_id>', methods=['GET', 'POST'])
def show_problem(prob_id):
	if request.method == 'GET':
		problem = probmgr.get_problem(prob_id)
		if problem is None:
			assert False, 'Problem id does not exist!'
		return render_template('problem.html', problem=problem)
		
	else:
		# Problem submission
		
		# Store the uploaded output file
		output_file = request.files['output_file']
		savedfilepath = ''
		if output_file:
			filename = secure_filename(output_file.filename)
			filename += str(uuid.uuid1())
			savedfilepath = os.path.join(app.config['PROBLEM_OUTPUT_FOLDER'], 
				filename)
			output_file.save(savedfilepath)

		# Feed output file to problem app
		# score = ProblemApp.test(prob_id, savedfilepath)
		score = randint(0, 100)
		
		# Record the score
		probmgr.record_score(prob_id, request.form['email'], score)
		
		return "You scored %s!  Goodluck with the competition!" % score
	


########## Main ###########

if __name__ == '__main__':
	app.config['PROBLEM_OUTPUT_FOLDER'] = 'problem_outputs/'
	if not os.path.exists(app.config['PROBLEM_OUTPUT_FOLDER']):
		os.makedirs(app.config['PROBLEM_OUTPUT_FOLDER'])
	
	app.debug = True
	app.run(host='0.0.0.0')

