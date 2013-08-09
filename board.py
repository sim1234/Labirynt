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
        #return [1, 1, 0, 0, 0]
        return [True, True, False, False, False]
    #class EmptyCell(object):
    #    pass
    
    def __init__(self, size_x, size_y, teleport=False):
        self.data = [[self.EmptyCell()]]
        self.clear(size_x, size_y)
        self.teleport = teleport
        
    def clear(self, size_x = None, size_y = None):
        if size_x == None:
            size_x = len(self.data) - 1
        if size_y == None:
            size_y = len(self.data[0]) - 1
        assert int(size_x) > 2 and int(size_y) > 2
        self.data = [[self.EmptyCell() for x in xrange(0, int(size_y + 1))] for x in xrange(0, int(size_x + 1))]

    def _d2i(self, direction):
        if direction == (0, -1): return 0
        if direction == (-1, 0): return 1
        if direction == (0, 1): return 2
        if direction == (1, 0): return 3
    
    def _i2d(self, number):
        if number == 0: return (0, -1)
        if number == 1: return (-1, 0)
        if number == 2: return (0, 1)
        if number == 3: return (1, 0)

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
            cell[self._d2i(c[2])] = False # obalenie sciany tej komorki
            self.save(px, py, cell)
        return px, py
    
    def _route(self, px, py, cell):
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        s_choices = []
        for d in directions:
            try:
                cell2 = self.access(px + d[0], py + d[1])
                if (not cell2[8]) and (not cell2[self._d2i(d) + 4]):
                    new_d = (d[0] * -1, d[1] * -1)
                    s_choices.append((px + d[0], py + d[1], new_d))
            except IndexError:
                pass
        if s_choices:
            random.shuffle(s_choices)
        return s_choices
    
   
                
                
    def _make(self, px, py):
        choices = []
        mtmp = 1
        while len(choices) or mtmp:
            mtmp = 0
            cell = self.access(px, py)
            
            if not cell[8]:
                choices += self._route(px, py, cell)
            cell[8] = True
            self.save(px, py, cell)
            px , py = self._break_wall(choices)
                
            
    def generate(self, px = None, py = None):
        if px == None:
            px = random.randint(0, len(self.data) - 2)
        if py == None:
            py = random.randint(0, len(self.data[0]) - 2)
        self._make(px, py)
        
    def draw(self, draw_line, cell_width = 10, cell_height = 10):
        sx, sy = len(self.data), len(self.data[0])
        x = 0
        while x < sx:
            y = 0
            while y < sy:
                cell = self.data[x][y]
                if cell[0] and x < sx - 1:
                    draw_line((cell_width * x, cell_height * y), (cell_width * (x + 1), cell_height * y))
                if cell[1] and y < sy - 1:
                    draw_line((cell_width * x, cell_height * y), (cell_width * x, cell_height * (y + 1)))
                y += 1
            x += 1
    
    
    
        
    
    def _solve_r(self, px, py, dpx, dpy):
        cell = self.access(px, py)
        if cell[8]:
            return
        cell[8] = True
        self.save(px, py, cell)
        for i in (0, 1, 2, 3):
            if not cell[i]:
                d = self._i2d(i)
                p2x, p2y = px + d[0], py + d[1]
                if p2x == dpx and p2y == dpy:
                    return [(px, py), (p2x, p2y)]
                r = self._solve_r(p2x, p2y, dpx, dpy)
                if r:
                    return [(px, py)] + r
     
    def _find_ways(self, px, py):#, exclude_direction = (0,0)):
        ways = []
        cell = self.access(px, py)
        if cell[8]:
            return []
        cell[8] = True
        self.save(px, py, cell)
        for i in (0, 1, 2, 3):
            if not cell[i]:
                d = self._i2d(i)
                p = (px + d[0], py + d[1], px, py)
                if not self.access(*p)[8]:
                    ways.append(p)
        return ways           
            
    def solve(self, draw_line, start_x = 0, start_y = 0, end_x = None, end_y = None):
        if end_x == None:
            end_x = len(self.data) - 2
        if end_y == None:
            end_y = len(self.data[0]) - 2
        self.access(start_x, start_y)
        self.access(end_x, end_y)
        px, py = start_x, start_y
        
        x = 0
        while x < len(self.data):
            y = 0
            while y < len(self.data[0]):
                self.data[x][y][4] = False
                y += 1
            x += 1

        choices = []
        mtmp = 1
        while len(choices) or mtmp:
            mtmp = 0
            cell = self.access(px, py)
            
            if not cell[8]:
                choices += self._find_ways(px, py)
            cell[8] = True
            self.save(px, py, cell)
            px , py = self._break_wall(choices)
        
        
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        s_choices = []
        for d in directions:
            try:
                cell2 = self.access(px + d[0], py + d[1])
                if (not cell2[8]) and (not cell2[self._d2i(d) + 4]):
                    new_d = (d[0] * -1, d[1] * -1)
                    s_choices.append((px + d[0], py + d[1], new_d))
            except IndexError:
                pass
        if s_choices:
            random.shuffle(s_choices)
        return s_choices
        
        
        
        
        
        
        
        
        #lpx, lpy = None, None
        #px, py = start_x, start_y
        #while not (px == end_x and py == end_y):
        #    ways = self._find_ways(px, py, lpx, lpy)
        #    
        #    
        #    lpx, lpy = px, py
        
        #w = self._solve_r(start_x, start_y, end_x, end_y)
        #print w
        #x = 1
        #while x < len(w):
        #    sx, sy = w[x - 1]
        #    ex, ey = w[x]
        #    sx, sy = sx * 10 + 4, sy * 10 + 4
        #    ex, ey = ex * 10 + 4, ey * 10 + 4
        #    draw_line((sx,sy),(ex,ey))
        #    x += 1
        
            
            
        
        
            

    

