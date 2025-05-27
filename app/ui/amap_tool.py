import tkinter as tk
from tkinter import ttk, messagebox
from config import config
from .amap.dialogs import ApiKeyDialog
from .amap.route_tab import RouteTab
from .amap.geocoding_tab import GeocodingTab
from .amap.weather_tab import WeatherTab
from .amap.utils import HistoryManager, FavoriteManager, show_history_window, show_favorites_window, show_settings_window


class AmapTool:
    """高德地图工具主类 - 重构后的版本"""
    
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
            dialog = ApiKeyDialog(self.parent, self.config)
            if not dialog.show():
                # 用户取消了API密钥配置，退出工具
                messagebox.showwarning("警告", "未配置API密钥，高德地图工具将无法使用")
                if hasattr(self.parent, 'destroy'):
                    self.parent.destroy()
                return False
        return True
    
    def setup_ui(self):
        """设置主界面"""
        # 创建主框架
        main_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = tk.Label(main_frame, text="🗺️ 高德地图工具", 
                              font=("微软雅黑", 16, "bold"), 
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack(pady=10)
        
        # 坐标系说明
        coord_info = tk.Label(main_frame, 
                             text="📍 支持多种坐标系：WGS-84、GCJ-02、BD-09，程序会自动进行坐标转换",
                             font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.accent_color)
        coord_info.pack(pady=(0, 10))
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 创建各个选项卡
        self.route_tab = RouteTab(self.parent, self.notebook, self.theme, self.config, 
                                 self.history_manager, self.favorite_manager)
        self.geocoding_tab = GeocodingTab(self.parent, self.notebook, self.theme, self.config)
        self.weather_tab = WeatherTab(self.parent, self.notebook, self.theme, self.config)
        
        # 状态栏
        self.create_status_bar(main_frame)
        
        # 设置状态更新回调
        self.route_tab.update_status = self.update_status
        self.geocoding_tab.update_status = self.update_status
        self.weather_tab.update_status = self.update_status
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status_frame = tk.Frame(parent, bg=self.theme.bg_color, relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 状态文本
        status_label = tk.Label(status_frame, textvariable=self.status_text,
                               font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.text_color)
        status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 工具按钮
        button_frame = tk.Frame(status_frame, bg=self.theme.bg_color)
        button_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # 历史记录按钮
        history_btn = tk.Button(button_frame, text="📜 历史", 
                               command=self.show_history,
                               font=("微软雅黑", 8), relief=tk.FLAT,
                               bg=self.theme.bg_color, fg=self.theme.accent_color)
        history_btn.pack(side=tk.LEFT, padx=2)
        
        # 收藏管理按钮
        favorites_btn = tk.Button(button_frame, text="⭐ 收藏", 
                                 command=self.manage_favorites,
                                 font=("微软雅黑", 8), relief=tk.FLAT,
                                 bg=self.theme.bg_color, fg=self.theme.accent_color)
        favorites_btn.pack(side=tk.LEFT, padx=2)
        
        # 设置按钮
        settings_btn = tk.Button(button_frame, text="⚙️ 设置", 
                                command=self.show_settings,
                                font=("微软雅黑", 8), relief=tk.FLAT,
                                bg=self.theme.bg_color, fg=self.theme.accent_color)
        settings_btn.pack(side=tk.LEFT, padx=2)
    
    def update_status(self, message):
        """更新状态栏信息"""
        self.status_text.set(message)
    
    def show_history(self):
        """显示历史记录"""
        show_history_window(self.parent, self.history_manager, self.theme)
    
    def manage_favorites(self):
        """管理收藏位置"""
        show_favorites_window(self.parent, self.favorite_manager, self.theme)
    
    def show_settings(self):
        """显示设置"""
        show_settings_window(self.parent, self.config, self.theme)