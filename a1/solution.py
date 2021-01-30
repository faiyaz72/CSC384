#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

  # Get all snowmans cordinates
  # Get distance cordinates
  # Compute and add
    snowballs = state.snowballs
    destination = state.destination
    distance = 0
    x0 = destination[0]
    y0 = destination[1]

    for snowball in snowballs:
      x1 = snowball[0]
      y1 = snowball[1]

      distance = distance + abs(x0 - x1) + abs(y0 - y1)

    return distance


#HEURISTICS
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    return 0

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.

    return (sN.hval * weight) + sN.gval

def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''

  # Get Search Engine running
  wrapped_fval_function = (lambda sN : fval_function(sN,weight))
  searchEngine = SearchEngine('custom')
  # searchEngine.trace_on(1)
  searchEngine.init_search(initial_state,snowman_goal_state,heur_fn,wrapped_fval_function)

  start = os.times()[0]

  searchResult = searchEngine.search(timebound)

  #search doc
  #timebound is a bound on the amount of time your code will execute the search. Once the run time exceeds the time bound, the search will stop; if no solution has been found, the search will return False.
  #costbound is an optional bound on the cost of each state s that is explored. The parameter costbound should be a 3-tuple (g bound,h bound,g + h bound). If a node's g val is greater than g bound, h val is greater than h bound, or g val + h val is greater than g + h bound, that node will not be expanded. You will use costbound to implement pruning in both of the anytime searches described below.

  end = os.times()[0] - start 
  costBoundTuple = (int(), int(), int())
  costSet = False

  while (end < timebound):
    if (searchResult == False):
      return searchResult
      
    if (searchResult.gval < costBoundTuple[0] or costSet == False):
      costSet = True
      costBoundTuple = (searchResult.gval, searchResult.gval, searchResult.gval)
      searchResult = searchEngine.search(timebound, costBoundTuple)
    end = os.times()[0] - start
    
  return searchResult

def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
  '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
  '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  return False

if __name__ == "__main__":
  len_benchmark = [44, 43, 20, 36, 35, 34, 18, 22, 34, 28, 32, 43, 35, -99, -99, 40, -99, -99, 46, -99]

  ##############################################################
  # TEST ANYTIME WEIGHTED A STAR
  print('Testing Anytime Weighted A Star')

  solved = 0; unsolved = []; benchmark = 0; timebound = 5 #time limit
  for i in range(0, len(PROBLEMS)):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i] #Final problems are hardest
    weight = 100 #we will start with a large weight so you can experiment with rate at which it decrements
    final = anytime_weighted_astar(s0, heur_fn=heur_manhattan_distance, weight=weight, timebound=timebound)

    if final:
      if i < len(len_benchmark):
        index = i
      else:
        index = 0
      if final.gval <= len_benchmark[index] or len_benchmark[index] == -99:
        benchmark += 1
      solved += 1
    else:
      unsolved.append(i)

  # s0 = PROBLEMS[3]
  # weight = 100 
  # final = anytime_weighted_astar(s0, heur_fn=heur_manhattan_distance, weight=weight, timebound=timebound)
  # if (final):
  #   print(final)

  print("\n*************************************")
  print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved, timebound))
  print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved, benchmark))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("The benchmark implementation solved {} out of the 20 practice problems given {} seconds.".format(15, timebound))
  print("*************************************\n")
