

class Problem(object):
	def __init__(self, prob_id, name, instructions, app_path):
		self.prob_id = prob_id
		self.name = name
		self.instructions = instructions
		self.app_path = app_path
		
		self.attempts = []  # list of ProblemAttempt


class ProblemAttempt(object):
	''' Represents an attempt at solving the problem '''
	
	def __init__(self, email, score):
		self.email = email
		self.score = score

		
class ProblemManager(object):
	def __init__(self):
		# Establish list of problems
		self.problems = [
			Problem('prob1', 'Problem 1', 'Do problem 1 stuff!', '/path/to/prob1app'), 
			Problem('prob2', 'Problem 2', 'Do stuff for problem 2', '/path/to/prob2app')
		]
		
		# Read problems from storage
	
	def get_problem(self, prob_id):
		for problem in self.problems:
			if problem.prob_id == prob_id:
				return problem
		return None
		
	
		
	def record_attempt(self, prob_id, email, score):
		attempt = ProblemAttempt(email, score)
		problem = self.get_problem(prob_id)
		problem.attempts.append(attempt)
		return attempt

	@staticmethod
	def score_attempt(app_path, output_file):
		pass

	@staticmethod
	def get_highest_scoring_attempts(problem):
		''' 
		Choose the highest scores for each player, then order the list by
		score.
		
		Returns a list of ProblemAttempts ordered from highest to lowest (duplicate
		attempts are considered so that only the highest attempt is considered).
		'''
		# Find the highest score for each player (email)
		highest_scores = dict()  # Dict format (string:ProblemAttempt)
		for attempt in problem.attempts:
			# Ensure a baseline score for this player has been established
			if attempt.email not in highest_scores.keys():
				highest_scores[attempt.email] = ProblemAttempt('', 0)
			
			# See if this score is better that the previous highest
			if attempt.score > highest_scores[attempt.email].score:
				# New high score found
				highest_scores[attempt.email] = attempt
				
		# Order the scores
		return sorted(highest_scores.values(), key = lambda attempt: attempt.score, reverse=True)
		
		
