# -*- coding: utf-8 -*-
"""KML文件处理工具模块"""

import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import math

def create_kml_placemark(name, lon, lat, description=""):
    """创建KML点标记"""
    placemark = ET.Element("Placemark")
    ET.SubElement(placemark, "name").text = name
    if description:
        ET.SubElement(placemark, "description").text = description
    point = ET.SubElement(placemark, "Point")
    ET.SubElement(point, "coordinates").text = f"{lon},{lat},0"
    return placemark

def create_kml_circle_placemark(name, center_lon, center_lat, radius_meters, description=""):
    """创建圆形KML Placemark，使用Polygon近似圆形"""
    placemark = ET.Element("Placemark")
    ET.SubElement(placemark, "name").text = name
    if description:
        ET.SubElement(placemark, "description").text = description
    
    # 创建圆形的多边形近似（36个点）
    polygon = ET.SubElement(placemark, "Polygon")
    outer_boundary = ET.SubElement(polygon, "outerBoundaryIs")
    linear_ring = ET.SubElement(outer_boundary, "LinearRing")
    
    # 计算圆周上的点
    coordinates_list = []
    num_points = 36  # 圆周上的点数
    
    # 地球半径（米）
    earth_radius = 6378137.0
    
    for i in range(num_points + 1):  # +1 to close the polygon
        angle = 2 * math.pi * i / num_points
        
        # 计算相对于中心点的偏移（以度为单位）
        lat_offset = (radius_meters * math.cos(angle)) / earth_radius * (180 / math.pi)
        lon_offset = (radius_meters * math.sin(angle)) / (earth_radius * math.cos(math.radians(center_lat))) * (180 / math.pi)
        
        point_lat = center_lat + lat_offset
        point_lon = center_lon + lon_offset
        
        coordinates_list.append(f"{point_lon},{point_lat},0")
    
    coordinates_text = " ".join(coordinates_list)
    ET.SubElement(linear_ring, "coordinates").text = coordinates_text
    
    return placemark

def parse_kml_points(file_path):
    """解析KML文件中的点信息"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # 确定命名空间
        namespace = ''
        if '}' in root.tag:
            namespace = root.tag.split('}')[0] + '}'
        
        points = []
        placemark_query = f'.//{namespace}Placemark'
        
        for placemark in root.findall(placemark_query):
            # 获取名称
            name_elem = placemark.find(f'{namespace}name')
            if name_elem is None:
                name_elem = placemark.find(f'.//{namespace}name')
            name = name_elem.text.strip() if name_elem is not None and name_elem.text else "未命名点"
            
            # 获取坐标（只处理Point类型）
            point_elem = placemark.find(f'.//{namespace}Point')
            if point_elem is not None:
                coords_elem = point_elem.find(f'{namespace}coordinates')
                if coords_elem is None:
                    coords_elem = point_elem.find(f'.//{namespace}coordinates')
                
                if coords_elem is not None and coords_elem.text:
                    coords_text = coords_elem.text.strip()
                    try:
                        # 处理坐标格式：lon,lat,alt 或 lon,lat
                        coords_parts = coords_text.replace(',', ' ').split()
                        lon = float(coords_parts[0])
                        lat = float(coords_parts[1])
                        
                        # 获取描述
                        desc_elem = placemark.find(f'{namespace}description')
                        if desc_elem is None:
                            desc_elem = placemark.find(f'.//{namespace}description')
                        description = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                        
                        points.append({
                            'name': name,
                            'lon': lon,
                            'lat': lat,
                            'description': description
                        })
                    except (ValueError, IndexError):
                        continue
        
        return points, None
    except ET.ParseError as e:
        return [], f"KML文件解析错误: {e}"
    except Exception as e:
        return [], f"读取KML文件时发生错误: {e}"

def pretty_print_xml(xml_string):
    """格式化XML字符串"""
    parsed_string = parseString(xml_string)
    return parsed_string.toprettyxml(indent="  ")

def create_kml_document(points, title="地理空间数据"):
    """创建完整的KML文档"""
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")
    ET.SubElement(document, "name").text = title
    
    for point in points:
        placemark = create_kml_placemark(
            point.get('name', '未命名点'),
            point.get('lon', 0),
            point.get('lat', 0),
            point.get('description', '')
        )
        document.append(placemark)
    
    return kml