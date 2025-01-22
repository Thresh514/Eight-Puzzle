import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel, QLineEdit, QComboBox, QGroupBox
)
from PyQt5.QtCore import QThread, pyqtSignal

class PuzzleSolverThread(QThread):
    result_signal = pyqtSignal(str)

    def __init__(self, board, algo, param):
        super().__init__()
        self.board = board
        self.algo = algo
        self.param = param

    def run(self):
        # 模拟解题结果
        try:
            # 假设结果生成代码替换此处
            result = f"Solving board: {self.board} using {self.algo} (param={self.param})\nSolution found!"
            self.result_signal.emit(result)
        except Exception as e:
            self.result_signal.emit(f"Error: {e}")


class PuzzleSolverApp(QWidget):
    """主窗口类，用于提供用户界面。"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eight Puzzle Solver")
        self.setGeometry(200, 200, 500, 750)
        self.setup_ui()

    def setup_ui(self):
        """初始化用户界面。"""
        main_layout = QVBoxLayout()

        # 使用说明
        self.instructions = QLabel(
            "Welcome to the Eight Puzzle Solver!\n"
            "1. Enter a 9-digit board configuration (e.g., '012345678').\n"
            "2. Select an algorithm and heuristic (if applicable).\n"
            "3. Click 'Solve Puzzle' to get the solution."
        )
        main_layout.addWidget(self.instructions)

        # 输入部分分组
        input_group = QGroupBox("Input")
        input_layout = QVBoxLayout()

        # 输入棋盘
        self.label = QLabel("Enter 8-puzzle board (e.g., '012345678'):")
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

        # 启动后台线程
        self.thread = PuzzleSolverThread(board, algo, param)
        self.thread.result_signal.connect(self.display_result)
        self.thread.start()

    def display_result(self, result):
        """显示解题结果，并恢复 UI 状态。"""
        self.result.setText(result)
        self.solve_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())
        
    window = PuzzleSolverApp()
    window.show()
    sys.exit(app.exec_())
