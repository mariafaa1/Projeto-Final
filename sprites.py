import pygame
from config import WIDTH, HEIGHT, PLAYER_SPEED, BULLET_SPEED, SHOOT_COOLDOWN

class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y, controls, assets):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = PLAYER_SPEED
        self.controls = controls
        self.assets = assets
        self.last_shot = pygame.time.get_ticks()

    def update(self, keys_pressed, bullets_group, all_sprites):
        if keys_pressed[self.controls['up']]:
            self.rect.y -= self.speed
        if keys_pressed[self.controls['down']]:
            self.rect.y += self.speed
        if keys_pressed[self.controls['left']]:
            self.rect.x -= self.speed
        if keys_pressed[self.controls['right']]:
            self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        now = pygame.time.get_ticks()
        if keys_pressed[self.controls['shoot']] and now - self.last_shot > SHOOT_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.assets['bullet'])
            bullets_group.add(bullet)
            all_sprites.add(bullet)
            self.assets['som_tiro'].play()
            self.last_shot = now

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()