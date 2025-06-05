# -*- coding: utf-8 -*-
"""扫雷游戏模块"""

import tkinter as tk
from tkinter import messagebox
import random

class MinesweeperGame:
    """扫雷游戏类"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        
        # 难度等级配置
        self.difficulty_levels = {
            "初级": {"rows": 9, "cols": 9, "mines": 10},
            "中级": {"rows": 16, "cols": 16, "mines": 40},
            "高级": {"rows": 16, "cols": 30, "mines": 99}
        }
        self.current_difficulty = "初级"
        
        # 游戏参数
        self.rows = 9
        self.cols = 9
        self.mines = 10
        
        # 游戏状态
        self.game_over = False
        self.first_click = True
        self.flags_count = 0
        
        # 游戏数据
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.buttons = []
        
        # 创建游戏界面
        self.create_widgets()
        self.init_game()
        
    def create_widgets(self):
        """创建游戏界面"""
        # 游戏标题
        title_label = tk.Label(self.parent, text="🎯 扫雷游戏", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=10)
        
        # 难度选择栏
        difficulty_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        difficulty_frame.pack(pady=5)
        
        tk.Label(difficulty_frame, text="难度等级:", 
                bg=self.theme.bg_color, fg=self.theme.text_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        for difficulty in self.difficulty_levels.keys():
            rb = tk.Radiobutton(difficulty_frame, text=difficulty, 
                               variable=self.difficulty_var, value=difficulty,
                               command=self.change_difficulty,
                               bg=self.theme.bg_color, fg=self.theme.text_color,
                               selectcolor=self.theme.bg_color,
                               font=("微软雅黑", 9))
            rb.pack(side=tk.LEFT, padx=5)
        
        # 游戏信息栏
        info_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        info_frame.pack(pady=5)
        
        self.mines_label = tk.Label(info_frame, text=f"剩余地雷: {self.mines}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 12))
        self.mines_label.pack(side=tk.LEFT, padx=10)
        
        restart_btn = tk.Button(info_frame, text="重新开始", 
                               command=self.restart_game,
                               bg="#4CAF50", fg="white", activebackground="#45A049",
                               font=("微软雅黑", 10, "bold"),
                               relief="raised", bd=2, cursor="hand2")
        restart_btn.pack(side=tk.RIGHT, padx=10)
        
        # 游戏状态显示区域
        self.status_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        self.status_frame.pack(pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="点击任意格子开始游戏", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 12, "bold"))
        self.status_label.pack()
        
        # 游戏区域
        self.game_frame = tk.Frame(self.parent, bg="#C0C0C0", relief="sunken", bd=2)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 创建游戏网格
        self.create_game_grid()
        
    def create_game_grid(self):
        """创建游戏网格"""
        self.buttons = []
        for i in range(self.rows):
            button_row = []
            for j in range(self.cols):
                btn = tk.Button(self.game_frame, width=2, height=1,
                               font=("微软雅黑", 10, "bold"),
                               relief="raised", bd=2)
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, r=i, c=j: self.left_click(r, c))
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.right_click(r, c))
                button_row.append(btn)
            self.buttons.append(button_row)
    
    def init_game(self):
        """初始化游戏"""
        self.game_over = False
        self.first_click = True
        self.flags_count = 0
        
        # 重置游戏数据
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 重置按钮状态
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].config(text="", bg="SystemButtonFace", state="normal")
        
        self.update_mines_label()
    
    def generate_mines(self, first_row, first_col):
        """生成地雷（避开第一次点击的位置）"""
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # 避开第一次点击的位置和已有地雷的位置
            if (row != first_row or col != first_col) and self.board[row][col] != -1:
                self.board[row][col] = -1  # -1表示地雷
                mines_placed += 1
        
        # 计算每个格子周围的地雷数量
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != -1:
                    count = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols and self.board[ni][nj] == -1:
                                count += 1
                    self.board[i][j] = count
    
    def left_click(self, row, col):
        """左键点击处理"""
        if self.game_over or self.revealed[row][col] or self.flagged[row][col]:
            return
        
        # 第一次点击时生成地雷
        if self.first_click:
            self.generate_mines(row, col)
            self.first_click = False
        
        self.reveal_cell(row, col)
        self.check_win_condition()
    
    def right_click(self, row, col):
        """右键点击处理（标记/取消标记）"""
        if self.game_over or self.revealed[row][col]:
            return
        
        if self.flagged[row][col]:
            # 取消标记
            self.flagged[row][col] = False
            self.buttons[row][col].config(text="", bg="SystemButtonFace")
            self.flags_count -= 1
        else:
            # 标记为地雷
            self.flagged[row][col] = True
            self.buttons[row][col].config(text="🚩", bg="yellow")
            self.flags_count += 1
        
        self.update_mines_label()
        self.status_label.config(text="点击任意格子开始游戏", fg=self.theme.text_color)
    
    def change_difficulty(self):
        """切换难度等级"""
        new_difficulty = self.difficulty_var.get()
        if new_difficulty != self.current_difficulty:
            self.current_difficulty = new_difficulty
            config = self.difficulty_levels[new_difficulty]
            self.rows = config["rows"]
            self.cols = config["cols"]
            self.mines = config["mines"]
            
            # 重新创建游戏网格
            for widget in self.game_frame.winfo_children():
                widget.destroy()
            self.create_game_grid()
            self.init_game()
    
    def reveal_cell(self, row, col):
        """揭开格子"""
        if self.revealed[row][col]:
            return
        
        self.revealed[row][col] = True
        
        if self.board[row][col] == -1:
            # 踩到地雷
            self.buttons[row][col].config(text="💣", bg="red")
            self.game_over = True
            self.show_all_mines()
            self.status_label.config(text="💥 踩到地雷了！游戏结束", fg="red")
        elif self.board[row][col] == 0:
            # 空格子，自动揭开周围的格子
            self.buttons[row][col].config(text="", bg="lightgray", relief="sunken")
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    ni, nj = row + di, col + dj
                    if 0 <= ni < self.rows and 0 <= nj < self.cols:
                        self.reveal_cell(ni, nj)
        else:
            # 数字格子
            colors = ["", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
            color = colors[self.board[row][col]] if self.board[row][col] < len(colors) else "black"
            self.buttons[row][col].config(text=str(self.board[row][col]), 
                                         bg="lightgray", fg=color, relief="sunken")
    
    def show_all_mines(self):
        """显示所有地雷"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1 and not self.revealed[i][j]:
                    if self.flagged[i][j]:
                        self.buttons[i][j].config(text="✓", bg="green")  # 正确标记
                    else:
                        self.buttons[i][j].config(text="💣", bg="lightcoral")
                elif self.flagged[i][j] and self.board[i][j] != -1:
                    self.buttons[i][j].config(text="❌", bg="orange")  # 错误标记
    
    def check_win_condition(self):
        """检查胜利条件"""
        if self.game_over:
            return
        
        # 检查是否所有非地雷格子都被揭开
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != -1 and not self.revealed[i][j]:
                    return  # 还有未揭开的非地雷格子
        
        # 胜利
        self.game_over = True
        self.status_label.config(text="🎉 恭喜你！成功扫除所有地雷！", fg="green")
    
    def update_mines_label(self):
        """更新地雷计数标签"""
        remaining = self.mines - self.flags_count
        self.mines_label.config(text=f"剩余地雷: {remaining}")
    
    def restart_game(self):
        """重新开始游戏"""
        self.init_game()