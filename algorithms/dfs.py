from grid import Grid, Node

def dfs(grid: Grid) -> tuple[list[Node], list[Node]]:
    ready, msg = grid.is_ready()
    if not ready:
        raise RuntimeError(f"DFS: {msg}")

    grid.reset_search_state()

    start: Node = grid.start_node
    end:   Node = grid.end_node

    stack: list[Node] = [start]
    start.in_open = True

    visited_order: list[Node] = []

    while stack:
        current: Node = stack.pop()

        if current.visited:
            continue

        current.visited = True
        visited_order.append(current)

        if current == end:
            return Grid.reconstruct_path(end), visited_order

        for neighbour in reversed(grid.get_neighbours(current)):
            if not neighbour.visited and not neighbour.in_open:
                neighbour.parent  = current
                neighbour.in_open = True
                stack.append(neighbour)

    return [], visited_order