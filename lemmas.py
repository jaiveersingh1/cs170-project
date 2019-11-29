# doc consisting of functions that check verify the enforcement of the improvements lemmas

def twoTAWalk(G, sol):
	"""
	If at least two TAs are walking along some edge, we would do better by 
	driving the car along that edge.

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true

def closeTAs(G, sol):
	"""
	TAs should get off at the closest vertex to their home.

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true

def noSameEdge(G, sol):
	"""
	The car should never drive along the same directed edge more than once.

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true

def kBridge(G, sol):
	"""
	If only k TAs have homes in a region of the graph that is separated from 
	the rest of the graph by a 	“bridge” of length at least k, then the car 
	should not cross that bridge.

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true

def groupWalk(G, sol):
	"""
	Given possible paths l=la+ls(la is alone, ls is shared) and s, where s < l, 
	take path l because there are savings induced from walking with more TAs.

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true

def shortcut(G, sol):
	"""
	If 0 TAs get off at some vertex b, and a shorter path exists from a->c as 
	opposed to a->b->c, then take the path from a->c. 

	Input:
		G - graph that represents the input problem
		sol - cycle that represents the outputted solution
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return true
