from grid import Node


def manhattan_distance(a: Node, b: Node) -> float:
    return abs(a.row - b.row) + abs(a.col - b.col)


def format_time(seconds: float) -> str:
    return f"{seconds * 1000:.2f} ms"


def format_stats(
    algorithm_name: str,
    path:           list,
    visited_order:  list,
    elapsed:        float,
) -> dict:
   
    path_cost = sum(node.cost for node in path) if path else 0

    return {
        "algorithm":      algorithm_name,
        "path_found":     len(path) > 0,
        "path_length":    len(path),
        "path_cost":      path_cost,
        "nodes_explored": len(visited_order),
        "time":           format_time(elapsed),
    }