

class Puzzle(object):

	def __init__(self, puzzle_id, name, instructions, app_path):
		self.puzzle_id = puzzle_id
		self.name = name
		self.instructions = instructions
		self.app_path = app_path
		self.problems = []
	
	def get_problem(self, prob_id):
		for problem in self.problems:
			if problem.prob_id == prob_id:
				return problem
		return None

	def get_team_points(self):
		"""
		Returns a list of teams with their total points ordered from highest to lowest for 
		this puzzle.
		<teamname, points>
		"""
		team_points_dict = dict()  
		for problem in self.problems:
			team_points_for_problem = problem.get_team_points()  # list of <points, teamname> pairs
			for teamname, points in team_points_for_problem:
				if teamname not in team_points_dict.keys():
					team_points_dict[teamname] = 0
				team_points_dict[teamname] = team_points_dict[teamname] + points
		team_points_list = team_points_dict.items()

		# Order the totals by points (highest to lowest)
		team_points_list = sorted(team_points_list, key = lambda team_total: team_total[1], reverse=True)
		return team_points_list