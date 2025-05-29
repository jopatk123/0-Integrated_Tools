import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import threading
import queue
import os
import random
import math

class ImageProcessorTool:
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        self.images_queue = queue.Queue()
        self.processed_images = []
        self.current_image_index = 0
        self.compress_count = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.parent_frame, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧控制面板 - 使用更紧凑的布局
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="5")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        control_frame.configure(width=280)  # 固定宽度
        
        # 文件夹选择区域 - 紧凑布局
        folder_frame = ttk.LabelFrame(control_frame, text="文件选择", padding="5")
        folder_frame.pack(fill=tk.X, pady=(0, 5))
        
        # 文件夹路径
        folder_select_frame = ttk.Frame(folder_frame)
        folder_select_frame.pack(fill=tk.X, pady=2)
        self.folder_path = tk.StringVar()
        ttk.Entry(folder_select_frame, textvariable=self.folder_path, font=('Arial', 8)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(folder_select_frame, text="浏览", command=self.browse_folder, width=6).pack(side=tk.RIGHT, padx=(2, 0))
        
        # 选项和加载按钮在同一行
        options_frame = ttk.Frame(folder_frame)
        options_frame.pack(fill=tk.X, pady=2)
        self.include_subfolders = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="含子文件夹", variable=self.include_subfolders).pack(side=tk.LEFT)
        ttk.Button(options_frame, text="加载图片", command=self.load_images, width=8).pack(side=tk.RIGHT)
        
        # 使用选项卡来组织功能
        notebook = ttk.Notebook(control_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 基础处理选项卡
        basic_frame = ttk.Frame(notebook, padding="5")
        notebook.add(basic_frame, text="基础处理")
        
        # 尺寸调整 - 紧凑布局
        resize_frame = ttk.LabelFrame(basic_frame, text="尺寸调整", padding="5")
        resize_frame.pack(fill=tk.X, pady=(0, 5))
        
        size_frame = ttk.Frame(resize_frame)
        size_frame.pack(fill=tk.X, pady=2)
        ttk.Label(size_frame, text="宽:", width=3).pack(side=tk.LEFT)
        self.width_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.width_var, width=8, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(size_frame, text="高:", width=3).pack(side=tk.LEFT)
        self.height_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.height_var, width=8, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(size_frame, text="调整", command=self.resize_images, width=6).pack(side=tk.RIGHT)
        
        # 裁剪设置 - 紧凑布局
        crop_frame = ttk.LabelFrame(basic_frame, text="裁剪设置", padding="5")
        crop_frame.pack(fill=tk.X, pady=(0, 5))
        
        crop_input_frame = ttk.Frame(crop_frame)
        crop_input_frame.pack(fill=tk.X, pady=2)
        ttk.Label(crop_input_frame, text="像素:", width=4).pack(side=tk.LEFT)
        self.crop_pixels = tk.StringVar(value="100")
        ttk.Entry(crop_input_frame, textvariable=self.crop_pixels, width=8, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(crop_input_frame, text="裁剪", command=self.crop_images, width=6).pack(side=tk.RIGHT)
        
        # 裁剪方式 - 水平布局
        crop_mode_frame = ttk.Frame(crop_frame)
        crop_mode_frame.pack(fill=tk.X, pady=2)
        self.crop_mode = tk.StringVar(value="bottom")
        ttk.Radiobutton(crop_mode_frame, text="底部", variable=self.crop_mode, value="bottom").pack(side=tk.LEFT)
        ttk.Radiobutton(crop_mode_frame, text="顶部", variable=self.crop_mode, value="top").pack(side=tk.LEFT, padx=(10, 0))
        
        # 高级处理选项卡
        advanced_frame = ttk.Frame(notebook, padding="5")
        notebook.add(advanced_frame, text="高级处理")
        
        # 随机旋转设置 - 紧凑布局
        rotate_frame = ttk.LabelFrame(advanced_frame, text="随机旋转", padding="5")
        rotate_frame.pack(fill=tk.X, pady=(0, 5))
        
        angle_input_frame = ttk.Frame(rotate_frame)
        angle_input_frame.pack(fill=tk.X, pady=2)
        ttk.Label(angle_input_frame, text="最小:", width=4).pack(side=tk.LEFT)
        self.min_angle_var = tk.StringVar(value="-5")
        ttk.Entry(angle_input_frame, textvariable=self.min_angle_var, width=6, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 3))
        ttk.Label(angle_input_frame, text="最大:", width=4).pack(side=tk.LEFT)
        self.max_angle_var = tk.StringVar(value="5")
        ttk.Entry(angle_input_frame, textvariable=self.max_angle_var, width=6, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(angle_input_frame, text="旋转", command=self.random_rotate_images, width=6).pack(side=tk.RIGHT)
        
        ttk.Label(rotate_frame, text="角度范围: -10° ~ +10°", font=('Arial', 7)).pack(pady=2)
        
        # 压缩设置 - 紧凑布局
        compress_frame = ttk.LabelFrame(advanced_frame, text="批量压缩", padding="5")
        compress_frame.pack(fill=tk.X, pady=(0, 5))
        
        quality_frame = ttk.Frame(compress_frame)
        quality_frame.pack(fill=tk.X, pady=2)
        ttk.Label(quality_frame, text="质量:", width=4).pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="85")
        ttk.Entry(quality_frame, textvariable=self.quality_var, width=8, font=('Arial', 8)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quality_frame, text="压缩", command=self.compress_images, width=6).pack(side=tk.RIGHT)
        
        # 覆盖原图选项
        self.overwrite_original = tk.BooleanVar(value=False)
        ttk.Checkbutton(compress_frame, text="覆盖原图", variable=self.overwrite_original).pack(pady=2)
        
        # 输出选项卡
        output_frame = ttk.Frame(notebook, padding="5")
        notebook.add(output_frame, text="输出设置")
        
        # 保存设置 - 紧凑布局
        save_frame = ttk.LabelFrame(output_frame, text="保存路径", padding="5")
        save_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.save_path = tk.StringVar()
        save_path_frame = ttk.Frame(save_frame)
        save_path_frame.pack(fill=tk.X, pady=2)
        ttk.Entry(save_path_frame, textvariable=self.save_path, font=('Arial', 8)).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(save_path_frame, text="浏览", command=self.browse_save_folder, width=6).pack(side=tk.RIGHT, padx=(2, 0))
        
        ttk.Button(save_frame, text="保存所有图片", command=self.save_images).pack(fill=tk.X, pady=(5, 0))
        
        # 右侧图片预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="图片预览", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 图片导航
        nav_frame = ttk.Frame(preview_frame)
        nav_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(nav_frame, text="上一张", command=self.prev_image).pack(side=tk.LEFT)
        self.image_counter = ttk.Label(nav_frame, text="0/0")
        self.image_counter.pack(side=tk.LEFT, padx=10)
        ttk.Button(nav_frame, text="下一张", command=self.next_image).pack(side=tk.LEFT)
        ttk.Button(nav_frame, text="删除", command=self.delete_image).pack(side=tk.LEFT, padx=(10, 0))
        
        # 图片显示区域
        self.canvas = tk.Canvas(preview_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path.set(folder_path)
    
    def browse_save_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.save_path.set(folder_path)
    
    def load_images(self):
        folder_path = self.folder_path.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("错误", "请选择有效的文件夹")
            return
        
        self.status_var.set("正在加载图片...")
        self.processed_images = []
        self.current_image_index = 0
        
        # 在后台线程中加载图片
        threading.Thread(target=self._load_images_thread, args=(folder_path,), daemon=True).start()
    
    def _load_images_thread(self, folder_path):
        image_files = []
        include_subfolders = self.include_subfolders.get()
        
        # 收集所有图片文件
        if include_subfolders:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        image_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(folder_path):
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    image_files.append(os.path.join(folder_path, file))
        
        # 加载图片
        for file_path in image_files:
            try:
                img = Image.open(file_path)
                self.processed_images.append({
                    'path': file_path,
                    'image': img,
                    'original': img.copy()
                })
            except Exception as e:
                print(f"无法加载图片 {file_path}: {e}")
        
        # 更新UI
        self.parent_frame.after(0, self._update_after_load)
    
    def _update_after_load(self):
        if self.processed_images:
            self.status_var.set(f"已加载 {len(self.processed_images)} 张图片")
            self.update_image_counter()
            self.display_current_image()
        else:
            self.status_var.set("未找到图片")
            self.image_counter.config(text="0/0")
            self.canvas.delete("all")
    
    def update_image_counter(self):
        if self.processed_images:
            self.image_counter.config(text=f"{self.current_image_index + 1}/{len(self.processed_images)}")
        else:
            self.image_counter.config(text="0/0")
    
    def display_current_image(self):
        if not self.processed_images:
            return
        
        self.canvas.delete("all")
        img_data = self.processed_images[self.current_image_index]
        img = img_data['image']
        
        # 调整图片大小以适应画布
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:  # 画布尚未完全初始化
            self.parent_frame.after(100, self.display_current_image)
            return
        
        img_width, img_height = img.size
        ratio = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_img)
        
        # 保存引用以防止垃圾回收
        self.current_photo = photo
        
        # 在画布中央显示图片
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
        # 显示图片信息
        filename = os.path.basename(img_data['path'])
        dimensions = f"{img_width}x{img_height}"
        self.status_var.set(f"当前图片: {filename} ({dimensions})")
    
    def prev_image(self):
        if self.processed_images and self.current_image_index > 0:
            self.current_image_index -= 1
            self.update_image_counter()
            self.display_current_image()
    
    def next_image(self):
        if self.processed_images and self.current_image_index < len(self.processed_images) - 1:
            self.current_image_index += 1
            self.update_image_counter()
            self.display_current_image()
    
    def resize_images(self):
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            width = int(self.width_var.get()) if self.width_var.get() else None
            height = int(self.height_var.get()) if self.height_var.get() else None
            
            if not width and not height:
                messagebox.showerror("错误", "请至少输入宽度或高度")
                return
            
            self.status_var.set("正在调整图片尺寸...")
            threading.Thread(target=self._resize_images_thread, args=(width, height), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _resize_images_thread(self, width, height):
        for img_data in self.processed_images:
            try:
                original = img_data['original']
                orig_width, orig_height = original.size
                
                # 计算新尺寸
                if width and height:  # 同时指定宽度和高度
                    new_size = (width, height)
                elif width:  # 只指定宽度，按比例计算高度
                    ratio = width / orig_width
                    new_size = (width, int(orig_height * ratio))
                else:  # 只指定高度，按比例计算宽度
                    ratio = height / orig_height
                    new_size = (int(orig_width * ratio), height)
                
                # 调整图片尺寸
                resized_img = original.resize(new_size, Image.LANCZOS)
                img_data['image'] = resized_img
                
            except Exception as e:
                print(f"调整图片尺寸失败: {e}")
        
        # 更新UI
        self.parent_frame.after(0, lambda: self._update_after_process("尺寸调整完成"))
    
    def crop_images(self):
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            pixels = int(self.crop_pixels.get())
            if pixels <= 0:
                messagebox.showerror("错误", "裁剪像素必须大于0")
                return
            
            crop_mode = self.crop_mode.get()
            self.status_var.set("正在裁剪图片...")
            threading.Thread(target=self._crop_images_thread, args=(pixels, crop_mode), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
    
    def _crop_images_thread(self, pixels, crop_mode):
        total_images = len(self.processed_images)
        processed_count = 0
        skipped_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                width, height = img.size
                
                if height <= pixels:
                    skipped_count += 1
                    continue  # 图片高度小于裁剪像素，跳过
                
                if crop_mode == "bottom":
                    # 保留上部分，裁剪底部
                    crop_box = (0, 0, width, height - pixels)
                else:  # crop_mode == "top"
                    # 保留下部分，裁剪顶部
                    crop_box = (0, pixels, width, height)
                
                cropped_img = img.crop(crop_box)
                img_data['image'] = cropped_img
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0:
                    self.parent_frame.after(0, lambda count=processed_count: 
                                   self.status_var.set(f"正在裁剪图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"裁剪图片失败: {e}")
        
        # 更新UI
        self.parent_frame.after(0, lambda: self._update_after_process(f"裁剪完成: 成功处理 {processed_count} 张图片，跳过 {skipped_count} 张图片"))
    
    def _update_after_process(self, message):
        self.status_var.set(message)
        self.display_current_image()
        
    def random_rotate_images(self):
        """批量随机旋转图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            min_angle = float(self.min_angle_var.get())
            max_angle = float(self.max_angle_var.get())
            
            # 验证角度范围
            if min_angle < -10 or min_angle > 10 or max_angle < -10 or max_angle > 10:
                messagebox.showerror("错误", "角度范围必须在-10到+10度之间")
                return
            
            if min_angle > max_angle:
                messagebox.showerror("错误", "最小角度不能大于最大角度")
                return
            
            self.status_var.set("正在随机旋转图片...")
            threading.Thread(target=self._random_rotate_images_thread, args=(min_angle, max_angle), daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的角度数字")
    
    def _random_rotate_images_thread(self, min_angle, max_angle):
        """在后台线程中随机旋转图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                
                # 生成随机角度
                random_angle = random.uniform(min_angle, max_angle)
                
                # 旋转图片
                rotated_img = self._rotate_and_crop_image(img, random_angle)
                img_data['image'] = rotated_img
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0:
                    self.parent_frame.after(0, lambda count=processed_count: 
                                   self.status_var.set(f"正在旋转图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"旋转图片失败: {e}")
        
        # 更新UI
        self.parent_frame.after(0, lambda: self._update_after_process(f"随机旋转完成: 成功处理 {processed_count} 张图片"))
    
    def _rotate_and_crop_image(self, img, angle):
        """旋转图片并裁剪掉空白区域"""
        # 转换角度为弧度
        angle_rad = math.radians(angle)
        
        # 获取原始尺寸
        width, height = img.size
        
        # 旋转图片（使用白色背景填充）
        rotated = img.rotate(angle, expand=True, fillcolor='white')
        
        # 计算旋转后的有效区域（去除空白边缘）
        # 对于小角度旋转，我们可以计算出内接矩形的尺寸
        cos_a = abs(math.cos(angle_rad))
        sin_a = abs(math.sin(angle_rad))
        
        # 计算内接矩形的尺寸
        new_width = int(width * cos_a + height * sin_a)
        new_height = int(width * sin_a + height * cos_a)
        
        # 计算裁剪区域，确保去除旋转产生的空白边缘
        # 使用更保守的裁剪策略
        crop_width = int(min(width * cos_a - height * sin_a, height * cos_a - width * sin_a))
        crop_height = int(min(height * cos_a - width * sin_a, width * cos_a - height * sin_a))
        
        # 确保裁剪尺寸为正数且不超过原图尺寸
        crop_width = max(1, min(crop_width, width))
        crop_height = max(1, min(crop_height, height))
        
        # 计算裁剪框的位置（居中裁剪）
        rotated_width, rotated_height = rotated.size
        left = (rotated_width - crop_width) // 2
        top = (rotated_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height
        
        # 裁剪图片
        cropped = rotated.crop((left, top, right, bottom))
        
        return cropped
        
    def compress_images(self):
        """批量压缩图片"""
        if not self.processed_images:
            messagebox.showerror("错误", "没有加载图片")
            return
        
        try:
            quality = int(self.quality_var.get())
            if quality < 1 or quality > 100:
                messagebox.showerror("错误", "压缩率必须在1-100之间")
                return
            
            # 如果不覆盖原图，需要选择保存路径
            overwrite = self.overwrite_original.get()
            save_path = ""
            
            if not overwrite:
                save_path = self.save_path.get()
                if not save_path:
                    save_path = filedialog.askdirectory(title="选择保存文件夹")
                    if not save_path:
                        return
                    self.save_path.set(save_path)
                
                # 确保保存路径存在
                if not os.path.isdir(save_path):
                    try:
                        os.makedirs(save_path)
                    except Exception as e:
                        messagebox.showerror("错误", f"无法创建保存文件夹: {e}")
                        return
            
            self.status_var.set("正在压缩图片...")
            self.compress_count = 0
            threading.Thread(target=self._compress_images_thread, 
                           args=(quality, overwrite, save_path), 
                           daemon=True).start()
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的压缩率数字")
    
    def _compress_images_thread(self, quality, overwrite, save_path):
        """在后台线程中压缩图片"""
        total_images = len(self.processed_images)
        processed_count = 0
        error_count = 0
        
        for img_data in self.processed_images:
            try:
                # 获取原始图片（未经处理的）
                original = img_data['original']
                original_path = img_data['path']
                filename = os.path.basename(original_path)
                
                # 确定保存路径
                if overwrite:
                    save_file_path = original_path
                else:
                    save_file_path = os.path.join(save_path, f"compressed_{filename}")
                
                # 获取文件格式
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext == '.jpg' or file_ext == '.jpeg':
                    format_to_save = 'JPEG'
                elif file_ext == '.png':
                    format_to_save = 'PNG'
                else:
                    # 对于其他格式，默认保存为JPEG
                    format_to_save = 'JPEG'
                    if not overwrite:  # 如果不是覆盖模式，修改文件扩展名
                        save_file_path = os.path.splitext(save_file_path)[0] + '.jpg'
                
                # 保存压缩后的图片
                original.save(save_file_path, format=format_to_save, quality=quality, optimize=True)
                processed_count += 1
                
                # 每处理5张图片更新一次状态
                if processed_count % 5 == 0:
                    self.parent_frame.after(0, lambda count=processed_count: 
                                   self.status_var.set(f"正在压缩图片... {count}/{total_images}"))
                
            except Exception as e:
                print(f"压缩图片失败 {filename}: {e}")
                error_count += 1
        
        self.compress_count = processed_count
        # 更新UI
        self.parent_frame.after(0, lambda: self._update_after_compress(processed_count, error_count, overwrite, save_path))
    
    def _update_after_compress(self, processed_count, error_count, overwrite, save_path):
        """压缩完成后更新UI"""
        if error_count > 0:
            message = f"压缩完成: 成功处理 {processed_count} 张图片，失败 {error_count} 张图片"
        else:
            if overwrite:
                message = f"压缩完成: 已成功压缩并覆盖 {processed_count} 张原图"
            else:
                message = f"压缩完成: 已成功压缩 {processed_count} 张图片到 {save_path}"
        
        self.status_var.set(message)
        messagebox.showinfo("压缩完成", message)
    
    def delete_image(self):
        if not self.processed_images:
            messagebox.showerror("错误", "没有图片可删除")
            return
        
        # 确认是否删除
        filename = os.path.basename(self.processed_images[self.current_image_index]['path'])
        confirm = messagebox.askyesno("确认删除", f"确定要删除图片 {filename} 吗？")
        if not confirm:
            return
        
        # 删除当前图片
        del self.processed_images[self.current_image_index]
        
        # 更新图片索引和显示
        if not self.processed_images:
            # 如果删除后没有图片了
            self.current_image_index = 0
            self.canvas.delete("all")
            self.image_counter.config(text="0/0")
            self.status_var.set("没有图片")
        else:
            # 如果删除的是最后一张图片，索引减1
            if self.current_image_index >= len(self.processed_images):
                self.current_image_index = len(self.processed_images) - 1
            
            # 更新计数器和显示
            self.update_image_counter()
            self.display_current_image()
            
        # 更新状态栏
        if self.processed_images:
            self.status_var.set(f"已删除图片，剩余 {len(self.processed_images)} 张图片")
        else:
            self.status_var.set("已删除所有图片")
    
    def save_images(self):
        if not self.processed_images:
            messagebox.showerror("错误", "没有图片可保存")
            return
        
        save_path = self.save_path.get()
        if not save_path:
            save_path = filedialog.askdirectory(title="选择保存文件夹")
            if not save_path:
                return
            self.save_path.set(save_path)
        
        if not os.path.isdir(save_path):
            try:
                os.makedirs(save_path)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建保存文件夹: {e}")
                return
        
        self.status_var.set("正在保存图片...")
        threading.Thread(target=self._save_images_thread, args=(save_path,), daemon=True).start()
    
    def _save_images_thread(self, save_path):
        saved_count = 0
        for img_data in self.processed_images:
            try:
                img = img_data['image']
                original_path = img_data['path']
                filename = os.path.basename(original_path)
                
                # 构建保存路径
                save_file_path = os.path.join(save_path, f"processed_{filename}")
                
                # 保存图片
                img.save(save_file_path)
                saved_count += 1
                
            except Exception as e:
                print(f"保存图片失败 {filename}: {e}")
        
        # 更新UI
        self.parent_frame.after(0, lambda: self.status_var.set(f"已保存 {saved_count} 张图片到 {save_path}"))