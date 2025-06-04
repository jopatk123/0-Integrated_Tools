# -*- coding: utf-8 -*-
"""视频格式转换功能模块"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import threading
import subprocess
from typing import List, Dict

class VideoConverterTab:
    """视频格式转换功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.update_status = None  # 状态更新回调函数
        
        # 支持的视频格式
        self.supported_formats = {
            'MP4': ['.mp4'],
            'AVI': ['.avi'],
            'MOV': ['.mov'],
            'WMV': ['.wmv'],
            'FLV': ['.flv'],
            'MKV': ['.mkv'],
            'WEBM': ['.webm'],
            'M4V': ['.m4v'],
            '3GP': ['.3gp'],
            'TS': ['.ts']
        }
        
        # 视频质量预设
        self.quality_presets = {
            '高质量': {'crf': 18, 'preset': 'slow'},
            '标准质量': {'crf': 23, 'preset': 'medium'},
            '快速压缩': {'crf': 28, 'preset': 'fast'},
            '极速压缩': {'crf': 32, 'preset': 'ultrafast'}
        }
        
        # 分辨率选项
        self.resolution_options = {
            '保持原分辨率': None,
            '4K (3840x2160)': '3840x2160',
            '2K (2560x1440)': '2560x1440',
            '1080p (1920x1080)': '1920x1080',
            '720p (1280x720)': '1280x720',
            '480p (854x480)': '854x480',
            '360p (640x360)': '640x360'
        }
        
        # 文件列表
        self.file_list = []
        
        # 检查FFmpeg
        self.check_ffmpeg()
        
        # 创建界面组件
        self.create_widgets()
        
    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=5)
            self.ffmpeg_available = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            self.ffmpeg_available = False
            
        if not self.ffmpeg_available:
            self.show_ffmpeg_warning()
            
    def show_ffmpeg_warning(self):
        """显示FFmpeg缺失的警告"""
        warning_msg = ("缺少FFmpeg工具，无法进行视频格式转换\n\n"
                      "请从以下地址下载并安装FFmpeg：\n"
                      "https://ffmpeg.org/download.html\n\n"
                      "安装后请确保ffmpeg命令在系统PATH中可用")
        
        warning_frame = tk.Frame(self.parent_frame, bg="#ffeeee", relief=tk.RAISED, bd=2)
        warning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        warning_label = tk.Label(warning_frame, text=warning_msg, 
                               bg="#ffeeee", fg="#cc0000", 
                               justify=tk.LEFT, font=("微软雅黑", 10))
        warning_label.pack(padx=10, pady=10)
        
    def create_widgets(self):
        """创建界面组件"""
        if not self.ffmpeg_available:
            return
            
        # 主要操作框架
        main_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文件选择区域
        file_frame = tk.LabelFrame(main_frame, text="视频文件选择", bg=self.theme.bg_color,
                                 font=("微软雅黑", 10, "bold"))
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        button_style = self.theme.get_button_style()
        
        # 添加文件按钮
        add_files_btn = tk.Button(button_frame, text="🎬 添加视频文件", 
                                command=self.add_files,
                                bg=button_style["bg"], fg=button_style["fg"],
                                font=("微软雅黑", 10))
        add_files_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加文件夹按钮
        add_folder_btn = tk.Button(button_frame, text="📂 添加文件夹", 
                                 command=self.add_folder,
                                 bg=button_style["bg"], fg=button_style["fg"],
                                 font=("微软雅黑", 10))
        add_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # 移除选中按钮
        remove_btn = tk.Button(button_frame, text="🗑️ 移除选中", 
                             command=self.remove_selected,
                             bg="#dc3545", fg="white",
                             font=("微软雅黑", 10))
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空列表按钮
        clear_btn = tk.Button(button_frame, text="🧹 清空列表", 
                            command=self.clear_list,
                            bg="#6c757d", fg="white",
                            font=("微软雅黑", 10))
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 文件列表
        list_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建Treeview显示文件列表
        columns = ('文件名', '格式', '大小', '时长', '路径')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=6)
        
        # 设置列标题
        for col in columns:
            self.file_tree.heading(col, text=col)
            
        # 设置列宽
        self.file_tree.column('文件名', width=200)
        self.file_tree.column('格式', width=80)
        self.file_tree.column('大小', width=100)
        self.file_tree.column('时长', width=100)
        self.file_tree.column('路径', width=300)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 转换设置区域
        settings_frame = tk.LabelFrame(main_frame, text="转换设置", bg=self.theme.bg_color,
                                     font=("微软雅黑", 10, "bold"))
        settings_frame.pack(fill=tk.X, pady=5)
        
        # 第一行设置
        settings_row1 = tk.Frame(settings_frame, bg=self.theme.bg_color)
        settings_row1.pack(fill=tk.X, padx=10, pady=5)
        
        # 目标格式选择
        tk.Label(settings_row1, text="目标格式：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        self.target_format = tk.StringVar(value="MP4")
        format_combo = ttk.Combobox(settings_row1, textvariable=self.target_format,
                                  values=list(self.supported_formats.keys()),
                                  state="readonly", width=10)
        format_combo.pack(side=tk.LEFT, padx=10)
        
        # 质量预设
        tk.Label(settings_row1, text="质量预设：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(20, 0))
        
        self.quality_preset = tk.StringVar(value="标准质量")
        quality_combo = ttk.Combobox(settings_row1, textvariable=self.quality_preset,
                                   values=list(self.quality_presets.keys()),
                                   state="readonly", width=12)
        quality_combo.pack(side=tk.LEFT, padx=10)
        
        # 第二行设置
        settings_row2 = tk.Frame(settings_frame, bg=self.theme.bg_color)
        settings_row2.pack(fill=tk.X, padx=10, pady=5)
        
        # 分辨率选择
        tk.Label(settings_row2, text="输出分辨率：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        self.resolution = tk.StringVar(value="保持原分辨率")
        resolution_combo = ttk.Combobox(settings_row2, textvariable=self.resolution,
                                      values=list(self.resolution_options.keys()),
                                      state="readonly", width=15)
        resolution_combo.pack(side=tk.LEFT, padx=10)
        
        # 帧率设置
        tk.Label(settings_row2, text="帧率(fps)：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT, padx=(20, 0))
        
        self.framerate = tk.StringVar(value="保持原帧率")
        framerate_combo = ttk.Combobox(settings_row2, textvariable=self.framerate,
                                     values=["保持原帧率", "60", "30", "25", "24", "15"],
                                     state="readonly", width=10)
        framerate_combo.pack(side=tk.LEFT, padx=10)
        
        # 第三行设置 - GPU加速
        settings_row3 = tk.Frame(settings_frame, bg=self.theme.bg_color)
        settings_row3.pack(fill=tk.X, padx=10, pady=5)
        
        # GPU加速选项 - 默认开启
        self.gpu_acceleration = tk.BooleanVar(value=True)
        gpu_checkbox = tk.Checkbutton(settings_row3, text="启用 NVIDIA GPU 加速",
                                    variable=self.gpu_acceleration,
                                    bg=self.theme.bg_color,
                                    font=("微软雅黑", 10))
        gpu_checkbox.pack(side=tk.LEFT)
        
        # GPU加速说明
        gpu_info_label = tk.Label(settings_row3, 
                                text="(需要NVIDIA显卡和正确驱动)",
                                bg=self.theme.bg_color, 
                                font=("微软雅黑", 9), fg="gray")
        gpu_info_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # 输出目录选择
        output_frame = tk.Frame(settings_frame, bg=self.theme.bg_color)
        output_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(output_frame, text="输出目录：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        self.output_dir_var = tk.StringVar()
        output_entry = tk.Entry(output_frame, textvariable=self.output_dir_var, width=50,
                              font=("微软雅黑", 10))
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_output_btn = tk.Button(output_frame, text="浏览", command=self.browse_output_dir,
                                    bg=button_style["bg"], fg=button_style["fg"],
                                    font=("微软雅黑", 10))
        browse_output_btn.pack(side=tk.RIGHT, padx=5)
        
        # 转换按钮
        convert_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        convert_frame.pack(fill=tk.X, pady=10)
        
        success_style = self.theme.get_button_style("success")
        self.convert_btn = tk.Button(convert_frame, text="🎬 开始转换", command=self.start_conversion,
                                   bg=success_style["bg"], fg=success_style["fg"], 
                                   font=("微软雅黑", 12, "bold"))
        self.convert_btn.pack(pady=10)
        
        # 进度条和状态
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(convert_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
        self.current_file_var = tk.StringVar(value="等待开始...")
        current_file_label = tk.Label(convert_frame, textvariable=self.current_file_var,
                                    bg=self.theme.bg_color, font=("微软雅黑", 9))
        current_file_label.pack(pady=2)
        
    def add_files(self):
        """添加视频文件"""
        if not self.ffmpeg_available:
            messagebox.showerror("错误", "FFmpeg未安装，无法进行视频转换")
            return
            
        filetypes = [("视频文件", "*.mp4 *.avi *.mov *.wmv *.flv *.mkv *.webm *.m4v *.3gp *.ts"),
                    ("所有文件", "*.*")]
        
        filenames = filedialog.askopenfilenames(
            title="选择视频文件",
            filetypes=filetypes
        )
        
        # 如果选择了文件且输出目录为空，自动设置输出目录
        if filenames and not self.output_dir_var.get():
            self.output_dir_var.set(os.path.dirname(filenames[0]))
        
        for filename in filenames:
            self.add_file_to_list(filename)
            
    def add_folder(self):
        """添加文件夹中的所有视频"""
        if not self.ffmpeg_available:
            messagebox.showerror("错误", "FFmpeg未安装，无法进行视频转换")
            return
            
        folder_path = filedialog.askdirectory(title="选择包含视频的文件夹")
        if not folder_path:
            return
            
        # 如果输出目录为空，自动设置为选择的文件夹
        if not self.output_dir_var.get():
            self.output_dir_var.set(folder_path)
            
        # 支持的扩展名
        supported_exts = []
        for exts in self.supported_formats.values():
            supported_exts.extend(exts)
            
        # 遍历文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file_path).suffix.lower()
                if file_ext in supported_exts:
                    self.add_file_to_list(file_path)
                    
    def add_file_to_list(self, file_path):
        """添加文件到列表"""
        # 检查文件是否已存在
        for item in self.file_list:
            if item['path'] == file_path:
                return
                
        try:
            # 获取文件信息
            file_size = os.path.getsize(file_path)
            file_size_str = self.format_file_size(file_size)
            
            file_name = os.path.basename(file_path)
            file_ext = Path(file_path).suffix.upper().replace('.', '')
            
            # 获取视频时长（如果可能）
            duration = self.get_video_duration(file_path)
            
            # 添加到列表
            file_info = {
                'name': file_name,
                'format': file_ext,
                'size': file_size_str,
                'duration': duration,
                'path': file_path
            }
            
            self.file_list.append(file_info)
            
            # 添加到TreeView
            self.file_tree.insert('', 'end', values=(file_name, file_ext, file_size_str, duration, file_path))
            
            if self.update_status:
                self.update_status(f"已添加视频: {file_name}")
                
        except Exception as e:
            messagebox.showerror("错误", f"添加文件失败: {e}")
            
    def get_video_duration(self, file_path):
        """获取视频时长"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
                   '-of', 'csv=p=0', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and result.stdout.strip():
                duration_seconds = float(result.stdout.strip())
                minutes = int(duration_seconds // 60)
                seconds = int(duration_seconds % 60)
                return f"{minutes:02d}:{seconds:02d}"
        except:
            pass
        return "未知"
        
    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
        
    def remove_selected(self):
        """移除选中的文件"""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要移除的文件")
            return
            
        for item in selected_items:
            # 获取文件路径
            values = self.file_tree.item(item, 'values')
            file_path = values[4]
            
            # 从文件列表中移除
            self.file_list = [f for f in self.file_list if f['path'] != file_path]
            
            # 从TreeView中移除
            self.file_tree.delete(item)
            
        if self.update_status:
            self.update_status(f"已移除 {len(selected_items)} 个文件")
            
    def clear_list(self):
        """清空文件列表"""
        if not self.file_list:
            return
            
        result = messagebox.askyesno("确认", "确定要清空所有文件吗？")
        if result:
            self.file_list.clear()
            self.file_tree.delete(*self.file_tree.get_children())
            if self.update_status:
                self.update_status("文件列表已清空")
                
    def browse_output_dir(self):
        """浏览选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir_var.set(directory)
            
    def start_conversion(self):
        """开始转换过程"""
        if not self.ffmpeg_available:
            messagebox.showerror("错误", "FFmpeg未安装，无法进行视频转换")
            return
            
        # 验证输入
        if not self.validate_inputs():
            return
            
        # 禁用转换按钮
        self.convert_btn.config(state="disabled")
        self.progress_var.set(0)
        self.current_file_var.set("准备开始转换...")
        
        if self.update_status:
            self.update_status("开始转换视频...")
        
        # 在新线程中执行转换
        thread = threading.Thread(target=self.convert_videos)
        thread.daemon = True
        thread.start()
        
    def validate_inputs(self):
        """验证输入参数"""
        if not self.file_list:
            messagebox.showerror("错误", "请先添加要转换的视频文件")
            return False
            
        output_dir = self.output_dir_var.get().strip()
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return False
            
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录: {e}")
                return False
                
        return True
        
    def convert_videos(self):
        """转换视频（在后台线程中执行）"""
        try:
            target_format = self.target_format.get().lower()
            output_dir = self.output_dir_var.get()
            quality_preset = self.quality_presets[self.quality_preset.get()]
            resolution = self.resolution_options[self.resolution.get()]
            framerate = self.framerate.get()
            
            total_files = len(self.file_list)
            converted_count = 0
            failed_count = 0
            
            for i, file_info in enumerate(self.file_list):
                try:
                    # 更新进度
                    progress = (i / total_files) * 100
                    self.progress_var.set(progress)
                    self.current_file_var.set(f"正在转换: {file_info['name']}")
                    
                    if self.update_status:
                        self.update_status(f"正在转换: {file_info['name']} ({i+1}/{total_files})")
                    
                    # 生成输出文件名
                    base_name = Path(file_info['name']).stem
                    target_ext = self.supported_formats[self.target_format.get()][0]
                    output_filename = f"{base_name}{target_ext}"
                    output_path = os.path.join(output_dir, output_filename)
                    
                    # 如果文件已存在，添加序号
                    counter = 1
                    while os.path.exists(output_path):
                        output_filename = f"{base_name}_{counter}{target_ext}"
                        output_path = os.path.join(output_dir, output_filename)
                        counter += 1
                    
                    # 构建FFmpeg命令
                    gpu_failed = False
                    if self.gpu_acceleration.get():
                        # 尝试使用NVIDIA GPU加速
                        cmd = ['ffmpeg', '-hwaccel', 'cuvid', '-c:v', 'h264_cuvid', '-i', file_info['path'], '-y']
                        
                        # GPU编码器设置
                        if target_format == 'mp4':
                            cmd.extend(['-c:v', 'h264_nvenc', '-c:a', 'aac'])
                        elif target_format == 'webm':
                            cmd.extend(['-c:v', 'vp9_nvenc', '-c:a', 'libopus'])
                        else:
                            cmd.extend(['-c:v', 'h264_nvenc', '-c:a', 'aac'])  # 默认使用h264_nvenc
                        
                        # GPU加速的质量设置
                        cmd.extend(['-cq', str(quality_preset['crf'])])
                        cmd.extend(['-preset', 'fast'])  # GPU编码器使用fast预设
                    else:
                        # 使用CPU软件编码
                        cmd = ['ffmpeg', '-i', file_info['path'], '-y']
                        
                        # 添加质量设置
                        cmd.extend(['-crf', str(quality_preset['crf'])])
                        cmd.extend(['-preset', quality_preset['preset']])
                        
                        # 添加编码器设置
                        if target_format == 'mp4':
                            cmd.extend(['-c:v', 'libx264', '-c:a', 'aac'])
                        elif target_format == 'webm':
                            cmd.extend(['-c:v', 'libvpx-vp9', '-c:a', 'libopus'])
                    
                    # 添加分辨率设置
                    if resolution:
                        cmd.extend(['-s', resolution])
                    
                    # 添加帧率设置
                    if framerate != "保持原帧率":
                        cmd.extend(['-r', framerate])
                    
                    cmd.append(output_path)
                    
                    # 执行转换
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    # 如果GPU转换失败，尝试回退到CPU
                    if result.returncode != 0 and self.gpu_acceleration.get():
                        if "cuvid" in result.stderr or "nvenc" in result.stderr or "CUDA" in result.stderr:
                            if self.update_status:
                                self.update_status(f"GPU加速失败，回退到CPU转换: {file_info['name']}")
                            
                            # 重新构建CPU命令
                            cmd = ['ffmpeg', '-i', file_info['path'], '-y']
                            
                            # 添加质量设置
                            cmd.extend(['-crf', str(quality_preset['crf'])])
                            cmd.extend(['-preset', quality_preset['preset']])
                            
                            # 添加编码器设置
                            if target_format == 'mp4':
                                cmd.extend(['-c:v', 'libx264', '-c:a', 'aac'])
                            elif target_format == 'webm':
                                cmd.extend(['-c:v', 'libvpx-vp9', '-c:a', 'libopus'])
                            
                            # 添加分辨率设置
                            if resolution:
                                cmd.extend(['-s', resolution])
                            
                            # 添加帧率设置
                            if framerate != "保持原帧率":
                                cmd.extend(['-r', framerate])
                            
                            cmd.append(output_path)
                            
                            # 重新执行转换
                            result = subprocess.run(cmd, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        converted_count += 1
                    else:
                        failed_count += 1
                        print(f"转换失败 {file_info['name']}: {result.stderr}")
                        
                except Exception as e:
                    failed_count += 1
                    print(f"转换失败 {file_info['name']}: {e}")
                    
            # 转换完成
            self.progress_var.set(100)
            self.current_file_var.set("转换完成")
            
            # 在主线程中显示结果
            self.parent_frame.after(0, lambda: self.conversion_completed(
                converted_count, failed_count, output_dir))
                
        except Exception as e:
            # 在主线程中显示错误
            self.parent_frame.after(0, lambda: self.conversion_failed(str(e)))
            
    def conversion_completed(self, converted_count, failed_count, output_dir):
        """转换完成回调"""
        self.convert_btn.config(state="normal")
        
        message = f"视频转换完成！\n\n成功转换: {converted_count} 个文件"
        if failed_count > 0:
            message += f"\n转换失败: {failed_count} 个文件"
        message += f"\n\n输出目录: {output_dir}"
        
        messagebox.showinfo("转换完成", message)
        
        if self.update_status:
            self.update_status(f"转换完成: 成功 {converted_count} 个，失败 {failed_count} 个")
            
    def conversion_failed(self, error_msg):
        """转换失败回调"""
        self.convert_btn.config(state="normal")
        self.progress_var.set(0)
        self.current_file_var.set("转换失败")
        
        messagebox.showerror("转换失败", f"视频转换过程中发生错误:\n{error_msg}")
        
        if self.update_status:
            self.update_status(f"转换失败: {error_msg}")