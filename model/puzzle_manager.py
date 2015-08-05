import subprocess
from puzzle import Puzzle
from problem import Problem
		

class PuzzleManager(object):
	def __init__(self):
		# Initialize list of puzzles
		self.puzzles = []

		############################################################################################
		##################################### First Test Puzzle ####################################
		############################################################################################
		puzzle_id = 'puzz1'
		puzz_name = 'First Test Puzzle'
		instructions = '''<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>
			<br/>
			<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>'''
		app_path = 'puzzle_apps/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, puzz_name, instructions, app_path)

		problem_id = 'puzz1_easy'
		prob_name = 'Easy'
		prob_desc = 'An easier challege for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		problem_id = 'puzz1_med'
		prob_name = 'Medium'
		prob_desc = 'The average challege for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		problem_id = 'puzz1_hard'
		prob_name = 'Hard'
		prob_desc = 'A difficult challenge for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		self.puzzles.append(puzzle)

		############################################################################################
		##################################### Second Test Puzzle ####################################
		############################################################################################
		puzzle_id = 'puzz2'
		puzz_name = 'Second Test Puzzle'
		instructions = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.'''
		app_path = 'puzzle_apps/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, puzz_name, instructions, app_path)

		problem_id = 'puzz2_easy'
		prob_name = 'Easy'
		prob_desc = 'An easier challege for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		problem_id = 'puzz2_med'
		prob_name = 'Medium'
		prob_desc = 'The average challege for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		problem_id = 'puzz2_hard'
		prob_name = 'Hard'
		prob_desc = 'A difficult challenge for the first test puzzle'
		problem = Problem(problem_id, prob_name, prob_desc)
		puzzle.problems.append(problem)

		self.puzzles.append(puzzle)
	
	def get_puzzle(self, puzzle_id):
		for puzzle in self.puzzles:
			if puzzle.puzzle_id == puzzle_id:
				return puzzle
		return None

	@staticmethod
	def score_attempt(app_path, solution_filepath):
		"""
		Runs the puzzle's external application and passes the solution file as the
		only parameter.  Stdout is returned from the app containing the score.
		"""
		score = subprocess.check_output([app_path, solution_filepath])
		return int(score)
		
		