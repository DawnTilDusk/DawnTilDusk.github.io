import pygame
import numpy as np
import sys

class PongEnv:
    def __init__(self, width=400, height=300):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        
        # 游戏元素
        self.paddle_width = 10
        self.paddle_height = 60
        self.ball_size = 10
        
        self.reset()
    
    def reset(self):
        # 初始化球拍和球的位置
        self.left_paddle = pygame.Rect(10, self.height//2 - self.paddle_height//2, 
                                     self.paddle_width, self.paddle_height)
        self.right_paddle = pygame.Rect(self.width - 20, self.height//2 - self.paddle_height//2, 
                                      self.paddle_width, self.paddle_height)
        
        # 球的初始位置和速度
        self.ball = pygame.Rect(self.width//2 - self.ball_size//2, 
                              self.height//2 - self.ball_size//2, 
                              self.ball_size, self.ball_size)
        self.ball_speed = [5 * np.random.choice([-1, 1]), 5 * np.random.uniform(-1, 1)]
        
        self.left_score = 0
        self.right_score = 0
        self.done = False
        
        return self._get_state()
    
    def _get_state(self):
        """返回当前状态（可用于强化学习）"""
        # 返回球拍位置、球位置、球速度等
        return np.array([
            self.left_paddle.centery / self.height,
            self.right_paddle.centery / self.height,
            self.ball.centerx / self.width,
            self.ball.centery / self.height,
            self.ball_speed[0] / 10,
            self.ball_speed[1] / 10
        ])
    
    def step(self, left_action, right_action=0):
        """执行动作
        left_action: 0-上, 1-静止, 2-下
        right_action: 0-上, 1-静止, 2-下 (可用于双智能体或对手控制)
        """
        # 处理左球拍动作
        if left_action == 0 and self.left_paddle.top > 0:
            self.left_paddle.y -= 5
        elif left_action == 2 and self.left_paddle.bottom < self.height:
            self.left_paddle.y += 5
        
        # 简单的AI控制右球拍（可以替换为另一个智能体）
        if self.ball.centery < self.right_paddle.centery and self.right_paddle.top > 0:
            self.right_paddle.y -= 4
        elif self.ball.centery > self.right_paddle.centery and self.right_paddle.bottom < self.height:
            self.right_paddle.y += 4
        
        # 更新球的位置
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]
        
        # 球碰到上下边界
        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            self.ball_speed[1] = -self.ball_speed[1]
        
        # 球碰到球拍
        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.ball_speed[0] = -self.ball_speed[0] * 1.1  # 稍微加速
            # 根据击中球拍的位置调整反弹角度
            hit_pos = (self.ball.centery - (self.left_paddle.centery if self.ball_speed[0] < 0 else self.right_paddle.centery)) / (self.paddle_height / 2)
            self.ball_speed[1] = hit_pos * 7
        
        # 得分判断
        reward = 0
        if self.ball.left <= 0:
            self.right_score += 1
            reward = -1  # 左球拍失分
            self.ball_speed = [5, 5 * np.random.uniform(-1, 1)]
            self.ball.center = (self.width//2, self.height//2)
        elif self.ball.right >= self.width:
            self.left_score += 1
            reward = 1   # 左球拍得分
            self.ball_speed = [-5, 5 * np.random.uniform(-1, 1)]
            self.ball.center = (self.width//2, self.height//2)
        
        # 游戏结束条件（例如达到一定分数）
        if self.left_score >= 5 or self.right_score >= 5:
            self.done = True
            reward = 10 if self.left_score >= 5 else -10
        
        return self._get_state(), reward, self.done, {}
    
    def render(self):
        """渲染游戏画面"""
        self.screen.fill((0, 0, 0))
        
        # 绘制球拍和球
        pygame.draw.rect(self.screen, (255, 255, 255), self.left_paddle)
        pygame.draw.rect(self.screen, (255, 255, 255), self.right_paddle)
        pygame.draw.ellipse(self.screen, (255, 255, 255), self.ball)
        
        # 绘制中线
        pygame.draw.aaline(self.screen, (255, 255, 255), 
                          (self.width//2, 0), (self.width//2, self.height))
        
        # 显示分数
        font = pygame.font.Font(None, 36)
        left_text = font.render(str(self.left_score), True, (255, 255, 255))
        right_text = font.render(str(self.right_score), True, (255, 255, 255))
        self.screen.blit(left_text, (self.width//4, 20))
        self.screen.blit(right_text, (3*self.width//4, 20))
        
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
    
    def close(self):
        pygame.quit()

# 使用示例
if __name__ == "__main__":
    env = PongEnv()
    state = env.reset()
    
    while True:
        # 简单的手动控制（上箭头和下箭头）
        action = 1  # 静止
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            action = 0
        elif keys[pygame.K_DOWN]:
            action = 2
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                env.close()
                sys.exit()
        
        state, reward, done, _ = env.step(action)
        env.render()
        
##        if done:
##            state = env.reset()