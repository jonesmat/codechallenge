from problem_attempt import ProblemAttempt


class Problem(object):
	def __init__(self, prob_id, name, description):
		self.prob_id = prob_id
		self.name = name
		self.description = description

		self.attempts = []  # list of ProblemAttempt

	@property
	def ordered_attempts(self):
		"""
		A property of a Problem that chooses the highest scores for each team, then orders the 
		list by score.
		
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