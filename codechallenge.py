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
	return render_template('home.html', puzzles=puzzmgr.puzzles)

@app.route('/puzzle/<puzzle_id>', methods=['GET', 'POST'])
def show_puzzle(puzzle_id):
	if request.method == 'GET':
		puzzle = puzzmgr.get_puzzle(puzzle_id)
		if puzzle is None:
			assert False, 'Puzzle id does not exist!'
			
		return render_template('puzzle.html', puzzle=puzzle)
		
	else:
		# Problem submission

		# retrieve form data
		prob_id = request.form['prob_id']
		teamname = request.form['teamname']
		solution_file = request.files['solution_file']  # Returns the actual File obj

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

		# Feed solution file to puzzle app
		puzzle = puzzmgr.get_puzzle(puzzle_id)
		score = puzzmgr.score_attempt(puzzle.app_path, solution_filepath)
		
		# Record the attempt
		attempt = ProblemAttempt(solution_filepath, teamname, score)
		problem = puzzle.get_problem(prob_id)
		problem.attempts.append(attempt)
		
		return render_template('puzzle_submitted.html', puzzle_id=puzzle_id, attempt=attempt)
	


########## Main ###########

if __name__ == '__main__':
	app.config['SOLUTION_FOLDER'] = 'solutions/'
	if not os.path.exists(app.config['SOLUTION_FOLDER']):
		os.makedirs(app.config['SOLUTION_FOLDER'])
	
	app.debug = True
	app.run(host='0.0.0.0')

