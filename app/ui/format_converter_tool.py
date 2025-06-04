# -*- coding: utf-8 -*-
"""格式转换工具"""

import tkinter as tk
from tkinter import ttk
from .format_converter.converter_tab import ConverterTab

class FormatConverterTool:
    """格式转换工具主类"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 标题框架
        title_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=5)
        
        title_label = tk.Label(title_frame, text="格式转换工具", 
                              bg=self.theme.bg_color, font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=5)
        
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "格式转换工具：支持Markdown与Word文档之间的相互转换。选择源文件和目标格式，点击转换即可。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980,
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
        
        # 格式转换选项卡
        converter_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(converter_frame, text="格式转换")
        
        # 创建转换功能模块
        self.converter_tab = ConverterTab(converter_frame, self.theme)
        self.converter_tab.update_status = self.update_status
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                   bg=self.theme.bg_color, anchor=tk.W, padx=10)
        self.status_label.pack(fill=tk.X)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)