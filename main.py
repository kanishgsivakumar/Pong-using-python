import pygame as pg 
from objects import *

clock = pg.time.Clock()
# variables
WIN_WIDTH = 802
WIN_HEIGHT = 533
MAX_SCORE = 5
DONE = False
pause = False
FPS = 30
withAi = False
welcome_screen = True
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(DISPLAY, 0, 32)
bg = pg.image.load("res/bg.png")
bg_i =pg.image.load("res/bg_i.png")
font = pg.font.Font("res\digital-7.ttf",100)
start = font.render("Start",True,WHITE)
font_s = pg.font.Font("res\digital-7.ttf",35)
f1 = font_s.render("  Press F1 for Single player",True,pg.Color(127,255,0))
f2 = font_s.render("  Press F2 for Multi player",True,pg.Color(127,255,0))
screen.blit(bg_i,(0,0))
screen.blit(f1,((WIN_WIDTH-f1.get_width())/2,WIN_HEIGHT/2))
screen.blit(f2,((WIN_WIDTH-f2.get_width())/2,WIN_HEIGHT/2+50))
pg.display.flip()
while welcome_screen:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            welcome_screen = False
            DONE = True

    else:
        pg.event.pump()
        if keys[pg.K_F1]:
            withAi= True
            welcome_screen = False
        if keys[pg.K_F2]:
            withAi = False
            welcome_screen = False

if withAi:
    left_player = Player(Directions.LEFT, 'COMP')
    right_player = Player(Directions.RIGHT, 'USER')
else:
    left_player = Player(Directions.LEFT, 'Left')
    right_player = Player(Directions.RIGHT, 'Right')
    
curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)

left_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.LEFT,withAi)
right_racket = Racket(screen, WIN_WIDTH, WIN_HEIGHT, Directions.RIGHT)

rackets = pg.sprite.Group()
rackets.add(left_racket)
rackets.add(right_racket)
stuff_to_draw = pg.sprite.Group()
stuff_to_draw.add(left_racket)
stuff_to_draw.add(right_racket)
def game_paused(screen,left_player,right_player):
    gray_overlay = pg.Surface((WIN_WIDTH,WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pg.draw.rect(gray_overlay,BLACK,[0,0,WIN_WIDTH,WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay,(0,0))
    game_paused =font.render(" Game Paused",True,WHITE)
    w,h = game_paused.get_size()
    screen.blit(game_paused,(WIN_WIDTH/2-w/2,WIN_HEIGHT/2-h/2))
    scoreline = font.render(
        '{} - {}'.format(left_player.score, right_player.score), True, WHITE)
    screen.blit(scoreline, (WIN_WIDTH / 2 - scoreline.get_width()/2, WIN_HEIGHT / 2 + scoreline.get_height()))
    pg.display.update()
    


def game_over(screen, winner, left_paper, right_player):
    gray_overlay = pg.Surface((WIN_WIDTH, WIN_HEIGHT))
    gray_overlay.fill(GRAY)
    gray_overlay.set_colorkey(GRAY)
    pg.draw.rect(gray_overlay, BLACK, [0, 0, WIN_WIDTH, WIN_HEIGHT])
    gray_overlay.set_alpha(99)
    screen.blit(gray_overlay, (0, 0))
    game_over = font.render('{} Won !'.format(winner.name), True, WHITE)
    screen.blit(game_over, (WIN_WIDTH / 2 - game_over.get_width()/2, WIN_HEIGHT / 2 - 100))
    scoreline = font.render(
        '{} - {}'.format(left_player.score, right_player.score), True, WHITE)
    screen.blit(scoreline,(WIN_WIDTH/2 - scoreline.get_width()/2,WIN_HEIGHT/2 + scoreline.get_height(),))
    pg.display.update()
    pg.time.delay(2000)

while (not DONE)  :
    keys = pg.key.get_pressed()
    screen.blit(bg,(0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            DONE = True
    if(pause):
        game_paused(screen,left_player,right_player)
        if keys[pg.K_F8]:
            pg.mixer.music.load("res/smb_pause.wav")
            pg.mixer.music.play()
            pause = False
        
    else:
        pg.event.pump()
        
        if keys[pg.K_ESCAPE]:
            DONE = True
        if keys[pg.K_UP]:
            right_racket.move_up()
            pg.mixer.music.load("res/smb_kick.wav")
            pg.mixer.music.play()
        if keys[pg.K_DOWN]:
            pg.mixer.music.load("res/smb_kick.wav")
            pg.mixer.music.play()
            right_racket.move_down()
        if not withAi:
            if keys[pg.K_w]:
                left_racket.move_up()
            if keys[pg.K_s]:
                left_racket.move_down()
        else:
            if (curr_ball.get_y_val() < left_racket.get_y_val())and(curr_ball.get_x_val()<WIN_WIDTH/2):
                left_racket.move_up()
            elif (curr_ball.get_y_val() > left_racket.get_y_val())and(curr_ball.get_x_val()<WIN_WIDTH/2):
                left_racket.move_down()
            else:
                pass
        if keys[pg.K_F7 ]:
            pg.mixer.music.load("res/smb_pause.wav")
            pg.mixer.music.play()
            pause = True
        stuff_to_draw.update()
        curr_ball.update()

        col_left, col_right = curr_ball.rect.colliderect(left_racket.rect), curr_ball.rect.colliderect(right_racket.rect)
        if col_right == 1 or col_left == 1:
            curr_ball.toggle_direction()
            curr_ball.hit()

        if curr_ball.get_x_val() <= 10:  # left border
            right_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)
        elif curr_ball.get_x_val() >= WIN_WIDTH-10:  # right border
            left_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)

        # Print scores
        font = pg.font.Font("res\digital-7.ttf", 100)

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
            if withAi:
                pg.mixer.music.load("res\smb_gameover.wav")
                pg.mixer.music.play()
            else:
                pg.mixer.music.load("res\smb_stage_clear.wav")
                pg.mixer.music.play()

            game_over(screen, left_player, left_player, right_player)
        elif right_player.score >= MAX_SCORE:
            pg.mixer.music.pygame.music.load("res\smb_stage_clear.wav")
            pg.mixer.music.pygame.music.play()
            game_over(screen, right_player, left_player, right_player)
        if left_player.score >= MAX_SCORE or right_player.score >= MAX_SCORE:
            DONE = True

        pg.display.set_caption('Pong')

        pg.display.flip()
        clock.tick(FPS)
    
        

pg.quit()
