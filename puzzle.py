import subprocess


class Puzzle(object):
	def __init__(self, puzzle_id, name, instructions, app_path):
		self.puzzle_id = puzzle_id
		self.name = name
		self.instructions = instructions
		self.app_path = app_path
		
		self.attempts = []  # list of PuzzleAttempt

	@property
	def ordered_attempts(self):
		"""
		A property of Puzzle that chooses the highest scores for each player, then orders the list 
		by score.
		
		Returns a list of PuzzleAttempts ordered from highest to lowest (distincly by teamname 
		favoring the highest score).
		"""
		# Find the highest score for each player (teamname)
		highest_scores = dict()  # Dict format (string:PuzzleAttempt)
		for attempt in self.attempts:
			# Ensure a baseline score for this player has been established
			if attempt.teamname not in highest_scores.keys():
				highest_scores[attempt.teamname] = PuzzleAttempt('', '', 0)
			
			# See if this score is better that the previous highest
			if attempt.score > highest_scores[attempt.teamname].score:
				# New high score found
				highest_scores[attempt.teamname] = attempt
				
		# Order the scores
		return sorted(highest_scores.values(), key = lambda attempt: attempt.score, reverse=True)


class PuzzleAttempt(object):
	''' Represents an attempt at solving the puzzle '''
	
	def __init__(self, solution_filepath, teamname, score):
		self.solution_filepath = solution_filepath
		self.teamname = teamname
		self.score = score

		
class PuzzleManager(object):
	def __init__(self):
		# Initialize list of puzzles
		self.puzzles = []

		puzzle_id = 'prob1e'
		name = 'First Test Puzzle (Easy)'
		instructions = '''<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>
			<br/>
			<div><a href="prob1m">Medium version</a></div>
			<div><a href="prob1h">Hard version</a></div>
			<br/>
			<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>'''
		app_path = 'puzzles/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, name, instructions, app_path)
		self.puzzles.append(puzzle)

		puzzle_id = 'prob1m'
		name = 'First Test Puzzle (Medium)'
		instructions = '''<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>
			<br/>
			<div><a href="prob1e">Easy version</a></div>
			<div><a href="prob1h">Hard version</a></div>
			<br/>
			<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>'''
		app_path = 'puzzles/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, name, instructions, app_path)
		self.puzzles.append(puzzle)

		puzzle_id = 'prob1h'
		name = 'First Test Puzzle (Hard)'
		instructions = '''<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>
			<br/>
			<div><a href="prob1e">Easy version</a></div>
			<div><a href="prob1m">Medium version</a></div>
			<br/>
			<div>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.</div>'''
		app_path = 'puzzles/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, name, instructions, app_path)
		self.puzzles.append(puzzle)

		puzzle_id = 'prob2'
		name = 'Second Test Puzzle'
		instructions = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.'''
		app_path = 'puzzles/TestPuzzle1.exe'
		puzzle = Puzzle(puzzle_id, name, instructions, app_path)
		self.puzzles.append(puzzle)
		
		# TODO Read puzzles from storage
	
	def get_puzzle(self, puzzle_id):
		for puzzle in self.puzzles:
			if puzzle.puzzle_id == puzzle_id:
				return puzzle
		return None
		
	def record_attempt(self, puzzle_id, solution_filepath, teamname, score):
		attempt = PuzzleAttempt(solution_filepath, teamname, score)
		puzzle = self.get_puzzle(puzzle_id)
		puzzle.attempts.append(attempt)
		return attempt

	@staticmethod
	def score_attempt(app_path, solution_filepath):
		"""
		Runs the puzzle's external application and passes the solution file as the
		only parameter.  Stdout is returned from the app containing the score.
		"""
		score = subprocess.check_output([app_path, solution_filepath])
		return int(score)
		
		
