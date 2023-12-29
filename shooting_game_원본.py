import pygame
import os
import sys
import random
from time import sleep

# 게임 스크린 크기
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640

# 색 정의
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
YELLOW = (250, 250, 50)
RED = (250, 50, 50)

# 전역 변수
FPS = 60

# 전투기 객체
class Fighter(pygame.sprite.Sprite):
    def __init__(self):
        super(Fighter, self).__init__()
        self.image = pygame.image.load(resource_path('resource/fighter.png'))
        self.rect = self.image.get_rect()
        self.reset()

    # 전투기 리셋
    def reset(self):
        self.rect.x = int(SCREEN_WIDTH / 2)
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.dx = 0
        self.dy = 0

    # 전투기 업데이트
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x < 0 or self.rect.x + self.rect.width > SCREEN_WIDTH:
            self.rect.x -= self.dx

        if self.rect.y < 0 or self.rect.y + self.rect.height > SCREEN_HEIGHT:
            self.rect.y -= self.dy

    # 전투기 그리기
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # 전투기 충돌 체크
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 미사일 객체
class Missile(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Missile, self).__init__()
        self.image = pygame.image.load(resource_path('resource/missile.png'))
        self.sound = pygame.mixer.Sound(resource_path('resource/missile.wav'))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    # 미사일 발사
    def launch(self):
        self.sound.play()

    # 미사일 업데이트
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0 :
            self.kill()

    # 미사일 충돌 체크
    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_rect(self, sprite):
                return sprite

# 암석 객체
class Rock(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, speed):
        super(Rock, self).__init__()
        rock_images_path = resource_path('./resource.resource/rock')
        image_file_list = os.listdir(rock_images_path)
        self.image_path_list = [os.path.join(rock_images_path, file)
                                for file in image_file_list if file.endswith(".png")]
        choice_rock_path = random.choice(self.image_path_list)
        self.image = pygame.image.load(choice_rock_path)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed

    # 암석 업데이트
    def update(self):
        self.rect.y += self.speed

    # 암석 게임 화면
    def out_of_screen(self):
        if self.rect.y > SCREEN_HEIGHT:
            return True

