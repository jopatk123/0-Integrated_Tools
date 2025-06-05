# -*- coding: utf-8 -*-
"""计算工具集"""

import tkinter as tk
from tkinter import ttk
from .calculation.calculator_tab import CalculatorTab
from .calculation.number_converter_tab import NumberConverterTab

class CalculationTool:
    """统一的计算工具集"""
    
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
        
        title_label = tk.Label(title_frame, text="计算工具集", 
                              bg=self.theme.bg_color, fg=self.theme.text_color,
                              font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=5)
        

        
        # 创建选项卡
        self.create_notebook()
        
        # 创建状态栏
        self.create_status_bar()
        
    def create_notebook(self):
        """创建选项卡"""
        # 选项卡框架
        notebook_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建选项卡控件
        self.sub_notebook = ttk.Notebook(notebook_frame)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 计算器选项卡
        calculator_frame = tk.Frame(self.sub_notebook, bg=self.theme.bg_color)
        self.sub_notebook.add(calculator_frame, text="🧮 计算器")
        
        # 创建计算器功能模块
        self.calculator_tab = CalculatorTab(calculator_frame, self.theme)
        self.calculator_tab.update_status = self.update_status
        
        # 数字转换选项卡
        converter_frame = tk.Frame(self.sub_notebook, bg=self.theme.bg_color)
        self.sub_notebook.add(converter_frame, text="🔢 数字转换")
        
        # 创建数字转换功能模块
        self.converter_tab = NumberConverterTab(converter_frame, self.theme)
        self.converter_tab.update_status = self.update_status
        
    def create_status_bar(self):
        """创建状态栏"""
        self.status_frame = tk.Frame(self.parent, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_var = tk.StringVar(value="准备就绪")
        self.status_label = tk.Label(self.status_frame, textvariable=self.status_var, 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), anchor=tk.W, padx=10)
        self.status_label.pack(fill=tk.X)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)
        self.parent.update_idletasks()