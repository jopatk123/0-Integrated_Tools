import tkinter as tk
from tkinter import ttk
import threading
from ...utils import amap_api


class WeatherTab:
    """天气预报选项卡"""
    
    def __init__(self, parent, notebook, theme, config):
        self.parent = parent
        self.notebook = notebook
        self.theme = theme
        self.config = config
        
        # 创建选项卡
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="🌤️ 天气预报")
        self.create_tab()
        
    def create_tab(self):
        """创建天气预报选项卡"""
        weather_frame = self.frame
        
        # 说明信息
        info_label = tk.Label(weather_frame, 
                             text="支持城市名称、详细地址查询，如：北京、上海、广州市天河区、杭州西湖区等",
                             font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.accent_color,
                             wraplength=600)
        info_label.pack(pady=(10, 5), padx=10, anchor=tk.W)
        
        # 城市输入
        input_frame = tk.Frame(weather_frame, bg=self.theme.bg_color)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(input_frame, text="城市/地址:", 
                font=("微软雅黑", 10), bg=self.theme.bg_color, fg=self.theme.text_color).pack(side=tk.LEFT)
        
        self.city_entry = tk.Entry(input_frame, width=30, font=("微软雅黑", 10))
        self.city_entry.pack(side=tk.LEFT, padx=(10, 10))
        self.city_entry.insert(0, "北京")
        
        # 绑定回车键
        self.city_entry.bind('<Return>', lambda event: self.query_weather())
        
        query_weather_btn = tk.Button(input_frame, text="查询天气", 
                                     command=self.query_weather,
                                     bg=self.theme.button_color, fg="white",
                                     font=("微软雅黑", 10), relief=tk.FLAT)
        query_weather_btn.pack(side=tk.LEFT)
        
        # 常用城市快捷按钮
        quick_cities_frame = tk.Frame(weather_frame, bg=self.theme.bg_color)
        quick_cities_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(quick_cities_frame, text="常用城市:", 
                font=("微软雅黑", 9), bg=self.theme.bg_color, fg=self.theme.text_color).pack(side=tk.LEFT)
        
        quick_cities = ["北京", "上海", "广州", "深圳", "杭州", "南京", "成都", "武汉"]
        for city in quick_cities:
            btn = tk.Button(quick_cities_frame, text=city, 
                           command=lambda c=city: self._set_city_and_query(c),
                           font=("微软雅黑", 8), relief=tk.FLAT,
                           bg=self.theme.bg_color, fg=self.theme.accent_color)
            btn.pack(side=tk.LEFT, padx=2)
        
        # 天气结果显示
        result_frame = tk.Frame(weather_frame, bg=self.theme.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Label(result_frame, text="天气信息:", 
                font=("微软雅黑", 10, "bold"), bg=self.theme.bg_color, fg=self.theme.text_color).pack(anchor=tk.W)
        
        text_frame = tk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.weather_result_text = tk.Text(text_frame, height=15, wrap=tk.WORD, font=("微软雅黑", 9))
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.weather_result_text.yview)
        self.weather_result_text.configure(yscrollcommand=scrollbar.set)
        
        self.weather_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def _set_city_and_query(self, city):
        """设置城市并查询天气"""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
        self.query_weather()
        
    def query_weather(self):
        """查询天气"""
        city_input = self.city_entry.get().strip()
        if not city_input:
            self._update_weather_result("请输入城市名称或地址")
            return
        
        self.update_status("正在查询天气...")
        
        # 在新线程中执行天气查询
        thread = threading.Thread(target=self._query_weather_thread, args=(city_input,))
        thread.daemon = True
        thread.start()
        
    def _query_weather_thread(self, city_input):
        """天气查询线程"""
        try:
            # 首先尝试直接查询天气
            self.parent.after(0, lambda: self.update_status(f"正在查询 {city_input} 的天气..."))
            
            weather_result = amap_api.weather(city_input)
            
            if weather_result['status'] == 'success':
                # 直接查询成功
                weather_info = self._format_weather_info(weather_result, city_input)
                self.parent.after(0, lambda: self._update_weather_result(weather_info))
                self.parent.after(0, lambda: self.update_status("天气查询完成"))
                return
            
            # 如果直接查询失败，尝试通过地理编码获取标准城市信息
            self.parent.after(0, lambda: self.update_status("正在解析地址..."))
            
            # 使用地理编码API将输入转换为标准地址
            geocode_result = amap_api.geocode(city_input)
            
            if geocode_result['status'] == 'success' and geocode_result.get('geocodes'):
                geocode = geocode_result['geocodes'][0]
                
                # 尝试使用不同的城市标识进行天气查询
                city_candidates = []
                
                # 1. 使用adcode（行政区划代码）
                adcode = geocode.get('adcode', '')
                if adcode:
                    city_candidates.append(adcode)
                
                # 2. 使用标准城市名称
                city_name = geocode.get('city', '')
                if city_name:
                    city_candidates.append(city_name)
                
                # 3. 使用省份名称（如果城市为空）
                province = geocode.get('province', '')
                if province and not city_name:
                    city_candidates.append(province)
                
                # 4. 使用区县名称
                district = geocode.get('district', '')
                if district:
                    city_candidates.append(district)
                
                # 依次尝试不同的城市标识
                for city_candidate in city_candidates:
                    if city_candidate:
                        self.parent.after(0, lambda c=city_candidate: self.update_status(f"正在查询 {c} 的天气..."))
                        weather_result = amap_api.weather(city_candidate)
                        
                        if weather_result['status'] == 'success':
                            weather_info = self._format_weather_info(weather_result, city_input, city_candidate)
                            self.parent.after(0, lambda: self._update_weather_result(weather_info))
                            self.parent.after(0, lambda: self.update_status("天气查询完成"))
                            return
                
                # 所有尝试都失败
                error_msg = f"无法获取 '{city_input}' 的天气信息\n\n解析到的地址信息：\n省份：{province}\n城市：{city_name}\n区县：{district}\n行政代码：{adcode}\n\n建议：请尝试输入更简洁的城市名称，如 '北京'、'上海'、'广州' 等"
            else:
                # 地理编码也失败
                error_msg = f"无法识别地址 '{city_input}'\n\n请检查输入的地址是否正确，或尝试输入标准的城市名称，如：\n• 北京\n• 上海\n• 广州\n• 深圳\n• 杭州"
            
            self.parent.after(0, lambda: self._update_weather_result(error_msg))
            self.parent.after(0, lambda: self.update_status("天气查询失败"))
            
        except Exception as e:
            error_msg = f"天气查询出错: {str(e)}\n\n请检查网络连接和API密钥配置"
            self.parent.after(0, lambda: self._update_weather_result(error_msg))
            self.parent.after(0, lambda: self.update_status("天气查询失败"))
            
    def _format_weather_info(self, weather_result, original_input, actual_city=None):
        """格式化天气信息显示"""
        try:
            city = weather_result.get('city', '')
            province = weather_result.get('province', '')
            reporttime = weather_result.get('reporttime', '')
            
            # 构建标题信息
            title_parts = []
            if actual_city and actual_city != original_input:
                title_parts.append(f"查询地址：{original_input}")
                title_parts.append(f"实际查询：{actual_city}")
            else:
                title_parts.append(f"查询地址：{original_input}")
            
            if province and city:
                title_parts.append(f"天气地区：{province} {city}")
            elif city:
                title_parts.append(f"天气地区：{city}")
            
            if reporttime:
                title_parts.append(f"更新时间：{reporttime}")
            
            result_lines = title_parts + ["\n" + "="*50 + "\n"]
            
            # 获取天气预报信息
            casts = weather_result.get('casts', [])
            if casts:
                for i, cast in enumerate(casts[:4]):  # 显示4天的天气
                    date = cast.get('date', '')
                    week = cast.get('week', '')
                    dayweather = cast.get('dayweather', '')
                    nightweather = cast.get('nightweather', '')
                    daytemp = cast.get('daytemp', '')
                    nighttemp = cast.get('nighttemp', '')
                    daywind = cast.get('daywind', '')
                    nightwind = cast.get('nightwind', '')
                    daypower = cast.get('daypower', '')
                    nightpower = cast.get('nightpower', '')
                    
                    day_label = "今天" if i == 0 else ("明天" if i == 1 else f"{date} {week}")
                    
                    result_lines.extend([
                        f"📅 {day_label} ({date} {week})",
                        f"🌤️  白天：{dayweather} {daytemp}°C",
                        f"🌙 夜间：{nightweather} {nighttemp}°C",
                        f"💨 风向：白天{daywind}{daypower} | 夜间{nightwind}{nightpower}",
                        ""
                    ])
            else:
                result_lines.append("暂无详细天气预报数据")
            
            return "\n".join(result_lines)
            
        except Exception as e:
            return f"天气信息格式化失败: {str(e)}"
    
    def _update_weather_result(self, text):
        """更新天气结果显示"""
        self.weather_result_text.delete(1.0, tk.END)
        self.weather_result_text.insert(tk.END, text)
        
    def update_status(self, message):
        """更新状态信息"""
        # 这里可以添加状态栏更新逻辑
        # 如果父组件有状态栏，可以通过回调更新
        pass