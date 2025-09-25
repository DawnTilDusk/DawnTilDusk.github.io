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
        
        # hyperparameters
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.decaying = 0.999999
        
        self.Q = np.zeros((2, 2, 21, 21, 3)) #state: ball_x_dir, ball_y_dir, l_y_diff, r_y_diff; action: down, stay, up
        
        self.last_state = None
        self.last_action = None
        
        #trace for visualization
        self.win_rate_max_episode = 50
        self.episode_cnt = 0 
        self.recent_win_rate = 0.000
        self.recent_win_history = []
        self.reward_history = []  
        self.win_rate_history = [] 
        self.total_reward = 0  
        
    def get_state(self):
        ball_x_dir = 1 if self.env.ball_speed[0] > 0 else 0
        ball_y_dir = 1 if self.env.ball_speed[1] > 0 else 0
        l_y_diff = (self.env.pad_y[0] + self.env.pad_height // 2) - self.env.ball_y
        r_y_diff = (self.env.pad_y[1] + self.env.pad_height // 2) - self.env.ball_y
        
        bin = np.linspace(-self.env.WINDOW_HEIGHT//2, self.env.WINDOW_HEIGHT//2, 22)
        l_y_diff_idx = np.clip(np.digitize(l_y_diff, bin) - 1, 0, 20)
        r_y_diff_idx = np.clip(np.digitize(r_y_diff, bin) - 1, 0, 20)
        return (ball_x_dir, ball_y_dir, l_y_diff_idx, r_y_diff_idx)
    
    def take_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.choice([0, 1, 2])
        else:
            action = np.argmax(self.Q[state])
        self.epsilon *= self.decaying
        return action
    
    def update_Q(self, last_state, last_action, reward, current_state):
        if last_state is not None and last_action is not None:
            self.Q[last_state][last_action] += self.alpha * (
                reward + self.gamma * np.max(self.Q[current_state]) - self.Q[last_state][last_action]
            )
    
    def L2_reward(self, a, b):
        return (100 - ((a-b)/100) ** 2) // 5
        
    def calculate_r(self):
        state = self.get_state()
        action = self.last_action
        
        # encourage moving towards the ball when ball is moving towards the pad
        if self.env.ball_speed[0] > 0:
            reward = self.L2_reward(self.env.pad_y[1] + self.env.pad_height // 2, self.env.ball_y)
        else: 
            reward = self.L2_reward(self.env.pad_y[1] + self.env.pad_height // 2, self.env.WINDOW_HEIGHT // 2)
            
        if self.env.pad_y[1] < 50:
            reward -= 10  # punish stay top
        
        elif self.env.pad_y[1] + self.env.pad_height > self.env.WINDOW_HEIGHT - 50:
            reward -= 10  # punish stay bottom
        
        if action is not None:
            #1 stay punishment and discourage staying when ball is moving away from the pad
            if action == 1 or (self.env.pad_speed[1] == 0 and self.env.ball_speed[0] <= 0): 
                reward -= 5
            # discourage moving away from the ball when ball is moving towards the pad
            if self.env.ball_speed[0] > 0:
                pad_center = self.env.pad_y[1] + self.env.pad_height // 2
                if (self.env.ball_y < pad_center and action == 0) or (self.env.ball_y > pad_center and action == 2):
                    reward -= 5
            
            
        if self.env.r_collision():
            reward += 200  # hit right paddle reward
            
        elif self.env.l_collision():
            reward -= 10  # hit left paddle punishment
        
        if self.env.ball_x < self.env.pad_width:
            reward += 50  # ball went out of left side reward

        elif self.env.ball_x > self.env.WINDOW_WIDTH - self.env.pad_width:
            reward -= 200  # ball went out of right side punishment
        
        # record reward history        
        self.reward_history.append(reward)
        if len(self.reward_history) > 500:
            self.reward_history.pop(0)
        self.total_reward += reward
            
        return reward
        
    def act(self):
        current_state = self.get_state()
        action = self.take_action(current_state)
        self.env.update_speed(action-1, 1)
        reward = self.calculate_r()
        self.update_Q(self.last_state, self.last_action, reward, current_state)
        
        self.last_state = current_state
        self.last_action = action
        
    def save_q_table(self, path="q_table.pkl", versioned=False):
#        保存Q表，支持版本化（避免覆盖）
#        :param versioned: 是否按时间戳生成版本（True：不覆盖，False：覆盖原文件）

        if versioned:
            # 按时间戳命名（格式：q_table_20240520_1530.pkl）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            path = f"q_table_{timestamp}.pkl"
    
        # 可选：手动确认是否覆盖
        confirm = "y"
        if os.path.exists(path) and not versioned:
            confirm = input(f"文件 {path} 已存在，是否覆盖？(y/n): ")

        if confirm.lower() != "y":
            print("保存取消")
            return
    
        with open(path, "wb") as f:
            pickle.dump(self.Q, f)
        print(f"Q表已保存到 {path}")
    
    def load_q_table(self, path="q_table.pkl"):
        """从本地文件加载 Q 表"""
        try:
            with open(path, "rb") as f:
                self.Q = pickle.load(f)
            print(f"已从 {path} 加载 Q 表")
            # 加载后可降低探索率，减少随机动作
            #self.epsilon = max(0.01, self.epsilon * 0.1)
        except FileNotFoundError:
            print(f"未找到 {path}，将使用新的 Q 表")
        
        

class PongEnv:
    WINDOW_WIDTH, WINDOW_HEIGHT = 1070, 600
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption("pong")
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
         
    def step(self):
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
            
        #Simple AI for left paddle
        self.bot_0.act(0)
        
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
            self.bot.recent_win_history.append(1)
            if len(self.bot.recent_win_history) > 10:
                self.bot.recent_win_history.pop(0)
                
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            check_over = True
            self.reset()
        
        elif self.ball_x > self.WINDOW_WIDTH:
            self.left_score += 1
            self.bot.recent_win_history.append(0)
            if len(self.bot.recent_win_history) > self.bot.win_rate_max_episode:
                self.bot.recent_win_history.pop(0)
                
            print(f"Left score: {self.left_score}, Right score: {self.right_score}")
            check_over = True
            self.reset()
        
        if check_over:    
            self.bot.episode_cnt += 1
            self.bot.recent_win_rate = sum(self.bot.recent_win_history) / min(self.bot.episode_cnt, self.bot.win_rate_max_episode)
            self.bot.win_rate_history.append(self.bot.recent_win_rate)
            if len(self.bot.win_rate_history) > self.bot.win_rate_max_episode:
                self.bot.win_rate_history.pop(0)

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
        
        # -------------------------- 新增：训练进度可视化 --------------------------
        # 1. 初始化小字体（用于指标文本）
        font_small = pygame.font.SysFont("simsun", 18)
        # 2. 计算关键指标
        avg_reward = np.mean(self.bot.reward_history) if self.bot.reward_history else 0.0
        avg_q_value = np.mean(self.bot.Q)  # Q表平均价值（反映收敛度）
        #recent_win_rate = np.mean(self.bot.win_rate_history) if self.bot.win_rate_history else 0.0
        
        # 3. 绘制指标文本（左上角排列）
        text_color = self.WHITE
        texts = [
            f"回合数: {self.bot.episode_cnt}",
            f"近期胜率: {self.bot.recent_win_rate:.2f}",
            f"平均奖励: {avg_reward:.2f}",
            f"Q表均值: {avg_q_value:.4f}",
            f"探索率: {self.bot.epsilon:.6f}"
        ]
        for i, text in enumerate(texts):
            text_surface = font_small.render(text, True, text_color)
            self.screen.blit(text_surface, (10, 10 + i*30))  # 每行间隔30像素
        
        # 4. 绘制胜率趋势图（左下角，宽200，高100，直观展示胜率变化）
        chart_x = 10
        chart_y = self.WINDOW_HEIGHT - 110  # 底部留出10像素边距
        chart_width = 200
        chart_height = 100
        
        # 绘制图表背景（灰色）
        pygame.draw.rect(self.screen, (50, 50, 50), (chart_x, chart_y, chart_width, chart_height))
        # 绘制坐标轴（白色）
        pygame.draw.line(self.screen, self.WHITE, (chart_x, chart_y + chart_height), (chart_x + chart_width, chart_y + chart_height), 1)  # X轴
        pygame.draw.line(self.screen, self.WHITE, (chart_x, chart_y), (chart_x, chart_y + chart_height), 1)  # Y轴
        # 绘制胜率折线（绿色，若有足够数据）
        if len(self.bot.win_rate_history) > 1:
            # 遍历历史胜率，计算每个点的坐标
            points = []
            for i, rate in enumerate(self.bot.win_rate_history):
                # X坐标：均匀分布在图表宽度内
                x = chart_x + (i / (len(self.bot.win_rate_history) - 1)) * chart_width
                # Y坐标：胜率0→1对应图表底部→顶部（反转Y轴）
                y = chart_y + chart_height - (rate * chart_height)
                points.append((int(x), int(y)))
            # 绘制折线
            pygame.draw.lines(self.screen, self.GREEN, False, points, 2)
        
        if len(self.bot.reward_history) > 1:
            # 绘制奖励趋势图（右下角，宽200，高100）
            chart_x = self.WINDOW_WIDTH - 210
            chart_y = self.WINDOW_HEIGHT - 110
            chart_width = 200
            chart_height = 100
            
            # 绘制图表背景（灰色）
            pygame.draw.rect(self.screen, (50, 50, 50), (chart_x, chart_y, chart_width, chart_height))
            # 绘制坐标轴（白色）
            pygame.draw.line(self.screen, self.WHITE, (chart_x, chart_y + chart_height), (chart_x + chart_width, chart_y + chart_height), 1)  # X轴
            pygame.draw.line(self.screen, self.WHITE, (chart_x, chart_y), (chart_x, chart_y + chart_height), 1)  # Y轴
            
            # 奖励值归一化到0-1范围内，便于绘图
            min_reward = min(self.bot.reward_history)
            max_reward = max(self.bot.reward_history)
            reward_range = max_reward - min_reward if max_reward != min_reward else 1.0
            
            points = []
            for i, r in enumerate(self.bot.reward_history):
                x = chart_x + (i / (len(self.bot.reward_history) - 1)) * chart_width
                normalized_r = (r - min_reward) / reward_range
                y = chart_y + chart_height - (normalized_r * chart_height)
                points.append((int(x), int(y)))
            # 绘制折线
            pygame.draw.lines(self.screen, self.BLUE, False, points, 2)
        # -------------------------------------------------------------------------
        
        pygame.display.flip()
        self.clock.tick(80) 


env = PongEnv()
while env.running:
    action = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.running = False
            env.bot.save_q_table("q_table.pkl")
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F2:
                env.bot.save_q_table(versioned=True)  # 按时间戳保存，不覆盖
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        env.update_speed(1, 0)
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        env.update_speed(-1, 0)
    else:
        env.update_speed(0, 0)
    
    env.step()
    env.render()
          
pygame.quit()