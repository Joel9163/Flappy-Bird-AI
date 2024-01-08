import pygame

class Bird:
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.tilt = 0 
        self.tick = 0
        self.vel = 0
        self.height = self.y
        self.img = img

    def jump(self):
        self.vel = -10.5
        self.tick = 0
        self.height = self.y

    def draw(self, win):
        r_img = pygame.transform.rotate(self.img, self.tilt)
        new_win = r_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(r_img, new_win.topleft)
    
    def move(self):
        self.tick  += 1
        delta = self.vel*(self.tick) + 1.5*(self.tick)**2

        #terminial velocity
        if delta > 14:
            delta = 16
            
        #To get bird to jump
        if delta < 0:
            delta -= 2

        self.y += delta
        
        if delta<0:
            self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

        

        
            