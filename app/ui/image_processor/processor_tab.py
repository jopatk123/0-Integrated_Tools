# -*- coding: utf-8 -*-
"""图像处理工具核心功能模块"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading
import queue
import os
import random
import math
import piexif
from datetime import datetime
import string

class ProcessorTab:
    """图像处理选项卡"""
    
    def __init__(self, parent, notebook, theme, config):
        self.parent = parent
        self.notebook = notebook
        self.theme = theme
        self.config = config
        self.update_status = None  # 状态更新回调函数
        
        # 初始化变量
        self.images_queue = queue.Queue()
        self.processed_images = []
        self.current_image_index = 0
        self.compress_count = 0
        
        # 创建选项卡
        self.tab_frame = ttk.Frame(notebook)
        notebook.add(self.tab_frame, text="🖼️ 图像处理")
        
        # 创建界面
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 主框架
        main_frame = tk.Frame(self.tab_frame, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧控制面板
        self.create_control_panel(main_frame)
        
        # 右侧预览面板
        self.create_preview_panel(main_frame)
    
    def create_control_panel(self, parent):
        """创建控制面板"""
        control_frame = tk.LabelFrame(parent, text="🎛️ 控制面板", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10, "bold"))
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.configure(width=300)
        
        # 文件选择区域
        self.create_file_selection(control_frame)
        
        # 功能选项卡
        self.create_function_notebook(control_frame)
    
    def create_file_selection(self, parent):
        """创建文件选择区域"""
        file_frame = tk.LabelFrame(parent, text="📁 文件选择", 
                                 bg=self.theme.bg_color, fg=self.theme.text_color,
                                 font=("微软雅黑", 9, "bold"))
        file_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 文件夹路径
        path_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.folder_path = tk.StringVar()
        path_entry = tk.Entry(path_frame, textvariable=self.folder_path, 
                            font=("微软雅黑", 9), bg="white")
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_btn = tk.Button(path_frame, text="浏览", command=self.browse_folder,
                             bg=self.theme.button_color, fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 选项和加载按钮
        options_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.include_subfolders = tk.BooleanVar(value=True)
        subfolder_cb = tk.Checkbutton(options_frame, text="包含子文件夹", 
                                    variable=self.include_subfolders,
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 9))
        subfolder_cb.pack(side=tk.LEFT)
        
        load_btn = tk.Button(options_frame, text="🔄 加载图片", command=self.load_images,
                           bg=self.theme.accent_color, fg="white",
                           font=("微软雅黑", 9, "bold"), relief=tk.RAISED, bd=2)
        load_btn.pack(side=tk.RIGHT)
    
    def create_function_notebook(self, parent):
        """创建功能选项卡"""
        func_notebook = ttk.Notebook(parent)
        func_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 基础处理选项卡
        self.create_basic_tab(func_notebook)
        
        # 高级处理选项卡
        self.create_advanced_tab(func_notebook)
        
        # 输出设置选项卡
        self.create_output_tab(func_notebook)
    
    def create_basic_tab(self, notebook):
        """创建基础处理选项卡"""
        basic_frame = tk.Frame(notebook, bg=self.theme.bg_color)
        notebook.add(basic_frame, text="基础处理")
        
        # 尺寸调整
        resize_frame = tk.LabelFrame(basic_frame, text="📏 尺寸调整", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9, "bold"))
        resize_frame.pack(fill=tk.X, padx=5, pady=5)
        
        size_frame = tk.Frame(resize_frame, bg=self.theme.bg_color)
        size_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(size_frame, text="宽度:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.width_var = tk.StringVar()
        tk.Entry(size_frame, textvariable=self.width_var, width=8, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(size_frame, text="高度:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.height_var = tk.StringVar()
        tk.Entry(size_frame, textvariable=self.height_var, width=8, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        resize_btn = tk.Button(size_frame, text="调整", command=self.resize_images,
                             bg=self.theme.button_color, fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        resize_btn.pack(side=tk.RIGHT)
        
        # 裁剪设置
        crop_frame = tk.LabelFrame(basic_frame, text="✂️ 裁剪设置", 
                                 bg=self.theme.bg_color, fg=self.theme.text_color,
                                 font=("微软雅黑", 9, "bold"))
        crop_frame.pack(fill=tk.X, padx=5, pady=5)
        
        crop_input_frame = tk.Frame(crop_frame, bg=self.theme.bg_color)
        crop_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(crop_input_frame, text="裁剪像素:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.crop_pixels = tk.StringVar(value="100")
        tk.Entry(crop_input_frame, textvariable=self.crop_pixels, width=8, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        crop_btn = tk.Button(crop_input_frame, text="裁剪", command=self.crop_images,
                           bg=self.theme.button_color, fg="white",
                           font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        crop_btn.pack(side=tk.RIGHT)
        
        # 裁剪方式
        crop_mode_frame = tk.Frame(crop_frame, bg=self.theme.bg_color)
        crop_mode_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.crop_mode = tk.StringVar(value="bottom")
        bottom_rb = tk.Radiobutton(crop_mode_frame, text="裁剪底部", variable=self.crop_mode, value="bottom",
                                 bg=self.theme.bg_color, fg=self.theme.text_color, font=("微软雅黑", 9))
        bottom_rb.pack(side=tk.LEFT)
        
        top_rb = tk.Radiobutton(crop_mode_frame, text="裁剪顶部", variable=self.crop_mode, value="top",
                              bg=self.theme.bg_color, fg=self.theme.text_color, font=("微软雅黑", 9))
        top_rb.pack(side=tk.LEFT, padx=(20, 0))
    
    def create_advanced_tab(self, notebook):
        """创建高级处理选项卡"""
        advanced_frame = tk.Frame(notebook, bg=self.theme.bg_color)
        notebook.add(advanced_frame, text="高级处理")
        
        # 随机旋转
        rotate_frame = tk.LabelFrame(advanced_frame, text="🔄 随机旋转", 
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9, "bold"))
        rotate_frame.pack(fill=tk.X, padx=5, pady=5)
        
        angle_frame = tk.Frame(rotate_frame, bg=self.theme.bg_color)
        angle_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(angle_frame, text="最小角度:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.min_angle_var = tk.StringVar(value="-5")
        tk.Entry(angle_frame, textvariable=self.min_angle_var, width=6, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        tk.Label(angle_frame, text="最大角度:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.max_angle_var = tk.StringVar(value="5")
        tk.Entry(angle_frame, textvariable=self.max_angle_var, width=6, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        rotate_btn = tk.Button(angle_frame, text="旋转", command=self.random_rotate_images,
                             bg=self.theme.button_color, fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        rotate_btn.pack(side=tk.RIGHT)
        
        tk.Label(rotate_frame, text="角度范围: -10° ~ +10°", 
               bg=self.theme.bg_color, fg=self.theme.accent_color,
               font=("微软雅黑", 8)).pack(padx=5, pady=2)
        
        # 压缩设置
        compress_frame = tk.LabelFrame(advanced_frame, text="🗜️ 批量压缩", 
                                     bg=self.theme.bg_color, fg=self.theme.text_color,
                                     font=("微软雅黑", 9, "bold"))
        compress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        quality_frame = tk.Frame(compress_frame, bg=self.theme.bg_color)
        quality_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(quality_frame, text="压缩质量:", bg=self.theme.bg_color, fg=self.theme.text_color,
               font=("微软雅黑", 9)).pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="85")
        tk.Entry(quality_frame, textvariable=self.quality_var, width=8, 
               font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=(5, 10))
        
        compress_btn = tk.Button(quality_frame, text="压缩", command=self.compress_images,
                               bg=self.theme.button_color, fg="white",
                               font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        compress_btn.pack(side=tk.RIGHT)
        
        # 覆盖原图选项
        self.overwrite_original = tk.BooleanVar(value=False)
        overwrite_cb = tk.Checkbutton(compress_frame, text="覆盖原图", 
                                    variable=self.overwrite_original,
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 9))
        overwrite_cb.pack(padx=5, pady=5)
        
        # 哈希修改设置
        hash_frame = tk.LabelFrame(advanced_frame, text="🔐 哈希修改", 
                                 bg=self.theme.bg_color, fg=self.theme.text_color,
                                 font=("微软雅黑", 9, "bold"))
        hash_frame.pack(fill=tk.X, padx=5, pady=5)
        
        hash_control_frame = tk.Frame(hash_frame, bg=self.theme.bg_color)
        hash_control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        hash_btn = tk.Button(hash_control_frame, text="修改哈希值", command=self.modify_hash_images,
                           bg=self.theme.button_color, fg="white",
                           font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        hash_btn.pack(side=tk.LEFT)
        
        # 哈希修改选项
        self.preserve_original_hash = tk.BooleanVar(value=False)
        preserve_cb = tk.Checkbutton(hash_control_frame, text="保留原图", 
                                   variable=self.preserve_original_hash,
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9))
        preserve_cb.pack(side=tk.LEFT, padx=(20, 0))
        
        tk.Label(hash_frame, text="通过修改EXIF数据和添加随机数据来改变图片哈希值", 
               bg=self.theme.bg_color, fg=self.theme.accent_color,
               font=("微软雅黑", 8)).pack(padx=5, pady=2)
    
    def create_output_tab(self, notebook):
        """创建输出设置选项卡"""
        output_frame = tk.Frame(notebook, bg=self.theme.bg_color)
        notebook.add(output_frame, text="输出设置")
        
        # 保存设置
        save_frame = tk.LabelFrame(output_frame, text="💾 保存路径", 
                                 bg=self.theme.bg_color, fg=self.theme.text_color,
                                 font=("微软雅黑", 9, "bold"))
        save_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.save_path = tk.StringVar()
        save_path_frame = tk.Frame(save_frame, bg=self.theme.bg_color)
        save_path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        save_entry = tk.Entry(save_path_frame, textvariable=self.save_path, 
                            font=("微软雅黑", 9), bg="white")
        save_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        save_browse_btn = tk.Button(save_path_frame, text="浏览", command=self.browse_save_folder,
                                  bg=self.theme.button_color, fg="white",
                                  font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        save_browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        save_all_btn = tk.Button(save_frame, text="💾 保存所有图片", command=self.save_images,
                               bg=self.theme.accent_color, fg="white",
                               font=("微软雅黑", 10, "bold"), relief=tk.RAISED, bd=2)
        save_all_btn.pack(fill=tk.X, padx=5, pady=(10, 5))
    
    def create_preview_panel(self, parent):
        """创建预览面板"""
        preview_frame = tk.LabelFrame(parent, text="🖼️ 图片预览", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10, "bold"))
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 图片导航
        nav_frame = tk.Frame(preview_frame, bg=self.theme.bg_color)
        nav_frame.pack(fill=tk.X, padx=10, pady=10)
        
        prev_btn = tk.Button(nav_frame, text="⬅️ 上一张", command=self.prev_image,
                           bg=self.theme.button_color, fg="white",
                           font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        prev_btn.pack(side=tk.LEFT)
        
        self.image_counter = tk.Label(nav_frame, text="0/0", 
                                    bg=self.theme.bg_color, fg=self.theme.text_color,
                                    font=("微软雅黑", 10, "bold"))
        self.image_counter.pack(side=tk.LEFT, padx=20)
        
        next_btn = tk.Button(nav_frame, text="下一张 ➡️", command=self.next_image,
                           bg=self.theme.button_color, fg="white",
                           font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        next_btn.pack(side=tk.LEFT)
        
        # 移除按钮（原删除按钮）
        remove_btn = tk.Button(nav_frame, text="📤 移除", command=self.remove_image,
                             bg="#FFA500", fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        remove_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # 删除到回收站按钮
        delete_btn = tk.Button(nav_frame, text="🗑️ 删除", command=self.delete_image_to_recycle,
                             bg="#DC143C", fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        delete_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # 图片显示区域
        canvas_frame = tk.Frame(preview_frame, bg=self.theme.bg_color)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", relief=tk.SUNKEN, bd=2)
        self.canvas.pack(fill=tk.BOTH, expand=True)
    
    # 文件操作方法
    def browse_folder(self):
        """浏览文件夹"""
        folder_path = filedialog.askdirectory(title="选择图片文件夹")
        if folder_path:
            self.folder_path.set(folder_path)
    
    def browse_save_folder(self):
        """浏览保存文件夹"""
        folder_path = filedialog.askdirectory(title="选择保存文件夹")
        if folder_path:
            self.save_path.set(folder_path)
    
    def load_images(self):
        """加载图片"""
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
        
        if self.update_status:
            self.update_status("正在加载图片...")
        
        self.processed_images = []
        self.current_image_index = 0
        
        # 在后台线程中加载图片
        threading.Thread(target=self._load_images_thread, args=(folder_path,), daemon=True).start()
    
    def _load_images_thread(self, folder_path):
        """在后台线程中加载图片"""
        image_files = []
        include_subfolders = self.include_subfolders.get()
        
        # 收集所有图片文件
        if include_subfolders:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        image_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_files.append(os.path.join(folder_path, file))
        
        # 加载图片
        for file_path in image_files:
            try:
                img = Image.open(file_path)
                self.processed_images.append({
                    'path': file_path,
                    'image': img,
                    'original': img.copy()
                })
            except Exception as e:
                print(f"无法加载图片 {file_path}: {e}")
        
        # 更新UI
        self.parent.after(0, self._update_after_load)
    
    def _update_after_load(self):
        """加载完成后更新界面"""
        if self.processed_images:
            if self.update_status:
                self.update_status(f"已加载 {len(self.processed_images)} 张图片")
            self.update_image_counter()
            self.display_current_image()
        else:
            if self.update_status:
                self.update_status("未找到图片")
            self.image_counter.config(text="0/0")
            self.canvas.delete("all")
    
    # 图片显示方法
    def update_image_counter(self):
        """更新图片计数器"""
        if self.processed_images:
            self.image_counter.config(text=f"{self.current_image_index + 1}/{len(self.processed_images)}")
        else:
            self.image_counter.config(text="0/0")
    
    def display_current_image(self):
        """显示当前图片"""
        if not self.processed_images:
            return
        
        self.canvas.delete("all")
        img_data = self.processed_images[self.current_image_index]
        img = img_data['image']
        
        # 调整图片大小以适应画布
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:  # 画布尚未完全初始化
            self.parent.after(100, self.display_current_image)
            return
        
        img_width, img_height = img.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img)
        
        # 保存引用以防止垃圾回收
        self.current_photo = photo
        
        # 在画布中央显示图片
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
        # 显示图片信息
        filename = os.path.basename(img_data['path'])
        dimensions = f"{img_width}x{img_height}"
        if self.update_status:
            self.update_status(f"当前图片: {filename} ({dimensions})")
    
    def prev_image(self):
        """上一张图片"""
        if self.processed_images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_image_counter()
            self.display_current_image()
    
    def next_image(self):
        """下一张图片"""
        if self.processed_images and self.current_image_index < len(self.processed_images) - 1:
            self.current_image_index += 1
            self.update_image_counter()
            self.display_current_image()
    
    def remove_image(self):
        """从列表中移除当前图片（不删除文件）"""
        if not self.processed_images:
            return
        
        del self.processed_images[self.current_image_index]
        
        if self.processed_images:
            if self.current_image_index >= len(self.processed_images):
                self.current_image_index = len(self.processed_images) - 1
            self.update_image_counter()
            self.display_current_image()
        else:
            self.current_image_index = 0
            self.update_image_counter()
            self.canvas.delete("all")
            if self.update_status:
                self.update_status("已移除所有图片")
    
    def delete_image_to_recycle(self):
        """删除当前图片到回收站"""
        if not self.processed_images:
            return
        
        current_image = self.processed_images[self.current_image_index]
        image_path = current_image['path']
        
        try:
            # 导入文件操作工具
            from app.utils.file_operations import FileOperations
            
            # 删除文件到回收站
            if FileOperations.delete_to_recycle_bin(image_path):
                # 从列表中移除
                del self.processed_images[self.current_image_index]
                
                if self.processed_images:
                    if self.current_image_index >= len(self.processed_images):
                        self.current_image_index = len(self.processed_images) - 1
                    self.update_image_counter()
                    self.display_current_image()
                else:
                    self.current_image_index = 0
                    self.update_image_counter()
                    self.canvas.delete("all")
                
                if self.update_status:
                    self.update_status(f"已删除图片到回收站: {os.path.basename(image_path)}")
            else:
                messagebox.showerror("错误", "删除图片到回收站失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"删除图片失败: {str(e)}")
    
    # 图片处理方法
    def resize_images(self):
        """调整图片尺寸"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            width = int(self.width_var.get()) if self.width_var.get() else None
            height = int(self.height_var.get()) if self.height_var.get() else None
            
            if not width and not height:
                messagebox.showerror("错误", "请至少输入宽度或高度")
                return
            
            if self.update_status:
                self.update_status("正在调整图片尺寸...")
            threading.Thread(target=self._resize_images_thread, args=(width, height), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _resize_images_thread(self, width, height):
        """在后台线程中调整图片尺寸"""
        for img_data in self.processed_images:
            try:
                original = img_data['original']
                orig_width, orig_height = original.size
                
                # 计算新尺寸
                if width and height:  # 同时指定宽度和高度
                    new_size = (width, height)
                elif width:  # 只指定宽度，按比例计算高度
                    ratio = width / orig_width
                    new_size = (width, int(orig_height * ratio))
                else:  # 只指定高度，按比例计算宽度
                    ratio = height / orig_height
                    new_size = (int(orig_width * ratio), height)
                
                # 调整图片尺寸
                resized_img = original.resize(new_size, Image.LANCZOS)
                img_data['image'] = resized_img
                
            except Exception as e:
                print(f"调整图片尺寸失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process("尺寸调整完成"))
    
    def crop_images(self):
        """裁剪图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            pixels = int(self.crop_pixels.get())
            if pixels <= 0:
                messagebox.showerror("错误", "裁剪像素必须大于0")
                return
            
            crop_mode = self.crop_mode.get()
            if self.update_status:
                self.update_status("正在裁剪图片...")
            threading.Thread(target=self._crop_images_thread, args=(pixels, crop_mode), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _crop_images_thread(self, pixels, crop_mode):
        """在后台线程中裁剪图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        skipped_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                width, height = img.size
                
                if height <= pixels:
                    skipped_count += 1
                    continue  # 图片高度小于裁剪像素，跳过
                
                if crop_mode == "bottom":
                    # 保留上部分，裁剪底部
                    crop_box = (0, 0, width, height - pixels)
                else:  # crop_mode == "top"
                    # 保留下部分，裁剪顶部
                    crop_box = (0, pixels, width, height)
                
                cropped_img = img.crop(crop_box)
                img_data['image'] = cropped_img
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0 and self.update_status:
                    self.parent.after(0, lambda count=processed_count: 
                                   self.update_status(f"正在裁剪图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"裁剪图片失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process(
            f"裁剪完成: 成功处理 {processed_count} 张图片，跳过 {skipped_count} 张图片"))
    
    def random_rotate_images(self):
        """批量随机旋转图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            min_angle = float(self.min_angle_var.get())
            max_angle = float(self.max_angle_var.get())
            
            # 验证角度范围
            if min_angle < -10 or min_angle > 10 or max_angle < -10 or max_angle > 10:
                messagebox.showerror("错误", "角度范围必须在-10到+10度之间")
                return
            
            if min_angle > max_angle:
                messagebox.showerror("错误", "最小角度不能大于最大角度")
                return
            
            if self.update_status:
                self.update_status("正在随机旋转图片...")
            threading.Thread(target=self._random_rotate_images_thread, args=(min_angle, max_angle), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的角度数字")
    
    def _random_rotate_images_thread(self, min_angle, max_angle):
        """在后台线程中随机旋转图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                
                # 生成随机角度
                random_angle = random.uniform(min_angle, max_angle)
                
                # 旋转图片
                rotated_img = self._rotate_and_crop_image(img, random_angle)
                img_data['image'] = rotated_img
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0 and self.update_status:
                    self.parent.after(0, lambda count=processed_count: 
                                   self.update_status(f"正在旋转图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"旋转图片失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process(f"随机旋转完成: 成功处理 {processed_count} 张图片"))
    
    def _rotate_and_crop_image(self, img, angle):
        """旋转图片并裁剪掉空白区域"""
        # 转换角度为弧度
        angle_rad = math.radians(angle)
        
        # 获取原始尺寸
        width, height = img.size
        
        # 旋转图片（使用白色背景填充）
        rotated = img.rotate(angle, expand=True, fillcolor='white')
        
        # 计算旋转后的有效区域（去除空白边缘）
        cos_a = abs(math.cos(angle_rad))
        sin_a = abs(math.sin(angle_rad))
        
        # 计算内接矩形的尺寸
        crop_width = int(min(width * cos_a - height * sin_a, height * cos_a - width * sin_a))
        crop_height = int(min(height * cos_a - width * sin_a, width * cos_a - height * sin_a))
        
        # 确保裁剪尺寸为正数且不超过原图尺寸
        crop_width = max(1, min(crop_width, width))
        crop_height = max(1, min(crop_height, height))
        
        # 计算裁剪框的位置（居中裁剪）
        rotated_width, rotated_height = rotated.size
        left = (rotated_width - crop_width) // 2
        top = (rotated_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height
        
        # 裁剪图片
        cropped = rotated.crop((left, top, right, bottom))
        
        return cropped
    
    def compress_images(self):
        """批量压缩图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            quality = int(self.quality_var.get())
            if quality < 1 or quality > 100:
                messagebox.showerror("错误", "压缩质量必须在1-100之间")
                return
            
            # 如果不覆盖原图，需要选择保存路径
            overwrite = self.overwrite_original.get()
            save_path = ""
            
            if not overwrite:
                save_path = self.save_path.get()
                if not save_path:
                    save_path = filedialog.askdirectory(title="选择保存文件夹")
                    if not save_path:
                        return
                    self.save_path.set(save_path)
            
            if self.update_status:
                self.update_status("正在压缩图片...")
            threading.Thread(target=self._compress_images_thread, args=(quality, overwrite, save_path), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的压缩质量数字")
    
    def _compress_images_thread(self, quality, overwrite, save_path):
        """在后台线程中压缩图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                original_path = img_data['path']
                
                if overwrite:
                    output_path = original_path
                else:
                    filename = os.path.basename(original_path)
                    output_path = os.path.join(save_path, filename)
                
                # 保存压缩后的图片
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0 and self.update_status:
                    self.parent.after(0, lambda count=processed_count: 
                                   self.update_status(f"正在压缩图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"压缩图片失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process(f"压缩完成: 成功处理 {processed_count} 张图片"))
    
    def save_images(self):
        """保存所有图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        save_path = self.save_path.get()
        if not save_path:
            save_path = filedialog.askdirectory(title="选择保存文件夹")
            if not save_path:
                return
            self.save_path.set(save_path)
        
        if self.update_status:
            self.update_status("正在保存图片...")
        threading.Thread(target=self._save_images_thread, args=(save_path,), daemon=True).start()
    
    def _save_images_thread(self, save_path):
        """在后台线程中保存图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                original_path = img_data['path']
                filename = os.path.basename(original_path)
                output_path = os.path.join(save_path, filename)
                
                # 保存图片
                img.save(output_path)
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0 and self.update_status:
                    self.parent.after(0, lambda count=processed_count: 
                                   self.update_status(f"正在保存图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"保存图片失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process(f"保存完成: 成功保存 {processed_count} 张图片到 {save_path}"))
    
    def _update_after_process(self, message):
        """处理完成后更新界面"""
        if self.update_status:
            self.update_status(message)
        self.display_current_image()
    
    def modify_hash_images(self):
        """修改图片哈希值"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        preserve_original = self.preserve_original_hash.get()
        
        if self.update_status:
            self.update_status("正在修改图片哈希值...")
        threading.Thread(target=self._modify_hash_images_thread, args=(preserve_original,), daemon=True).start()
    
    def _modify_hash_images_thread(self, preserve_original):
        """在后台线程中修改图片哈希值"""
        total_images = len(self.processed_images)
        processed_count = 0
        
        for i, img_data in enumerate(self.processed_images):
            try:
                img = img_data['image']
                original_path = img_data['path']
                
                # 修改图片哈希值
                modified_img = self._modify_single_image_hash(img, original_path)
                
                if modified_img:
                    # 如果不保留原图，则替换当前图片
                    if not preserve_original:
                        self.processed_images[i]['image'] = modified_img
                    
                    processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0 and self.update_status:
                    self.parent.after(0, lambda count=processed_count: 
                                   self.update_status(f"正在修改哈希值... {count}/{total_images}"))
                
            except Exception as e:
                print(f"修改图片哈希值失败: {e}")
        
        # 更新UI
        self.parent.after(0, lambda: self._update_after_process(f"哈希修改完成: 成功处理 {processed_count} 张图片"))
    
    def _modify_single_image_hash(self, img, original_path):
        """修改单张图片的哈希值"""
        try:
            # 创建图片副本
            modified_img = img.copy()
            
            # 获取原始图片格式
            original_format = img.format if img.format else 'JPEG'
            
            # 创建新的EXIF数据（仅对JPEG格式）
            if original_format.upper() in ['JPEG', 'JPG']:
                try:
                    exif_dict = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}
                    exif_dict["0th"][piexif.ImageIFD.Make] = f"Modified_{self._generate_random_string()}"
                    exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
                    exif_dict["0th"][piexif.ImageIFD.Software] = f"HashModifier_{self._generate_random_string(5)}"
                    
                    # 添加一些随机的EXIF数据
                    exif_dict["Exif"][piexif.ExifIFD.UserComment] = f"Hash_{self._generate_random_string(20)}".encode('utf-8')
                    
                    # 将EXIF数据转换为字节
                    exif_bytes = piexif.dump(exif_dict)
                    
                    # 创建临时文件来保存带有新EXIF的图片
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
                        temp_path = temp_file.name
                    
                    # 保存图片到临时文件
                    if modified_img.mode == 'RGBA':
                        modified_img = modified_img.convert('RGB')
                    modified_img.save(temp_path, 'JPEG', exif=exif_bytes)
                    
                    # 添加随机数据到文件末尾
                    with open(temp_path, 'ab') as f:
                        f.write(os.urandom(random.randint(10, 100)))
                    
                    # 重新加载修改后的图片
                    modified_img = Image.open(temp_path)
                    modified_img.load()  # 确保图片数据被加载
                    
                    # 删除临时文件
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
                        
                except Exception as e:
                    print(f"EXIF处理失败: {e}")
                    # 如果EXIF处理失败，至少进行像素级别的微调
                    modified_img = self._apply_pixel_modification(modified_img)
            else:
                # 对于PNG等格式，进行像素级别的微调
                modified_img = self._apply_pixel_modification(modified_img)
            
            return modified_img
            
        except Exception as e:
            print(f"修改图片哈希值时出错: {e}")
            return None
    
    def _apply_pixel_modification(self, img):
        """对图片进行微小的像素修改"""
        try:
            # 创建图片副本
            modified_img = img.copy()
            pixels = modified_img.load()
            width, height = modified_img.size
            
            # 随机选择几个像素点进行微调（不超过10个点）
            num_modifications = min(10, width * height // 10000)
            
            for _ in range(num_modifications):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                
                if modified_img.mode == 'RGB':
                    r, g, b = pixels[x, y]
                    # 对RGB值进行微小调整（±1）
                    r = max(0, min(255, r + random.choice([-1, 1])))
                    g = max(0, min(255, g + random.choice([-1, 1])))
                    b = max(0, min(255, b + random.choice([-1, 1])))
                    pixels[x, y] = (r, g, b)
                elif modified_img.mode == 'RGBA':
                    r, g, b, a = pixels[x, y]
                    r = max(0, min(255, r + random.choice([-1, 1])))
                    g = max(0, min(255, g + random.choice([-1, 1])))
                    b = max(0, min(255, b + random.choice([-1, 1])))
                    pixels[x, y] = (r, g, b, a)
            
            return modified_img
            
        except Exception as e:
            print(f"像素修改失败: {e}")
            return img
    
    def _generate_random_string(self, length=10):
        """生成随机字符串"""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))