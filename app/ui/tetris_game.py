import tkinter as tk
import random
from tkinter import messagebox
import json
import os

class TetrisGame:
    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        self.canvas = None
        self.score_label = None
        self.level_label = None
        self.lines_label = None
        self.high_score_label = None
        self.next_piece_canvas = None

        self.cols = 10
        self.rows = 20
        self.cell_size = 30
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.high_score = 0
        self.game_over = False
        self.paused = False

        self.current_piece = None
        self.next_piece = None
        self.current_x = 0
        self.current_y = 0
        self.initial_speed = 500
        self.game_speed = self.initial_speed  # Milliseconds
        
        self.load_high_score()

        self.shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1, 0], [0, 1, 1]],  # Z
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 1], [0, 0, 1]],  # L
            [[1, 1, 1], [1, 0, 0]],  # J
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1], [1, 1]]   # O
        ]
        self.shape_colors = ["#00FFFF", "#FF0000", "#00FF00", "#FFA500", "#0000FF", "#800080", "#FFFF00"]
        # Corresponds to I, Z, S, L, J, T, O

        self.setup_ui()
        self.start_game()

    def load_high_score(self):
        """加载最高分记录"""
        try:
            if os.path.exists("tetris_high_score.json"):
                with open("tetris_high_score.json", "r") as f:
                    data = json.load(f)
                    self.high_score = data.get("high_score", 0)
        except:
            self.high_score = 0
    
    def save_high_score(self):
        """保存最高分记录"""
        try:
            with open("tetris_high_score.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass
    
    def show_instructions(self):
        """显示游戏说明"""
        instructions = (
            "🧩 俄罗斯方块游戏说明 🧩\n\n"
            "🎯 游戏目标：\n"
            "控制下落的方块，填满整行来消除并获得分数！\n\n"
            "🎮 操作方法：\n"
            "• 方向键/WASD/数字键盘：移动和旋转方块\n"
            "• ←→/A/D：左右移动方块\n"
            "• ↓/S：加速下落\n"
            "• ↑/W/Z/X：旋转方块\n"
            "• 空格键/回车键：瞬间下落到底\n"
            "• P键/ESC键：暂停/继续游戏\n"
            "• R键：重新开始游戏\n\n"
            "📊 计分规则：\n"
            "• 消除1行：100分\n"
            "• 消除2行：300分\n"
            "• 消除3行：500分\n"
            "• 消除4行：800分（Tetris！）\n"
            "• 连续消除有额外奖励\n"
            "• 每10行升一级，速度加快\n\n"
            "🎨 方块类型：\n"
            "• I型（直线）- 青色 | 最适合Tetris\n"
            "• O型（方块）- 黄色 | 稳定填充\n"
            "• T型（T形）- 紫色 | T-Spin专用\n"
            "• L型（L形）- 橙色 | 角落填充\n"
            "• J型（反L）- 蓝色 | 角落填充\n"
            "• S型（S形）- 绿色 | 波浪填充\n"
            "• Z型（Z形）- 红色 | 波浪填充\n\n"
            "⚠️ 游戏结束条件：\n"
            "• 方块堆积到顶部无法放置新方块\n\n"
            "💡 高级策略：\n"
            "• 尽量保持底部平整，避免留洞\n"
            "• 为I型方块预留4格宽的空间\n"
            "• 学习T-Spin技巧获得更高分数\n"
            "• 提前观察下一个方块规划位置\n"
            "• 优先消除多行，获得更高分数\n"
            "• 合理利用暂停功能思考布局！\n\n"
            "🏆 进阶技巧：\n"
            "• T-Spin：利用T型方块的特殊旋转\n"
            "• 开局模板：使用固定开局提高效率\n"
            "• 堆叠技巧：为Tetris创造机会"
        )
        messagebox.showinfo("游戏说明", instructions)

    def setup_ui(self):
        main_frame = tk.Frame(self.parent, bg=self.theme.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        game_area_frame = tk.Frame(main_frame, bg=self.theme.bg_color)
        game_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        side_panel_frame = tk.Frame(main_frame, bg=self.theme.bg_color, width=180)
        side_panel_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10,0))
        side_panel_frame.pack_propagate(False)

        # Game Canvas
        self.canvas_width = self.cols * self.cell_size
        self.canvas_height = self.rows * self.cell_size
        self.canvas = tk.Canvas(game_area_frame, width=self.canvas_width, height=self.canvas_height, 
                               bg="#1C1C1C", highlightthickness=2, highlightcolor="#3498DB")
        self.canvas.pack(pady=(0,10))

        # 信息显示区域
        info_frame = tk.Frame(side_panel_frame, bg=self.theme.bg_color)
        info_frame.pack(pady=10, fill=tk.X)
        
        # Score Label
        self.score_label = tk.Label(info_frame, text=f"分数: {self.score}", 
                                   font=("Microsoft YaHei", 12, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.score_label.pack(pady=2)
        
        # High Score Label
        self.high_score_label = tk.Label(info_frame, text=f"最高分: {self.high_score}", 
                                        font=("Microsoft YaHei", 12, "bold"), 
                                        bg=self.theme.bg_color, fg=self.theme.text_color)
        self.high_score_label.pack(pady=2)
        
        # Level Label
        self.level_label = tk.Label(info_frame, text=f"等级: {self.level}", 
                                   font=("Microsoft YaHei", 12, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.level_label.pack(pady=2)
        
        # Lines Label
        self.lines_label = tk.Label(info_frame, text=f"消除行数: {self.lines_cleared}", 
                                   font=("Microsoft YaHei", 12, "bold"), 
                                   bg=self.theme.bg_color, fg=self.theme.text_color)
        self.lines_label.pack(pady=2)

        # Next Piece Display
        tk.Label(side_panel_frame, text="下一个方块:", font=("Microsoft YaHei", 12, "bold"), 
                bg=self.theme.bg_color, fg=self.theme.text_color).pack(pady=(15,5))
        self.next_piece_canvas_size = 4 * self.cell_size
        self.next_piece_canvas = tk.Canvas(side_panel_frame, width=self.next_piece_canvas_size, 
                                          height=self.next_piece_canvas_size, bg="#2C2C2C", 
                                          highlightthickness=1, highlightcolor="#555555")
        self.next_piece_canvas.pack(pady=5)

        # 按钮区域
        button_frame = tk.Frame(side_panel_frame, bg=self.theme.bg_color)
        button_frame.pack(pady=15, fill=tk.X)
        
        # Restart Button
        restart_button = tk.Button(button_frame, text="重新开始", command=self.restart_game, 
                                   font=("Microsoft YaHei", 10), bg="#4CAF50", fg="white", 
                                   activebackground="#388E3C", relief="raised", bd=2, cursor="hand2")
        restart_button.pack(pady=3, fill=tk.X)
        
        # Pause Button
        self.pause_button = tk.Button(button_frame, text="暂停", command=self.toggle_pause, 
                                     font=("Microsoft YaHei", 10), bg="#FFC107", fg="black", 
                                     activebackground="#FFA000", relief="raised", bd=2, cursor="hand2")
        self.pause_button.pack(pady=3, fill=tk.X)
        
        # Instructions Button
        instructions_button = tk.Button(button_frame, text="游戏说明", command=self.show_instructions, 
                                       font=("Microsoft YaHei", 10), bg="#2196F3", fg="white", 
                                       activebackground="#1976D2", relief="raised", bd=2, cursor="hand2")
        instructions_button.pack(pady=3, fill=tk.X)

        # Bind keys
        try:
            root = self.parent.winfo_toplevel()
            # 方向键控制
            root.bind("<Left>", lambda event: self.move_piece(-1, 0))
            root.bind("<Right>", lambda event: self.move_piece(1, 0))
            root.bind("<Down>", lambda event: self.move_piece(0, 1))
            root.bind("<Up>", lambda event: self.rotate_piece()) # Rotate
            # WASD控制
            root.bind("a", lambda event: self.move_piece(-1, 0))
            root.bind("d", lambda event: self.move_piece(1, 0))
            root.bind("s", lambda event: self.move_piece(0, 1))
            root.bind("w", lambda event: self.rotate_piece())
            root.bind("A", lambda event: self.move_piece(-1, 0))
            root.bind("D", lambda event: self.move_piece(1, 0))
            root.bind("S", lambda event: self.move_piece(0, 1))
            root.bind("W", lambda event: self.rotate_piece())
            # 数字键盘控制
            root.bind("<KP_Left>", lambda event: self.move_piece(-1, 0))
            root.bind("<KP_Right>", lambda event: self.move_piece(1, 0))
            root.bind("<KP_Down>", lambda event: self.move_piece(0, 1))
            root.bind("<KP_Up>", lambda event: self.rotate_piece())
            # 特殊功能键
            root.bind("<space>", lambda event: self.drop_piece()) # Hard drop
            root.bind("<Return>", lambda event: self.drop_piece()) # 回车键也可以瞬间下落
            root.bind("p", lambda event: self.toggle_pause()) # Pause
            root.bind("P", lambda event: self.toggle_pause()) # Pause
            root.bind("<Escape>", lambda event: self.toggle_pause()) # ESC暂停
            root.bind("r", lambda event: self.restart_game()) # R键重新开始
            root.bind("R", lambda event: self.restart_game()) # R键重新开始
            # Z键和X键用于旋转（经典俄罗斯方块控制）
            root.bind("z", lambda event: self.rotate_piece())
            root.bind("Z", lambda event: self.rotate_piece())
            root.bind("x", lambda event: self.rotate_piece())
            root.bind("X", lambda event: self.rotate_piece())
            root.bind('<Key>', self.handle_key_press)
            root.focus_set()
        except:
            pass  # 如果绑定失败，忽略错误

    def new_piece(self):
        if self.next_piece is None:
            idx = random.randint(0, len(self.shapes) - 1)
            self.current_piece = {"shape": self.shapes[idx], "color": self.shape_colors[idx], "id": idx}
        else:
            self.current_piece = self.next_piece
        
        idx_next = random.randint(0, len(self.shapes) - 1)
        self.next_piece = {"shape": self.shapes[idx_next], "color": self.shape_colors[idx_next], "id": idx_next}
        
        self.current_x = self.cols // 2 - len(self.current_piece["shape"][0]) // 2
        self.current_y = 0
        self.draw_next_piece()
        if not self.check_collision(self.current_piece["shape"], self.current_x, self.current_y):
            self.game_over = True

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 0:
                    color_index = self.board[r][c] -1 # Assuming 0 is empty, 1-7 are colors
                    color = self.shape_colors[color_index]
                    self.draw_cell(c, r, color)
        self.draw_piece(self.current_piece["shape"], self.current_x, self.current_y, self.current_piece["color"])

    def draw_cell(self, x_col, y_row, color, on_canvas=None):
        canvas_to_draw_on = on_canvas if on_canvas else self.canvas
        x1 = x_col * self.cell_size
        y1 = y_row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        canvas_to_draw_on.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333", width=1)

    def draw_piece(self, piece_shape, x_offset, y_offset, color, on_canvas=None):
        if piece_shape:
            for r, row_data in enumerate(piece_shape):
                for c, cell_val in enumerate(row_data):
                    if cell_val == 1:
                        self.draw_cell(x_offset + c, y_offset + r, color, on_canvas)
    
    def draw_next_piece(self):
        self.next_piece_canvas.delete("all")
        if self.next_piece:
            shape = self.next_piece["shape"]
            color = self.next_piece["color"]
            # Center the piece on the small canvas
            piece_width = len(shape[0]) * self.cell_size
            piece_height = len(shape) * self.cell_size
            x_offset = (self.next_piece_canvas_size - piece_width) / (2 * self.cell_size)
            y_offset = (self.next_piece_canvas_size - piece_height) / (2 * self.cell_size)
            self.draw_piece(shape, x_offset, y_offset, color, self.next_piece_canvas)

    def check_collision(self, piece_shape, x_offset, y_offset):
        for r, row_data in enumerate(piece_shape):
            for c, cell_val in enumerate(row_data):
                if cell_val == 1:
                    board_x, board_y = x_offset + c, y_offset + r
                    if not (0 <= board_x < self.cols and 0 <= board_y < self.rows and self.board[board_y][board_x] == 0):
                        return False # Collision
        return True # No collision

    def move_piece(self, dx, dy):
        if self.game_over or self.paused:
            return
        new_x = self.current_x + dx
        new_y = self.current_y + dy
        if self.check_collision(self.current_piece["shape"], new_x, new_y):
            self.current_x = new_x
            self.current_y = new_y
            self.draw_board()
            return True
        elif dy == 1 and dx == 0: # Trying to move down but collided
            self.lock_piece()
        return False

    def rotate_piece(self):
        if self.game_over or self.paused or not self.current_piece:
            return
        shape = self.current_piece["shape"]
        # Transpose and reverse rows for rotation
        rotated_shape = [list(row) for row in zip(*shape[::-1])]
        
        # Wall kick logic (simple version)
        original_x = self.current_x
        if self.check_collision(rotated_shape, self.current_x, self.current_y):
            self.current_piece["shape"] = rotated_shape
        elif self.check_collision(rotated_shape, self.current_x + 1, self.current_y): # Try kick right
            self.current_x += 1
            self.current_piece["shape"] = rotated_shape
        elif self.check_collision(rotated_shape, self.current_x - 1, self.current_y): # Try kick left
            self.current_x -=1
            self.current_piece["shape"] = rotated_shape
        # Add more sophisticated wall kick tests if needed for specific shapes like I
        # For 'I' piece, it might need to kick further
        elif self.current_piece["id"] == 0: # 'I' piece
            if self.check_collision(rotated_shape, self.current_x + 2, self.current_y):
                self.current_x += 2
                self.current_piece["shape"] = rotated_shape
            elif self.check_collision(rotated_shape, self.current_x - 2, self.current_y):
                self.current_x -= 2
                self.current_piece["shape"] = rotated_shape
        else:
            self.current_x = original_x # Reset x if no valid rotation found

        self.draw_board()

    def drop_piece(self):
        if self.game_over or self.paused:
            return
        while self.move_piece(0, 1):
            pass # Keep moving down until it locks
        # self.lock_piece() # move_piece will call lock_piece when it can't move down

    def lock_piece(self):
        if not self.current_piece: return
        shape = self.current_piece["shape"]
        for r, row_data in enumerate(shape):
            for c, cell_val in enumerate(row_data):
                if cell_val == 1:
                    board_y = self.current_y + r
                    board_x = self.current_x + c
                    if 0 <= board_y < self.rows and 0 <= board_x < self.cols:
                         self.board[board_y][board_x] = self.current_piece["id"] + 1 # Store color index + 1
        self.clear_lines()
        self.new_piece()
        self.draw_board()
        if self.game_over:
            self.show_game_over()

    def clear_lines(self):
        lines_cleared = 0
        new_board = [[0] * self.cols for _ in range(self.rows)]
        new_row_idx = self.rows - 1
        for r in range(self.rows - 1, -1, -1):
            if all(self.board[r]): # Line is full
                lines_cleared += 1
            else:
                new_board[new_row_idx] = self.board[r]
                new_row_idx -= 1
        self.board = new_board
        if lines_cleared > 0:
            # 更新消除的行数
            self.lines_cleared += lines_cleared
            
            # Score calculation based on lines cleared
            score_multiplier = [0, 100, 300, 500, 800]
            base_score = score_multiplier[min(lines_cleared, 4)]
            # 等级加成
            self.score += base_score * self.level
            
            # 等级系统：每消除10行升一级
            new_level = (self.lines_cleared // 10) + 1
            if new_level > self.level:
                self.level = new_level
                # 每升一级，速度加快
                self.game_speed = max(50, self.initial_speed - (self.level - 1) * 50)
            
            self.update_labels()

    def update_labels(self):
        """更新所有标签显示"""
        self.score_label.config(text=f"分数: {self.score}")
        self.high_score_label.config(text=f"最高分: {self.high_score}")
        self.level_label.config(text=f"等级: {self.level}")
        self.lines_label.config(text=f"消除行数: {self.lines_cleared}")

    def game_loop(self):
        if not self.game_over and not self.paused:
            self.move_piece(0, 1) # Move piece down automatically
        
        if not self.game_over:
            self.parent.after(self.game_speed, self.game_loop)
        else:
            self.show_game_over()

    def start_game(self):
        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.game_speed = self.initial_speed
        self.update_labels()
        self.new_piece() # Get first and next piece
        self.new_piece() # Actually sets current to first next, and generates a new next
        self.draw_board()
        if hasattr(self, 'game_over_text_id') and self.game_over_text_id:
            self.canvas.delete(self.game_over_text_id)
            self.game_over_text_id = None
        self.game_loop()

    def restart_game(self):
        self.start_game()

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="继续")
            # 在画布上显示暂停信息
            self.canvas.create_text(self.canvas_width//2, self.canvas_height//2, 
                                   text="游戏暂停\n按P键继续", 
                                   font=("Microsoft YaHei", 20, "bold"), 
                                   fill="#FFD700", tags="pause_text")
        else:
            self.pause_button.config(text="暂停")
            self.canvas.delete("pause_text")
            self.game_loop()

    def show_game_over(self):
        self.game_over = True
        
        # 检查并更新最高分
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            new_record = True
        else:
            new_record = False
        
        # 清空画布
        self.canvas.delete("all")
        
        # 创建游戏结束界面
        center_x = self.canvas_width // 2
        center_y = self.canvas_height // 2
        
        # 游戏结束标题
        self.canvas.create_text(center_x, center_y - 80, text="🎮 游戏结束 🎮", 
                               font=("Microsoft YaHei", 24, "bold"), fill="#FF4444")
        
        # 分数信息
        self.canvas.create_text(center_x, center_y - 40, text=f"最终分数: {self.score}", 
                               font=("Microsoft YaHei", 16, "bold"), fill="#FFFFFF")
        
        self.canvas.create_text(center_x, center_y - 10, text=f"达到等级: {self.level}", 
                               font=("Microsoft YaHei", 14), fill="#CCCCCC")
        
        self.canvas.create_text(center_x, center_y + 15, text=f"消除行数: {self.lines_cleared}", 
                               font=("Microsoft YaHei", 14), fill="#CCCCCC")
        
        # 新纪录提示
        if new_record:
            self.canvas.create_text(center_x, center_y + 45, text="🏆 新纪录！🏆", 
                                   font=("Microsoft YaHei", 18, "bold"), fill="#FFD700")
        
        # 重新开始提示
        self.canvas.create_text(center_x, center_y + 80, text="点击'重新开始'按钮继续游戏", 
                               font=("Microsoft YaHei", 12), fill="#888888")
        
        self.update_labels()

if __name__ == '__main__':
    root = tk.Tk()
    root.title("俄罗斯方块测试")
    root.geometry("600x700") # Adjusted for side panel

    class DummyTheme:
        def __init__(self):
            self.bg_color = "#34495E"
            self.text_color = "#ECF0F1"

    game_container = tk.Frame(root, bg=DummyTheme().bg_color)
    game_container.pack(fill=tk.BOTH, expand=True)

    tetris_game = TetrisGame(game_container, DummyTheme())
    root.mainloop()