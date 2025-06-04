# -*- coding: utf-8 -*-
"""Excel图片提取工具主类 - 重构后的版本"""

import tkinter as tk
from tkinter import ttk
from config import config
from .excel_image_extractor.extractor_tab import ExtractorTab

class ExcelImageExtractorTool:
    """Excel图片提取工具主类 - 重构后的版本"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.status_text = tk.StringVar(value="就绪")
        
        # 初始化配置
        self.config = config
        
        # 设置UI
        self.setup_ui()
    
    def setup_ui(self):
        """设置主界面"""
        # 创建主框架
        main_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, text="📊 Excel图片提取工具", 
                              font=("微软雅黑", 16, "bold"), 
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack(pady=10)
        
        # 功能说明
        info_label = tk.Label(main_frame, 
                             text="📋 从Excel文件中提取所有图片，支持预览和批量导出",
                             font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.accent_color)
        info_label.pack(pady=(0, 10))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建提取选项卡
        self.extractor_tab = ExtractorTab(self.parent, self.notebook, self.theme, self.config)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
        # 设置状态更新回调
        self.extractor_tab.update_status = self.update_status
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = tk.Frame(parent, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 状态文本
        status_label = tk.Label(status_frame, textvariable=self.status_text,
                               font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.text_color)
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_text.set(message)