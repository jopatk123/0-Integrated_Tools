# -*- coding: utf-8 -*-
"""距离计算模块"""

import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    计算两个经纬度坐标点之间的距离（单位：米）
    使用Haversine公式计算球面距离
    
    Args:
        lat1 (float): 第一个点的纬度
        lon1 (float): 第一个点的经度
        lat2 (float): 第二个点的纬度
        lon2 (float): 第二个点的经度
        
    Returns:
        float: 两点之间的距离（米）
    """
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371000  # 地球半径（米）
    distance = r * c
    
    return distance

def haversine_distance_vectorized(lat1, lon1, lat2_array, lon2_array):
    """
    向量化的Haversine距离计算，一次计算一个点到多个点的距离
    
    Args:
        lat1 (float): 单个点的纬度
        lon1 (float): 单个点的经度
        lat2_array (numpy.ndarray): 多个点的纬度数组
        lon2_array (numpy.ndarray): 多个点的经度数组
        
    Returns:
        numpy.ndarray: 距离数组（米）
    """
    # 将经纬度转换为弧度
    lat1_rad = np.radians(lat1)
    lon1_rad = np.radians(lon1)
    lat2_rad = np.radians(lat2_array)
    lon2_rad = np.radians(lon2_array)
    
    # Haversine公式的向量化计算
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    r = 6371000  # 地球半径（米）
    distances = r * c
    
    return distances