# -*- coding: utf-8 -*-
"""坐标转换工具模块"""

import math

# 坐标转换常量
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
    """WGS84坐标系转GCJ02坐标系（高德、谷歌中国等）"""
    if not (73.66 < lng_wgs < 135.05 and 3.86 < lat_wgs < 53.55):
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
    """GCJ02坐标系转WGS84坐标系"""
    if not (73.66 < lng_gcj < 135.05 and 3.86 < lat_gcj < 53.55):
        return lng_gcj, lat_gcj
    mglng, mglat = wgs84_to_gcj02(lng_gcj, lat_gcj)
    lng_wgs = lng_gcj * 2 - mglng
    lat_wgs = lat_gcj * 2 - mglat
    return lng_wgs, lat_wgs