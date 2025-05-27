# 文件工具集成平台

一个功能丰富的桌面工具集成平台，提供文件管理、图片处理、地理空间分析等多种实用工具。

## 🚀 功能特性

### 📁 文件管理工具

- **文件路径获取**：快速获取文件和文件夹的完整路径
- **文件重命名**：批量重命名文件，支持多种命名规则
- **文件整理**：按类型、日期等规则自动整理文件
- **文件时间分类**：根据文件创建/修改时间进行分类整理

### 🖼️ 图片处理工具

- **图片GPS提取**：从图片EXIF信息中提取GPS坐标
- **图片处理**：基础的图片编辑和处理功能
- **Excel图片提取**：从Excel文件中批量提取图片

### 🎥 视频处理工具

- **视频压缩**：高效的视频文件压缩和格式转换

### 🗺️ 地理空间工具

- **高德地图工具**：
  - 🚗 路径规划（驾车、步行、公交）
  - 📍 地理编码和逆地理编码
  - 🌤️ 天气查询
  - 💾 收藏位置和历史记录管理
- **地理空间分析工具**：
  - 🔍 POI搜索（支持WGS-84坐标系）
  - 🔄 坐标转换（WGS-84 ↔ GCJ-02）
  - 📊 格式转换（Excel ↔ KML）
  - 📍 地址与经纬度批量转换
  - 🎯 KML点画圆功能
  - ⭐ 收藏位置管理
- **最近点位匹配**：地理位置点位匹配分析

### ⚙️ 系统功能

- **主题管理**：支持多种界面主题
- **配置管理**：个性化设置和配置保存
- **历史记录**：操作历史记录和快速重用

## 📦 安装和使用

### 前置要求

