from problem import Problem


class Puzzle(object):

	def __init__(self, data_mgr):
		self.data_mgr = data_mgr
		self.problems = []

		self.puzzle_id = ''
		self.name = ''
		self.instructions = ''
		self.app_path = ''
		self.state = PuzzleState.NEW
	
	def load(self, puzzle_data):
		'''
		Check how the DataManager loads puzzle data if there is an issue here.
		'''
		self.puzzle_id = puzzle_data[0]
		self.name = puzzle_data[1]
		self.instructions = puzzle_data[2]
		self.app_path = puzzle_data[3]
		self.state = puzzle_data[4]

		# Load problems
		problems_data = self.data_mgr.get_problems_data(self.puzzle_id)
		for problem_data in problems_data:
			problem = Problem(self.data_mgr)
			problem.load(problem_data)
			
			self.problems.append(problem)
					

	def get_problem(self, prob_id):
		for problem in self.problems:
			if problem.prob_id == prob_id:
				return problem
		return None

	def get_puzzle_point_totals(self):
		"""
		Returns a list of teams with their total points ordered from highest to lowest for 
		this puzzle.
		<teamname, points>
		"""

		team_points_dict = dict()  
		for problem in self.problems:
			best_attempts = problem.get_best_attempts()
			for best_attempt in best_attempts:
				if best_attempt.teamname not in team_points_dict.keys():
					team_points_dict[best_attempt.teamname] = 0

				team_points_dict[best_attempt.teamname] += best_attempt.points_awarded

		team_points_list = team_points_dict.items()

		# Order the totals by points (highest to lowest)
		team_points_list = sorted(team_points_list, key = lambda team_total: team_total[1], reverse=True)
		return team_points_list

	def reset(self):
		for problem in self.problems:
			problem.attempts = []
		self.state = PuzzleState.NEW


class PuzzleState(object):
	NEW 		= "NEW"
	OPEN 		= "OPEN"
	CLOSED 		= "CLOSED"