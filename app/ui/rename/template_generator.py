# -*- coding: utf-8 -*-
"""重命名工具模板生成器"""

import pandas as pd
from tkinter import filedialog, messagebox

class TemplateGenerator:
    """Excel模板生成器"""
    
    @staticmethod
    def export_excel_template():
        """导出Excel重命名模版"""
        # 选择保存文件的位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")],
            title="选择模版保存位置"
        )
        
        if not file_path:
            return
            
        try:
            # 创建示例数据
            template_data = {
                '原路径': [
                    'C:\\示例文件夹\\原文件名1.txt',
                    'C:\\示例文件夹\\原文件名2.jpg',
                    'C:\\示例文件夹\\原文件名3.pdf'
                ],
                '新名称': [
                    '新文件名1.txt',
                    '新文件名2.jpg', 
                    '新文件名3.pdf'
                ],
                '路径文件是否存在': [
                    '',
                    '',
                    ''
                ]
            }
            
            # 创建DataFrame并导出到Excel
            df = pd.DataFrame(template_data)
            df.to_excel(file_path, index=False, engine='openpyxl')
            
            messagebox.showinfo("成功", f"Excel模版已导出到：{file_path}\n\n使用说明：\n1. 在'原路径'列填入要重命名的文件完整路径\n2. 在'新名称'列填入新的文件名（包含扩展名）\n3. 导入Excel后可点击'检测文件路径'按钮检查文件是否存在\n4. 保存后通过'导入Excel'按钮导入")
            
        except Exception as e:
            messagebox.showerror("错误", f"导出模版时出错: {str(e)}")