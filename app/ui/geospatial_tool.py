# -*- coding: utf-8 -*-
"""地理空间工具 - 重构版本"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import config
from .geospatial.dialogs import ConfigDialog
from .geospatial.poi_search_tab import POISearchTab
from .geospatial.conversion_tab import ConversionTab

class GeospatialTool:
    """地理空间工具主类 - 重构后的版本"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.status_text = tk.StringVar(value="就绪")
        
        # 初始化配置
        self.config = config
        
        # 检查API密钥
        self.check_api_key()
        
        # 设置UI
        self.setup_ui()
    
    def check_api_key(self):
        """检查API密钥"""
        api_key = self.config.get_amap_api_key()
        if not api_key:
            messagebox.showwarning(
                "API Key未配置", 
                "请在配置中设置您的高德Web服务API Key。\n"
                "您可以从这里申请：https://lbs.amap.com/dev/key/app\n"
                "点击'配置管理'按钮进行设置。"
            )
    
    def setup_ui(self):
        """设置主界面"""
        # 创建主框架
        main_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(
            main_frame, 
            text="🌍 地理空间工具集", 
            font=("微软雅黑", 16, "bold"), 
            bg=self.theme.bg_color, 
            fg=self.theme.text_color
        )
        title_label.pack(pady=10)
        
        # 坐标系说明
        coord_info = tk.Label(
            main_frame, 
            text="📍 支持WGS-84坐标系，自动转换为GCJ-02调用高德API，结果转回WGS-84",
            font=("微软雅黑", 9), 
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        coord_info.pack(pady=(0, 10))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建各个选项卡
        self.poi_search_tab = POISearchTab(
            self.parent, self.notebook, self.theme, self.config, None
        )
        self.conversion_tab = ConversionTab(
            self.parent, self.notebook, self.theme, self.config
        )
        
        # 状态栏
        self.create_status_bar(main_frame)
        
        # 设置状态更新回调
        self.poi_search_tab.update_status = self.update_status
        self.conversion_tab.update_status = self.update_status
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = tk.Frame(parent, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 状态文本
        status_label = tk.Label(
            status_frame, 
            textvariable=self.status_text,
            font=("微软雅黑", 9), 
            bg=self.theme.bg_color, 
            fg=self.theme.text_color
        )
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 工具按钮
        button_frame = tk.Frame(status_frame, bg=self.theme.bg_color)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # 配置管理按钮
        config_btn = tk.Button(
            button_frame, 
            text="⚙️ 配置", 
            command=self.show_config,
            font=("微软雅黑", 8), 
            relief=tk.FLAT,
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        config_btn.pack(side=tk.LEFT, padx=2)
        
        # 帮助按钮
        help_btn = tk.Button(
            button_frame, 
            text="❓ 帮助", 
            command=self.show_help,
            font=("微软雅黑", 8), 
            relief=tk.FLAT,
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        help_btn.pack(side=tk.LEFT, padx=2)
    
    def update_status(self, message):
        """更新状态栏"""
        self.status_text.set(message)
        self.parent.update_idletasks()
    
    def show_config(self):
        """显示配置对话框"""
        dialog = ConfigDialog(self.parent, self.config)
        if dialog.show():
            # 配置更新后，刷新收藏位置
            if hasattr(self.poi_search_tab, 'update_favorite_locations'):
                self.poi_search_tab.update_favorite_locations()
            self.update_status("配置已更新")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
🌍 地理空间工具集使用说明

📍 POI搜索功能：
• 输入WGS-84坐标和关键字搜索周边POI
• 支持收藏常用位置
• 可导出结果为Excel或KML格式

🔄 格式转换功能：
• Excel ↔ KML 格式互转
• 地址 ↔ 经纬度批量转换
• KML点画圆功能

⚙️ 配置说明：
• 需要配置高德地图Web服务API Key
• 申请地址：https://lbs.amap.com/dev/key/app
• 选择'Web服务'平台类型

📋 坐标系说明：
• 输入输出均使用WGS-84坐标系
• 程序自动处理与高德API的坐标转换
• 确保数据的标准化和兼容性

💡 使用提示：
• 建议先配置API Key再使用
• 可以收藏常用位置便于快速选择
• 批量转换支持Excel文件导入导出
        """
        
        # 创建帮助窗口
        help_window = tk.Toplevel(self.parent)
        help_window.title("使用帮助")
        help_window.geometry("500x600")
        help_window.transient(self.parent)
        
        # 居中显示
        help_window.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # 创建文本框和滚动条
        text_frame = tk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            font=("微软雅黑", 10),
            bg="white",
            fg="black"
        )
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 插入帮助文本
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # 关闭按钮
        close_btn = tk.Button(
            help_window, 
            text="关闭", 
            command=help_window.destroy,
            font=("微软雅黑", 10)
        )
        close_btn.pack(pady=10)

# 为了保持向后兼容性，创建一个包装类
class GeoSpatialApp(GeospatialTool):
    """向后兼容的包装类"""
    
    def __init__(self, master):
        # 创建一个简单的主题对象
        class SimpleTheme:
            bg_color = "#f0f0f0"
            text_color = "#000000"
            accent_color = "#0066cc"
        
        theme = SimpleTheme()
        super().__init__(master, theme)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("地理空间工具集")
    root.geometry("800x700")
    app = GeoSpatialApp(root)
    root.mainloop()