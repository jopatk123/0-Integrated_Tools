#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片处理工具集
整合了图片GPS提取和图片处理功能的统一界面
"""

import tkinter as tk
from tkinter import ttk
from .image_processor.processor_tab import ProcessorTab
from .image_processor.gps_extractor_tab import GPSExtractorTab

class ImageProcessorTool:
    """统一的图片处理工具集"""
    
    def __init__(self, parent_frame, theme, config=None):
        self.parent_frame = parent_frame
        self.theme = theme
        self.config = config
        
        # 创建界面组件
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题框架
        title_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(title_frame, text="图片处理工具集", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=5)
        
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "图片处理工具集：提供图片GPS坐标提取、批量图片处理、尺寸调整、裁剪、旋转、压缩、哈希修改等功能。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  justify=tk.LEFT, wraplength=980,
                                  font=("微软雅黑", 10))
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 创建选项卡
        self.create_notebook()
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_notebook(self):
        """创建选项卡"""
        # 选项卡框架
        notebook_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # GPS提取选项卡
        gps_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(gps_frame, text="📍 GPS提取")
        
        # 创建GPS提取功能模块
        self.gps_extractor_tab = GPSExtractorTab(gps_frame, self.theme)
        self.gps_extractor_tab.update_status = self.update_status
        
        # 图片处理选项卡
        processor_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(processor_frame, text="🖼️ 图片处理")
        
        # 创建图片处理功能模块
        # 为ProcessorTab创建一个临时的notebook来兼容其原有设计
        temp_notebook = ttk.Notebook(processor_frame)
        temp_notebook.pack(fill=tk.BOTH, expand=True)
        
        self.processor_tab = ProcessorTab(processor_frame, temp_notebook, self.theme, self.config)
        self.processor_tab.update_status = self.update_status
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor=tk.W, padx=10)
        self.status_label.pack(fill=tk.X)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)
        self.parent_frame.update_idletasks()