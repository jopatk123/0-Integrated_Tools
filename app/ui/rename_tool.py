# -*- coding: utf-8 -*-
"""重命名工具"""

import tkinter as tk
from tkinter import ttk
from .rename.rename_tab import RenameTab

class RenameTool:
    """重命名工具主类"""
    
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
        
        title_label = tk.Label(title_frame, text="重命名工具", 
                              bg=self.theme.bg_color, font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=5)
        
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "重命名工具：通过Excel文件批量设置文件重命名规则，支持文件路径检测和批量重命名操作。"
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
        
        # 重命名选项卡
        rename_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(rename_frame, text="重命名")
        
        # 创建重命名功能模块
        self.rename_tab = RenameTab(rename_frame, self.theme)
        self.rename_tab.update_status = self.update_status
        
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
        
    def add_item_to_rename_list(self, path):
        """添加项目到重命名列表（向后兼容接口）"""
        if hasattr(self, 'rename_tab'):
            self.rename_tab.add_item_to_rename_list(path)