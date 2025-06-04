# -*- coding: utf-8 -*-
"""文件排序工具"""

import tkinter as tk
from tkinter import ttk
from config import config
from .file_sorter.sorter_tab import SorterTab

class FileSorterTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_frame = ttk.Frame(self.parent_frame, padding="10")
        title_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(title_frame, text="文件排序工具", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # 使用说明
        desc_frame = ttk.Frame(self.parent_frame, padding="10")
        desc_frame.pack(fill=tk.X)
        
        desc_text = "根据文件修改时间自动分组整理文件，相近时间的文件会被归类到同一文件夹中。"
        desc_label = ttk.Label(desc_frame, text=desc_text, 
                              foreground="gray", wraplength=600)
        desc_label.pack(side=tk.LEFT)
        
        # 创建选项卡
        notebook = ttk.Notebook(self.parent_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文件排序选项卡
        sorter_frame = ttk.Frame(notebook)
        notebook.add(sorter_frame, text="文件排序")
        
        # 创建排序功能模块
        self.sorter_tab = SorterTab(sorter_frame, self.theme)
        
        # 状态栏
        self.create_status_bar()
    
    def create_status_bar(self):
        self.status_frame = ttk.Frame(self.parent_frame)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def update_status(self, message):
        self.status_label.config(text=message)