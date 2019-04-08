import pygame
WIN_WIDTH = 802
WIN_HEIGHT = 533
MAX_SCORE = 5
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (64, 64, 64)
pygame.init()
font = pygame.font.Font("res\digital-7.ttf",75)
font_m = pygame.font.Font("res\digital-7.ttf",50)
font_s = pygame.font.Font("res\digital-7.ttf",25)
bg = pygame.image.load("res/bg.png")
bg_i =pygame.image.load("res/bg_i.png")
