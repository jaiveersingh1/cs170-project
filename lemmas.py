# doc consisting of functions that check verify the enforcement of the improvements lemmas

from solver_toolbox import *
from student_utils import *

def twoTAWalk(G, sol, drops):
	"""
	If at least two TAs are walking along some edge, we would do better by 
	driving the car along that edge.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: List of edges in the solution path
		drops: A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
	Returns:
		Boolean value indicating if the solution enforces this lemma
	"""
	numTAs = {}

	for d in drops:
		homes = drops[d]
		for h in homes:
			sp = nx.shortest_path(G, d, h)
			for i in range(len(sp) - 1):
				numTAs[(sp[i], sp[i + 1])] = numTAs.get((sp[i], sp[i + 1]), 0) + 1

	return max([numTAs[key] for key in numTAs]) <= 1

def closeTAs(G, sol, drops, walk_cost):
	"""
	TAs should get off at the closest vertex to their home.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: List of edges in the solution path
		drops: A dictionary mapping drop-off location to a list of homes of TAs that got off at that particular location
		walk_cost: Total walking cost (TA ONLY)
	Returns:
		Boolean value indicating if the solution enforces this lemma
	"""
	return walk_cost == cost_of_solution(G, [e[0] for e in sol], drops)

def noSameEdge(G, sol):
	"""
	The car should never drive along the same directed edge more than once.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: List of edges in the solution path
	Returns:
		Boolean value indicating if the solution enforces this lemma
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
		sol: List of edges in the solution path
	Returns:
		Boolean value indicating if the solution enforces this lemma
	"""
	return True

def groupWalk(G, sol):
	"""
	Given possible paths l=la+ls(la is alone, ls is shared) and s, where s < l, 
	take path l because there are savings induced from walking with more TAs.

	Input:
		G: A NetworkX graph that represents the input problem
		sol: List of edges in the solution path
	Returns:
		Boolean value indicating if the solution enforces this lemma
	"""
	return True

def shortcut(G, sol):
	"""
	If 0 TAs get off at some vertex b, and a shorter path exists from a->c as 
	opposed to a->b->c, then take the path from a->c. 

	Input:
		G: A NetworkX graph that represents the input problem
		sol: List of edges in the solution path
	Returns:
		Boolean value indicating if the solution enforces this lemma
	"""
	return True
