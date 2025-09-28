import uuid
import networkx as nx
import matplotlib.pyplot as plt

# ====== базові класи/функції з твого прикладу ======
class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

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
    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.show()

# ====== НОВЕ: побудова дерева з бінарної купи ======
def heap_to_tree(heap, kind="min", highlight_violations=True):
    """
    heap : список значень (масив купи)
    kind : 'min' або 'max' — тип купи (використовується для підсвічування порушень)
    """
    if not heap:
        raise ValueError("Порожня купа")

    # створюємо вузол для кожного елемента
    nodes = [Node(v) for v in heap]

    # з'єднуємо дітей за індексами: left=2i+1, right=2i+2
    n = len(heap)
    for i in range(n):
        li, ri = 2*i + 1, 2*i + 2
        if li < n:
            nodes[i].left = nodes[li]
        if ri < n:
            nodes[i].right = nodes[ri]

        # (опційно) підсвічуємо порушення властивості купи
        if highlight_violations:
            if li < n:
                bad = heap[li] < heap[i] if kind == "min" else heap[li] > heap[i]
                if bad:
                    nodes[li].color = "#d9534f"   # червоний
            if ri < n:
                bad = heap[ri] < heap[i] if kind == "min" else heap[ri] > heap[i]
                if bad:
                    nodes[ri].color = "#d9534f"

    return nodes[0]  # корінь дерева

def draw_heap(heap, kind="min"):
    """Зручний обгортник: одразу будує дерево з купи та малює."""
    root = heap_to_tree(heap, kind=kind)
    draw_tree(root)

# ====== приклад використання ======
if __name__ == "__main__":
    # мін-купа у масивному представленні
    min_heap = [1, 3, 5, 7, 9, 6, 8, 10, 12, 15]
    draw_heap(min_heap, kind="min")

