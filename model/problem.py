from time import strptime
from problem_attempt import ProblemAttempt


class Problem(object):
	def __init__(self, data_mgr):
		self.data_mgr = data_mgr
		self.attempts = []  # list of ProblemAttempt

		self.prob_id = ''
		self.name = ''
		self.description = ''
		self.problem_file = ''

		self.low_score_is_best = True  # True, Lowest is best (like golf).  False, Highest score is
									   # best (like baseball).

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
		attempts_data = self.data_mgr.get_attempts_data(self.prob_id)
		for attempt_data in attempts_data:
			attempt = ProblemAttempt()
			attempt.load(attempt_data)
				
			self.attempts.append(attempt)

	def get_best_attempts(self):
		"""
		Returns a list of best ProblemAttempts for each team ordered from highest to lowest.
		"""
		# Find the best attempt for each team
		best_attempts_dict = dict()  # Dict format (string:ProblemAttempt)

		for attempt in self.attempts:
			# Only consider attempts that are valid
			if attempt.score < 0:
				continue

			# Ensure a baseline attempt for this team has been established
			if attempt.teamname not in best_attempts_dict.keys():
				best_attempts_dict[attempt.teamname] = ProblemAttempt()
			
			# See if this attempt has a lower score than the previous (lower is better)
			if self.low_score_is_best:
				if best_attempts_dict[attempt.teamname].score is None or \
					attempt.score < best_attempts_dict[attempt.teamname].score:
					# New lower scoring attempt found
					best_attempts_dict[attempt.teamname] = attempt
			else:
				if best_attempts_dict[attempt.teamname].score is None or \
					attempt.score > best_attempts_dict[attempt.teamname].score:
					# New higher scoring attempt found
					best_attempts_dict[attempt.teamname] = attempt

		# Order the attempts by score
		best_attempts = sorted(best_attempts_dict.values(), key = lambda attempt: \
			(attempt.score, attempt.timedata), reverse=(not self.low_score_is_best))

		# Assign points to the best attempts.
		# The best scoring team will be awarded 10 points, the next 9 points, and so on.  The 11th
		# place team and lower will all receive 0 points.
		best_attempts_with_points = []

		first_place_points = 10  # Start with 10 points for the first position
		for position, attempt in enumerate(best_attempts):
			points_awarded = max(first_place_points - position, 0)
			attempt.points_awarded = points_awarded

			best_attempts_with_points.append( attempt )

		return best_attempts_with_points
