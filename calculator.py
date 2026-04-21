#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
科学计算器 - 支持基本运算和科学计算
"""

import tkinter as tk
from tkinter import ttk
import math
import re


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("科学计算器")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        
        self.expression = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 显示区域
        display_frame = tk.Frame(self.root, bg="#2c3e50", height=100)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 表达式显示
        self.expr_label = tk.Label(
            display_frame, 
            text="", 
            font=("Arial", 14), 
            bg="#2c3e50", 
            fg="#ecf0f1",
            anchor="e"
        )
        self.expr_label.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        # 结果显示
        result_entry = tk.Entry(
            display_frame,
            textvariable=self.result_var,
            font=("Arial", 32, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            justify="right",
            bd=0,
            relief=tk.FLAT
        )
        result_entry.pack(fill=tk.X, padx=10, pady=(0, 10), ipady=10)
        
        # 按钮框架
        button_frame = tk.Frame(self.root, bg="#ecf0f1")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 定义按钮布局
        # 第一行：科学计算功能
        buttons = [
            ["sin", "cos", "tan", "log", "ln"],
            ["asin", "acos", "atan", "√", "x²"],
            ["xʸ", "n!", "π", "e", "rad"],
            ["(", ")", "mod", "C", "⌫"],
            ["7", "8", "9", "/", "*"],
            ["4", "5", "6", "-", "+"],
            ["1", "2", "3", ".", "="],
            ["0", "00", "+/-", "EXP", "1/x"]
        ]
        
        # 颜色配置
        colors = {
            "number": "#ffffff",  # 数字按钮
            "operator": "#3498db",  # 运算符
            "scientific": "#9b59b6",  # 科学计算
            "clear": "#e74c3c",  # 清除
            "equals": "#2ecc71"  # 等于
        }
        
        # 创建按钮
        for i, row in enumerate(buttons):
            for j, btn_text in enumerate(row):
                # 确定按钮类型和颜色
                if btn_text in ["0", "00", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    bg_color = colors["number"]
                    fg_color = "#2c3e50"
                elif btn_text in ["+", "-", "*", "/", "=", ".", "+/-", "mod", "EXP", "1/x"]:
                    if btn_text == "=":
                        bg_color = colors["equals"]
                        fg_color = "#ffffff"
                    else:
                        bg_color = colors["operator"]
                        fg_color = "#ffffff"
                elif btn_text in ["C", "⌫"]:
                    bg_color = colors["clear"]
                    fg_color = "#ffffff"
                else:
                    bg_color = colors["scientific"]
                    fg_color = "#ffffff"
                
                # 创建按钮
                btn = tk.Button(
                    button_frame,
                    text=btn_text,
                    font=("Arial", 14, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    bd=0,
                    relief=tk.RAISED,
                    command=lambda x=btn_text: self.on_button_click(x)
                )
                
                # 网格布局
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                button_frame.grid_columnconfigure(j, weight=1)
                button_frame.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, char):
        """处理按钮点击事件"""
        if char == "C":
            self.clear_all()
        elif char == "⌫":
            self.backspace()
        elif char == "=":
            self.calculate()
        elif char in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "√", "x²", "n!", "1/x"]:
            self.apply_unary_operation(char)
        elif char in ["xʸ", "mod", "EXP"]:
            self.expression += f" {char} "
            self.update_display()
        elif char == "rad":
            self.toggle_angle_mode()
        elif char == "π":
            self.expression += str(math.pi)
            self.update_display()
        elif char == "e":
            self.expression += str(math.e)
            self.update_display()
        elif char == "+/-":
            self.negate_number()
        elif char == "(":
            self.expression += "("
            self.update_display()
        elif char == ")":
            self.expression += ")"
            self.update_display()
        else:
            self.expression += str(char)
            self.update_display()
    
    def update_display(self):
        """更新显示屏"""
        self.result_var.set(self.expression if self.expression else "0")
    
    def clear_all(self):
        """清空所有"""
        self.expression = ""
        self.result_var.set("0")
        self.expr_label.config(text="")
    
    def backspace(self):
        """退格"""
        if self.expression:
            self.expression = self.expression[:-1]
            self.update_display()
    
    def calculate(self):
        """执行计算"""
        try:
            # 保存原始表达式用于显示
            original_expr = self.expression
            
            # 预处理表达式
            expr = self.preprocess_expression(self.expression)
            
            # 安全计算
            result = self.safe_eval(expr)
            
            # 格式化结果
            if isinstance(result, float):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.expr_label.config(text=f"{original_expr} =")
            self.result_var.set(str(result))
            self.expression = str(result)
            
        except Exception as e:
            self.result_var.set("错误")
            self.expression = ""
    
    def preprocess_expression(self, expr):
        """预处理表达式，替换特殊符号"""
        # 移除空格
        expr = expr.strip()
        
        # 替换运算符
        expr = expr.replace("×", "*").replace("÷", "/")
        expr = expr.replace("mod", "%")
        expr = expr.replace("EXP", "*10**")
        
        # 处理隐式乘法 (如 2π, 3(4+5))
        expr = re.sub(r'(\d)([a-zA-Z(])', r'\1*\2', expr)
        expr = re.sub(r'(\))(\d)', r'\1*\2', expr)
        expr = re.sub(r'(\))([a-zA-Z])', r'\1*\2', expr)
        
        return expr
    
    def safe_eval(self, expr):
        """安全地计算表达式"""
        # 只允许安全的字符和操作
        allowed_chars = set("0123456789.+-*/%() ")
        if not all(c in allowed_chars for c in expr):
            raise ValueError("包含非法字符")
        
        # 使用 eval 但限制命名空间
        return eval(expr, {"__builtins__": {}}, {})
    
    def apply_unary_operation(self, op):
        """应用一元运算"""
        try:
            current_value = float(eval(self.expression)) if self.expression else 0
            
            if op == "sin":
                result = math.sin(math.radians(current_value))
            elif op == "cos":
                result = math.cos(math.radians(current_value))
            elif op == "tan":
                result = math.tan(math.radians(current_value))
            elif op == "asin":
                result = math.degrees(math.asin(current_value))
            elif op == "acos":
                result = math.degrees(math.acos(current_value))
            elif op == "atan":
                result = math.degrees(math.atan(current_value))
            elif op == "log":
                result = math.log10(current_value) if current_value > 0 else float('inf')
            elif op == "ln":
                result = math.log(current_value) if current_value > 0 else float('inf')
            elif op == "√":
                result = math.sqrt(current_value) if current_value >= 0 else float('nan')
            elif op == "x²":
                result = current_value ** 2
            elif op == "n!":
                result = math.factorial(int(current_value)) if current_value >= 0 and current_value == int(current_value) else float('nan')
            elif op == "1/x":
                result = 1 / current_value if current_value != 0 else float('inf')
            
            self.expr_label.config(text=f"{op}({current_value}) =")
            self.result_var.set(str(result))
            self.expression = str(result)
            
        except Exception as e:
            self.result_var.set("错误")
            self.expression = ""
    
    def negate_number(self):
        """正负号切换"""
        if self.expression:
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.update_display()


def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
