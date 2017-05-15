import math
import pygame
import random


class Asteroid(pygame.sprite.Sprite):
  def __init__(self, screen_size):
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load('img/sprites/asteroid.png').convert_alpha()
    size = random.randint(55, 110)
    self.image = pygame.transform.scale(self.image, (size, size))
    self.rect = self.image.get_rect()

    self.speed = random.randint(2, 8)
    self.width, self.height = screen_size

    x = random.choice([(-size / 2), (self.width + size / 2)])
    y = random.choice([(-size / 2), (self.height + size / 2)])
    self.rect.center = (x, y)

    if x > 0 and y > 0:  # bottom right
      self.angle = random.randint(181, 269)
    if x > 0 and y < 0:  # top right
      self.angle = random.randint(271, 359)
    if x < 0 and y < 0:  # top left
      self.angle = random.randint(1, 89)
    if x < 0 and y > 0:  # bottom left
      self.angle = random.randint(91, 179)

  def update_location(self):
    dy = self.speed * math.cos(math.radians(self.angle))
    dx = self.speed * math.sin(math.radians(self.angle))
    self.rect = self.rect.move(dx, dy)

    if (self.rect.left < -100 or self.rect.right > self.width + 100 or
      self.rect.top < -100 or self.rect.bottom > self.height + 100):
      return True


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
