# coding: utf-8

import pygame
from board import *



class game:
    def __init__(self, a_w, a_h):
        pygame.init()
        #pygame.key.set_repeat(1, 1)
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
        #self.b = Board(20, 20, fn, 0, 0)
        #genmaze(self.b)
        self.b = Maze(9, 9, 0)
        #self.b.save(2,3, [0,0,0,0,0,0,0,0,0])
        self.b.generate()
    
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
            if event.type == pygame.QUIT:
                self.tryb = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_g:
                    self.b.clear()
                    self.b.generate()
                if event.key == pygame.K_c:
                    self.b.clear()
                if event.key == pygame.K_s:
                    self.b.solve(self.draw_line)
                
        
        if self.keys[pygame.K_BACKQUOTE]:
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


    def draw_line(self, (p1x, p1y), (p2x, p2y)):
        pygame.draw.line(self.bufor, (0,0,0), (p1x + 15, p1y + 15), (p2x + 15, p2y + 15), 2)


    def frame(self):
        self.b.draw(self.draw_line, 10, 10)



