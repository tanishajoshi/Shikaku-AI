from Shikaku import *
from time import *
import hashlib

class ShikakuSolver:
  def __init__(self, problem, maxTime, visualizer=None):
    self._problem = problem
    self._maxTime = maxTime
    self._time = time()
    self._visualizer = visualizer
    self._numExpansions = 0
    self._backTracks = 0
    
    if self._visualizer:
      self._visualizer.setup(self._problem)
    
  def timeRemaining(self):
    return time() < self._time + self._maxTime
    
  def solution(self):
    
    self._time = time()
    solution = self.solve()
    solutionTime = time() - self._time
    
    print('Solution key =', hashlib.md5(str(solution).encode()).hexdigest())
    print('Number of nodes expanded =', self._numExpansions)
    print('Number of backtracks =', self._backTracks)
    if self._numExpansions > 0:
      print('Search time per node =', solutionTime / self._numExpansions)
    print('Time =', solutionTime)
    
    return solution

  def solve(self, state=None):
    pass
    
  def getPuzzle(self):
    return self._problem
