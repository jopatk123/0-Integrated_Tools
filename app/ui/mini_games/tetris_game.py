# -*- coding: utf-8 -*-
"""俄罗斯方块游戏模块"""

import tkinter as tk
from tkinter import messagebox
import random

class TetrisGame:
    """俄罗斯方块游戏类"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        
        # 游戏参数
        self.board_width = 10
        self.board_height = 20
        self.cell_size = 25
        self.fall_speed = 500  # 毫秒
        
        # 游戏状态
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_running = False
        self.game_paused = False
        
        # 游戏数据
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.next_piece = None
        
        # 方块形状定义
        self.shapes = {
            'I': [['.....',
                   '..#..',
                   '..#..',
                   '..#..',
                   '..#..'],
                  ['.....',
                   '.....',
                   '####.',
                   '.....',
                   '.....']],
            'O': [['.....',
                   '.....',
                   '.##..',
                   '.##..',
                   '.....']],
            'T': [['.....',
                   '.....',
                   '.#...',
                   '###..',
                   '.....'],
                  ['.....',
                   '.....',
                   '.#...',
                   '.##..',
                   '.#...'],
                  ['.....',
                   '.....',
                   '.....',
                   '###..',
                   '.#...'],
                  ['.....',
                   '.....',
                   '.#...',
                   '##...',
                   '.#...']],
            'S': [['.....',
                   '.....',
                   '.##..',
                   '##...',
                   '.....'],
                  ['.....',
                   '.....',
                   '.#...',
                   '.##..',
                   '..#..']],
            'Z': [['.....',
                   '.....',
                   '##...',
                   '.##..',
                   '.....'],
                  ['.....',
                   '.....',
                   '..#..',
                   '.##..',
                   '.#...']],
            'J': [['.....',
                   '.....',
                   '.#...',
                   '.#...',
                   '##...'],
                  ['.....',
                   '.....',
                   '.....',
                   '#....',
                   '###..'],
                  ['.....',
                   '.....',
                   '.##..',
                   '.#...',
                   '.#...'],
                  ['.....',
                   '.....',
                   '.....',
                   '###..',
                   '..#..']],
            'L': [['.....',
                   '.....',
                   '.#...',
                   '.#...',
                   '.##..'],
                  ['.....',
                   '.....',
                   '.....',
                   '###..',
                   '#....'],
                  ['.....',
                   '.....',
                   '##...',
                   '.#...',
                   '.#...'],
                  ['.....',
                   '.....',
                   '.....',
                   '..#..',
                   '###..']]}
        
        self.shape_colors = {
            'I': '#00FFFF',  # 青色
            'O': '#FFFF00',  # 黄色
            'T': '#800080',  # 紫色
            'S': '#00FF00',  # 绿色
            'Z': '#FF0000',  # 红色
            'J': '#0000FF',  # 蓝色
            'L': '#FFA500'   # 橙色
        }
        
        # 创建游戏界面
        self.create_widgets()
        self.generate_new_piece()
        
    def create_widgets(self):
        """创建游戏界面"""
        # 游戏标题
        title_label = tk.Label(self.parent, text="🧩 俄罗斯方块", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 18, "bold"))
        title_label.pack(pady=10)
        
        # 主游戏区域
        main_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧游戏板区域
        game_board_frame = tk.Frame(main_frame, bg="#F0F0F0", relief="sunken", bd=2)
        game_board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 游戏画布
        self.canvas = tk.Canvas(game_board_frame, 
                               width=self.board_width * self.cell_size,
                               height=self.board_height * self.cell_size,
                               bg="black", highlightthickness=0)
        self.canvas.pack(expand=True, padx=10, pady=10)
        
        # 右侧信息面板
        info_panel = tk.Frame(main_frame, bg=self.theme.bg_color, width=200)
        info_panel.pack(side=tk.RIGHT, fill=tk.Y)
        info_panel.pack_propagate(False)
        
        # 下一个方块预览
        next_frame = tk.LabelFrame(info_panel, text="下一个方块", 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  font=("微软雅黑", 10, "bold"))
        next_frame.pack(fill=tk.X, pady=5)
        
        # 创建预览画布
        self.next_canvas = tk.Canvas(next_frame, width=100, height=80, 
                                    bg="black", highlightthickness=0)
        self.next_canvas.pack(padx=5, pady=5)
        
        # 游戏统计
        stats_frame = tk.LabelFrame(info_panel, text="游戏统计", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 10, "bold"))
        stats_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = tk.Label(stats_frame, text=f"得分: {self.score}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor="w")
        self.score_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.level_label = tk.Label(stats_frame, text=f"等级: {self.level}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor="w")
        self.level_label.pack(fill=tk.X, padx=5, pady=2)
        
        self.lines_label = tk.Label(stats_frame, text=f"消除行数: {self.lines_cleared}", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor="w")
        self.lines_label.pack(fill=tk.X, padx=5, pady=2)
        
        # 游戏状态显示区域
        status_frame = tk.LabelFrame(info_panel, text="游戏状态", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10, "bold"))
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, text="点击开始游戏", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 9), anchor="w")
        self.status_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 控制按钮
        control_frame = tk.LabelFrame(info_panel, text="游戏控制", 
                                     bg=self.theme.bg_color, fg=self.theme.text_color,
                                     font=("微软雅黑", 10, "bold"))
        control_frame.pack(fill=tk.X, pady=5)
        
        start_btn = tk.Button(control_frame, text="开始", 
                             command=self.start_game,
                             bg="#4CAF50", fg="white", activebackground="#45A049",
                             font=("微软雅黑", 9, "bold"),
                             relief="raised", bd=2, cursor="hand2")
        start_btn.pack(fill=tk.X, padx=5, pady=2)
        
        pause_btn = tk.Button(control_frame, text="暂停", 
                             command=self.pause_game,
                             bg="#FF9800", fg="white", activebackground="#F57C00",
                             font=("微软雅黑", 9, "bold"),
                             relief="raised", bd=2, cursor="hand2")
        pause_btn.pack(fill=tk.X, padx=5, pady=2)
        
        restart_btn = tk.Button(control_frame, text="重新开始", 
                               command=self.restart_game,
                               bg="#F44336", fg="white", activebackground="#D32F2F",
                               font=("微软雅黑", 9, "bold"),
                               relief="raised", bd=2, cursor="hand2")
        restart_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # 操作说明
        help_frame = tk.LabelFrame(info_panel, text="操作说明", 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  font=("微软雅黑", 10, "bold"))
        help_frame.pack(fill=tk.X, pady=5)
        
        help_text = "A/D: 左右移动\nS: 快速下降\nW: 旋转方块\n空格: 暂停"
        help_label = tk.Label(help_frame, text=help_text, 
                             bg=self.theme.bg_color, fg=self.theme.text_color,
                             font=("微软雅黑", 8), justify=tk.LEFT)
        help_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 绑定键盘事件
        self.bind_keys()
    
    def bind_keys(self):
        """绑定键盘事件"""
        self.parent.bind("<Key>", self.on_key_press)
        self.parent.focus_set()
    
    def on_key_press(self, event):
        """键盘按键处理"""
        if not self.game_running or self.game_paused:
            return
            
        key = event.keysym.lower()
        
        if key in ['a', 'left']:
            self.move_piece(-1, 0)
        elif key in ['d', 'right']:
            self.move_piece(1, 0)
        elif key in ['s', 'down']:
            self.move_piece(0, 1)
        elif key in ['w', 'up']:
            self.rotate_piece()
        elif key == 'space':
            self.pause_game()
    
    def generate_new_piece(self):
        """生成新方块"""
        if self.next_piece is None:
            self.next_piece = random.choice(list(self.shapes.keys()))
        
        self.current_piece = self.next_piece
        self.next_piece = random.choice(list(self.shapes.keys()))
        self.current_rotation = 0
        self.current_x = self.board_width // 2 - 2
        self.current_y = 0
        
        # 检查游戏是否结束
        if self.check_collision(self.current_piece, self.current_rotation, self.current_x, self.current_y):
            self.game_over()
    
    def get_piece_shape(self, piece, rotation):
        """获取方块形状"""
        return self.shapes[piece][rotation % len(self.shapes[piece])]
    
    def check_collision(self, piece, rotation, x, y):
        """检查碰撞"""
        shape = self.get_piece_shape(piece, rotation)
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    new_x = x + j
                    new_y = y + i
                    
                    # 检查边界
                    if (new_x < 0 or new_x >= self.board_width or 
                        new_y >= self.board_height):
                        return True
                    
                    # 检查与已有方块的碰撞
                    if new_y >= 0 and self.board[new_y][new_x] != 0:
                        return True
        
        return False
    
    def move_piece(self, dx, dy):
        """移动方块"""
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        
        if not self.check_collision(self.current_piece, self.current_rotation, new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
            self.draw_game()
            return True
        return False
    
    def rotate_piece(self):
        """旋转方块"""
        new_rotation = (self.current_rotation + 1) % len(self.shapes[self.current_piece])
        
        if not self.check_collision(self.current_piece, new_rotation, self.current_x, self.current_y):
            self.current_rotation = new_rotation
            self.draw_game()
    
    def place_piece(self):
        """放置方块到游戏板"""
        shape = self.get_piece_shape(self.current_piece, self.current_rotation)
        
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    board_x = self.current_x + j
                    board_y = self.current_y + i
                    if board_y >= 0:
                        self.board[board_y][board_x] = self.current_piece
        
        # 检查并清除完整的行
        lines_cleared = self.clear_lines()
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.score += lines_cleared * 100 * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(50, 500 - (self.level - 1) * 50)
            self.update_stats()
        
        # 生成新方块
        self.generate_new_piece()
    
    def clear_lines(self):
        """清除完整的行"""
        lines_to_clear = []
        
        for i in range(self.board_height):
            if all(cell != 0 for cell in self.board[i]):
                lines_to_clear.append(i)
        
        # 移除完整的行
        for line in reversed(lines_to_clear):
            del self.board[line]
            self.board.insert(0, [0] * self.board_width)
        
        return len(lines_to_clear)
    
    def draw_game(self):
        """绘制游戏画面"""
        self.canvas.delete("all")
        
        # 绘制游戏板
        for i in range(self.board_height):
            for j in range(self.board_width):
                if self.board[i][j] != 0:
                    color = self.shape_colors.get(self.board[i][j], '#FFFFFF')
                    x1 = j * self.cell_size
                    y1 = i * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
        
        # 绘制当前方块
        if self.current_piece:
            shape = self.get_piece_shape(self.current_piece, self.current_rotation)
            color = self.shape_colors[self.current_piece]
            
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == '#':
                        x = self.current_x + j
                        y = self.current_y + i
                        if 0 <= x < self.board_width and y >= 0:
                            x1 = x * self.cell_size
                            y1 = y * self.cell_size
                            x2 = x1 + self.cell_size
                            y2 = y1 + self.cell_size
                            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
        
        # 绘制下一个方块预览
        self.draw_next_piece()
    
    def draw_next_piece(self):
        """绘制下一个方块预览"""
        self.next_canvas.delete("all")
        
        if self.next_piece:
            shape = self.get_piece_shape(self.next_piece, 0)
            color = self.shape_colors[self.next_piece]
            
            # 计算预览方块的位置（居中显示）
            preview_size = 15
            start_x = 25
            start_y = 15
            
            for i, row in enumerate(shape):
                for j, cell in enumerate(row):
                    if cell == '#':
                        x1 = start_x + j * preview_size
                        y1 = start_y + i * preview_size
                        x2 = x1 + preview_size
                        y2 = y1 + preview_size
                        self.next_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
    
    def update_stats(self):
        """更新统计信息"""
        self.score_label.config(text=f"得分: {self.score}")
        self.level_label.config(text=f"等级: {self.level}")
        self.lines_label.config(text=f"消除行数: {self.lines_cleared}")
    
    def game_loop(self):
        """游戏主循环"""
        if self.game_running and not self.game_paused:
            # 方块自动下落
            if not self.move_piece(0, 1):
                self.place_piece()
        
        if self.game_running:
            self.parent.after(self.fall_speed, self.game_loop)
    
    def start_game(self):
        """开始游戏"""
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.status_label.config(text="游戏进行中...", fg=self.theme.text_color)
            self.draw_game()
            self.game_loop()
    
    def pause_game(self):
        """暂停/继续游戏"""
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.status_label.config(text="游戏已暂停", fg="orange")
            else:
                self.status_label.config(text="游戏进行中...", fg=self.theme.text_color)
    
    def restart_game(self):
        """重新开始游戏"""
        self.game_running = False
        self.game_paused = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 500
        
        # 重置游戏板
        self.board = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        
        # 重置方块
        self.current_piece = None
        self.next_piece = None
        self.generate_new_piece()
        
        # 更新显示
        self.status_label.config(text="点击开始游戏", fg=self.theme.text_color)
        self.update_stats()
        self.draw_game()
    
    def game_over(self):
        """游戏结束"""
        self.game_running = False
        self.status_label.config(text=f"💀 游戏结束！得分: {self.score}", fg="red")
        self.draw_game()