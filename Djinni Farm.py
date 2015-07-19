import pygame as pg
import time as t
from random import randint, choice
from math import sin, cos, radians
import sys

class Djinn:
    def __init__(self, name, element):
        self.name = name
        self.element = element
        self.health = 100
        self.hunger = 0
        self.happiness = 100
        self.hatred = 0
        self.t0 = t.time()
        self.radius = 30
        self.pos = [960, 360]
        self.speed = 0
        self.angle = 0

    def move(self):
        movement = randint(1,60)
        if movement == 1:
            self.speed += randint(-1, 1)
        elif movement == 2:
            self.speed += -1
            self.angle += choice((-30, 30))
        elif movement == 3:
            self.speed += 1
        elif movement == 4:
            self.angle += choice((-30, 30))
            self.speed -= 1
        elif movement == 5:
            self.speed += 1
        else:
            self.angle += randint(-5, 5)
        if self.angle > 360: self.angle -= 360
        elif self.angle < 0: self.angle += 360
        if self.speed > 5: self.speed = 5
        if self.speed < -1: self. speed = -1
        dx = sin(radians(self.angle))
        dy = cos(radians(self.angle))
        self.pos[0] += int(dx * self.speed)
        self.pos[1] -= int(dy * self.speed)
        if self.pos[0] < 720 + self.radius:
            self.pos[0] = 720 + self.radius
            self.angle *= -1
        elif self.pos[0] > 1200 - self.radius:
            self.pos[0] = 1200 - self.radius
            self.angle *= -1
        elif self.pos[1] < 80 + self.radius:
            self.pos[1] = 80 + self.radius
            self.angle *= -1
            self.angle += 180
        elif self.pos[1] > 640 - self.radius:
            self.pos[1] = 640 - self.radius
            self.angle *= -1
            self.angle += 180

    def get_hungry(self, timepassed):
        if self.speed > 0:
            self.hunger += (self.speed * timepassed)/4


    def get_bars(self):
        self.healthbar = 480 * (self.health / 100)
        self.hungerbar = 480 * (self.hunger / 100)
        self.happinessbar = 480 * (self.happiness / 100)
        self.hatredbar = 480 * (self.hatred / 100)

    def pass_time(self):
        self.t1 = t.time()
        timepassed = self.t1 - self.t0
        self.t0 = self.t1
        self.health -= timepassed * 0.1
        #self.hunger += timepassed
        self.happiness -= timepassed * 0.4
        self.get_hungry(timepassed)
        traits = ['health', 'hunger', 'happiness', 'hatred']
        for trait in traits:
            trait_value = getattr(self, trait)
            if trait_value > 100: setattr(self, trait, 100)
            elif trait_value < 0: setattr(self, trait, 0)


class GameInfrastructure:
    def __init__(self):
        self.CAPTION = 'DJINNI FARM!'
        self.SCREEN_SIZE = (1280,720)
        self.clock = pg.time.Clock()
        self.fps = 30
        pg.display.set_caption(self.CAPTION)
        self.screen = pg.display.set_mode(self.SCREEN_SIZE)
        self.home = pg.image.load('assets\home.png').convert()

        self.RED = (255,0,0)
        self.GREEN = (0,255,0)
        self.BLUE = (0,0,255)
        self.BLACK = (0, 0, 0)
        self.VENUSBROWN = (213, 169, 106)

    def event_handling(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(), sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.current_djinn.speed += 0.1
                elif event.key == pg.K_DOWN:
                    self.current_djinn.speed -= 0.1
                elif event.key == pg.K_LEFT:
                    self.current_djinn.angle -= 10
                elif event.key == pg.K_RIGHT:
                    self.current_djinn.angle += 10

    def update_djinn(self):
        self.current_djinn.move()

    def update_bars(self):
        self.current_djinn.pass_time()
        self.current_djinn.get_bars()

    def draw(self):
        self.screen.blit(self.home, (0,0))
        pg.draw.rect(self.screen, self.BLACK, ((80,360),(self.current_djinn.healthbar,40)))
        pg.draw.rect(self.screen, self.BLACK, ((80,440),(self.current_djinn.hungerbar,40)))
        pg.draw.rect(self.screen, self.BLACK, ((80,520),(self.current_djinn.happinessbar,40)))
        pg.draw.rect(self.screen, self.BLACK, ((80,600),(self.current_djinn.hatredbar,40)))
        pg.draw.circle(self.screen, self.VENUSBROWN, self.current_djinn.pos, self.current_djinn.radius)

    def update_screen(self):
        pg.display.flip()

    def prepare(self):
        self.current_djinn = Djinn('Flint', 'Venus')

    def main_loop(self):
        self.prepare()
        while True:
            self.event_handling()
            self.update_djinn()
            self.update_bars()
            self.draw()
            self.update_screen()
            self.clock.tick(self.fps)

GameInfrastructure().main_loop()