# -*- coding: utf-8 -*-
"""图片格式转换功能模块"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import threading
from typing import List, Dict

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class ImageConverterTab:
    """图片格式转换功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.update_status = None  # 状态更新回调函数
        
        # 支持的图片格式
        self.supported_formats = {
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'BMP': ['.bmp'],
            'TIFF': ['.tiff', '.tif'],
            'GIF': ['.gif'],
            'WEBP': ['.webp'],
            'ICO': ['.ico']
        }
        
        # 文件列表
        self.file_list = []
        
        # 检查依赖库
        self.check_dependencies()
        
        # 创建界面组件
        self.create_widgets()
        
    def check_dependencies(self):
        """检查必要的依赖库是否已安装"""
        if not PIL_AVAILABLE:
            self.show_dependency_warning()
            
    def show_dependency_warning(self):
        """显示缺少依赖库的警告"""
        warning_msg = "缺少Pillow库，无法进行图片格式转换\n\n请运行以下命令安装：\nuv add pillow"
        
        warning_frame = tk.Frame(self.parent_frame, bg="#ffeeee", relief=tk.RAISED, bd=2)
        warning_frame.pack(fill=tk.X, padx=10, pady=5)
        
        warning_label = tk.Label(warning_frame, text=warning_msg, 
                               bg="#ffeeee", fg="#cc0000", 
                               justify=tk.LEFT, font=("微软雅黑", 10))
        warning_label.pack(padx=10, pady=10)
        
    def create_widgets(self):
        """创建界面组件"""
        if not PIL_AVAILABLE:
            return
            
        # 主要操作框架
        main_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 文件选择区域
        file_frame = tk.LabelFrame(main_frame, text="文件选择", bg=self.theme.bg_color,
                                 font=("微软雅黑", 10, "bold"))
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 按钮区域
        button_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        button_style = self.theme.get_button_style()
        
        # 添加文件按钮
        add_files_btn = tk.Button(button_frame, text="📁 添加文件", 
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
        columns = ('文件名', '格式', '大小', '路径')
        self.file_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        # 设置列标题
        for col in columns:
            self.file_tree.heading(col, text=col)
            
        # 设置列宽
        self.file_tree.column('文件名', width=200)
        self.file_tree.column('格式', width=80)
        self.file_tree.column('大小', width=100)
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
        
        # 目标格式选择
        format_frame = tk.Frame(settings_frame, bg=self.theme.bg_color)
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(format_frame, text="目标格式：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        self.target_format = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(format_frame, textvariable=self.target_format,
                                  values=list(self.supported_formats.keys()),
                                  state="readonly", width=15)
        format_combo.pack(side=tk.LEFT, padx=10)
        
        # 质量设置（仅对JPEG有效）
        quality_frame = tk.Frame(settings_frame, bg=self.theme.bg_color)
        quality_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(quality_frame, text="JPEG质量：", bg=self.theme.bg_color,
                font=("微软雅黑", 10)).pack(side=tk.LEFT)
        
        self.quality_var = tk.IntVar(value=95)
        quality_scale = tk.Scale(quality_frame, from_=1, to=100, orient=tk.HORIZONTAL,
                               variable=self.quality_var, length=200)
        quality_scale.pack(side=tk.LEFT, padx=10)
        
        tk.Label(quality_frame, text="(1-100, 仅JPEG格式有效)", bg=self.theme.bg_color,
                font=("微软雅黑", 9), fg="gray").pack(side=tk.LEFT, padx=5)
        
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
        self.convert_btn = tk.Button(convert_frame, text="🔄 开始转换", command=self.start_conversion,
                                   bg=success_style["bg"], fg=success_style["fg"], 
                                   font=("微软雅黑", 12, "bold"))
        self.convert_btn.pack(pady=10)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(convert_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(pady=5)
        
    def add_files(self):
        """添加文件"""
        if not PIL_AVAILABLE:
            messagebox.showerror("错误", "Pillow库未安装，无法进行图片转换")
            return
            
        filetypes = [("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.gif *.webp *.ico"),
                    ("所有文件", "*.*")]
        
        filenames = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=filetypes
        )
        
        # 如果选择了文件且输出目录为空，自动设置输出目录
        if filenames and not self.output_dir_var.get():
            self.output_dir_var.set(os.path.dirname(filenames[0]))
        
        for filename in filenames:
            self.add_file_to_list(filename)
            
    def add_folder(self):
        """添加文件夹中的所有图片"""
        if not PIL_AVAILABLE:
            messagebox.showerror("错误", "Pillow库未安装，无法进行图片转换")
            return
            
        folder_path = filedialog.askdirectory(title="选择包含图片的文件夹")
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
            
            # 添加到列表
            file_info = {
                'name': file_name,
                'format': file_ext,
                'size': file_size_str,
                'path': file_path
            }
            
            self.file_list.append(file_info)
            
            # 添加到TreeView
            self.file_tree.insert('', 'end', values=(file_name, file_ext, file_size_str, file_path))
            
            if self.update_status:
                self.update_status(f"已添加文件: {file_name}")
                
        except Exception as e:
            messagebox.showerror("错误", f"添加文件失败: {e}")
            
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
            file_path = values[3]
            
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
        if not PIL_AVAILABLE:
            messagebox.showerror("错误", "Pillow库未安装，无法进行图片转换")
            return
            
        # 验证输入
        if not self.validate_inputs():
            return
            
        # 禁用转换按钮
        self.convert_btn.config(state="disabled")
        self.progress_var.set(0)
        
        if self.update_status:
            self.update_status("开始转换图片...")
        
        # 在新线程中执行转换
        thread = threading.Thread(target=self.convert_images)
        thread.daemon = True
        thread.start()
        
    def validate_inputs(self):
        """验证输入参数"""
        if not self.file_list:
            messagebox.showerror("错误", "请先添加要转换的图片文件")
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
        
    def convert_images(self):
        """转换图片（在后台线程中执行）"""
        try:
            target_format = self.target_format.get()
            output_dir = self.output_dir_var.get()
            quality = self.quality_var.get()
            
            total_files = len(self.file_list)
            converted_count = 0
            failed_count = 0
            
            for i, file_info in enumerate(self.file_list):
                try:
                    # 更新进度
                    progress = (i / total_files) * 100
                    self.progress_var.set(progress)
                    
                    if self.update_status:
                        self.update_status(f"正在转换: {file_info['name']} ({i+1}/{total_files})")
                    
                    # 打开图片
                    with Image.open(file_info['path']) as img:
                        # 处理透明度
                        if target_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                            # JPEG不支持透明度，转换为RGB
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            if img.mode == 'P':
                                img = img.convert('RGBA')
                            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                            img = background
                        elif target_format == 'PNG' and img.mode == 'CMYK':
                            # PNG不支持CMYK，转换为RGB
                            img = img.convert('RGB')
                        
                        # 生成输出文件名
                        base_name = Path(file_info['name']).stem
                        target_ext = self.supported_formats[target_format][0]
                        output_filename = f"{base_name}{target_ext}"
                        output_path = os.path.join(output_dir, output_filename)
                        
                        # 如果文件已存在，添加序号
                        counter = 1
                        while os.path.exists(output_path):
                            output_filename = f"{base_name}_{counter}{target_ext}"
                            output_path = os.path.join(output_dir, output_filename)
                            counter += 1
                        
                        # 保存图片
                        save_kwargs = {}
                        if target_format == 'JPEG':
                            save_kwargs['quality'] = quality
                            save_kwargs['optimize'] = True
                        elif target_format == 'PNG':
                            save_kwargs['optimize'] = True
                        
                        img.save(output_path, format=target_format, **save_kwargs)
                        converted_count += 1
                        
                except Exception as e:
                    failed_count += 1
                    print(f"转换失败 {file_info['name']}: {e}")
                    
            # 转换完成
            self.progress_var.set(100)
            
            # 在主线程中显示结果
            self.parent_frame.after(0, lambda: self.conversion_completed(
                converted_count, failed_count, output_dir))
                
        except Exception as e:
            # 在主线程中显示错误
            self.parent_frame.after(0, lambda: self.conversion_failed(str(e)))
            
    def conversion_completed(self, converted_count, failed_count, output_dir):
        """转换完成回调"""
        self.convert_btn.config(state="normal")
        
        message = f"图片转换完成！\n\n成功转换: {converted_count} 个文件"
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
        
        messagebox.showerror("转换失败", f"图片转换过程中发生错误:\n{error_msg}")
        
        if self.update_status:
            self.update_status(f"转换失败: {error_msg}")