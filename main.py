import tkinter as tk
from tkinter import messagebox
from app.integrated_tool import IntegratedTool
from app.utils.amap_api import amap_api

def check_api_availability():
    """检查高德API是否可用"""
    is_available, message = amap_api.test_connection()
    return is_available, message

if __name__ == "__main__":
    # 检查高德API可用性
    api_available, api_message = check_api_availability()
    
    if not api_available:
        # 创建一个临时的根窗口来显示消息框
        temp_root = tk.Tk()
        temp_root.withdraw()  # 隐藏临时窗口
        messagebox.showerror("启动错误", f"无法启动程序：高德地图API不可用\n\n详细信息: {api_message}\n\n请检查网络连接或API密钥配置。")
        temp_root.destroy()
    else:
        # API可用，正常启动程序
        root = tk.Tk()
        app = IntegratedTool(root)
        root.mainloop()
    