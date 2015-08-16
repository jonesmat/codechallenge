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

	def __init__(self, oauth2_cred_filepath):
		# Create an OAuth2 credential object for accessing the google doc
		json_key = json.load(open(oauth2_cred_filepath))
		scope = ['https://spreadsheets.google.com/feeds']
		credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)

		# Login with your Google account
		gc = gspread.authorize(credentials)

		# open the spreadsheet by its url
		spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PmHHHjyvoSg-erK_CvMmKCtYsezHOGHvoUu6EiZWutM/edit#gid=0')

		# Get the worksheets by name
		self.puzzles_worksheet = spreadsheet.worksheet("Puzzles")
		self.problems_worksheet = spreadsheet.worksheet("Problems")
		self.attempts_worksheet = spreadsheet.worksheet("Attempts")

	def get_puzzles_data(self):
		'''
			Returns raw puzzle data in the following format:

			[ [ Id, Name, Instructions, App path ], ... ]
		'''
		puzzles_data = self.puzzles_worksheet.get_all_values()

		if puzzles_data is None or len(puzzles_data) == 0:
			assert('Unable to load puzzle data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_puzzles_data = []
		for puzzle_data in puzzles_data:
			if puzzle_data[0] is not None and len(puzzle_data[0]) > 0:
				temp_puzzles_data.append(puzzle_data)
		puzzles_data = temp_puzzles_data

		# Return all rows except the first (its a header row)
		return puzzles_data[1:]

	def get_problems_data(self):
		'''
			Returns raw problem data in the following format:

			[ [ Puzzle Id, Problem Id, Name, Description, Problem Filepath ], ... ]
		'''
		problems_data = self.problems_worksheet.get_all_values()

		if problems_data is None or len(problems_data) == 0:
			assert('Unable to load problem data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_problems_data = []
		for problem_data in problems_data:
			if problem_data[0] is not None and len(problem_data[0]) > 0:
				temp_problems_data.append(problem_data)
		problems_data = temp_problems_data

		# Return all rows except the first (its a header row)
		return problems_data[1:]

	def get_attempts_data(self):
		'''
			Returns raw problem attempt data in the following format:

			[ [ Problem Id, TeamName, Score, Timestamp, Solution Filepath ], ... ]
		'''
		attempts_data = self.attempts_worksheet.get_all_values()

		if attempts_data is None or len(attempts_data) == 0:
			assert('Unable to load problem data')

		# gspread will return ALL rows in the worksheet, even empty ones.
		# Remove the empty rows
		temp_attempts_data = []
		for attempt_data in attempts_data:
			if attempt_data[0] is not None and len(attempt_data[0]) > 0:
				temp_attempts_data.append(attempt_data)
		attempts_data = temp_attempts_data

		# Return all rows except the first (its a header row)
		return attempts_data[1:]

	def save_puzzles_data(self, puzzles_data):
		'''
		Each save replaces the data on the google spreadsheet with the data
		passed to this function.

		*** This is not an atomic save, in the event of a problem with saving
		use google's revision history feature to recover. ***
		'''

		# Clear all data to make room for the save
		self.puzzles_worksheet.resize(1, 5)  # resizes to 1 row and 5 columns

		# Save rows one by one (not the most efficent way, but I don't care...)
		for puzzle_data in puzzles_data:
			self.puzzles_worksheet.append_row(puzzle_data)

	def save_attempts_data(self, attempts_data):
		'''
		Each save replaces the data on the google spreadsheet with the data
		passed to this function.

		*** This is not an atomic save, in the event of a problem with saving
		use google's revision history feature to recover. ***
		'''

		# Clear all data to make room for the save
		self.attempts_worksheet.resize(1, 5)  # resizes to 1 row and 5 columns

		# Save rows one by one (not the most efficent way, but I don't care...)
		for attempt_data in attempts_data:
			self.attempts_worksheet.append_row(attempt_data)