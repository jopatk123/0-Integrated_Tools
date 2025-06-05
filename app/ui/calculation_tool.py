import tkinter as tk
from tkinter import ttk, messagebox
import math
import re

from app.ui.snake_game import SnakeGame
from app.ui.game_2048 import Game2048
from app.ui.tetris_game import TetrisGame

class CalculationTool:
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.setup_ui()
        
    def setup_ui(self):
        # 创建子选项卡
        self.sub_notebook = ttk.Notebook(self.parent)
        self.sub_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建计算器选项卡
        self.calculator_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.calculator_frame, text="计算器")
        self.setup_calculator()
        
        # 创建小写转大写选项卡
        self.converter_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.converter_frame, text="小写转大写")
        self.setup_converter()

        # 创建贪吃蛇选项卡
        self.snake_game_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.snake_game_frame, text="贪吃蛇")
        self.setup_snake_game()

        # 创建2048游戏选项卡
        self.game_2048_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.game_2048_frame, text="2048游戏")
        self.setup_2048_game()

        # 创建俄罗斯方块选项卡
        self.tetris_frame = ttk.Frame(self.sub_notebook)
        self.sub_notebook.add(self.tetris_frame, text="俄罗斯方块")
        self.setup_tetris_game()
        
    def setup_calculator(self):
        # 计算器主框架
        calc_main_frame = tk.Frame(self.calculator_frame, bg=self.theme.bg_color)
        calc_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 创建左右两个子框架，调整比例分配
        left_frame = tk.Frame(calc_main_frame, bg=self.theme.bg_color)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))

        # 右侧历史框架，固定宽度，减少空间占用
        right_frame = tk.Frame(calc_main_frame, bg=self.theme.bg_color, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        right_frame.pack_propagate(False)  # 防止子组件改变框架大小
        
        # 左侧：显示屏和按钮
        # 显示屏
        self.display_var = tk.StringVar(value="0")
        display_frame = tk.Frame(left_frame, bg=self.theme.bg_color)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        display_entry = tk.Entry(display_frame, textvariable=self.display_var, 
                                font=("Microsoft YaHei", 16, "bold"), justify="right", state="readonly",
                                bg="#2C2C2C", fg="#00FF00", bd=3, relief="sunken")
        display_entry.pack(fill=tk.X, ipady=10)
        
        # 粘贴按钮 (移到显示屏下方)
        paste_btn = tk.Button(left_frame, text="粘贴", font=("Microsoft YaHei", 9),
                             command=self.paste_from_clipboard, bg="#9C27B0", fg="white",
                             activebackground="#7B1FA2", relief="raised", bd=2, cursor="hand2")
        paste_btn.pack(fill=tk.X, pady=(0, 10), ipadx=8, ipady=2)
        
        # 按钮框架
        self.buttons_frame = tk.Frame(left_frame, bg=self.theme.bg_color)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True)

        # 右侧：计算历史 - 优化布局
        history_label = tk.Label(right_frame, text="计算历史", font=("Microsoft YaHei", 11, "bold"),
                                bg=self.theme.bg_color, fg=self.theme.text_color)
        history_label.pack(pady=(0, 8))
        
        # 创建历史记录框架，添加滚动条
        history_container = tk.Frame(right_frame, bg=self.theme.bg_color)
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
        clear_history_btn = tk.Button(right_frame, text="清除历史", font=("Microsoft YaHei", 9),
                                     command=self.clear_history_only, bg="#6C757D", fg="white",
                                     activebackground="#5A6268", relief="raised", bd=1, cursor="hand2")
        clear_history_btn.pack(pady=(8, 0), ipadx=5, ipady=2)

        # 移除顶部的历史记录状态栏
        # history_frame = tk.Frame(calc_main_frame, bg=self.theme.bg_color)
        # history_frame.pack(fill=tk.X, pady=(0, 15))
        
        # tk.Label(history_frame, text="计算历史:", font=("Microsoft YaHei", 10),
        #         bg=self.theme.bg_color, fg=self.theme.text_color).pack(side=tk.LEFT)
        
        # self.history_var = tk.StringVar(value="暂无历史记录")
        # history_label = tk.Label(history_frame, textvariable=self.history_var, 
        #                         font=("Microsoft YaHei", 9), bg="#F0F0F0", fg="#666666",
        #                         relief="sunken", bd=1, anchor="w")
        # history_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0), ipady=3)
        
        # 计算器状态
        self.current_input = ""
        self.result = 0
        self.operation = None
        self.new_input = True
        self.calculation_history = []
        
        # 设置计算器按钮
        self.setup_calculator_buttons()

    def setup_snake_game(self):
        # 贪吃蛇游戏界面初始化
        # 清空之前可能存在的 "开发中" 标签
        for widget in self.snake_game_frame.winfo_children():
            widget.destroy()
        # 实例化贪吃蛇游戏
        self.snake_game_instance = SnakeGame(self.snake_game_frame, self.theme)
        pass

    def setup_2048_game(self):
        # 2048游戏界面初始化
        # 清空之前可能存在的 "开发中" 标签
        for widget in self.game_2048_frame.winfo_children():
            widget.destroy()
        # 实例化2048游戏
        self.game_2048_instance = Game2048(self.game_2048_frame, self.theme)
        pass

    def setup_tetris_game(self):
        # 俄罗斯方块游戏界面初始化
        # 清空之前可能存在的 "开发中" 标签
        for widget in self.tetris_frame.winfo_children():
            widget.destroy()
        # 实例化俄罗斯方块游戏
        self.tetris_game_instance = TetrisGame(self.tetris_frame, self.theme)
        
    def setup_calculator_buttons(self):
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
        # Unused scientific function elif blocks completely removed
        elif char == 'tax':
            self.tax_calculator()
              
    def input_number(self, char):
        if self.new_input:
            self.current_input = char
            self.new_input = False
        else:
            if char == '.' and '.' in self.current_input:
                return
            self.current_input += char
        self.display_var.set(self.current_input)
        
    def input_operator(self, op):
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
            clipboard_content = self.calculator_frame.clipboard_get()
            
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
        
    def clear_entry(self):
        self.current_input = "0"
        self.display_var.set("0")
        self.new_input = True
        
    def backspace(self):
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
            self.new_input = True
        self.display_var.set(self.current_input)
        
    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display_var.set(self.current_input)
            
    def scientific_function(self, func):
        if self.current_input:
            try:
                num = float(self.current_input)
                if func == 'sin':
                    result = math.sin(math.radians(num))
                elif func == 'cos':
                    result = math.cos(math.radians(num))
                elif func == 'tan':
                    result = math.tan(math.radians(num))
                elif func == '√':
                    if num >= 0:
                        result = math.sqrt(num)
                    else:
                        messagebox.showerror("错误", "负数不能开平方根")
                        return
                elif func == 'log':
                    if num > 0:
                        result = math.log10(num)
                    else:
                        messagebox.showerror("错误", "对数的真数必须大于0")
                        return
                elif func == 'ln':
                    if num > 0:
                        result = math.log(num)
                    else:
                        messagebox.showerror("错误", "自然对数的真数必须大于0")
                        return
                        
                self.current_input = str(result)
                self.display_var.set(self.current_input)
                self.new_input = True
            except Exception as e:
                messagebox.showerror("错误", f"计算错误: {str(e)}")
                
    def input_constant(self, value):
        """输入常数"""
        self.current_input = str(value)
        self.display_var.set(self.current_input)
        self.new_input = False
    
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
    
    def calculate_trig(self, func):
        """计算三角函数"""
        try:
            if self.current_input:
                value = float(self.current_input)
                # 将角度转换为弧度
                radians = math.radians(value)
                
                if func == 'sin':
                    result = math.sin(radians)
                elif func == 'cos':
                    result = math.cos(radians)
                elif func == 'tan':
                    result = math.tan(radians)
                
                history_entry = f"{func}({value}°) = {result}"
                self.add_to_history(history_entry)
                self.current_input = str(result)
                self.display_var.set(self.current_input)
                self.new_input = True
        except Exception:
            self.display_var.set("错误")
    
    def calculate_log(self, func):
        """计算对数函数"""
        try:
            if self.current_input:
                value = float(self.current_input)
                if value > 0:
                    if func == 'log':
                        result = math.log10(value)
                    elif func == 'ln':
                        result = math.log(value)
                    
                    history_entry = f"{func}({value}) = {result}"
                    self.add_to_history(history_entry)
                    self.current_input = str(result)
                    self.display_var.set(self.current_input)
                    self.new_input = True
                else:
                    self.display_var.set("错误")
        except Exception:
            self.display_var.set("错误")
        
    def input_parenthesis(self, char):
        # 简单的括号处理，这里可以扩展更复杂的表达式计算
        if self.new_input:
            self.current_input = char
            self.new_input = False
        else:
            self.current_input += char
        self.display_var.set(self.current_input)
        
    def tax_calculator(self):
        # 税率计算器弹窗
        tax_window = tk.Toplevel(self.parent)
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
        
    def setup_converter(self):
        # 小写转大写主框架
        conv_main_frame = tk.Frame(self.converter_frame, bg=self.theme.bg_color)
        conv_main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = tk.Label(conv_main_frame, text="数字小写转大写", 
                              font=("Microsoft YaHei", 18, "bold"),
                              bg=self.theme.bg_color, fg=self.theme.text_color)
        title_label.pack(pady=(0, 20))
        
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
        
        # 结果显示框架
        result_frame = tk.Frame(conv_main_frame, bg=self.theme.bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(result_frame, text="转换结果:", 
                font=("Microsoft YaHei", 12),
                bg=self.theme.bg_color, fg=self.theme.text_color).pack(anchor="w")
        
        self.result_text = tk.Text(result_frame, height=10, font=("Microsoft YaHei", 12),
                                  bg="#F8F9FA", fg="#212529", wrap=tk.WORD,
                                  bd=2, relief="sunken")
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 滚动条
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
    def convert_to_chinese(self):
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
            
            # 添加一些示例说明
            self.result_text.insert(tk.END, "说明:\n")
            self.result_text.insert(tk.END, "• 支持整数和小数（最多两位小数）\n")
            self.result_text.insert(tk.END, "• 自动处理零的读法\n")
            self.result_text.insert(tk.END, "• 符合中文数字表达习惯\n")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"转换失败: {str(e)}")
            
    def number_to_chinese(self, amount):
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
        self.amount_var.set("")
        self.result_text.delete(1.0, tk.END)