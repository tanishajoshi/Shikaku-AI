from Shikaku import *
from cs1graphics import *

class ShikakuVisualizer:
  def __init__(self, windowSize, showOptions=False):
    self._windowSize = windowSize
    self._showOptions = showOptions
    
  def setup(self, problem):
    self._problem = problem
    self._size = problem._size
    self._scale = self._windowSize/self._size
    
    self._canvas = Canvas(self._windowSize, self._windowSize)
    self._canvas.setAutoRefresh(False)
    self._canvas.setTitle('Shikaku')
    
    self._regionColor = [Color.randomColor() for _ in range(self._problem.numRegions())]
    
    self._squares = []
    for row in range(self._size):
      rowSq = []
      for col in range(self._size):
        s = Square(self._scale)
        s.move((col+.5)*self._scale, (row+.5)*self._scale)
        s.setBorderWidth(.01*self._scale)
        self._canvas.add(s)
        rowSq.append(s)
      self._squares.append(rowSq)
      
    for regionId in range(self._problem.numRegions()):
      (row, col) = self._problem.getRegionOrigin(regionId)
      s = self._problem.getRegionSize(regionId)
      
      t = Text(str(s))
      t.setFontSize(.5*self._scale)
      t.move((col+.5)*self._scale, (row+.5)*self._scale)
      t.setDepth(-5)
      self._canvas.add(t)
      
    self.draw(self._problem._known)
    
    if self._showOptions:
      self._optionsCanvas = Canvas(self._windowSize, self._windowSize)
      self._optionsCanvas.setAutoRefresh(False)
      self._optionsCanvas.setTitle('Options')
      
      for row in range(self._size):
        for col in range(self._size):
          s = Square(self._scale)
          s.move((col+.5)*self._scale, (row+.5)*self._scale)
          s.setBorderWidth(.01*self._scale)
          s.setDepth(-4)
          self._optionsCanvas.add(s)

        for regionId in range(self._problem.numRegions()):
          (row, col) = self._problem.getRegionOrigin(regionId)
          s = self._problem.getRegionSize(regionId)
          
          t = Text(str(s))
          t.setFontSize(.5*self._scale)
          t.move((col+.5)*self._scale, (row+.5)*self._scale)
          t.setDepth(-5)
          self._optionsCanvas.add(t)
                
      self._options = []
          
      self._optionsCanvas.refresh()
    else:
      self._optionsCanvas = None
          
          
          
  def draw(self, state, options=None):
    for row in range(self._size):
      for col in range(self._size):
        region = state[row,col]
        
        if region > -1:
          self._squares[row][col].setFillColor(self._regionColor[region])
        else:
          self._squares[row][col].setFillColor('white')
    
    self._canvas.refresh()
    
    if options and self._optionsCanvas:
      for o in self._options:
        self._optionsCanvas.remove(o)
      self._options = []
        
      for row in range(self._size):
        for col in range(self._size):
          regions = set()
          
          if state[row,col] > -1:
            s = Square(self._scale)
            s.setBorderWidth(0)
            s.move((col+.5)*self._scale, (row+.5)*self._scale)
            s.setFillColor(self._regionColor[state[row,col]])
            
            self._optionsCanvas.add(s)
            self._options.append(s)
            
            
          else:
            for (k,v) in options.items():
              for rectangle in v:
                if rectangle[0] <= row < rectangle[0]+rectangle[2] and rectangle[1] <= col < rectangle[1]+rectangle[3]:
                  regions.add(k)
                  
            regions = list(regions)
                    
            if len(regions) <= 4:
              sz = 2
            elif len(regions) <= 9:
              sz = 3
            elif len(regions) <= 16:
              sz = 4
            elif len(regions) <= 25:
              sz = 5
            elif len(regions) <= 36:
              sz = 6
            elif len(regions) <= 49:
              sz = 7
            elif len(regions) <= 64:
              sz = 8
            elif len(regions) <= 81:
              sz = 9
            elif len(regions) <= 100:
              sz = 10
            else:
              sz = 16
              
            for i, regionId in enumerate(regions): 
              s = Square(self._scale/sz)
              s.setBorderWidth(0)
              s.move(col*self._scale, row*self._scale)
              
              r = i // sz
              c = i % sz
              
              s.move( (c+.5)*self._scale/sz, (r+.5)*self._scale/sz )
              s.setFillColor(self._regionColor[regionId])
              
              self._optionsCanvas.add(s)
              self._options.append(s)
            
      self._optionsCanvas.refresh()
          
            
        
      
        
        
      
