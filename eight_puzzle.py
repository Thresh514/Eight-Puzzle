from searcher import *
from timer import *

def create_searcher(algorithm, param):
    """
    Create and return the appropriate searcher object.

    Args:
        algorithm (str): The search algorithm ('random', 'BFS', 'DFS', 'Greedy', 'A*').
        param: Parameter for the searcher (e.g., depth limit or heuristic function).

    Returns:
        Searcher: The corresponding searcher object.
    """
    searcher = None
    if algorithm == 'random':
        searcher = Searcher(param)
    elif algorithm == 'BFS':
        searcher = BFSearcher(param)
    elif algorithm == 'DFS':
        searcher = DFSearcher(param)
    elif algorithm == 'Greedy':
        if callable(param):  # 确保 param 是函数
            searcher = GreedySearcher(param)
        else:
            raise ValueError("For Greedy search, param must be a heuristic function (e.g., h1 or h2).")
    elif algorithm == 'A*':
        if callable(param):  # 确保 param 是函数
            searcher = AStarSearcher(param)
        else:
            raise ValueError("For A* search, param must be a heuristic function (e.g., h1 or h2).")
    else:
        print(f"Unknown algorithm: {algorithm}")
    return searcher

def validate_board(board_str):
    """
    Validate the initial board configuration.

    Args:
        board_str (str): A 9-character string representing the board configuration.

    Returns:
        bool: True if the board is valid, False otherwise.
    """
    if len(board_str) != 9 or set(board_str) != set("012345678"):
        print("Invalid board configuration! Please enter a 9-character string with digits 0-8.")
        return False
    return True

def eight_puzzle(init_boardstr, algorithm, param, result=None):
    """
    Driver function for solving Eight Puzzles using state-space search.
    
    Args:
        init_boardstr (str): Initial board configuration.
        algorithm (str): Search algorithm to use ('random', 'BFS', 'DFS', 'Greedy', 'A*').
        param: Parameter for the searcher (depth limit or heuristic function).
        result (list, optional): A list to store the result for GUI output.
    """
    init_board = Board(init_boardstr)
    init_state = State(init_board, None, 'init')
    searcher = create_searcher(algorithm, param)

    if not init_board.is_solvable():
        if result is not None:
            result.append("The puzzle is unsolvable.")
        return

    if searcher is None:
        if result is not None:
            result.append("Unknown algorithm. Please select a valid algorithm.")
        return

    timer = Timer(algorithm)
    timer.start()

    try:
        soln = searcher.find_solution(init_state)
    except KeyboardInterrupt:
        if result is not None:
            result.append("Search terminated by user.")
        return
    except Exception as e:
        if result is not None:
            result.append(f"An error occurred: {e}")
        return

    timer.end()
    if result is not None:
        result.append(f"Time: {timer.get_diff():.5f} seconds, States tested: {searcher.num_tested}")

    if soln is None:
        if result is not None:
            result.append("Failed to find a solution.")
    else:
        if result is not None:
            result.append(f"Found a solution requiring {soln.num_moves} moves.")
            # Store the solution steps
            steps = []
            soln.print_moves_to_list(steps)  # 修改打印逻辑为支持列表输出
            result.extend(steps)

def main():
    """
    Main function for the Eight Puzzle Solver.
    """
    print("Welcome to the Eight Puzzle Solver!")
    while True:
        board_str = input("Enter the initial board configuration (e.g., '012345678'): ").strip()
        if not validate_board(board_str):
            continue

        print("\nAvailable algorithms:")
        print("1. Random Search")
        print("2. Breadth-First Search (BFS)")
        print("3. Depth-First Search (DFS)")
        print("4. Greedy Search")
        print("5. A* Search")

        algo_map = {
            '1': 'random',
            '2': 'BFS',
            '3': 'DFS',
            '4': 'Greedy',
            '5': 'A*'
        }
        algo_choice = input("Choose an algorithm (1-5): ").strip()
        algorithm = algo_map.get(algo_choice)
        if algorithm is None:
            print("Invalid choice! Please select a valid algorithm.")
            continue

        if algorithm in ['Greedy', 'A*']:
            heuristic = input("Choose a heuristic (h1: misplaced tiles, h2: Manhattan distance): ").strip()
            param = h1 if heuristic == 'h1' else h2
        else:
            depth_limit = input("Enter depth limit (default: 10): ").strip()
            param = int(depth_limit) if depth_limit.isdigit() else 10

        eight_puzzle(board_str, algorithm, param)

        restart = input("Do you want to solve another puzzle? (y/n): ").strip().lower()
        if restart != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()