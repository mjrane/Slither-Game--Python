import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

head = pygame.image.load('/content/sample_data/snake.png')
appleimg = pygame.image.load("/content/sample_data/apple.png")
icon = pygame.image.load('/content/sample_data/icon.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
block_size = 20
FPS = 10
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)
direction = "right"
AppleThickness = 30


def snake(block_size, snakelist):
    if direction == "right":
        directed_head = pygame.transform.rotate(head, 270)
    elif direction == "left":
        directed_head = pygame.transform.rotate(head, 90)
    elif direction == "up":
        directed_head = head
    elif direction == "down":
        directed_head = pygame.transform.rotate(head, 180)
    gameDisplay.blit(directed_head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0],
                                              XnY[1], block_size, block_size])


def text_object(msg, color, size):
    if size == "small":
        textSurface = smallfont.render(msg, True, color)
    elif size == "medium":
        textSurface = medfont.render(msg, True, color)
    elif size == "large":
        textSurface = largefont.render(msg, True, color)
    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_object(msg, color, size)
    textRect.center = (display_width/2), (display_height/2)+y_displace
    gameDisplay.blit(textSurf, textRect)


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()
            if event.type is pygame.KEYDOWN:
                if event.key is pygame.K_c:
                    intro = False
                if event.key is pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of game is eating red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you grow",
                          black,
                          10)
        message_to_screen("If you run into edges or youself,you die!",
                          black,
                          50)
        message_to_screen("Press C to play and Q to Quit",
                          red,
                          180)
        pygame.display.update()
        clock.tick(15)


def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))
    randAppleY = round(random.randrange(0, display_height-AppleThickness))
    return randAppleX, randAppleY


def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0, 0])


def pause():
    message_to_screen("Paused", black, -100, "large")
    message_to_screen("Press C to continue, P to pause or Q to quit",
                      black, 25)
    pygame.display.update()

    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                quit()
            if event.type is pygame.KEYDOWN:
                if event.key is pygame.K_c:
                    paused = False
                elif event.key is pygame.K_q:
                    pygame.quit()
                    quit()
        #gameDisplay.fill(white)


def GameLoop():
    global direction
    direction = 'right'
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 10
    lead_y_change = 0

    randAppleX, randAppleY = randAppleGen()
    snakelist = []
    snakeLength = 1
    while not gameExit:
        if gameOver is True:
            message_to_screen("Game over.",
                              black,
                              -50,
                              size="large")
            message_to_screen("Press C to play again or Q to quit",
                              red,
                              50,
                              size="medium")
            pygame.display.update()
        while gameOver is True:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type is pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key is pygame.K_c:
                        GameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size/2
                    lead_y_change = 0

                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size/2
                    lead_y_change = 0

                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size/2
                    lead_x_change = 0

                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size/2
                    lead_x_change = 0
            elif event.key is pygame.K_p:
                    pause()

        if (lead_x+block_size > display_width or
                lead_x < 0 or
                lead_y+block_size > display_height or
                lead_y < 0):
            gameOver = True

        lead_x += lead_x_change
        gameDisplay.fill(white)
        lead_y += lead_y_change
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakelist.append(snakeHead)

        if len(snakelist) > snakeLength:
            del snakelist[0]
        snake(block_size, snakelist)
        for segment in snakelist[:-1]:
            if (segment is snakeHead):
                gameOver = True
        score(snakeLength-1)

        pygame.display.update()

        if (lead_x > randAppleX and
                lead_x < randAppleX+AppleThickness or
                lead_x+block_size > randAppleX and
                lead_x+block_size < randAppleX+AppleThickness):

            if (lead_y > randAppleY and
                    lead_y < randAppleY+AppleThickness or
                    lead_y+block_size > randAppleY and
                    lead_y+block_size < randAppleY+AppleThickness):
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)
    pygame.quit()
    quit()
game_intro()
GameLoop()
