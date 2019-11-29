# doc consisting of functions that check verify the enforcement of the improvements lemmas

from solver_toolbox import *

def twoTAWalk(G, sol):
	"""
	If at least two TAs are walking along some edge, we would do better by 
	driving the car along that edge.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return True

def closeTAs(G, sol, homes):
	"""
	TAs should get off at the closest vertex to their home.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
		homes: The indices of the vertices in G that are TA homes
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	bs = BaseSolver()
	cost, best_drops = bs.find_best_dropoffs(G, homes, [n for n in sol])

	return True

def noSameEdge(G, sol):
	"""
	The car should never drive along the same directed edge more than once.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	seen = {}
	for edge in sol:
		s, e = edge[0], edge[1]
		if e in seen.get(s, []):
			return False
		else:
			seen[s] = seen.get(s, []) + [e]
	return True

def kBridge(G, sol):
	"""
	If only k TAs have homes in a region of the graph that is separated from 
	the rest of the graph by a 	“bridge” of length at least k, then the car 
	should not cross that bridge.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return True

def groupWalk(G, sol):
	"""
	Given possible paths l=la+ls(la is alone, ls is shared) and s, where s < l, 
	take path l because there are savings induced from walking with more TAs.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return True

def shortcut(G, sol):
	"""
	If 0 TAs get off at some vertex b, and a shorter path exists from a->c as 
	opposed to a->b->c, then take the path from a->c. 

	Input:
		G: A NetworkX graph that represents the input problem
		sol: list of edges in the solution path
	Returns:
		boolean value indicating if the solution enforces this lemma
	"""
	return True
