#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
高德地图API连接测试脚本
用于测试高德地图API服务是否能正常连接和响应
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.utils.amap_api import AmapAPI
from config import config
import time

def test_api_connection():
    """测试API连接"""
    print("=" * 50)
    print("高德地图API连接测试")
    print("=" * 50)
    
    # 初始化API
    amap = AmapAPI()
    
    # 检查API密钥
    api_key = config.get_amap_api_key()
    if not api_key:
        print("❌ 错误: 未配置高德地图API密钥")
        print("请在config.py中设置正确的API密钥")
        return False
    
    print(f"✓ API密钥已配置: {api_key[:8]}...{api_key[-8:]}")
    print()
    
    # 测试1: 逆地理编码（坐标转地址）
    print("测试1: 逆地理编码（坐标转地址）")
    print("-" * 30)
    test_lng, test_lat = 116.397428, 39.90923  # 北京天安门坐标
    print(f"测试坐标: 经度={test_lng}, 纬度={test_lat}")
    
    try:
        result = amap.regeocode(test_lng, test_lat)
        if result['status'] == 'success':
            print(f"✓ 逆地理编码成功")
            print(f"  地址: {result['formatted_address']}")
            print(f"  省份: {result['province']}")
            print(f"  城市: {result['city']}")
            print(f"  区县: {result['district']}")
        else:
            print(f"❌ 逆地理编码失败: {result['message']}")
            return False
    except Exception as e:
        print(f"❌ 逆地理编码异常: {str(e)}")
        return False
    
    print()
    
    # 测试2: 地理编码（地址转坐标）
    print("测试2: 地理编码（地址转坐标）")
    print("-" * 30)
    test_address = "北京市朝阳区阜通东大街6号"
    print(f"测试地址: {test_address}")
    
    try:
        result = amap.geocode(test_address, "北京")
        if result['status'] == 'success':
            print(f"✓ 地理编码成功")
            print(f"  坐标: 经度={result['lng']}, 纬度={result['lat']}")
            print(f"  标准地址: {result['formatted_address']}")
            print(f"  城市: {result['city']}")
        else:
            print(f"❌ 地理编码失败: {result['message']}")
            return False
    except Exception as e:
        print(f"❌ 地理编码异常: {str(e)}")
        return False
    
    print()
    
    # 测试3: 路径规划
    print("测试3: 驾车路径规划")
    print("-" * 30)
    origin = "116.397428,39.90923"  # 天安门
    destination = "116.3974,39.9093"  # 附近一点
    print(f"起点: {origin}")
    print(f"终点: {destination}")
    
    try:
        result = amap.direction_driving(origin, destination)
        if result['status'] == 'success':
            print(f"✓ 路径规划成功")
            print(f"  距离: {result['distance']}米")
            print(f"  预计时间: {result['duration']}秒")
            print(f"  路径数量: {len(result['paths'])}条")
        else:
            print(f"❌ 路径规划失败: {result['message']}")
            return False
    except Exception as e:
        print(f"❌ 路径规划异常: {str(e)}")
        return False
    
    return True

def test_api_performance():
    """测试API性能"""
    print()
    print("测试4: API响应性能")
    print("-" * 30)
    
    amap = AmapAPI()
    test_coordinates = [
        (116.397428, 39.90923),  # 北京
        (121.473701, 31.230416), # 上海
        (113.280637, 23.125178), # 广州
    ]
    
    total_time = 0
    success_count = 0
    
    for i, (lng, lat) in enumerate(test_coordinates, 1):
        start_time = time.time()
        try:
            result = amap.regeocode(lng, lat)
            end_time = time.time()
            response_time = end_time - start_time
            total_time += response_time
            
            if result['status'] == 'success':
                success_count += 1
                print(f"  请求{i}: ✓ 成功 ({response_time:.2f}秒) - {result['formatted_address'][:20]}...")
            else:
                print(f"  请求{i}: ❌ 失败 ({response_time:.2f}秒) - {result['message']}")
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            total_time += response_time
            print(f"  请求{i}: ❌ 异常 ({response_time:.2f}秒) - {str(e)}")
    
    avg_time = total_time / len(test_coordinates)
    success_rate = (success_count / len(test_coordinates)) * 100
    
    print(f"\n性能统计:")
    print(f"  平均响应时间: {avg_time:.2f}秒")
    print(f"  成功率: {success_rate:.1f}%")
    print(f"  总请求数: {len(test_coordinates)}")
    print(f"  成功数: {success_count}")

def main():
    """主函数"""
    try:
        # 基础功能测试
        if test_api_connection():
            print("\n🎉 所有基础测试通过！高德地图API服务连接正常")
            
            # 性能测试
            test_api_performance()
            
            print("\n" + "=" * 50)
            print("✅ 测试完成！高德地图API服务工作正常")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print("❌ 测试失败！请检查API配置和网络连接")
            print("=" * 50)
            return 1
            
    except KeyboardInterrupt:
        print("\n\n⚠️  测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n\n❌ 测试过程中发生未预期的错误: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)