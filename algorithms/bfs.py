# BFS — explores layer by layer, optimal only without weights

from collections import deque
from grid import Grid, Node


def bfs(grid: Grid) -> tuple[list[Node], list[Node]]:

    ready, msg = grid.is_ready()
    if not ready:
        raise RuntimeError(f"BFS: {msg}")

    grid.reset_search_state()

    start: Node = grid.start_node
    end:   Node = grid.end_node

    queue: deque[Node] = deque()
    start.in_open = True
    start.g = 0
    queue.append(start)

    visited_order: list[Node] = []   # animation order

    while queue:
        current: Node = queue.popleft()

        if current.visited:
            continue

        current.visited = True
        visited_order.append(current)

        if current == end:
            path = Grid.reconstruct_path(end)
            return path, visited_order

        for neighbour in grid.get_neighbours(current):
            if not neighbour.visited and not neighbour.in_open:
                neighbour.parent  = current
                neighbour.g       = current.g + 1   # BFS: hop count only
                neighbour.in_open = True
                queue.append(neighbour)

    return [], visited_order