- **Python 3.8+**
- **uv包管理器** - [安装指南](https://docs.astral.sh/uv/getting-started/installation/)
- **高德地图API密钥**（仅地图功能需要） - [申请地址](https://console.amap.com/dev/key/app)

### 快速开始

1. **克隆或下载项目**

   ```bash
   git clone <repository-url>
   cd Integrated_Tools
   ```
2. **使用快速启动脚本（推荐）**

   ```bash
   # Windows
   start.bat
   ```

   或手动启动：

   ```bash
   # 创建虚拟环境
   uv venv

   # 安装依赖
   uv pip install -r requirements.txt

   # 启动应用
   uv run python main.py
   ```
3. **配置API密钥**（可选）

   - 如需使用高德地图功能，首次启动时会提示输入API密钥
   - 其他工具无需额外配置即可使用

## 📖 使用指南

### 文件管理工具

#### 文件路径获取

1. 选择"文件路径获取"选项卡
2. 拖拽文件或文件夹到指定区域
3. 自动获取完整路径信息

#### 文件重命名

1. 选择"文件重命名"选项卡
2. 选择目标文件夹
3. 设置重命名规则
4. 执行批量重命名

#### 文件整理

1. 选择"文件整理"选项卡
2. 选择源文件夹和目标文件夹
3. 设置整理规则（按类型、日期等）
4. 开始自动整理

### 图片处理工具

#### 图片GPS提取

1. 选择"图片经纬度提取"选项卡
2. 选择包含图片的文件夹
3. 自动扫描并提取GPS信息
4. 导出结果到Excel文件

#### Excel图片提取

1. 选择"Excel图片提取"选项卡
2. 选择包含图片的Excel文件
3. 设置输出文件夹
4. 批量提取所有图片

### 地理空间工具

#### 高德地图工具

1. 选择"高德地图工具"选项卡
2. 在"路径规划"子选项卡中：
   - 输入起点和终点坐标
   - 选择路径类型（驾车/步行/公交）
   - 点击"计算路径"获取结果
3. 在"批量地理编码"子选项卡中：
   - 导入包含地址的Excel文件
   - 批量转换地址为坐标
4. 在"天气预报"子选项卡中：
   - 输入城市名称查询天气

#### 地理空间分析工具

1. 选择"地理空间工具"选项卡
2. 在"POI搜索"子选项卡中：
   - 输入WGS-84坐标和搜索关键字
   - 设置搜索半径
   - 查看周边POI信息
   - 导出结果为Excel或KML格式
3. 在"格式转换"子选项卡中：
   - Excel与KML格式互转
   - 地址与经纬度批量转换
   - KML点画圆功能
4. 支持收藏常用位置便于快速选择

#### 最近点位匹配

1. 选择"最近点位匹配"选项卡
2. 导入两组地理坐标数据
3. 设置匹配参数
4. 执行匹配分析

## 🏗️ 项目结构

```
Integrated_Tools/
├── app/
│   ├── integrated_tool.py          # 主集成平台
│   ├── ui/                         # 用户界面模块
│   │   ├── amap/                   # 高德地图工具模块
│   │   │   ├── route_tab.py        # 路径规划
│   │   │   ├── geocoding_tab.py    # 地理编码
│   │   │   ├── weather_tab.py      # 天气查询
│   │   │   ├── dialogs.py          # 对话框组件
│   │   │   └── utils.py            # 工具函数
│   │   ├── geospatial/             # 地理空间工具模块
│   │   │   ├── coordinate_utils.py # 坐标转换工具
│   │   │   ├── amap_api.py         # 高德API封装
│   │   │   ├── kml_utils.py        # KML文件处理
│   │   │   ├── poi_search_tab.py   # POI搜索界面
│   │   │   ├── conversion_tab.py   # 格式转换界面
│   │   │   └── dialogs.py          # 配置对话框
│   │   ├── amap_tool.py            # 高德地图工具主类
│   │   ├── file_path_tool.py       # 文件路径工具
│   │   ├── rename_tool.py          # 重命名工具
│   │   ├── file_organizer_tool.py  # 文件整理工具
│   │   ├── video_resizer_tool.py   # 视频压缩工具
│   │   ├── image_gps_extractor_tool.py # 图片GPS提取
│   │   ├── file_sorter_tool.py     # 文件分类工具
│   │   ├── point_matcher_tool.py   # 点位匹配工具
│   │   ├── image_processor_tool.py # 图片处理工具
│   │   ├── excel_image_extractor_tool.py # Excel图片提取
│   │   └── geospatial_tool.py      # 地理空间工具主类
│   └── utils/                      # 工具库
│       ├── amap_api.py             # 高德地图API
│       ├── coordinate_converter.py  # 坐标转换
│       ├── file_operations.py      # 文件操作
│       ├── history_manager.py      # 历史管理
│       └── theme.py                # 主题管理
├── config.py                       # 配置管理
├── main.py                         # 应用入口
├── requirements.txt                # 依赖列表
├── pyproject.toml                  # 项目配置
├── start.bat                       # 启动脚本
├── user_config.json               # 用户配置
├── user_history.json              # 用户历史
└── README.md                       # 说明文档
```

## 🔧 配置文件

应用会自动创建以下配置文件：

- `user_config.json` - 用户个人配置
- `user_history.json` - 操作历史记录
- `config.py` - 应用配置管理

### 配置选项示例

```json
{
  "amap_api_key": "your_api_key_here",
  "theme": "light",
  "window_size": "1000x700",
  "auto_save_history": true,
  "max_history_records": 1000
}
```

## 🔑 API密钥申请（高德地图功能）

1. 访问[高德开放平台](https://console.amap.com/dev/key/app)
2. 注册并登录账号
3. 创建新应用
4. 申请"Web服务API"密钥
5. 在应用设置中配置密钥

## 🐛 故障排除

### 常见问题

1. **应用启动失败**

   - 检查Python版本（需要3.8+）
   - 确认依赖是否完整安装：`uv pip install -r requirements.txt`
   - 查看控制台错误信息
2. **高德地图功能无法使用**

   - 检查API密钥是否正确配置
   - 确认网络连接正常
   - 查看API配额是否用完
3. **文件处理失败**

   - 确认文件路径正确且有访问权限
   - 检查文件格式是否支持
   - 确保有足够的磁盘空间

### 日志查看

应用运行时的详细信息会显示在控制台中，如遇问题请查看控制台输出获取错误详情。
