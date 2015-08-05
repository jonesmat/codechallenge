from flask import Flask, request, render_template, redirect
from werkzeug import secure_filename
import os
from random import randint
import uuid
from puzzle import Puzzle, PuzzleManager


########## Initialization ###########

app = Flask(__name__, static_url_path="", static_folder = "content")

probmgr = PuzzleManager() 


########## Routes ###########


@app.route('/')
def home():
	return render_template('home.html', puzzles=probmgr.puzzles)

@app.route('/puzzle/<puzzle_id>', methods=['GET', 'POST'])
def show_puzzle(puzzle_id):
	if request.method == 'GET':
		puzzle = probmgr.get_puzzle(puzzle_id)
		if puzzle is None:
			assert False, 'Puzzle id does not exist!'
			
		high_scoring_attempts = puzzle.ordered_attempts
		return render_template('puzzle.html', puzzle=puzzle, 
								high_scoring_attempts=high_scoring_attempts)
		
	else:
		# Puzzle submission
		
		# Store the uploaded solution file
		solution_file = request.files['solution_file']  # Returns the actual File obj
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
		puzzle = probmgr.get_puzzle(puzzle_id)
		score = probmgr.score_attempt(puzzle.app_path, solution_filepath)
		
		# Record the attempt
		attempt = probmgr.record_attempt(puzzle_id, solution_filepath, request.form['teamname'], score)
		
		return render_template('puzzle_submitted.html', puzzle_id=puzzle_id, attempt=attempt)
	


########## Main ###########

if __name__ == '__main__':
	app.config['SOLUTION_FOLDER'] = 'solutions/'
	if not os.path.exists(app.config['SOLUTION_FOLDER']):
		os.makedirs(app.config['SOLUTION_FOLDER'])
	
	app.debug = True
	app.run(host='0.0.0.0')

