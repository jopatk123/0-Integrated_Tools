#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""系统文件处理工具集 - 整合了文件路径获取、重命名、整理、时间分类功能"""

import tkinter as tk
from tkinter import ttk
from config import config
from .system_files.path_tab import PathTab
from .system_files.rename_tab import RenameTab
from .system_files.organizer_tab import OrganizerTab
from .system_files.sorter_tab import SorterTab

class SystemFileTool:
    """系统文件处理工具集主类"""
    
    def __init__(self, parent_frame, theme, config):
        self.parent_frame = parent_frame
        self.theme = theme
        self.config = config
        
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
        
        title_label = tk.Label(title_frame, text="🗂️ 系统文件处理工具集", 
                              font=("微软雅黑", 16, "bold"),
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack()
        
    def create_instruction_frame(self):
        """创建使用说明框架"""
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instruction_text = "📋 集成了文件路径获取、批量重命名、文件整理、时间分类等功能的完整文件管理解决方案。通过选项卡切换不同功能，支持文件批量处理和工作流整合。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, fg=self.theme.accent_color,
                                  justify=tk.LEFT, wraplength=980, font=("微软雅黑", 10))
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
    def create_tabs(self):
        """创建选项卡"""
        # 选项卡框架
        notebook_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各功能选项卡的框架
        self.path_frame = ttk.Frame(self.notebook)
        self.rename_frame = ttk.Frame(self.notebook)
        self.organizer_frame = ttk.Frame(self.notebook)
        self.sorter_frame = ttk.Frame(self.notebook)
        
        # 添加选项卡
        self.notebook.add(self.path_frame, text="📁 路径获取")
        self.notebook.add(self.rename_frame, text="✏️ 批量重命名")
        self.notebook.add(self.organizer_frame, text="📂 文件整理")
        self.notebook.add(self.sorter_frame, text="⏰ 时间分类")
        
        # 创建各功能模块
        self.create_path_tab()
        self.create_rename_tab()
        self.create_organizer_tab()
        self.create_sorter_tab()
        
    def create_path_tab(self):
        """创建文件路径获取选项卡"""
        self.path_tab = PathTab(self.path_frame, self.theme, self.notebook, self)
        
    def create_rename_tab(self):
        """创建批量重命名选项卡"""
        self.rename_tab = RenameTab(self.rename_frame, self.theme)
        # 设置状态更新回调
        self.rename_tab.update_status = self.update_status
        
    def create_organizer_tab(self):
        """创建文件整理选项卡"""
        # 创建一个临时的notebook用于OrganizerTab
        temp_notebook = ttk.Notebook(self.organizer_frame)
        temp_notebook.pack(fill=tk.BOTH, expand=True)
        
        self.organizer_tab = OrganizerTab(self.organizer_frame, temp_notebook, self.theme, self.config)
        # 设置状态更新回调
        self.organizer_tab.update_status = self.update_status
        
    def create_sorter_tab(self):
        """创建时间分类选项卡"""
        self.sorter_tab = SorterTab(self.sorter_frame, self.theme)
        
    def create_status_bar(self):
        """创建状态栏"""
        status_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               bg=self.theme.bg_color, fg=self.theme.text_color,
                               font=("微软雅黑", 9))
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_var.set(message)
        self.parent_frame.update_idletasks()
        
    def get_rename_tool(self):
        """获取重命名工具实例，供文件路径工具使用"""
        return self.rename_tab if hasattr(self, 'rename_tab') else None