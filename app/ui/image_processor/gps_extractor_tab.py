# -*- coding: utf-8 -*-
"""图片GPS提取功能模块"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import threading
import shutil
import os
import pathlib

class GPSExtractorTab:
    """图片GPS提取功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.folder_path = tk.StringVar()
        self.image_data = []
        self.renamed_count = 0
        self.update_status = None  # 状态更新回调函数
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建界面组件"""
        # 顶部框架 - 选择文件夹
        top_frame = ttk.Frame(self.parent_frame, padding="10")
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="选择图片文件夹:").pack(side=tk.LEFT, padx=(0, 10))
        
        entry = ttk.Entry(top_frame, textvariable=self.folder_path, width=50)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        button_style = self.theme.get_button_style()
        browse_btn = tk.Button(top_frame, text="浏览...", 
                             command=self.browse_folder,
                             bg=button_style["bg"], fg=button_style["fg"])
        browse_btn.pack(side=tk.LEFT)
        
        # 中间框架 - 表格显示
        mid_frame = ttk.Frame(self.parent_frame, padding="10")
        mid_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建表格
        columns = ("文件名", "完整路径", "经度", "纬度", "重命名")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(mid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        scrollbar_x = ttk.Scrollbar(mid_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scrollbar_x.set)
        
        # 放置表格和滚动条
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 底部框架 - 按钮
        bottom_frame = ttk.Frame(self.parent_frame, padding="10")
        bottom_frame.pack(fill=tk.X)
        
        scan_btn = tk.Button(bottom_frame, text="扫描图片", 
                           command=self.start_scan,
                           bg=button_style["bg"], fg=button_style["fg"])
        scan_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(bottom_frame, text="导出Excel", 
                             command=self.export_excel,
                             bg=button_style["bg"], fg=button_style["fg"])
        export_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        import_btn = tk.Button(bottom_frame, text="导入Excel", 
                             command=self.import_excel,
                             bg=button_style["bg"], fg=button_style["fg"])
        import_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        rename_btn = tk.Button(bottom_frame, text="重命名图片", 
                             command=self.rename_images,
                             bg=button_style["bg"], fg=button_style["fg"])
        rename_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        rename_folder_btn = tk.Button(bottom_frame, text="重命名文件夹", 
                                   command=self.rename_folders,
                                   bg=button_style["bg"], fg=button_style["fg"])
        rename_folder_btn.pack(side=tk.LEFT)
    
    def browse_folder(self):
        """浏览文件夹"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
    
    def start_scan(self):
        """开始扫描图片"""
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
        
        # 清空表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.image_data = []
        if self.update_status:
            self.update_status("正在扫描...")
        
        # 使用线程避免UI冻结
        threading.Thread(target=self.scan_folder, args=(folder,), daemon=True).start()
    
    def scan_folder(self, folder):
        """扫描文件夹中的图片"""
        image_extensions = (".jpg", ".jpeg", ".png", ".tiff", ".bmp")
        count = 0
        
        for root, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(image_extensions):
                    count += 1
                    if self.update_status:
                        self.update_status(f"已扫描 {count} 张图片...")
                    
                    file_path = os.path.join(root, file)
                    lat, lon = self.get_gps_info(file_path)
                    
                    self.image_data.append({
                        "文件名": file,
                        "完整路径": file_path,
                        "经度": lon,
                        "纬度": lat,
                        "重命名": ""
                    })
                    
                    # 更新UI（在主线程中）
                    self.parent_frame.after(0, self.add_to_tree, file, file_path, lon, lat)
        
        self.parent_frame.after(0, self._scan_complete, count)
    
    def add_to_tree(self, filename, filepath, lon, lat):
        """添加到表格"""
        self.tree.insert("", tk.END, values=(filename, filepath, lon, lat, ""))
    
    def _scan_complete(self, count):
        """扫描完成"""
        if self.update_status:
            self.update_status(f"扫描完成，共找到 {count} 张图片")
    
    def get_gps_info(self, file_path):
        """提取图片GPS信息"""
        try:
            with Image.open(file_path) as img:
                exif_data = img._getexif()
                if not exif_data:
                    return "N/A", "N/A"
                
                # 提取GPS信息
                gps_info = {}
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "GPSInfo":
                        for gps_tag, gps_value in value.items():
                            gps_info[GPSTAGS.get(gps_tag, gps_tag)] = gps_value
                
                # 计算经纬度
                if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                    lat = self.convert_to_degrees(gps_info["GPSLatitude"])
                    lon = self.convert_to_degrees(gps_info["GPSLongitude"])
                    
                    # 考虑南纬和西经为负值
                    if gps_info.get("GPSLatitudeRef", "N") == "S":
                        lat = -lat
                    if gps_info.get("GPSLongitudeRef", "E") == "W":
                        lon = -lon
                    
                    return round(lat, 6), round(lon, 6)
        except Exception as e:
            print(f"处理图片 {file_path} 时出错: {e}")
        
        return "N/A", "N/A"
    
    def convert_to_degrees(self, value):
        """将GPS坐标从度分秒格式转换为十进制度"""
        d, m, s = value
        return d + (m / 60.0) + (s / 3600.0)
    
    def export_excel(self):
        """导出Excel文件"""
        if not self.image_data:
            messagebox.showinfo("提示", "没有数据可导出")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
            title="保存 Excel 文件"
        )
        
        if file_path:
            try:
                df = pd.DataFrame(self.image_data)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("成功", f"数据已成功导出到 {file_path}\n\n您可以在Excel中的'重命名'列填写新的文件名，然后通过'导入Excel'功能将其导回程序，最后点击'重命名图片'按钮完成重命名操作。")
                if self.update_status:
                    self.update_status("数据导出完成")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def import_excel(self):
        """导入Excel文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel 文件", "*.xlsx")],
            title="选择Excel文件"
        )
        
        if not file_path:
            return
        
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 检查必要的列是否存在
            required_columns = ["文件名", "完整路径", "重命名"]
            for col in required_columns:
                if col not in df.columns:
                    messagebox.showerror("错误", f"Excel文件缺少必要的列: {col}")
                    return
            
            # 清空当前数据和表格
            self.image_data = []
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # 导入数据
            count = 0
            for _, row in df.iterrows():
                # 检查文件是否存在
                if os.path.exists(row["完整路径"]):
                    count += 1
                    # 添加到数据列表
                    image_info = {
                        "文件名": row["文件名"],
                        "完整路径": row["完整路径"],
                        "经度": row.get("经度", "N/A"),
                        "纬度": row.get("纬度", "N/A"),
                        "重命名": row.get("重命名", "")
                    }
                    self.image_data.append(image_info)
                    
                    # 更新表格
                    self.tree.insert("", tk.END, values=(
                        image_info["文件名"],
                        image_info["完整路径"],
                        image_info["经度"],
                        image_info["纬度"],
                        image_info["重命名"]
                    ))
            
            if self.update_status:
                self.update_status(f"已导入 {count} 张图片信息")
            messagebox.showinfo("成功", f"已成功导入 {count} 张图片信息")
            
        except Exception as e:
            messagebox.showerror("错误", f"导入失败: {e}")
    
    def rename_images(self):
        """重命名图片"""
        if not self.image_data:
            messagebox.showinfo("提示", "没有图片数据可重命名")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", "确定要根据Excel中的'重命名'列重命名图片吗？\n此操作不可撤销！"):
            return
        
        self.renamed_count = 0
        errors = []
        
        for image_info in self.image_data:
            old_path = image_info["完整路径"]
            new_name = image_info.get("重命名", "").strip()
            
            # 如果重命名字段为空，跳过
            if not new_name:
                continue
            
            try:
                # 检查文件是否存在
                if not os.path.exists(old_path):
                    errors.append(f"文件不存在: {old_path}")
                    continue
                
                # 获取文件目录和扩展名
                directory = os.path.dirname(old_path)
                _, extension = os.path.splitext(old_path)
                
                # 构建新路径
                new_path = os.path.join(directory, new_name + extension)
                
                # 检查新文件名是否已存在
                if os.path.exists(new_path) and old_path.lower() != new_path.lower():
                    errors.append(f"目标文件已存在: {new_path}")
                    continue
                
                # 重命名文件
                shutil.move(old_path, new_path)
                
                # 更新数据
                image_info["文件名"] = new_name + extension
                image_info["完整路径"] = new_path
                
                self.renamed_count += 1
                
            except Exception as e:
                errors.append(f"重命名 {old_path} 失败: {str(e)}")
        
        # 更新表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for image_info in self.image_data:
            self.tree.insert("", tk.END, values=(
                image_info["文件名"],
                image_info["完整路径"],
                image_info["经度"],
                image_info["纬度"],
                image_info["重命名"]
            ))
        
        # 显示结果
        if errors:
            error_message = "\n".join(errors[:10])
            if len(errors) > 10:
                error_message += f"\n...还有 {len(errors) - 10} 个错误未显示"
            
            messagebox.showwarning("警告", f"已成功重命名 {self.renamed_count} 张图片，但有 {len(errors)} 个错误:\n{error_message}")
        else:
            messagebox.showinfo("成功", f"已成功重命名 {self.renamed_count} 张图片")
        
        if self.update_status:
            self.update_status(f"已重命名 {self.renamed_count} 张图片")
    
    def rename_folders(self):
        """重命名文件夹"""
        if not self.image_data:
            messagebox.showinfo("提示", "没有图片数据可用于重命名文件夹")
            return
        
        # 确认对话框
        if not messagebox.askyesno("确认", "确定要将图片所在的文件夹重命名为图片名称吗？\n此操作不可撤销！"):
            return
        
        # 获取选中的图片
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请先选择要用于重命名文件夹的图片")
            return
        
        renamed_count = 0
        errors = []
        
        for item in selected_items:
            # 获取选中项的值
            values = self.tree.item(item, "values")
            file_path = values[1]  # 完整路径在第二列
            file_name = values[0]  # 文件名在第一列
            
            try:
                # 检查文件是否存在
                if not os.path.exists(file_path):
                    errors.append(f"文件不存在: {file_path}")
                    continue
                
                # 获取文件名（不含扩展名）作为新的文件夹名
                file_name_without_ext = os.path.splitext(file_name)[0]
                
                # 获取当前文件夹路径和父文件夹路径
                current_folder = os.path.dirname(file_path)
                parent_folder = os.path.dirname(current_folder)
                current_folder_name = os.path.basename(current_folder)
                
                # 如果当前文件夹已经是以图片名命名的，则跳过
                if current_folder_name == file_name_without_ext:
                    continue
                
                # 构建新的文件夹路径
                new_folder_path = os.path.join(parent_folder, file_name_without_ext)
                
                # 检查新文件夹是否已存在
                if os.path.exists(new_folder_path) and current_folder.lower() != new_folder_path.lower():
                    errors.append(f"目标文件夹已存在: {new_folder_path}")
                    continue
                
                # 重命名文件夹
                shutil.move(current_folder, new_folder_path)
                
                # 更新数据中所有相关图片的路径
                for image_info in self.image_data:
                    if os.path.dirname(image_info["完整路径"]) == current_folder:
                        old_path = image_info["完整路径"]
                        file_basename = os.path.basename(old_path)
                        new_path = os.path.join(new_folder_path, file_basename)
                        image_info["完整路径"] = new_path
                
                renamed_count += 1
                
            except Exception as e:
                errors.append(f"重命名文件夹 {current_folder} 失败: {str(e)}")
        
        # 更新表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for image_info in self.image_data:
            self.tree.insert("", tk.END, values=(
                image_info["文件名"],
                image_info["完整路径"],
                image_info["经度"],
                image_info["纬度"],
                image_info["重命名"]
            ))
        
        # 显示结果
        if errors:
            error_message = "\n".join(errors[:10])
            if len(errors) > 10:
                error_message += f"\n...还有 {len(errors) - 10} 个错误未显示"
            
            messagebox.showwarning("警告", f"已成功重命名 {renamed_count} 个文件夹，但有 {len(errors)} 个错误:\n{error_message}")
        else:
            messagebox.showinfo("成功", f"已成功重命名 {renamed_count} 个文件夹")
        
        if self.update_status:
            self.update_status(f"已重命名 {renamed_count} 个文件夹")