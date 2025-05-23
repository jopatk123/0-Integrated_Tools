import os
import shutil
import datetime
import fnmatch

class FileOperations:
    @staticmethod
    def get_file_info(file_path):
        """获取文件信息"""
        try:
            file_size = os.path.getsize(file_path)
            modified_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
            # 将文件大小转换为MB单位
            if file_size >= 1024 * 1024:  # 大于等于1MB
                size_str = f"{file_size/(1024*1024):.2f} MB"
            else:  # 小于1MB
                size_str = f"{file_size/1024:.2f} KB"
            return {
                "size": size_str,
                "modified": modified_time
            }
        except (OSError, PermissionError) as e:
            print(f"无法访问文件 {file_path}: {e}")
            return {
                "size": "未知",
                "modified": "未知"
            }
    
    @staticmethod
    def scan_files(folder_path, filter_pattern="*.*", include_subfolders=True):
        """扫描文件夹中的文件"""
        result = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                if not include_subfolders and root != folder_path:
                    continue
                    
                for file in files:
                    # 使用通配符匹配
                    if fnmatch.fnmatch(file, filter_pattern):
                        file_path = os.path.join(root, file)
                        try:
                            info = FileOperations.get_file_info(file_path)
                            result.append({
                                "path": file_path,
                                "size": info["size"],
                                "modified": info["modified"]
                            })
                        except Exception as e:
                            print(f"处理文件时出错 {file_path}: {e}")
        except Exception as e:
            print(f"扫描文件夹时出错: {e}")
            
        return result
    
    @staticmethod
    def scan_folders(folder_path, include_subfolders=True):
        """扫描文件夹中的子文件夹"""
        result = []
        
        try:
            for root, dirs, files in os.walk(folder_path):
                if not include_subfolders and root != folder_path:
                    continue
                    
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    try:
                        modified_time = datetime.datetime.fromtimestamp(
                            os.path.getmtime(dir_path)).strftime("%Y-%m-%d %H:%M:%S")
                        
                        result.append({
                            "path": dir_path,
                            "size": "<DIR>",
                            "modified": modified_time
                        })
                    except Exception as e:
                        print(f"处理文件夹时出错 {dir_path}: {e}")
        except Exception as e:
            print(f"扫描文件夹时出错: {e}")
            
        return result
    
    @staticmethod
    def delete_item(path):
        """删除文件或文件夹"""
        try:
            if os.path.isfile(path):
                os.remove(path)
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return True
            return False
        except Exception as e:
            print(f"删除失败 {path}: {e}")
            return False
            
    @staticmethod
    def delete_to_recycle_bin(path):
        """删除文件或文件夹到回收站"""
        try:
            import send2trash
            send2trash.send2trash(path)
            return True
        except ImportError:
            print("未安装send2trash模块，请使用pip install send2trash安装")
            return False
        except Exception as e:
            print(f"删除到回收站失败 {path}: {e}")
            return False
    
    @staticmethod
    def rename_file(original_path, new_name):
        """重命名文件"""
        try:
            if os.path.exists(original_path):
                new_path = os.path.join(os.path.dirname(original_path), new_name)
                os.rename(original_path, new_path)
                return True, ""
            else:
                return False, f"文件不存在: {original_path}"
        except Exception as e:
            return False, f"重命名失败 {original_path}: {str(e)}"