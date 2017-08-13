# source activate pygame

import pygame
import sys
import random
import time

check_errors = pygame.init()
if check_errors[1] > 0:
  print("%d errors occurred" % check_errors[1])
  sys.exit(-1)
else:
  print("starting...")


surface_dimensions = (720, 460)
play_surface = pygame.display.set_mode(surface_dimensions)
pygame.display.set_caption("Snake")

red = pygame.Color(255, 0, 0) # game over
green = pygame.Color(0, 255, 0) # snake
black = pygame.Color(0, 0, 0) # score
white = pygame.Color(255,255,255) # background
brown = pygame.Color(165,42,42) # food

def spawn_food():
  return [random.randrange(1, 72)*10, random.randrange(1, 46)*10]

fps_controller = pygame.time.Clock()
snake_pos = [100, 50]
snake_body = [[100,50],[90,50],[80,50]]

food_pos = spawn_food()
food_spawn = True

direction = "RIGHT"
changeto = direction


def game_over():
  my_font = pygame.font.SysFont("monaco", 72)
  go_surf = my_font.render("Game over!", True, red)
  go_rect = go_surf.get_rect()
  go_rect.midtop = (360, 15)
  play_surface.blit(go_surf, go_rect)
  pygame.display.flip()
  print("game over")
  time.sleep(4)
  pygame.quit()
  # sys.exit()


def is_valid_change(changeto, direction):
  x = ["LEFT", "RIGHT"]
  y = ["UP", "DOWN"]
  return (changeto in x and direction in y) or (changeto in y and direction in x)


def move_snake(direction, food_pos, food_spawn):
  # move head
  if direction == "RIGHT":
    snake_pos[0] += 10
  elif direction == "LEFT":
    snake_pos[0] -= 10
  elif direction == "UP":
    snake_pos[1] -= 10
  elif direction == "DOWN":
    snake_pos[1] += 10

  # update body
  snake_body.insert(0, snake_pos)
  # if you eat food, don't create it again
  if snake_pos == food_pos:
    food_spawn = False
  # otherwise reduce body size (really just moving everything)
  else:
    snake_body.pop()

  if not food_spawn:
    food_pos = spawn_food()
    food_spawn = True


def draw(play_surface):
  play_surface.fill(white)
  pygame.display.flip()
  for pos in snake_body:
    pos = [pos[i] % surface_dimensions[i] for i in range(2)]
    r = pygame.Rect(*pos, 10, 10)
    pygame.draw.rect(play_surface, green, r)
  pygame.display.flip()
  fps_controller.tick(25)


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      # sys.exit()
    elif event.type == pygame.KEYDOWN:
      if event.key in [pygame.K_RIGHT, ord('d')]:
        changeto = "RIGHT"
      elif event.key in [pygame.K_LEFT, ord('a')]:
        changeto = "LEFT"
      elif event.key in [pygame.K_UP, ord('w')]:
        changeto = "UP"
      elif event.key in [pygame.K_DOWN, ord('s')]:
        changeto = "DOWN"
      elif event.key == pygame.K_ESCAPE:
        print("exit")
        pygame.event.post(pygame.event.Event(pygame.QUIT))

      if is_valid_change(changeto, direction):
        direction = changeto

  move_snake(direction, food_pos, food_spawn)
  draw(play_surface)


game_over()
time.sleep(2)
