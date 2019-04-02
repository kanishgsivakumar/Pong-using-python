import pygame
from objects import *

clock = pygame.time.Clock()
# variables
WIN_WIDTH = 802
WIN_HEIGHT = 533
MAX_SCORE = 5
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY, 0, 32)
bg = pygame.image.load("res/bg.png")
bg_i =pygame.image.load("res/bg_i.png")
font = pygame.font.Font("res\digital-7.ttf",50)
start = font.render("Start",True,WHITE)
font_s = pygame.font.Font("res\digital-7.ttf",15)
f1 = font_s.render("Press F1 for Single player",True,pygame.Color(32,178,170))
f2 = font_s.render("Press F2 for Multi player",True,pygame.Color(32,178,170))
DONE = False
pause = False
FPS = 30
withAi = False
screen.blit(bg_i,(0,0))
screen.blit(f1,((WIN_WIDTH-start.get_width())/2,WIN_HEIGHT/2))
pygame.display.flip()
running = True






if withAi:
    left_player = Player(Directions.LEFT, 'COMP')
    right_player = Player(Directions.RIGHT, 'USER')
else:
    left_player = Player(Directions.LEFT, 'Left')
    right_player = Player(Directions.RIGHT, 'Right')
    
curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)

left_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.LEFT,withAi)
right_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.RIGHT)

rackets = pygame.sprite.Group()
rackets.add(left_racket)
rackets.add(right_racket)
stuff_to_draw = pygame.sprite.Group()
stuff_to_draw.add(left_racket)
stuff_to_draw.add(right_racket)
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
        '{} - {}'.format(left_player.score, right_player.score), True, WHITE)
    screen.blit(scoreline, (WIN_WIDTH / 2 - scoreline.get_width()/2, WIN_HEIGHT / 2 + scoreline.get_height()))
    pygame.display.update()
    


def game_over(screen, winner, left_paper, right_player):
    gray_overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pygame.draw.rect(gray_overlay, BLACK, [0, 0, WIN_WIDTH, WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay, (0, 0))
    game_over = font.render('{} Won !'.format(winner.name), True, WHITE)
    screen.blit(game_over, (WIN_WIDTH / 2 - game_over.get_width()/2, WIN_HEIGHT / 2 - 100))
    scoreline = font.render(
        '{} - {}'.format(left_player.score, right_player.score), True, WHITE)
    screen.blit(scoreline,(WIN_WIDTH/2 - scoreline.get_width()/2,WIN_HEIGHT/2 + scoreline.get_height(),))
    pygame.display.update()
    pygame.time.delay(2000)

while (not DONE)  :
    keys = pygame.key.get_pressed()
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
    if(pause):
        game_paused(screen,left_player,right_player)
        if keys[pygame.K_F8]:
            pygame.mixer.music.load("res/smb_pause.wav")
            pygame.mixer.music.play()
            pause = False
        
    else:
        pygame.event.pump()
        
        if keys[pygame.K_ESCAPE]:
            DONE = True
        if keys[pygame.K_UP]:
            right_racket.move_up()
        if keys[pygame.K_DOWN]:
            right_racket.move_down()
        if not withAi:
            if keys[pygame.K_w]:
                left_racket.move_up()
            if keys[pygame.K_s]:
                left_racket.move_down()
        else:
            if (curr_ball.get_y_val() < left_racket.get_y_val())and(curr_ball.get_x_val()<WIN_WIDTH/2):
                left_racket.move_up()
            elif (curr_ball.get_y_val() > left_racket.get_y_val())and(curr_ball.get_x_val()<WIN_WIDTH/2):
                left_racket.move_down()
            else:
                pass
        if keys[pygame.K_F7 ]:
            pygame.mixer.music.load("res/smb_pause.wav")
            pygame.mixer.music.play()
            pause = True
        stuff_to_draw.update()
        curr_ball.update()

        col_left, col_right = curr_ball.rect.colliderect(left_racket.rect), curr_ball.rect.colliderect(right_racket.rect)
        if col_right == 1 or col_left == 1:
            curr_ball.toggle_direction()
            curr_ball.hit()

        if curr_ball.get_x_val() <= 0:  # left border
            right_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)
        elif curr_ball.get_x_val() >= WIN_WIDTH:  # right border
            left_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)

        # Print scores
        font = pygame.font.Font("res\digital-7.ttf", 25)

        left_player_score = font.render(
            '{}'.format(left_player.score), True, (255, 255, 255))
        right_player_score = font.render(
            '{}'.format(right_player.score), True, (255, 255, 255))
        goal_text = font.render(
            '{}'.format(MAX_SCORE), True, (255, 255, 0))

        screen.blit(left_player_score, (WIN_WIDTH / 2 - 100, 10))
        screen.blit(right_player_score, (WIN_WIDTH / 2 + 100, 10))
        screen.blit(goal_text, (WIN_WIDTH / 2, 0))

        stuff_to_draw.draw(screen)
        curr_ball.draw(screen)

        if left_player.score >= MAX_SCORE:
            game_over(screen, left_player, left_player, right_player)
        elif right_player.score >= MAX_SCORE:
            game_over(screen, right_player, left_player, right_player)

        if left_player.score >= MAX_SCORE or right_player.score >= MAX_SCORE:
            DONE = True

        pygame.display.set_caption('Ping Pong '+ "Difficulty : "+str(clock.get_fps())[0:2])

        pygame.display.flip()
        clock.tick(FPS)
    
        

pygame.quit()
