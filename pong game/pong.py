import random

import pygame
pygame.init()
clock = pygame.time.Clock()


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    ball.x = ball.x + ball_speed_x  # ball horizontal speed
    ball.y = ball.y + ball_speed_y  # ball vertical speed

    if ball.left <= 0:
        pygame.mixer.music.load('pong.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.load('gameover.mp3')
        pygame.mixer.music.play()
        player_score = player_score + 1
        score_time = pygame.time.get_ticks()
    if ball.right >= width:
        pygame.mixer.music.load('pong.wav')
        pygame.mixer.music.play()
        pygame.mixer.music.load('gameover.mp3')
        pygame.mixer.music.play()
        opponent_score = opponent_score + 1
        score_time = pygame.time.get_ticks()

    if ball.top <= 0 or ball.bottom >= height:
        pygame.mixer.music.load('pong.wav')
        pygame.mixer.music.play()
        ball_speed_y = ball_speed_y * (-1)  # reverse the vertical speed

    # collision with paddles and it is certain that ball is going to right
    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.music.load('pong.wav')
        pygame.mixer.music.play()

        # improving collision
        if abs(ball.right - player.left) < 10:
            ball_speed_x = ball_speed_x * (-1)
        if abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * (-1)
        if abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y = ball_speed_y * (-1)

    # collision with paddles and it is certain that ball is going to left
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.music.load('pong.wav')
        pygame.mixer.music.play()

        # improving collision
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x = ball_speed_x * (-1)
        if abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y = ball_speed_y * (-1)
        if abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y = ball_speed_y * (-1)


def player_animation():
    player.y = player.y + player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height


def opponent_animation():
    opponent.y = opponent.y + opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height


def ball_reset():
    '''It reset the ball in the center when ball hits the wall'''
    global ball_speed_x, ball_speed_y, score_time
    current_time = pygame.time.get_ticks()
    ball.center = (width/2, height/2)

    if current_time - score_time < 1000:
        number_three = font.render('3', False, light_grey)
        screen.blit(number_three, (width/2-10, height/2+40))

    if 1000 < current_time - score_time < 2000:
        number_two = font.render('2', False, light_grey)
        screen.blit(number_two, (width/2-10, height/2+40))

    if 2000 < current_time - score_time < 3000:
        number_one = font.render('1', False, light_grey)
        screen.blit(number_one, (width/2-10, height/2+40))

    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


# Game specific variables
FPS = 60
width = 800
height = 600
exit_game = False
game_over = False
score_time = True

# player
player_x = width-20
player_y = height/2 - 70
player_width = 10
player_height = 140
player_speed = 0

# Opponent
opponent_x = 10
opponent_y = height/2 - 70
opponent_width = 10
opponent_height = 140
opponent_speed = 0

# Ball
ball_x = width/2 - 15
ball_y = height/2 - 15
ball_width = 30
ball_height = 30
ball_speed_x = 7
ball_speed_y = 7

# Color
light_grey = (200, 200, 200)

# Score text
player_score = 0
opponent_score = 0
wining_score = 11
font = pygame.font.Font('freesansbold.ttf', 34)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('pong game')

player = pygame.Rect(player_x, player_y, player_width, player_height)
opponent = pygame.Rect(opponent_x, opponent_y, opponent_width, opponent_height)
ball = pygame.Rect(ball_x, ball_y, ball_width, ball_height)


def gameloop():
    global player_speed, opponent_speed, exit_game, game_over

    while not exit_game:
        if game_over:

            if player_score == wining_score:
                screen.fill('grey12')
                player_win = font.render('player 1 wins', False, light_grey)
                screen.blit(player_win, (width/2+20, height/2))

            if opponent_score == wining_score:
                screen.fill('grey12')
                opponent_win = font.render('player 2 wins', False, light_grey)
                screen.blit(opponent_win, (width/2-40, height/2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # when up / down key pressed (player)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player_speed = player_speed + 7
                    if event.key == pygame.K_UP:
                        player_speed = player_speed - 7

                # when up / down key released (player)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player_speed = player_speed - 7
                    if event.key == pygame.K_UP:
                        player_speed = player_speed + 7

                # when up / down key pressed (opponent)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        opponent_speed = opponent_speed + 7
                    if event.key == pygame.K_w:
                        opponent_speed = opponent_speed - 7

                # when up / down key released (opponent)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_s:
                        opponent_speed = opponent_speed - 7
                    if event.key == pygame.K_w:
                        opponent_speed = opponent_speed + 7

            ball_animation()
            player_animation()
            opponent_animation()

            if player_score == wining_score or opponent_score == wining_score:
                game_over = True

            screen.fill('grey12')
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            pygame.draw.ellipse(screen, light_grey, ball)
            pygame.draw.aaline(screen, light_grey, (width/2, 0), (width/2, height))

            if score_time:
                ball_reset()

            player_font = font.render(f'{player_score}', False, light_grey)
            screen.blit(player_font, (width/2+20, height/2))

            opponent_font = font.render(f'{opponent_score}', False, light_grey)
            screen.blit(opponent_font, (width / 2-40, height / 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameloop()