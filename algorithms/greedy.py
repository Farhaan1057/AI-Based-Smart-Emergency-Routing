# Greedy BFS — uses only h(n), fast but can miss optimal path due to ignoring actual cost

import heapq
from grid import Grid, Node
from utils import manhattan_distance


def greedy(grid: Grid) -> tuple[list[Node], list[Node]]:
   
    ready, msg = grid.is_ready()
    if not ready:
        raise RuntimeError(f"Greedy BFS: {msg}")

    grid.reset_search_state()

    start: Node = grid.start_node
    end:   Node = grid.end_node

    counter: int = 0
    open_heap: list = []

    start.h       = manhattan_distance(start, end)
    start.f       = start.h     
    start.g       = 0
    start.in_open = True

    heapq.heappush(open_heap, (start.h, counter, start))

    visited_order: list[Node] = []

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current.visited:
            continue

        current.visited = True
        visited_order.append(current)

        if current == end:
            path = Grid.reconstruct_path(end)
            return path, visited_order

        for neighbour in grid.get_neighbours(current):
            if neighbour.visited:
                continue

            tentative_g = current.g + neighbour.cost
            h = manhattan_distance(neighbour, end)

            if not neighbour.in_open or tentative_g < neighbour.g:
                neighbour.parent  = current
                neighbour.g       = tentative_g
                neighbour.h       = h
                neighbour.f       = h          
                neighbour.in_open = True

                counter += 1
                heapq.heappush(open_heap, (neighbour.h, counter, neighbour))

    return [], visited_order