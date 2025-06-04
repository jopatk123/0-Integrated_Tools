# -*- coding: utf-8 -*-
"""
图像处理工具
支持批量图像处理，包括尺寸调整、裁剪、旋转、压缩等功能
"""

import tkinter as tk
from tkinter import ttk
from config import config
from .image_processor.processor_tab import ProcessorTab

class ImageProcessorTool:
    def __init__(self, parent, theme, config):
        self.parent = parent
        self.theme = theme
        self.config = config
        
        # 直接使用传入的parent框架，不创建新窗口
        self.window = parent
        
        # 创建界面
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 主内容区域
        content_frame = tk.Frame(self.window, bg=self.theme.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建处理选项卡
        self.processor_tab = ProcessorTab(self.window, self.notebook, self.theme, self.config)
        self.processor_tab.update_status = self.update_status
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.window, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(status_frame, textvariable=self.status_var, 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 9), anchor=tk.W)
        status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_var.set(message)