# 게임 객체
class Game():
    def __init__(self):
        self.menu_image = pygame.image.load(resource_path('resource/background.png'))
        self.background_image = pygame.image.load(resource_path('resource/background.png'))
        self.explosion_image = pygame.image.load(resource_path('resource/explosion.png'))
        self.default_font = pygame.font.Font(resource_path('resource/NanumGothic.ttf'), 28)
        self.font_70 = pygame.font.Font(resource_path('resource/NanumGothic.ttf'), 70)
        self.font_30 = pygame.font.Font(resource_path('resource/NanumGothic.ttf'), 30)
        explosion_file = ('resource/explosion01.wav',
                          'resource/explosion02.wav',
                          'resource/explosion03.wav')
        self.explosion_path_list = [resource_path(file) for file in explosion_file]
        self.gameover_sound = pygame.mixer.Sound(resource_path('resource/gameover.wav'))
        pygame.mixer.music.load(resource_path('resource/music.wav'))

        self.fighter = Fighter()
        self.missiles = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()

        self.occur_prob = 40
        self.shot_count = 0
        self.count_missed = 0

        # 게임 메뉴 On/Off
        self.menu_on = True

    # 게임 이벤트 처리 및 조작
    def process_events(self):
        # 게임 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            # 메뉴 화면 이벤트 처리
            if self.menu_on:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        self.shot_count = 0
                        self.count_missed = 0
                        # 게임 메뉴 On/Off
                        self.menu_on = False
            # 게임 화면 이벤트 처리
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.fighter.dx -= 5
                    elif event.key == pygame.K_RIGHT:
                        self.fighter.dx += 5
                    elif event.key == pygame.K_UP:
                        self.fighter.dy -= 5
                    elif event.key == pygame.K_DOWN:
                        self.fighter.dy += 5
                    elif event.key == pygame.K_SPACE:
                        missile = Missile(self.fighter.rect.centerx, self.fighter.rect.y, 10)
                        missile.launch()
                        self.missiles.add(missile)
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.fighter.dx = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.fighter.dy = 0

        return False

    # 게임 로직 수행
    def run_logic(self, screen):
        # 운석 수와 속도 조절
        occur_of_rocks = 1 + int(self.shot_count / 300)
        min_rock_speed = 1 + int(self.shot_count / 200)
        max_rock_speed = 1 + int(self.shot_count / 100)

        # 랜덤 확률의 빈도로 수행
        if random.randint(1, self.occur_prob) == 1:
            # 운석 생성 및 생성된 운석만큼 점수 증가
            for i in range(occur_of_rocks):
                speed = random.randint(min_rock_speed, max_rock_speed)
                rock = Rock(random.randint(0, SCREEN_WIDTH - 30), 0, speed)
                self.rocks.add(rock)

        # 미사일 충돌 체크
        for missile in self.missiles:
            rock = missile.collide(self.rocks)
            if rock:
                self.occur_explosion(screen, rock.rect.x, rock.rect.y)
                self.shot_count += 1
                missile.kill()
                rock.kill()

        # 암석 화면 벗어남 체크
        for rock in self.rocks:
            if rock.out_of_screen():
                rock.kill()
                self.count_missed += 1

        # 암석과 충돌하거나 3번 이상 놓친 경우
        if self.fighter.collide(self.rocks) or self.count_missed >= 3:
            pygame.mixer_music.stop()
            self.occur_explosion(screen, self.fighter.rect.x, self.fighter.rect.y)
            self.gameover_sound.play()
            self.rocks.empty()
            self.fighter.reset()
            self.menu_on = True
            sleep(1)

    # 텍스트 그리기
    def draw_text(self, screen, text, font, x, y, color):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = x, y
        screen.blit(text_obj, text_rect)

    # 충돌 이벤트 발생
    def occur_explosion(self, screen, x, y):
        explosion_rect = self.explosion_image.get_rect()
        explosion_rect.x = x
        explosion_rect.y = y
        screen.blit(self.explosion_image, explosion_rect)
        pygame.display.update()

        explosion_sound = pygame.mixer.Sound(random.choice(self.explosion_path_list))
        explosion_sound.play()

    # 게임 메뉴 출력
    def display_menu(self, screen):
        screen.blit(self.menu_image, [0, 0])
        draw_x = int(SCREEN_WIDTH / 2)
        draw_y = int(SCREEN_HEIGHT / 4)
        self.draw_text(screen, '지구를 지켜라!',
                       self.font_70, draw_x, draw_y, YELLOW)
        self.draw_text(screen, '스페이스 키를 누르면',
                       self.font_30, draw_x, draw_y + 200, WHITE)
        self.draw_text(screen, '게임이 시작됩니다.',
                       self.font_30, draw_x, draw_y + 250, WHITE)

    # 게임 프레임 출력
    def display_frame(self, screen):
        # 배경 이미지
        screen.blit(self.background_image, self.background_image.get_rect())
        self.draw_text(screen, '파괴한 운석: {}'.format(self.shot_count),
                       self.default_font, 100, 20, YELLOW)
        self.draw_text(screen, '놓친 운석: {}'.format(self.count_missed),
                       self.default_font, 400, 20, RED)
        self.rocks.update()
        self.rocks.draw(screen)
        self.missiles.update()
        self.missiles.draw(screen)
        self.fighter.update()
        self.fighter.draw(screen)


# 게임 리소스 경로
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    pygame.init()
    pygame.display.set_caption('Shooting Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        if game.menu_on:  # 게임 메뉴 처리
            game.display_menu(screen)
        else:  # 게임 화면 처리
            game.run_logic(screen)
            game.display_frame(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
