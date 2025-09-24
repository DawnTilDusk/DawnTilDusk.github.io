import pygame
import numpy as np
import sys
import os

class Bot_0:
    def __init__(self, env):
        self.env = env
        self.speed = 4
        self.ball_center = self.env.ball_y
        self.pad_center = self.env.right_pad_y + self.env.pad_height // 2
            
    def act(self):
        if self.ball_center > self.env.right_pad_y and self.ball_center < self.env.right_pad_y + self.env.pad_height:
            return
        if self.ball_center < self.pad_center and self.env.right_pad_y > 0:
            self.env.right_pad_y -= self.speed
        elif self.ball_center > self.pad_center and self.env.right_pad_y + self.env.pad_height < self.env.WINDOW_HEIGHT:
            self.env.right_pad_y += self.speed
    
    

class PongEnv:
    WINDOW_WIDTH, WINDOW_HEIGHT = 1070, 600
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("pong")
        self.running = True
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        #package
        if hasattr(sys, '_MEIPASS'):
            # 打包后的路径：_MEIPASS/assets/bg.png
            self.bg_path = os.path.join(sys._MEIPASS, 'assets', 'bg.png')
        else:
            # 未打包时的路径：当前文件夹/assets/bg.png
            self.bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'bg.png')
        try:
            self.image = pygame.image.load(self.bg_path)
        except FileNotFoundError:
            print(f"警告：未找到图片 {self.bg_path}，使用备用背景")
            self.image = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            self.image.fill((40, 40, 40))  # 灰色备用背景
        
        # Load and scale background image
        self.img_width, self.img_height = self.image.get_size()
        self.scale_x = self.WINDOW_WIDTH / self.img_width
        self.scale_y = self.WINDOW_HEIGHT / self.img_height
        self.scale = min(self.scale_x, self.scale_y)
        self.new_width = int(self.img_width * self.scale)
        self.new_height = int(self.img_height * self.scale)
        self.scaled_image = pygame.transform.smoothscale(self.image, (self.new_width, self.new_height))
        self.image_x = (self.WINDOW_WIDTH - self.new_width) // 2
        self.image_y = (self.WINDOW_HEIGHT - self.new_height) // 2
        
        # Define colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255,235,205)
        self.list_colors = [self.WHITE, self.BLACK, self.RED, self.GREEN, self.BLUE, self.YELLOW]
        
        #paddles       
        self.left_pad_x = 10
        self.right_pad_x = self.WINDOW_WIDTH - self.left_pad_x
        self.pad_width = 10
        self.pad_height = 80
        self.pad_maxspeed = 10
        self.pad_speed = [0, 0]
        self.accellerate = 0.8
        self.decellerate = 1.2
        
        #ball
        self.ball_radius = 10
        self.factor = 1.1
        
        #score
        self.left_score = 0
        self.right_score = 0
        
        #reset
        self.reset()
    
    # Reset the game state
    def reset(self):
        self.left_pad_y = (self.WINDOW_HEIGHT - 50) // 2
        self.right_pad_y = (self.WINDOW_HEIGHT - 50) // 2
        self.ball_x = self.WINDOW_WIDTH // 2    
        self.ball_y = self.WINDOW_HEIGHT // 2
        self.ball_speed = [5 * np.random.choice([-1, 1]), 5 * np.random.uniform(-1, 1)]
#        self.ball_speed = [5 * np.random.choice([-1, 1]), 5 * np.random.choice([np.random.uniform(-1, -0.5), np.random.uniform(0.5, 1)])]
        
    def step(self):
        if not self.running:
            return
        
        #Paddle movement
        if self.left_pad_y + self.pad_speed[0] > 0 and self.left_pad_y + self.pad_speed[0] < self.WINDOW_HEIGHT - self.pad_height:
            self.left_pad_y += self.pad_speed[0]
            
        #Simple AI for right paddle
        bot = Bot_0(self)
        bot.act()
        self.right_pad_y = bot.env.right_pad_y
        
        #Ball movement
            
        self.ball_x += int(self.ball_speed[0])
        self.ball_y += int(self.ball_speed[1])
        
        #Paddle bounce back    
        if self.ball_x < self.left_pad_x + self.pad_width and self.ball_y + self.ball_radius > self.left_pad_y and self.ball_y - self.ball_radius < self.left_pad_y + self.pad_height:
            self.ball_speed[0] = -self.ball_speed[0] * self.factor
            self.ball_speed[1] += np.random.uniform(-3, 3)
        if self.ball_x > self.right_pad_x - self.pad_width and self.ball_y + self.ball_radius > self.right_pad_y and self.ball_y - self.ball_radius < self.right_pad_y + self.pad_height:
            self.ball_speed[0] = -self.ball_speed[0] * self.factor
            self.ball_speed[1] += np.random.uniform(-3, 3)
        
        if self.ball_y < 0 or self.ball_y > self.WINDOW_HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]
        
        if self.ball_x < 0:
            self.right_score += 1
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            self.reset()
        
        elif self.ball_x > self.WINDOW_WIDTH:
            self.left_score += 1
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            self.reset()

    def render(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.scaled_image, (self.image_x, self.image_y))
        pygame.draw.rect(self.screen, self.YELLOW, (self.left_pad_x, self.left_pad_y, self.pad_width, self.pad_height))
        pygame.draw.rect(self.screen, self.YELLOW, (self.right_pad_x, self.right_pad_y, self.pad_width, self.pad_height))
        pygame.draw.circle(self.screen, self.YELLOW, (self.ball_x, self.ball_y), self.ball_radius)
        pygame.draw.line(self.screen, self.YELLOW, (self.WINDOW_WIDTH//2, 100), (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT), 1)
        pygame.draw.line(self.screen, self.YELLOW, (0, 100), (self.WINDOW_WIDTH, 100), 1)

        font = pygame.font.SysFont("Arial", 50)
        score_text = font.render(f"{self.left_score} : {self.right_score}", True, self.WHITE)
        self.screen.blit(score_text, (self.WINDOW_WIDTH//2 - score_text.get_width()//2, 50 - score_text.get_height()//2))
        
        pygame.display.flip()
        self.clock.tick(80) 


env = PongEnv()
while env.running:
    action = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.running = False
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        env.pad_speed[0] = min(-env.pad_speed[0] - env.accellerate, -env.pad_maxspeed)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        env.pad_speed[0] = max(env.pad_speed[0] + env.accellerate, env.pad_maxspeed)
    else:
        env.pad_speed[0] = env.pad_speed[0] - env.decellerate if env.pad_speed[0] > 0 else 0
    env.step()
    env.render()
    
          
pygame.quit()