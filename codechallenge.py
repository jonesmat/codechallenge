from flask import Flask, request, render_template, redirect
from werkzeug import secure_filename
import os
from random import randint
import uuid
from problem import Problem, ProblemManager


########## Initialization ###########

app = Flask(__name__, static_url_path="", static_folder = "content")

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
			
		high_scoring_attempts = probmgr.get_highest_scoring_attempts(problem)
		return render_template('problem.html', problem=problem, 
								high_scoring_attempts=high_scoring_attempts)
		
	else:
		# Problem submission
		
		# Store the uploaded output file
		output_file = request.files['output_file']  # Returns the actual File obj
		output_filepath = ''
		if output_file:
			filename = secure_filename(output_file.filename)
			filename += str(uuid.uuid1())
			output_filepath = os.path.join(app.config['PROBLEM_OUTPUT_FOLDER'], 
				filename)
			output_file.save(output_filepath)

		# Feed output file to problem app
		problem = probmgr.get_problem(prob_id)
		score = probmgr.score_attempt(problem.app_path, output_filepath)
		
		# Record the attempt
		attempt = probmgr.record_attempt(prob_id, request.form['email'], score)
		
		return render_template('problem_submitted.html', prob_id=prob_id, attempt=attempt)
	


########## Main ###########

if __name__ == '__main__':
	app.config['PROBLEM_OUTPUT_FOLDER'] = 'problem_outputs/'
	if not os.path.exists(app.config['PROBLEM_OUTPUT_FOLDER']):
		os.makedirs(app.config['PROBLEM_OUTPUT_FOLDER'])
	
	app.debug = True
	app.run(host='0.0.0.0')

