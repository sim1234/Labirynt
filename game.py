# coding: utf-8

import pygame
from pygame.locals import *
from board import Board, genmaze, fn



class game:
    def __init__(self, a_w, a_h):
        pygame.init()
        self.a_w = a_w
        self.a_h = a_h
        self.tryb = 1
        self.fps = 100
        self.keys = pygame.key.get_pressed()
        self.window = pygame.display.set_mode((a_w, a_h)) 
        pygame.display.set_caption("Labirynt") 
        self.screen = pygame.display.get_surface() 
        self.bufor = pygame.Surface((a_w,a_h))
        self.fpsclock = pygame.time.Clock()
        self.b = Board(20, 20, fn, 0, 0)
        genmaze(self.b)
    
    def printt(self, px, py, text, bit = None, size=10, color=(0,0,0), bgcolor=(200,200,200)):
        if bit == None:
            bit = self.bufor
        font = pygame.font.Font(pygame.font.match_font('doesNotExist,Arial'), size)
        text = font.render(text, True, color, bgcolor)
        textRect = text.get_rect()
        textRect.x = px
        textRect.y = py
        bit.blit(text, textRect)
    
    def endframe(self):
        events = pygame.event.get()
        self.keys = pygame.key.get_pressed()
        for event in events:
            if event.type == QUIT: self.tryb = 0
        
        if self.keys[K_BACKQUOTE]:
            self.printt(self.a_w-18, self.a_h-10, str(int(self.fpsclock.get_fps())))
        #if self.keys[K_g]:
        #    genmaze(self.b)

        self.screen.blit(self.bufor,(0,0))
        pygame.display.flip()
        self.bufor.fill((255,255,255))
        self.fpsclock.tick(self.fps)
        #pygame.time.wait(1)
    
    def play(self):
        while self.tryb:
            self.frame()
            self.endframe()

    def frame(self):
        rx = 10
        ry = 10
        c = (0,0,0)
        t = 2
        x = 0
        while x < len(self.b.m):
            y = 0
            while y < len(self.b.m[0]):
                o = self.b.m[x][y]
                if o[0]:
                    pygame.draw.line(self.bufor, c, (rx*x,ry*y), (rx*x+rx,ry*y), t)
                if o[1]:
                    pygame.draw.line(self.bufor, c, (rx*x+rx,ry*y), (rx*x+rx,ry*y+ry), t)
                if o[3]:
                    pygame.draw.line(self.bufor, c, (rx*x,ry*y), (rx*x,ry*y+ry), t)
                if o[2]:
                    pygame.draw.line(self.bufor, c, (rx*x,ry*y+ry), (rx*x+rx,ry*y+ry), t)
                y += 1
            x += 1
        #pygame.draw.circle(self.bufor, (255,0,0), (50,50), 0)

