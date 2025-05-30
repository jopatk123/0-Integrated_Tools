import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    计算两个经纬度坐标点之间的距离（单位：米）
    使用Haversine公式计算球面距离
    """
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371000  # 地球半径（米）
    distance = r * c
    
    return distance

class PointMatcherTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 设置变量
        self.data_file_path = tk.StringVar()
        self.point_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.parent_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="最近点位匹配工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 说明文本
        instruction_frame = ttk.LabelFrame(main_frame, text="使用说明", padding="10")
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
        instruction_label = ttk.Label(instruction_frame, text=instructions, justify=tk.LEFT)
        instruction_label.pack(anchor=tk.W)
        
        # 模板下载按钮
        template_frame = ttk.Frame(instruction_frame)
        template_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(template_frame, text="下载基准点位模板 (Data.xlsx)", command=self.download_data_template).pack(side=tk.LEFT, padx=5)
        ttk.Button(template_frame, text="下载目标点位模板 (Point.xlsx)", command=self.download_point_template).pack(side=tk.LEFT, padx=5)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        # Data文件选择
        data_file_frame = ttk.Frame(file_frame)
        data_file_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(data_file_frame, text="基准点位文件 (Data.xlsx):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(data_file_frame, textvariable=self.data_file_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(data_file_frame, text="浏览...", command=self.browse_data_file).pack(side=tk.LEFT, padx=5)
        
        # Point文件选择
        point_file_frame = ttk.Frame(file_frame)
        point_file_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(point_file_frame, text="目标点位文件 (Point.xlsx):").pack(side=tk.LEFT, padx=5)
        ttk.Entry(point_file_frame, textvariable=self.point_file_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(point_file_frame, text="浏览...", command=self.browse_point_file).pack(side=tk.LEFT, padx=5)
        
        # 输出文件选择
        output_file_frame = ttk.Frame(file_frame)
        output_file_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(output_file_frame, text="输出保存位置:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(output_file_frame, textvariable=self.output_dir, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_file_frame, text="选择位置...", command=self.browse_output_dir).pack(side=tk.LEFT, padx=5)
        
        # 输出文件名
        output_name_frame = ttk.Frame(file_frame)
        output_name_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(output_name_frame, text="输出文件名:").pack(side=tk.LEFT, padx=5)
        ttk.Entry(output_name_frame, textvariable=self.output_file_path, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.output_file_path.set("Point_with_closest_matches.xlsx")
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="开始计算", command=self.start_calculation, width=20).pack(side=tk.LEFT, padx=10)
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def browse_data_file(self):
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
        filename = filedialog.askopenfilename(
            title="选择目标点位文件",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
        )
        if filename:
            self.point_file_path.set(filename)
            self.log(f"已选择目标点位文件: {filename}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(
            title="选择输出保存位置"
        )
        if directory:
            self.output_dir.set(directory)
            self.log(f"已选择输出位置: {directory}")
    
    def download_data_template(self):
        """下载基准点位数据模板"""
        try:
            # 创建模板数据
            template_data = {
                '点位名称': ['基准点1', '基准点2', '基准点3'],
                '经度': [116.3974, 116.4074, 116.4174],
                '纬度': [39.9093, 39.9193, 39.9293]
            }
            
            template_df = pd.DataFrame(template_data)
            
            # 选择保存位置
            filename = filedialog.asksaveasfilename(
                title="保存基准点位模板",
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx")],
                initialfile="Data_template.xlsx"
            )
            
            if filename:
                template_df.to_excel(filename, index=False)
                self.log(f"基准点位模板已保存到: {filename}")
                messagebox.showinfo("成功", f"基准点位模板已保存到: {filename}")
        except Exception as e:
            error_msg = f"保存模板时发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
    
    def download_point_template(self):
        """下载目标点位数据模板"""
        try:
            # 创建模板数据
            template_data = {
                '点位名称': ['目标点1', '目标点2', '目标点3'],
                '经度': [116.3984, 116.4084, 116.4184],
                '纬度': [39.9103, 39.9203, 39.9303]
            }
            
            template_df = pd.DataFrame(template_data)
            
            # 选择保存位置
            filename = filedialog.asksaveasfilename(
                title="保存目标点位模板",
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx")],
                initialfile="Point_template.xlsx"
            )
            
            if filename:
                template_df.to_excel(filename, index=False)
                self.log(f"目标点位模板已保存到: {filename}")
                messagebox.showinfo("成功", f"目标点位模板已保存到: {filename}")
        except Exception as e:
            error_msg = f"保存模板时发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.parent_frame.update_idletasks()
    
    def start_calculation(self):
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
            self.status_var.set("正在计算...")
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
                self.status_var.set("就绪")
                return
            
            if missing_point_columns:
                error_msg = f"目标点位文件缺少必要的列: {', '.join(missing_point_columns)}"
                self.log(error_msg)
                messagebox.showerror("错误", error_msg)
                self.status_var.set("就绪")
                return
            
            # 创建结果DataFrame
            result_df = point_df.copy()
            result_df['最近点位名称'] = ''
            result_df['最近距离(米)'] = 0.0
            
            self.log(f"正在计算{len(point_df)}个点位的最近匹配...")
            
            # 为Point表中的每个点找到Data表中最近的点
            for i, point_row in point_df.iterrows():
                min_distance = float('inf')
                closest_point = None
                
                # 获取当前点的经纬度
                point_lat = point_row['纬度']
                point_lon = point_row['经度']
                
                # 计算与Data表中所有点的距离
                for j, data_row in data_df.iterrows():
                    data_lat = data_row['纬度']
                    data_lon = data_row['经度']
                    
                    # 计算距离
                    distance = haversine_distance(point_lat, point_lon, data_lat, data_lon)
                    
                    # 更新最近点
                    if distance < min_distance:
                        min_distance = distance
                        closest_point = data_row
                
                # 将最近点的信息添加到结果中
                if closest_point is not None:
                    result_df.at[i, '最近点位名称'] = closest_point['点位名称']
                    result_df.at[i, '最近距离(米)'] = min_distance
                
                # 更新进度
                if (i + 1) % 10 == 0 or i == len(point_df) - 1:
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
            self.status_var.set("就绪")
            
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
            self.status_var.set("就绪")