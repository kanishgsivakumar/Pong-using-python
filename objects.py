import pygame
import random
from enum import Enum
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (64, 64, 64)

class Ball(pygame.sprite.Sprite):

    def __init__(self, screen, width, height):
        super().__init__()

        self.width, self.height = width, height
        self.direction = random.choice([Directions.DOWN_LEFT, Directions.DOWN_RIGHT, Directions.UP_LEFT, Directions.UP_RIGHT])
        self.screen = screen
        self.image = pygame.Surface([25, 25])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, [0, 0, 10, 10])
        self.rect = self.image.get_rect()
        self.position = (width/2,height/2)
        self.hits = 0
        self.speed_up = 1.0

    def draw(self, screen):
        pygame.draw.circle(screen,WHITE,self.position,5)
    def hit(self):
        self.hits += 1
        self.speed_up = 1.0+self.hits/10

    @property
    def position(self):
        return (self.rect.x, self.rect.y)

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def up_left(self):
        self.position = (self.position[0] - 10*self.speed_up, self.position[1] - 10*self.speed_up)

    def up_right(self):

        self.position = (self.position[0] + 10*self.speed_up, self.position[1] - 10*self.speed_up)

    def down_left(self):

        self.position = (self.position[0] - 10*self.speed_up, self.position[1] + 10*self.speed_up)

    def down_right(self):

        self.position = (self.position[0] + 10*self.speed_up, self.position[1] + 10*self.speed_up)

    def update(self):
        if self.position[1] <= 10:  # upper border
            self.direction = random.choice(
                [Directions.DOWN_LEFT, Directions.DOWN_RIGHT])
        if self.position[1] >= self.height - 10:  # bottom border
            self.direction = random.choice(
                [Directions.UP_LEFT, Directions.UP_RIGHT])

        options = {Directions.UP_LEFT: self.up_left,
                   Directions.UP_RIGHT: self.up_right,
                   Directions.DOWN_LEFT: self.down_left,
                   Directions.DOWN_RIGHT: self.down_right,
                   }
        options[self.direction]()

    def toggle_direction(self):
        if self.direction == Directions.DOWN_LEFT:
            new_direction = Directions.DOWN_RIGHT

        if self.direction == Directions.DOWN_RIGHT:
            new_direction = Directions.DOWN_LEFT

        if self.direction == Directions.UP_RIGHT:
            new_direction = Directions.UP_LEFT

        if self.direction == Directions.UP_LEFT:
            new_direction = Directions.UP_RIGHT

        try:
            self.direction = new_direction
        except NameError:
            pass

    def get_x_val(self):
        return self.rect.x

class Racket(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, side):
        super().__init__()

        self.width, self.height = width, height
        self.racket_height = 100
        self.movement_speed = 20
        offset = 20
        self.screen = screen
        self.image = pygame.Surface([10, self.racket_height])
        self.image.fill(WHITE)
        pygame.draw.rect(self.image, WHITE, [0, 0, 10, self.racket_height])
        self.rect = self.image.get_rect()
        print(side)
        if side is Directions.LEFT:
            self.position = (offset, self.height / 2)
        else:
            self.position = (self.width - offset - 10, self.height / 2)

    @property
    def position(self):
        return (self.rect.x, self.rect.y)

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def move_up(self):
        if self.position[1] > 0:
            self.position = (self.position[0], self.position[1] - self.movement_speed)

    def move_down(self):
        if self.position[1] + self.racket_height < self.height:
            self.position = (self.position[0], self.position[1] + self.movement_speed)



class Directions(Enum):
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = 1
    DOWN_RIGHT = 3
    LEFT = 4
    RIGHT = 6

class Player():

    def __init__(self, side, name):
        self.side = side
        self.points = 0
        self.name = name

    @property
    def score(self):
        return self.points

    @score.setter
    def score(self, val):
        self.points += val
