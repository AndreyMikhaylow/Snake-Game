import pygame, sys, random

# FPS
fps = pygame.time.Clock()

# colors
green = pygame.Color(0, 255, 0)
black = pygame.Color(0, 0, 0)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)
white = pygame.Color(255, 255, 255)

# snake speed
speed = 10

# background
background = pygame.image.load('images/background.jpg')
background = pygame.transform.scale(background, (1380, 840))

# window
width, height = 1380, 840
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# check errors
check_errors = pygame.init()

if check_errors[1] > 0:
    print('Error ' + check_errors[1])
else:
    print('Game successfully initialized')

# the initial size of the snake
square_size = 60


# init vars
def init_vars():
    global head_pos, food_pos, food_spawn, snake_body, direction, score
    direction = 'RIGHT'
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (width // square_size)) * square_size,
                random.randrange(1, (height // square_size)) * square_size]
    food_spawn = True
    score = 0


init_vars()


game_over = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # key binding
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord('w')
                    and direction != 'DOWN'):
                direction = 'UP'

            elif (event.key == pygame.K_DOWN or event.key == ord('s')
                  and direction != 'UP'):
                direction = 'DOWN'

            elif (event.key == pygame.K_LEFT or event.key == ord('a')
                  and direction != 'RIGHT'):
                direction = 'LEFT'

            elif (event.key == pygame.K_RIGHT or event.key == ord('d')
                  and direction != 'LEFT'):
                direction = 'RIGHT'

    # direction
    if direction == 'UP':
        head_pos[1] -= square_size

    elif direction == 'DOWN':
        head_pos[1] += square_size

    elif direction == 'LEFT':
        head_pos[0] -= square_size

    else:
        head_pos[0] += square_size

    if head_pos[0] < 0:
        head_pos[0] = width - square_size

    elif head_pos[0] > width - square_size:
        head_pos[0] = 0

    elif head_pos[1] < 0:
        head_pos[1] = height - square_size

    elif head_pos[1] > height - square_size:
        head_pos[1] = 0

    # eating
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # spawn_food
    if not food_spawn:
        food_pos = [random.randrange(width // square_size) * square_size,
                    random.randrange(height // square_size) * square_size]
        food_spawn = True

    # game
    game_screen.blit(background, (0, 0))
    for pos in snake_body:
        pygame.draw.rect(game_screen, green, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size - 2, square_size - 2))

    pygame.draw.rect(game_screen, red, pygame.Rect(
        food_pos[0], food_pos[1], square_size, square_size))

    # game over
    if game_over:
        game_screen.fill(black)
        font_score = pygame.font.SysFont('Verdana', 50)
        text_score = font_score.render('Score: ' + str(score), True, white)

        font_game_over = pygame.font.SysFont('Verdana', 80)
        text_game_over = font_game_over.render('Game Over', True, white)

        font_play_again = pygame.font.SysFont('Verdana', 60)
        text_play_again = font_play_again.render('Play Again', True, green)
        text_play_again_rect = text_play_again.get_rect(topleft=(525, 425))

        font_exit = pygame.font.SysFont('Verdana', 50)
        text_exit = font_exit.render('Exit', True, red)
        text_exit_rect = text_exit.get_rect(topleft=(630, 540))

        game_screen.blit(text_score, (575, 330))
        game_screen.blit(text_game_over, (465, 200))
        game_screen.blit(text_play_again, text_play_again_rect)
        game_screen.blit(text_exit, text_exit_rect)

        # restart_game
        mouse = pygame.mouse.get_pos()
        if text_play_again_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            direction = 'RIGHT'
            head_pos = [120, 60]
            snake_body = [[120, 60]]
            food_pos = [random.randrange(1, (width // square_size)) * square_size,
                        random.randrange(1, (height // square_size)) * square_size]
            food_spawn = True
            score = 0
            game_over = False

        # exit_game
        mouse = pygame.mouse.get_pos()
        if text_exit_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            break

    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            game_over = True

    pygame.display.flip()
    fps.tick(speed)
