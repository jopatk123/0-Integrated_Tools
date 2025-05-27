# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from ...utils import amap_api

class ApiKeyDialog:
    """API密钥配置对话框"""
    
    def __init__(self, parent, config):
        self.parent = parent
        self.config = config
        
    def show(self):
        """显示API密钥配置对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("配置高德地图API密钥")
        dialog.geometry("500x300")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 居中显示
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # 说明文本
        info_text = """为了使用高德地图的完整功能，请配置您的API密钥：

1. 访问高德开放平台：https://lbs.amap.com/
2. 注册账号并创建应用
3. 获取Web服务API密钥
4. 在下方输入您的API密钥

注意：个人开发者每日有免费调用额度
必须配置API密钥才能使用本工具的功能"""
        
        info_label = tk.Label(dialog, text=info_text, justify=tk.LEFT, wraplength=450)
        info_label.pack(pady=10, padx=10)
        
        # API密钥输入
        key_frame = tk.Frame(dialog)
        key_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(key_frame, text="API密钥:").pack(anchor=tk.W)
        key_entry = tk.Entry(key_frame, width=50, show="*")
        key_entry.pack(fill=tk.X, pady=5)
        
        # 按钮
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def save_key():
            api_key = key_entry.get().strip()
            if api_key:
                self.config.set_amap_api_key(api_key)
                amap_api.set_api_key(api_key)
                messagebox.showinfo("成功", "API密钥已保存")
                dialog.destroy()
            else:
                messagebox.showerror("错误", "请输入有效的API密钥")
        
        def cancel():
            dialog.destroy()
            # 如果没有API密钥，关闭整个工具
            if not self.config.get_amap_api_key():
                messagebox.showwarning("警告", "未配置API密钥，无法使用高德地图功能")
                self.parent.quit()
        
        tk.Button(button_frame, text="保存", command=save_key).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", command=cancel).pack(side=tk.LEFT, padx=5)
        
        key_entry.focus()