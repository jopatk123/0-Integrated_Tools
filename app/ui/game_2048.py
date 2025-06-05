import tkinter as tk
import random
from tkinter import messagebox
import json
import os

class Game2048:
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.grid_cells = []
        self.score = 0
        self.best_score = 0
        self.moves = 0
        self.game_over_flag = False
        self.won_flag = False
        self.continue_after_win = False

        self.grid_size = 4
        self.cell_size = 100
        self.cell_padding = 6
        self.font_size_tile = 32
        self.font_size_score = 16
        self.font_size_game_over = 24
        
        self.load_best_score()

        self.color_bg_game = "#92877d"
        self.color_bg_empty_cell = "#9e948a"
        self.color_text_dark = "#776e65"
        self.color_text_light = "#f9f6f2"
        self.tile_colors = {
            0: "#9e948a",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            # Higher tiles
            4096: "#3c3a32",
            8192: "#3c3a32",
        }

        self.setup_ui()
        self.start_game()

    def load_best_score(self):
        """加载最佳分数"""
        try:
            if os.path.exists("2048_best_score.json"):
                with open("2048_best_score.json", "r") as f:
                    data = json.load(f)
                    self.best_score = data.get("best_score", 0)
        except:
            self.best_score = 0
    
    def save_best_score(self):
        """保存最佳分数"""
        try:
            with open("2048_best_score.json", "w") as f:
                json.dump({"best_score": self.best_score}, f)
        except:
            pass
    
    def show_instructions(self):
        """显示游戏说明"""
        instructions = (
            "🎯 2048游戏说明 🎯\n\n"
            "🎮 游戏目标：\n"
            "通过合并相同数字的方块，最终得到2048方块！\n\n"
            "🕹️ 操作方法：\n"
            "• 方向键/WASD/数字键盘：移动所有方块\n"
            "• R键：重新开始游戏\n"
            "• 相同数字的方块会合并成一个\n"
            "• 每次移动后会随机出现新方块\n\n"
            "📊 计分规则：\n"
            "• 合并方块时获得对应分数\n"
            "• 合并的数字越大，得分越高\n"
            "• 步数越少，效率越高\n"
            "• 挑战更高分数！\n\n"
            "🏆 胜利条件：\n"
            "• 成功合并出2048方块即获胜\n"
            "• 获胜后可以选择继续游戏挑战更高数字\n\n"
            "❌ 失败条件：\n"
            "• 棋盘填满且无法移动时游戏结束\n\n"
            "💡 高级策略：\n"
            "• 选择一个角落作为最大数字的位置\n"
            "• 保持数字有序排列（如蛇形排列）\n"
            "• 避免随意移动，每步都要有计划\n"
            "• 尽量保持一行或一列为空\n"
            "• 优先合并小数字，为大数字腾出空间\n\n"
            "🎨 方块颜色：\n"
            "• 数字越大，颜色越鲜艳\n"
            "• 2048方块为金黄色！"
        )
        messagebox.showinfo("游戏说明", instructions)

    def setup_ui(self):
        # 信息面板
        info_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        info_frame.pack(pady=10)
        
        # Score and Best Score Labels
        score_frame = tk.Frame(info_frame, bg=self.theme.bg_color)
        score_frame.pack()
        
        self.score_label = tk.Label(score_frame, text=f"分数: {self.score}", 
                                    font=("Microsoft YaHei", self.font_size_score, "bold"), 
                                    bg=self.theme.bg_color, fg=self.theme.text_color)
        self.score_label.grid(row=0, column=0, padx=20)
        
        self.best_score_label = tk.Label(score_frame, text=f"最佳: {self.best_score}", 
                                         font=("Microsoft YaHei", self.font_size_score, "bold"), 
                                         bg=self.theme.bg_color, fg=self.theme.text_color)
        self.best_score_label.grid(row=0, column=1, padx=20)
        
        self.moves_label = tk.Label(score_frame, text=f"步数: {self.moves}", 
                                   font=("Microsoft YaHei", self.font_size_score, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.moves_label.grid(row=0, column=2, padx=20)

        # Game Grid Frame
        self.grid_frame = tk.Frame(self.parent, bg=self.color_bg_game, relief="raised", bd=3)
        self.grid_frame.pack(pady=15)

        for r in range(self.grid_size):
            row_frames = []
            for c in range(self.grid_size):
                frame = tk.Frame(self.grid_frame, 
                                 width=self.cell_size, height=self.cell_size, 
                                 bg=self.color_bg_empty_cell, relief="sunken", bd=1)
                frame.grid(row=r, column=c, padx=self.cell_padding, pady=self.cell_padding)
                frame.grid_propagate(False)
                label = tk.Label(frame, text="", font=("Microsoft YaHei", self.font_size_tile, "bold"))
                label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
                row_frames.append(label)
            self.grid_cells.append(row_frames)

        # 按钮面板
        button_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        button_frame.pack(pady=10)

        # Restart Button
        restart_button = tk.Button(button_frame, text="重新开始", command=self.start_game, 
                                   font=("Microsoft YaHei", 10), bg="#4CAF50", fg="white", 
                                   activebackground="#388E3C", relief="raised", bd=2, cursor="hand2")
        restart_button.grid(row=0, column=0, padx=5)
        
        # Undo Button (placeholder for future implementation)
        undo_button = tk.Button(button_frame, text="撤销", command=self.undo_move, 
                               font=("Microsoft YaHei", 10), bg="#FF9800", fg="white", 
                               activebackground="#F57C00", relief="raised", bd=2, cursor="hand2")
        undo_button.grid(row=0, column=1, padx=5)
        
        # Instructions Button
        instructions_button = tk.Button(button_frame, text="游戏说明", command=self.show_instructions, 
                                       font=("Microsoft YaHei", 10), bg="#2196F3", fg="white", 
                                       activebackground="#1976D2", relief="raised", bd=2, cursor="hand2")
        instructions_button.grid(row=0, column=2, padx=5)

        # Bind arrow keys
        try:
            root = self.parent.winfo_toplevel()
            root.bind("<Left>", lambda event: self.handle_key_press("Left"))
            root.bind("<Right>", lambda event: self.handle_key_press("Right"))
            root.bind("<Up>", lambda event: self.handle_key_press("Up"))
            root.bind("<Down>", lambda event: self.handle_key_press("Down"))
            root.bind("<KeyPress-r>", lambda event: self.start_game())
            root.bind("<KeyPress-R>", lambda event: self.start_game())
            # WASD控制
            root.bind("a", lambda event: self.handle_key_press("Left"))
            root.bind("d", lambda event: self.handle_key_press("Right"))
            root.bind("w", lambda event: self.handle_key_press("Up"))
            root.bind("s", lambda event: self.handle_key_press("Down"))
            root.bind("A", lambda event: self.handle_key_press("Left"))
            root.bind("D", lambda event: self.handle_key_press("Right"))
            root.bind("W", lambda event: self.handle_key_press("Up"))
            root.bind("S", lambda event: self.handle_key_press("Down"))
            # 数字键盘控制
            root.bind("<KP_Left>", lambda event: self.handle_key_press("Left"))
            root.bind("<KP_Right>", lambda event: self.handle_key_press("Right"))
            root.bind("<KP_Up>", lambda event: self.handle_key_press("Up"))
            root.bind("<KP_Down>", lambda event: self.handle_key_press("Down"))
        except:
            pass  # 如果绑定失败，忽略错误

    def undo_move(self):
        """撤销上一步移动（简单实现）"""
        messagebox.showinfo("撤销功能", "撤销功能将在未来版本中实现！")
    
    def start_game(self):
        self.matrix = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.moves = 0
        self.game_over_flag = False
        self.won_flag = False
        self.continue_after_win = False
        self.update_labels()
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid_ui()
        if hasattr(self, 'game_over_label') and self.game_over_label.winfo_exists():
            self.game_over_label.destroy()

    def update_grid_ui(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.matrix[r][c]
                cell_label = self.grid_cells[r][c]
                cell_label.config(text=str(value) if value != 0 else "", 
                                  bg=self.tile_colors.get(value, "#3c3a32"), 
                                  fg=self.color_text_light if value >= 8 else self.color_text_dark)
                # Adjust font size for larger numbers
                if value >= 1024:
                    cell_label.config(font=("Microsoft YaHei", self.font_size_tile - 8, "bold"))
                elif value >= 128:
                    cell_label.config(font=("Microsoft YaHei", self.font_size_tile - 4, "bold"))
                else:
                    cell_label.config(font=("Microsoft YaHei", self.font_size_tile, "bold"))

    def add_new_tile(self):
        empty_cells = []
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.matrix[r][c] == 0:
                    empty_cells.append((r, c))
        
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.matrix[r][c] = 2 if random.random() < 0.9 else 4 # 90% chance for 2, 10% for 4

    def handle_key_press(self, direction):
        if self.game_over_flag:
            return

        moved = False
        if direction == "Left":
            self.matrix, moved = self.slide_left(self.matrix)
        elif direction == "Right":
            self.matrix, moved = self.slide_right(self.matrix)
        elif direction == "Up":
            self.matrix, moved = self.slide_up(self.matrix)
        elif direction == "Down":
            self.matrix, moved = self.slide_down(self.matrix)

        if moved:
            self.moves += 1
            self.add_new_tile()
            self.update_grid_ui()
            
            # Check for win condition (2048 tile)
            if not self.won_flag and self.check_win():
                self.won_flag = True
                self.show_win_message()
            
            if self.check_game_over():
                self.game_over()
        self.update_labels()

    def slide_left(self, grid):
        new_grid = [[0]*self.grid_size for _ in range(self.grid_size)]
        moved = False
        for r in range(self.grid_size):
            pos = 0
            temp_row = [val for val in grid[r] if val != 0]
            merged_row = []
            skip = False
            for i in range(len(temp_row)):
                if skip:
                    skip = False
                    continue
                if i + 1 < len(temp_row) and temp_row[i] == temp_row[i+1]:
                    merged_value = temp_row[i] * 2
                    merged_row.append(merged_value)
                    self.score += merged_value
                    skip = True
                    moved = True
                else:
                    merged_row.append(temp_row[i])
            
            for val in merged_row:
                new_grid[r][pos] = val
                pos += 1
            
            if grid[r] != new_grid[r]:
                 moved = True
        return new_grid, moved

    def slide_right(self, grid):
        reversed_grid = [row[::-1] for row in grid]
        new_grid, moved = self.slide_left(reversed_grid)
        return [row[::-1] for row in new_grid], moved

    def slide_up(self, grid):
        transposed_grid = [list(col) for col in zip(*grid)]
        new_grid, moved = self.slide_left(transposed_grid)
        return [list(col) for col in zip(*new_grid)], moved

    def slide_down(self, grid):
        transposed_grid = [list(col) for col in zip(*grid)]
        new_grid, moved = self.slide_right(transposed_grid) # Use slide_right on transposed
        return [list(col) for col in zip(*new_grid)], moved

    def check_game_over(self):
        # Check for empty cells
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.matrix[r][c] == 0:
                    return False # Game not over
        
        # Check for possible merges horizontally
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                if self.matrix[r][c] == self.matrix[r][c+1]:
                    return False # Game not over
        
        # Check for possible merges vertically
        for c in range(self.grid_size):
            for r in range(self.grid_size - 1):
                if self.matrix[r][c] == self.matrix[r+1][c]:
                    return False # Game not over
        
        return True # Game over

    def game_over(self):
        self.game_over_flag = True
        
        # Update best score if needed
        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()
            self.update_labels()
        
        # Create game over overlay
        overlay_frame = tk.Frame(self.grid_frame, bg="#FFFFFF", relief="raised", bd=3)
        overlay_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.9, relheight=0.7)
        
        if self.won_flag and not self.continue_after_win:
            title_text = "🎉 恭喜获胜！ 🎉"
            title_color = "#F1C40F"
        else:
            title_text = "🎮 游戏结束 🎮"
            title_color = "#E74C3C"
        
        tk.Label(overlay_frame, text=title_text, 
                font=("Microsoft YaHei", 18, "bold"), 
                bg="#FFFFFF", fg=title_color).pack(pady=10)
        
        tk.Label(overlay_frame, text=f"最终分数: {self.score}", 
                font=("Microsoft YaHei", 14), 
                bg="#FFFFFF", fg=self.color_text_dark).pack(pady=2)
        
        tk.Label(overlay_frame, text=f"移动步数: {self.moves}", 
                font=("Microsoft YaHei", 14), 
                bg="#FFFFFF", fg=self.color_text_dark).pack(pady=2)
        
        if self.score == self.best_score and self.score > 0:
            tk.Label(overlay_frame, text="🏆 新纪录！ 🏆", 
                    font=("Microsoft YaHei", 16, "bold"), 
                    bg="#FFFFFF", fg="#F1C40F").pack(pady=5)
        
        tk.Label(overlay_frame, text="点击'重新开始'继续游戏", 
                font=("Microsoft YaHei", 12), 
                bg="#FFFFFF", fg="#7F8C8D").pack(pady=10)
        
        self.game_over_label = overlay_frame

    def check_win(self):
        """检查是否达到2048"""
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.matrix[r][c] == 2048:
                    return True
        return False
    
    def show_win_message(self):
        """显示胜利消息"""
        result = messagebox.askyesno(
            "🎉 恭喜获胜！ 🎉", 
            f"您成功达到了2048！\n\n当前分数: {self.score}\n移动步数: {self.moves}\n\n是否继续游戏挑战更高分数？",
            icon="question"
        )
        if result:
            self.continue_after_win = True
        else:
            self.game_over()
    
    def update_labels(self):
        """更新所有标签"""
        self.score_label.config(text=f"分数: {self.score}")
        self.best_score_label.config(text=f"最佳: {self.best_score}")
        self.moves_label.config(text=f"步数: {self.moves}")

if __name__ == '__main__':
    root = tk.Tk()
    root.title("2048 游戏测试")
    root.geometry("500x650")

    class DummyTheme:
        def __init__(self):
            self.bg_color = "#FAF8EF"
            self.text_color = "#776E65"

    game_container = tk.Frame(root, bg=DummyTheme().bg_color)
    game_container.pack(fill=tk.BOTH, expand=True)

    game_2048 = Game2048(game_container, DummyTheme())
    root.mainloop()