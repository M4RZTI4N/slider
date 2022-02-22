#\u001b[38;2;255;127;0m
#imports
from replit import clear
from getkey import getkey, keys
#classes
class Cell():
  def __init__(self,x,y,t):
    self.x = x
    self.y = y
    self.type = t
  def getX(self):
    return self.x
  def getY(self):
    return self.y
  def getType(self):
    return self.type
  def canMove(self):
    return not self.type == 'W' 
  def __str__(self):
    if self.type == '0':
      return "\u001b[38;2;63;63;63m"+"[]" + "\u001b[0m"
    elif self.type == 'W':
      return "\u001b[38;2;255;255;255m"+"[]" + "\u001b[0m"
    elif self.type == 'S':
      return "\u001b[38;2;0;255;255m"+"[]" + "\u001b[0m"
    elif self.type == 'E':
      return "\u001b[38;2;0;255;0m"+"[]" + "\u001b[0m"
class Lock(Cell):
  def __init__(self,x,y):
    super().__init__(x,y,'L')
    self.locked = True
  def unlock(self):
    self.locked = False
  def getLocked(self):
    return self.locked
  def canMove(self):
    return not self.locked
  def __str__(self):
    if self.locked:
      return "\u001b[38;2;255;0;0m"+"[]" + "\u001b[0m"
    else:
      return "\u001b[38;2;63;0;0m"+"[]" + "\u001b[0m"
class Key(Cell):
  def __init__(self,x,y):
    super().__init__(x,y,'K')
    self.lock = []
    self.used = False
  def addLock(self,lock):
    self.lock.append(lock)
  def canMove(self):
    self.used = True
    for l in self.lock:
      l.unlock()
    return True
  def __str__(self):
    if not self.used:
      return "\u001b[38;2;255;255;0m"+"[]" + "\u001b[0m"
    else:
      return "\u001b[38;2;63;63;0m"+"[]" + "\u001b[0m"
  
class Level():
  def __init__(self,file):
    self.grid = None
    self.finish = None
    self.start = None
    self.playerX = None
    self.playerY = None
    self.parseFile(file)
  def parseFile(self,file):
    self.grid = []
    keys={}
    locks={}
    
    with open(file,'r') as f:
      lines = f.readlines()
      
      for l in lines:
        row = []
        cells = l.split()
        for c in cells:
          if 'K' in c:
            newKey = Key(l.index(c),lines.index(l))
            num = c[1:]
            if num in keys.keys():
              keys[num].append(newKey)
            else:
              keys[num] = [newKey]
            row.append(newKey)
          elif 'L' in c:
            newLock = Lock(l.index(c),lines.index(l))
            num = c[1:]
            if num in locks.keys():
              locks[num].append(newLock)
            else:
              locks[num] = [newLock]
            row.append(newLock)
          else:
            newCell = Cell(l.index(c),lines.index(l),c)
            row.append(newCell)
            if c == 'S':
              self.start = newCell
              self.playerX = cells.index(c)
              self.playerY = lines.index(l)
            if c == 'E':
              self.finish = newCell
        self.grid.append(row)
      
    print(keys.keys())
    print(locks.keys())
    for key in keys.keys():
      for k in keys[key]:
        for l in locks[key]:
          k.addLock(l)
  def move(self,d):
    delta = {
      'w':[0,-1],
      'a':[-1,0],
      's':[0,1],
      'd':[1,0],
      keys.UP:[0,-1],
      keys.LEFT:[-1,0],
      keys.DOWN:[0,1],
      keys.RIGHT:[1,0],
    }
    if d in delta.keys():
      m = delta[d]
    else:
      m = None
      return None
    prevX = self.playerX
    prevY = self.playerY
    nextX = self.playerX + m[0]
    nextY = self.playerY + m[1]
    while 0 <= nextY < len(self.grid) and 0 <= nextX < len(self.grid[nextY])  and self.grid[nextY][nextX].canMove():
      prevX = nextX
      prevY = nextY
      nextX = prevX + m[0]
      nextY = prevY + m[1]
    self.playerX = prevX
    self.playerY = prevY
  def getFinished(self):
    return self.grid[self.playerY][self.playerX].getType() == 'E'
  def display(self):
    for y in range(len(self.grid)):
      for x in range(len(self.grid[y])):
        if x == self.playerX and y == self.playerY:
          print('██',end='')
        else:
          print(self.grid[y][x],end='')
      print()
class Game():
  def __init__(self,file_list):
    self.file_list = file_list
    self.activeLevel = 0
    self.levels = []
    for file in self.file_list:
      self.levels.append(Level(file))
    self.currentLevel = self.levels[0]
  def run(self):
    while self.activeLevel < len(self.levels):
      clear()
      self.currentLevel.display()
      k = getkey()
      self.currentLevel.move(k)
      if self.currentLevel.getFinished():
        self.activeLevel += 1
        if self.activeLevel <len(self.levels):
          self.currentLevel = self.levels[self.activeLevel]
          
    clear()
    self.currentLevel.display()
    print('You win!')
#main
def main():
  g = Game(['level1.txt','level2.txt','level3.txt'])
  g.run()
main()