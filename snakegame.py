# source activate pygame

import pygame
import sys
import random
import time


class Snake:  
  def spawn_food(self):
    return [random.randrange(1, 72)*10, random.randrange(1, 46)*10]

  def setup_pygame(self):
    check_errors = pygame.init()
    pygame.font.init()
    if check_errors[1] > 0:
      print("%d errors occurred" % check_errors[1])
      sys.exit(-1)
    else:
      print("starting...")  

    self.red = pygame.Color(255, 0, 0) # game over
    self.green = pygame.Color(0, 255, 0) # snake
    self.black = pygame.Color(0, 0, 0) # score
    self.white = pygame.Color(255,255,255) # background
    self.brown = pygame.Color(165,42,42) # food

  def __init__(self, through_walls=False, speed=30):
    self.setup_pygame()
    self.surface_dimensions = (720, 460) 
    self.play_surface = pygame.display.set_mode(self.surface_dimensions)
    pygame.display.set_caption("Snake") 
    self.fps_controller = pygame.time.Clock()

    self.score = 0
    self.snake_pos = [100, 50]
    self.snake_body = [[100,50],[90,50],[80,50]]

    self.food_pos = self.spawn_food()
    self.food_spawn = True

    self.direction = "RIGHT"
    self.changeto = self.direction

    self.through_walls = through_walls
    self.speed = speed

  def show_score(self, position=(50,20)):
    my_font = pygame.font.SysFont("monaco", 24)
    score_surface = my_font.render("Score :{}".format(self.score), True, self.black)
    score_rect = score_surface.get_rect()
    score_rect.midtop = position
    self.play_surface.blit(score_surface, score_rect)
    # pygame.display.flip()

  def game_over(self):
    my_font = pygame.font.SysFont("monaco", 72)
    go_surf = my_font.render("Game over!", True, self.red)
    go_rect = go_surf.get_rect()
    go_rect.midtop = (360, 15)
    self.show_score(position=(360, 120))
    self.play_surface.blit(go_surf, go_rect)
    pygame.display.flip()
    print("game over")
    time.sleep(4)
    pygame.quit()

  def is_valid_change(self):
    x = ["LEFT", "RIGHT"]
    y = ["UP", "DOWN"]
    return (self.changeto in x and self.direction in y) or (self.changeto in y and self.direction in x)


  def move_snake(self):
    # move head
    if self.direction == "RIGHT":
      self.snake_pos[0] += 10
    elif self.direction == "LEFT":
      self.snake_pos[0] -= 10
    elif self.direction == "UP":
      self.snake_pos[1] -= 10
    elif self.direction == "DOWN":
      self.snake_pos[1] += 10

    # update body
    self.snake_body.insert(0, list(self.snake_pos))
    # if you eat food, don't create it again
    if self.snake_pos == self.food_pos:
      self.score += 1
      self.food_spawn = False
    # otherwise reduce body size (really just moving everything)
    else:
      self.snake_body.pop()

    if not self.food_spawn:
      self.food_pos = self.spawn_food()
      self.food_spawn = True


  def draw(self):
    self.play_surface.fill(self.white)
    # pygame.display.flip()

    # draw snake
    for i, pos in enumerate(self.snake_body):
      # if you cross youself
      if i > 0 and self.snake_pos == pos:
        self.game_over()
        return False
      if self.through_walls:
        pos = [pos[i] % surface_dimensions[i] for i in range(2)]
      else:
        # out of bounds
        if not(0 <= pos[0] <= self.surface_dimensions[0]-10) or not(0 <= pos[1] < self.surface_dimensions[1]-10):
          self.game_over()
          return False
      # draw snake    
      pygame.draw.rect(self.play_surface, self.green, pygame.Rect(*pos, 10, 10))

    # draw food
    pygame.draw.rect(self.play_surface, self.brown, pygame.Rect(*self.food_pos, 10, 10))

    self.show_score()
    pygame.display.flip()
    self.fps_controller.tick(self.speed)
    return True

  def game_loop(self):
    self.keep_going=True
    while self.keep_going:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          print("quit")
          pygame.quit()
          # sys.exit()
        elif event.type == pygame.KEYDOWN:
          if event.key in [pygame.K_RIGHT, ord('d')]:
            self.changeto = "RIGHT"
          elif event.key in [pygame.K_LEFT, ord('a')]:
            self.changeto = "LEFT"
          elif event.key in [pygame.K_UP, ord('w')]:
            self.changeto = "UP"
          elif event.key in [pygame.K_DOWN, ord('s')]:
            self.changeto = "DOWN"
          elif event.key == pygame.K_ESCAPE:
            print("exit")
            pygame.event.post(pygame.event.Event(pygame.QUIT))

          if self.is_valid_change():
            self.direction = self.changeto

      self.move_snake()
      self.keep_going = self.draw()

    self.game_over()
    time.sleep(1)

if __name__ == "__main__":
  s = Snake(through_walls=False, speed=10)
  s.game_loop()
