import tkinter as tk
import random
from tkinter import messagebox

class SnakeGame:
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.canvas = None
        self.score_label = None
        self.level_label = None
        self.high_score_label = None

        self.snake = []
        self.food = []
        self.direction = "Right"
        self.next_direction = "Right"  # 防止快速按键导致的反向移动
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.high_score = 0
        self.food_eaten = 0
        self.combo = 0
        self.max_combo = 0
        self.achievements = set()

        self.initial_speed = 200  # 初始速度
        self.game_speed = self.initial_speed
        self.cell_size = 20
        self.canvas_width = 400
        self.canvas_height = 400

        self.load_high_score()
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        # 信息面板
        info_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        info_frame.pack(pady=5)
        
        # Score Label
        self.score_label = tk.Label(info_frame, text=f"分数: {self.score}", 
                                   font=("Microsoft YaHei", 12, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.score_label.grid(row=0, column=0, padx=10)
        
        # Level Label
        self.level_label = tk.Label(info_frame, text=f"等级: {self.level}", 
                                   font=("Microsoft YaHei", 12, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.level_label.grid(row=0, column=1, padx=10)
        
        # High Score Label
        self.high_score_label = tk.Label(info_frame, text=f"最高分: {self.high_score}", 
                                         font=("Microsoft YaHei", 12, "bold"), 
                                         bg=self.theme.bg_color, fg=self.theme.text_color)
        self.high_score_label.grid(row=0, column=2, padx=10)

        # Game Canvas
        self.canvas = tk.Canvas(self.parent, width=self.canvas_width, height=self.canvas_height, 
                               bg="#2C3E50", highlightthickness=2, highlightcolor="#3498DB")
        self.canvas.pack(pady=10)
        
        # 按钮面板
        button_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        button_frame.pack(pady=5)

        # Restart Button
        restart_button = tk.Button(button_frame, text="重新开始", command=self.restart_game, 
                                   font=("Microsoft YaHei", 10), bg="#4CAF50", fg="white", 
                                   activebackground="#388E3C", relief="raised", bd=2, cursor="hand2")
        restart_button.grid(row=0, column=0, padx=5)
        
        # Pause Button
        self.pause_button = tk.Button(button_frame, text="暂停", command=self.toggle_pause, 
                                     font=("Microsoft YaHei", 10), bg="#FFC107", fg="black", 
                                     activebackground="#FFA000", relief="raised", bd=2, cursor="hand2")
        self.pause_button.grid(row=0, column=1, padx=5)
        
        # Instructions Button
        instructions_button = tk.Button(button_frame, text="游戏说明", command=self.show_instructions, 
                                       font=("Microsoft YaHei", 10), bg="#2196F3", fg="white", 
                                       activebackground="#1976D2", relief="raised", bd=2, cursor="hand2")
        instructions_button.grid(row=0, column=2, padx=5)

        # Bind arrow keys for controlling the snake
        try:
            root = self.parent.winfo_toplevel()
            root.bind("<Left>", lambda event: self.change_direction("Left"))
            root.bind("<Right>", lambda event: self.change_direction("Right"))
            root.bind("<Up>", lambda event: self.change_direction("Up"))
            root.bind("<Down>", lambda event: self.change_direction("Down"))
            root.bind("<space>", lambda event: self.toggle_pause())
            root.bind("p", lambda event: self.toggle_pause())
            root.bind("P", lambda event: self.toggle_pause())
            root.bind("r", lambda event: self.restart_game())
            root.bind("R", lambda event: self.restart_game())
            root.bind("<Escape>", lambda event: self.toggle_pause())
            # WASD控制
            root.bind("a", lambda event: self.change_direction("Left"))
            root.bind("d", lambda event: self.change_direction("Right"))
            root.bind("w", lambda event: self.change_direction("Up"))
            root.bind("s", lambda event: self.change_direction("Down"))
            root.bind("A", lambda event: self.change_direction("Left"))
            root.bind("D", lambda event: self.change_direction("Right"))
            root.bind("W", lambda event: self.change_direction("Up"))
            root.bind("S", lambda event: self.change_direction("Down"))
        except:
            pass  # 如果绑定失败，忽略错误

    def load_high_score(self):
        """加载最高分记录"""
        try:
            with open("snake_high_score.txt", "r") as f:
                self.high_score = int(f.read().strip())
        except:
            self.high_score = 0
    
    def save_high_score(self):
        """保存最高分记录"""
        try:
            with open("snake_high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass
    
    def show_instructions(self):
        """显示游戏说明"""
        instructions = (
            "🐍 贪吃蛇游戏说明 🐍\n\n"
            "🎯 游戏目标：\n"
            "控制贪吃蛇吃食物，让蛇变得更长，获得更高分数！\n\n"
            "🎮 操作方法：\n"
            "• 方向键：控制蛇的移动方向\n"
            "• 空格键/P键：暂停/继续游戏\n"
            "• R键：重新开始游戏\n\n"
            "📊 计分规则：\n"
            "• 每吃一个食物得10分\n"
            "• 连续吃食物有额外奖励\n"
            "• 每升一级速度会加快\n"
            "• 每吃5个食物升一级\n\n"
            "⚠️ 游戏结束条件：\n"
            "• 蛇撞到墙壁\n"
            "• 蛇撞到自己的身体\n\n"
            "💡 高级技巧：\n"
            "• 规划好路线，避免困住自己\n"
            "• 利用暂停功能思考策略\n"
            "• 尽量让蛇身形成螺旋状\n"
            "• 挑战更高分数和等级！\n\n"
            "🏆 成就系统：\n"
            "• 达到100分：蛇类新手\n"
            "• 达到500分：蛇类高手\n"
            "• 达到1000分：蛇王传说！"
        )
        messagebox.showinfo("游戏说明", instructions)

    def start_game(self):
        self.game_over = False
        self.paused = False
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.combo = 0
        self.max_combo = 0
        self.achievements = set()
        self.game_speed = self.initial_speed
        self.update_labels()
        self.direction = "Right"
        self.next_direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)] # Initial snake position and length
        self.create_food()
        self.run_game()

    def restart_game(self):
        if self.canvas:
            self.canvas.delete("all")
        self.start_game()

    def toggle_pause(self):
        """切换暂停状态"""
        if self.game_over:
            return
        
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="继续")
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                   text="游戏暂停\n按空格键或P键继续", 
                                   font=("Microsoft YaHei", 16, "bold"), 
                                   fill="#ECF0F1", tags="pause_text")
        else:
            self.pause_button.config(text="暂停")
            self.canvas.delete("pause_text")
            self.run_game()

    def run_game(self):
        if self.game_over:
            self.show_game_over()
            return
        
        if self.paused:
            return

        self.direction = self.next_direction  # 应用下一个方向
        self.move_snake()
        self.check_collisions()
        self.draw_elements()
        self.parent.after(self.game_speed, self.run_game)

    def create_food(self):
        max_x = (self.canvas_width - self.cell_size) // self.cell_size
        max_y = (self.canvas_height - self.cell_size) // self.cell_size
        self.food = (random.randint(0, max_x) * self.cell_size, 
                       random.randint(0, max_y) * self.cell_size)

    def draw_elements(self):
        self.canvas.delete("all")
        
        # Draw grid lines (optional, for better visual)
        for i in range(0, self.canvas_width, self.cell_size):
            self.canvas.create_line(i, 0, i, self.canvas_height, fill="#34495E", width=1)
        for i in range(0, self.canvas_height, self.cell_size):
            self.canvas.create_line(0, i, self.canvas_width, i, fill="#34495E", width=1)
        
        # Draw snake with gradient effect
        for i, segment in enumerate(self.snake):
            if i == 0:  # Head
                self.canvas.create_rectangle(segment[0], segment[1], 
                                             segment[0] + self.cell_size, segment[1] + self.cell_size, 
                                             fill="#1ABC9C", outline="#16A085", width=2)
                # Add eyes to the head
                eye_size = 3
                if self.direction == "Right":
                    eye1_x, eye1_y = segment[0] + 12, segment[1] + 5
                    eye2_x, eye2_y = segment[0] + 12, segment[1] + 12
                elif self.direction == "Left":
                    eye1_x, eye1_y = segment[0] + 5, segment[1] + 5
                    eye2_x, eye2_y = segment[0] + 5, segment[1] + 12
                elif self.direction == "Up":
                    eye1_x, eye1_y = segment[0] + 5, segment[1] + 5
                    eye2_x, eye2_y = segment[0] + 12, segment[1] + 5
                else:  # Down
                    eye1_x, eye1_y = segment[0] + 5, segment[1] + 12
                    eye2_x, eye2_y = segment[0] + 12, segment[1] + 12
                
                self.canvas.create_oval(eye1_x, eye1_y, eye1_x + eye_size, eye1_y + eye_size, fill="white")
                self.canvas.create_oval(eye2_x, eye2_y, eye2_x + eye_size, eye2_y + eye_size, fill="white")
            else:  # Body
                alpha = max(0.3, 1 - i * 0.05)  # Fade effect
                color_intensity = int(255 * alpha)
                body_color = f"#{46:02x}{color_intensity:02x}{113:02x}"  # Gradient green
                self.canvas.create_rectangle(segment[0], segment[1], 
                                             segment[0] + self.cell_size, segment[1] + self.cell_size, 
                                             fill=body_color, outline="#27AE60")
        
        # Draw food with animation effect
        food_colors = ["#E74C3C", "#F39C12", "#E67E22"]  # Red, Orange, Dark Orange
        food_color = food_colors[self.score % len(food_colors)]
        self.canvas.create_oval(self.food[0] + 2, self.food[1] + 2, 
                                self.food[0] + self.cell_size - 2, self.food[1] + self.cell_size - 2, 
                                fill=food_color, outline="#C0392B", width=2)
        # Add sparkle effect
        center_x = self.food[0] + self.cell_size // 2
        center_y = self.food[1] + self.cell_size // 2
        self.canvas.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, fill="white", outline="")

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Left":
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.cell_size, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.cell_size)
        else:
            return # Should not happen

        self.snake.insert(0, new_head)

        # Check if snake ate food
        if new_head[0] == self.food[0] and new_head[1] == self.food[1]:
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            
            # 计算得分（基础分+连击奖励）
            base_score = 10
            combo_bonus = min(self.combo * 2, 50)  # 连击奖励最多50分
            total_score = base_score + combo_bonus
            self.score += total_score
            self.food_eaten += 1
            
            # Level up every 5 foods
            if self.food_eaten % 5 == 0:
                self.level += 1
                # Increase speed (decrease delay)
                if self.game_speed > 80:
                    self.game_speed = max(80, self.game_speed - 15)
            
            # 检查成就
            self.check_achievements()
            
            self.update_labels()
            self.create_food()
            
            # Avoid creating food on snake body
            while self.food in self.snake:
                self.create_food()
        else:
            self.snake.pop()
            # 没吃到食物，连击重置
            if self.combo > 0:
                self.combo = 0

    def change_direction(self, new_direction):
        """改进的方向控制，防止快速按键导致的反向移动"""
        if new_direction == "Left" and self.direction != "Right":
            self.next_direction = new_direction
        elif new_direction == "Right" and self.direction != "Left":
            self.next_direction = new_direction
        elif new_direction == "Up" and self.direction != "Down":
            self.next_direction = new_direction
        elif new_direction == "Down" and self.direction != "Up":
            self.next_direction = new_direction

    def check_collisions(self):
        head_x, head_y = self.snake[0]

        # Wall collision
        if not (0 <= head_x < self.canvas_width and 0 <= head_y < self.canvas_height):
            self.game_over = True
            return

        # Self-collision (check if head collides with any part of its body)
        for segment in self.snake[1:]:
            if head_x == segment[0] and head_y == segment[1]:
                self.game_over = True
                return

    def check_achievements(self):
        """检查并显示成就"""
        new_achievements = []
        
        if self.score >= 100 and "snake_novice" not in self.achievements:
            self.achievements.add("snake_novice")
            new_achievements.append("🏅 成就解锁：蛇类新手！")
        
        if self.score >= 500 and "snake_expert" not in self.achievements:
            self.achievements.add("snake_expert")
            new_achievements.append("🏆 成就解锁：蛇类高手！")
        
        if self.score >= 1000 and "snake_legend" not in self.achievements:
            self.achievements.add("snake_legend")
            new_achievements.append("👑 成就解锁：蛇王传说！")
        
        if self.combo >= 10 and "combo_master" not in self.achievements:
            self.achievements.add("combo_master")
            new_achievements.append("⚡ 成就解锁：连击大师！")
        
        if len(self.snake) >= 20 and "long_snake" not in self.achievements:
            self.achievements.add("long_snake")
            new_achievements.append("🐍 成就解锁：超长巨蛇！")
        
        # 显示新成就
        for achievement in new_achievements:
            self.show_achievement_popup(achievement)
    
    def show_achievement_popup(self, achievement_text):
        """显示成就弹窗"""
        try:
            # 在画布上显示临时成就文本
            achievement_id = self.canvas.create_text(
                self.canvas_width // 2, 50,
                text=achievement_text,
                font=("Microsoft YaHei", 14, "bold"),
                fill="#F1C40F",
                tags="achievement"
            )
            # 3秒后删除
            self.parent.after(3000, lambda: self.canvas.delete("achievement"))
        except:
            pass
    
    def update_labels(self):
        """更新所有标签显示"""
        combo_text = f" (连击x{self.combo})" if self.combo > 1 else ""
        self.score_label.config(text=f"分数: {self.score}{combo_text}")
        self.level_label.config(text=f"等级: {self.level}")
        self.high_score_label.config(text=f"最高分: {self.high_score}")

    def show_game_over(self):
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            self.update_labels()
            
        # Clear canvas and show game over message
        self.canvas.delete("all")
        
        # Background for game over message
        self.canvas.create_rectangle(50, self.canvas_height // 2 - 80, 
                                    self.canvas_width - 50, self.canvas_height // 2 + 80,
                                    fill="#2C3E50", outline="#3498DB", width=3)
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 - 50,
                                text="🎮 游戏结束! 🎮", font=("Microsoft YaHei", 20, "bold"), fill="#E74C3C")
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 - 20,
                                text=f"最终得分: {self.score}", font=("Microsoft YaHei", 14), fill="#ECF0F1")
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                                text=f"达到等级: {self.level}", font=("Microsoft YaHei", 14), fill="#ECF0F1")
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 20,
                                text=f"吃掉食物: {self.food_eaten} 个", font=("Microsoft YaHei", 14), fill="#ECF0F1")
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40,
                                text=f"最大连击: {self.max_combo}", font=("Microsoft YaHei", 14), fill="#ECF0F1")
        
        if self.score == self.high_score and self.score > 0:
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 65,
                                    text="🏆 新纪录! 🏆", font=("Microsoft YaHei", 16, "bold"), fill="#F1C40F")
        
        # 显示获得的成就
        if self.achievements:
            achievement_text = f"解锁成就: {len(self.achievements)} 个"
            self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 85,
                                    text=achievement_text, font=("Microsoft YaHei", 12), fill="#3498DB")
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 105,
                                text="点击'重新开始'继续游戏 (R键)", font=("Microsoft YaHei", 12), fill="#BDC3C7")

if __name__ == '__main__':
    # Example usage (for testing the game independently)
    root = tk.Tk()
    root.title("贪吃蛇游戏测试")
    root.geometry("450x550")
    
    # Dummy theme for testing
    class DummyTheme:
        def __init__(self):
            self.bg_color = "#34495E"
            self.text_color = "#ECF0F1"

    game_frame = tk.Frame(root, bg=DummyTheme().bg_color)
    game_frame.pack(fill=tk.BOTH, expand=True)
    
    snake_game = SnakeGame(game_frame, DummyTheme())
    root.mainloop()