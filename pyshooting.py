import random
from time import sleep
from typing import Any

import pygame
from pygame.locals import *

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 640

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

FPS = 60

# 파이썬3 - super().__init__() 
# 파이썬2 - super(해당 클래스,self).__init__() (파이썬3에서도 사용가능)

class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # super(Fighter, self).__init__()
        self.image = pygame.image.load('./resource/fighter.png')
        self.rect = self.image.get_rect()
        self.rect.x = int(WINDOW_WIDTH / 2)
        self.rect.y = WINDOW_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:  #
            self.rect.x -= self.dx 

        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
            
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super().__init__() # super(Missile, self).__init__()
        self.image = pygame.image.load("./resource/missile.png")
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound("./resource/missile.wav")

    def launch(self):
        self.sound.play()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite
            
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super().__init__() # super(Rock, self).__init__() # python version 3, 2
        rock_images = (
            "./resource/rock01.png",
            "./resource/rock02.png",
            "./resource/rock03.png",
            "./resource/rock04.png",
            "./resource/rock05.png",
            "./resource/rock06.png",
            "./resource/rock07.png",
            "./resource/rock08.png",
            "./resource/rock09.png",
            "./resource/rock10.png",
            "./resource/rock11.png",
            "./resource/rock12.png",
            "./resource/rock13.png",
            "./resource/rock14.png",
            "./resource/rock15.png",
            "./resource/rock16.png",
            "./resource/rock17.png",
            "./resource/rock18.png",
            "./resource/rock19.png",
            "./resource/rock20.png",
            "./resource/rock21.png",
            "./resource/rock22.png",
            "./resource/rock23.png",
            "./resource/rock24.png",
            "./resource/rock25.png",
            "./resource/rock26.png",
            "./resource/rock27.png",
            "./resource/rock28.png",
            "./resource/rock29.png",
            "./resource/rock30.png"
            )
        self.image = pygame.image.load(random.choice(rock_images))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    def update(self):
        self.rect.y += self.speed 

    def out_of_screen(self):
        if self.rect.y > WINDOW_HEIGHT:
            return True
        
# 메소드 설정
def draw_text(text, font, surface, x, y, main_color):
    text_obj  = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)

def occur_explosion(surface, x, y):
    explosion_image = pygame.image.load("./resource/explosion.png")
    explosion_rect = explosion_image.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_image, explosion_rect)

    explosion_sounds = ("./resource/explosion01.wav", "./resource/explosion02.wav", "./resource/explosion03.wav")
    explosion_sound = pygame.mixer.Sound(random.choice(explosion_sounds))
    explosion_sound.play()


# 게임 시작 진행 종료
def game_loop():
    default_font = pygame.font.Font("./resource/NanumGothic.ttf", 28)
    background_image = pygame.image.load("./resource/background.png")
    gameover_sound = pygame.mixer.Sound("./resource/gameover.wav")
    pygame.mixer.music.load("./resource/music.wav")
    pygame.mixer.music.play(-1) # 무한 반복
    fpss_clock = pygame.time.Clock()
    
    fighter = Fighter()
    missiles = pygame.sprite.Group()
    
    rocks = pygame.sprite.Group()

    occur_prob = 40
    shot_count = 0
    count_missed = 0
    
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    fighter.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    fighter.dx += 5
                elif event.key == pygame.K_UP:
                    fighter.dy -= 5
                elif event.key == pygame.K_DOWN:
                    fighter.dy += 5
                elif event.key == pygame.K_SPACE:
                    # global missile
                    missile = Missile(fighter.rect.centerx, fighter.rect.y, 10)
                    missile.launch()
                    missiles.add(missile)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighter.dx =  0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighter.dy =  0

            # X 눌렀을 때 종료
            if event.type == QUIT:
                pygame.quit()
                


        screen.blit(background_image, background_image.get_rect())

        occur_of_rocks = 1 + int(shot_count / 300)
        min_rock_speed = 1 + int(shot_count / 200)      
        max_rock_speed = 1 + int(shot_count / 100)

        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, WINDOW_WIDTH - 30), 0, speed)
                rocks.add(rock)

        draw_text("파괴한 운석: {}".format(shot_count), default_font, screen, 100, 20, YELLOW)
        draw_text("놓친 운석: {}".format(count_missed), default_font, screen, 400, 20, RED)

        for missile in missiles:
            rock = missile.collide(rocks)
            if rock:
                missile.kill()
                rock.kill()
                occur_explosion(screen, rock.rect.x, rock.rect.y)
                shot_count += 1
        
        for rock in rocks:
            if rock.out_of_screen():
                rock.kill()
                count_missed += 1

        rocks.update()
        rocks.draw(screen)
        missiles.update()  ############################################################
        missiles.draw(screen)
        fighter.update()
        fighter.draw(screen)
        pygame.display.flip()

        if fighter.collide(rocks) or count_missed >= 3:
            pygame.mixer_music.stop()
            occur_explosion(screen, fighter.rect.x, fighter.rect.y)
            pygame.display.update()
            gameover_sound.play()
            sleep(1)
            done =  True
        
        fpss_clock.tick(FPS)

    return "game_menu"

def game_menu():
    start_image = pygame.image.load("./resource/background.png")
    screen.blit(start_image, [0, 0])
    draw_x = int(WINDOW_WIDTH / 2)
    draw_y = int(WINDOW_WIDTH / 4)
    font_70 = pygame.font.Font("./resource/NanumGothic.ttf", 70)
    font_40 = pygame.font.Font("./resource/NanumGothic.ttf", 40)

    draw_text("지구를 지켜라~", font_70, screen, draw_x, draw_y, YELLOW)
    draw_text("엔터 키를 누르면", font_40, screen, draw_x, draw_y + 200, WHITE)
    draw_text("게임이 시작됩니다.", font_40, screen, draw_x, draw_y + 250, WHITE)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "play"
        if event.type == QUIT:
            return "quit"
        
    return "game_menu"


def main():
    global screen 

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("pyShooing")

    action = "game_menu"
    while action != "quit":
        if action == "game_menu":
            action = game_menu()
        elif action == "play":
            action = game_loop()
    
    pygame.quit()

if __name__ == "__main__":
    main()

