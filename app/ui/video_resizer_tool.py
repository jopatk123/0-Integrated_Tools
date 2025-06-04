# -*- coding: utf-8 -*-
"""视频调整工具"""

import tkinter as tk
from tkinter import ttk
from .video_resizer.feature_tab import VideoResizerFeatureTab
from ..utils.theme import ThemeManager

class VideoResizerTool:
    """视频调整工具主类"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 创建界面组件
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题
        title_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(title_frame, text="视频调整工具", 
                              font=("Arial", 16, "bold"),
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack(pady=5)
        
        # 使用说明
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "使用说明：选择要压缩的视频文件或文件夹，设置输出目录和压缩程度，然后点击'开始压缩'按钮。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  justify=tk.LEFT, wraplength=980)
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(self.parent_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 视频调整选项卡
        self.video_resizer_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(self.video_resizer_frame, text="视频压缩")
        
        # 创建功能模块
        self.feature_tab = VideoResizerFeatureTab(self.video_resizer_frame, self.theme)
        self.feature_tab.update_status = self.update_status
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(self.status_frame, text="就绪", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   anchor=tk.W)
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
    
    def update_status(self, message):
        """更新状态栏信息"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)