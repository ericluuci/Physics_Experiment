# Eric Lu

import pygame
from pygame import *
import sys

def main():

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Super Crates - Eric Lu")

    timer = pygame.time.Clock()

    up = left = right = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#373830"))
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                       P",
        "P                       P",
        "P                       P",
        "P                PPPP   P",
        "P                       P",
        "P                       P",
        "P                       P",
        "P   PPPPPP              P",
        "P                       P",
        "P                       P",
        "P                       P",
        "P                       P",
        "P            PPPPPPPPPPPP",
        "P                       P",
        "P                       P",
        "P                       P",
        "P                       P",
        "PPPPPPPPPPPPPPPPPPPPPPPPP",]
    
    # build the level
    for row in level:
        for col in row:
            if (col == "P"):
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            x += 32
        y += 32
        x = 0

    entities.add(player)

    while True:
        timer.tick(60)
        for e in pygame.event.get():
            
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                up = True
            if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                left = True
            if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):
                right = True
            
            if e.type == KEYUP and (e.key == K_UP or e.key == K_w):
                up = False
            if e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d):
                right = False
            if e.type == KEYUP and (e.key == K_LEFT or e.key == K_a):
                left = False

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        # update player, draw everything else
        player.update(up, left, right, platforms)
        entities.draw(screen)

        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)

class Player(Entity):
    
    def __init__(self, x, y):
        
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = Surface((32,32))
        self.image.fill(Color("#ffffff"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self, up, left, right, platforms):
        
        if (up and self.onGround):
            self.yvel -= 10
            
        if left:
            self.xvel = -8
            
        if right:
            self.xvel = 8
            
        if not self.onGround:
            self.yvel += 0.3
            
            if (self.yvel > 100):
                self.yvel = 100
            
        if not(left or right):
            self.xvel = 0
            
        # increment in x direction
        self.rect.left += self.xvel
        
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        
        # increment in y direction
        self.rect.top += self.yvel
        
        # assuming we're in the air
        self.onGround = False;
        
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                
                if xvel > 0: # Collide Right
                    self.rect.right = p.rect.left
                if xvel < 0: # Collide Left
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom


class Platform(Entity):
    
    def __init__(self, x, y):
        
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.convert()
        self.image.fill(Color("#faff02"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

if __name__ == "__main__":
    main()
