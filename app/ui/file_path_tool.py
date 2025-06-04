# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from config import config
from .file_path.path_tab import PathTab

class FilePathTool:
    def __init__(self, parent_frame, theme, notebook, rename_tool=None):
        self.parent_frame = parent_frame
        self.theme = theme
        self.notebook = notebook
        self.rename_tool = rename_tool
        
        # 初始化状态变量
        self.status_var = tk.StringVar(value="就绪")
        
        # 设置窗口
        self.setup_window()
        
        # 创建界面组件
        self.create_title_frame()
        self.create_instruction_frame()
        self.create_tabs()
        self.create_status_bar()
        
    def setup_window(self):
        """设置窗口属性"""
        # ttk.Frame不支持bg选项，跳过背景色设置
        pass
        
    def create_title_frame(self):
        """创建标题框架"""
        title_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        title_frame.pack(fill=tk.X, pady=(10, 5))
        
        title_label = tk.Label(title_frame, text="文件路径工具", 
                              font=("Arial", 16, "bold"),
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack()
        
    def create_instruction_frame(self):
        """创建使用说明框架"""
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "使用说明：选择文件夹路径后，可以扫描文件或文件夹，支持文件过滤和子文件夹包含选项。扫描结果可复制路径、导出或添加到重命名工具。点击列标题可以按该列进行排序。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980)
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
    def create_tabs(self):
        """创建选项卡"""
        # 创建Notebook
        self.tab_notebook = ttk.Notebook(self.parent_frame)
        self.tab_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建文件路径选项卡
        path_frame = tk.Frame(self.tab_notebook, bg=self.theme.bg_color)
        self.tab_notebook.add(path_frame, text="文件路径扫描")
        
        # 创建PathTab实例
        self.path_tab = PathTab(path_frame, self.theme, self.notebook, self.rename_tool)
        
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = ttk.Label(self.parent_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)