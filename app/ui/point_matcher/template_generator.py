# -*- coding: utf-8 -*-
"""模板生成器模块"""

import pandas as pd
from tkinter import filedialog, messagebox

class TemplateGenerator:
    """模板生成器类"""
    
    def __init__(self, log_callback=None):
        """
        初始化模板生成器
        
        Args:
            log_callback (callable): 日志回调函数
        """
        self.log_callback = log_callback
        
    def log(self, message):
        """记录日志"""
        if self.log_callback:
            self.log_callback(message)
    
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
                return True
        except Exception as e:
            error_msg = f"保存模板时发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
            return False
    
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
                return True
        except Exception as e:
            error_msg = f"保存模板时发生错误: {str(e)}"
            self.log(error_msg)
            messagebox.showerror("错误", error_msg)
            return False