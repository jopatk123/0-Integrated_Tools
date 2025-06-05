# -*- coding: utf-8 -*-
"""贪吃蛇游戏模块"""

import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    """贪吃蛇游戏类"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        
        # 游戏参数
        self.canvas_width = 400
        self.canvas_height = 400
        self.cell_size = 20
        self.game_speed = 150  # 毫秒
        
        # 游戏状态
        self.game_running = False
        self.game_paused = False
        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        
        # 蛇和食物
        self.snake = [(10, 10), (10, 9), (10, 8)]  # 蛇身坐标列表
        self.food = None
        
        # 创建游戏界面
        self.create_widgets()
        self.generate_food()
        self.bind_keys()
        
    def create_widgets(self):
        """创建游戏界面"""
        # 游戏标题
        title_label = tk.Label(self.parent, text="🐍 贪吃蛇游戏", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=10)
        
        # 游戏信息栏
        info_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        info_frame.pack(pady=5)
        
        self.score_label = tk.Label(info_frame, text=f"得分: {self.score}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 12))
        self.score_label.pack(side=tk.LEFT, padx=10)
        
        # 游戏状态显示区域
        self.status_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        self.status_frame.pack(pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="点击开始游戏按钮开始", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 12, "bold"))
        self.status_label.pack()
        
        # 控制按钮
        control_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        control_frame.pack(pady=5)
        
        start_btn = tk.Button(control_frame, text="开始游戏", 
                             command=self.start_game,
                             bg="#4CAF50", fg="white", activebackground="#45A049",
                             font=("微软雅黑", 10, "bold"),
                             relief="raised", bd=2, cursor="hand2")
        start_btn.pack(side=tk.LEFT, padx=5)
        
        pause_btn = tk.Button(control_frame, text="暂停/继续", 
                             command=self.pause_game,
                             bg="#FF9800", fg="white", activebackground="#F57C00",
                             font=("微软雅黑", 10, "bold"),
                             relief="raised", bd=2, cursor="hand2")
        pause_btn.pack(side=tk.LEFT, padx=5)
        
        restart_btn = tk.Button(control_frame, text="重新开始", 
                               command=self.restart_game,
                               bg="#F44336", fg="white", activebackground="#D32F2F",
                               font=("微软雅黑", 10, "bold"),
                               relief="raised", bd=2, cursor="hand2")
        restart_btn.pack(side=tk.LEFT, padx=5)
        
        # 操作说明
        instruction_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        instruction_frame.pack(pady=2)
        
        instruction_label = tk.Label(instruction_frame, 
                                    text="使用方向键或WASD控制蛇的移动方向", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10))
        instruction_label.pack()
        
        # 游戏画布
        canvas_frame = tk.Frame(self.parent, bg="#F0F0F0", relief="sunken", bd=2)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_width, height=self.canvas_height,
                               bg="black", highlightthickness=0)
        self.canvas.pack(expand=True)
        
    def bind_keys(self):
        """绑定键盘事件"""
        self.parent.bind("<Key>", self.on_key_press)
        self.parent.focus_set()
    
    def on_key_press(self, event):
        """键盘按键处理"""
        key = event.keysym
        
        # 方向控制
        if key in ["Up", "w", "W"] and self.direction != "Down":
            self.next_direction = "Up"
        elif key in ["Down", "s", "S"] and self.direction != "Up":
            self.next_direction = "Down"
        elif key in ["Left", "a", "A"] and self.direction != "Right":
            self.next_direction = "Left"
        elif key in ["Right", "d", "D"] and self.direction != "Left":
            self.next_direction = "Right"
        elif key == "space":
            self.pause_game()
    
    def generate_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, (self.canvas_width // self.cell_size) - 1)
            y = random.randint(0, (self.canvas_height // self.cell_size) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def draw_game(self):
        """绘制游戏画面"""
        self.canvas.delete("all")
        
        # 绘制蛇
        for i, (x, y) in enumerate(self.snake):
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            if i == 0:  # 蛇头
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lime", outline="darkgreen", width=2)
            else:  # 蛇身
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="darkgreen")
        
        # 绘制食物
        if self.food:
            x, y = self.food
            x1 = x * self.cell_size
            y1 = y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_oval(x1, y1, x2, y2, fill="red", outline="darkred", width=2)
    
    def move_snake(self):
        """移动蛇"""
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        
        # 根据方向移动
        if self.direction == "Up":
            new_head = (head_x, head_y - 1)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 1)
        elif self.direction == "Left":
            new_head = (head_x - 1, head_y)
        elif self.direction == "Right":
            new_head = (head_x + 1, head_y)
        
        # 检查碰撞
        if self.check_collision(new_head):
            self.game_over()
            return
        
        # 添加新头部
        self.snake.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"得分: {self.score}")
            self.generate_food()
            # 增加游戏速度
            if self.game_speed > 50:
                self.game_speed -= 2
        else:
            # 移除尾部
            self.snake.pop()
    
    def check_collision(self, head):
        """检查碰撞"""
        x, y = head
        
        # 检查边界碰撞
        if (x < 0 or x >= self.canvas_width // self.cell_size or 
            y < 0 or y >= self.canvas_height // self.cell_size):
            return True
        
        # 检查自身碰撞
        if head in self.snake:
            return True
        
        return False
    
    def game_loop(self):
        """游戏主循环"""
        if self.game_running and not self.game_paused:
            self.move_snake()
            self.draw_game()
        
        if self.game_running:
            self.parent.after(self.game_speed, self.game_loop)
    
    def start_game(self):
        """开始游戏"""
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.game_loop()
    
    def pause_game(self):
        """暂停/继续游戏"""
        if self.game_running:
            self.game_paused = not self.game_paused
    
    def restart_game(self):
        """重新开始游戏"""
        self.game_running = False
        self.game_paused = False
        self.score = 0
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_speed = 150
        self.snake = [(10, 10), (10, 9), (10, 8)]
        
        self.score_label.config(text=f"得分: {self.score}")
        self.status_label.config(text="点击开始游戏按钮开始", fg=self.theme.text_color)
        self.generate_food()
        self.draw_game()
    
    def game_over(self):
        """游戏结束"""
        self.game_running = False
        self.status_label.config(text=f"💀 游戏结束！最终得分: {self.score}", fg="red")
        self.draw_game()