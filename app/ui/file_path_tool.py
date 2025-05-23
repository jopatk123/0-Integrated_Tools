import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pyperclip
import threading
from app.utils.file_operations import FileOperations

class FilePathTool:
    def __init__(self, parent_frame, theme, notebook, rename_tool=None):
        self.parent_frame = parent_frame
        self.theme = theme
        self.notebook = notebook
        self.rename_tool = rename_tool
        
        # 初始化变量
        self.folder_path = tk.StringVar()
        self.filter_var = tk.StringVar()
        self.include_subfolders = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="就绪")
        
        # 排序相关变量
        self.sort_column = "path"  # 默认按路径排序
        self.sort_reverse = False  # 默认升序
        
        # 创建界面组件
        self.create_top_frame()
        self.create_filter_frame()
        self.create_file_path_treeview()
        self.create_status_bar()
        
    def create_top_frame(self):
        # 使用说明框架
        instruction_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=5)
        
        # 使用说明文本
        instruction_text = "使用说明：选择文件夹路径后，可以扫描文件或文件夹，支持文件过滤和子文件夹包含选项。扫描结果可复制路径、导出或添加到重命名工具。点击列标题可以按该列进行排序。"
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, justify=tk.LEFT, wraplength=980)
        instruction_label.pack(fill=tk.X, padx=5, pady=5)
        
        # 顶部框架
        top_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 文件夹路径输入框
        folder_label = tk.Label(top_frame, text="文件夹路径:", bg=self.theme.bg_color)
        folder_label.pack(side=tk.LEFT, padx=5)
        
        self.folder_entry = tk.Entry(top_frame, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 浏览按钮
        button_style = self.theme.get_button_style()
        browse_button = tk.Button(top_frame, text="浏览", command=self.browse_folder,
                               bg=button_style["bg"], fg=button_style["fg"])
        browse_button.pack(side=tk.LEFT, padx=5)

        # 导出按钮
        export_button = tk.Button(top_frame, text="导出路径", command=self.export_paths,
                               bg=button_style["bg"], fg=button_style["fg"])
        export_button.pack(side=tk.LEFT, padx=5)
        
    def create_filter_frame(self):
        # 过滤框架
        filter_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        filter_frame.pack(fill=tk.X, pady=5)
        
        # 文件过滤选项
        filter_label = tk.Label(filter_frame, text="文件过滤:", bg=self.theme.bg_color)
        filter_label.pack(side=tk.LEFT, padx=5)
        
        self.filter_entry = tk.Entry(filter_frame, textvariable=self.filter_var, width=20)
        self.filter_entry.pack(side=tk.LEFT, padx=5)
        self.filter_entry.insert(0, "*.*")
        
        # 包含子文件夹选项
        subfolder_check = tk.Checkbutton(filter_frame, text="包含子文件夹",
                                      variable=self.include_subfolders, bg=self.theme.bg_color)
        subfolder_check.pack(side=tk.LEFT, padx=10)
        
        # 扫描按钮
        button_style = self.theme.get_button_style()
        scan_button = tk.Button(filter_frame, text="扫描文件", command=self.scan_files,
                             bg=button_style["bg"], fg=button_style["fg"])
        scan_button.pack(side=tk.LEFT, padx=5)
        
        # 扫描文件夹按钮
        scan_folders_button = tk.Button(filter_frame, text="扫描文件夹", command=self.scan_folders,
                                    bg=button_style["bg"], fg=button_style["fg"])
        scan_folders_button.pack(side=tk.LEFT, padx=5)
        
        # 删除按钮（初始隐藏）
        warning_style = self.theme.get_button_style("warning")
        self.delete_button = tk.Button(filter_frame, text="删除", command=self.delete_items,
                                    bg=warning_style["bg"], fg=warning_style["fg"])
        
        # 删除到回收站按钮（初始隐藏）
        self.recycle_button = tk.Button(filter_frame, text="删除(回收站)", command=self.delete_to_recycle_bin,
                                    bg=warning_style["bg"], fg=warning_style["fg"])
        
        # 移除按钮（初始隐藏）
        caution_style = self.theme.get_button_style("caution")
        self.remove_button = tk.Button(filter_frame, text="移除", command=self.remove_items,
                                    bg=caution_style["bg"], fg=caution_style["fg"])
        
    def create_file_path_treeview(self):
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
        self.file_tree["columns"] = ("path", "size", "modified")
        self.file_tree.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.file_tree.column("path", width=400, minwidth=200)
        self.file_tree.column("size", width=100, minwidth=100)
        self.file_tree.column("modified", width=150, minwidth=150)
        
        # 设置列标题
        self.file_tree.heading("#0", text="序号")
        self.file_tree.heading("path", text="路径", command=lambda: self.sort_treeview("path"))
        self.file_tree.heading("size", text="大小", command=lambda: self.sort_treeview("size"))
        self.file_tree.heading("modified", text="修改时间", command=lambda: self.sort_treeview("modified"))
        
        # 添加右键菜单
        self.create_file_path_context_menu()
        
    def create_file_path_context_menu(self):
        self.file_path_menu = tk.Menu(self.parent_frame, tearoff=0)
        self.file_path_menu.add_command(label="复制路径", command=self.copy_path)
        self.file_path_menu.add_command(label="添加到重命名列表", command=self.add_to_rename_list)
        self.file_tree.bind("<Button-3>", self.show_file_path_menu)
        
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)
            
    def scan_files(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showwarning("警告", "请先选择文件夹！")
            return
            
        # 清空现有项目
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        # 获取过滤模式
        filter_pattern = self.filter_var.get()
        if not filter_pattern:
            filter_pattern = "*.*"
            
        self.status_var.set("正在扫描文件...")
        # 使用FileOperations扫描文件
        try:
            files = FileOperations.scan_files(
                folder_path, 
                filter_pattern, 
                self.include_subfolders.get()
            )
            
            # 添加到列表
            count = 0
            for file_info in files:
                count += 1
                self.file_tree.insert("", "end", text=str(count),
                                  values=(file_info["path"], 
                                         file_info["size"],
                                         file_info["modified"]))
                            
            if count == 0:
                self.status_var.set(f"未找到匹配的文件（过滤条件：{filter_pattern}）")
                messagebox.showinfo("提示", f"未找到匹配的文件（过滤条件：{filter_pattern}）")
            else:
                self.status_var.set(f"扫描完成，共找到 {count} 个文件")
            
            # 根据扫描结果显示或隐藏操作按钮
            self.show_action_buttons()
            
        except Exception as e:
            self.status_var.set(f"扫描文件时出错: {str(e)}")
            messagebox.showerror("错误", f"扫描文件时出错: {str(e)}")
            
    def scan_folders(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showwarning("警告", "请先选择文件夹！")
            return
            
        # 清空现有项目
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
            
        self.status_var.set("正在扫描文件夹...")
        # 使用FileOperations扫描文件夹
        folders = FileOperations.scan_folders(
            folder_path, 
            self.include_subfolders.get()
        )
        
        # 添加到列表
        count = 0
        for folder_info in folders:
            count += 1
            self.file_tree.insert("", "end", text=str(count),
                              values=(folder_info["path"], 
                                     folder_info["size"],
                                     folder_info["modified"]))
        
        if count == 0:
            self.status_var.set("未找到文件夹")
        else:
            self.status_var.set(f"扫描完成，共找到 {count} 个文件夹")
                                  
        # 根据扫描结果显示或隐藏操作按钮
        self.show_action_buttons()
        
    def show_file_path_menu(self, event):
        item = self.file_tree.selection()
        if item:
            self.file_path_menu.post(event.x_root, event.y_root)
            
    def copy_path(self):
        item = self.file_tree.selection()
        if item:
            path = self.file_tree.item(item[0])["values"][0]
            pyperclip.copy(path)
            
    def add_to_rename_list(self):
        selected_items = self.file_tree.selection()
        if not selected_items or not self.rename_tool:
            return
            
        # 切换到重命名选项卡
        self.notebook.select(1)
        
        # 添加选中的项目到重命名列表
        for item in selected_items:
            path = self.file_tree.item(item)["values"][0]
            self.rename_tool.add_item_to_rename_list(path)
        
    def export_paths(self):
        if not self.file_tree.get_children():
            messagebox.showwarning("警告", "没有可导出的路径！")
            return
            
        # 选择保存文件的位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            title="选择导出位置"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for item in self.file_tree.get_children():
                    values = self.file_tree.item(item)["values"]
                    path = values[0]  # 获取路径
                    size = values[1]  # 获取大小
                    modified = values[2]  # 获取修改时间
                    f.write(f"{path}\t{size}\t{modified}\n")
                    
            messagebox.showinfo("成功", f"路径已导出到：{file_path}")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出路径时出错: {str(e)}")
            
    def show_action_buttons(self):
        """显示操作按钮"""
        if self.file_tree.get_children():  # 如果列表中有项目
            self.delete_button.pack(side=tk.LEFT, padx=5)
            self.recycle_button.pack(side=tk.LEFT, padx=5)
            self.remove_button.pack(side=tk.LEFT, padx=5)
        else:
            self.delete_button.pack_forget()
            self.recycle_button.pack_forget()
            self.remove_button.pack_forget()
            
    def delete_items(self):
        """删除选中的文件或文件夹"""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的项目！")
            return
            
        # 确认删除
        count = len(selected_items)
        if not messagebox.askyesno("确认删除", 
                                f"确定要删除选中的 {count} 个项目吗？\n此操作不可恢复！"):
            return
            
        success_count = 0
        error_messages = []
        
        for item in selected_items:
            path = self.file_tree.item(item)["values"][0]
            if FileOperations.delete_item(path):
                success_count += 1
                self.file_tree.delete(item)
            else:
                error_messages.append(f"删除失败 {path}")
                
        # 显示结果
        if error_messages:
            messagebox.showerror("错误", "\n".join(error_messages))
        else:
            messagebox.showinfo("成功", f"成功删除 {success_count} 个项目")
            
        # 检查是否需要隐藏操作按钮
        self.show_action_buttons()
            
    def remove_items(self):
        """从列表中移除选中的项目（不删除实际文件）"""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要移除的项目！")
            return
            
        # 直接从列表中移除
        for item in selected_items:
            self.file_tree.delete(item)
            
        # 检查是否需要隐藏操作按钮
        self.show_action_buttons()
        
    def sort_treeview(self, column):
        """按指定列排序Treeview"""
        # 获取所有项目
        items = [(self.file_tree.item(item)["values"], item) for item in self.file_tree.get_children('')]
        
        # 如果点击的是当前排序列，则反转排序顺序
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        
        # 根据列类型进行排序
        if column == "size":
            # 对大小进行排序（需要将KB转换为数字）
            items.sort(key=lambda x: float(x[0][1].split()[0]) if x[0][1] and " " in x[0][1] else 0, reverse=self.sort_reverse)
        elif column == "modified":
            # 对修改时间进行排序
            items.sort(key=lambda x: x[0][2] if x[0][2] else "", reverse=self.sort_reverse)
        else:
            # 对路径进行排序
            items.sort(key=lambda x: x[0][0] if x[0][0] else "", reverse=self.sort_reverse)
        
        # 重新排列项目
        for index, (values, item) in enumerate(items):
            self.file_tree.move(item, '', index)
            # 更新序号
            self.file_tree.item(item, text=str(index+1))
        
        # 更新列标题显示排序方向
        for col in ("path", "size", "modified"):
            if col == column:
                direction = "▼" if self.sort_reverse else "▲"
                self.file_tree.heading(col, text=f"{self.get_column_title(col)} {direction}", 
                                    command=lambda c=col: self.sort_treeview(c))
            else:
                self.file_tree.heading(col, text=self.get_column_title(col), 
                                    command=lambda c=col: self.sort_treeview(c))
    
    def get_column_title(self, column):
        """获取列的原始标题"""
        if column == "path":
            return "路径"
        elif column == "size":
            return "大小"
        elif column == "modified":
            return "修改时间"
        return ""
        
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = ttk.Label(self.parent_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def delete_to_recycle_bin(self):
        """删除选中的文件或文件夹到回收站"""
        selected_items = self.file_tree.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的项目！")
            return
            
        # 确认删除
        count = len(selected_items)
        if not messagebox.askyesno("确认删除到回收站", 
                                f"确定要将选中的 {count} 个项目移动到回收站吗？"):
            return
            
        # 检查是否安装了send2trash模块
        try:
            import send2trash
        except ImportError:
            result = messagebox.askyesno("模块缺失", 
                                      "需要安装send2trash模块才能使用此功能。\n是否立即安装？")
            if result:
                self.status_var.set("正在安装send2trash模块...")
                threading.Thread(target=self._install_send2trash, daemon=True).start()
            return
            
        success_count = 0
        error_messages = []
        
        for item in selected_items:
            path = self.file_tree.item(item)["values"][0]
            if FileOperations.delete_to_recycle_bin(path):
                success_count += 1
                self.file_tree.delete(item)
            else:
                error_messages.append(f"删除失败 {path}")
                
        # 显示结果
        if error_messages:
            self.status_var.set(f"删除到回收站出错: {len(error_messages)} 个项目失败")
            messagebox.showerror("错误", "\n".join(error_messages))
        else:
            self.status_var.set(f"成功将 {success_count} 个项目移动到回收站")
            messagebox.showinfo("成功", f"成功将 {success_count} 个项目移动到回收站")
            
        # 检查是否需要隐藏操作按钮
        self.show_action_buttons()
        
    def _install_send2trash(self):
        """安装send2trash模块"""
        import subprocess
        try:
            subprocess.check_call(["pip", "install", "send2trash"])
            self.parent_frame.after(0, lambda: self.status_var.set("send2trash模块安装成功，请重试删除操作"))
            messagebox.showinfo("安装成功", "send2trash模块安装成功，请重试删除操作")
        except Exception as e:
            self.parent_frame.after(0, lambda: self.status_var.set(f"安装send2trash模块失败: {e}"))
            messagebox.showerror("安装失败", f"安装send2trash模块失败: {e}\n请手动运行: pip install send2trash")