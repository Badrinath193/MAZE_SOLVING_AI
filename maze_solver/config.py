# Configuration Settings for Maze Solver

class Config:
    def __init__(self):
        # Maze settings
        self.maze_width = 20  # Width of the maze
        self.maze_height = 20  # Height of the maze
        self.start_position = (0, 0)  # Starting position in the maze
        self.end_position = (19, 19)  # Ending position in the maze

        # Solver settings
        self.solve_method = 'DFS'  # Method for solving the maze (DFS/BFS/A*)
        self.delay = 0.1  # Delay between steps for visualization

        # Additional settings can be added here

    def display_settings(self):
        print("Maze Width:", self.maze_width)
        print("Maze Height:", self.maze_height)
        print("Start Position:", self.start_position)
        print("End Position:", self.end_position)
        print("Solver Method:", self.solve_method)
        print("Delay between steps:", self.delay)