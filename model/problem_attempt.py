

class ProblemAttempt(object):
	''' Represents an attempt at solving a problem on a puzzle '''
	
	def __init__(self):
		self.teamname = ''
		self.score = 0
		self.timestamp = ''  # Human readable time of submission (helpful for reading on spreadsheet)
		self.timedata = 0  # Computer friendly time of submission
		self.solution_filepath = ''

	def load(self, data):
		self.teamname = data[1]
		self.score = int(data[2])
		self.timestamp = data[3]
		self.timedata = data[4]
		self.solution_filepath = data[5]