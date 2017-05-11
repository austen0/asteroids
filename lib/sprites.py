import math
import pygame
import random


class Asteroid(pygame.sprite.Sprite):
  def __init__(self, screen_size):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/sprites/asteroid.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (110, 110))
    self.original = self.image
    self.rect = self.image.get_rect()

    width, height = screen_size
    self.rect.center = (
      random.randint(55, width - 55), random.randint(55, height - 55))


class Bullet(pygame.sprite.Sprite):
  def __init__(self, screen_size, starting_coords, angle):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/sprites/missile.png').convert_alpha()
    self.original = self.image
    self.rect = self.image.get_rect()
    self.angle = angle
    self.speed = 20
    self.screen_size = screen_size

    self.rect = self.rect.move(starting_coords)
    self.image = pygame.transform.rotate(self.original, math.degrees(angle))
    self.rect = self.image.get_rect(center=starting_coords)

  def update_location(self):
    dy = self.speed * math.cos(self.angle + math.pi)
    dx = self.speed * math.sin(self.angle + math.pi)
    self.rect = self.rect.move(dx, dy)

    width, height = self.screen_size
    if (self.rect.left < 0 or self.rect.right > width or
      self.rect.top < 0 or self.rect.bottom > height):
      return True


class Crosshair(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/sprites/crosshair.png').convert_alpha()
    self.image = pygame.transform.scale(self.image, (20, 20))
    self.rect = self.image.get_rect()

  def update_location(self, mouse_coords):
    self.rect.center = mouse_coords


class Player(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load('img/sprites/ship.png').convert_alpha()
    self.original = self.image
    self.rect = self.image.get_rect()
    self.speed = 10

  def aim(self, mouse_coords):
    player_center_x, player_center_y = self.rect.center
    mouse_x, mouse_y = mouse_coords

    dx = mouse_x - player_center_x
    dy = mouse_y - player_center_y

    angle = math.atan2(float(-dy), float(dx)) - 0.5 * math.pi
    angle %= 2 * math.pi

    self.image = pygame.transform.rotate(self.original, math.degrees(angle))
    self.rect = self.image.get_rect(center=(player_center_x, player_center_y))
    return angle

  def move(self, direction):
    if direction == 'up':
      self.rect = self.rect.move([0, -self.speed])
    if direction == 'left':
      self.rect = self.rect.move([-self.speed, 0])
    if direction == 'down':
      self.rect = self.rect.move([0, self.speed])
    if direction == 'right':
      self.rect = self.rect.move([self.speed, 0])
