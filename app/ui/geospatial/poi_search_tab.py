# -*- coding: utf-8 -*-
"""POI搜索选项卡模块"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import xml.etree.ElementTree as ET
import openpyxl
from .amap_api import search_nearby_pois_amap
from .kml_utils import create_kml_placemark, pretty_print_xml

class POISearchTab:
    """POI搜索选项卡"""
    
    def __init__(self, parent, notebook, theme, config, favorite_manager):
        self.parent = parent
        self.theme = theme
        self.config = config
        self.favorite_manager = favorite_manager
        self.current_results = []
        self.update_status = None  # 状态更新回调函数
        
        # 创建选项卡
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🔍 POI搜索")
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主容器
        main_paned = ttk.PanedWindow(self.frame, orient=tk.VERTICAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 输入区域
        input_container = ttk.Frame(main_paned)
        main_paned.add(input_container, weight=0)
        
        input_frame = ttk.LabelFrame(input_container, text="周边POI查询 (WGS-84输入)")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.create_input_section(input_frame)
        
        # 结果区域
        results_container = ttk.Frame(main_paned)
        main_paned.add(results_container, weight=1)
        
        self.create_results_section(results_container)
        
        # 导出按钮区域
        self.create_export_section(results_container)
    
    def create_input_section(self, parent):
        """创建输入区域"""
        # 收藏位置选择
        config_frame = ttk.Frame(parent)
        config_frame.grid(row=0, column=0, columnspan=3, pady=5, sticky="ew")
        
        ttk.Label(config_frame, text="收藏位置:").pack(side=tk.LEFT, padx=5)
        self.favorite_var = tk.StringVar()
        self.favorite_combo = ttk.Combobox(config_frame, textvariable=self.favorite_var, 
                                          width=15, state="readonly")
        self.favorite_combo.pack(side=tk.LEFT, padx=5)
        self.favorite_combo.bind("<<ComboboxSelected>>", self.on_favorite_selected)
        self.update_favorite_locations()
        
        # 经度输入
        ttk.Label(parent, text="WGS-84 经度:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lon_entry = ttk.Entry(parent, width=25)
        self.lon_entry.grid(row=1, column=1, padx=5, pady=5)
        self.lon_entry.insert(0, "119.429737")
        
        # 收藏按钮
        self.add_favorite_button = ttk.Button(parent, text="收藏", 
                                             command=self.add_current_location_to_favorites)
        self.add_favorite_button.grid(row=1, column=2, padx=5, pady=5)
        
        # 纬度输入
        ttk.Label(parent, text="WGS-84 纬度:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lat_entry = ttk.Entry(parent, width=25)
        self.lat_entry.grid(row=2, column=1, padx=5, pady=5)
        self.lat_entry.insert(0, "25.97546")
        
        # 关键字输入
        ttk.Label(parent, text="查询关键字:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.keyword_entry = ttk.Entry(parent, width=25)
        self.keyword_entry.grid(row=3, column=1, padx=5, pady=5)
        self.keyword_entry.insert(0, "加油站")
        
        # 半径输入
        ttk.Label(parent, text="查询半径 (km):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.radius_entry = ttk.Entry(parent, width=25)
        self.radius_entry.grid(row=4, column=1, padx=5, pady=5)
        self.radius_entry.insert(0, "6")
        
        # 搜索按钮
        self.search_button = ttk.Button(parent, text="查询POI", command=self.perform_search)
        self.search_button.grid(row=5, column=0, columnspan=3, pady=10)
        
        # 配置列权重
        parent.grid_columnconfigure(1, weight=1)
    
    def create_results_section(self, parent):
        """创建结果显示区域"""
        results_frame = ttk.LabelFrame(parent, text="查询结果")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建表格
        columns = ("name", "lon", "lat")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        self.results_tree.heading("name", text="名称")
        self.results_tree.heading("lon", text="WGS-84 经度")
        self.results_tree.heading("lat", text="WGS-84 纬度")
        
        self.results_tree.column("name", width=250, stretch=tk.YES)
        self.results_tree.column("lon", width=150, anchor="e", stretch=tk.YES)
        self.results_tree.column("lat", width=150, anchor="e", stretch=tk.YES)
        
        # 滚动条
        vsb = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        hsb = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.results_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)
    
    def create_export_section(self, parent):
        """创建导出按钮区域"""
        export_frame = ttk.Frame(parent)
        export_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.export_excel_button = ttk.Button(export_frame, text="导出Excel", 
                                             command=self.export_to_excel)
        self.export_excel_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.export_kml_button = ttk.Button(export_frame, text="导出KML", 
                                           command=self.export_to_kml)
        self.export_kml_button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def perform_search(self):
        """执行POI搜索"""
        if self.update_status:
            self.update_status("正在查询...")
        
        api_key = self.config.get_amap_api_key()
        if not api_key:
            messagebox.showerror("API Key错误", "请先在配置中设置有效的高德API Key。")
            if self.update_status:
                self.update_status("API Key未配置")
            return
        
        try:
            wgs_lon_str = self.lon_entry.get().strip()
            wgs_lat_str = self.lat_entry.get().strip()
            keywords = self.keyword_entry.get().strip()
            radius_km_str = self.radius_entry.get().strip()
            
            if not all([wgs_lon_str, wgs_lat_str, keywords, radius_km_str]):
                messagebox.showerror("输入错误", "所有输入字段均不能为空。")
                if self.update_status:
                    self.update_status("输入字段不能为空")
                return
            
            wgs_lon = float(wgs_lon_str)
            wgs_lat = float(wgs_lat_str)
            radius_km = float(radius_km_str)
        except ValueError:
            messagebox.showerror("输入错误", "经纬度和半径必须是有效的数字。")
            if self.update_status:
                self.update_status("输入错误：需要数字格式")
            return
        
        if radius_km <= 0:
            messagebox.showerror("输入错误", "查询半径必须大于0。")
            if self.update_status:
                self.update_status("半径错误：必须大于0")
            return
        
        radius_meters = radius_km * 1000
        
        # 清空之前的结果
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)
        self.current_results = []
        
        # 执行搜索
        error_msg, pois = search_nearby_pois_amap(wgs_lon, wgs_lat, radius_meters, keywords, api_key=api_key)
        
        if error_msg:
            messagebox.showerror("查询失败", f"{error_msg}")
            if self.update_status:
                self.update_status(f"查询失败: {error_msg}")
        elif pois:
            self.current_results = pois
            for poi in pois:
                self.results_tree.insert("", "end", values=(
                    poi["name"],
                    f"{poi['wgs84_lon']:.6f}",
                    f"{poi['wgs84_lat']:.6f}"
                ))
            if self.update_status:
                self.update_status(f"查询完成，找到 {len(pois)} 个结果")
        else:
            messagebox.showinfo("查询结果", "未找到符合条件的POI。")
            if self.update_status:
                self.update_status("未找到结果")
    
    def export_to_excel(self):
        """导出结果到Excel"""
        if not self.current_results:
            messagebox.showinfo("无数据", "没有可导出的查询结果。")
            return
        
        try:
            import openpyxl
        except ImportError:
            messagebox.showerror("缺少库", "需要安装 openpyxl 库才能导出Excel。\n请运行: pip install openpyxl")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel 工作簿", "*.xlsx"), ("所有文件", "*.*")],
            title="保存查询结果为Excel"
        )
        
        if not file_path:
            return
        
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = "查询结果"
            
            sheet["A1"] = "名称"
            sheet["B1"] = "WGS-84 经度"
            sheet["C1"] = "WGS-84 纬度"
            
            for row_idx, poi in enumerate(self.current_results, start=2):
                sheet[f"A{row_idx}"] = poi["name"]
                sheet[f"B{row_idx}"] = poi["wgs84_lon"]
                sheet[f"C{row_idx}"] = poi["wgs84_lat"]
            
            workbook.save(file_path)
            messagebox.showinfo("导出成功", f"结果已成功导出到:\n{file_path}")
            if self.update_status:
                self.update_status(f"结果已导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("导出失败", f"导出到Excel时发生错误: {e}")
            if self.update_status:
                self.update_status(f"导出失败: {e}")
    
    def export_to_kml(self):
        """导出结果到KML"""
        if not self.current_results:
            messagebox.showinfo("无数据", "没有可导出的查询结果。")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".kml",
            filetypes=[("KML 文件", "*.kml"), ("所有文件", "*.*")],
            title="保存查询结果为KML"
        )
        
        if not file_path:
            return
        
        kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
        document = ET.SubElement(kml, "Document")
        
        for poi in self.current_results:
            placemark = create_kml_placemark(poi["name"], poi["wgs84_lon"], poi["wgs84_lat"])
            document.append(placemark)
        
        try:
            tree_string = ET.tostring(kml, encoding='utf-8', method='xml')
            pretty_xml_string = pretty_print_xml(tree_string.decode('utf-8'))
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(pretty_xml_string)
            messagebox.showinfo("导出成功", f"结果已成功导出到:\n{file_path}")
            if self.update_status:
                self.update_status(f"KML结果已导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("导出KML失败", f"导出到KML时发生错误: {e}")
            if self.update_status:
                self.update_status(f"导出KML失败: {e}")
    
    def update_favorite_locations(self):
        """更新收藏位置下拉框"""
        favorites = self.config.get_favorite_locations()
        favorite_names = [loc['name'] for loc in favorites]
        self.favorite_combo['values'] = favorite_names
        if favorite_names:
            self.favorite_combo.set('')
    
    def on_favorite_selected(self, event):
        """当选择收藏位置时，自动填充坐标"""
        selected_name = self.favorite_var.get()
        if selected_name:
            favorites = self.config.get_favorite_locations()
            for loc in favorites:
                if loc['name'] == selected_name:
                    self.lon_entry.delete(0, tk.END)
                    self.lon_entry.insert(0, str(loc['lng']))
                    self.lat_entry.delete(0, tk.END)
                    self.lat_entry.insert(0, str(loc['lat']))
                    break
    
    def add_current_location_to_favorites(self):
        """将当前输入的坐标添加到收藏位置"""
        try:
            lng = float(self.lon_entry.get().strip())
            lat = float(self.lat_entry.get().strip())
            
            name = tk.simpledialog.askstring("添加收藏位置", "请输入位置名称:")
            if name and name.strip():
                if self.config.add_favorite_location(name.strip(), lng, lat):
                    self.update_favorite_locations()
                    messagebox.showinfo("成功", f"已添加收藏位置: {name.strip()}")
                else:
                    messagebox.showerror("错误", "添加收藏位置失败")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的坐标")