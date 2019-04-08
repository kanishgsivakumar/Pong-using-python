import pygame
import random as random
from enum import Enum
from constants import *

def game_paused(screen,left_player,right_player):
    gray_overlay = pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pygame.draw.rect(gray_overlay,BLACK,[0,0,WIN_WIDTH,WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay,(0,0))
    game_paused =font.render(" Game Paused",True,WHITE)
    w,h = game_paused.get_size()
    screen.blit(game_paused,(WIN_WIDTH/2-w/2,WIN_HEIGHT/2-h/2))
    scoreline = font.render(
        '{} - {}'.format(left_player, right_player), True, WHITE)
    screen.blit(scoreline, (WIN_WIDTH / 2 - scoreline.get_width()/2, WIN_HEIGHT / 2 + scoreline.get_height()))
    pygame.display.update()
    
def loading_screen(screen):
    screen.blit(bg, (0, 0))
    info = font_s.render("Use W and S keys for right player ",True,(127,255,0))
    screen.blit(info, (WIN_WIDTH / 2 - info.get_width()/2, WIN_HEIGHT / 2 ))
    info2 = font_s.render("Use up and down keys for left player",True,(127,255,0))
    screen.blit(info2, (WIN_WIDTH / 2 - info2.get_width()/2, WIN_HEIGHT / 2 - 50))
    info2 = font_s.render("Use F7 to pause the game",True,(127,255,0))
    screen.blit(info2, (WIN_WIDTH / 2 - info2.get_width()/2, WIN_HEIGHT / 2 + 50))
    info2 = font_m.render("Loading ...",True,WHITE)
    screen.blit(info2, (25,75))

    pygame.display.update()
    pygame.time.delay(2000)
def game_over(screen, winner, left_player, right_player):
    gray_overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pygame.draw.rect(gray_overlay, BLACK, [0, 0, WIN_WIDTH, WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay, (0, 0))
    game_over = font.render('{} Won !'.format(winner), True, WHITE)
    screen.blit(game_over, (WIN_WIDTH / 2 - game_over.get_width()/2, WIN_HEIGHT / 2 - 100))
    scoreline = font.render(
        '{} - {}'.format(left_player, right_player), True, WHITE)
    screen.blit(scoreline,(WIN_WIDTH/2 - scoreline.get_width()/2,WIN_HEIGHT/2 + scoreline.get_height(),))
    pygame.display.update()
    pygame.time.delay(2000)

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
        pygame.draw.circle(screen,pygame.Color(127,255,0),self.position,5)
    def hit(self):
        self.hits += 1
        self.speed_up = 1.0+self.hits/10
        pygame.mixer.music.load("res/smb_fireball.wav")
        pygame.mixer.music.play(0)
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
        rdm = random.randint(0,10)
        if self.position[1] <= 10:  # upper border
            if self.direction == Directions.UP_RIGHT:
                if not(rdm == 10):
                    self.direction = Directions.DOWN_RIGHT    
                else:
                    self.direction = Directions.DOWN_LEFT
            else:
                if not(rdm == 10):
                    self.direction = Directions.DOWN_LEFT    
                else:
                    self.direction = Directions.DOWN_RIGHT

        if self.position[1] >= self.height - 10:  # bottom border
            if self.direction == Directions.DOWN_RIGHT:
                if not(rdm == 10):
                    self.direction = Directions.UP_RIGHT    
                else:
                    self.direction = Directions.UP_LEFT
            else:
                if not(rdm == 10):
                    self.direction = Directions.UP_LEFT    
                else:
                    self.direction = Directions.UP_RIGHT

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
    def get_y_val(self):
        return self.rect.y


class Racket(pygame.sprite.Sprite):

    def __init__(self, screen, width, height, side,Ai = False):
        super().__init__()

        self.width, self.height = width, height
        self.racket_height = 100
        self.movement_speed = 20
        offset = 20
        self.sound = 0
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
            pygame.mixer.music.load("res/smb_kick.wav")
            pygame.mixer.music.play(0)
    def get_y_val(self):
        return self.rect.y
        
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
