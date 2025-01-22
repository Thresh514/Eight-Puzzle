import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox, QGroupBox
)
from PyQt5.QtCore import QThread, pyqtSignal
from timer import Timer

class PuzzleSolverThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, board, algo, param):
        super().__init__()
        self.board = board
        self.algo = algo
        self.param = param
        self.timer = Timer("Solver Timer")
        self.is_running = True  # 控制线程是否运行


    def format_board(self, board):
        """格式化棋盘为 3x3 格式，并将 0 替换为 _"""
        return '\n'.join([' '.join(row).replace("0", "_") for row in [board[i:i+3] for i in range(0, len(board), 3)]])

    def stop(self):
        """停止线程运行"""
        self.is_running = False

    def run(self):
        try:
            self.timer.start()
            self.result_signal.emit(f"Starting to solve:\n{self.format_board(self.board)}\nAlgorithm: {self.algo}\n")

            current_board = list(self.board)
            goal_state = "123456780"  # 目标状态
            steps = 0

            while ''.join(current_board) != goal_state:
                if not self.is_running:  # 检查停止标志
                    self.result_signal.emit("Solving stopped by user.\n")
                    break
                # 模拟棋盘状态变化
                steps += 1
                current_board[steps % len(current_board)], current_board[(steps + 1) % len(current_board)] = \
                    current_board[(steps + 1) % len(current_board)], current_board[steps % len(current_board)]

                formatted_board = self.format_board(current_board)
                elapsed_time = self.timer.elapsed_time()
                self.result_signal.emit(
                    f"Step {steps}:\n{formatted_board}\nTime: {elapsed_time:.2f}s, Steps: {steps}\n"
                )
                self.msleep(500)

            # 完成后输出总时间和步数
            total_time = self.timer.get_diff()
            self.result_signal.emit(f"Solution found! 🎉\nTotal time: {total_time:.2f}s, Total steps: {steps}\n")
            self.timer.end()
        except Exception as e:
            self.timer.end()  # 确保计时器结束
            self.result_signal.emit(f"Error: {e}\n")






class PuzzleSolverApp(QWidget):
    """主窗口类，用于提供用户界面。"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eight Puzzle Solver")
        self.setGeometry(200, 200, 500, 1000)
        self.setup_ui()

    def setup_ui(self):
        """初始化用户界面。"""
        main_layout = QVBoxLayout()

        # 使用说明
        self.instructions = QLabel(
            "Welcome to the Eight Puzzle Solver!\n"
            "1. Enter a 9-digit board configuration with digits 0-8 (e.g., '012345678').\n"
            "2. Select an algorithm and heuristic (if applicable).\n"
            "3. Click 'Solve Puzzle' to get the solution."
        )
        main_layout.addWidget(self.instructions)

        # 输入部分分组
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        # 输入棋盘
        self.label = QLabel("Enter 8-puzzle board with digits 0-8 (e.g., '012345678'):")
        input_layout.addWidget(self.label)
        self.input_board = QLineEdit()
        self.input_board.setPlaceholderText("Enter numbers 0-8 (e.g., 012345678)")
        input_layout.addWidget(self.input_board)

        # 选择算法
        self.label_algo = QLabel("Select Algorithm:")
        input_layout.addWidget(self.label_algo)
        self.algo_select = QComboBox()
        self.algo_select.addItems(["BFS", "DFS", "Greedy", "A*"])
        input_layout.addWidget(self.algo_select)

        # 选择启发式
        self.label_heuristic = QLabel("Select Heuristic (for Greedy/A*):")
        input_layout.addWidget(self.label_heuristic)
        self.heuristic_select = QComboBox()
        self.heuristic_select.addItems(["h1 (Misplaced Tiles)", "h2 (Manhattan Distance)"])
        input_layout.addWidget(self.heuristic_select)

        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)

        # Solve 按钮
        self.solve_button = QPushButton("Solve Puzzle")
        self.solve_button.clicked.connect(self.solve_puzzle)
        
        main_layout.addWidget(self.solve_button)

        # Stop 按钮
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)  # 初始状态不可用
        self.stop_button.clicked.connect(self.stop_puzzle)
        main_layout.addWidget(self.stop_button)


        # 输出部分分组
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        output_layout.addWidget(self.result)
        output_group.setLayout(output_layout)

        main_layout.addWidget(output_group)

        self.setLayout(main_layout)

    def solve_puzzle(self):
        board = self.input_board.text().strip()
        algo = self.algo_select.currentText()
        heuristic_choice = self.heuristic_select.currentText()
        self.result.clear()

        # 输入验证
        if len(board) != 9 or not all(c in "012345678" for c in board):
            self.result.setText("Invalid board configuration! Please enter a valid 9-digit string with digits 0-8.")
            return

    # 设置参数
        param = heuristic_choice if algo in ["Greedy", "A*"] else 20

    # 更新状态并禁用按钮
        self.result.setText(f"Solving {board} using {algo}...")
        self.solve_button.setEnabled(False)
        self.stop_button.setEnabled(True)  # 启用 Stop 按钮

    # 启动后台线程
        self.thread = PuzzleSolverThread(board, algo, param)
        self.thread.result_signal.connect(self.display_result)
        self.thread.finished.connect(self.on_thread_finished)  # 线程结束后调用
        self.thread.start()


    def display_result(self, result):
        """显示解题结果，并恢复 UI 状态。"""
        self.result.append(result)
        self.result.ensureCursorVisible()

    def stop_puzzle(self):
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.stop()  # 调用线程的 stop 方法
            self.result.append("Solving stopped by user.\n")  # 在输出区域显示停止信息
            self.result.ensureCursorVisible()
            self.stop_button.setEnabled(False)
            self.solve_button.setEnabled(True)  # 恢复 Solve 按钮状态
    
    def on_thread_finished(self):
        """线程结束后恢复按钮状态"""
        self.solve_button.setEnabled(True)
        self.stop_button.setEnabled(False)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())
        
    window = PuzzleSolverApp()
    window.show()
    sys.exit(app.exec_())
