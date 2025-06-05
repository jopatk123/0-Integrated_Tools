# -*- coding: utf-8 -*-
"""2048游戏模块"""

import tkinter as tk
from tkinter import messagebox
import random
import copy

class Game2048:
    """2048游戏类"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        
        # 游戏参数
        self.grid_size = 4
        self.cell_size = 80
        
        # 游戏状态
        self.score = 0
        self.best_score = 0
        self.game_over = False
        
        # 游戏数据
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.previous_grid = None
        self.previous_score = 0
        
        # 颜色配置
        self.colors = {
            0: ("#CDC1B4", "#776E65"),
            2: ("#EEE4DA", "#776E65"),
            4: ("#EDE0C8", "#776E65"),
            8: ("#F2B179", "#F9F6F2"),
            16: ("#F59563", "#F9F6F2"),
            32: ("#F67C5F", "#F9F6F2"),
            64: ("#F65E3B", "#F9F6F2"),
            128: ("#EDCF72", "#F9F6F2"),
            256: ("#EDCC61", "#F9F6F2"),
            512: ("#EDC850", "#F9F6F2"),
            1024: ("#EDC53F", "#F9F6F2"),
            2048: ("#EDC22E", "#F9F6F2")
        }
        
        # 创建游戏界面
        self.create_widgets()
        self.new_game()
        
    def create_widgets(self):
        """创建游戏界面"""
        # 游戏标题
        title_label = tk.Label(self.parent, text="🔢 2048游戏", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=10)
        
        # 游戏信息栏
        info_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        info_frame.pack(pady=5)
        
        # 得分显示
        score_frame = tk.Frame(info_frame, bg=self.theme.bg_color)
        score_frame.pack(side=tk.LEFT, padx=10)
        
        self.score_label = tk.Label(score_frame, text=f"得分: {self.score}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 12))
        self.score_label.pack()
        
        self.best_label = tk.Label(score_frame, text=f"最高: {self.best_score}", 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  font=("微软雅黑", 10))
        self.best_label.pack()
        
        # 游戏状态显示区域
        self.status_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        self.status_frame.pack(pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="使用方向键或WASD移动方块", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 12, "bold"))
        self.status_label.pack()
        
        # 控制按钮
        control_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        control_frame.pack(pady=5)
        
        new_game_btn = tk.Button(control_frame, text="新游戏", 
                                command=self.new_game,
                                bg="#4CAF50", fg="white", activebackground="#45A049",
                                font=("微软雅黑", 10, "bold"),
                                relief="raised", bd=2, cursor="hand2")
        new_game_btn.pack(side=tk.LEFT, padx=5)
        
        undo_btn = tk.Button(control_frame, text="撤销", 
                            command=self.undo_move,
                            bg="#FF9800", fg="white", activebackground="#F57C00",
                            font=("微软雅黑", 10, "bold"),
                            relief="raised", bd=2, cursor="hand2")
        undo_btn.pack(side=tk.LEFT, padx=5)
        
        # 游戏说明
        instruction_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        instruction_frame.pack(pady=5)
        
        instruction_label = tk.Label(instruction_frame, 
                                    text="使用方向键或WASD移动方块，相同数字合并得分！", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10))
        instruction_label.pack()
        
        # 游戏区域
        game_frame = tk.Frame(self.parent, bg="#BBADA0", relief="raised", bd=5)
        game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建游戏网格
        self.create_game_grid(game_frame)
        
        # 绑定键盘事件
        self.bind_keys()
        
    def create_game_grid(self, parent):
        """创建游戏网格"""
        self.grid_frame = tk.Frame(parent, bg="#BBADA0")
        self.grid_frame.pack(expand=True)
        
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                cell = tk.Label(self.grid_frame, text="", 
                               width=6, height=3,
                               font=("微软雅黑", 20, "bold"),
                               relief="raised", bd=2)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)
    
    def bind_keys(self):
        """绑定键盘事件"""
        self.parent.bind("<Key>", self.on_key_press)
        self.parent.focus_set()
    
    def on_key_press(self, event):
        """键盘按键处理"""
        if self.game_over:
            return
            
        key = event.keysym.lower()
        moved = False
        
        if key in ["up", "w"]:
            moved = self.move_up()
        elif key in ["down", "s"]:
            moved = self.move_down()
        elif key in ["left", "a"]:
            moved = self.move_left()
        elif key in ["right", "d"]:
            moved = self.move_right()
        
        if moved:
            self.add_random_tile()
            self.update_display()
            if self.check_game_over():
                self.game_over = True
                self.status_label.config(text=f"💀 游戏结束！最终得分: {self.score}", fg="red")
            elif self.check_win():
                self.status_label.config(text="🎉 恭喜你达到2048！", fg="green")
    
    def new_game(self):
        """开始新游戏"""
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.previous_grid = None
        self.previous_score = 0
        
        # 添加两个初始方块
        self.add_random_tile()
        self.add_random_tile()
        
        self.status_label.config(text="使用方向键或WASD移动方块", fg=self.theme.text_color)
        self.update_display()
    
    def add_random_tile(self):
        """添加随机方块"""
        empty_cells = [(i, j) for i in range(self.grid_size) 
                      for j in range(self.grid_size) if self.grid[i][j] == 0]
        
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
    
    def update_display(self):
        """更新显示"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value == 0:
                    self.cells[i][j].config(text="", bg="#CDC1B4")
                else:
                    bg_color, fg_color = self.colors.get(value, ("#3C3A32", "#F9F6F2"))
                    self.cells[i][j].config(text=str(value), bg=bg_color, fg=fg_color)
        
        self.score_label.config(text=f"得分: {self.score}")
        self.best_label.config(text=f"最高: {max(self.best_score, self.score)}")
    
    def move_left(self):
        """向左移动"""
        self.save_state()
        moved = False
        
        for i in range(self.grid_size):
            # 移动非零元素到左边
            row = [cell for cell in self.grid[i] if cell != 0]
            
            # 合并相同的相邻元素
            j = 0
            while j < len(row) - 1:
                if row[j] == row[j + 1]:
                    row[j] *= 2
                    self.score += row[j]
                    row.pop(j + 1)
                j += 1
            
            # 填充剩余位置为0
            row.extend([0] * (self.grid_size - len(row)))
            
            # 检查是否有变化
            if row != self.grid[i]:
                moved = True
                self.grid[i] = row
        
        return moved
    
    def move_right(self):
        """向右移动"""
        self.save_state()
        moved = False
        
        for i in range(self.grid_size):
            # 移动非零元素到右边
            row = [cell for cell in self.grid[i] if cell != 0]
            
            # 合并相同的相邻元素（从右到左）
            j = len(row) - 1
            while j > 0:
                if row[j] == row[j - 1]:
                    row[j] *= 2
                    self.score += row[j]
                    row.pop(j - 1)
                    j -= 1
                j -= 1
            
            # 在左边填充0
            row = [0] * (self.grid_size - len(row)) + row
            
            # 检查是否有变化
            if row != self.grid[i]:
                moved = True
                self.grid[i] = row
        
        return moved
    
    def move_up(self):
        """向上移动"""
        self.save_state()
        moved = False
        
        for j in range(self.grid_size):
            # 获取列
            column = [self.grid[i][j] for i in range(self.grid_size)]
            
            # 移动非零元素到上边
            column = [cell for cell in column if cell != 0]
            
            # 合并相同的相邻元素
            i = 0
            while i < len(column) - 1:
                if column[i] == column[i + 1]:
                    column[i] *= 2
                    self.score += column[i]
                    column.pop(i + 1)
                i += 1
            
            # 填充剩余位置为0
            column.extend([0] * (self.grid_size - len(column)))
            
            # 检查是否有变化并更新列
            for i in range(self.grid_size):
                if self.grid[i][j] != column[i]:
                    moved = True
                self.grid[i][j] = column[i]
        
        return moved
    
    def move_down(self):
        """向下移动"""
        self.save_state()
        moved = False
        
        for j in range(self.grid_size):
            # 获取列
            column = [self.grid[i][j] for i in range(self.grid_size)]
            
            # 移动非零元素到下边
            column = [cell for cell in column if cell != 0]
            
            # 合并相同的相邻元素（从下到上）
            i = len(column) - 1
            while i > 0:
                if column[i] == column[i - 1]:
                    column[i] *= 2
                    self.score += column[i]
                    column.pop(i - 1)
                    i -= 1
                i -= 1
            
            # 在上边填充0
            column = [0] * (self.grid_size - len(column)) + column
            
            # 检查是否有变化并更新列
            for i in range(self.grid_size):
                if self.grid[i][j] != column[i]:
                    moved = True
                self.grid[i][j] = column[i]
        
        return moved
    
    def save_state(self):
        """保存当前状态用于撤销"""
        self.previous_grid = copy.deepcopy(self.grid)
        self.previous_score = self.score
    
    def undo_move(self):
        """撤销上一步"""
        if self.previous_grid is not None:
            self.grid = copy.deepcopy(self.previous_grid)
            self.score = self.previous_score
            self.game_over = False
            self.update_display()
            self.previous_grid = None
    
    def check_game_over(self):
        """检查游戏是否结束"""
        # 检查是否有空格
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    return False
        
        # 检查是否可以合并
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current = self.grid[i][j]
                # 检查右边
                if j < self.grid_size - 1 and self.grid[i][j + 1] == current:
                    return False
                # 检查下边
                if i < self.grid_size - 1 and self.grid[i + 1][j] == current:
                    return False
        
        return True
    
    def check_win(self):
        """检查是否获胜（达到2048）"""
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 2048:
                    return True
        return False