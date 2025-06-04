import tkinter as tk
from tkinter import ttk
from app.ui.file_path_tool import FilePathTool
from app.ui.rename_tool import RenameTool
from app.ui.file_organizer_tool import FileOrganizerTool
from app.ui.video_resizer_tool import VideoResizerTool
from app.ui.image_gps_extractor_tool import ImageGPSExtractorTool
from app.ui.file_sorter_tool import FileSorterTool
from app.ui.point_matcher_tool import PointMatcherTool
from app.ui.image_processor_tool import ImageProcessorTool
from app.ui.excel_image_extractor_tool import ExcelImageExtractorTool
from app.ui.geospatial_tool import GeoSpatialApp # Import the new tool
from app.ui.amap_tool import AmapTool # Import the Amap tool
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
        
        # 初始化文件路径工具界面
        self.file_path_tool = FilePathTool(self.file_path_frame, self.theme, self.notebook, self.rename_tool)
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg=self.theme.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡的框架
        self.file_path_frame = ttk.Frame(self.notebook)
        self.rename_frame = ttk.Frame(self.notebook)
        self.organizer_frame = ttk.Frame(self.notebook)
        self.video_resizer_frame = ttk.Frame(self.notebook)
        self.image_gps_frame = ttk.Frame(self.notebook)
        self.file_sorter_frame = ttk.Frame(self.notebook)
        self.point_matcher_frame = ttk.Frame(self.notebook)
        self.image_processor_frame = ttk.Frame(self.notebook)
        self.excel_image_extractor_frame = ttk.Frame(self.notebook)
        self.geospatial_tool_frame = ttk.Frame(self.notebook) # Create a frame for the new tool
        self.amap_tool_frame = ttk.Frame(self.notebook) # Create a frame for the Amap tool
        self.format_converter_frame = ttk.Frame(self.notebook) # Create a frame for the format converter tool
        
        # 添加选项卡
        self.notebook.add(self.file_path_frame, text="文件路径获取")
        self.notebook.add(self.rename_frame, text="文件重命名")
        self.notebook.add(self.organizer_frame, text="文件整理")
        self.notebook.add(self.video_resizer_frame, text="视频压缩")
        self.notebook.add(self.image_gps_frame, text="图片经纬度提取")
        self.notebook.add(self.file_sorter_frame, text="文件时间分类")
        self.notebook.add(self.point_matcher_frame, text="最近点位匹配")
        self.notebook.add(self.image_processor_frame, text="图片处理工具")
        self.notebook.add(self.excel_image_extractor_frame, text="Excel图片提取")
        self.notebook.add(self.geospatial_tool_frame, text="地理空间工具") # Add a tab for the new tool
        self.notebook.add(self.amap_tool_frame, text="高德地图工具") # Add a tab for the Amap tool
        self.notebook.add(self.format_converter_frame, text="格式转换工具") # Add a tab for the format converter tool
        
        # 初始化重命名工具界面 - 必须在创建选项卡后初始化
        self.rename_tool = RenameTool(self.rename_frame, self.theme)
        
        # 初始化文件整理工具界面
        self.file_organizer_tool = FileOrganizerTool(self.organizer_frame, self.theme)
        
        # 初始化视频压缩工具界面
        self.video_resizer_tool = VideoResizerTool(self.video_resizer_frame, self.theme)
        
        # 初始化图片经纬度提取工具界面
        self.image_gps_extractor_tool = ImageGPSExtractorTool(self.image_gps_frame, self.theme)
        
        # 初始化文件时间分类工具界面
        self.file_sorter_tool = FileSorterTool(self.file_sorter_frame, self.theme)
        
        # 初始化最近点位匹配工具界面
        self.point_matcher_tool = PointMatcherTool(self.point_matcher_frame, self.theme)
        
        # 初始化图片处理工具界面
        self.image_processor_tool = ImageProcessorTool(self.image_processor_frame, self.theme, self.config)
        
        # 初始化Excel图片提取工具界面
        self.excel_image_extractor_tool = ExcelImageExtractorTool(self.excel_image_extractor_frame, self.theme)

        # Initialize the new geospatial tool
        self.geospatial_tool = GeoSpatialApp(self.geospatial_tool_frame) # Initialize the new tool
        
        # Initialize the Amap tool
        self.amap_tool = AmapTool(self.amap_tool_frame, self.theme) # Initialize the Amap tool
        
        # Initialize the format converter tool
        self.format_converter_tool = FormatConverterTool(self.format_converter_frame, self.theme) # Initialize the format converter tool