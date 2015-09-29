import os
from random import randint
import uuid
import time

from flask import Flask, request, render_template, redirect
from werkzeug import secure_filename

from data_manager import DataManager
from model.puzzle_manager import PuzzleManager
from model.puzzle import Puzzle, PuzzleState
from model.problem import Problem
from model.problem_attempt import ProblemAttempt


########## Initialization ###########


app = Flask(__name__, static_url_path="", static_folder = "content")

datamgr = DataManager()
datamgr.load()

puzzmgr = PuzzleManager(datamgr) 
puzzmgr.load()

ADMIN_PASSWORD = 'puzzles'

# Setup web app configurations
app.config['SOLUTION_FOLDER'] = 'solutions/'
if not os.path.exists(app.config['SOLUTION_FOLDER']):
	os.makedirs(app.config['SOLUTION_FOLDER'])

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024  # 10KB


########## Routes ###########


@app.route('/')
def home():
	try:
		return render_template('home.html', puzzles=puzzmgr.puzzles, 
			global_point_totals=puzzmgr.get_global_point_totals())
		
	except Exception as ex:
		return render_template('error.html', error=str(ex)), 500

@app.route('/puzzle/<puzzle_id>', methods=['GET', 'POST'])
def show_puzzle(puzzle_id):
	try:
		if request.method == 'GET':
			puzzle = puzzmgr.get_puzzle(puzzle_id)
			if puzzle is None:
				return render_template('error.html', error="Puzzle does not exist!"), 403

			if puzzle.state == PuzzleState.OPEN:
				return render_template('puzzle.html', puzzle=puzzle, 
					global_point_totals=puzzmgr.get_global_point_totals(), 
					puzzle_point_totals=puzzle.get_puzzle_point_totals())

			elif puzzle.state == PuzzleState.CLOSED:
				return render_template('puzzle_closed.html', puzzle=puzzle, 
					global_point_totals=puzzmgr.get_global_point_totals(), 
					puzzle_point_totals=puzzle.get_puzzle_point_totals())

			elif puzzle.state == PuzzleState.NEW:
				return render_template('error.html', error="Puzzle is not yet available!"), 403 

		else:
			# Problem submission

			# retrieve form data
			prob_id = request.form['prob_id']
			teamname = request.form['teamname']
			solution_file = request.files['solution_file']  # Returns the actual File obj

			# ensure the puzzle is open and accepting submissions
			puzzle = puzzmgr.get_puzzle(puzzle_id)
			if puzzle.state != PuzzleState.OPEN:
				# The puzzle is not open, redirect to the closed puzzle page
				return render_template('puzzle_closed.html', puzzle=puzzle, 
					global_point_totals=puzzmgr.get_global_point_totals(), 
					puzzle_point_totals=puzzle.get_puzzle_point_totals())

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
			problem = puzzle.get_problem(prob_id)
			score, error_msg = puzzmgr.score_attempt(puzzle.app_path, problem.problem_file, solution_filepath)
			
			# Record the attempt
			attempt = ProblemAttempt()
			attempt.teamname = teamname
			attempt.score = -1  # -1 indicates an error
			if score > 0:
				attempt.score = score
				attempt.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
				attempt.timedata = time.time()
				attempt.solution_filepath = solution_filepath
				problem.attempts.append(attempt)

				puzzmgr.save()  # Data changed, lets save it.
			else:
				pass  # TODO log it
			
			return render_template('puzzle_submitted.html', puzzle_id=puzzle_id, attempt=attempt, 
									global_point_totals=puzzmgr.get_global_point_totals(), 
									error_msg=error_msg)
	except Exception as ex:
		return render_template('error.html', error=str(ex)), 500


@app.route('/admin', methods=['GET', 'POST'])
def show_admin():
	try:
		if request.method == 'GET':
			return render_template('login.html', global_point_totals=puzzmgr.get_global_point_totals())
		else:
			
			if 'passcode' in request.form:
				# Admin is attempting to login
				passcode = request.form['passcode']

				if passcode == ADMIN_PASSWORD:
					return render_template('admin.html', puzzmgr=puzzmgr, 
											global_point_totals=puzzmgr.get_global_point_totals())
				else:
					return render_template('login.html', 
											global_point_totals=puzzmgr.get_global_point_totals())
			elif 'puzzle_id' in request.form:
				# Admin is updating a puzzle

				puzzle = puzzmgr.get_puzzle(request.form['puzzle_id'])
				assert(puzzle)

				# Determine which action the admin is taking on the puzzle
				if 'open_puzzle' in request.form and puzzle.state != PuzzleState.OPEN:
					puzzle.state = PuzzleState.OPEN
				elif 'close_puzzle' in request.form and puzzle.state != PuzzleState.CLOSED:
					puzzle.state = PuzzleState.CLOSED
				elif 'reset_puzzle' in request.form and puzzle.state != PuzzleState.NEW:
					puzzle.reset()

				puzzmgr.save()  # Data changed, save it

				# Return to the admin page after updating the puzzle
				return render_template('admin.html', puzzmgr=puzzmgr, 
										global_point_totals=puzzmgr.get_global_point_totals())
			elif 'reload_data' in request.form:
				# Admin is requesting a data reload
				datamgr.load()
				puzzmgr.load()

				# Reload the admin page
				return render_template('admin.html', puzzmgr=puzzmgr, 
											global_point_totals=puzzmgr.get_global_point_totals())
	except Exception as ex:
		return render_template('error.html', error=str(ex)), 500


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

	app.debug = True
	app.run(host='0.0.0.0')

