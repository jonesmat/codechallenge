import subprocess
from puzzle import Puzzle
from problem import Problem


'''
+----------+                                           
| Problem  |                                           
|  File    | +-------> +--------------+                
+----------+           |              |       +-------+
                       |  Puzzle App  | +---> | Score |
+----------+           |              |       +-------+
| Solution | +-------> +--------------+                
|   File   |                                           
+----------+     
'''


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
		app_path = 'puzzles/puzzle1/Puzzle1.exe'
		puzzle = Puzzle(puzzle_id, puzz_name, instructions, app_path)

		problem_id = 'puzz1_easy'
		prob_name = 'Easy'
		prob_desc = 'An easier challege for the first test puzzle'
		prob_file = 'puzzles/puzzle1/problem1.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
		puzzle.problems.append(problem)

		problem_id = 'puzz1_med'
		prob_name = 'Medium'
		prob_desc = 'The average challege for the first test puzzle'
		prob_file = 'puzzles/puzzle1/problem2.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
		puzzle.problems.append(problem)

		problem_id = 'puzz1_hard'
		prob_name = 'Hard'
		prob_desc = 'A difficult challenge for the first test puzzle'
		prob_file = 'puzzles/puzzle1/problem3.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
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
		app_path = 'puzzles/puzzle2/Puzzle2.exe'
		puzzle = Puzzle(puzzle_id, puzz_name, instructions, app_path)

		problem_id = 'puzz2_easy'
		prob_name = 'Easy'
		prob_desc = 'An easier challege for the first test puzzle'
		prob_file = 'puzzles/puzzle2/problem1.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
		puzzle.problems.append(problem)

		problem_id = 'puzz2_med'
		prob_name = 'Medium'
		prob_desc = 'The average challege for the first test puzzle'
		prob_file = 'puzzles/puzzle2/problem2.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
		puzzle.problems.append(problem)

		problem_id = 'puzz2_hard'
		prob_name = 'Hard'
		prob_desc = 'A difficult challenge for the first test puzzle'
		prob_file = 'puzzles/puzzle2/problem3.txt'
		problem = Problem(problem_id, prob_name, prob_desc, prob_file)
		puzzle.problems.append(problem)

		self.puzzles.append(puzzle)
	
	def get_puzzle(self, puzzle_id):
		for puzzle in self.puzzles:
			if puzzle.puzzle_id == puzzle_id:
				return puzzle
		return None

	def get_total_team_points(self):
		"""
		Returns a list of teams with their total points ordered from highest to lowest.
		<teamname, points>
		"""
		team_point_totals_dict = dict()  
		for puzzle in self.puzzles:
			team_points_for_puzzle = puzzle.get_team_points()  # list of <points, teamname> pairs
			for teamname, points in team_points_for_puzzle:
				if teamname not in team_point_totals_dict.keys():
					team_point_totals_dict[teamname] = 0
				team_point_totals_dict[teamname] = team_point_totals_dict[teamname] + points
		team_point_totals = team_point_totals_dict.items()

		# Order the totals by points (highest to lowest)
		team_point_totals = sorted(team_point_totals, key = lambda team_total: team_total[1], reverse=True)
		return team_point_totals

	@staticmethod
	def score_attempt(app_path, problem_filepath, solution_filepath):
		"""
		Runs the puzzle's external application and passes the problem file and the solution file as
		commandline arguments.

		This function returns the score and any stderr from the external app.
		"""
		
		# Execute the puzzle application and collect the output.
		app_output = ''
		try:
			app_output = subprocess.check_output([app_path, problem_filepath, solution_filepath], 
				stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError as ex:
			# The app returned a non-zero return code.  Build an error message and return it.
			error_str = 'Command \'' + ' '.join(ex.cmd) + '\' failed with ' + str(ex.returncode) + \
				' retcode. ' + ex.output
			return (-1, error_str)

		# At this point the app has returned successfully.  Attempt to pull a score from the output.

		if len(app_output) == 0:
			error_str = 'The problem app didn\'t return any data'
			return (-1, error_str)

		try:
			# Try converting the output to an integer.  This indicates that a valid score was
			# returned.
			score = int(app_output)

			# We have a score, return it.
			return (score, '')
		except ValueError as ex:
			# The string output returned by the app wasn't an integer, it must have been an error.
			error_str = app_output
			return (-1, error_str)

	