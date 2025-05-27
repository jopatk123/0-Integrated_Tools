"""高德地图工具的公共工具函数"""

import tkinter as tk
from tkinter import messagebox
import threading
from ...utils import amap_api


class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, config):
        self.config = config
    
    def add_record(self, query_type, **kwargs):
        """添加历史记录"""
        # 这里可以实现历史记录的添加逻辑
        pass
    
    def add_entry(self, entry):
        """添加历史记录条目"""
        # 这里可以实现历史记录条目的添加逻辑
        pass
    
    def get_all_records(self):
        """获取所有历史记录"""
        # 这里可以实现获取历史记录的逻辑
        return []
    
    def clear_all_records(self):
        """清空所有历史记录"""
        # 这里可以实现清空历史记录的逻辑
        pass


class FavoriteManager:
    """收藏位置管理器"""
    
    def __init__(self, config):
        self.config = config
    
    def get_favorites(self):
        """获取收藏位置列表"""
        return self.config.get('favorite_locations', [])
    
    def add_favorite(self, name, lng, lat):
        """添加收藏位置"""
        favorites = self.get_favorites()
        # 检查是否已存在同名位置
        for i, location in enumerate(favorites):
            if location.get('name') == name:
                favorites[i] = {'name': name, 'lng': lng, 'lat': lat}
                break
        else:
            favorites.append({'name': name, 'lng': lng, 'lat': lat})
        
        self.config.set('favorite_locations', favorites)
        self.config.save_config()
    
    def remove_favorite(self, name):
        """删除收藏位置"""
        favorites = self.get_favorites()
        for i, location in enumerate(favorites):
            if location.get('name') == name:
                favorites.pop(i)
                break
        
        self.config.set('favorite_locations', favorites)
        self.config.save_config()


def show_history_window(parent, history_manager, theme):
    """显示历史记录窗口"""
    try:
        # 创建历史记录窗口
        history_window = tk.Toplevel(parent)
        history_window.title("历史记录")
        history_window.geometry("600x400")
        history_window.transient(parent)
        
        # 居中显示
        history_window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # 历史记录列表
        listbox_frame = tk.Frame(history_window)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        history_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        history_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_listbox.yview)
        
        # 加载历史记录
        def load_history():
            history_listbox.delete(0, tk.END)
            records = history_manager.get_all_records()
            for record in records:
                timestamp = record.get('timestamp', '')
                query_type = record.get('query_type', '')
                origin = record.get('origin', '')
                destination = record.get('destination', '')
                
                if query_type == 'route_planning':
                    display_text = f"[{timestamp}] 路径规划: {origin} → {destination}"
                else:
                    display_text = f"[{timestamp}] {query_type}: {origin}"
                
                history_listbox.insert(tk.END, display_text)
        
        load_history()
        
        # 按钮框架
        button_frame = tk.Frame(history_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def delete_selected():
            selection = history_listbox.curselection()
            if selection:
                if messagebox.askyesno("确认删除", "确定要删除选中的历史记录吗？"):
                    # 这里需要实现删除逻辑
                    load_history()
        
        def clear_all():
            if messagebox.askyesno("确认清空", "确定要清空所有历史记录吗？"):
                history_manager.clear_all_records()
                load_history()
        
        tk.Button(button_frame, text="删除选中", command=delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="清空全部", command=clear_all).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="关闭", command=history_window.destroy).pack(side=tk.RIGHT, padx=5)
        
    except Exception as e:
        messagebox.showerror("错误", f"显示历史记录失败: {str(e)}")


