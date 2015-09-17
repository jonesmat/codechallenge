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
	def __init__(self, data_mgr):
		self.puzzles = []
		self.data_mgr = data_mgr

	def load(self):
		# init data before loading
		self.puzzles = []

		# Load puzzles
		puzzles_data = self.data_mgr.get_puzzles_data()
		for puzzle_data in puzzles_data:
			puzzle = Puzzle(self.data_mgr)
			puzzle.load(puzzle_data)

			self.puzzles.append(puzzle)
	
	def save(self):
		# Save Puzzles
		puzzles_data = []
		for puzzle in self.puzzles:
			puzzles_data.append([puzzle.puzzle_id, puzzle.name, puzzle.instructions, 
								 puzzle.app_path, puzzle.state])
		self.data_mgr.save_puzzles_data(puzzles_data)

		# TODO Save Problems

		# Save Problem Attempts
		attempts_data = []
		for puzzle in self.puzzles:
			for problem in puzzle.problems:
				for attempt in problem.attempts:
					attempts_data.append([problem.prob_id, attempt.teamname, attempt.score, 
											attempt.timestamp, attempt.timedata, 
											attempt.solution_filepath])
		self.data_mgr.save_attempts_data(attempts_data)

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

	