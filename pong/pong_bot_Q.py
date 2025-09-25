#train bot_Q with no mu
import pygame
import numpy as np
import sys
import pickle
import os
from datetime import datetime

class Bot_0:
    def __init__(self, env):
        self.env = env
        self.speed = 5
            
    def act(self, side):
        self.ball_center = self.env.ball_y
        self.pad_center = self.env.pad_y[side] + self.env.pad_height // 2
        if self.ball_center > self.env.pad_y[side] and self.ball_center < self.env.pad_y[side] + self.env.pad_height:
            return
        if self.ball_center < self.pad_center and self.env.pad_y[side] > 0:
            self.env.pad_y[side] -= self.speed
        elif self.ball_center > self.pad_center and self.env.pad_y[side] + self.env.pad_height < self.env.WINDOW_HEIGHT:
            self.env.pad_y[side] += self.speed   
   
#Q-learning agent 
class Bot_Q:
    
    def __init__(self, env, alpha=0.05, gamma=0.9, epsilon=0.000849):
        self.env = env
        self.Q = np.zeros((2, 2, 21, 21, 3)) #state: ball_x_dir, ball_y_dir, l_y_diff, r_y_diff; action: down, stay, up
    
    def get_state(self):
        ball_x_dir = 1 if self.env.ball_speed[0] > 0 else 0
        ball_y_dir = 1 if self.env.ball_speed[1] > 0 else 0
        l_y_diff = (self.env.pad_y[0] + self.env.pad_height // 2) - self.env.ball_y
        r_y_diff = (self.env.pad_y[1] + self.env.pad_height // 2) - self.env.ball_y
        
        bin = np.linspace(-self.env.WINDOW_HEIGHT//2, self.env.WINDOW_HEIGHT//2, 22)
        l_y_diff_idx = np.clip(np.digitize(l_y_diff, bin) - 1, 0, 20)
        r_y_diff_idx = np.clip(np.digitize(r_y_diff, bin) - 1, 0, 20)
        return (ball_x_dir, ball_y_dir, l_y_diff_idx, r_y_diff_idx)
    
    def act(self):
        state = self.get_state()
        action = np.argmax(self.Q[state])
        self.env.update_speed(action-1, 1)
        
    def load_q_table(self, path="q_table.pkl"):
        """从本地文件加载 Q 表"""
        try:
            with open(path, "rb") as f:
                self.Q = pickle.load(f)
            print(f"已从 {path} 加载 Q 表")
            # 加载后可降低探索率，减少随机动作
            #self.epsilon = max(0.01, self.epsilon * 0.1)
        except FileNotFoundError:
            print(f"未找到 {path}，请载入Q表")
        

class PongEnv:
    WINDOW_WIDTH, WINDOW_HEIGHT = 1070, 600
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("pong-v3")
        self.running = True
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Load and scale background image
        self.image = pygame.image.load('bg.png')
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
        self.pad_width = 10
        self.pad_height = 80
        self.pad_x = [0, self.WINDOW_WIDTH - self.pad_width]
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
        
        #bots
        self.bot_0 = Bot_0(self)
        self.bot = Bot_Q(self)
        self.bot.load_q_table()
        
        #reset
        self.reset()
        
    def update_speed(self, mode, side):
        if mode == 1: # up
            self.pad_speed[side] = max(self.pad_speed[side] - self.accellerate, -self.pad_maxspeed)
#            print(f"Speed: {self.pad_speed[side]}")
        elif mode == -1: # down
            self.pad_speed[side] = min(self.pad_speed[side] + self.accellerate, self.pad_maxspeed)
#            print(f"Speed: {self.pad_speed[side]}")
        elif mode == 0: # stay
            if self.pad_speed[side] > 0:
                 self.pad_speed[side] = max(self.pad_speed[side] - self.decellerate, 0)
            elif self.pad_speed[side] < 0:
                 self.pad_speed[side] = min(self.pad_speed[side] + self.decellerate, 0)
#            print(f"Speed: {self.pad_speed[side]}")
    
    # Reset the game state
    def reset(self):
        self.pad_y = [(self.WINDOW_HEIGHT - self.pad_height) // 2, (self.WINDOW_HEIGHT - self.pad_height) // 2]
        self.ball_x = self.WINDOW_WIDTH // 2    
        self.ball_y = self.WINDOW_HEIGHT // 2
        self.ball_speed = [5 * np.random.choice([-1, 1]), 5 * np.random.uniform(-1, 1)]
#        self.ball_speed = [5 * np.random.choice([-1, 1]), 5 * np.random.choice([np.random.uniform(-1, -0.5), np.random.uniform(0.5, 1)])]

    def l_collision(self):
        return self.ball_x < self.pad_x[0] + self.pad_width and self.ball_y + self.ball_radius > self.pad_y[0] and self.ball_y - self.ball_radius < self.pad_y[0] + self.pad_height
   
    def r_collision(self):
        return self.ball_x > self.pad_x[1] - self.pad_width and self.ball_y + self.ball_radius > self.pad_y[1] and self.ball_y - self.ball_radius < self.pad_y[1] + self.pad_height
         
    def step(self, mode):
        if not self.running:
            return
        
        #Paddle movement
        if  self.pad_y[0] + self.pad_speed[0] < 0:
            self.pad_y[0] = 0
        elif self.pad_y[0] + self.pad_speed[0] > self.WINDOW_HEIGHT - self.pad_height:
            self.pad_y[0] = self.WINDOW_HEIGHT - self.pad_height
        else:
            self.pad_y[0] += self.pad_speed[0]
            
        if  self.pad_y[1] + self.pad_speed[1] < 0:
            self.pad_y[1] = 0
        elif self.pad_y[1] + self.pad_speed[1] > self.WINDOW_HEIGHT - self.pad_height:
            self.pad_y[1] = self.WINDOW_HEIGHT - self.pad_height
        else:
            self.pad_y[1] += self.pad_speed[1]
        
        if mode == "bot_0":
            #Simple AI for left paddle
            self.bot_0.act(1)
        elif mode == "bot_Q" :
            #Q-learning agent for right paddle
            self.bot.act()
        
        #Ball movement            
        self.ball_x += int(self.ball_speed[0])
        self.ball_y += int(self.ball_speed[1])
        
        #Paddle bounce back    
        if self.l_collision():
            self.ball_speed[0] = -self.ball_speed[0] * self.factor
            self.ball_speed[1] += np.random.uniform(-3, 3)
        if self.r_collision():
            self.ball_speed[0] = -self.ball_speed[0] * self.factor
            self.ball_speed[1] += np.random.uniform(-3, 3)
        
        if self.ball_y < 0 or self.ball_y > self.WINDOW_HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]
        
        # Score update and episode end check
        check_over = False 
        if self.ball_x < 0:
            self.right_score += 1
                
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            check_over = True
            self.reset()
        
        elif self.ball_x > self.WINDOW_WIDTH:
            self.left_score += 1
                
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            check_over = True
            self.reset()    

    def render(self):
        self.screen.fill(self.BLACK)
        self.screen.blit(self.scaled_image, (self.image_x, self.image_y))
        pygame.draw.rect(self.screen, self.YELLOW, (self.pad_x[0], self.pad_y[0], self.pad_width, self.pad_height))
        pygame.draw.rect(self.screen, self.YELLOW, (self.pad_x[1], self.pad_y[1], self.pad_width, self.pad_height))
        pygame.draw.circle(self.screen, self.YELLOW, (self.ball_x, self.ball_y), self.ball_radius)
        pygame.draw.line(self.screen, self.YELLOW, (self.WINDOW_WIDTH//2, 100), (self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT), 1)
        pygame.draw.line(self.screen, self.YELLOW, (0, 100), (self.WINDOW_WIDTH, 100), 1)

        font = pygame.font.SysFont("consolas", 50)
        score_text = font.render(f"{self.left_score}   :   {self.right_score}", True, self.WHITE)
        self.screen.blit(score_text, (self.WINDOW_WIDTH//2 - score_text.get_width()//2, 50 - score_text.get_height()//2))
        
        pygame.display.flip()
        self.clock.tick(80) 


env = PongEnv()
mode = "bot_Q"
print("Press F2 for bot_0, F3 for bot_Q\n Default mode is bot_Q")
while env.running:
    action = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.running = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                mode = "bot_0"
            elif event.key == pygame.K_F3:
                mode = "bot_Q"
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        env.update_speed(1, 0)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        env.update_speed(-1, 0)
    else:
        env.update_speed(0, 0)
    
    env.step(mode)
    env.render()
          
pygame.quit()