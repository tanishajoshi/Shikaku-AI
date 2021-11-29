import copy
import numpy

class Shikaku:
  def __init__(self, size, locations):
    # Location is a list of (row, col, size)
    self._size = size   # Number of rows and columns
    
    self._known = -1 * numpy.ones((size,size), dtype=numpy.int8)
    
    self._numRegions = len(locations)
    
    self._regionSize = numpy.zeros( (self._numRegions,), dtype=numpy.int8 )
    self._regionOrigin = numpy.zeros( (self._numRegions, 2), dtype=numpy.int8)
    
    for regionId, (row, col, size) in enumerate(locations):
      self._regionSize[regionId] = size
      self._regionOrigin[regionId, 0] = row
      self._regionOrigin[regionId, 1] = col
      
      self._known[row,col] = regionId
      
  def getBoard(self):
    return self._known
    
  def setValue(self, row, col, value):
    self._known[row, col] = value
    
  def getValue(self, row, col, value):
    return self._known[row, col]
    
  def size(self):
    return self._size
    
  def numRegions(self):
    return self._numRegions
    
  def getRegionSize(self, regionId):
    return self._regionSize[regionId]
    
  def getRegionOrigin(self, regionId):
    # Return (row, col) of the initial square of the region
    return self._regionOrigin[regionId]
    
  def isGoal(self, board=None):
    if board is None:
      board = self._known
      
    # Should be filled in
    if numpy.min(board) == -1:
      return False
    
    # Each region should have to correct size
    for regionId, regionSize in enumerate(self._regionSize):
      if numpy.count_nonzero(board == regionId) != regionSize:
        return False
    
    return True
    
  def __str__(self):
    s = 'Region sizes\n'
    for regionId, regionSize in enumerate(self._regionSize):
      s += '%3d\t%3d\n' % (regionId, regionSize)
    s += '\n'
    
    s += '\nRegion origins\n'
    for row in range(self._size):
      for col in range(self._size):
        
        regionSize = -1
        for regionId in range(self._numRegions):
          if self._regionOrigin[regionId][0] == row and self._regionOrigin[regionId][1] == col:
            regionSize = self._regionSize[regionId]
            
        if regionSize > -1:
          s += '%3d ' % regionSize
        else:
          s += '  _ '
      s += '\n'
    
    s += '\nRegion ids\n'
    for row in range(self._size):
      for col in range(self._size):
        if self._known[row,col] > -1:
          s += '%3d ' % self._known[row,col]
        else:
          s += '  _ '
      s += '\n'
      
    return s
      
