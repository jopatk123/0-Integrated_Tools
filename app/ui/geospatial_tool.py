# -*- coding: utf-8 -*-
"""地理空间工具集 - 整合高德地图工具和地理空间工具的所有功能"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import config
from .geospatial.dialogs import ConfigDialog
from .geospatial.poi_search_tab import POISearchTab
from .geospatial.conversion_tab import ConversionTab
from .geospatial.route_tab import RouteTab
from .geospatial.geocoding_tab import GeocodingTab
from .geospatial.weather_tab import WeatherTab
from .geospatial.utils import HistoryManager, FavoriteManager, show_history_window, show_favorites_window, show_settings_window

class GeospatialTool:
    """合并后的地理空间工具主类 - 整合所有地理空间相关功能"""
    
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.status_text = tk.StringVar(value="就绪")
        
        # 初始化配置和管理器
        self.config = config
        self.history_manager = HistoryManager(self.config)
        self.favorite_manager = FavoriteManager(self.config)
        
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
        
        # 功能说明
        feature_info = tk.Label(
            main_frame, 
            text="📍 集成POI搜索、路径规划、地理编码、天气查询、格式转换等功能 | 支持WGS-84、GCJ-02、BD-09坐标系自动转换",
            font=("微软雅黑", 9), 
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        feature_info.pack(pady=(0, 10))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建各个选项卡
        self.poi_search_tab = POISearchTab(
            self.parent, self.notebook, self.theme, self.config, self.favorite_manager
        )
        
        self.route_tab = RouteTab(
            self.parent, self.notebook, self.theme, self.config, 
            self.history_manager, self.favorite_manager
        )
        
        self.geocoding_tab = GeocodingTab(
            self.parent, self.notebook, self.theme, self.config
        )
        
        self.weather_tab = WeatherTab(
            self.parent, self.notebook, self.theme, self.config
        )
        
        self.conversion_tab = ConversionTab(
            self.parent, self.notebook, self.theme, self.config
        )
        
        # 状态栏
        self.create_status_bar(main_frame)
        
        # 设置状态更新回调
        self.poi_search_tab.update_status = self.update_status
        self.route_tab.update_status = self.update_status
        self.geocoding_tab.update_status = self.update_status
        self.weather_tab.update_status = self.update_status
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
        
        # 历史记录按钮
        history_btn = tk.Button(
            button_frame, 
            text="📜 历史", 
            command=self.show_history,
            font=("微软雅黑", 8), 
            relief=tk.FLAT,
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        history_btn.pack(side=tk.LEFT, padx=2)
        
        # 收藏管理按钮
        favorites_btn = tk.Button(
            button_frame, 
            text="⭐ 收藏", 
            command=self.manage_favorites,
            font=("微软雅黑", 8), 
            relief=tk.FLAT,
            bg=self.theme.bg_color, 
            fg=self.theme.accent_color
        )
        favorites_btn.pack(side=tk.LEFT, padx=2)
        
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
    
    def show_history(self):
        """显示历史记录"""
        show_history_window(self.parent, self.history_manager, self.theme)
    
    def manage_favorites(self):
        """管理收藏位置"""
        show_favorites_window(self.parent, self.favorite_manager, self.theme)
        # 更新POI搜索标签页的收藏位置下拉框
        if hasattr(self.poi_search_tab, 'update_favorite_locations'):
            self.poi_search_tab.update_favorite_locations()
        self.update_status("收藏位置已更新")
    
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

🔍 POI搜索功能：
• 输入WGS-84坐标和关键字搜索周边POI
• 支持收藏常用位置
• 可导出结果为Excel或KML格式

🚗 路径规划功能：
• 支持驾车、步行、公交路径规划
• 提供详细的路线信息和导航指引
• 可保存常用路线到历史记录

📍 批量地理编码：
• 批量查询坐标对应的行政区域信息
• 支持Excel文件导入导出
• 自动处理坐标系转换

🌤️ 天气预报：
• 支持城市名称、详细地址查询
• 提供实时天气和预报信息
• 常用城市快捷查询

🔄 格式转换功能：
• Excel ↔ KML 格式互转
• 地址 ↔ 经纬度批量转换
• KML点画圆功能
• 提供标准Excel模板下载

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
• 历史记录保存最近的查询结果
        """
        
        # 创建帮助窗口
        help_window = tk.Toplevel(self.parent)
        help_window.title("使用帮助")
        help_window.geometry("600x700")
        help_window.transient(self.parent)
        help_window.grab_set()
        
        # 设置窗口居中
        help_window.update_idletasks()
        x = (help_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (help_window.winfo_screenheight() // 2) - (700 // 2)
        help_window.geometry(f"600x700+{x}+{y}")
        
        # 创建滚动文本框
        text_frame = tk.Frame(help_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(
            text_frame, 
            wrap=tk.WORD, 
            font=("微软雅黑", 10),
            bg=self.theme.bg_color,
            fg=self.theme.text_color
        )
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        # 关闭按钮
        close_btn = tk.Button(
            help_window, 
            text="关闭", 
            command=help_window.destroy,
            font=("微软雅黑", 10),
            bg=self.theme.button_color,
            fg="white"
        )
        close_btn.pack(pady=10)