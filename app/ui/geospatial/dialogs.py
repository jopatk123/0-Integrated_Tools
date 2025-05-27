# -*- coding: utf-8 -*-
"""地理空间工具对话框模块"""

import tkinter as tk
from tkinter import ttk, messagebox

class ConfigDialog:
    """配置对话框"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.result = False
        
    def show(self):
        """显示配置对话框"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("地理空间工具配置")
        self.dialog.geometry("600x500")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        self.setup_ui()
        
        # 等待对话框关闭
        self.dialog.wait_window()
        return self.result
    
    def setup_ui(self):
        """设置对话框界面"""
        # 主框架
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # API Key配置
        api_frame = ttk.LabelFrame(main_frame, text="高德地图API配置")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.api_key_var = tk.StringVar(value=self.config.get_amap_api_key() or "")
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # 显示/隐藏API Key按钮
        self.show_api_key = tk.BooleanVar()
        show_button = ttk.Checkbutton(api_frame, text="显示", variable=self.show_api_key, 
                                     command=lambda: api_key_entry.config(show="" if self.show_api_key.get() else "*"))
        show_button.grid(row=0, column=2, padx=5, pady=5)
        
        # API Key说明
        info_text = (
            "请在高德开放平台申请Web服务API Key:\n"
            "1. 访问 https://lbs.amap.com/dev/key/app\n"
            "2. 注册并创建应用\n"
            "3. 选择'Web服务'平台\n"
            "4. 复制API Key到上方输入框"
        )
        info_label = ttk.Label(api_frame, text=info_text, justify=tk.LEFT, foreground="gray")
        info_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="w")
        
        api_frame.grid_columnconfigure(1, weight=1)
        
        # 收藏位置管理
        favorites_frame = ttk.LabelFrame(main_frame, text="收藏位置管理")
        favorites_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 收藏位置列表
        list_frame = ttk.Frame(favorites_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ("name", "lng", "lat")
        self.favorites_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        self.favorites_tree.heading("name", text="名称")
        self.favorites_tree.heading("lng", text="经度")
        self.favorites_tree.heading("lat", text="纬度")
        
        self.favorites_tree.column("name", width=200)
        self.favorites_tree.column("lng", width=120)
        self.favorites_tree.column("lat", width=120)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.favorites_tree.yview)
        self.favorites_tree.configure(yscrollcommand=scrollbar.set)
        
        self.favorites_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加收藏位置
        add_frame = ttk.Frame(favorites_frame)
        add_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(add_frame, text="名称:").grid(row=0, column=0, padx=5)
        self.name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.name_var, width=15).grid(row=0, column=1, padx=5)
        
        ttk.Label(add_frame, text="经度:").grid(row=0, column=2, padx=5)
        self.lng_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.lng_var, width=12).grid(row=0, column=3, padx=5)
        
        ttk.Label(add_frame, text="纬度:").grid(row=0, column=4, padx=5)
        self.lat_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.lat_var, width=12).grid(row=0, column=5, padx=5)
        
        ttk.Button(add_frame, text="添加", command=self.add_favorite).grid(row=0, column=6, padx=10)
        ttk.Button(add_frame, text="删除选中", command=self.delete_favorite).grid(row=0, column=7, padx=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="保存", command=self.save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel_config).pack(side=tk.RIGHT, padx=5)
        
        # 刷新收藏位置列表
        self.refresh_favorites_tree()
    
    def refresh_favorites_tree(self):
        """刷新收藏位置列表"""
        # 清空现有项目
        for item in self.favorites_tree.get_children():
            self.favorites_tree.delete(item)
        
        # 添加收藏位置
        favorites = self.config.get_favorite_locations()
        for fav in favorites:
            self.favorites_tree.insert("", "end", values=(fav['name'], fav['lng'], fav['lat']))
    
    def add_favorite(self):
        """添加收藏位置"""
        try:
            name = self.name_var.get().strip()
            lng = float(self.lng_var.get().strip())
            lat = float(self.lat_var.get().strip())
            
            if name and self.config.add_favorite_location(name, lng, lat):
                self.refresh_favorites_tree()
                self.name_var.set("")
                self.lng_var.set("")
                self.lat_var.set("")
                messagebox.showinfo("成功", f"已添加收藏位置: {name}")
            else:
                messagebox.showerror("错误", "请输入有效的名称和坐标")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字坐标")
    
    def delete_favorite(self):
        """删除选中的收藏位置"""
        selected = self.favorites_tree.selection()
        if selected:
            item = self.favorites_tree.item(selected[0])
            name = item['values'][0]
            if messagebox.askyesno("确认删除", f"确定要删除收藏位置 '{name}' 吗？"):
                if self.config.remove_favorite_location(name):
                    self.refresh_favorites_tree()
                    messagebox.showinfo("成功", f"已删除收藏位置: {name}")
        else:
            messagebox.showwarning("提示", "请先选择要删除的收藏位置")
    
    def save_config(self):
        """保存配置"""
        api_key = self.api_key_var.get().strip()
        if api_key and self.config.set_amap_api_key(api_key):
            self.result = True
            messagebox.showinfo("成功", "配置已保存")
            self.dialog.destroy()
        elif not api_key:
            messagebox.showerror("错误", "请输入API Key")
        else:
            messagebox.showerror("错误", "保存配置失败")
    
    def cancel_config(self):
        """取消配置"""
        self.dialog.destroy()

class FavoriteLocationDialog:
    """收藏位置选择对话框"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        self.selected_location = None
        
    def show(self):
        """显示收藏位置选择对话框"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("选择收藏位置")
        self.dialog.geometry("400x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 100,
            self.parent.winfo_rooty() + 100
        ))
        
        self.setup_ui()
        
        # 等待对话框关闭
        self.dialog.wait_window()
        return self.selected_location
    
    def setup_ui(self):
        """设置对话框界面"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 说明标签
        ttk.Label(main_frame, text="请选择一个收藏位置:").pack(pady=(0, 10))
        
        # 收藏位置列表
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("name", "lng", "lat")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("name", text="名称")
        self.tree.heading("lng", text="经度")
        self.tree.heading("lat", text="纬度")
        
        self.tree.column("name", width=150)
        self.tree.column("lng", width=100)
        self.tree.column("lat", width=100)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 双击选择
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="选择", command=self.select_location).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(side=tk.RIGHT, padx=5)
        
        # 加载收藏位置
        self.load_favorites()
    
    def load_favorites(self):
        """加载收藏位置"""
        favorites = self.config.get_favorite_locations()
        for fav in favorites:
            self.tree.insert("", "end", values=(fav['name'], fav['lng'], fav['lat']))
    
    def on_double_click(self, event):
        """双击选择"""
        self.select_location()
    
    def select_location(self):
        """选择位置"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item['values']
            self.selected_location = {
                'name': values[0],
                'lng': float(values[1]),
                'lat': float(values[2])
            }
            self.dialog.destroy()
        else:
            messagebox.showwarning("提示", "请选择一个位置")
    
    def cancel(self):
        """取消选择"""
        self.dialog.destroy()