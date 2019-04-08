import pygame as pygame 
from constants import *
from objects import *

clock = pygame.time.Clock()
# variables
DONE = False
pause = False
loading = False
withAi = False
god_mode = False
welcome_screen = True
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY, 0, 32)


f1 = font_s.render("  Press F1 for Single player",True,pygame.Color(127,255,0))
f2 = font_s.render("  Press F2 for Multi player",True,pygame.Color(127,255,0))
screen.blit(bg_i,(0,0))
screen.blit(f1,((WIN_WIDTH-f1.get_width())/2,WIN_HEIGHT/2))
screen.blit(f2,((WIN_WIDTH-f2.get_width())/2,WIN_HEIGHT/2+50))
pygame.display.flip()
while welcome_screen:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            welcome_screen = False
            DONE = True

    else:
        pygame.event.pump()
        if keys[pygame.K_F1]:
            withAi= True
            welcome_screen = False
        if keys[pygame.K_F2]:
            withAi = False
            welcome_screen = False
        if keys[pygame.K_F3]:
            withAi = False
            god_mode = True
            welcome_screen = False

loading_screen(screen)
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



while (not DONE)  :
    keys = pygame.key.get_pressed()
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
    if(pause):
        game_paused(screen,left_player.score,right_player.score)
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
            pygame.mixer.music.load("res/smb_kick.wav")
            pygame.mixer.music.play()
        if keys[pygame.K_DOWN]:
            pygame.mixer.music.load("res/smb_kick.wav")
            pygame.mixer.music.play()
            right_racket.move_down()
        if not (withAi or god_mode):
            if keys[pygame.K_w]:
                pygame.mixer.music.load("res/smb_kick.wav")
                pygame.mixer.music.play()
                left_racket.move_up()
            if keys[pygame.K_s]:
                pygame.mixer.music.load("res/smb_kick.wav")
                pygame.mixer.music.play()
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

        if curr_ball.get_x_val() <= 10:  # left border
            right_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)
        elif curr_ball.get_x_val() >= WIN_WIDTH-10:  # right border
            left_player.score = 1
            curr_ball = Ball(screen, WIN_WIDTH, WIN_HEIGHT)

        # Print scores
        font = pygame.font.Font("res\digital-7.ttf", 100)

        left_score = font.render(
            '{}'.format(left_player.score), True, (0, 0, 255))
        right_score = font.render(
            '{}'.format(right_player.score), True, (255, 0, 0))
        goal_text = font.render(
            '{}'.format(MAX_SCORE), True,pygame.Color(127,255,0))

        screen.blit(left_score, ( 100-left_score.get_width()/2, 10))
        screen.blit(right_score, (WIN_WIDTH - 100 -right_score.get_width()/2, 10))
        screen.blit(goal_text, ((WIN_WIDTH-goal_text.get_width())/2, 0))

        stuff_to_draw.draw(screen)
        curr_ball.draw(screen)

        if left_player.score >= MAX_SCORE:
            if withAi:
                pygame.mixer.music.load("res\smb_gameover.wav")
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load("res\smb_stage_clear.wav")
                pygame.mixer.music.play()

            game_over(screen, left_player.name, left_player.score,right_player.score)
        elif right_player.score >= MAX_SCORE:
            pygame.mixer.music.load("res\smb_stage_clear.wav")
            pygame.mixer.music.play()
            game_over(screen, right_player.name, left_player.score, right_player.score)
        if left_player.score >= MAX_SCORE or right_player.score >= MAX_SCORE:
            DONE = True

        pygame.display.set_caption('Pong')

        pygame.display.flip()
        clock.tick(FPS)
    
        

pygame.quit()
