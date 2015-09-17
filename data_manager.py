import json
from oauth2client.client import SignedJwtAssertionCredentials

from thirdparty import gspread



class DataManager(object):
	''' 
	Provides an interface for the model to store and retrieve data.  the
	current implementation uses a Google Spreadsheet to store data.

	Gspread is the thirdparty library used for accessing Google spreadsheet.
	https://github.com/burnash/gspread
	'''

	def __init__(self, oauth2_cred_filepath, spreadsheet_url):
		# Create an OAuth2 credential object for accessing the google doc
		json_key = json.load(open(oauth2_cred_filepath))
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
		
		# Disable host checking because Windows has problems reading from CA cert path when running in IIS
		import ssl
		def no_default_cert_create_default_https_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None,
                           capath=None, cadata=None):
			if not isinstance(purpose, ssl._ASN1Object):
				raise TypeError(purpose)

			context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

			# SSLv2 considered harmful.
			context.options |= ssl.OP_NO_SSLv2

			# SSLv3 has problematic security and is only required for really old
			# clients such as IE6 on Windows XP
			context.options |= ssl.OP_NO_SSLv3

			# disable compression to prevent CRIME attacks (OpenSSL 1.0+)
			context.options |= getattr(ssl._ssl, "OP_NO_COMPRESSION", 0)
			return context
			
		
		ssl._create_default_https_context = no_default_cert_create_default_https_context
		import httplib2
		http = httplib2.Http( disable_ssl_certificate_validation = True )
		
		# Login with your Google account
		gc = gspread.authorize(credentials, http)

		# open the spreadsheet by its url
		spreadsheet = gc.open_by_url(spreadsheet_url)

		# Get the worksheets by name
		self.puzzles_worksheet = spreadsheet.worksheet("Puzzles")
		self.problems_worksheet = spreadsheet.worksheet("Problems")
		self.attempts_worksheet = spreadsheet.worksheet("Attempts")

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
		self.puzzles_data = self.puzzles_worksheet.get_all_values()

		if self.puzzles_data is None or len(self.puzzles_data) == 0:
			assert('Unable to load puzzle data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_puzzles_data = []
		for puzzle_data in self.puzzles_data:
			if puzzle_data[0] is not None and len(puzzle_data[0]) > 0:
				temp_puzzles_data.append(puzzle_data)
		self.puzzles_data = temp_puzzles_data

		# Remove the header row
		self.puzzles_data.pop(0)

		
		#########################################################
		##################### LOAD PROBLEMS #####################
		#########################################################
		self.problems_data = self.problems_worksheet.get_all_values()

		if self.problems_data is None or len(self.problems_data) == 0:
			assert('Unable to load problem data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_problems_data = []
		for problem_data in self.problems_data:
			if problem_data[0] is not None and len(problem_data[0]) > 0:
				temp_problems_data.append(problem_data)
		self.problems_data = temp_problems_data

		# Remove the header row
		self.problems_data.pop(0)

		
		#########################################################
		##################### LOAD ATTEMPTS ######################
		#########################################################
		self.attempts_data = self.attempts_worksheet.get_all_values()

		if self.attempts_data is None or len(self.attempts_data) == 0:
			assert('Unable to load problem data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_attempts_data = []
		for attempt_data in self.attempts_data:
			if attempt_data[0] is not None and len(attempt_data[0]) > 0:
				temp_attempts_data.append(attempt_data)
		self.attempts_data = temp_attempts_data

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
		Each save replaces the data on the google spreadsheet with the data
		passed to this function.

		*** This is not an atomic save, in the event of a problem with saving
		use google's revision history feature to recover. ***
		'''
		# Clear all data to make room for the save
		columns = 5
		self.puzzles_worksheet.resize(1, columns)  # resizes to a header row and 5 columns

		# Now that the data has been cleared, resize to the number of puzzles
		last_row = len(puzzles_data) + 1
		self.puzzles_worksheet.resize(last_row, columns)

		# Grab the cells so we can populate them
		cell_list = self.puzzles_worksheet.range('A2:E%d' % last_row)

		# Example cell_list format for a range of A1:C3:
		# [Cell_A1, Cell_A2, Cell_A3, Cell_B1, Cell_B2, Cell_B3, Cell_C1, Cell_C2, Cell_C3]

		# Now that we have the cells from the range, update the cell values with the data.
		cell_index = 0
		for puzzle_data in puzzles_data:
			for column in range(0, columns):
				cell_list[cell_index].value = puzzle_data[column]
				cell_index = cell_index + 1

		self.puzzles_worksheet.update_cells(cell_list)

	def save_attempts_data(self, attempts_data):
		'''
		Each save replaces the data on the google spreadsheet with the data
		passed to this function.

		*** This is not an atomic save, in the event of a problem with saving
		use google's revision history feature to recover. ***
		'''
		# Clear all data to make room for the save
		columns = 6
		self.attempts_worksheet.resize(1, columns)  # resizes to a header row and 6 columns

		# Now that the data has been cleared, resize to the number of attempts
		last_row = len(attempts_data) + 1
		self.attempts_worksheet.resize(last_row, columns)

		# Grab the cells so we can populate them
		cell_list = self.attempts_worksheet.range('A2:F%d' % last_row)

		# Example cell_list format for a range of A1:C3:
		# [Cell_A1, Cell_A2, Cell_A3, Cell_B1, Cell_B2, Cell_B3, Cell_C1, Cell_C2, Cell_C3]

		# Now that we have the cells from the range, update the cell values with the data.
		cell_index = 0
		for attempt_data in attempts_data:
			for column in range(0, columns):
				cell_list[cell_index].value = attempt_data[column]
				cell_index = cell_index + 1

		self.attempts_worksheet.update_cells(cell_list)
		
