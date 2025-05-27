# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ...utils.coordinate_converter import wgs84_to_gcj02, gcj02_to_wgs84, convert_coordinates, calculate_distance
from ...utils import amap_api
from .utils import call_amap_api, format_api_result, show_history_window, show_favorites_window, show_settings_window

class RouteTab:
    """路径规划选项卡"""
    
    def __init__(self, parent, notebook, theme, config, history_manager, favorite_manager):
        self.parent = parent
        self.notebook = notebook
        self.theme = theme
        self.config = config
        self.history_manager = history_manager
        self.favorite_manager = favorite_manager
        self.update_status = None  # 状态更新回调函数，由主类设置
        
        # 创建选项卡
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🚗 路径规划")
        self.setup_ui()
        
    def setup_ui(self):
        """创建路径规划选项卡UI"""
        # 起点输入
        origin_frame = tk.Frame(self.frame)
        origin_frame.pack(fill=tk.X, pady=5)
        
        origin_label_frame = tk.Frame(origin_frame)
        origin_label_frame.pack(fill=tk.X)
        
        tk.Label(origin_label_frame, text="起点经纬度 (WGS-84):", 
                font=("微软雅黑", 10), bg=self.theme.bg_color, fg=self.theme.text_color).pack(side=tk.LEFT)
        
        # 收藏位置按钮
        tk.Button(origin_label_frame, text="收藏位置", 
                 command=lambda: self.show_favorite_locations('origin'),
                 font=("微软雅黑", 8)).pack(side=tk.RIGHT, padx=5)
        
        self.origin_entry = tk.Entry(origin_frame, font=("微软雅黑", 10))
        self.origin_entry.pack(fill=tk.X, pady=2)
        self.origin_entry.insert(0, "116.397428,39.90923")  # 默认值：天安门
        
        # 终点输入
        destination_frame = tk.Frame(self.frame)
        destination_frame.pack(fill=tk.X, pady=5)
        
        destination_label_frame = tk.Frame(destination_frame)
        destination_label_frame.pack(fill=tk.X)
        
        tk.Label(destination_label_frame, text="终点经纬度 (WGS-84):", 
                font=("微软雅黑", 10), bg=self.theme.bg_color, fg=self.theme.text_color).pack(side=tk.LEFT)
        
        # 收藏位置按钮
        tk.Button(destination_label_frame, text="收藏位置", 
                 command=lambda: self.show_favorite_locations('destination'),
                 font=("微软雅黑", 8)).pack(side=tk.RIGHT, padx=5)
        
        self.destination_entry = tk.Entry(destination_frame, font=("微软雅黑", 10))
        self.destination_entry.pack(fill=tk.X, pady=2)
        self.destination_entry.insert(0, "116.407526,39.90403")  # 默认值：王府井
        
        # 计算按钮和功能按钮
        btn_frame = tk.Frame(self.frame, bg=self.theme.bg_color)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 主要功能按钮
        main_button_frame = tk.Frame(btn_frame, bg=self.theme.bg_color)
        main_button_frame.pack()
        
        calculate_btn = tk.Button(main_button_frame, text="计算路径", 
                                 command=self.calculate_routes,
                                 bg=self.theme.button_color, fg="white",
                                 font=("微软雅黑", 10), relief=tk.FLAT)
        calculate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # 辅助功能按钮
        aux_button_frame = tk.Frame(btn_frame, bg=self.theme.bg_color)
        aux_button_frame.pack(pady=5)
        
        tk.Button(aux_button_frame, text="历史记录", 
                 command=self.show_history,
                 font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(aux_button_frame, text="管理收藏", 
                 command=self.manage_favorites,
                 font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(aux_button_frame, text="设置", 
                 command=self.show_settings,
                 font=("微软雅黑", 9)).pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = tk.Frame(self.frame, bg=self.theme.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(result_frame, text="路径规划结果:", 
                font=("微软雅黑", 10, "bold"), bg=self.theme.bg_color, fg=self.theme.text_color).pack(anchor=tk.W)
        
        # 创建文本框和滚动条
        text_frame = tk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(text_frame, height=15, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def calculate_routes(self):
        """计算路径规划"""
        try:
            # 从输入框获取坐标
            origin_coords = self.origin_entry.get().strip()
            destination_coords = self.destination_entry.get().strip()
            
            if not origin_coords or not destination_coords:
                messagebox.showerror("错误", "请输入起点和终点坐标")
                return
                
            # 验证坐标格式
            try:
                start_lng, start_lat = map(float, origin_coords.split(','))
                end_lng, end_lat = map(float, destination_coords.split(','))
            except ValueError:
                messagebox.showerror("错误", "坐标格式错误，请使用：经度,纬度")
                return
            
            if self.update_status:
                self.update_status("正在计算路径...")
            
            # 在新线程中执行路径计算
            thread = threading.Thread(target=self._calculate_routes_thread, 
                                    args=(start_lng, start_lat, end_lng, end_lat))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"计算路径时出错: {str(e)}")
            if self.update_status:
                self.update_status("就绪")
            
    def _calculate_routes_thread(self, start_lng, start_lat, end_lng, end_lat):
        """在线程中计算路径"""
        try:
            # 将WGS-84坐标转换为GCJ-02坐标（高德地图使用的坐标系）
            start_lng_gcj, start_lat_gcj = wgs84_to_gcj02(start_lng, start_lat)
            end_lng_gcj, end_lat_gcj = wgs84_to_gcj02(end_lng, end_lat)
            
            origin = f"{start_lng_gcj},{start_lat_gcj}"
            destination = f"{end_lng_gcj},{end_lat_gcj}"
            
            # 在结果中显示坐标转换信息
            coord_info = f"坐标转换信息:\n起点: WGS-84({start_lng:.6f}, {start_lat:.6f}) -> GCJ-02({start_lng_gcj:.6f}, {start_lat_gcj:.6f})\n终点: WGS-84({end_lng:.6f}, {end_lat:.6f}) -> GCJ-02({end_lng_gcj:.6f}, {end_lat_gcj:.6f})\n\n"
            
            results = [coord_info]
            
            # 首先获取起点和终点的地址信息
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("正在获取起点地址..."))
            start_address_result = self._call_amap_api("maps_regeocode", {
                "location": origin
            })
            
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("正在获取终点地址..."))
            end_address_result = self._call_amap_api("maps_regeocode", {
                "location": destination
            })
            
            # 显示地址信息
            if start_address_result:
                results.append(f"起点地址信息:\n{start_address_result}\n")
            if end_address_result:
                results.append(f"终点地址信息:\n{end_address_result}\n")
            
            # 计算直线距离
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("正在计算直线距离..."))
            straight_distance_result = self._call_amap_api("maps_distance", {
                "origins": origin,
                "destination": destination,
                "type": "0"  # 直线距离
            })
            if straight_distance_result:
                results.append(f"直线距离:\n{straight_distance_result}\n")
            
            # 计算驾车路径
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("正在计算驾车路径..."))
            driving_result = self._call_amap_api("maps_direction_driving", {
                "origin": origin,
                "destination": destination
            })
            if driving_result:
                results.append(f"驾车路径:\n{driving_result}\n")
            
            # 计算步行路径
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("正在计算步行路径..."))
            walking_result = self._call_amap_api("maps_direction_walking", {
                "origin": origin,
                "destination": destination
            })
            if walking_result:
                results.append(f"步行路径:\n{walking_result}\n")
            
            # 保存到历史记录
            history_entry = {
                "type": "route_planning",
                "origin": f"{start_lng},{start_lat}",
                "destination": f"{end_lng},{end_lat}",
                "origin_address": start_address_result or "未知地址",
                "destination_address": end_address_result or "未知地址"
            }
            self.history_manager.add_entry(history_entry)
            
            # 更新UI显示结果
            result_text = "\n".join(results)
            self.parent.after(0, lambda: self._update_result(result_text))
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("路径计算完成"))
            
        except Exception as e:
            error_msg = f"路径计算出错: {str(e)}"
            self.parent.after(0, lambda: self._update_result(error_msg))
            if self.update_status:
                self.parent.after(0, lambda: self.update_status("计算失败"))
            
    def _call_amap_api(self, tool_name, params):
        """调用高德地图API"""
        try:
            # 检查是否配置了API密钥
            api_key = self.config.get_amap_api_key()
            
            if not api_key:
                return "错误：未配置API密钥，请先配置高德地图API密钥"
            
            # 调用真实API
            if tool_name == "maps_direction_driving":
                result = amap_api.direction_driving(params['origin'], params['destination'])
                if result['status'] == 'success':
                    return self._format_driving_result(result)
                else:
                    return f"驾车路径查询失败: {result.get('message', '未知错误')}"
            elif tool_name == "maps_direction_walking":
                result = amap_api.direction_walking(params['origin'], params['destination'])
                if result['status'] == 'success':
                    return self._format_walking_result(result)
                else:
                    return f"步行路径查询失败: {result.get('message', '未知错误')}"
            elif tool_name == "maps_distance":
                distance_type = int(params.get('type', '1'))
                result = amap_api.distance(params['origins'], params['destination'], distance_type)
                if result['status'] == 'success':
                    return self._format_distance_result(result, distance_type)
                else:
                    return f"距离查询失败: {result.get('message', '未知错误')}"
            elif tool_name == "maps_regeocode":
                lng, lat = map(float, params['location'].split(','))
                result = amap_api.regeocode(lng, lat)
                if result['status'] == 'success':
                    return self._format_regeocode_result(result)
                else:
                    return f"逆地理编码查询失败: {result.get('message', '未知错误')}"
            else:
                return f"不支持的API工具: {tool_name}"
                
        except Exception as e:
            return f"API调用失败: {str(e)}"
    
    def _format_driving_result(self, result):
        """格式化驾车路径结果"""
        try:
            distance = float(result['distance']) / 1000  # 转换为公里
            duration = int(result['duration']) // 60  # 转换为分钟
            
            steps_text = []
            for step in result.get('steps', []):
                instruction = step['instruction']
                step_distance = float(step['distance'])
                if step_distance >= 1000:
                    distance_str = f"{step_distance/1000:.1f}公里"
                else:
                    distance_str = f"{step_distance:.0f}米"
                steps_text.append(f"• {instruction} ({distance_str})")
            
            return f"""驾车路径规划：
距离：{distance:.1f}公里
预计用时：{duration}分钟

详细路线：
{chr(10).join(steps_text)}"""
        except Exception as e:
            return f"驾车路径解析失败: {str(e)}"
    
    def _format_walking_result(self, result):
        """格式化步行路径结果"""
        try:
            distance = float(result['distance'])  # 米
            duration = int(result['duration']) // 60  # 转换为分钟
            
            if distance >= 1000:
                distance_str = f"{distance/1000:.1f}公里"
            else:
                distance_str = f"{distance:.0f}米"
            
            steps_text = []
            for step in result.get('steps', []):
                instruction = step['instruction']
                step_distance = float(step['distance'])
                if step_distance >= 1000:
                    step_distance_str = f"{step_distance/1000:.1f}公里"
                else:
                    step_distance_str = f"{step_distance:.0f}米"
                steps_text.append(f"• {instruction} ({step_distance_str})")
            
            return f"""步行路径规划：
距离：{distance_str}
预计用时：{duration}分钟

详细路线：
{chr(10).join(steps_text)}"""
        except Exception as e:
            return f"步行路径解析失败: {str(e)}"
    
    def _format_distance_result(self, result, distance_type):
        """格式化距离测量结果"""
        try:
            distance = float(result['distance'])
            
            if distance >= 1000:
                distance_str = f"{distance/1000:.1f}公里"
            else:
                distance_str = f"{distance:.0f}米"
            
            type_names = {0: "直线距离", 1: "驾车距离", 3: "步行距离"}
            type_name = type_names.get(distance_type, "距离")
            
            if distance_type == 1 and 'duration' in result:
                duration = int(result['duration']) // 60
                return f"{type_name}：{distance_str}\n预计用时：{duration}分钟"
            else:
                return f"{type_name}：{distance_str}"
        except Exception as e:
            return f"距离测量解析失败: {str(e)}"
    
    def _format_regeocode_result(self, result):
        """格式化逆地理编码结果"""
        try:
            province = result.get('province', '')
            city = result.get('city', '')
            district = result.get('district', '')
            township = result.get('township', '')
            
            formatted_address = result.get('formatted_address', '')
            
            # 获取POI信息
            pois = result.get('pois', [])
            poi_info = ""
            if pois:
                nearest_poi = pois[0]
                poi_name = nearest_poi.get('name', '')
                poi_distance = nearest_poi.get('distance', '')
                if poi_name and poi_distance:
                    poi_info = f"\n附近地标：{poi_name} (距离{poi_distance}米)"
            
            return f"""地址信息：
省份：{province}
城市：{city}
区县：{district}
街道：{township}
详细地址：{formatted_address}{poi_info}"""
        except Exception as e:
            return f"地址解析失败: {str(e)}"
    
    def _update_result(self, text):
        """更新结果显示"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
    
    def show_favorite_locations(self, entry_type):
        """显示收藏位置选择对话框"""
        # TODO: 实现收藏位置功能
        messagebox.showinfo("提示", "收藏位置功能待实现")
    
    def show_history(self):
        """显示历史记录"""
        # TODO: 实现历史记录功能
        messagebox.showinfo("提示", "历史记录功能待实现")
    
    def manage_favorites(self):
        """管理收藏位置"""
        # TODO: 实现收藏管理功能
        messagebox.showinfo("提示", "收藏管理功能待实现")
    
    def show_settings(self):
        """显示设置"""
        # TODO: 实现设置功能
        messagebox.showinfo("提示", "设置功能待实现")