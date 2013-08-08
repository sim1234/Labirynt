import random


def ch(c): # [1,1,1,1,0,0,0,0,0]
    if c == (0,-1): return 0
    if c == (1, 0): return 1
    if c == (0, 1): return 2
    if c == (-1,0): return 3
##        self.bt = a[0] # borders
##        self.br = a[1]
##        self.bb = a[2]
##        self.bl = a[3]
##        self.sbt = a[4] # solidborders
##        self.sbb = a[5]
##        self.sbr = a[6]
##        self.sbl = a[7]
        

def norm(v, mn, mx, d = None): # Makes v in <mn, mx)
    if d == None:
        d = mx - mn
    while v < mn:
        v += d
    while v >= mx:
        v -= d
    return v

def fn():
    return [1,1,1,1,0,0,0,0,0]

class Board(object):
    def __init__(self, sx, sy, EmptyCell, grow=False, teleport=False):
        assert int(sx) > 2 and int(sy) > 2
        sx, sy = int(sx), int(sy)
        self.cell = EmptyCell
        self.m = [[self.cell() for x in xrange(0, int(sy))] for x in xrange(0, int(sx))]
        self.grow = bool(grow)
        self.tele = bool(teleport)


    def access(self, px, py):
        if self.tele:
            px = norm(px, 0, len(self.m))
            py = norm(py, 0, len(self.m[0]))
        else:
            if self.grow:
                while px < 0:
                    self.m.insert(0, [self.cell() for x in xrange(0, len(self.m[0]))])
                    px += 1
                while px >= len(self.m):
                    self.m.append([self.cell() for x in xrange(0, len(self.m[0]))])
                    px -= 1
                while py < 0:
                    for x in xrange(0, len(self.m)):
                        self.m[x].insert(0, self.cell())
                    py += 1
                while py >= len(self.m[0]):
                    for x in xrange(0, len(self.m)):
                        self.m[x].append(self.cell())
                    py -= 1
            else:
                #print px, py
                if px < 0 or px >= len(self.m) or py < 0 or py >= len(self.m[0]):
                    raise IndexError("Px or Py out of range!")
        return self.m[px][py]
        


    def step(self):
        t = [[False for x in xrange(len(self.m[0]))] for x in xrange(0, len(self.m))]
        for x in xrange(0, len(self.m)):
            for y in xrange(0, len(self.m[0])):
                c = self.CAN((x, y))
                s = self.m[x][y]
                if s:
                    s = c in self.stay
                else:
                    s = c in self.born
                t[x][y] = s
        self.m = t


def make(b, x, y):
    #print x,y
    j = b.access(x, y)
    if j[8]:
        return 
    else:
        j[8] = 1
    l = [(1,0), (-1,0), (0,1), (0,-1)]
    random.shuffle(l)
    t = []
    for n in l:
        try:
            r = b.access(x+n[0], y+n[1])
            if (not r[8]) and (not r[ch(n) + 4]):
                t.append((x+n[0], y+n[1], n, r, j))
        except IndexError:
            pass       
    for e in t:
        if not e[3][8]:
            tt = ch(e[2])
            j[tt] = 0
            tt += 2
            if tt >= 4:
                tt -= 4
            e[3][tt] = 0
        make(b, e[0], e[1])

def bre(t):
    e = t.pop()
    if not e[3][8]:
        tt = ch(e[2])
        e[4][tt] = 0 # obalenie sciany tej komorki
        tt += 2
        if tt >= 4:
            tt -= 4
        e[3][tt] = 0 # obalenie sciany drugiej komorki
        #e[3][8] = 1 # bylem tu
    return e[0], e[1]

def route(b, t, x, y, j):
    l = [(1,0), (-1,0), (0,1), (0,-1)]
    tm = []
    for n in l:
        try:
            r = b.access(x+n[0], y+n[1])
            if (not r[8]) and (not r[ch(n) + 4]):
                tm.append((x+n[0], y+n[1], n, r, j))
        except IndexError:
            pass
    if tm == []:
        return tm
    random.shuffle(tm)
    t.extend(tm)
    return tm

def make2(b, x, y):
    t = []
    mtmp = 1
    while len(t) or mtmp:
        mtmp = 0
        j = b.access(x, y)
        
        if j[8]:
            x , y = bre(t) 
        else:
            j[8] = 1
            route(b, t, x, y, j)     
            x , y = bre(t)
            
        
def genmaze(b):
    x = random.randint(0, len(b.m)-1)
    y = random.randint(0, len(b.m[0])-1)
    make2(b, x, y)
    #make(b, 5, 5)


    

