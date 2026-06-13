#  grid.py  —  Smart Emergency Response Routing System

EMPTY    = "empty"
START    = "start"
END      = "end"
OBSTACLE = "obstacle"
TRAFFIC  = "traffic"

NORMAL_COST  = 1    # cost to enter a normal cell
TRAFFIC_COST = 5    # cost to enter a traffic (high-congestion) cell

class Node:

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

        self.cell_type: str = EMPTY
        self.cost: int      = NORMAL_COST

        self.parent:   "Node | None" = None
        self.g:        float         = float("inf")
        self.h:        float         = 0.0
        self.f:        float         = float("inf")
        self.visited:  bool          = False
        self.in_open:  bool          = False

    @property
    def is_obstacle(self) -> bool:
        return self.cell_type == OBSTACLE

    @property
    def is_traffic(self) -> bool:
        return self.cell_type == TRAFFIC

    @property
    def is_start(self) -> bool:
        return self.cell_type == START

    @property
    def is_end(self) -> bool:
        return self.cell_type == END

    @property
    def is_walkable(self) -> bool:
        """Any cell that is NOT an obstacle can be traversed."""
        return self.cell_type != OBSTACLE

    def set_type(self, cell_type: str) -> None:
        """Change the cell type and update the movement cost accordingly."""
        self.cell_type = cell_type
        self.cost = TRAFFIC_COST if cell_type == TRAFFIC else NORMAL_COST

    def reset_type(self) -> None:
        """Return cell to empty state."""
        self.set_type(EMPTY)

    def reset_search_state(self) -> None:
        """
        Called before every algorithm run.
        Clears all pathfinding data without touching cell type / cost.
        """
        self.parent  = None
        self.g       = float("inf")
        self.h       = 0.0
        self.f       = float("inf")
        self.visited = False
        self.in_open = False

    def __lt__(self, other: "Node") -> bool:
        """Primary: compare by f; tie-break by h (prefer nodes closer to goal)."""
        if self.f != other.f:
            return self.f < other.f
        return self.h < other.h

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def __repr__(self) -> str:
        return f"Node({self.row}, {self.col}, type={self.cell_type}, g={self.g}, h={self.h:.1f})"

class Grid:
    def __init__(self, rows: int = 25, cols: int = 25):
        self.rows = rows
        self.cols = cols

        self._nodes: list[list[Node]] = [
            [Node(r, c) for c in range(cols)]
            for r in range(rows)
        ]

        self.start_node: Node | None = None
        self.end_node:   Node | None = None

    def get_node(self, row: int, col: int) -> Node:
        """Return the Node at (row, col). Raises IndexError if out of bounds."""
        if not self.in_bounds(row, col):
            raise IndexError(f"({row}, {col}) is outside the grid ({self.rows}×{self.cols})")
        return self._nodes[row][col]

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def set_start(self, row: int, col: int) -> None:
        """
        Place the start (ambulance) node.
        Clears the previous start node first.
        """
        if self.start_node is not None:
            self.start_node.reset_type()

        node = self.get_node(row, col)
        if node.is_end:
            return

        node.set_type(START)
        self.start_node = node

    def set_end(self, row: int, col: int) -> None:
        """
        Place the end (hospital) node.
        Clears the previous end node first.
        """
        if self.end_node is not None:
            self.end_node.reset_type()

        node = self.get_node(row, col)
        if node.is_start:
            return

        node.set_type(END)
        self.end_node = node

    def set_obstacle(self, row: int, col: int) -> None:
        """Toggle an obstacle cell. Start / end cells cannot become obstacles."""
        node = self.get_node(row, col)
        if node.is_start or node.is_end:
            return
        if node.is_obstacle:
            node.reset_type()           
        else:
            node.set_type(OBSTACLE)     

    def set_traffic(self, row: int, col: int) -> None:
        node = self.get_node(row, col)
        if node.is_start or node.is_end or node.is_obstacle:
            return
        if node.is_traffic:
            node.reset_type()           
        else:
            node.set_type(TRAFFIC)      

    def get_neighbours(self, node: Node) -> list[Node]:
        """
        Return the up-to-4 walkable (non-obstacle) orthogonal neighbours
        of the given node (no diagonals — realistic road grid).
        """
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        neighbours: list[Node] = []

        for dr, dc in directions:
            nr, nc = node.row + dr, node.col + dc
            if self.in_bounds(nr, nc):
                neighbour = self._nodes[nr][nc]
                if neighbour.is_walkable:
                    neighbours.append(neighbour)

        return neighbours

    def reset_search_state(self) -> None:
        for row in self._nodes:
            for node in row:
                node.reset_search_state()

    def clear_path(self) -> None:
        self.reset_search_state()

    def reset_grid(self) -> None:
        for row in self._nodes:
            for node in row:
                node.reset_type()
                node.reset_search_state()

        self.start_node = None
        self.end_node   = None

    def is_ready(self) -> tuple[bool, str]:
        if self.start_node is None:
            return False, "No start node placed. Click a cell to set the ambulance position."
        if self.end_node is None:
            return False, "No end node placed. Click a cell to set the hospital position."
        return True, ""

    @staticmethod
    def reconstruct_path(end_node: Node) -> list[Node]:
        path: list[Node] = []
        current: Node | None = end_node

        while current is not None:
            path.append(current)
            current = current.parent

        path.reverse()

        if len(path) < 2:
            return []
        return path

    def all_nodes(self):
        
        for row in self._nodes:
            yield from row

    def __repr__(self) -> str:
        return f"Grid({self.rows}×{self.cols}, start={self.start_node}, end={self.end_node})"