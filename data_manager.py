import csv


class DataManager(object):
	''' 
	Provides an interface for the model to store and retrieve data locally.
	'''

	def __init__(self):
		# Define the data filenames
		self.puzzles_data_filepath = 'data/puzzles_data'
		self.problems_data_filepath = 'data/problems_data'
		self.attempts_data_filepath = 'data/attempts_data'

		# Initialize data storage
		self.puzzles_data = []
		self.problems_data = []
		self.attempts_data = []

	def load(self):
		# Init data before loading
		self.puzzles_data = []
		self.problems_data = []
		self.attempts_data = []

		#########################################################
		##################### LOAD PUZZLES ######################
		#########################################################
		with open(self.puzzles_data_filepath, 'rU') as f:
			reader = csv.reader(f)
			self.puzzles_data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		
		if self.puzzles_data is None or len(self.puzzles_data) == 0:
			assert('Unable to load puzzle data')

		# Remove the header row
		self.puzzles_data.pop(0)

		
		#########################################################
		##################### LOAD PROBLEMS #####################
		#########################################################
		with open(self.problems_data_filepath, 'rU') as f:
			reader = csv.reader(f)
			self.problems_data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		
		if self.problems_data is None or len(self.problems_data) == 0:
			assert('Unable to load problem data')

		# Remove the header row
		self.problems_data.pop(0)

		
		#########################################################
		##################### LOAD ATTEMPTS ######################
		#########################################################
		with open(self.attempts_data_filepath, 'rU') as f:
			reader = csv.reader(f)
			self.attempts_data = list(list(rec) for rec in csv.reader(f, delimiter=','))
		
		if self.attempts_data is None or len(self.attempts_data) == 0:
			assert('Unable to load attempt data')

		# Remove the header row
		self.attempts_data.pop(0)

	def get_puzzles_data(self):
		'''
			Puzzle data in the following format:
			[ [ Id, Name, Instructions, App path ], ... ]
		'''
		return self.puzzles_data

	def get_problems_data(self, puzzle_id):
		'''
			Problem data in the following format:
			[ [ Puzzle Id, Problem Id, Name, Description, Problem Filepath ], ... ]
		'''
		# Return only the problems for the specified puzzle_id
		return [problem for problem in self.problems_data if problem[0] == puzzle_id]

	def get_attempts_data(self, problem_id):
		'''
			Problem attempt data in the following format:
			[ [ Problem Id, TeamName, Score, Timestamp, Timedata, Solution Filepath ], ... ]
		'''
		return [attempt for attempt in self.attempts_data if attempt[0] == problem_id]

	def save_puzzles_data(self, puzzles_data):
		'''
		The puzzle data passed in is a list of lists:
			[ [ Id, Name, Instructions, App path, Status ], ... ]
		'''
		header_row = ['Puzzle Id', 'Name', 'Instructions', 'App path', 'Status']
		
		with open(self.puzzles_data_filepath, "wb") as f:
			writer = csv.writer(f)
			writer.writerows([header_row] + puzzles_data)

	def save_attempts_data(self, attempts_data):
		'''
		The attempts data passed in is a list of lists:
			[ [ Problem Id, TeamName, Score, Timestamp, Timedata, Solution Filepath ], ... ]
		'''
		header_row = ['Problem Id', 'TeamName', 'Score', 'Timestamp', 'Timedata', 'Solution Filepath']
		
		with open(self.attempts_data_filepath, "wb") as f:
			writer = csv.writer(f)
			writer.writerows([header_row] + attempts_data)
		
