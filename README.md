# 文件工具集成平台

## 项目简介

本项目是一个基于Python和Tkinter开发的多功能文件工具集成平台，旨在为用户提供文件路径获取、批量重命名、文件整理、图片GPS信息提取、视频压缩等常用文件操作的图形化解决方案。平台采用模块化设计，便于扩展和维护。

## 主要功能

- **文件路径获取**：浏览、扫描指定文件夹，支持文件过滤、导出Excel格式路径信息（包含完整路径、名称、大小、修改时间）、复制路径等操作。
- **批量文件重命名**：支持手动添加、Excel导入重命名规则，提供Excel模版导出功能，一键批量重命名。
- **文件整理**：可将文件自动整理到与文件名同名的文件夹中。
- **图片GPS信息提取**：批量提取图片的GPS信息，支持重命名图片和文件夹。
- **视频压缩**：批量压缩视频文件，支持自定义压缩程度。
- **最近点位匹配**：根据经纬度坐标计算并匹配最近的点位，支持Excel导入导出。
- **图片处理工具**：批量加载、预览、调整图片大小、裁剪和保存图片，支持多线程处理。

## 项目结构

```
.
├── main.py                  # 主程序入口
├── app/                     # 应用程序包
│   ├── __init__.py
│   ├── integrated_tool.py   # 主应用程序类，集成各功能模块
│   ├── ui/                  # 用户界面模块
│   │   ├── __init__.py
│   │   ├── file_path_tool.py        # 文件路径工具UI
│   │   ├── rename_tool.py           # 重命名工具UI
│   │   ├── file_organizer_tool.py   # 文件整理工具UI
│   │   ├── file_sorter_tool.py      # 文件分组工具UI
│   │   ├── image_gps_extractor_tool.py # 图片GPS信息提取UI
│   │   ├── video_resizer_tool.py    # 视频压缩工具UI
│   │   ├── point_matcher_tool.py    # 最近点位匹配工具UI
│   │   └── image_processor_tool.py  # 图片处理工具UI
│   └── utils/               # 工具类
│       ├── __init__.py
│       ├── file_operations.py       # 文件操作工具
│       └── theme.py                # 主题管理器
├── Rename_Template.xlsx      # 重命名模板示例
├── requirements.txt          # 依赖库列表
├── pyproject.toml            # 项目配置文件
├── .python-version           # Python版本配置
├── .gitignore                # Git忽略文件
└── README.md                 # 项目说明文档
```

## 环境管理

本项目使用uv进行环境管理，确保依赖一致性和可重现性。

1. 安装uv（如果尚未安装）：
   ```
   pip install uv
   ```
2. 安装依赖：
   ```
   uv pip install -r requirements.txt
   # 或者使用pyproject.toml
   uv pip install -e .
   ```

## 安装与运行

1. 安装依赖（传统方式）：
   ```
   pip install -r requirements.txt
   ```
   
   或使用uv（推荐）：
   ```
   uv pip install -r requirements.txt
   ```
   
2. 运行主程序：
   ```
   python main.py
   ```

## 使用说明

1. 启动程序后，选择所需功能模块（如文件路径获取、重命名、整理等）。
2. 按界面提示操作，如选择文件夹、设置过滤条件、导入Excel等。
3. 各模块均支持批量操作和结果导出。

## 扩展开发

- 新功能建议在`app/ui/`目录下新建模块。
- 在`app/integrated_tool.py`中注册新模块并添加到主界面。
- 通用工具类建议放在`app/utils/`目录下。

## 依赖说明

- Python 3.13+
- tkinter（Python内置）
- pandas>=1.3.0（数据处理和Excel操作）
- Pillow>=8.0.0（图像处理）
- pyperclip>=1.8.0（剪贴板操作）
- openpyxl>=3.0.0（Excel文件读写）
- matplotlib>=3.3.0（图表绘制）
- piexif>=1.1.0（图片EXIF信息处理）
- geopy>=2.0.0（地理位置计算）
- numpy>=1.20.0（数值计算）
- opencv-python>=4.5.0（图像和视频处理）
- send2trash>=1.8.0（安全删除文件到回收站）
- requests>=2.25.0（网络请求）

## 贡献与反馈

欢迎提交Issue或PR，提出建议或反馈问题。

## 许可证

本项目采用MIT License。