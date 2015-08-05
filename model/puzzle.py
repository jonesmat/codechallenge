

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