def show_favorites_window(parent, favorite_manager, theme):
    """显示收藏管理窗口"""
    try:
        # 创建收藏管理窗口
        favorites_window = tk.Toplevel(parent)
        favorites_window.title("管理收藏位置")
        favorites_window.geometry("500x400")
        favorites_window.transient(parent)
        
        # 居中显示
        favorites_window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # 收藏列表
        list_frame = tk.Frame(favorites_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        favorites_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        favorites_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=favorites_listbox.yview)
        
        # 加载收藏位置
        def load_favorites():
            favorites_listbox.delete(0, tk.END)
            favorite_locations = favorite_manager.get_favorites()
            for location in favorite_locations:
                if isinstance(location, dict):
                    name = location.get('name', '未命名')
                    lng = location.get('lng', 0)
                    lat = location.get('lat', 0)
                    coords = f"{lng},{lat}"
                    favorites_listbox.insert(tk.END, f"{name}: {coords}")
        
        load_favorites()
        
        # 添加新收藏
        add_frame = tk.Frame(favorites_window)
        add_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(add_frame, text="名称:").pack(side=tk.LEFT)
        name_entry = tk.Entry(add_frame, width=15)
        name_entry.pack(side=tk.LEFT, padx=5)
        
        tk.Label(add_frame, text="坐标:").pack(side=tk.LEFT)
        coords_entry = tk.Entry(add_frame, width=20)
        coords_entry.pack(side=tk.LEFT, padx=5)
        
        def add_favorite():
            name = name_entry.get().strip()
            coords = coords_entry.get().strip()
            if name and coords:
                try:
                    # 解析坐标
                    lng, lat = map(float, coords.split(','))
                    favorite_manager.add_favorite(name, lng, lat)
                    name_entry.delete(0, tk.END)
                    coords_entry.delete(0, tk.END)
                    load_favorites()
                except ValueError:
                    messagebox.showerror("错误", "坐标格式错误，请使用 经度,纬度 格式")
            else:
                messagebox.showwarning("警告", "请输入名称和坐标")
        
        tk.Button(add_frame, text="添加", command=add_favorite).pack(side=tk.LEFT, padx=5)
        
        # 按钮框架
        button_frame = tk.Frame(favorites_window)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        def delete_selected():
            selection = favorites_listbox.curselection()
            if selection:
                if messagebox.askyesno("确认删除", "确定要删除选中的收藏位置吗？"):
                    text = favorites_listbox.get(selection[0])
                    name = text.split(':')[0]
                    favorite_manager.remove_favorite(name)
                    load_favorites()
        
        tk.Button(button_frame, text="删除选中", command=delete_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="关闭", command=favorites_window.destroy).pack(side=tk.RIGHT, padx=5)
        
    except Exception as e:
        messagebox.showerror("错误", f"管理收藏位置失败: {str(e)}")


def show_settings_window(parent, config, theme):
    """显示设置窗口"""
    try:
        # 创建设置窗口
        settings_window = tk.Toplevel(parent)
        settings_window.title("设置")
        settings_window.geometry("400x300")
        settings_window.transient(parent)
        
        # 居中显示
        settings_window.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # API密钥设置
        api_frame = tk.LabelFrame(settings_window, text="API设置", padx=10, pady=10)
        api_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(api_frame, text="高德地图API密钥:").pack(anchor=tk.W)
        api_key_entry = tk.Entry(api_frame, width=50, show="*")
        api_key_entry.pack(fill=tk.X, pady=5)
        
        # 加载当前API密钥
        current_key = config.get_amap_api_key()
        if current_key:
            api_key_entry.insert(0, current_key)
        
        # 缓存设置
        cache_frame = tk.LabelFrame(settings_window, text="缓存设置", padx=10, pady=10)
        cache_frame.pack(fill=tk.X, padx=10, pady=10)
        
        cache_enabled_var = tk.BooleanVar()
        cache_enabled_var.set(config.get('cache_enabled', True))
        tk.Checkbutton(cache_frame, text="启用结果缓存", variable=cache_enabled_var).pack(anchor=tk.W)
        
        tk.Label(cache_frame, text="缓存过期时间(小时):").pack(anchor=tk.W)
        cache_ttl_entry = tk.Entry(cache_frame, width=10)
        cache_ttl_entry.pack(anchor=tk.W, pady=5)
        cache_ttl_entry.insert(0, str(config.get('cache_ttl_hours', 24)))
        
        # 历史记录设置
        history_frame = tk.LabelFrame(settings_window, text="历史记录设置", padx=10, pady=10)
        history_frame.pack(fill=tk.X, padx=10, pady=10)
        
        history_enabled_var = tk.BooleanVar()
        history_enabled_var.set(config.get('history_enabled', True))
        tk.Checkbutton(history_frame, text="启用历史记录", variable=history_enabled_var).pack(anchor=tk.W)
        
        tk.Label(history_frame, text="最大历史记录数:").pack(anchor=tk.W)
        max_history_entry = tk.Entry(history_frame, width=10)
        max_history_entry.pack(anchor=tk.W, pady=5)
        max_history_entry.insert(0, str(config.get('max_history_records', 100)))
        
        # 保存设置
        def save_settings():
            try:
                # 保存API密钥
                new_api_key = api_key_entry.get().strip()
                if new_api_key:
                    config.set_amap_api_key(new_api_key)
                
                # 保存缓存设置
                config.set('cache_enabled', cache_enabled_var.get())
                try:
                    cache_ttl = int(cache_ttl_entry.get())
                    config.set('cache_ttl_hours', cache_ttl)
                except ValueError:
                    pass
                
                # 保存历史记录设置
                config.set('history_enabled', history_enabled_var.get())
                try:
                    max_history = int(max_history_entry.get())
                    config.set('max_history_records', max_history)
                except ValueError:
                    pass
                
                config.save_config()
                messagebox.showinfo("成功", "设置已保存")
                settings_window.destroy()
                
            except Exception as e:
                messagebox.showerror("错误", f"保存设置失败: {str(e)}")
        
        # 按钮框架
        button_frame = tk.Frame(settings_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="保存", command=save_settings).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="取消", command=settings_window.destroy).pack(side=tk.RIGHT, padx=5)
        
    except Exception as e:
        messagebox.showerror("错误", f"显示设置窗口失败: {str(e)}")


