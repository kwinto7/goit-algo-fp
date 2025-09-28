import uuid
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# ---------- Базові класи/малювання (з твого коду) ----------
class Node:
    def __init__(self, key, color="#87CEEB"):  # skyblue як hex
        self.left = None
        self.right = None
        self.val = key
        self.color = color         # HEX-колір вузла
        self.id = str(uuid.uuid4())  # унікальний id

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {n: data["label"] for n, data in tree.nodes(data=True)}

    plt.clf()
    plt.figure(1, figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.tight_layout()
    plt.pause(0.001)

# ---------- Утиліти для кольорів ----------
def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def lerp(a, b, t):
    return int(a + (b - a) * t)

def gradient_hex(n: int, start_hex: str = "#10304C", end_hex: str = "#B8DBFF"):
    """
    Повертає n кольорів від темного до світлого (HEX).
    start_hex/end_hex — початковий/кінцевий кольори градієнта.
    """
    if n <= 0:
        return []
    if n == 1:
        return [start_hex]
    sr, sg, sb = hex_to_rgb(start_hex)
    er, eg, eb = hex_to_rgb(end_hex)
    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = lerp(sr, er, t)
        g = lerp(sg, eg, t)
        b = lerp(sb, eb, t)
        colors.append(rgb_to_hex((r, g, b)))
    return colors

# ---------- Обходи без рекурсії ----------
def bfs_order(root: Node):
    """Повертає список вузлів у порядку обходу BFS (черга)."""
    order = []
    q = deque([root])
    seen = set([root.id])
    while q:
        u = q.popleft()
        order.append(u)
        for v in (u.left, u.right):
            if v and v.id not in seen:
                seen.add(v.id)
                q.append(v)
    return order

def dfs_order(root: Node):
    """Повертає список вузлів у порядку ітеративного DFS (стек, pre-order)."""
    order = []
    stack = [root]
    seen = set([root.id])
    while stack:
        u = stack.pop()
        order.append(u)
        # щоб відвідувати спочатку ліву гілку, у стек кладемо спочатку праву
        for v in (u.right, u.left):
            if v and v.id not in seen:
                seen.add(v.id)
                stack.append(v)
    return order

# ---------- Візуалізація покроково ----------
def visualize_traversal(root: Node, mode: str = "bfs", pause: float = 0.6):
    """
    mode: 'bfs' або 'dfs'
    pause: затримка між кроками (сек)
    Кожен відвіданий вузол отримує унікальний HEX-колір від темного до світлого.
    """
    # зібрати порядок обходу
    order = bfs_order(root) if mode == "bfs" else dfs_order(root)

    # зробити градієнт кольорів
    palette = gradient_hex(len(order), start_hex="#10304C", end_hex="#B8DBFF")

    # спочатку зробимо всі вузли нейтральними (світло-сірими)
    def reset_colors(node):
        if not node:
            return
        node.color = "#D9D9D9"
        reset_colors(node.left)
        reset_colors(node.right)

    # рекурсивне скидання тільки для кольорів, не для обходу
    reset_colors(root)

    plt.ion()
    plt.figure(1)

    # покрокове фарбування
    for i, node in enumerate(order):
        node.color = palette[i]
        draw_tree(root)
        plt.title(f"{mode.upper()} крок {i+1}: відвідали вузол {node.val}", fontsize=12)
        plt.pause(pause)

    # фінальний кадр залишаємо на екрані
    plt.ioff()
    draw_tree(root)
    plt.title(f"Завершено {mode.upper()}", fontsize=12)
    plt.show()

# ---------- Демонстрація ----------
if __name__ == "__main__":
    # Приклад дерева
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # Візуалізація: BFS та DFS (ітеративно)
    visualize_traversal(root, mode="bfs", pause=0.7)
    visualize_traversal(root, mode="dfs", pause=0.7)
