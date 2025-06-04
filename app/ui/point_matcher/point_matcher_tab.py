# -*- coding: utf-8 -*-
"""点匹配功能选项卡模块"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import os
from .distance_calculator import haversine_distance_vectorized
from .template_generator import TemplateGenerator

class PointMatcherTab:
    """点匹配功能选项卡类"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 设置变量
        self.data_file_path = tk.StringVar()
        self.point_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.status_var = tk.StringVar(value="就绪")
        
        # 创建模板生成器
        self.template_generator = TemplateGenerator(log_callback=self.log)
        
        # 创建界面
        self.create_widgets()
        
        # 状态更新回调（由主工具设置）
        self.update_status = None
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 说明文本
        instruction_frame = tk.LabelFrame(main_frame, text="使用说明", 
                                        bg=self.theme.bg_color, font=("微软雅黑", 10, "bold"))
        instruction_frame.pack(fill=tk.X, pady=5)
        
        instructions = (
            "1. 准备两个Excel文件：\n"
            "   - Data.xlsx：包含基准点位数据（点位名称、经度、纬度）\n"
            "   - Point.xlsx：包含需要匹配的目标点位数据（点位名称、经度、纬度）\n"
            "2. 可以下载模板文件作为参考\n"
            "3. 选择这两个文件\n"
            "4. 选择输出保存位置\n"
            "5. 点击'开始计算'按钮\n"
            "6. 结果将保存为Excel文件"
        )
        instruction_label = tk.Label(instruction_frame, text=instructions, 
                                   justify=tk.LEFT, bg=self.theme.bg_color,
                                   font=("微软雅黑", 9))
        instruction_label.pack(anchor=tk.W, padx=10, pady=5)
        
        # 模板下载按钮
        template_frame = tk.Frame(instruction_frame, bg=self.theme.bg_color)
        template_frame.pack(fill=tk.X, pady=5, padx=10)
        
        button_style = self.theme.get_button_style()
        
        data_template_btn = tk.Button(template_frame, text="下载基准点位模板 (Data.xlsx)", 
                                    command=self.template_generator.download_data_template,
                                    bg=button_style["bg"], fg=button_style["fg"],
                                    font=("微软雅黑", 9))
        data_template_btn.pack(side=tk.LEFT, padx=5)
        
        point_template_btn = tk.Button(template_frame, text="下载目标点位模板 (Point.xlsx)", 
                                     command=self.template_generator.download_point_template,
                                     bg=button_style["bg"], fg=button_style["fg"],
                                     font=("微软雅黑", 9))
        point_template_btn.pack(side=tk.LEFT, padx=5)
        
        # 文件选择区域
        file_frame = tk.LabelFrame(main_frame, text="文件选择", 
                                 bg=self.theme.bg_color, font=("微软雅黑", 10, "bold"))
        file_frame.pack(fill=tk.X, pady=5)
        
        # Data文件选择
        data_file_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        data_file_frame.pack(fill=tk.X, pady=2, padx=10)
        
        tk.Label(data_file_frame, text="基准点位文件 (Data.xlsx):", 
               bg=self.theme.bg_color, font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        data_entry = tk.Entry(data_file_frame, textvariable=self.data_file_path, 
                            width=50, font=("微软雅黑", 9))
        data_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        data_browse_btn = tk.Button(data_file_frame, text="浏览...", 
                                  command=self.browse_data_file,
                                  bg=button_style["bg"], fg=button_style["fg"],
                                  font=("微软雅黑", 9))
        data_browse_btn.pack(side=tk.LEFT, padx=5)
        
        # Point文件选择
        point_file_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        point_file_frame.pack(fill=tk.X, pady=2, padx=10)
        
        tk.Label(point_file_frame, text="目标点位文件 (Point.xlsx):", 
               bg=self.theme.bg_color, font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        point_entry = tk.Entry(point_file_frame, textvariable=self.point_file_path, 
                             width=50, font=("微软雅黑", 9))
        point_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        point_browse_btn = tk.Button(point_file_frame, text="浏览...", 
                                   command=self.browse_point_file,
                                   bg=button_style["bg"], fg=button_style["fg"],
                                   font=("微软雅黑", 9))
        point_browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 输出文件选择
        output_file_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        output_file_frame.pack(fill=tk.X, pady=2, padx=10)
        
        tk.Label(output_file_frame, text="输出保存位置:", 
               bg=self.theme.bg_color, font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        output_entry = tk.Entry(output_file_frame, textvariable=self.output_dir, 
                              width=50, font=("微软雅黑", 9))
        output_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        output_browse_btn = tk.Button(output_file_frame, text="选择位置...", 
                                    command=self.browse_output_dir,
                                    bg=button_style["bg"], fg=button_style["fg"],
                                    font=("微软雅黑", 9))
        output_browse_btn.pack(side=tk.LEFT, padx=5)
        
        # 输出文件名
        output_name_frame = tk.Frame(file_frame, bg=self.theme.bg_color)
        output_name_frame.pack(fill=tk.X, pady=2, padx=10)
        
        tk.Label(output_name_frame, text="输出文件名:", 
               bg=self.theme.bg_color, font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        output_name_entry = tk.Entry(output_name_frame, textvariable=self.output_file_path, 
                                   width=50, font=("微软雅黑", 9))
        output_name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.output_file_path.set("Point_with_closest_matches.xlsx")
        
        # 操作按钮
        button_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=10)
        
        calc_btn = tk.Button(button_frame, text="开始计算", 
                           command=self.start_calculation,
                           bg=button_style["bg"], fg=button_style["fg"],
                           font=("微软雅黑", 10, "bold"), width=20)
        calc_btn.pack(side=tk.LEFT, padx=10)
        
        # 日志区域
        log_frame = tk.LabelFrame(main_frame, text="处理日志", 
                                bg=self.theme.bg_color, font=("微软雅黑", 10, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建日志文本框和滚动条的容器
        log_container = tk.Frame(log_frame, bg=self.theme.bg_color)
        log_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = tk.Text(log_container, wrap=tk.WORD, height=10, 
                              font=("微软雅黑", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = tk.Scrollbar(log_container, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def browse_data_file(self):
        """浏览基准点位文件"""
        filename = filedialog.askopenfilename(
            title="选择基准点位文件",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if filename:
            self.data_file_path.set(filename)
            # 设置默认输出位置为基准点文件所在目录
            if not self.output_dir.get():
                default_dir = os.path.dirname(filename)
                self.output_dir.set(default_dir)
            self.log(f"已选择基准点位文件: {filename}")
    
    def browse_point_file(self):
        """浏览目标点位文件"""
        filename = filedialog.askopenfilename(
            title="选择目标点位文件",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if filename:
            self.point_file_path.set(filename)
            self.log(f"已选择目标点位文件: {filename}")
    
    def browse_output_dir(self):
        """浏览输出保存位置"""
        directory = filedialog.askdirectory(
            title="选择输出保存位置"
        )
        if directory:
            self.output_dir.set(directory)
            self.log(f"已选择输出位置: {directory}")
    
    def log(self, message):
        """记录日志"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.parent_frame.update_idletasks()
    
    def start_calculation(self):
        """开始计算最近点位匹配"""
        # 检查文件是否已选择
        if not self.data_file_path.get() or not self.point_file_path.get():
            messagebox.showerror("错误", "请先选择基准点位文件和目标点位文件！")
            return
        
        # 检查输出位置是否已选择
        if not self.output_dir.get():
            messagebox.showerror("错误", "请先选择输出保存位置！")
            return
        
        # 检查输出文件名是否已填写
        if not self.output_file_path.get():
            messagebox.showerror("错误", "请填写输出文件名！")
            return
        
        # 检查文件是否存在
        if not os.path.exists(self.data_file_path.get()):
            messagebox.showerror("错误", f"基准点位文件不存在: {self.data_file_path.get()}")
            return
        
        if not os.path.exists(self.point_file_path.get()):
            messagebox.showerror("错误", f"目标点位文件不存在: {self.point_file_path.get()}")
            return
        
        try:
            if self.update_status:
                self.update_status("正在计算...")
            self.log("开始计算最近点位匹配...")
            
            # 读取Excel文件
            self.log("正在读取Excel文件...")
            data_df = pd.read_excel(self.data_file_path.get())
            point_df = pd.read_excel(self.point_file_path.get())
            
            # 检查必要的列是否存在
            required_data_columns = ['点位名称', '经度', '纬度']
            required_point_columns = ['点位名称', '经度', '纬度']
            
            missing_data_columns = [col for col in required_data_columns if col not in data_df.columns]
            missing_point_columns = [col for col in required_point_columns if col not in point_df.columns]
            
            if missing_data_columns:
                error_msg = f"基准点位文件缺少必要的列: {', '.join(missing_data_columns)}"
                self.log(error_msg)
                messagebox.showerror("错误", error_msg)
                if self.update_status:
                    self.update_status("就绪")
                return
            
            if missing_point_columns:
                error_msg = f"目标点位文件缺少必要的列: {', '.join(missing_point_columns)}"
                self.log(error_msg)
                messagebox.showerror("错误", error_msg)
                if self.update_status:
                    self.update_status("就绪")
                return
            
            # 创建结果DataFrame
            result_df = point_df.copy()
            result_df['最近点位名称'] = ''
            result_df['最近距离(米)'] = 0.0
            
            self.log(f"正在计算{len(point_df)}个点位的最近匹配...")
            self.log("使用优化算法进行向量化计算，大幅提升计算速度...")
            
            # 提取基准点位的经纬度数组
            data_lats = data_df['纬度'].values
            data_lons = data_df['经度'].values
            data_names = data_df['点位名称'].values
            
            # 为Point表中的每个点找到Data表中最近的点（使用向量化计算）
            for i, point_row in point_df.iterrows():
                # 获取当前点的经纬度
                point_lat = point_row['纬度']
                point_lon = point_row['经度']
                
                # 使用向量化函数一次计算到所有基准点的距离
                distances = haversine_distance_vectorized(point_lat, point_lon, data_lats, data_lons)
                
                # 找到最小距离的索引
                min_idx = np.argmin(distances)
                min_distance = distances[min_idx]
                closest_name = data_names[min_idx]
                
                # 将最近点的信息添加到结果中
                result_df.at[i, '最近点位名称'] = closest_name
                result_df.at[i, '最近距离(米)'] = min_distance
                
                # 更新进度（减少更新频率以提高性能）
                if (i + 1) % 50 == 0 or i == len(point_df) - 1:
                    self.log(f"已处理 {i + 1}/{len(point_df)} 个点位")
                    self.parent_frame.update_idletasks()
            
            # 保存结果到新的Excel文件
            output_file = os.path.join(self.output_dir.get(), self.output_file_path.get())
            
            # 将数值列转换为字符串，避免科学计数法显示
            # 将距离值转换为字符串，保留两位小数
            result_df['最近距离(米)'] = result_df['最近距离(米)'].apply(lambda x: f"{x:.2f}")
            
            # 使用ExcelWriter保存，并设置选项
            self.log(f"正在保存结果到 {output_file}...")
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, sheet_name='最近点位匹配结果')
                
                # 获取工作表
                worksheet = writer.sheets['最近点位匹配结果']
                
                # 调整列宽以适应内容
                for idx, col in enumerate(result_df.columns):
                    max_length = max(result_df[col].astype(str).map(len).max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = max_length
            
            self.log(f"计算完成！结果已保存到 {output_file}")
            self.log("所有数值已转换为文本格式，避免科学计数法显示问题")
            
            messagebox.showinfo("完成", f"计算完成！结果已保存到 {output_file}")
            if self.update_status:
                self.update_status("就绪")
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
            if self.update_status:
                self.update_status("就绪")