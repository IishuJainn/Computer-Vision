import random
import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time


# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Balloon Escape")

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Images
imgBalloon1 = pygame.image.load('BalloonRed.png').convert_alpha()
rectBalloon1 = imgBalloon1.get_rect()
rectBalloon1.x, rectBalloon1.y = 500, 300

imgBalloon2 = pygame.image.load('BalloonGrey.png').convert_alpha()
rectBalloon2 = imgBalloon2.get_rect()
rectBalloon2.x, rectBalloon2.y = 500, 300

imgBalloon3 = pygame.image.load('BalloonBlack.png').convert_alpha()
rectBalloon3 = imgBalloon3.get_rect()
rectBalloon3.x, rectBalloon3.y = 500, 300

Bonus = pygame.image.load('Donut.png').convert_alpha()
BonusRect = Bonus.get_rect()
# To Hide the Bonus
BonusRect.x, BonusRect.y = 1300, 800

# Variables
speed = 15
score = 0
startTime = time.time()
totalTime = 60
lives = 5

# Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)


def resetBalloon(ballon):
    ballon.x = random.randint(100, img.shape[1] - 100)
    ballon.y = img.shape[0] + 50


# Main loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    timeRemain = int(totalTime -(time.time()-startTime))
    if timeRemain < 0 or lives == 0:
        window.fill((255,255,255))
        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Your Score: {score}', True, (50, 50, 255))
        if timeRemain < 0:
            textTime = font.render(f'Time UP', True, (50, 50, 255))
        else:
            textTime = font.render(f'Lives Over', True, (50, 50, 255))
        window.blit(textScore, (500, 350))
        window.blit(textTime, (530, 275))

    else:
        # OpenCV
        success, img = cap.read()
        img = cv2.flip(img, 1)
        hands, img = detector.findHands(img, flipType=False)

        rectBalloon1.y -= speed  # Move the balloon up
        rectBalloon2.y -= speed  # Move the balloon up
        rectBalloon3.y -= speed

        # Creating Bonus
        if timeRemain == 40 or timeRemain == 20:
            resetBalloon(BonusRect)
        BonusRect.y -=15

        # Move the balloon up
        # check if balloon has reached the top without pop
        if rectBalloon1.y < 0:
            score +=1
            resetBalloon(rectBalloon1)
            speed += 1
            pygame.mixer.music.load("score.wav")
            pygame.mixer.music.play()

        elif rectBalloon2.y < 0:
            score +=1
            resetBalloon(rectBalloon2)
            pygame.mixer.music.load("score.wav")
            pygame.mixer.music.play()
            # speed += 1

        elif rectBalloon3.y < 0:
            score +=1
            resetBalloon(rectBalloon3)
            pygame.mixer.music.load("score.wav")
            pygame.mixer.music.play()
            # speed += 1

        if hands:
            hand = hands[0]
            x, y = hand['lmList'][8][:2]
            if BonusRect.collidepoint(x,y):
                lives +=1
                pygame.mixer.music.load("point.wav")
                pygame.mixer.music.play()
                BonusRect.x, BonusRect.y = 1300, 800

            if rectBalloon1.collidepoint(x, y):
                resetBalloon(rectBalloon1)
                lives -=1
                pygame.mixer.music.load("Balloon burst.wav")
                pygame.mixer.music.play()
            if rectBalloon2.collidepoint(x, y):
                resetBalloon(rectBalloon2)
                lives -= 1
                pygame.mixer.music.load("Balloon burst.wav")
                pygame.mixer.music.play()
            if rectBalloon3.collidepoint(x, y):
                resetBalloon(rectBalloon3)
                lives -= 1
                pygame.mixer.music.load("Balloon burst.wav")
                pygame.mixer.music.play()

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        frame = pygame.transform.flip(frame, True, False)
        window.blit(frame, (0, 0))
        window.blit(imgBalloon1, rectBalloon1)
        window.blit(imgBalloon2, rectBalloon2)
        window.blit(imgBalloon3, rectBalloon3)
        window.blit(Bonus, BonusRect)

        font = pygame.font.Font(None, 50)
        textScore = font.render(f'Score: {score} Life :{lives}', True, (50, 50, 255))
        textTime = font.render(f'Time: {timeRemain}', True, (50, 50, 255))
        window.blit(textScore, (35, 35))
        window.blit(textTime, (1000, 35))
    # Update Display
    pygame.display.update()
    # Set FPS
    clock.tick(fps)