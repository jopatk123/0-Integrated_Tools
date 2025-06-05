# -*- coding: utf-8 -*-
"""计算器功能模块"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class CalculatorTab:
    """计算器功能选项卡"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.update_status = None  # 状态更新回调函数
        
        # 计算器状态
        self.current_input = ""
        self.result = 0
        self.operation = None
        self.new_input = True
        self.calculation_history = []
        
        # 创建界面组件
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 计算器主框架
        calc_main_frame = tk.Frame(self.parent_frame, bg=self.theme.bg_color)
        calc_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建左右两个子框架，调整比例分配
        left_frame = tk.Frame(calc_main_frame, bg=self.theme.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # 右侧历史框架，固定宽度，减少空间占用
        right_frame = tk.Frame(calc_main_frame, bg=self.theme.bg_color, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        right_frame.pack_propagate(False)  # 防止子组件改变框架大小
        
        # 左侧：显示屏和按钮
        self.create_display(left_frame)
        self.create_buttons(left_frame)
        
        # 右侧：计算历史
        self.create_history(right_frame)
        
    def create_display(self, parent):
        """创建显示屏"""
        # 显示屏
        self.display_var = tk.StringVar(value="0")
        display_frame = tk.Frame(parent, bg=self.theme.bg_color)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        display_entry = tk.Entry(display_frame, textvariable=self.display_var, 
                                font=("Microsoft YaHei", 16, "bold"), justify="right", state="readonly",
                                bg="#2C2C2C", fg="#00FF00", bd=3, relief="sunken")
        display_entry.pack(fill=tk.X, ipady=10)
        
        # 粘贴按钮
        paste_btn = tk.Button(parent, text="粘贴", font=("Microsoft YaHei", 9),
                             command=self.paste_from_clipboard, bg="#9C27B0", fg="white",
                             activebackground="#7B1FA2", relief="raised", bd=2, cursor="hand2")
        paste_btn.pack(fill=tk.X, pady=(0, 10), ipadx=8, ipady=2)
        
    def create_buttons(self, parent):
        """创建按钮"""
        # 按钮框架
        self.buttons_frame = tk.Frame(parent, bg=self.theme.bg_color)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # 优化第一行按钮布局
        first_row_buttons = [
            ('√', 'sqrt'), ('x^y', '^'), ('+/-', 'sign'), ('税率', 'tax')
        ]

        for i, (text, cmd) in enumerate(first_row_buttons):
            if cmd == 'tax':
                bg_color = "#607D8B" # 税率用深灰色
                active_bg = "#455A64"
            elif cmd in ['sign']:
                 bg_color = "#F44336"  # 红色
                 active_bg = "#D32F2F"
            else:
                bg_color = "#FF9800"  # 橙色
                active_bg = "#F57C00"

            btn = tk.Button(self.buttons_frame, text=text, font=("Microsoft YaHei", 10, "bold"),
                           command=lambda c=cmd: self.button_click(c),
                           bg=bg_color, fg="white", activebackground=active_bg,
                           relief="raised", bd=2, cursor="hand2")
            btn.grid(row=0, column=i, sticky="nsew", padx=2, pady=2, ipadx=8, ipady=8)
        
        # 第二行：←, C (优化布局)
        row2_buttons = [
            ('←', 'backspace'), ('C', 'clear')
        ]
        
        for i, (text, cmd) in enumerate(row2_buttons):
            bg_color = "#F44336"  # 红色
            active_bg = "#D32F2F"
            
            btn = tk.Button(self.buttons_frame, text=text, font=("Microsoft YaHei", 11, "bold"),
                           command=lambda c=cmd: self.button_click(c),
                           bg=bg_color, fg="white", activebackground=active_bg,
                           relief="raised", bd=2, cursor="hand2")
            # 让这两个按钮各占两列，填满一行
            btn.grid(row=1, column=i*2, columnspan=2, sticky="nsew", padx=2, pady=2, ipadx=8, ipady=10)
        
        # 数字和基本运算按钮 (优化布局和间距)
        number_buttons = [
            [('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/')],
            [('4', '4'), ('5', '5'), ('6', '6'), ('×', '*')],
            [('1', '1'), ('2', '2'), ('3', '3'), ('-', '-')],
            [('0', '0'), ('.', '.'), ('=', '='), ('+', '+')]
        ]
        
        for row_idx, row in enumerate(number_buttons, start=2):
            for col_idx, (text, cmd) in enumerate(row):
                if text.isdigit() or text == '.':
                    bg_color = "#2196F3"  # 蓝色数字
                    active_bg = "#1976D2"
                    font_size = 14
                elif text == '=':
                    bg_color = "#4CAF50"  # 绿色等号
                    active_bg = "#388E3C"
                    font_size = 14
                else:
                    bg_color = "#9C27B0"  # 紫色运算符
                    active_bg = "#7B1FA2"
                    font_size = 13
                
                if text == '0':
                    btn = tk.Button(self.buttons_frame, text=text, font=("Microsoft YaHei", font_size, "bold"),
                                   command=lambda c=cmd: self.button_click(c),
                                   bg=bg_color, fg="white", activebackground=active_bg,
                                   relief="raised", bd=2, cursor="hand2", anchor=tk.CENTER)
                    btn.grid(row=row_idx, column=col_idx, columnspan=2, sticky="nsew", padx=2, pady=2, ipadx=8, ipady=12)
                else:
                    btn = tk.Button(self.buttons_frame, text=text, font=("Microsoft YaHei", font_size, "bold"),
                                   command=lambda c=cmd: self.button_click(c),
                                   bg=bg_color, fg="white", activebackground=active_bg,
                                   relief="raised", bd=2, cursor="hand2")
                    btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2, ipadx=8, ipady=12)
        
        # 配置按钮网格权重，优化比例
        for i in range(6): # 6行按钮
            self.buttons_frame.grid_rowconfigure(i, weight=1, minsize=50)
        for j in range(4): # 4列按钮
            self.buttons_frame.grid_columnconfigure(j, weight=1, minsize=60)
            
    def create_history(self, parent):
        """创建历史记录区域"""
        # 右侧：计算历史 - 优化布局
        history_label = tk.Label(parent, text="计算历史", font=("Microsoft YaHei", 11, "bold"),
                                bg=self.theme.bg_color, fg=self.theme.text_color)
        history_label.pack(pady=(0, 8))
        
        # 创建历史记录框架，添加滚动条
        history_container = tk.Frame(parent, bg=self.theme.bg_color)
        history_container.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(history_container, font=("Microsoft YaHei", 9),
                                   bg="#F8F9FA", fg="#495057", relief="sunken", bd=1, 
                                   wrap=tk.WORD, width=25, height=15)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 添加滚动条
        history_scrollbar = tk.Scrollbar(history_container, command=self.history_text.yview)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=history_scrollbar.set)
        
        self.history_text.config(state=tk.DISABLED) # 初始设为不可编辑
        
        # 添加清除历史按钮
        clear_history_btn = tk.Button(parent, text="清除历史", font=("Microsoft YaHei", 9),
                                     command=self.clear_history_only, bg="#6C757D", fg="white",
                                     activebackground="#5A6268", relief="raised", bd=1, cursor="hand2")
        clear_history_btn.pack(pady=(8, 0), ipadx=5, ipady=2)
        
    def button_click(self, char):
        """处理按钮点击事件"""
        if char.isdigit() or char == '.':
            self.input_number(char)
        elif char in ['+', '-', '×', '÷', '*', '/']:
            self.input_operator(char)
        elif char == '=':
            self.calculate()
        elif char == 'clear':
            self.clear_all()
        elif char == 'backspace':
            self.backspace()
        elif char == 'sign':
            self.toggle_sign()
        elif char == 'sqrt':
            self.calculate_sqrt()
        elif char == '^':
            self.input_operator('**')
        elif char == 'tax':
            self.tax_calculator()
              
    def input_number(self, char):
        """输入数字"""
        if self.new_input:
            self.current_input = char
            self.new_input = False
        else:
            if char == '.' and '.' in self.current_input:
                return
            self.current_input += char
        self.display_var.set(self.current_input)
        
    def input_operator(self, op):
        """输入运算符"""
        if self.current_input:
            if self.operation and not self.new_input:
                self.calculate()
            # 修改：支持连续计算，使用当前显示的值作为基础
            self.result = float(self.current_input)
            self.operation = op
            self.new_input = True
            
    def calculate(self):
        """执行计算 - 支持连续计算"""
        try:
            if self.operation and self.current_input:
                current_value = float(self.current_input)
                old_result = self.result
                
                if self.operation == '+':
                    self.result = self.result + current_value
                elif self.operation == '-':
                    self.result = self.result - current_value
                elif self.operation == '×' or self.operation == '*':
                    self.result = self.result * current_value
                elif self.operation == '÷' or self.operation == '/':
                    if current_value != 0:
                        self.result = self.result / current_value
                    else:
                        self.display_var.set("错误")
                        return
                elif self.operation == '**':
                    self.result = self.result ** current_value
                
                # 记录计算历史
                history_entry = f"{old_result} {self.operation} {current_value} = {self.result}"
                self.add_to_history(history_entry)
                
                self.display_var.set(str(self.result))
                # 修改：保持当前结果作为下次计算的基础，支持连续计算
                self.current_input = str(self.result)
                self.operation = None
                self.new_input = True
        except Exception as e:
            self.display_var.set("错误")
            self.current_input = ""
            self.operation = None
            self.new_input = True
    
    def add_to_history(self, entry):
        """添加计算历史记录到右侧文本框"""
        self.calculation_history.append(entry)
        # 更新历史显示
        self.history_text.config(state=tk.NORMAL) # 允许编辑
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END) # 滚动到底部
        self.history_text.config(state=tk.DISABLED) # 禁止编辑
    
    def paste_from_clipboard(self):
        """从剪贴板粘贴数值"""
        try:
            # 获取剪贴板内容
            clipboard_content = self.parent_frame.clipboard_get()
            
            # 尝试将内容转换为数字
            try:
                number = float(clipboard_content.strip())
                # 清除当前输入并设置新值
                self.clear_all()
                self.current_input = str(number)
                self.display_var.set(self.current_input)
                self.new_input = False
            except ValueError:
                # 如果不是有效数字，显示错误
                messagebox.showwarning("粘贴错误", "剪贴板内容不是有效的数字")
        except tk.TclError:
            # 剪贴板为空或无法访问
             messagebox.showwarning("粘贴错误", "无法访问剪贴板或剪贴板为空")
                  
    def clear_all(self):
        """清空所有"""
        self.current_input = "0"
        self.result = 0
        self.operation = None
        self.new_input = True
        self.display_var.set("0")
        # 修改：按C时在历史记录中添加分隔符，而不是清空历史
        self.add_separator_to_history()
        
    def add_separator_to_history(self):
        """在历史记录中添加分隔符"""
        if self.calculation_history:  # 只有当历史记录不为空时才添加分隔符
            separator = "--------"
            self.calculation_history.append(separator)
            self.history_text.config(state=tk.NORMAL)
            self.history_text.insert(tk.END, separator + "\n")
            self.history_text.see(tk.END)
            self.history_text.config(state=tk.DISABLED)
    
    def clear_history_only(self):
        """仅清除历史记录，不影响当前计算"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.calculation_history = []
        
    def backspace(self):
        """退格"""
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
            self.new_input = True
        self.display_var.set(self.current_input)
        
    def toggle_sign(self):
        """切换正负号"""
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display_var.set(self.current_input)
    
    def calculate_sqrt(self):
        """计算平方根"""
        try:
            if self.current_input:
                value = float(self.current_input)
                if value >= 0:
                    result = math.sqrt(value)
                    history_entry = f"√{value} = {result}"
                    self.add_to_history(history_entry)
                    self.current_input = str(result)
                    self.display_var.set(self.current_input)
                    self.new_input = True
                else:
                    self.display_var.set("错误")
        except Exception:
            self.display_var.set("错误")
    
    def tax_calculator(self):
        """税率计算器弹窗"""
        # 税率计算器弹窗
        tax_window = tk.Toplevel(self.parent_frame)
        tax_window.title("税率计算器")
        tax_window.geometry("450x350")
        tax_window.configure(bg=self.theme.bg_color)
        tax_window.resizable(False, False)
        
        # 输入框架
        input_frame = tk.Frame(tax_window, bg=self.theme.bg_color)
        input_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(input_frame, text="金额:", font=("Microsoft YaHei", 12),
                bg=self.theme.bg_color, fg=self.theme.text_color).grid(row=0, column=0, sticky="w")
        amount_var = tk.StringVar()
        tk.Entry(input_frame, textvariable=amount_var, font=("Microsoft YaHei", 12),
                bd=2, relief="sunken").grid(row=0, column=1, sticky="ew", padx=(10, 0), ipady=5)
        
        tk.Label(input_frame, text="税率(%):", font=("Microsoft YaHei", 12),
                bg=self.theme.bg_color, fg=self.theme.text_color).grid(row=1, column=0, sticky="w", pady=(15, 0))
        tax_rate_var = tk.StringVar(value="13")
        tk.Entry(input_frame, textvariable=tax_rate_var, font=("Microsoft YaHei", 12),
                bd=2, relief="sunken").grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=(15, 0), ipady=5)
        
        input_frame.grid_columnconfigure(1, weight=1)
        
        # 结果显示
        result_frame = tk.Frame(tax_window, bg=self.theme.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        result_text = tk.Text(result_frame, height=8, font=("Microsoft YaHei", 11),
                             bg="#F8F9FA", fg="#212529", bd=2, relief="sunken")
        result_text.pack(fill=tk.BOTH, expand=True)
        
        def calculate_tax():
            try:
                amount = float(amount_var.get())
                tax_rate = float(tax_rate_var.get()) / 100
                
                tax_amount = amount * tax_rate
                total_amount = amount + tax_amount
                
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"原金额: {amount:.2f}\n")
                result_text.insert(tk.END, f"税率: {tax_rate*100:.2f}%\n")
                result_text.insert(tk.END, f"税额: {tax_amount:.2f}\n")
                result_text.insert(tk.END, f"含税总额: {total_amount:.2f}\n")
                result_text.insert(tk.END, f"\n不含税金额: {amount/(1+tax_rate):.2f}\n")
                result_text.insert(tk.END, f"税额: {amount*tax_rate/(1+tax_rate):.2f}\n")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
                
        tk.Button(input_frame, text="计算", command=calculate_tax,
                 bg="#2196F3", fg="white", activebackground="#1976D2",
                 font=("Microsoft YaHei", 12, "bold"), relief="raised", bd=3,
                 cursor="hand2").grid(row=2, column=0, columnspan=2, pady=(20, 0), ipadx=20, ipady=8)