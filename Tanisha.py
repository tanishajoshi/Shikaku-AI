from numpy import int16, int8
from Shikaku import *
from ShikakuVisualizer import *
from Puzzles import *
from ShikakuSolver import *


class PartiallySolvedPuzzle:
  def __init__(self, board, options):
    self.board = board
    self.options = options    
    
class joshit(ShikakuSolver):
  def __init__(self, problem, maxTime, visualizer):
    ShikakuSolver.__init__(self, problem, maxTime, visualizer)
    
  def solve(self):
    
    # Setup the possible options
    options = {}
    for i in range(self._problem.numRegions()):
      # Build all possible rectangles of the correct size and add them to
      # the options for that region.  Note there are much better ways
      # to do this.
      size = self._problem.getRegionSize(i)
      rectangles = []
      for height in range(1, size+1):
        if size % height == 0:
          width = size // height          
          for row in range(0, self._problem.size() - height+1):
            for col in range(0, self._problem.size() - width+1):
              if row <= self._problem.getRegionOrigin(i)[0] < row + height:
                if col <= self._problem.getRegionOrigin(i)[1] < col + width:
                  if numpy.all(numpy.logical_or(self._problem._known == -1, self._problem._known==i)[row:row+height, col:col+width]):
                    rectangles.append( (row, col, height, width) )
              
      options[i] = rectangles
      
    root = PartiallySolvedPuzzle(copy.copy(self._problem._known), options)
      
    if self._visualizer:
      self._visualizer.draw(root.board)
      
    if self._problem.isGoal(root.board):  # We found the solution
      return root.board
    
    solution = self.backtrack(root)
    if solution is not None:
      return solution.board
    return None # Time is out, return nothing
  
  #return the largest region among the options
  def moveOrder(self, state):
    reordered = {}
    for regionNo in state.options.keys():
      rSize = self._problem.getRegionSize(regionNo)
      rId = regionNo
      if rSize in reordered:
        reordered[rSize].append(rId)
      else:
        reordered[rSize] = [rId]
    return reordered
  
  
  def backtrack(self, state):    
    if not self.timeRemaining():
      return None
      
    if self._problem.isGoal(state.board):  # We found the solution
      return state
      
    if self._visualizer:
      self._visualizer.draw(state.board, state.options)
  
    # Choose an region to fix
    # reorder according to sizes
      
    
    ordered = self.moveOrder(state)
    maxRegionSize = max(ordered.keys()) #return largest region size (key)
    
    regionIds = list(ordered[maxRegionSize]) 
    if regionIds: regionId = regionIds.pop()
    regionOptions = state.options.pop(regionId)
    #print("region options", regionOptions)
    self._numExpansions += 1
    
    for rectangle in regionOptions:
      # Check if this choice is consistent with selections
      # that have already been made.  It is consistent if every
      # square has either the region id or -1 in it.
      consistent = numpy.all(numpy.logical_or(state.board == -1, state.board==regionId)[rectangle[0]:rectangle[0]+rectangle[2], rectangle[1]:rectangle[1]+rectangle[3]])
      
      #pruning overlapping stuff idk
      overlap = numpy.any(numpy.logical_and(state.board >-1, state.board != regionId)[rectangle[0]:rectangle[0]+rectangle[2], rectangle[1]:rectangle[1]+rectangle[3]])
      
      if (not overlap):
        if consistent:
          newState = copy.deepcopy(state)
        
          for row in range(rectangle[0], rectangle[0]+rectangle[2]):
            for col in range(rectangle[1], rectangle[1]+rectangle[3]):
              newState.board[row,col] = regionId
            
          if self._visualizer:
            self._visualizer.draw(newState.board)
        
          solution = self.backtrack(newState)
          if solution is not None:
            return solution
          self._backTracks += 1
          
      return None           
    
