import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
from app.utils.file_operations import FileOperations

class RenameTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 创建界面组件
        self.create_top_frame()
        self.create_rename_treeview()
        
    def create_top_frame(self):
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        # 使用说明文本
        instruction_text = "使用说明：通过导入Excel文件批量设置文件重命名规则，Excel文件需包含两列数据（原路径和新名称）。也可从文件路径工具中添加文件，完成设置后点击'执行重命名'按钮。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980)
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 顶部框架
        top_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 导入Excel按钮
        button_style = self.theme.get_button_style()
        import_button = tk.Button(top_frame, text="导入Excel", command=self.import_excel,
                               bg=button_style["bg"], fg=button_style["fg"])
        import_button.pack(side=tk.LEFT, padx=5)
        
        # 导出Excel模版按钮
        export_template_button = tk.Button(top_frame, text="导出Excel模版", command=self.export_excel_template,
                                        bg=button_style["bg"], fg=button_style["fg"])
        export_template_button.pack(side=tk.LEFT, padx=5)
        
        # 执行重命名按钮
        self.rename_button = tk.Button(top_frame, text="执行重命名", command=self.execute_rename,
                                    bg=button_style["bg"], fg=button_style["fg"], state=tk.DISABLED)
        self.rename_button.pack(side=tk.LEFT, padx=5)
        
    def create_rename_treeview(self):
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
        self.rename_tree["columns"] = ("original_path", "new_name")
        self.rename_tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.rename_tree.column("original_path", width=400, minwidth=200)
        self.rename_tree.column("new_name", width=400, minwidth=200)
        
        # 设置列标题
        self.rename_tree.heading("#0", text="序号")
        self.rename_tree.heading("original_path", text="原路径")
        self.rename_tree.heading("new_name", text="新名称")
        
    def add_item_to_rename_list(self, path):
        """添加项目到重命名列表"""
        # 获取当前重命名列表中的项目数
        count = len(self.rename_tree.get_children()) + 1
        
        # 添加到重命名列表
        self.rename_tree.insert("", "end", text=str(count),
                            values=(path, os.path.basename(path)))
        
        # 启用重命名按钮
        self.rename_button.config(state=tk.NORMAL)
        
    def import_excel(self):
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
                                    values=(original_path, new_name))
                
            # 启用重命名按钮
            if len(self.rename_tree.get_children()) > 0:
                self.rename_button.config(state=tk.NORMAL)
                
        except Exception as e:
            messagebox.showerror("错误", f"导入Excel时出错: {str(e)}")
    
    def export_excel_template(self):
        """导出Excel重命名模版"""
        # 选择保存文件的位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择模版保存位置"
        )
        
        if not file_path:
            return
            
        try:
            # 创建示例数据
            template_data = {
                '原路径': [
                    'C:\\示例文件夹\\原文件名1.txt',
                    'C:\\示例文件夹\\原文件名2.jpg',
                    'C:\\示例文件夹\\原文件名3.pdf'
                ],
                '新名称': [
                    '新文件名1.txt',
                    '新文件名2.jpg', 
                    '新文件名3.pdf'
                ]
            }
            
            # 创建DataFrame并导出到Excel
            df = pd.DataFrame(template_data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            messagebox.showinfo("成功", f"Excel模版已导出到：{file_path}\n\n使用说明：\n1. 在'原路径'列填入要重命名的文件完整路径\n2. 在'新名称'列填入新的文件名（包含扩展名）\n3. 保存后通过'导入Excel'按钮导入")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出模版时出错: {str(e)}")
            
    def execute_rename(self):
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