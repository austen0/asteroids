import math
import pygame
import random
import sys

import lib.sprites as sprites

SCREEN_SIZE = 1024, 768
BLACK = 0, 0, 0


pygame.init()
pygame.display.set_caption('asteroids')
pygame.mouse.set_visible(0)

screen = pygame.display.set_mode(SCREEN_SIZE)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)
screen.blit(background, (0, 0))
pygame.display.flip()
clock = pygame.time.Clock()

player = sprites.Player()
crosshair = sprites.Crosshair()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

while 1:
  clock.tick(60)

  mouse_coords = pygame.mouse.get_pos()
  crosshair.update_location(mouse_coords)
  aim_angle = player.aim(mouse_coords)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      bullets.add(sprites.Bullet(SCREEN_SIZE, player.rect.center, aim_angle))

  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    sys.exit()
  if keys[pygame.K_w]:
    player.move('up')
  if keys[pygame.K_a]:
    player.move('left')
  if keys[pygame.K_s]:
    player.move('down')
  if keys[pygame.K_d]:
    player.move('right')

  roll = random.random()
  if roll < 0.025:
    asteroids.add(sprites.Asteroid(SCREEN_SIZE))

  if bullets:
    for b in bullets:
      offscreen = b.update_location()
      if offscreen:
        b.kill()
  pygame.sprite.groupcollide(bullets, asteroids, True, True)

  allsprites = pygame.sprite.LayeredUpdates(
    asteroids, bullets, crosshair, player)
  allsprites.move_to_front(crosshair)

  screen.blit(background, (0, 0))
  allsprites.draw(screen)
  pygame.display.flip()
