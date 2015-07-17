import subprocess


class Problem(object):
	def __init__(self, prob_id, name, instructions, app_path):
		self.prob_id = prob_id
		self.name = name
		self.instructions = instructions
		self.app_path = app_path
		
		self.attempts = []  # list of ProblemAttempt

	@property
	def ordered_attempts(self):
		"""
		A property of Problem that chooses the highest scores for each player, then orders the list 
		by score.
		
		Returns a list of ProblemAttempts ordered from highest to lowest (distincly by teamname 
		favoring the highest score).
		"""
		# Find the highest score for each player (teamname)
		highest_scores = dict()  # Dict format (string:ProblemAttempt)
		for attempt in self.attempts:
			# Ensure a baseline score for this player has been established
			if attempt.teamname not in highest_scores.keys():
				highest_scores[attempt.teamname] = ProblemAttempt('', '', 0)
			
			# See if this score is better that the previous highest
			if attempt.score > highest_scores[attempt.teamname].score:
				# New high score found
				highest_scores[attempt.teamname] = attempt
				
		# Order the scores
		return sorted(highest_scores.values(), key = lambda attempt: attempt.score, reverse=True)


class ProblemAttempt(object):
	''' Represents an attempt at solving the problem '''
	
	def __init__(self, output_filepath, teamname, score):
		self.output_filepath = output_filepath
		self.teamname = teamname
		self.score = score

		
class ProblemManager(object):
	def __init__(self):
		# Initialize list of problems
		self.problems = []

		prob_id = 'prob1e'
		name = 'First Test Problem (Easy)'
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
		app_path = 'problem_apps/TestProblem1.exe'
		problem = Problem(prob_id, name, instructions, app_path)
		self.problems.append(problem)

		prob_id = 'prob1m'
		name = 'First Test Problem (Medium)'
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
		app_path = 'problem_apps/TestProblem1.exe'
		problem = Problem(prob_id, name, instructions, app_path)
		self.problems.append(problem)

		prob_id = 'prob1h'
		name = 'First Test Problem (Hard)'
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
		app_path = 'problem_apps/TestProblem1.exe'
		problem = Problem(prob_id, name, instructions, app_path)
		self.problems.append(problem)

		prob_id = 'prob2'
		name = 'Second Test Problem'
		instructions = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod 
			tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis 
			nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis 
			aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat 
			nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui 
			officia deserunt mollit anim id est laborum.'''
		app_path = 'problem_apps/TestProblem1.exe'
		problem = Problem(prob_id, name, instructions, app_path)
		self.problems.append(problem)
		
		# TODO Read problems from storage
	
	def get_problem(self, prob_id):
		for problem in self.problems:
			if problem.prob_id == prob_id:
				return problem
		return None
		
	def record_attempt(self, prob_id, output_filepath, teamname, score):
		attempt = ProblemAttempt(output_filepath, teamname, score)
		problem = self.get_problem(prob_id)
		problem.attempts.append(attempt)
		return attempt

	@staticmethod
	def score_attempt(app_path, output_filepath):
		"""
		Runs the problem's external application and passes the output file as the
		only parameter.  Stdout is returned from the app containing the score.
		"""
		score = subprocess.check_output([app_path, output_filepath])
		return int(score)
		
		
