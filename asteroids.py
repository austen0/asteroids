import math
import pygame
import random
import sys
import time

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

player = pygame.sprite.GroupSingle(sprites.Player())
player.sprite.rect.center = screen.get_rect().center
crosshair = sprites.Crosshair()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

score = 0

while 1:
  clock.tick(60)

  mouse_coords = pygame.mouse.get_pos()
  crosshair.update_location(mouse_coords)
  aim_angle = player.sprite.aim(mouse_coords)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      bullets.add(
        sprites.Bullet(SCREEN_SIZE, player.sprite.rect.center, aim_angle))

  keys = pygame.key.get_pressed()
  if keys[pygame.K_ESCAPE]:
    sys.exit()
  if keys[pygame.K_w]:
    player.sprite.move('up')
  if keys[pygame.K_a]:
    player.sprite.move('left')
  if keys[pygame.K_s]:
    player.sprite.move('down')
  if keys[pygame.K_d]:
    player.sprite.move('right')

  roll = random.random()
  if roll < 0.025:
    asteroids.add(sprites.Asteroid(SCREEN_SIZE))

  if bullets:
    for b in bullets:
      offscreen_bullets = b.update_location()
      if offscreen_bullets:
        b.kill()
  if asteroids:
    for a in asteroids:
      offscreen_asteroids = a.update_location()
      if offscreen_asteroids:
        a.kill()
  if pygame.sprite.groupcollide(bullets, asteroids, True, True):
    score += 1
  player_collision = pygame.sprite.groupcollide(player, asteroids, False, True)

  if player_collision:
    score = 0

  allsprites = pygame.sprite.LayeredUpdates(
    asteroids, bullets, crosshair, player)
  allsprites.move_to_front(crosshair)

  font = pygame.font.Font(None, 36)
  text = font.render('Score: %d' % score, True, (255, 255, 255))
  textpos = text.get_rect()
  textpos.centerx = screen.get_rect().right - textpos.width / 2
  textpos.centery = textpos.height / 2
  background.fill(BLACK)
  background.blit(text, textpos)

  screen.blit(background, (0, 0))
  allsprites.draw(screen)
  pygame.display.flip()
