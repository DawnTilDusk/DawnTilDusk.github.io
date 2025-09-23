import pygame
import numpy as np
import sys

pygame.init()


WINDOW_WIDTH, WINDOW_HEIGHT = 1070, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
image = pygame.image.load('bg.png')

pygame.display.set_caption("pong")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

list_colors = [WHITE, BLACK, RED, GREEN, BLUE]

running = True
pad_y = (WINDOW_HEIGHT - 50) // 2
pad_x = (WINDOW_WIDTH - 50) // 2
while running:
    speed = 10
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        pad_y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        pad_y += speed 
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pad_x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        pad_x += speed   
            
    screen.fill(BLACK)
    
    img_width, img_height = image.get_size()
    scale_x = WINDOW_WIDTH / img_width
    scale_y = WINDOW_HEIGHT / img_height
    scale = min(scale_x, scale_y)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    scaled_image = pygame.transform.smoothscale(image, (new_width, new_height))
    
    x = (WINDOW_WIDTH - new_width) // 2
    y = (WINDOW_HEIGHT - new_height) // 2
    
    screen.blit(scaled_image, (x, y))
    
 #   for i in range(50, 100):
 #       screen.fill(BLACK)
 #       screen.blit(scaled_image, (x, y))
 #       pygame.draw.rect(screen, WHITE, (i, 50, 100, 50))
  #      pygame.draw.circle(screen, RED, (i, 50), 30)   
 #       pygame.display.flip()
#        pygame.time.delay(10)

    pygame.draw.rect(screen, WHITE, (20, pad_y, 2, 100))
#    pygame.draw.rect(screen, WHITE, (pad_x, pad_y, 2, 50))
    
    pygame.display.flip()
    clock.tick(80)        
pygame.quit()