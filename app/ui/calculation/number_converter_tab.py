# -*- coding: utf-8 -*-
"""数字转换器功能模块"""

import tkinter as tk
from tkinter import ttk, messagebox
import re

class NumberConverterTab:
    """数字转换器功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.update_status = None  # 状态更新回调函数
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 小写转大写主框架
        conv_main_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        conv_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(conv_main_frame, text="数字小写转大写", 
                              font=("Microsoft YaHei", 18, "bold"),
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack(pady=(0, 20))
        
        # 使用说明
        instruction_frame = tk.Frame(conv_main_frame, bg=self.theme.bg_color)
        instruction_frame.pack(fill=tk.X, pady=(0, 20))
        
        instruction_text = (
            "功能说明：\n"
            "• 支持整数和小数（最多两位小数）\n"
            "• 自动处理零的读法\n"
            "• 符合中文数字表达习惯\n"
            "• 适用于财务、合同等正式文档"
        )
        instruction_label = tk.Label(instruction_frame, text=instruction_text, 
                                  bg=self.theme.bg_color, fg=self.theme.text_color,
                                  justify=tk.LEFT, font=("Microsoft YaHei", 10))
        instruction_label.pack(anchor="w")
        
        # 输入框架
        input_frame = tk.Frame(conv_main_frame, bg=self.theme.bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(input_frame, text="请输入数字金额:", 
                font=("Microsoft YaHei", 12),
                bg=self.theme.bg_color, fg=self.theme.text_color).pack(anchor="w")
        
        self.amount_var = tk.StringVar()
        amount_entry = tk.Entry(input_frame, textvariable=self.amount_var, 
                               font=("Microsoft YaHei", 14), bd=2, relief="sunken")
        amount_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # 绑定回车键
        amount_entry.bind('<Return>', lambda e: self.convert_to_chinese())
        
        # 按钮框架
        button_frame = tk.Frame(conv_main_frame, bg=self.theme.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        convert_btn = tk.Button(button_frame, text="转换", 
                               command=self.convert_to_chinese,
                               bg="#4CAF50", fg="white", activebackground="#45A049",
                               font=("Microsoft YaHei", 12, "bold"),
                               relief="raised", bd=3, cursor="hand2")
        convert_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=15, ipady=5)
        
        clear_btn = tk.Button(button_frame, text="清空", 
                             command=self.clear_converter,
                             bg="#F44336", fg="white", activebackground="#DA190B",
                             font=("Microsoft YaHei", 12, "bold"),
                             relief="raised", bd=3, cursor="hand2")
        clear_btn.pack(side=tk.LEFT, ipadx=15, ipady=5)
        
        # 示例按钮
        example_btn = tk.Button(button_frame, text="示例", 
                               command=self.show_examples,
                               bg="#2196F3", fg="white", activebackground="#1976D2",
                               font=("Microsoft YaHei", 12, "bold"),
                               relief="raised", bd=3, cursor="hand2")
        example_btn.pack(side=tk.LEFT, padx=(10, 0), ipadx=15, ipady=5)
        
        # 结果显示框架
        result_frame = tk.Frame(conv_main_frame, bg=self.theme.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(result_frame, text="转换结果:", 
                font=("Microsoft YaHei", 12),
                bg=self.theme.bg_color, fg=self.theme.text_color).pack(anchor="w")
        
        # 创建结果文本框和滚动条的容器
        text_container = tk.Frame(result_frame, bg=self.theme.bg_color)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.result_text = tk.Text(text_container, height=10, font=("Microsoft YaHei", 12),
                                  bg="#F8F9FA", fg="#212529", wrap=tk.WORD,
                                  bd=2, relief="sunken")
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = tk.Scrollbar(text_container, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def convert_to_chinese(self):
        """转换为中文大写"""
        try:
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                messagebox.showwarning("警告", "请输入金额")
                return
                
            # 验证输入格式
            if not re.match(r'^\d+(\.\d{1,2})?$', amount_str):
                messagebox.showerror("错误", "请输入有效的金额格式（最多两位小数）")
                return
                
            amount = float(amount_str)
            if amount >= 1000000000000:  # 万亿
                messagebox.showerror("错误", "金额过大，请输入小于1万亿的金额")
                return
                
            chinese_amount = self.number_to_chinese(amount)
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"输入金额: {amount_str}元\n\n")
            self.result_text.insert(tk.END, f"大写金额: {chinese_amount}\n\n")
            
            # 添加格式化显示
            self.result_text.insert(tk.END, "格式化显示:\n")
            self.result_text.insert(tk.END, f"￥{amount_str}\n")
            self.result_text.insert(tk.END, f"{chinese_amount}\n\n")
            
            # 更新状态
            if self.update_status:
                self.update_status(f"成功转换金额: {amount_str}元")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            
    def number_to_chinese(self, amount):
        """将数字转换为中文大写"""
        # 中文数字映射
        chinese_nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        chinese_units = ['', '拾', '佰', '仟']
        chinese_big_units = ['', '万', '亿']
        
        if amount == 0:
            return "人民币零元整"
            
        # 分离整数和小数部分
        integer_part = int(amount)
        decimal_part = round((amount - integer_part) * 100)
        
        result = "人民币"
        
        # 处理整数部分
        if integer_part == 0:
            result += "零元"
        else:
            result += self.convert_integer_part(integer_part, chinese_nums, chinese_units, chinese_big_units) + "元"
            
        # 处理小数部分
        if decimal_part == 0:
            result += "整"
        else:
            jiao = decimal_part // 10
            fen = decimal_part % 10
            
            if jiao > 0:
                result += chinese_nums[jiao] + "角"
            if fen > 0:
                result += chinese_nums[fen] + "分"
                
        return result
        
    def convert_integer_part(self, num, chinese_nums, chinese_units, chinese_big_units):
        """转换整数部分"""
        if num == 0:
            return ""
            
        result = ""
        unit_index = 0
        
        while num > 0:
            section = num % 10000
            if section > 0:
                section_str = self.convert_section(section, chinese_nums, chinese_units)
                if unit_index > 0:
                    section_str += chinese_big_units[unit_index]
                result = section_str + result
                
                # 处理零的情况
                if num > 10000 and section < 1000:
                    result = "零" + result
                    
            num //= 10000
            unit_index += 1
            
        return result
        
    def convert_section(self, num, chinese_nums, chinese_units):
        """转换四位数段"""
        if num == 0:
            return ""
            
        result = ""
        zero_flag = False
        
        for i in range(4):
            digit = num % 10
            if digit > 0:
                if zero_flag:
                    result = "零" + result
                    zero_flag = False
                result = chinese_nums[digit] + chinese_units[i] + result
            elif len(result) > 0:
                zero_flag = True
                
            num //= 10
            
        return result
        
    def clear_converter(self):
        """清空转换器"""
        self.amount_var.set("")
        self.result_text.delete(1.0, tk.END)
        if self.update_status:
            self.update_status("已清空转换器")
            
    def show_examples(self):
        """显示示例"""
        examples = [
            ("123.45", "人民币壹佰贰拾叁元肆角伍分"),
            ("1000", "人民币壹仟元整"),
            ("10000.50", "人民币壹万元伍角"),
            ("100000", "人民币拾万元整"),
            ("1234567.89", "人民币壹佰贰拾叁万肆仟伍佰陆拾柒元捌角玖分")
        ]
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "转换示例:\n\n")
        
        for amount, chinese in examples:
            self.result_text.insert(tk.END, f"输入: {amount}元\n")
            self.result_text.insert(tk.END, f"输出: {chinese}\n\n")
            
        self.result_text.insert(tk.END, "使用说明:\n")
        self.result_text.insert(tk.END, "• 支持整数和小数（最多两位小数）\n")
        self.result_text.insert(tk.END, "• 自动处理零的读法\n")
        self.result_text.insert(tk.END, "• 符合中文数字表达习惯\n")
        self.result_text.insert(tk.END, "• 适用于财务、合同等正式文档\n")
        
        if self.update_status:
            self.update_status("已显示转换示例")