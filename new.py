import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
GROUND_Y = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reverse Cat Mario - Thwomp Drop")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
SKY = (135, 206, 235)

scroll_x = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('동아리 발표회 프로그램\\고양이 마리오\\sprite\\28.png').convert_alpha()
        # self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, GROUND_Y - 40)
        self.vel_y = 0
        self.on_ground = False
        self.jump_timer = 0
        self.invincible_timer = 0
        self.invincible = False

    def update(self, dt):
        self.rect.x += 4
        self.jump_timer += dt
        if self.jump_timer >= 1.5:
            if self.on_ground:
                self.vel_y = -10
            self.jump_timer = 0

        self.invincible_timer += dt
        if self.invincible_timer >= 0.1:
            self.invincible = True
        if self.invincible and self.invincible_timer >= 2.0:
            self.invincible = False
            self.invincible_timer = 0

        self.vel_y += 0.5
        self.rect.y += self.vel_y

        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def draw(self, screen):
        if self.invincible:
            pygame.draw.rect(screen, (255, 255, 0), (self.rect.x - scroll_x - 5, self.rect.y - 5, 50, 50))
        screen.blit(self.image, (self.rect.x - scroll_x, self.rect.y))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Thwomp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(GRAY)
        pygame.draw.rect(self.image, BLACK, (10, 10, 10, 10))
        pygame.draw.rect(self.image, BLACK, (40, 10, 10, 10))
        pygame.draw.rect(self.image, BLACK, (20, 35, 20, 8))
        self.rect = self.image.get_rect()
        self.start_y = y
        self.rect.x = x
        self.rect.y = y
        self.state = "waiting"
        self.fall_speed = 0
        self.rise_speed = 6
        self.rise_delay_timer = 0

    def toggle(self):
        if self.state == "waiting":
            self.state = "falling"
            self.fall_speed = 1

    def move_left(self):
        self.rect.x -= 5

    def move_right(self):
        self.rect.x += 5

    def update(self, dt=0):
        if self.state == "falling":
            self.fall_speed += 0.8
            self.rect.y += self.fall_speed
            if self.rect.bottom >= GROUND_Y:
                self.rect.bottom = GROUND_Y
                self.state = "waiting_to_rise"
                self.rise_delay_timer = 0
        elif self.state == "waiting_to_rise":
            self.rise_delay_timer += dt
            if self.rise_delay_timer >= 0.2:
                self.state = "rising"
        elif self.state == "rising":
            self.rect.y -= self.rise_speed
            if self.rect.y <= self.start_y:
                self.rect.y = self.start_y
                self.state = "waiting"

class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 80))
        self.image.fill((255, 255, 0))
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def reset_game():
    global all_sprites, platforms, thwomps, flags, player, scroll_x, game_state

    scroll_x = 0
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    thwomps = pygame.sprite.Group()
    flags = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(0, 3000, 300):
        p = Platform(i, GROUND_Y, 300, 50)
        all_sprites.add(p)
        platforms.add(p)

    platforms_data = [
        (400, GROUND_Y - 100, 100, 20),
        (800, GROUND_Y - 150, 100, 20),
        (1200, GROUND_Y - 120, 100, 20),
        (1600, GROUND_Y - 180, 100, 20),
        (2000, GROUND_Y - 130, 120, 20),
        (2400, GROUND_Y - 100, 150, 20),
    ]
    for x, y, w, h in platforms_data:
        plat = Platform(x, y, w, h)
        all_sprites.add(plat)
        platforms.add(plat)

    thwomp_positions = [
        (600, 100),
        (1000, 80),
        (1400, 120),
        (1800, 60),
    ]
    for x, y in thwomp_positions:
        t = Thwomp(x, y)
        all_sprites.add(t)
        thwomps.add(t)

    flag = Flag(2900, GROUND_Y - 80)
    all_sprites.add(flag)
    flags.add(flag)

    game_state = "playing"

reset_game()

while True:
    dt = clock.tick(60) / 1000
    screen.fill(SKY)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        for t in thwomps:
            t.move_left()
    if keys[pygame.K_d]:
        for t in thwomps:
            t.move_right()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == "playing":
                for t in thwomps:
                    t.toggle()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "lose":
                reset_game()

    if game_state == "playing":
        player.update(dt)
        for sprite in all_sprites:
            if sprite != player:
                sprite.update(dt)

        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits and player.vel_y > 0:
            player.rect.bottom = hits[0].rect.top
            player.vel_y = 0
            player.on_ground = True

        for t in thwomps:
            if t.rect.colliderect(player.rect):
                if not player.invincible:
                    game_state = "win"

        if pygame.sprite.spritecollide(player, flags, False):
            game_state = "win"

        if player.rect.x > 2800:
            game_state = "lose"

        if player.rect.centerx - scroll_x > WIDTH // 2:
            scroll_x = player.rect.centerx - WIDTH // 2

        for sprite in all_sprites:
            if sprite != player:
                screen.blit(sprite.image, (sprite.rect.x - scroll_x, sprite.rect.y))
        player.draw(screen)

    elif game_state == "win":
        screen.fill((0, 255, 0))
        text = font.render("YOU WIN!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

    elif game_state == "lose":
        screen.fill((255, 0, 0))
        text = font.render("GAME OVER!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2))
        text2 = font.render("Click to retry", True, WHITE)
        screen.blit(text2, (WIDTH // 2 - 120, HEIGHT // 2 + 60))

    pygame.display.flip()
