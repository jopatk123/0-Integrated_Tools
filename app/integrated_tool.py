import tkinter as tk
from tkinter import ttk
from app.ui.system_file_tool import SystemFileTool
from app.ui.video_resizer_tool import VideoResizerTool
# from app.ui.image_gps_extractor_tool import ImageGPSExtractorTool  # 已合并到图片处理工具
# 原文件路径获取、重命名、整理、时间分类工具已合并到系统文件处理工具
from app.ui.point_matcher_tool import PointMatcherTool
from app.ui.image_processor_tool import ImageProcessorTool
from app.ui.excel_image_extractor_tool import ExcelImageExtractorTool
from app.ui.geospatial_tool import GeospatialTool # Import the geospatial tool
from app.ui.format_converter_tool import FormatConverterTool # Import the format converter tool
from app.utils.theme import ThemeManager
from app.config import config

class IntegratedTool:
    def __init__(self, root):
        self.root = root
        self.root.title("文件工具集成平台")
        self.root.geometry("1000x900")
        self.root.minsize(800, 600)
        
        # 设置主题颜色
        self.theme = ThemeManager()
        self.config = config
        self.root.configure(bg=self.theme.bg_color)
        
        # 创建主框架
        self.create_main_frame()
        
        # 创建选项卡
        self.create_notebook()
        
        # 文件路径工具已合并到系统文件处理工具
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.theme.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡的框架
        self.system_file_frame = ttk.Frame(self.notebook)
        self.video_resizer_frame = ttk.Frame(self.notebook)
        # self.image_gps_frame = ttk.Frame(self.notebook)  # 已合并到图片处理工具
        # 原文件路径、重命名、整理、时间分类框架已合并到系统文件处理工具
        self.point_matcher_frame = ttk.Frame(self.notebook)
        self.image_processor_frame = ttk.Frame(self.notebook)
        self.excel_image_extractor_frame = ttk.Frame(self.notebook)
        self.geospatial_frame = ttk.Frame(self.notebook) # Create a frame for the geospatial tool
        self.format_converter_frame = ttk.Frame(self.notebook) # Create a frame for the format converter tool
        
        # 添加选项卡
        self.notebook.add(self.system_file_frame, text="系统文件处理")
        self.notebook.add(self.video_resizer_frame, text="视频压缩")
        # self.notebook.add(self.image_gps_frame, text="图片经纬度提取")  # 已合并到图片处理工具
        # 原文件路径获取、重命名、整理、时间分类选项卡已合并到系统文件处理
        self.notebook.add(self.point_matcher_frame, text="最近点位匹配")
        self.notebook.add(self.image_processor_frame, text="图片处理工具集")
        self.notebook.add(self.excel_image_extractor_frame, text="Excel图片提取")
        self.notebook.add(self.geospatial_frame, text="地理空间工具集") # Add a tab for the geospatial tool
        self.notebook.add(self.format_converter_frame, text="格式转换工具") # Add a tab for the format converter tool
        
        # 初始化系统文件处理工具界面
        self.system_file_tool = SystemFileTool(self.system_file_frame, self.theme, self.config)
        
        # 初始化视频压缩工具界面
        self.video_resizer_tool = VideoResizerTool(self.video_resizer_frame, self.theme)
        
        # 初始化图片经纬度提取工具界面 - 已合并到图片处理工具
        # self.image_gps_extractor_tool = ImageGPSExtractorTool(self.image_gps_frame, self.theme)
        
        # 原重命名、文件整理、文件时间分类工具已合并到系统文件处理工具
        
        # 初始化最近点位匹配工具界面
        self.point_matcher_tool = PointMatcherTool(self.point_matcher_frame, self.theme)
        
        # 初始化图片处理工具界面
        self.image_processor_tool = ImageProcessorTool(self.image_processor_frame, self.theme, self.config)
        
        # 初始化Excel图片提取工具界面
        self.excel_image_extractor_tool = ExcelImageExtractorTool(self.excel_image_extractor_frame, self.theme)

        # Initialize the geospatial tool
        self.geospatial_tool = GeospatialTool(self.geospatial_frame, self.theme) # Initialize the geospatial tool
        
        # Initialize the format converter tool
        self.format_converter_tool = FormatConverterTool(self.format_converter_frame, self.theme) # Initialize the format converter tool