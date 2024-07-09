import sys

def manhattan_distance(state, goal_state):
    """
    Calculate the Manhattan distance between two points on a grid.

    Parameters:
    state: A tuple representing the coordinates of the current state (e.g., (x1, y1)).
    goal_state: A tuple representing the coordinates of the goal state (e.g., (x2, y2)).

    Returns:
    The Manhattan distance between state and goal_state, which is abs(x1 - x2) + abs(y1 - y2).
    """
    return abs(state[0] - goal_state[0]) + abs(state[1] - goal_state[1])

class Node():
    """
    Represents a node in the search tree.

    Attributes:
    state: The current state represented by the node (e.g., coordinates on the grid).
    parent: The parent node from which this node was generated.
    action: The action taken to get from the parent node to this node.
    cost: The cost to reach this node from the start node.
    heuristic: The heuristic value (in this case, the Manhattan distance to the goal).
    """
    def __init__(self, state, parent, action, cost, heuristic):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

class PriorityQueueFrontier():
    """
    Implements the search frontier using a priority queue.

    Methods:
    add(self, node): Adds the given node to the frontier and sorts it based on the heuristic value.
    contains_state(self, state): Checks if the frontier contains the given state.
    empty(self): Checks if the frontier is empty.
    remove(self): Removes and returns the node with the highest priority (lowest heuristic value) from the frontier.
    """
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)
        self.frontier.sort(key=lambda x: x.heuristic + x.cost)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

class Maze():
    """
    Represents a maze and reads the maze layout from a file.
    """

    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def print(self):
        """
        Print the maze with visual representation of walls, start, goal, and solution path.
        """
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()

    def neighbors(self, state):
        """
        Find neighboring states that can be moved to from the current state.

        Parameters:
        state: Current state (coordinates) on the grid.

        Returns:
        List of valid neighboring states along with the actions to reach them.
        """
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self):
        """
        Solve the maze using the A* search algorithm.

        Actions:
        - Initialize the number of explored nodes to 0.
        - Create the start node with initial state, no parent, no action, cost 0,
          and heuristic based on Manhattan distance.
        - Create a priority queue frontier and add the start node to it.
        - Create a set to keep track of explored states.
        - Set the movement cost within the maze to 1 for each step, initializing the cost of the initial node accordingly.
        """

        
        # Initialize the number of explored nodes to 0
        self.num_explored = 0 

        # Create the start node with initial state, no parent, no action, cost 0, and heuristic based on Manhattan distance
        start = Node(state=self.start, parent=None, action=None, cost=0, heuristic=manhattan_distance(self.start, self.goal))

        # Create a priority queue frontier and add the start node to it
        frontier = PriorityQueueFrontier()
        frontier.add(start)
        
        # Create a set to keep track of explored states
        self.explored = set()

        # Continue the search loop until a solution is found or the frontier is empty
        while True:
            # If the frontier is empty and no solution is found, raise an exception
            if frontier.empty():
                raise Exception("no solution")
            
            # Remove a node from the frontier and Increment the count of explored nodes
            node = frontier.remove()
            self.num_explored += 1

            # If the current node's state is the goal, reconstruct the solution path and Exit the search loop if a solution is found
            if node.state == self.goal:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                actions.reverse()
                states.reverse()
                self.solution = (actions, states)
                return

            # Add the current node's state to the set of explored states
            self.explored.add(node.state)

            # Explore neighbors of the current node
            for action, state in self.neighbors(node.state):
                # Check if the neighbor is not in the frontier or explored set
                if not frontier.contains_state(state) and state not in self.explored:
                    # Assuming a uniform cost of 1 for each step

                    # Create a child node with updated information and add it to the frontier
                    child = Node(state=state, parent=node, action=action, cost=node.cost + 1, heuristic=manhattan_distance(state, self.goal))
                    frontier.add(child)

    def output_image(self, filename, show_solution=True, show_explored=True):
        """
        Generate an image representation of the maze with optional highlighting of solution path and explored states.

        Parameters:
        filename: Name of the output image file.
        show_solution: Flag to indicate whether to highlight the solution path (default True).
        show_explored: Flag to indicate whether to highlight explored states (default True).
        """
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python maze.py maze.txt")

    m = Maze(sys.argv[1])
    print("Maze:")
    m.print()
    print("Solving...")
    m.solve()
    print("States Explored:", m.num_explored)
    print("Solution:")
    m.print()
    m.output_image("maze.png", show_explored=True)
