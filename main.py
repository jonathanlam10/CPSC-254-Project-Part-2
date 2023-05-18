#! /usr/bin/env python3
import pygame
import os
import random
import sys
import math
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Sound affects added for jump and duck motion for part 2 of project
JUMP_SOUND = pygame.mixer.Sound("jump_sound_effect.mp3")
MACHINE_SOUND = pygame.mixer.Sound("machine_sound_effect.mp3")

BackgroundColor = pygame.color.Color('#FA5F55')
MenuColor = pygame.color.Color('#89CFF0')

RUNNING = [pygame.image.load(os.path.join("assets/tank", "TankRun1.png")),
           pygame.image.load(os.path.join("assets/tank", "TankRun2.png"))]
JUMPING = pygame.image.load(os.path.join("assets/tank", "TankJump.png"))
DUCKING = [pygame.image.load(os.path.join("assets/tank", "TankDuck1.png")),
           pygame.image.load(os.path.join("assets/tank", "TankDuck2.png"))]

SMALL_OBS = [pygame.image.load(os.path.join("assets/cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assets/cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assets/cactus", "SmallCactus3.png"))]
LARGE_OBS = [pygame.image.load(os.path.join("assets/cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assets/cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assets/cactus", "LargeCactus3.png"))]

SMALL_METEOR = [pygame.image.load(os.path.join("assets/bear", "Bear0.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear1.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear2.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear3.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear4.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear5.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear6.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear7.png")),]
LARGE_METEOR = [pygame.image.load(os.path.join("assets/bear", "Bear0.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear1.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear2.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear3.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear4.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear5.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear6.png")),
                pygame.image.load(os.path.join("assets/bear", "Bear7.png")),]

BIRD = [pygame.image.load(os.path.join("assets/bird", "Bird1.png")),
        pygame.image.load(os.path.join("assets/bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("assets/other", "Cloud.png"))

BG = pygame.image.load(os.path.join("assets/other", "Track.png"))

BULLET = [ pygame.image.load(os.path.join("assets/other", "Rocket.png"))]


class Tank:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.tankDuck = False
        self.tankRun = True
        self.tankJump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.tankRect = self.image.get_rect()
        self.tankRect.x = self.X_POS
        self.tankRect.y = self.Y_POS

    def update(self, userInput):
        if self.tankDuck:
            self.duck()
        if self.tankRun:
            self.run()
        if self.tankJump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.tankJump:
            self.tankDuck = False
            self.tankRun = False
            self.tankJump = True
            JUMP_SOUND.play()
        elif userInput[pygame.K_DOWN] and not self.tankJump:
            self.tankDuck = True
            self.tankRun = False
            self.tankJump = False
            MACHINE_SOUND.play()
        elif not (self.tankJump or userInput[pygame.K_DOWN]):
            self.tankDuck = False
            self.tankRun = True
            self.tankJump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.tankRect = self.image.get_rect()
        self.tankRect.x = self.X_POS
        self.tankRect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.tankRect = self.image.get_rect()
        self.tankRect.x = self.X_POS
        self.tankRect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.tankJump:
            self.tankRect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.tankJump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.tankRect.x, self.tankRect.y))

"""
class Bullet:
    def __init__(self, x, y):
        self.image = BULLET
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel = 10

    def update(self):
        self.rect.x += self.vel

    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
"""
        
class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

# Horizontal Obstacles
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

# Vertical Obstacles
#  
# Have these obstacles come from the top of the screen, and despawn at BG (the track)
# Obstacles will descend, but maintain the speed of the tank, to make it seem like they are falling from the sky
class Obstacle2:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.y = 0

    def update(self):
        self.rect.y += game_speed / 4
        if self.rect.y > 380:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
        
class SmallMeteor(Obstacle2):
    def __init__(self, image):
        self.type = 0
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.x = 425

class LargeMeteor(Obstacle2):
    def __init__(self, image):
        self.type = 0
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.x = 400

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Tank()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    bullets = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            #fixed this as was not functionally correctly project part 2
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # bullet shot from tank (triggered by q key) that evaporates obstacles upon impact, granting 200 points each
            """
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    bullets.append(Bullet(BULLET))
                    for bullet in bullets:
                        bullet.draw(SCREEN)
                        bullet.update()
                        if bullet.rect.colliderect(obstacle.rect):
                            obstacles.pop()
                            points += 500
            """

        SCREEN.fill(BackgroundColor)
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 4) == 0:
                obstacles.append(SmallCactus(SMALL_OBS))
            elif random.randint(0, 4) == 1:
                obstacles.append(LargeCactus(LARGE_OBS))
            elif random.randint(0, 4) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 4) == 3:
                obstacles.append(SmallMeteor(SMALL_METEOR))
            elif random.randint(0, 4) == 4:
                obstacles.append(LargeMeteor(LARGE_METEOR))
                

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.tankRect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                sound = pygame.mixer.Sound("assets/audio/esm_8_bit_game_over_1_arcade_80s_simple_alert_notification_game.mp3")
                sound.play()
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill(MenuColor)
        font = pygame.font.Font('freesansbold.ttf', 30)
        #added this for a background music loop thorught the game
        music = pygame.mixer.music.load("war_music.mp3")
        pygame.mixer.music.play(-1)
        if death_count == 0:
            text = font.render("Tank Runner, Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            #fixed this as was not functionally correctly project part 2
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)