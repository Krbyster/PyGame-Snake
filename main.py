import pygame
import time
import random

# initializing --------------------------------------------------------------------------------------------------------

snakeSpeed = 15

windowX = 720
windowY = 480

black = pygame.Color(0,0,0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

fruitCount = 0
redFruitSpawned = 0
redFruits = []

# red fruit class ---------------------------------------------------------------------------------------------

class RedFruit:
    def __init__(self, screen, x, y, lifespan):
        self.screen = screen
        self.position = [x,y]
        self.rect = pygame.Rect(x, y, 10, 10)
        self.color = red
        self.lifespan = lifespan

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def age(self):
        # Decrease lifespan by 1
        self.lifespan -= 1

        # Check if lifespan has expired
        if self.lifespan <= 0:
            self.rect = "Fruit has expired"

    def is_collided_with_snake(self, snake_head):
        return self.position == snake_head

# pygame setup --------------------------------------------------------------------------------------------------------

pygame.init()

pygame.display.set_caption('Snake Tutorial Project')
gameWindow = pygame.display.set_mode((windowX, windowY))

fps = pygame.time.Clock()

snakePosition = [100,50]

# here is the position of the snakes 4 body segments
snakeBody = [[100,50], [90,50], [80,50], [70,50]]
fruitPosition = [random.randrange(1,(windowX//10))*10, random.randrange(1,(windowY//10))*10]
fruitSpawn = True

# snake starts pointing right
direction = 'RIGHT'
changeTo = direction

# score setup --------------------------------------------------------------------------------------------------------

score = 0

def showScore(choice, color, font, size):
    scoreFont = pygame.font.SysFont(font, size)
    scoreSurface = scoreFont.render("Score :"+str(score), True, color)
    scoreRectangle = scoreSurface.get_rect()
    gameWindow.blit(scoreSurface, scoreRectangle)

# game over --------------------------------------------------------------------------------------------------------

def gameOver():
    myFont = pygame.font.SysFont('times new roman', 50)

    gameOverSurface = myFont.render("Your Score is: " + str(score), True, red)
    gameOverRectangle = gameOverSurface.get_rect()

    # load the image
    image = pygame.image.load('squidward.jpg')
    imageRectangle = image.get_rect()

    # calculate the total width and height of the text and image
    imageWidth = imageRectangle.width
    textWidth = gameOverRectangle.width
    #totalWidth = max(gameOverRectangle.width, imageRectangle.width)
    totalHeight = gameOverRectangle.height + imageRectangle.height

    # calculate the x and y positions of the text and image
    textX = (windowX - textWidth) / 2
    imageX = (windowX - imageWidth) / 2
    y = (windowY - totalHeight) / 2

    # set the position of the text
    gameOverRectangle.x = textX
    gameOverRectangle.y = y

    # set the position of the image
    imageRectangle.x = imageX
    imageRectangle.y = y + gameOverRectangle.height

    # draw the text and the image on the screen
    gameWindow.blit(gameOverSurface, gameOverRectangle)
    gameWindow.blit(image, imageRectangle)
    pygame.display.flip()

    # close program after 2 seconds
    time.sleep(2)
    pygame.quit()
    quit()

# run the game ---------------------------------------------------------------------------------------------------------
while True:
    # key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                changeTo = 'UP'
            if event.key == pygame.K_DOWN:
                changeTo = 'DOWN'
            if event.key == pygame.K_LEFT:
                changeTo = 'LEFT'
            if event.key == pygame.K_RIGHT:
                changeTo = 'RIGHT'
    # change direction so long as turn is not 180 deg
    if changeTo == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if changeTo == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    # moving snake coordinates with input
    if direction == 'UP':
        snakePosition[1] -= 10
    if direction == 'DOWN':
        snakePosition[1] += 10
    if direction == 'LEFT':
        snakePosition[0] -= 10
    if direction == 'RIGHT':
        snakePosition[0] += 10

    # increase score when snake eats fruit
    snakeBody.insert(0, list(snakePosition))
    # when the snake collides with fruit...
    if snakePosition[0] == fruitPosition[0] and snakePosition[1] == fruitPosition[1]:
        score += 10
        fruitSpawn = False
    else:
        snakeBody.pop()
    # spawn new fruit after it is eaten
    if not fruitSpawn:
        # take note of tiles that have red fruits on them
        occupiedPositions = []
        for rf in redFruits:
            occupiedPositions.append(rf.position)
        fruitPosition = [random.randrange(1,(windowX//10)) *10, random.randrange(1,(windowY//10)) *10]
        # dont allow a fruit to spawn on a tile with a red fruit
        while fruitPosition in occupiedPositions:
            fruitPosition = [random.randrange(1, (windowX // 10)) * 10, random.randrange(1, (windowY // 10)) * 10]
        fruitSpawn = True
        fruitCount += 1
        redFruits.append(RedFruit(gameWindow,                               # screen
                                random.randrange(1, (windowX // 10)) * 10,  # x
                                random.randrange(1, (windowY // 10)) * 10,  # y
                                redFruitSpawned+2))                         # lifespan
        redFruitSpawned += 1

        # decrease fruit lifespans
        for rf in redFruits:
            rf.age()
            # removed expired red fruits
            if rf.lifespan <= 0:
                redFruits.remove(rf)

    gameWindow.fill(black)

    # draw the snake segments
    for pos in snakeBody:
        pygame.draw.rect(gameWindow, green, pygame.Rect(pos[0], pos[1], 10, 10))
    # draw the fruits
    pygame.draw.rect(gameWindow, white, pygame.Rect(fruitPosition[0], fruitPosition[1], 10, 10))
    for rf in redFruits:
        rf.draw()

    # check for game over
    # check if snake ran into wall
    if snakePosition[0] < 0 or snakePosition[0] > windowX -10:
        gameOver()
    if snakePosition[1] < 0 or snakePosition[1] > windowY -10:
        gameOver()
    # check if snake collided with red fruit
    for rf in redFruits:
        if rf.is_collided_with_snake(snakePosition):
            gameOver()
    # check if snake collided with self
    for block in snakeBody[1:]:
        if snakePosition[0] == block[0] and snakePosition[1] == block[1]:
            gameOver()

    # show score continuously
    showScore(1, white, 'times new roman', 20)
    # refresh screen
    pygame.display.update()
    # refresh rate
    extraSpeed = fruitCount//2
    fps.tick(snakeSpeed + extraSpeed)

