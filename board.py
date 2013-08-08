import random



def norm(v, mn, mx, d = None): # Makes v in <mn, mx)
    if d == None:
        d = mx - mn
    while v < mn:
        v += d
    while v >= mx:
        v -= d
    return v




#
#         Dane:                                               Wynik:     
# 
#           0                                                   0
#         _______                                             _______
#        |                                                   |      |
#     1  |                                                1  |      |  3
#        |                                                   |______|
#
#                                                               2
#
#    0 - gorna scianka                                  0 - gorna scianka   
#    1 - lewa scianka                                   1 - lewa scianka 
#    2, 3 - twardosc kolejnych scianek                  2 - dolna scianka
#    4 - przetworzone                                   3 - prawa scianka
#                                                       4, 5, 6, 7 - twardosc kolejnych scianek
#                                                       8 - przetworzone
#
#



class Maze(object):
    
    def EmptyCell(self):
        return [1, 1, 0, 0, 0]
    #class EmptyCell(object):
    #    pass
    
    def __init__(self, size_x, size_y, teleport=False):
        assert int(size_x) > 2 and int(size_y) > 2
        self.data = [[self.EmptyCell() for x in xrange(0, int(size_y + 1))] for x in xrange(0, int(size_x + 1))]
        self.teleport = teleport

    def _d2i(self, direction):
        if direction == (0,-1): return 0
        if direction == (-1, 0): return 1
        if direction == (0, 1): return 2
        if direction == (1,0): return 3

    def _access(self, px, py):
        if self.teleport:
            px = norm(px, 0, len(self.data))
            py = norm(py, 0, len(self.data[0]))
        else:
            #if px < 0 or px >= len(self.data) or py < 0 or py >= len(self.data[0]):
            if px < 0 or py < 0:
                raise IndexError("Px or Py out of range! (%d, %d)" % (px, py))
        return self.data[px][py]
    
    def access(self, px, py):
        a = self._access(px, py) # main
        b = self._access(px, py + 1) # bottom
        c = self._access(px + 1, py) # right
        return [a[0], a[1], b[0], c[1], a[2], a[3], b[2], c[3], a[4] ]
    
    def save(self, px, py, state):
        a = self._access(px, py) # main
        b = self._access(px, py + 1) # bottom
        c = self._access(px + 1, py) # right
        a[0], a[1], b[0], c[1], a[2], a[3], b[2], c[3], a[4] = state
        
    def _break_wall(self, choices):
        c = choices.pop() # [px, py, direction]
        px, py = c[0], c[1]
        cell = self.access(px, py)
        if not cell[8]:
            cell[self._d2i(c[2])] = 0 # obalenie sciany tej komorki
            self.save(px, py, cell)
        return px, py
    
    def _route(self, x, y, cell):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        s_choices = []
        for d in directions:
            try:
                cell2 = self.access(x + d[0], y + d[1])
                if (not cell2[8]) and (not cell2[self._d2i(d) + 4]):
                    new_d = (d[0] * -1, d[1] * -1)
                    s_choices.append((x + d[0], y + d[1], new_d))
            except IndexError:
                pass
        if s_choices:
            random.shuffle(s_choices)
        return s_choices
    
   
                
                
    def _make(self, x, y):
        choices = []
        mtmp = 1
        while len(choices) or mtmp:
            mtmp = 0
            cell = self.access(x, y)
            
            if not cell[8]:
                choices += self._route(x, y, cell)
            cell[8] = 1
            self.save(x, y, cell)
            x , y = self._break_wall(choices)
                
            
    def genmaze(self):
        x = random.randint(0, len(self.data)-2)
        y = random.randint(0, len(self.data[0])-2)
        self._make(x, y)
        
    
            

    

