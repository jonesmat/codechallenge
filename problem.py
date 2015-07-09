

class Problem(object):
	def __init__(self, prob_id, name, instructions):
		self.prob_id = prob_id
		self.name = name
		self.instructions = instructions
		
		self.scores = []  # list of ProblemScores


class ProblemScore(object):
	def __init__(self, email, score):
		self.email = email
		self.score = score

		
class ProblemManager(object):
	def __init__(self):
		# Establish list of problems
		self.problems = [
			Problem('prob1', 'Problem 1', 'Do problem 1 stuff!'), 
			Problem('prob2', 'Problem 2', 'Do stuff for problem 2')
		]
		
		# Read problems from storage
	
	def get_problem(self, prob_id):
		for problem in self.problems:
			if problem.prob_id == prob_id:
				return problem
		return None
		
	def record_score(self, prob_id, email, score):
		score = ProblemScore(email, score)
		problem = self.get_problem(prob_id)
		problem.scores.append(score)

