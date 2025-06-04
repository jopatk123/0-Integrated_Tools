# -*- coding: utf-8 -*-
"""格式转换工具"""

import tkinter as tk
from tkinter import ttk
from .format_converter.converter_tab import ConverterTab
from .format_converter.image_converter_tab import ImageConverterTab
from .format_converter.video_converter_tab import VideoConverterTab
from .format_converter.audio_converter_tab import AudioConverterTab

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
        
        instruction_text = (
            "格式转换工具支持多种文件格式的相互转换：\n\n"
            "📄 文档转换：支持 Markdown 和 Word 文档的相互转换\n"
            "🖼️ 图片转换：支持常用图片格式的批量转换和处理\n"
            "🎬 视频转换：支持常用视频格式的转换和压缩\n"
            "🎵 音频转换：支持常用音频格式的转换和处理\n\n"
            "请选择相应的选项卡进行操作。"
        )
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
        
        # 文档格式转换选项卡
        converter_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(converter_frame, text="📄 文档转换")
        
        # 创建文档转换功能模块
        self.converter_tab = ConverterTab(converter_frame, self.theme)
        self.converter_tab.update_status = self.update_status
        
        # 图片格式转换选项卡
        image_converter_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(image_converter_frame, text="🖼️ 图片转换")
        
        # 创建图片转换功能模块
        self.image_converter_tab = ImageConverterTab(image_converter_frame, self.theme)
        self.image_converter_tab.update_status = self.update_status
        
        # 视频格式转换选项卡
        video_converter_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(video_converter_frame, text="🎬 视频转换")
        
        # 创建视频转换功能模块
        self.video_converter_tab = VideoConverterTab(video_converter_frame, self.theme)
        self.video_converter_tab.update_status = self.update_status
        
        # 音频格式转换选项卡
        audio_converter_frame = tk.Frame(self.notebook, bg=self.theme.bg_color)
        self.notebook.add(audio_converter_frame, text="🎵 音频转换")
        
        # 创建音频转换功能模块
        self.audio_converter_tab = AudioConverterTab(audio_converter_frame, self.theme)
        self.audio_converter_tab.update_status = self.update_status
        
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