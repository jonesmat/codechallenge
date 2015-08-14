import os
from random import randint
import uuid

from flask import Flask, request, render_template, redirect
from werkzeug import secure_filename

from model.puzzle_manager import PuzzleManager
from model.puzzle import Puzzle
from model.problem import Problem
from model.problem_attempt import ProblemAttempt


########## Initialization ###########


app = Flask(__name__, static_url_path="", static_folder = "content")

puzzmgr = PuzzleManager() 


########## Routes ###########


@app.route('/')
def home():
	return render_template('home.html', puzzles=puzzmgr.puzzles, team_points_total=puzzmgr.get_total_team_points())

@app.route('/puzzle/<puzzle_id>', methods=['GET', 'POST'])
def show_puzzle(puzzle_id):
	if request.method == 'GET':
		puzzle = puzzmgr.get_puzzle(puzzle_id)
		if puzzle is None:
			assert False, 'Puzzle id does not exist!'

		return render_template('puzzle.html', puzzle=puzzle, team_points_total=puzzmgr.get_total_team_points())
	else:
		# Problem submission

		# retrieve form data
		prob_id = request.form['prob_id']
		teamname = request.form['teamname']
		solution_file = request.files['solution_file']  # Returns the actual File obj

		# Clean and truncate teamname to prevent abuse
		teamname = teamname.strip()
		if len(teamname) > 15:
			teamname = teamname[0:12] + '...'

		# Store the uploaded solution file
		solution_filepath = ''
		if solution_file:
			filename = secure_filename(solution_file.filename)
			filename += str(uuid.uuid1())
			solution_filepath = os.path.join(app.config['SOLUTION_FOLDER'], 
				filename)
			solution_file.save(solution_filepath)
		else:
			# An solution file is required, can't continue without it
			return redirect('/', code=302)

		# Feed solution and problem files to puzzle app to score the attempt.
		puzzle = puzzmgr.get_puzzle(puzzle_id)
		problem = puzzle.get_problem(prob_id)
		score, error_msg = puzzmgr.score_attempt(puzzle.app_path, problem.problem_file, solution_filepath)
		
		# Record the attempt
		attempt = ProblemAttempt(solution_filepath, teamname, score, error_msg)
		problem.attempts.append(attempt)
		
		return render_template('puzzle_submitted.html', puzzle_id=puzzle_id, attempt=attempt, team_points_total=puzzmgr.get_total_team_points())

# Error handlers
@app.errorhandler(403)
def forbidden_request(error):
	return render_template('error.html', error=error), 403

@app.errorhandler(404)
def page_not_found_request(error):
	return render_template('error.html', error=error), 404
	
@app.errorhandler(410)
def gone_request(error):
	return render_template('error.html', error=error), 410
	
@app.errorhandler(413)
def file_too_large_request(error):
	return render_template('error.html', error=error), 413
	
@app.errorhandler(500)
def internal_server_error_request(error):
	return render_template('error.html', error=error), 500



########## Main ###########

if __name__ == '__main__':
	# Configure the app
	app.config['SOLUTION_FOLDER'] = 'solutions/'
	if not os.path.exists(app.config['SOLUTION_FOLDER']):
		os.makedirs(app.config['SOLUTION_FOLDER'])
	
	app.config['MAX_CONTENT_LENGTH'] = 10 * 1024  # 10KB

	app.debug = True
	app.run(host='0.0.0.0')

