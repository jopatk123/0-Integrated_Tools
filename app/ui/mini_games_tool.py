# -*- coding: utf-8 -*-
"""小游戏工具集模块"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.ui.mini_games.minesweeper_game import MinesweeperGame
from app.ui.mini_games.snake_game import SnakeGame
from app.ui.mini_games.game2048 import Game2048
from app.ui.mini_games.tetris_game import TetrisGame

class MiniGamesTool:
    """小游戏工具集"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题框架
        title_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(title_frame, text="小游戏工具集", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=5)
        
        # 游戏按钮框架
        games_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        games_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建游戏按钮网格
        self.create_game_buttons(games_frame)
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_game_buttons(self, parent_frame):
        """创建游戏按钮"""
        # 游戏列表
        games = [
            ("🎯 扫雷", "minesweeper", "#FF6B6B"),
            ("🐍 贪吃蛇", "snake", "#4ECDC4"),
            ("🔢 2048游戏", "game2048", "#45B7D1"),
            ("🧩 俄罗斯方块", "tetris", "#96CEB4")
        ]
        
        # 创建按钮容器
        button_container = tk.Frame(parent_frame, bg=self.theme.bg_color)
        button_container.pack(expand=True)
        
        # 创建游戏按钮（2x2布局）
        for i, (text, game_type, color) in enumerate(games):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(button_container, text=text,
                           command=lambda gt=game_type: self.launch_game(gt),
                           bg=color, fg="white", activebackground=self._darken_color(color),
                           font=("微软雅黑", 14, "bold"),
                           relief="raised", bd=3, cursor="hand2",
                           width=15, height=3)
            btn.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
            
        # 配置网格权重
        for i in range(2):
            button_container.grid_rowconfigure(i, weight=1)
            button_container.grid_columnconfigure(i, weight=1)
            
    def _darken_color(self, color):
        """将颜色变暗用于按钮激活状态"""
        color_map = {
            "#FF6B6B": "#E55555",
            "#4ECDC4": "#3BB5AD",
            "#45B7D1": "#3A9BC1",
            "#96CEB4": "#7FB89A"
        }
        return color_map.get(color, color)
        
    def launch_game(self, game_type):
        """启动游戏"""
        game_names = {
            "minesweeper": "扫雷",
            "snake": "贪吃蛇",
            "game2048": "2048游戏",
            "tetris": "俄罗斯方块"
        }
        
        game_name = game_names.get(game_type, "未知游戏")
        
        # 创建游戏窗口
        game_window = tk.Toplevel(self.parent)
        game_window.title(f"{game_name} - 小游戏")
        game_window.geometry("600x700")
        game_window.configure(bg=self.theme.bg_color)
        game_window.resizable(True, True)
        
        # 设置窗口图标（可选）
        try:
            game_window.iconbitmap(default=None)
        except:
            pass
            
        # 根据游戏类型创建对应的游戏界面
        if game_type == "minesweeper":
            MinesweeperGame(game_window, self.theme)
        elif game_type == "snake":
            SnakeGame(game_window, self.theme)
        elif game_type == "game2048":
            Game2048(game_window, self.theme)
        elif game_type == "tetris":
            TetrisGame(game_window, self.theme)
            
        # 更新状态
        self.update_status(f"已启动{game_name}游戏")
        

        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = tk.Frame(self.parent, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="准备就绪 - 选择一个游戏开始娱乐吧！")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor=tk.W, padx=10)
        self.status_label.pack(fill=tk.X)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)
        self.parent.update_idletasks()

def main():
    """主函数"""
    root = tk.Tk()
    root.title("小游戏工具集")
    root.geometry("800x600")
    root.configure(bg="#2C3E50")
    
    # 创建主题
    class Theme:
        def __init__(self):
            self.bg_color = "#2C3E50"
            self.text_color = "#FFFFFF"
            self.button_color = "#3498DB"
            self.button_text_color = "#FFFFFF"
    
    theme = Theme()
    
    # 创建小游戏工具
    app = MiniGamesTool(root, theme)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()