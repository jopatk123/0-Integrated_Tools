# -*- coding: utf-8 -*-
"""
个人配置文件
用于管理API密钥、个人偏好设置等
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置管理类"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'user_config.json')
        self.default_config = {
            # API配置 - 从环境变量获取
            'amap_api_key': os.getenv('AMAP_API_KEY', ''),  # 高德地图API密钥
            
            # 个人偏好设置
            'favorite_locations': [
                {'name': '家', 'lng': 119.3512459004, 'lat': 25.9990695670},
                {'name': '公司', 'lng': 119.3481015320, 'lat': 26.0031822025}
            ],
            
            # 常用城市
            'favorite_cities': ['北京', '上海', '广州', '深圳'],
            
            # 界面设置
            'ui_settings': {
                'window_size': '1000x700',
                'theme': 'default',
                'auto_save_results': True,
                'show_coordinate_conversion': True
            },
            
            # 缓存设置
            'cache_settings': {
                'enable_cache': True,
                'cache_duration_hours': 24,
                'max_cache_size_mb': 50
            },
            
            # 历史记录设置
            'history_settings': {
                'max_history_items': 100,
                'auto_clear_days': 30
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置，确保所有必要的键都存在
                return self._merge_config(self.default_config, config)
            except Exception as e:
                print(f"配置文件加载失败，使用默认配置: {e}")
                return self.default_config.copy()
        else:
            # 首次运行，创建默认配置文件
            self.save_config(self.default_config)
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """保存配置文件"""
        try:
            config_to_save = config or self.config
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"配置文件保存失败: {e}")
            return False
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置，确保用户配置包含所有默认键"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        return self.save_config()
    
    def get_amap_api_key(self) -> str:
        """获取高德地图API密钥"""
        # 优先从环境变量获取，其次从配置文件
        api_key = os.getenv('AMAP_API_KEY')
        if api_key:
            return api_key
        return self.get('amap_api_key', '')
    
    def set_amap_api_key(self, api_key: str) -> bool:
        """设置高德地图API密钥"""
        return self.set('amap_api_key', api_key)
    
    def get_favorite_locations(self) -> list:
        """获取收藏位置"""
        return self.get('favorite_locations', [])
    
    def add_favorite_location(self, name: str, lng: float, lat: float) -> bool:
        """添加收藏位置"""
        favorites = self.get_favorite_locations()
        # 检查是否已存在
        for loc in favorites:
            if loc['name'] == name:
                loc['lng'] = lng
                loc['lat'] = lat
                return self.set('favorite_locations', favorites)
        # 添加新位置
        favorites.append({'name': name, 'lng': lng, 'lat': lat})
        return self.set('favorite_locations', favorites)
    
    def remove_favorite_location(self, name: str) -> bool:
        """删除收藏位置"""
        favorites = self.get_favorite_locations()
        favorites = [loc for loc in favorites if loc['name'] != name]
        return self.set('favorite_locations', favorites)

# 全局配置实例
config = Config()