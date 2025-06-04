# -*- coding: utf-8 -*-
"""重命名工具选项卡"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
from ...utils.file_operations import FileOperations
from .template_generator import TemplateGenerator

class RenameTab:
    """重命名功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.update_status = None  # 状态更新回调函数
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        # 使用说明文本
        instruction_text = "使用说明：通过导入Excel文件批量设置文件重命名规则，Excel文件需包含两列数据（原路径和新名称）。也可从文件路径工具中添加文件，完成设置后点击'执行重命名'按钮。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980,
                                  font=("微软雅黑", 10))
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 顶部按钮框架
        self.create_button_frame()
        
        # 创建表格
        self.create_rename_treeview()
        
    def create_button_frame(self):
        """创建按钮框架"""
        top_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 按钮样式
        button_style = self.theme.get_button_style()
        
        # 导入Excel按钮
        import_button = tk.Button(top_frame, text="导入Excel", command=self.import_excel,
                               bg=button_style["bg"], fg=button_style["fg"],
                               font=("微软雅黑", 9))
        import_button.pack(side=tk.LEFT, padx=5)
        
        # 导出Excel模版按钮
        export_template_button = tk.Button(top_frame, text="导出Excel模版", 
                                        command=TemplateGenerator.export_excel_template,
                                        bg=button_style["bg"], fg=button_style["fg"],
                                        font=("微软雅黑", 9))
        export_template_button.pack(side=tk.LEFT, padx=5)
        
        # 检测文件路径按钮
        check_path_button = tk.Button(top_frame, text="检测文件路径", command=self.check_file_paths,
                                   bg=button_style["bg"], fg=button_style["fg"],
                                   font=("微软雅黑", 9))
        check_path_button.pack(side=tk.LEFT, padx=5)
        
        # 导出当前数据按钮
        export_data_button = tk.Button(top_frame, text="导出当前数据", command=self.export_current_data,
                                    bg=button_style["bg"], fg=button_style["fg"],
                                    font=("微软雅黑", 9))
        export_data_button.pack(side=tk.LEFT, padx=5)
        
        # 执行重命名按钮
        self.rename_button = tk.Button(top_frame, text="执行重命名", command=self.execute_rename,
                                    bg=button_style["bg"], fg=button_style["fg"], 
                                    state=tk.DISABLED, font=("微软雅黑", 9))
        self.rename_button.pack(side=tk.LEFT, padx=5)
        
    def create_rename_treeview(self):
        """创建重命名表格"""
        # 表格框架
        tree_frame = tk.Frame(self.parent_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建滚动条
        scrollbar_y = tk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview
        self.rename_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar_y.set,
                                     xscrollcommand=scrollbar_x.set)
        self.rename_tree.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        scrollbar_y.config(command=self.rename_tree.yview)
        scrollbar_x.config(command=self.rename_tree.xview)
        
        # 定义列
        self.rename_tree["columns"] = ("original_path", "new_name", "path_exists")
        self.rename_tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.rename_tree.column("original_path", width=350, minwidth=200)
        self.rename_tree.column("new_name", width=350, minwidth=200)
        self.rename_tree.column("path_exists", width=150, minwidth=100)
        
        # 设置列标题
        self.rename_tree.heading("#0", text="序号")
        self.rename_tree.heading("original_path", text="原路径")
        self.rename_tree.heading("new_name", text="新名称")
        self.rename_tree.heading("path_exists", text="路径文件是否存在")
        
    def add_item_to_rename_list(self, path):
        """添加项目到重命名列表"""
        # 获取当前重命名列表中的项目数
        count = len(self.rename_tree.get_children()) + 1
        
        # 添加到重命名列表
        self.rename_tree.insert("", "end", text=str(count),
                            values=(path, os.path.basename(path), ""))
        
        # 启用重命名按钮
        if len(self.rename_tree.get_children()) > 0:
            self.rename_button.config(state=tk.NORMAL)
            
        if self.update_status:
            self.update_status(f"已添加文件到重命名列表: {os.path.basename(path)}")
        
    def import_excel(self):
        """导入Excel文件"""
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )
        
        if not file_path:
            return
            
        try:
            df = pd.read_excel(file_path)
            
            if len(df.columns) < 2:
                messagebox.showwarning("格式错误", "Excel文件格式不正确，请确保包含至少两列数据")
                return
                
            # 清空现有项目
            for item in self.rename_tree.get_children():
                self.rename_tree.delete(item)
                
            # 添加数据到表格
            for index, row in df.iterrows():
                original_path = str(row[0])
                new_name = str(row[1])
                
                self.rename_tree.insert("", "end", text=str(index + 1),
                                    values=(original_path, new_name, ""))
                
            # 启用重命名按钮
            if len(self.rename_tree.get_children()) > 0:
                self.rename_button.config(state=tk.NORMAL)
                
            if self.update_status:
                self.update_status(f"已导入Excel文件，共{len(df)}条记录")
                
        except Exception as e:
            messagebox.showerror("错误", f"导入Excel时出错: {str(e)}")
            if self.update_status:
                self.update_status("导入Excel文件失败")
    
    def execute_rename(self):
        """执行重命名操作"""
        if not self.rename_tree.get_children():
            messagebox.showwarning("警告", "重命名列表为空！")
            return
            
        if not messagebox.askyesno("确认", "是否确认执行重命名操作？"):
            return
            
        success_count = 0
        error_count = 0
        error_messages = []
        
        for item in self.rename_tree.get_children():
            values = self.rename_tree.item(item)["values"]
            original_path = values[0]
            new_name = values[1]
            
            success, error_msg = FileOperations.rename_file(original_path, new_name)
            if success:
                success_count += 1
            else:
                error_count += 1
                error_messages.append(error_msg)
                
        # 显示结果
        result_message = f"重命名完成！\n成功: {success_count}\n失败: {error_count}"
        if error_messages:
            result_message += "\n\n错误详情:\n" + "\n".join(error_messages)
            
        messagebox.showinfo("重命名结果", result_message)
        
        if self.update_status:
            self.update_status(f"重命名完成 - 成功: {success_count}, 失败: {error_count}")
        
    def check_file_paths(self):
        """检测文件路径是否存在"""
        if not self.rename_tree.get_children():
            messagebox.showwarning("警告", "重命名列表为空！")
            return
            
        checked_count = 0
        exists_count = 0
        
        for item in self.rename_tree.get_children():
            values = list(self.rename_tree.item(item)["values"])
            original_path = values[0]
            
            # 检查文件是否存在
            if os.path.exists(original_path):
                values[2] = "存在"
                exists_count += 1
            else:
                values[2] = "不存在"
                
            # 更新表格中的数据
            self.rename_tree.item(item, values=values)
            checked_count += 1
            
        messagebox.showinfo("检测结果", f"路径检测完成！\n总计检测: {checked_count}\n文件存在: {exists_count}\n文件不存在: {checked_count - exists_count}")
        
        if self.update_status:
            self.update_status(f"路径检测完成 - 存在: {exists_count}, 不存在: {checked_count - exists_count}")
         
    def export_current_data(self):
        """导出当前面板显示的数据"""
        if not self.rename_tree.get_children():
            messagebox.showwarning("警告", "当前没有数据可导出！")
            return
            
        # 选择保存文件的位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择导出文件保存位置"
        )
        
        if not file_path:
            return
            
        try:
            # 收集当前表格中的所有数据
            export_data = {
                '原路径': [],
                '新名称': [],
                '路径文件是否存在': []
            }
            
            for item in self.rename_tree.get_children():
                values = self.rename_tree.item(item)["values"]
                export_data['原路径'].append(values[0])
                export_data['新名称'].append(values[1])
                export_data['路径文件是否存在'].append(values[2] if len(values) > 2 else '')
                
            # 创建DataFrame并导出到Excel
            df = pd.DataFrame(export_data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            messagebox.showinfo("成功", f"数据已成功导出到：{file_path}\n\n导出记录数：{len(df)}")
            
            if self.update_status:
                self.update_status(f"数据已导出到: {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出数据时出错: {str(e)}")
            if self.update_status:
                self.update_status("导出数据失败")