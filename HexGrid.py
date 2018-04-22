# hexagonal grid class

import pygame
from heapq import heappush, heappop

class HexTile:
   # constructor initialization
   def __init__(self, x=0, y=0, passable = True, neighbours = []):
      self._location = (x,y)
      self._passable = passable
      self._neighbours = []
   
   # get all neighbour tiles
   def GetNeighbours(self):
      return self._neighbours

   # add neighbour
   def AddNeighbour(self, coord):
      self._neighbours.append(coord)

   # get location
   def GetLocation(self):
      return self._location

class HexGrid:
   # constructor initialization
   def __init__(self, gridWidth=10, gridHeight=10):
      self._gridWidth = gridWidth          # width of the grid
      self._gridHeight = gridHeight        # height of the grid
      self._board = {}                     # the board is a dictionary with keys being the tile hex coordinate and values being the tiles itself
      self._neighbourShift = [(1,0),(1,1),(0,1),(-1,0),(-1,-1),(0,-1)] # defines the 1 shift from 1 tile to its neighbouring tiles      

   # calculate first postition (upper left corner)
   def GridToPixelPos(self, gridPos):
      x = gridPos[0]
      y = gridPos[1]
      return ((x * self._hexWidth + (y % 2) * self._hexWidth/2),(y * self._hexHeight * 3/4))

   # calculate HexCoord from GridPos
   def GridToHexCoord(self, gridPos):
      return (gridPos[0] + int((gridPos[1] + 1)/2),gridPos[1])

   # calculate GridPos from HexCoord
   def HexToGridPos(self, hexCoord):
      return (hexCoord[0] - int((hexCoord[1] + 1)/2),hexCoord[1])

   # calculate distance between two HexCoord
   def Distance(self, hexCoord1, hexCoord2):
      z1 = -1 * (hexCoord1[0] + hexCoord1[1])
      z2 = -1 * (hexCoord2[0] + hexCoord2[1])
      return max(abs(hexCoord2[0] - hexCoord1[0]), abs(hexCoord2[1] - hexCoord1[1]), abs(z2-z1))

   # create the grid
   def CreateGrid(self):
      # empty board
      self._board = {}

      # fill board with tiles
      for i in range(self._gridHeight):
         for j in range(self._gridWidth):
            tile = HexTile(j + int((i + 1)/ 2),i)
            self._board[tile.GetLocation()] = tile

      # find neighbours for each tile
      for key in self._board:
         curKey = key
         for shift in self._neighbourShift:
            neighbour = ((curKey[0]+shift[0]),(curKey[1]+shift[1]))
            if neighbour in self._board:
               self._board[curKey].AddNeighbour(neighbour)

   # find shortest path between 2 tiles
   def FindPath(self, start, goal):
      path = (self.Distance(start,goal),[start]) # initialize first path, a path to start and remaining distance from start to goal
      searched = []                            # list of already searched node
      openPaths = []                           # priority queue of currently available paths
      heappush(openPaths, path)                # push initial path to the queue

      while(len(openPaths) > 0):               # keep searching while openPaths is not empty
         curPath = heappop(openPaths)          # pop shortest distance path
         if curPath[1][-1] == goal:            # if the last node in the path is the goal, return path
            return curPath[1]

         searched.append(curPath[1][-1])                          # push processed node into the searched node list
         neighbours = self._board[curPath[1][-1]].GetNeighbours() # get all the neighbours of the last node in the path
         for neighbour in neighbours:
            if neighbour in searched:          # if neighbour is already searched, skip it
               continue
            newPath = curPath[1][:]            # new node, copy the path, append the new node, calculate distance, push to openpaths
            newPath.append(neighbour)
            heappush(openPaths,(len(newPath) + self.Distance(newPath[-1],goal),newPath))
      return [] # if there's no path, return an empty path
         

   # driver
   def Test(self):
      print("Hello world!")
      self.CreateGrid()

      # for visualization using pygame
      pygame.init()
      displaySurface = pygame.display.set_mode([640,480])
      tileSprite = pygame.image.load("Hex32x32.png")
      tileSprite.set_colorkey([0,0,0])
      tileSpriteHighlighted = pygame.image.load("HexHighlighted32x32.png")
      tileSpriteHighlighted.set_colorkey([0,0,0])
      tileWidth = tileSprite.get_width()
      tileHeight = tileSprite.get_height()

      # draw the grid
      for i in range(self._gridHeight):
         for j in range(self._gridWidth):
            displaySurface.blit(tileSprite, ((j * tileWidth + (i % 2) * tileWidth/2),(i * tileHeight * 3/4)))
      pygame.display.flip()

      # pygame main loop
      running = True
      while(running):
         # try using FindPath
         path = self.FindPath(self.GridToHexCoord((0,0)),self.GridToHexCoord((3,2)))
         # draw the path
         for node in path:
            gridPos = self.HexToGridPos(node)
            displaySurface.blit(tileSpriteHighlighted, ((gridPos[0] * tileWidth + (gridPos[1] % 2) * tileWidth/2),(gridPos[1] * tileHeight * 3/4)))
         pygame.display.flip()

         # handles closing with x 
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
               running = False
      pygame.quit()

if __name__ == "__main__":
   hexGrid = HexGrid()
   hexGrid.Test()