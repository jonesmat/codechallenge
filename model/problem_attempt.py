

class ProblemAttempt(object):
	''' Represents an attempt at solving a problem on a puzzle '''
	
	def __init__(self, solution_filepath, teamname, score, error_msg):
		self.solution_filepath = solution_filepath
		self.teamname = teamname
		self.score = score  # Greater than or equal to 0 if an error didn't occur
		self.error_msg = error_msg  # An error that may have occured when scoring the attempt