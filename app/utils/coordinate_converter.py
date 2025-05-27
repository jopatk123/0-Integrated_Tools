# -*- coding: utf-8 -*-
"""
坐标转换工具模块
支持WGS-84和GCJ-02坐标系之间的转换
"""

import math

# 坐标转换相关常数
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def _transform_lat(lng, lat):
    """纬度转换辅助函数"""
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret

def _transform_lng(lng, lat):
    """经度转换辅助函数"""
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

def wgs84_to_gcj02(lng_wgs, lat_wgs):
    """WGS84坐标系转GCJ02坐标系（高德、谷歌中国等）
    
    Args:
        lng_wgs (float): WGS84经度
        lat_wgs (float): WGS84纬度
        
    Returns:
        tuple: (GCJ02经度, GCJ02纬度)
    """
    if not (73.66 < lng_wgs < 135.05 and 3.86 < lat_wgs < 53.55):
        # 坐标超出中国范围，不进行转换
        return lng_wgs, lat_wgs
        
    dlat = _transform_lat(lng_wgs - 105.0, lat_wgs - 35.0)
    dlng = _transform_lng(lng_wgs - 105.0, lat_wgs - 35.0)
    radlat = lat_wgs / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat_wgs + dlat
    mglng = lng_wgs + dlng
    return mglng, mglat

def gcj02_to_wgs84(lng_gcj, lat_gcj):
    """GCJ02坐标系转WGS84坐标系
    
    Args:
        lng_gcj (float): GCJ02经度
        lat_gcj (float): GCJ02纬度
        
    Returns:
        tuple: (WGS84经度, WGS84纬度)
    """
    if not (73.66 < lng_gcj < 135.05 and 3.86 < lat_gcj < 53.55):
        # 坐标超出中国范围，不进行转换
        return lng_gcj, lat_gcj
        
    # 使用迭代方法进行更精确的转换
    mglng, mglat = wgs84_to_gcj02(lng_gcj, lat_gcj)
    lng_wgs = lng_gcj * 2 - mglng
    lat_wgs = lat_gcj * 2 - mglat
    return lng_wgs, lat_wgs

def is_in_china(lng, lat):
    """判断坐标是否在中国境内
    
    Args:
        lng (float): 经度
        lat (float): 纬度
        
    Returns:
        bool: 是否在中国境内
    """
    return 73.66 < lng < 135.05 and 3.86 < lat < 53.55

def convert_coordinates(lng, lat, from_system='WGS84', to_system='GCJ02'):
    """通用坐标转换函数
    
    Args:
        lng (float): 经度
        lat (float): 纬度
        from_system (str): 源坐标系 ('WGS84' 或 'GCJ02')
        to_system (str): 目标坐标系 ('WGS84' 或 'GCJ02')
        
    Returns:
        tuple: (转换后经度, 转换后纬度)
    """
    if from_system == to_system:
        return lng, lat
        
    if from_system == 'WGS84' and to_system == 'GCJ02':
        return wgs84_to_gcj02(lng, lat)
    elif from_system == 'GCJ02' and to_system == 'WGS84':
        return gcj02_to_wgs84(lng, lat)
    else:
        raise ValueError(f"不支持的坐标系转换: {from_system} -> {to_system}")

def calculate_distance(lng1, lat1, lng2, lat2):
    """计算两个经纬度点之间的直线距离（球面距离）
    使用Haversine公式计算地球表面两点间的最短距离
    
    Args:
        lng1 (float): 起点经度
        lat1 (float): 起点纬度
        lng2 (float): 终点经度
        lat2 (float): 终点纬度
        
    Returns:
        float: 距离（单位：米）
    """
    # 地球半径（米）
    R = 6371000
    
    # 将角度转换为弧度
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lng = math.radians(lng2 - lng1)
    
    # Haversine公式
    a = (math.sin(delta_lat / 2) * math.sin(delta_lat / 2) +
         math.cos(lat1_rad) * math.cos(lat2_rad) *
         math.sin(delta_lng / 2) * math.sin(delta_lng / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # 计算距离
    distance = R * c
    return distance