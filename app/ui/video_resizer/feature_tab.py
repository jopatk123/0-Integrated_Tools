# -*- coding: utf-8 -*-
"""视频调整功能模块"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import subprocess

class VideoResizerFeatureTab:
    """视频调整功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.video_files = []
        self.output_directory = None
        self.compression_thread = None
        self.is_compressing = False
        self.update_status = None  # 状态更新回调
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 文件夹选择区域
        folder_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        folder_frame.pack(fill=tk.X, pady=5)
        
        self.folder_label = tk.Label(folder_frame, text="输出文件夹: 未选择 (将使用原视频所在目录)", 
                                   bg=self.theme.bg_color, anchor="w")
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        button_style = self.theme.get_button_style()
        select_folder_btn = tk.Button(folder_frame, text="选择输出文件夹", 
                                   command=self.select_output_folder,
                                   bg=button_style["bg"], fg=button_style["fg"])
        select_folder_btn.pack(side=tk.RIGHT, padx=5)
        
        # 视频文件选择区域
        video_select_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        video_select_frame.pack(fill=tk.X, pady=5)
        
        select_videos_btn = tk.Button(video_select_frame, text="选择视频文件夹", 
                                    command=self.select_videos_folder,
                                    bg=button_style["bg"], fg=button_style["fg"])
        select_videos_btn.pack(side=tk.LEFT, padx=5)
        
        add_videos_btn = tk.Button(video_select_frame, text="添加视频文件", 
                                 command=self.add_videos,
                                 bg=button_style["bg"], fg=button_style["fg"])
        add_videos_btn.pack(side=tk.LEFT, padx=5)
        
        # 视频列表
        list_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        list_label = tk.Label(list_frame, text="已选择的视频文件:", 
                            bg=self.theme.bg_color, anchor="w")
        list_label.pack(fill=tk.X, padx=5, pady=2)
        
        # 创建滚动条
        scrollbar_y = tk.Scrollbar(list_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(list_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建列表框
        self.video_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar_y.set,
                                      xscrollcommand=scrollbar_x.set)
        self.video_listbox.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # 配置滚动条
        scrollbar_y.config(command=self.video_listbox.yview)
        scrollbar_x.config(command=self.video_listbox.xview)
        
        # 视频列表管理按钮
        list_mgmt_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        list_mgmt_frame.pack(fill=tk.X, pady=5)
        
        remove_video_btn = tk.Button(list_mgmt_frame, text="删除所选视频", 
                                   command=self.remove_selected_video,
                                   bg=button_style["bg"], fg=button_style["fg"])
        remove_video_btn.pack(side=tk.LEFT, padx=5)
        
        clear_list_btn = tk.Button(list_mgmt_frame, text="清空列表", 
                                 command=self.clear_video_list,
                                 bg=button_style["bg"], fg=button_style["fg"])
        clear_list_btn.pack(side=tk.LEFT, padx=5)
        
        # 压缩设置
        compression_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        compression_frame.pack(fill=tk.X, pady=5)
        
        compression_label = tk.Label(compression_frame, text="压缩程度:", 
                                   bg=self.theme.bg_color, anchor="w")
        compression_label.pack(fill=tk.X, padx=5, pady=2)
        
        slider_label_frame = tk.Frame(compression_frame, bg=self.theme.bg_color)
        slider_label_frame.pack(fill=tk.X, padx=5)
        
        low_label = tk.Label(slider_label_frame, text="低质量/小文件", 
                           bg=self.theme.bg_color, anchor="w")
        low_label.pack(side=tk.LEFT)
        
        high_label = tk.Label(slider_label_frame, text="高质量/大文件", 
                            bg=self.theme.bg_color, anchor="e")
        high_label.pack(side=tk.RIGHT)
        
        self.compression_slider = tk.Scale(compression_frame, from_=0, to=100, 
                                        orient=tk.HORIZONTAL, length=300,
                                        bg=self.theme.bg_color)
        self.compression_slider.set(50)  # 默认中等压缩
        self.compression_slider.pack(padx=5, pady=5)
        
        self.compression_value_label = tk.Label(compression_frame, text="压缩程度: 50%", 
                                             bg=self.theme.bg_color)
        self.compression_value_label.pack(padx=5, pady=2)
        self.compression_slider.config(command=self.update_compression_label)
        
        # GPU 加速选项
        gpu_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        gpu_frame.pack(fill=tk.X, pady=5)
        
        self.gpu_acceleration = tk.BooleanVar()
        self.gpu_checkbox = tk.Checkbutton(gpu_frame, text="启用 NVIDIA GPU 加速 (需要支持的显卡和驱动)", 
                                         variable=self.gpu_acceleration,
                                         bg=self.theme.bg_color, anchor="w")
        self.gpu_checkbox.pack(fill=tk.X, padx=5, pady=2)
        
        # GPU 加速说明
        gpu_info_label = tk.Label(gpu_frame, 
                                text="注意：GPU 加速需要 NVIDIA 显卡和正确的驱动程序。如果启用后出现错误，请关闭此选项。", 
                                bg=self.theme.bg_color, anchor="w", 
                                font=("Arial", 8), fg="gray")
        gpu_info_label.pack(fill=tk.X, padx=5, pady=2)
        
        # 进度条
        progress_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                         maximum=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        self.progress_bar.pack_forget()  # 初始隐藏
        
        # 压缩按钮
        button_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.compress_btn = tk.Button(button_frame, text="开始压缩", 
                                    command=self.start_compression,
                                    bg=button_style["bg"], fg=button_style["fg"])
        self.compress_btn.pack(padx=5, pady=5)
    
    def update_compression_label(self, value):
        """更新压缩程度标签"""
        self.compression_value_label.config(text=f"压缩程度: {int(float(value))}%")
    
    def select_output_folder(self):
        """选择输出文件夹"""
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_directory = folder
            self.folder_label.config(text=f"输出文件夹: {folder}")
            if self.update_status:
                self.update_status(f"已选择输出文件夹: {folder}")
    
    def select_videos_folder(self):
        """选择视频文件夹"""
        folder = filedialog.askdirectory(title="选择包含视频的文件夹")
        if folder:
            self.scan_for_videos(folder)
    
    def scan_for_videos(self, folder):
        """扫描文件夹中的视频文件"""
        video_extensions = [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"]
        added_count = 0
        
        for root, _, files in os.walk(folder):
            for file in files:
                if any(file.lower().endswith(ext) for ext in video_extensions):
                    full_path = os.path.join(root, file)
                    if full_path not in self.video_files:
                        self.video_files.append(full_path)
                        self.video_listbox.insert(tk.END, full_path)
                        added_count += 1
        
        if self.update_status:
            self.update_status(f"从文件夹中添加了 {added_count} 个视频文件")
    
    def add_videos(self):
        """添加视频文件"""
        files = filedialog.askopenfilenames(
            title="选择视频文件", 
            filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv")]
        )
        
        added_count = 0
        for file in files:
            if file not in self.video_files:
                self.video_files.append(file)
                self.video_listbox.insert(tk.END, file)
                added_count += 1
        
        if self.update_status:
            self.update_status(f"添加了 {added_count} 个视频文件")
    
    def remove_selected_video(self):
        """删除选中的视频"""
        selected_indices = self.video_listbox.curselection()
        if not selected_indices:
            return
            
        # 从后往前删除，避免索引变化
        removed_count = 0
        for index in sorted(selected_indices, reverse=True):
            removed_item = self.video_listbox.get(index)
            self.video_listbox.delete(index)
            self.video_files.remove(removed_item)
            removed_count += 1
        
        if self.update_status:
            self.update_status(f"删除了 {removed_count} 个视频文件")
    
    def clear_video_list(self):
        """清空视频列表"""
        self.video_listbox.delete(0, tk.END)
        self.video_files = []
        if self.update_status:
            self.update_status("已清空视频列表")
    
    def start_compression(self):
        """开始压缩"""
        if not self.video_files:
            messagebox.showwarning("警告", "请先选择视频文件！")
            return
        
        if self.is_compressing:
            messagebox.showinfo("提示", "正在压缩中，请等待完成...")
            return
        
        # 确定是否使用原始目录
        use_original_dirs = self.output_directory is None
        
        # 显示进度条并禁用按钮
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        self.progress_var.set(0)
        self.compress_btn.config(state=tk.DISABLED)
        self.is_compressing = True
        
        if self.update_status:
            self.update_status(f"开始压缩 {len(self.video_files)} 个视频文件...")
        
        # 创建并启动压缩线程
        self.compression_thread = threading.Thread(
            target=self.compress_videos,
            args=(self.video_files, self.output_directory, 
                  self.compression_slider.get(), use_original_dirs)
        )
        self.compression_thread.daemon = True
        self.compression_thread.start()
    
    def compress_videos(self, video_files, output_dir, compression_level, use_original_dirs):
        """压缩视频文件"""
        total_files = len(video_files)
        success_count = 0
        error_count = 0
        error_messages = []
        
        for i, video_file in enumerate(video_files):
            try:
                # 计算基于压缩级别的参数
                crf_value = 51 - int(float(compression_level) * 0.51)  # 0-100 映射到 51-0 (0是最高质量)
                
                # 创建输出文件名
                filename = os.path.basename(video_file)
                output_filename = f"compressed_{filename}"
                
                # 如果使用原始目录，则每个视频输出到其原始目录
                if use_original_dirs:
                    output_dir = os.path.dirname(video_file)
                    
                output_path = os.path.join(output_dir, output_filename)
                
                # 使用ffmpeg进行视频压缩
                if self.gpu_acceleration.get():
                    # 使用 NVIDIA GPU 加速
                    cmd = [
                        "ffmpeg", 
                        "-hwaccel", "cuvid",
                        "-c:v", "h264_cuvid",
                        "-i", video_file, 
                        "-c:v", "h264_nvenc",
                        "-crf", str(crf_value), 
                        "-preset", "fast", 
                        "-y", output_path
                    ]
                else:
                    # 使用 CPU 软件编码
                    cmd = [
                        "ffmpeg", "-i", video_file, 
                        "-crf", str(crf_value), 
                        "-preset", "medium", 
                        "-y", output_path
                    ]
                
                process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                stdout, stderr = process.communicate()
                
                if process.returncode != 0:
                    error_count += 1
                    error_messages.append(f"处理文件 {video_file} 时出错: {stderr}")
                else:
                    success_count += 1
                
                # 更新进度
                progress = int(((i + 1) / total_files) * 100)
                self.update_progress(progress)
                
            except Exception as e:
                error_count += 1
                error_messages.append(f"处理文件 {video_file} 时出错: {str(e)}")
        
        # 完成后更新UI
        self.compression_finished(success_count, error_count, error_messages)
    
    def update_progress(self, value):
        """更新进度条"""
        # 在主线程中更新UI
        self.parent_frame.after(0, lambda: self.progress_var.set(value))
    
    def compression_finished(self, success_count, error_count, error_messages):
        """压缩完成处理"""
        # 在主线程中更新UI
        def update_ui():
            self.progress_var.set(100)
            self.compress_btn.config(state=tk.NORMAL)
            self.is_compressing = False
            
            # 显示结果
            result_message = f"视频压缩完成！\n成功: {success_count}\n失败: {error_count}"
            if error_messages:
                result_message += "\n\n错误详情:\n" + "\n".join(error_messages[:5])
                if len(error_messages) > 5:
                    result_message += f"\n...等 {len(error_messages) - 5} 个错误未显示"
                    
            messagebox.showinfo("压缩结果", result_message)
            
            if self.update_status:
                self.update_status(f"压缩完成 - 成功: {success_count}, 失败: {error_count}")
        
        self.parent_frame.after(0, update_ui)