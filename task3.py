import heapq
from typing import Dict, List, Tuple, Any, Optional

Graph = Dict[Any, List[Tuple[Any, float]]]

def dijkstra(graph: Graph, source: Any) -> Tuple[Dict[Any, float], Dict[Any, Optional[Any]]]:
    """
    Повертає:
      dist[v]  — мінімальна відстань від source до v
      parent[v] — попередник v у найкоротшому шляху (для відновлення шляху)
    Умови: всі ваги ребер невід’ємні.
    """
    # 1) ініціалізація
    dist = {v: float('inf') for v in graph}
    dist[source] = 0.0
    parent: Dict[Any, Optional[Any]] = {v: None for v in graph}

    # 2) бінарна купа з пар (відстань, вершина)
    pq: List[Tuple[float, Any]] = [(0.0, source)]

    # 3) основний цикл
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            # «прострочений» запис; пропускаємо (classic lazy deletion)
            continue

        # релаксація ребер u → v
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                heapq.heappush(pq, (nd, v))

    return dist, parent


def reconstruct_path(parent: Dict[Any, Optional[Any]], target: Any) -> List[Any]:
    """Відновлює шлях до target за масивом попередників."""
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    return path[::-1]

if __name__ == "__main__":
    # Створимо зважений неорієнтований граф
    G: Graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
        'D': [('B', 5), ('C', 8), ('E', 2), ('F', 6)],
        'E': [('C', 10), ('D', 2), ('F', 2)],
        'F': [('D', 6), ('E', 2)]
    }

    src = 'A'
    dist, parent = dijkstra(G, src)

    print("Мінімальні відстані від", src)
    for v in sorted(G):
        print(f"  {v}: {dist[v]}")

    print("\nНайкоротні шляхи:")
    for v in sorted(G):
        print(f"  {src} → {v}: {reconstruct_path(parent, v)}")