def call_amap_api(tool_name, **kwargs):
    """调用高德地图API的统一接口"""
    try:
        if tool_name == "driving_route":
            return amap_api.direction_driving(kwargs['origin'], kwargs['destination'])
        elif tool_name == "walking_route":
            return amap_api.direction_walking(kwargs['origin'], kwargs['destination'])
        elif tool_name == "distance_measurement":
            return amap_api.distance(kwargs['origin'], kwargs['destination'])
        elif tool_name == "regeocode":
            return amap_api.regeocode(kwargs['lng'], kwargs['lat'])
        elif tool_name == "weather":
            return amap_api.weather(kwargs['city'])
        else:
            return {'status': 'error', 'message': f'未知的工具名称: {tool_name}'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


def format_api_result(tool_name, result):
    """格式化API结果的统一接口"""
    if result['status'] != 'success':
        return f"查询失败: {result.get('message', '未知错误')}"
    
    try:
        if tool_name == "driving_route":
            return _format_driving_result(result)
        elif tool_name == "walking_route":
            return _format_walking_result(result)
        elif tool_name == "distance_measurement":
            return _format_distance_result(result)
        elif tool_name == "regeocode":
            return _format_regeocode_result(result)
        elif tool_name == "weather":
            return _format_weather_result(result)
        else:
            return f"未知的工具类型: {tool_name}"
    except Exception as e:
        return f"结果格式化失败: {str(e)}"


def _format_driving_result(result):
    """格式化驾车路径结果"""
    distance = result.get('distance', 0)
    duration = result.get('duration', 0)
    
    # 转换距离和时间
    distance_km = float(distance) / 1000
    duration_min = int(duration) // 60
    duration_hour = duration_min // 60
    duration_min = duration_min % 60
    
    result_text = f"🚗 驾车路径规划\n"
    result_text += f"📏 总距离: {distance_km:.2f} 公里\n"
    
    if duration_hour > 0:
        result_text += f"⏱️ 预计时间: {duration_hour}小时{duration_min}分钟\n"
    else:
        result_text += f"⏱️ 预计时间: {duration_min}分钟\n"
    
    return result_text


def _format_walking_result(result):
    """格式化步行路径结果"""
    distance = result.get('distance', 0)
    duration = result.get('duration', 0)
    
    # 转换距离和时间
    distance_km = float(distance) / 1000
    duration_min = int(duration) // 60
    
    result_text = f"🚶 步行路径规划\n"
    result_text += f"📏 总距离: {distance_km:.2f} 公里\n"
    result_text += f"⏱️ 预计时间: {duration_min}分钟\n"
    
    return result_text


def _format_distance_result(result):
    """格式化距离测量结果"""
    distance = result.get('distance', 0)
    distance_km = float(distance) / 1000
    
    result_text = f"📐 直线距离测量\n"
    result_text += f"📏 直线距离: {distance_km:.2f} 公里\n"
    
    return result_text


def _format_regeocode_result(result):
    """格式化逆地理编码结果"""
    province = result.get('province', '')
    city = result.get('city', '')
    district = result.get('district', '')
    formatted_address = result.get('formatted_address', '')
    
    result_text = f"📍 位置信息\n"
    result_text += f"🏛️ 省份: {province}\n"
    result_text += f"🏙️ 城市: {city}\n"
    result_text += f"🏘️ 区县: {district}\n"
    result_text += f"📮 详细地址: {formatted_address}\n"
    
    return result_text


def _format_weather_result(result):
    """格式化天气结果"""
    city = result.get('city', '')
    province = result.get('province', '')
    reporttime = result.get('reporttime', '')
    
    result_text = f"🌤️ {province} {city} 天气预报\n"
    result_text += f"🕐 更新时间: {reporttime}\n\n"
    
    casts = result.get('casts', [])
    for i, cast in enumerate(casts[:4]):
        date = cast.get('date', '')
        week = cast.get('week', '')
        dayweather = cast.get('dayweather', '')
        nightweather = cast.get('nightweather', '')
        daytemp = cast.get('daytemp', '')
        nighttemp = cast.get('nighttemp', '')
        
        day_label = "今天" if i == 0 else ("明天" if i == 1 else f"{date} {week}")
        result_text += f"📅 {day_label}\n"
        result_text += f"☀️ 白天: {dayweather} {daytemp}°C\n"
        result_text += f"🌙 夜间: {nightweather} {nighttemp}°C\n\n"
    
    return result_text