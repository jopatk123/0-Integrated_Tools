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
        print(f"警告：高德地图API不可用 - {api_message}")
        print("程序将继续启动，但地理空间相关功能可能受限。")
    
    # 无论API是否可用都启动程序
    root = tk.Tk()
    app = IntegratedTool(root)
    root.mainloop()
    