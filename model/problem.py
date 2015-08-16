from problem_attempt import ProblemAttempt


class Problem(object):
	def __init__(self, data_mgr):
		self.data_mgr = data_mgr
		self.attempts = []  # list of ProblemAttempt

		self.prob_id = ''
		self.name = ''
		self.description = ''
		self.problem_file = ''
	
	def load(self, data):
		'''
		Check how the DataManager loads problem data if there is an issue here.
		'''
		# data[0] stores the puzzle id, which isn't needed here
		self.prob_id = data[1]
		self.name = data[2]
		self.description = data[3]
		self.problem_file = data[4]

		# Load problem attempts
		attempts_data = self.data_mgr.get_attempts_data()
		for attempt_data in attempts_data:
			attempt_problem_id = attempt_data[0]

			# Make sure this attempt is intended for this problem
			if attempt_problem_id == self.prob_id:
				attempt = ProblemAttempt()
				attempt.load(attempt_data)
				
				self.attempts.append(attempt)

	def get_best_attempts(self):
		"""
		Returns a list of best ProblemAttempts for each team ordered from highest to lowest.
		"""
		# Find the best attempt for each team
		best_attempts = dict()  # Dict format (string:ProblemAttempt)
		for attempt in self.attempts:
			# Only consider attempts that are valid
			if attempt.score < 0:
				continue

			# Ensure a baseline attempt for this team has been established
			if attempt.teamname not in best_attempts.keys():
				best_attempts[attempt.teamname] = ProblemAttempt()
			
			# See if this attempt has a higher score than the previous
			if attempt.score > best_attempts[attempt.teamname].score:
				# New best attempt found
				best_attempts[attempt.teamname] = attempt
				
		# Order the attempts by score (highest to lowest)
		best_attempts = sorted(best_attempts.values(), key = lambda attempt: attempt.score, reverse=True)
		return best_attempts

	def get_team_points(self):
		"""
		Returns the points scored by each team on this problem (structed as a list of 
		<teamname, points> pairs).

		The highest scoring team will be awarded 10 points, the next 9 points, and so on.  The 11th
		place team and lower will all receive 0 points.
		"""
		team_points_list = []
		best_attempts = self.get_best_attempts()  # best attempts are assumed to be pre-sorted highest-to-lowest

		points_at_position = 10  # Start with 10 points for the first position
		for position, attempt in enumerate(best_attempts):
			points_awarded = points_at_position

			team_points_list.append( (attempt.teamname, points_awarded) )

			# If the next score is the same as the current attempts score, grant them both the same
			# amount of points for tying.  Otherwise, update the points at position.
			if len(best_attempts) > (position + 1):
				if best_attempts[position + 1].score != attempt.score:
					points_at_position = max(10 - (position + 1), 0)				
			
		return team_points_list

