

class ProblemAttempt(object):
	''' Represents an attempt at solving a problem on a puzzle '''
	
	def __init__(self, solution_filepath, teamname, score):
		self.solution_filepath = solution_filepath
		self.teamname = teamname
		self.score = score