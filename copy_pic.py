import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import piexif
from datetime import datetime
import hashlib
import random
import string

class ImageHashModifier:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("图片哈希值修改器")
        self.window.geometry("500x300")
        
        # 设置中文字体（尝试几种常见的中文字体）
        self.chinese_font = ('Microsoft YaHei', 10)  # 微软雅黑
        # 如果系统没有微软雅黑，尝试其他中文字体
        if not self.check_font_exists('Microsoft YaHei'):
            self.chinese_font = ('SimSun', 10)  # 宋体
            if not self.check_font_exists('SimSun'):
                self.chinese_font = ('SimHei', 10)  # 黑体
                if not self.check_font_exists('SimHei'):
                    self.chinese_font = ('Arial Unicode MS', 10)  # Mac系统可能有的字体
        
        # 创建界面元素
        self.create_widgets()
        
    def check_font_exists(self, font_name):
        """检查字体是否存在"""
        try:
            tk.font.Font(font=(font_name, 10))
            return True
        except:
            return False
        
    def create_widgets(self):
        # 设置窗口字体
        self.window.option_add('*Font', self.chinese_font)
        
        # 选择文件夹按钮
        self.select_button = tk.Button(
            self.window, 
            text="选择文件夹", 
            command=self.select_folder,
            height=2,
            width=20,
            font=self.chinese_font
        )
        self.select_button.pack(pady=20)
        
        # 显示选择的文件夹路径
        self.path_label = tk.Label(
            self.window, 
            text="未选择文件夹", 
            wraplength=400,
            font=self.chinese_font
        )
        self.path_label.pack(pady=10)
        
        # 处理按钮
        self.process_button = tk.Button(
            self.window, 
            text="开始处理", 
            command=self.process_images,
            height=2,
            width=20,
            font=self.chinese_font
        )
        self.process_button.pack(pady=20)
        
        # 状态显示
        self.status_label = tk.Label(
            self.window, 
            text="",
            font=self.chinese_font
        )
        self.status_label.pack(pady=10)
        
    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.path_label.config(text=f"已选择文件夹: {self.folder_path}")

    def generate_random_string(self, length=10):
        """生成随机字符串作为新文件名"""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
    
    def modify_image(self, image_path):
        """修改图片的元数据和添加随机数据"""
        try:
            # 读取图片
            img = Image.open(image_path)
            
            # 创建新的EXIF数据
            exif_dict = {"0th":{}, "Exif":{}, "GPS":{}, "1st":{}, "thumbnail":None}
            exif_dict["0th"][piexif.ImageIFD.Make] = f"Modified_{self.generate_random_string()}"
            exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
            exif_bytes = piexif.dump(exif_dict)
            
            # 获取原始图片格式
            original_format = img.format.lower() if img.format else 'jpeg'
            extension = '.png' if original_format == 'png' else '.jpg'
            
            # 生成新文件名
            new_filename = f"modified_{self.generate_random_string()}{extension}"
            new_path = os.path.join(self.folder_path, new_filename)
            
            # 保存图片，PNG格式不添加EXIF数据以保持透明通道
            if original_format == 'png':
                img.save(new_path, "PNG")
            else:
                img.save(new_path, "JPEG", exif=exif_bytes)
            
            # 添加随机数据到文件末尾
            with open(new_path, 'ab') as f:
                f.write(os.urandom(random.randint(10, 100)))
                
            return True
        except Exception as e:
            print(f"处理图片时出错: {str(e)}")
            return False
            
    def process_images(self):
        if not hasattr(self, 'folder_path'):
            messagebox.showerror("错误", "请先选择文件夹！")
            return
            
        # 获取所有图片文件
        image_files = [f for f in os.listdir(self.folder_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            messagebox.showinfo("提示", "所选文件夹中没有找到支持的图片格式！")
            return
            
        # 处理每个图片
        success_count = 0
        for image_file in image_files:
            image_path = os.path.join(self.folder_path, image_file)
            if self.modify_image(image_path):
                success_count += 1
                
        # 显示处理结果
        self.status_label.config(
            text=f"处理完成！\n成功处理 {success_count} 张图片，共 {len(image_files)} 张"
        )
        messagebox.showinfo("完成", f"成功处理 {success_count} 张图片，共 {len(image_files)} 张")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageHashModifier()
    app.run()