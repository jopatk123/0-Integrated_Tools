# -*- coding: utf-8 -*-
"""高德地图API调用模块"""

import requests
import json
import requests.utils
from .coordinate_utils import wgs84_to_gcj02, gcj02_to_wgs84

def get_address_from_amap(lon_wgs, lat_wgs, api_key):
    """使用高德逆地理编码API获取地址信息 (输入WGS-84, API使用GCJ-02)"""
    if not api_key:
        return "错误：请在配置中设置您的高德API Key"
    
    lon_gcj, lat_gcj = wgs84_to_gcj02(lon_wgs, lat_wgs)
    url = f"https://restapi.amap.com/v3/geocode/regeo?output=json&location={lon_gcj},{lat_gcj}&key={api_key}&radius=1000&extensions=base"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "1" and data.get("regeocode"):
            return data["regeocode"].get("formatted_address", "地址未找到")
        else:
            return f"高德API错误: {data.get('info', '未知错误')}"
    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {e}"
    except json.JSONDecodeError:
        return "解析高德API响应失败"

def get_coords_from_amap(address, city, api_key):
    """使用高德地理编码API获取经纬度信息 (返回WGS-84)"""
    if not api_key:
        return "错误：请在配置中设置您的高德API Key", None, None
    
    url = f"https://restapi.amap.com/v3/geocode/geo?address={requests.utils.quote(address)}&city={requests.utils.quote(city)}&output=json&key={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("status") == "1" and data.get("geocodes"):
            location_gcj_str = data["geocodes"][0].get("location")
            if location_gcj_str:
                lon_gcj_str, lat_gcj_str = location_gcj_str.split(',')
                lon_wgs, lat_wgs = gcj02_to_wgs84(float(lon_gcj_str), float(lat_gcj_str))
                return None, lon_wgs, lat_wgs
            else:
                return "未找到经纬度", None, None
        else:
            return f"高德API错误: {data.get('info', '未知错误')}", None, None
    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {e}", None, None
    except (json.JSONDecodeError, IndexError):
        return "解析高德API响应或数据格式错误", None, None

def search_nearby_pois_amap(lon_wgs, lat_wgs, radius_meters, search_keywords, search_types="", api_key=None):
    """使用高德周边搜索API查找POI (输入WGS-84, API使用GCJ-02, 输出WGS-84)"""
    if not api_key:
        return "错误：请在配置中设置您的高德API Key", []
    
    lon_gcj, lat_gcj = wgs84_to_gcj02(lon_wgs, lat_wgs)

    url_params = {
        "key": api_key,
        "location": f"{lon_gcj},{lat_gcj}",
        "keywords": search_keywords,
        "radius": str(radius_meters),
        "offset": "25",
        "page": "1",
        "output": "json"
    }
    if search_types:
        url_params["types"] = search_types
    
    base_url = "https://restapi.amap.com/v3/place/around"
    query_string_parts = []
    for k, v in url_params.items():
        if v:
            query_string_parts.append(f"{k}={requests.utils.quote(str(v))}")

    url = f"{base_url}?{'&'.join(query_string_parts)}"
    
    pois = []
    response_text = "N/A"
    try:
        response = requests.get(url, timeout=10)
        response_text = response.text
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "1":
            if "pois" in data and data["pois"]:
                for poi_data in data["pois"]:
                    name = poi_data.get("name")
                    location_gcj_str = poi_data.get("location")
                    if name and location_gcj_str:
                        gcj_lon_str, gcj_lat_str = location_gcj_str.split(',')
                        wgs_lon, wgs_lat = gcj02_to_wgs84(float(gcj_lon_str), float(gcj_lat_str))
                        pois.append({
                            "name": name,
                            "wgs84_lon": wgs_lon,
                            "wgs84_lat": wgs_lat,
                            "gcj02_location_from_amap": location_gcj_str
                        })
                return None, pois
            else:
                return "未找到符合条件的POI", [] 
        else:
            return f"高德API错误: {data.get('info', '未知错误')} (infocode: {data.get('infocode')})", []
            
    except requests.exceptions.RequestException as e:
        return f"网络请求错误: {e}", []
    except json.JSONDecodeError:
        return f"解析高德API响应失败. URL: {url}, Response: {response_text}", []
    except Exception as e:
        return f"处理POI数据时发生未知错误: {e}", []