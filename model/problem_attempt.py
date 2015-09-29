

class ProblemAttempt(object):
	''' Represents an attempt at solving a problem on a puzzle '''
	
	def __init__(self):
		# Loaded members
		self.teamname = ''
		self.score = None
		self.timestamp = ''  # Human readable time of submission (helpful for reading on spreadsheet)
		self.timedata = 0  # Computer friendly time of submission
		self.solution_filepath = ''

		# Computed members
		self.points_awarded = 0

	def load(self, data):
		self.teamname = data[1]
		self.score = int(data[2])
		self.timestamp = data[3]
		self.timedata = data[4]
		self.solution_filepath = data[5]