import pygame
import random


class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self, x, img):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.img = img
        self.PIPE_TOP = pygame.transform.flip(img, False, True)
        self.PIPE_BOTTOM = img
        self.passed = False
        self.set_height()

    def move(self):
        self.x -= self.VEL

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird, win):

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bot_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bot_offset = (self.x - bird.x, self.bottom - round(bird.y))

        return  bird_mask.overlap(bot_mask, bot_offset) or bird_mask.overlap(top_mask,top_offset)
    