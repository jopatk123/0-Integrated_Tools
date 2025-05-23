import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil

class FileOrganizerTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        # 初始化变量
        self.files_list = []
        
        # 创建界面组件
        self.create_top_frame()
        self.create_file_list_treeview()
        
    def create_top_frame(self):
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        # 使用说明文本
        instruction_text = "使用说明：添加需要整理的文件或文件夹，点击'执行整理'将自动为每个文件创建与文件名同名的文件夹，并将文件移动到对应文件夹中。可通过'删除选中'按钮移除不需要整理的文件。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980)
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 顶部框架
        top_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 添加按钮
        button_style = self.theme.get_button_style()
        
        # 添加文件夹按钮
        add_folder_btn = tk.Button(top_frame, text="添加文件夹", command=self.add_folder,
                               bg=button_style["bg"], fg=button_style["fg"])
        add_folder_btn.pack(side=tk.LEFT, padx=5)
        
        # 添加文件按钮
        add_file_btn = tk.Button(top_frame, text="添加文件", command=self.add_files,
                              bg=button_style["bg"], fg=button_style["fg"])
        add_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除选中按钮
        caution_style = self.theme.get_button_style("caution")
        remove_btn = tk.Button(top_frame, text="删除选中", command=self.remove_selected,
                            bg=caution_style["bg"], fg=caution_style["fg"])
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 执行整理按钮
        organize_btn = tk.Button(top_frame, text="执行整理", command=self.organize_files,
                              bg=button_style["bg"], fg=button_style["fg"])
        organize_btn.pack(side=tk.RIGHT, padx=5)
        
        # 状态栏
        status_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        status_bar = tk.Label(status_frame, textvariable=self.status_var, 
                           relief=tk.SUNKEN, anchor=tk.W, bg=self.theme.bg_color)
        status_bar.pack(fill=tk.X)
        
    def create_file_list_treeview(self):
        # 表格框架
        tree_frame = tk.Frame(self.parent_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 创建滚动条
        scrollbar_y = tk.Scrollbar(tree_frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview
        self.file_tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar_y.set,
                                   xscrollcommand=scrollbar_x.set)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        scrollbar_y.config(command=self.file_tree.yview)
        scrollbar_x.config(command=self.file_tree.xview)
        
        # 定义列
        self.file_tree["columns"] = ("name", "path")
        self.file_tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.file_tree.column("name", width=200, minwidth=100)
        self.file_tree.column("path", width=400, minwidth=200)
        
        # 设置列标题
        self.file_tree.heading("#0", text="序号")
        self.file_tree.heading("name", text="文件名")
        self.file_tree.heading("path", text="路径")
        
    def add_folder(self):
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            try:
                count = 0
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path) and file_path not in [f["path"] for f in self.files_list]:
                            self.add_file_to_list(file_path)
                            count += 1
                
                self.status_var.set(f"已添加文件夹中的 {count} 个文件")
            except Exception as e:
                messagebox.showerror("错误", f"添加文件夹时出错: {str(e)}")
    
    def add_files(self):
        file_paths = filedialog.askopenfilenames(title="选择文件")
        if file_paths:
            count = 0
            for file_path in file_paths:
                if file_path not in [f["path"] for f in self.files_list]:
                    self.add_file_to_list(file_path)
                    count += 1
            
            self.status_var.set(f"已添加 {count} 个文件")
    
    def add_file_to_list(self, file_path):
        file_name = os.path.basename(file_path)
        self.files_list.append({"name": file_name, "path": file_path})
        
        # 获取当前列表中的项目数
        count = len(self.file_tree.get_children()) + 1
        
        # 添加到列表
        self.file_tree.insert("", tk.END, text=str(count), values=(file_name, file_path))
    
    def remove_selected(self):
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的文件")
            return
        
        for item in selected_items:
            values = self.file_tree.item(item, "values")
            file_path = values[1]
            # 从列表中移除
            self.files_list = [f for f in self.files_list if f["path"] != file_path]
            # 从树视图中移除
            self.file_tree.delete(item)
        
        # 重新编号
        self.renumber_items()
        
        self.status_var.set(f"已从列表中移除 {len(selected_items)} 个文件")
    
    def renumber_items(self):
        """重新为列表项编号"""
        items = self.file_tree.get_children()
        for i, item in enumerate(items, 1):
            self.file_tree.item(item, text=str(i))
    
    def organize_files(self):
        if not self.files_list:
            messagebox.showinfo("提示", "请先添加文件")
            return
        
        if not messagebox.askyesno("确认", "确定要将文件整理到与文件名同名的文件夹中吗？"):
            return
        
        success_count = 0
        error_count = 0
        error_messages = []
        
        for file_info in self.files_list.copy():
            file_path = file_info["path"]
            file_name = file_info["name"]
            file_name_without_ext = os.path.splitext(file_name)[0]
            
            # 获取文件所在目录
            parent_dir = os.path.dirname(file_path)
            
            # 创建与文件名同名的文件夹
            folder_path = os.path.join(parent_dir, file_name_without_ext)
            
            try:
                # 如果文件夹不存在，则创建
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # 移动文件到文件夹
                dest_path = os.path.join(folder_path, file_name)
                shutil.move(file_path, dest_path)
                
                # 从列表中移除已处理的文件
                self.files_list.remove(file_info)
                success_count += 1
            except Exception as e:
                error_count += 1
                error_messages.append(f"处理文件 {file_name} 时出错: {str(e)}")
        
        # 更新界面
        self.refresh_file_list()
        
        # 显示结果
        result_message = f"整理完成！\n成功: {success_count}\n失败: {error_count}"
        if error_messages:
            result_message += "\n\n错误详情:\n" + "\n".join(error_messages)
            
        messagebox.showinfo("整理结果", result_message)
        
        self.status_var.set(f"整理完成: 成功 {success_count} 个，失败 {error_count} 个")
    
    def refresh_file_list(self):
        # 清空树视图
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # 重新添加文件
        for i, file_info in enumerate(self.files_list, 1):
            self.file_tree.insert("", tk.END, text=str(i), 
                               values=(file_info["name"], file_info["path"]))