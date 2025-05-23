class ThemeManager:
    def __init__(self):
        # 设置主题颜色
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a7abc"
        self.warning_color = "#ff4444"
        self.caution_color = "#ffcc44"
    
    def get_button_style(self, button_type="normal"):
        """获取按钮样式"""
        if button_type == "normal":
            return {"bg": self.accent_color, "fg": "white"}
        elif button_type == "warning":
            return {"bg": self.warning_color, "fg": "white"}
        elif button_type == "caution":
            return {"bg": self.caution_color, "fg": "white"}
        else:
            return {"bg": self.accent_color, "fg": "white"}