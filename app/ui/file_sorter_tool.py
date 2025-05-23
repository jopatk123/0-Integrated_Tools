import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime
import time
from app.utils.theme import ThemeManager

class FileSorterTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 设置变量
        self.folder_path = tk.StringVar()
        self.time_value = tk.StringVar(value="3")
        self.time_unit = tk.StringVar(value="分钟")
        self.progress_var = tk.DoubleVar()
        
        self.create_widgets()
    
    def create_widgets(self):
        # 文件夹选择部分
        folder_frame = ttk.Frame(self.parent_frame, padding="10")
        folder_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(folder_frame, text="选择文件夹:").pack(side=tk.LEFT, padx=5)
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path, width=50)
        folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        button_style = self.theme.get_button_style()
        browse_btn = tk.Button(folder_frame, text="浏览...", 
                             command=self.browse_folder,
                             bg=button_style["bg"], fg=button_style["fg"])
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 时间阈值设置部分
        time_frame = ttk.Frame(self.parent_frame, padding="10")
        time_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(time_frame, text="时间阈值:").pack(side=tk.LEFT, padx=5)
        
        time_entry = ttk.Entry(time_frame, textvariable=self.time_value, width=10)
        time_entry.pack(side=tk.LEFT, padx=5)
        
        time_unit_combo = ttk.Combobox(time_frame, textvariable=self.time_unit, 
                                      values=["秒", "分钟", "小时", "天"], 
                                      width=10, state="readonly")
        time_unit_combo.pack(side=tk.LEFT, padx=5)
        
        # 操作按钮
        btn_frame = ttk.Frame(self.parent_frame, padding="10")
        btn_frame.pack(fill=tk.X, pady=10)
        
        sort_btn = tk.Button(btn_frame, text="开始分类", 
                           command=self.start_sorting,
                           bg=button_style["bg"], fg=button_style["fg"])
        sort_btn.pack(side=tk.LEFT, padx=5)
        
        # 日志区域
        log_frame = ttk.LabelFrame(self.parent_frame, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 进度条
        progress_frame = ttk.Frame(self.parent_frame, padding="10")
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, padx=5)
    
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.log(f"已选择文件夹: {folder_selected}")
    
    def log(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{current_time}] {message}\n")
        self.log_text.see(tk.END)
        self.parent_frame.update()
    
    def get_time_threshold_seconds(self):
        try:
            value = float(self.time_value.get())
            unit = self.time_unit.get()
            
            if unit == "秒":
                return value
            elif unit == "分钟":
                return value * 60
            elif unit == "小时":
                return value * 3600
            elif unit == "天":
                return value * 86400
            else:
                return value * 60  # 默认为分钟
        except ValueError:
            messagebox.showerror("错误", "请输入有效的时间值")
            return None
    
    def start_sorting(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
        
        threshold_seconds = self.get_time_threshold_seconds()
        if threshold_seconds is None:
            return
        
        try:
            self.log(f"开始扫描文件夹: {folder_path}")
            self.log(f"时间阈值设置为: {self.time_value.get()} {self.time_unit.get()}")
            
            # 获取所有文件及其修改时间
            files_with_time = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 只处理直接位于所选文件夹下的文件
                    if os.path.dirname(file_path) == folder_path:
                        mod_time = os.path.getmtime(file_path)
                        files_with_time.append((file_path, mod_time))
            
            if not files_with_time:
                self.log("没有找到文件")
                messagebox.showinfo("信息", "所选文件夹中没有文件")
                return
            
            # 按修改时间排序
            files_with_time.sort(key=lambda x: x[1])
            
            # 分组
            groups = []
            current_group = [files_with_time[0]]
            
            for i in range(1, len(files_with_time)):
                current_file = files_with_time[i]
                prev_file = current_group[-1]
                
                # 如果当前文件与上一个文件的时间差小于阈值，则加入当前组
                if current_file[1] - prev_file[1] <= threshold_seconds:
                    current_group.append(current_file)
                else:
                    # 否则创建新组
                    groups.append(current_group)
                    current_group = [current_file]
            
            # 添加最后一组
            if current_group:
                groups.append(current_group)
            
            self.log(f"找到 {len(files_with_time)} 个文件，分为 {len(groups)} 个组")
            
            # 创建文件夹并移动文件
            total_files = len(files_with_time)
            processed_files = 0
            
            for i, group in enumerate(groups):
                # 创建新文件夹
                timestamp = datetime.fromtimestamp(group[0][1]).strftime("%Y%m%d_%H%M%S")
                group_folder = os.path.join(folder_path, f"Group_{timestamp}")
                
                if not os.path.exists(group_folder):
                    os.makedirs(group_folder)
                    self.log(f"创建文件夹: {os.path.basename(group_folder)}")
                
                # 移动文件
                for file_path, _ in group:
                    file_name = os.path.basename(file_path)
                    dest_path = os.path.join(group_folder, file_name)
                    
                    # 如果目标文件已存在，添加序号
                    if os.path.exists(dest_path):
                        name, ext = os.path.splitext(file_name)
                        counter = 1
                        while os.path.exists(os.path.join(group_folder, f"{name}_{counter}{ext}")):
                            counter += 1
                        dest_path = os.path.join(group_folder, f"{name}_{counter}{ext}")
                    
                    shutil.move(file_path, dest_path)
                    self.log(f"移动文件: {file_name} -> {os.path.basename(group_folder)}")
                    
                    processed_files += 1
                    self.progress_var.set((processed_files / total_files) * 100)
                    self.parent_frame.update()
            
            self.log("文件分类完成！")
            messagebox.showinfo("完成", "文件分类已完成！")
            self.progress_var.set(100)
            
        except Exception as e:
            self.log(f"错误: {str(e)}")
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")