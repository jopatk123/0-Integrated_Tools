# -*- coding: utf-8 -*-
"""文件整理工具核心功能模块"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import threading

class OrganizerTab:
    """文件整理选项卡"""
    
    def __init__(self, parent, notebook, theme, config):
        self.parent = parent
        self.notebook = notebook
        self.theme = theme
        self.config = config
        self.update_status = None  # 状态更新回调函数
        
        # 初始化变量
        self.files_list = []
        
        # 创建选项卡
        self.tab_frame = ttk.Frame(notebook)
        notebook.add(self.tab_frame, text="📁 文件整理")
        
        # 创建界面
        self.setup_ui()
    
    def setup_ui(self):
        """设置界面"""
        # 主框架
        main_frame = tk.Frame(self.tab_frame, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 使用说明
        self.create_instruction_frame(main_frame)
        
        # 操作按钮
        self.create_button_frame(main_frame)
        
        # 文件列表
        self.create_file_list_frame(main_frame)
    
    def create_instruction_frame(self, parent):
        """创建使用说明框架"""
        instruction_frame = tk.LabelFrame(parent, text="📋 使用说明", 
                                        bg=self.theme.bg_color, fg=self.theme.text_color,
                                        font=("微软雅黑", 10, "bold"))
        instruction_frame.pack(fill=tk.X, pady=(0, 10))
        
        instruction_text = (
            "• 添加需要整理的文件或文件夹\n"
            "• 点击'执行整理'将自动为每个文件创建与文件名同名的文件夹\n"
            "• 文件将被移动到对应的文件夹中\n"
            "• 可通过'删除选中'按钮移除不需要整理的文件"
        )
        
        instruction_label = tk.Label(instruction_frame, text=instruction_text,
                                   bg=self.theme.bg_color, fg=self.theme.text_color,
                                   font=("微软雅黑", 9), justify=tk.LEFT)
        instruction_label.pack(fill=tk.X, padx=10, pady=5)
    
    def create_button_frame(self, parent):
        """创建按钮框架"""
        button_frame = tk.Frame(parent, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 左侧按钮组
        left_frame = tk.Frame(button_frame, bg=self.theme.bg_color)
        left_frame.pack(side=tk.LEFT)
        
        # 添加文件夹按钮
        add_folder_btn = tk.Button(left_frame, text="📁 添加文件夹", 
                                 command=self.add_folder,
                                 bg=self.theme.button_color, fg="white",
                                 font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        add_folder_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 添加文件按钮
        add_file_btn = tk.Button(left_frame, text="📄 添加文件", 
                               command=self.add_files,
                               bg=self.theme.button_color, fg="white",
                               font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        add_file_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除选中按钮
        remove_btn = tk.Button(left_frame, text="🗑️ 删除选中", 
                             command=self.remove_selected,
                             bg=self.theme.caution_color, fg="white",
                             font=("微软雅黑", 9), relief=tk.RAISED, bd=2)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 右侧按钮组
        right_frame = tk.Frame(button_frame, bg=self.theme.bg_color)
        right_frame.pack(side=tk.RIGHT)
        
        # 执行整理按钮
        organize_btn = tk.Button(right_frame, text="🚀 执行整理", 
                               command=self.organize_files,
                               bg=self.theme.accent_color, fg="white",
                               font=("微软雅黑", 10, "bold"), relief=tk.RAISED, bd=2)
        organize_btn.pack(side=tk.RIGHT)
    
    def create_file_list_frame(self, parent):
        """创建文件列表框架"""
        list_frame = tk.LabelFrame(parent, text="📋 文件列表", 
                                 bg=self.theme.bg_color, fg=self.theme.text_color,
                                 font=("微软雅黑", 10, "bold"))
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Treeview和滚动条
        tree_container = tk.Frame(list_frame, bg=self.theme.bg_color)
        tree_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 创建Treeview
        self.file_tree = ttk.Treeview(tree_container, 
                                    yscrollcommand=v_scrollbar.set,
                                    xscrollcommand=h_scrollbar.set)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # 配置滚动条
        v_scrollbar.config(command=self.file_tree.yview)
        h_scrollbar.config(command=self.file_tree.xview)
        
        # 定义列
        self.file_tree["columns"] = ("name", "path", "size")
        self.file_tree.column("#0", width=60, minwidth=60, stretch=tk.NO)
        self.file_tree.column("name", width=200, minwidth=150)
        self.file_tree.column("path", width=400, minwidth=200)
        self.file_tree.column("size", width=100, minwidth=80)
        
        # 设置列标题
        self.file_tree.heading("#0", text="序号")
        self.file_tree.heading("name", text="文件名")
        self.file_tree.heading("path", text="路径")
        self.file_tree.heading("size", text="大小")
    
    def add_folder(self):
        """添加文件夹"""
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
                
                if self.update_status:
                    self.update_status(f"已添加文件夹中的 {count} 个文件")
            except Exception as e:
                messagebox.showerror("错误", f"添加文件夹时出错: {str(e)}")
    
    def add_files(self):
        """添加文件"""
        file_paths = filedialog.askopenfilenames(title="选择文件")
        if file_paths:
            count = 0
            for file_path in file_paths:
                if file_path not in [f["path"] for f in self.files_list]:
                    self.add_file_to_list(file_path)
                    count += 1
            
            if self.update_status:
                self.update_status(f"已添加 {count} 个文件")
    
    def add_file_to_list(self, file_path):
        """添加文件到列表"""
        file_name = os.path.basename(file_path)
        
        # 获取文件大小
        try:
            file_size = os.path.getsize(file_path)
            size_str = self.format_file_size(file_size)
        except:
            size_str = "未知"
        
        self.files_list.append({"name": file_name, "path": file_path, "size": size_str})
        
        # 获取当前列表中的项目数
        count = len(self.file_tree.get_children()) + 1
        
        # 添加到树视图
        self.file_tree.insert("", tk.END, text=str(count), 
                             values=(file_name, file_path, size_str))
    
    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def remove_selected(self):
        """删除选中的文件"""
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
        
        if self.update_status:
            self.update_status(f"已从列表中移除 {len(selected_items)} 个文件")
    
    def renumber_items(self):
        """重新为列表项编号"""
        items = self.file_tree.get_children()
        for i, item in enumerate(items, 1):
            self.file_tree.item(item, text=str(i))
    
    def organize_files(self):
        """整理文件"""
        if not self.files_list:
            messagebox.showinfo("提示", "请先添加文件")
            return
        
        if not messagebox.askyesno("确认", "确定要将文件整理到与文件名同名的文件夹中吗？"):
            return
        
        if self.update_status:
            self.update_status("正在整理文件...")
        
        # 在后台线程中执行整理操作
        threading.Thread(target=self._organize_files_thread, daemon=True).start()
    
    def _organize_files_thread(self):
        """在后台线程中整理文件"""
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
                
                # 更新状态
                if self.update_status:
                    self.parent.after(0, lambda: self.update_status(
                        f"正在整理文件... ({success_count}/{success_count + error_count + len(self.files_list)})"))
                
            except Exception as e:
                error_count += 1
                error_messages.append(f"处理文件 {file_name} 时出错: {str(e)}")
        
        # 在主线程中更新界面
        self.parent.after(0, lambda: self._organize_complete(success_count, error_count, error_messages))
    
    def _organize_complete(self, success_count, error_count, error_messages):
        """整理完成后的处理"""
        # 更新界面
        self.refresh_file_list()
        
        # 显示结果
        result_message = f"整理完成！\n成功: {success_count}\n失败: {error_count}"
        if error_messages:
            result_message += "\n\n错误详情:\n" + "\n".join(error_messages[:5])  # 只显示前5个错误
            if len(error_messages) > 5:
                result_message += f"\n... 还有 {len(error_messages) - 5} 个错误"
        
        messagebox.showinfo("整理结果", result_message)
        
        if self.update_status:
            self.update_status(f"整理完成: 成功 {success_count} 个，失败 {error_count} 个")
    
    def refresh_file_list(self):
        """刷新文件列表"""
        # 清空树视图
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # 重新添加文件
        for i, file_info in enumerate(self.files_list, 1):
            self.file_tree.insert("", tk.END, text=str(i), 
                                 values=(file_info["name"], file_info["path"], file_info["size"]))