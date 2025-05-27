# -*- coding: utf-8 -*-
"""
历史记录管理模块
用于保存和管理用户的查询历史
"""

import os
import json
import datetime
from typing import List, Dict, Any, Optional

class HistoryManager:
    """历史记录管理器"""
    
    def __init__(self, history_file: str = None):
        if history_file is None:
            self.history_file = os.path.join(os.path.dirname(__file__), '..', '..', 'user_history.json')
        else:
            self.history_file = history_file
        
        self.max_items = 100  # 最大历史记录数
        self.auto_clear_days = 30  # 自动清理天数
        
    def add_record(self, record_type: str, data: Dict[str, Any]) -> bool:
        """添加历史记录"""
        try:
            history = self._load_history()
            
            # 创建新记录
            new_record = {
                'id': self._generate_id(),
                'type': record_type,
                'timestamp': datetime.datetime.now().isoformat(),
                'data': data
            }
            
            # 添加到历史记录开头
            history.insert(0, new_record)
            
            # 限制记录数量
            if len(history) > self.max_items:
                history = history[:self.max_items]
            
            # 保存历史记录
            return self._save_history(history)
            
        except Exception as e:
            print(f"添加历史记录失败: {e}")
            return False
    
    def get_history(self, record_type: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """获取历史记录"""
        try:
            history = self._load_history()
            
            # 过滤记录类型
            if record_type:
                history = [record for record in history if record.get('type') == record_type]
            
            # 限制数量
            if limit:
                history = history[:limit]
            
            return history
            
        except Exception as e:
            print(f"获取历史记录失败: {e}")
            return []
    
    def delete_record(self, record_id: str) -> bool:
        """删除指定历史记录"""
        try:
            history = self._load_history()
            history = [record for record in history if record.get('id') != record_id]
            return self._save_history(history)
            
        except Exception as e:
            print(f"删除历史记录失败: {e}")
            return False
    
    def clear_history(self, record_type: str = None) -> bool:
        """清空历史记录"""
        try:
            if record_type:
                # 只清空指定类型的记录
                history = self._load_history()
                history = [record for record in history if record.get('type') != record_type]
                return self._save_history(history)
            else:
                # 清空所有记录
                return self._save_history([])
                
        except Exception as e:
            print(f"清空历史记录失败: {e}")
            return False
    
    def auto_cleanup(self) -> bool:
        """自动清理过期记录"""
        try:
            history = self._load_history()
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=self.auto_clear_days)
            
            # 过滤掉过期记录
            filtered_history = []
            for record in history:
                try:
                    record_date = datetime.datetime.fromisoformat(record.get('timestamp', ''))
                    if record_date >= cutoff_date:
                        filtered_history.append(record)
                except:
                    # 如果时间戳解析失败，保留记录
                    filtered_history.append(record)
            
            return self._save_history(filtered_history)
            
        except Exception as e:
            print(f"自动清理历史记录失败: {e}")
            return False
    
    def get_recent_locations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """获取最近使用的位置"""
        history = self.get_history('route_planning', limit * 2)  # 获取更多记录以便筛选
        locations = []
        seen_locations = set()
        
        for record in history:
            data = record.get('data', {})
            origin = data.get('origin')
            destination = data.get('destination')
            
            for loc in [origin, destination]:
                if loc and loc not in seen_locations:
                    try:
                        lng, lat = map(float, loc.split(','))
                        locations.append({
                            'coordinates': loc,
                            'lng': lng,
                            'lat': lat,
                            'last_used': record.get('timestamp')
                        })
                        seen_locations.add(loc)
                        if len(locations) >= limit:
                            break
                    except (ValueError, AttributeError):
                        # 忽略无效的坐标格式
                        continue
            
            if len(locations) >= limit:
                break
        
        return locations
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取使用统计"""
        try:
            history = self._load_history()
            
            stats = {
                'total_records': len(history),
                'by_type': {},
                'by_date': {},
                'most_recent': None,
                'oldest': None
            }
            
            if not history:
                return stats
            
            # 按类型统计
            for record in history:
                record_type = record.get('type', 'unknown')
                stats['by_type'][record_type] = stats['by_type'].get(record_type, 0) + 1
            
            # 按日期统计
            for record in history:
                try:
                    timestamp = record.get('timestamp', '')
                    date = datetime.datetime.fromisoformat(timestamp).date().isoformat()
                    stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
                except:
                    pass
            
            # 最新和最旧记录
            stats['most_recent'] = history[0].get('timestamp') if history else None
            stats['oldest'] = history[-1].get('timestamp') if history else None
            
            return stats
            
        except Exception as e:
            print(f"获取统计信息失败: {e}")
            return {'total_records': 0, 'by_type': {}, 'by_date': {}}
    
    def _load_history(self) -> List[Dict[str, Any]]:
        """加载历史记录文件"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"历史记录文件加载失败: {e}")
                return []
        return []
    
    def _save_history(self, history: List[Dict[str, Any]]) -> bool:
        """保存历史记录文件"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"历史记录文件保存失败: {e}")
            return False
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return str(uuid.uuid4())[:8]

# 全局历史记录管理器实例
history_manager = HistoryManager()