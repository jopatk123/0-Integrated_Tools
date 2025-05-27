# -*- coding: utf-8 -*-
"""
高德地图API调用模块
提供真实的高德地图API调用功能
"""

import requests
import json
import time
from typing import Dict, Any, Optional, Tuple
from config import config

class AmapAPI:
    """高德地图API调用类"""
    
    def __init__(self):
        self.base_url = "https://restapi.amap.com/v3"
        self.api_key = config.get_amap_api_key()
        self.timeout = 10
        self.retry_times = 3
        self.retry_delay = 1
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
        config.set_amap_api_key(api_key)
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """发起API请求"""
        if not self.api_key:
            raise ValueError("请先设置高德地图API密钥")
        
        # 添加API密钥到参数
        params['key'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        for attempt in range(self.retry_times):
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                
                data = response.json()
                
                # 检查API响应状态
                if data.get('status') == '1':
                    return data
                else:
                    error_msg = data.get('info', '未知错误')
                    if attempt == self.retry_times - 1:
                        raise Exception(f"API调用失败: {error_msg}")
                    else:
                        time.sleep(self.retry_delay)
                        continue
                        
            except requests.exceptions.RequestException as e:
                if attempt == self.retry_times - 1:
                    raise Exception(f"网络请求失败: {str(e)}")
                else:
                    time.sleep(self.retry_delay)
                    continue
        
        return None
    
    def regeocode(self, lng: float, lat: float) -> Dict[str, Any]:
        """逆地理编码 - 坐标转地址"""
        params = {
            'location': f"{lng},{lat}",
            'poitype': '',
            'radius': 1000,
            'extensions': 'all',
            'batch': 'false',
            'roadlevel': 0
        }
        
        try:
            data = self._make_request('geocode/regeo', params)
            if data and 'regeocode' in data:
                regeocode = data['regeocode']
                formatted_address = regeocode.get('formatted_address', '')
                addressComponent = regeocode.get('addressComponent', {})
                
                return {
                    'status': 'success',
                    'formatted_address': formatted_address,
                    'province': addressComponent.get('province', ''),
                    'city': addressComponent.get('city', ''),
                    'district': addressComponent.get('district', ''),
                    'township': addressComponent.get('township', ''),
                    'street': addressComponent.get('streetNumber', {}).get('street', ''),
                    'number': addressComponent.get('streetNumber', {}).get('number', ''),
                    'adcode': addressComponent.get('adcode', ''),
                    'pois': regeocode.get('pois', [])[:5]  # 只取前5个POI
                }
            else:
                return {'status': 'error', 'message': '逆地理编码失败'}
                
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def geocode(self, address: str, city: str = '') -> Dict[str, Any]:
        """地理编码 - 地址转坐标"""
        params = {
            'address': address,
            'city': city
        }
        
        try:
            data = self._make_request('geocode/geo', params)
            if data and 'geocodes' in data and data['geocodes']:
                geocode = data['geocodes'][0]
                location = geocode.get('location', '').split(',')
                
                if len(location) == 2:
                    return {
                        'status': 'success',
                        'lng': float(location[0]),
                        'lat': float(location[1]),
                        'formatted_address': geocode.get('formatted_address', ''),
                        'province': geocode.get('province', ''),
                        'city': geocode.get('city', ''),
                        'district': geocode.get('district', ''),
                        'level': geocode.get('level', '')
                    }
            
            return {'status': 'error', 'message': '地理编码失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def direction_driving(self, origin: str, destination: str, waypoints: str = '') -> Dict[str, Any]:
        """驾车路径规划"""
        params = {
            'origin': origin,
            'destination': destination,
            'extensions': 'all',
            'strategy': 0,  # 速度优先
            'ferry': 1,
            'exclude': ''
        }
        
        if waypoints:
            params['waypoints'] = waypoints
        
        try:
            data = self._make_request('direction/driving', params)
            if data and 'route' in data:
                route = data['route']
                paths = route.get('paths', [])
                
                if paths:
                    path = paths[0]  # 取第一条路径
                    return {
                        'status': 'success',
                        'distance': int(path.get('distance', 0)),
                        'duration': int(path.get('duration', 0)),
                        'tolls': int(path.get('tolls', 0)),
                        'toll_distance': int(path.get('toll_distance', 0)),
                        'steps': self._format_driving_steps(path.get('steps', []))
                    }
            
            return {'status': 'error', 'message': '驾车路径规划失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def direction_walking(self, origin: str, destination: str) -> Dict[str, Any]:
        """步行路径规划"""
        params = {
            'origin': origin,
            'destination': destination,
            'extensions': 'all'
        }
        
        try:
            data = self._make_request('direction/walking', params)
            if data and 'route' in data:
                route = data['route']
                paths = route.get('paths', [])
                
                if paths:
                    path = paths[0]
                    return {
                        'status': 'success',
                        'distance': int(path.get('distance', 0)),
                        'duration': int(path.get('duration', 0)),
                        'steps': self._format_walking_steps(path.get('steps', []))
                    }
            
            return {'status': 'error', 'message': '步行路径规划失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def direction_transit(self, origin: str, destination: str, city: str, cityd: str = '') -> Dict[str, Any]:
        """公交路径规划"""
        params = {
            'origin': origin,
            'destination': destination,
            'city': city,
            'cityd': cityd or city,
            'extensions': 'all',
            'strategy': 0,
            'nightflag': 0,
            'date': '',
            'time': ''
        }
        
        try:
            data = self._make_request('direction/transit/integrated', params)
            if data and 'route' in data:
                route = data['route']
                transits = route.get('transits', [])
                
                if transits:
                    transit = transits[0]
                    return {
                        'status': 'success',
                        'distance': int(transit.get('distance', 0)),
                        'duration': int(transit.get('duration', 0)),
                        'cost': float(transit.get('cost', 0)),
                        'segments': self._format_transit_segments(transit.get('segments', []))
                    }
            
            return {'status': 'error', 'message': '公交路径规划失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def distance(self, origins: str, destination: str, distance_type: int = 1) -> Dict[str, Any]:
        """距离测量"""
        params = {
            'origins': origins,
            'destination': destination,
            'type': distance_type  # 1:驾车距离 0:直线距离 3:步行距离
        }
        
        try:
            data = self._make_request('distance', params)
            if data and 'results' in data:
                results = data['results']
                if results:
                    result = results[0]
                    return {
                        'status': 'success',
                        'distance': int(result.get('distance', 0)),
                        'duration': int(result.get('duration', 0))
                    }
            
            return {'status': 'error', 'message': '距离测量失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def weather(self, city: str) -> Dict[str, Any]:
        """天气查询"""
        params = {
            'city': city,
            'extensions': 'all'
        }
        
        try:
            data = self._make_request('weather/weatherInfo', params)
            if data and 'forecasts' in data:
                forecasts = data['forecasts']
                if forecasts:
                    forecast = forecasts[0]
                    return {
                        'status': 'success',
                        'city': forecast.get('city', ''),
                        'adcode': forecast.get('adcode', ''),
                        'province': forecast.get('province', ''),
                        'reporttime': forecast.get('reporttime', ''),
                        'casts': forecast.get('casts', [])
                    }
            
            return {'status': 'error', 'message': '天气查询失败'}
            
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def _format_driving_steps(self, steps: list) -> list:
        """格式化驾车路径步骤"""
        formatted_steps = []
        for step in steps[:10]:  # 只取前10步
            formatted_steps.append({
                'instruction': step.get('instruction', ''),
                'road': step.get('road', ''),
                'distance': int(step.get('distance', 0)),
                'duration': int(step.get('duration', 0)),
                'action': step.get('action', '')
            })
        return formatted_steps
    
    def _format_walking_steps(self, steps: list) -> list:
        """格式化步行路径步骤"""
        formatted_steps = []
        for step in steps[:10]:
            formatted_steps.append({
                'instruction': step.get('instruction', ''),
                'road': step.get('road', ''),
                'distance': int(step.get('distance', 0)),
                'duration': int(step.get('duration', 0))
            })
        return formatted_steps
    
    def _format_transit_segments(self, segments: list) -> list:
        """格式化公交路径段"""
        formatted_segments = []
        for segment in segments[:5]:
            walking = segment.get('walking', {})
            bus = segment.get('bus', {})
            
            formatted_segments.append({
                'walking': {
                    'distance': int(walking.get('distance', 0)),
                    'duration': int(walking.get('duration', 0))
                },
                'bus': {
                    'buslines': bus.get('buslines', [])[:3] if bus else []
                }
            })
        return formatted_segments
    
    def test_connection(self) -> Tuple[bool, str]:
        """测试API连接"""
        try:
            # 使用一个简单的逆地理编码请求测试连接
            result = self.regeocode(116.397428, 39.90923)
            if result['status'] == 'success':
                return True, "API连接正常"
            else:
                return False, f"API调用失败: {result['message']}"
        except Exception as e:
            return False, f"连接测试失败: {str(e)}"

# 全局API实例
amap_api = AmapAPI()