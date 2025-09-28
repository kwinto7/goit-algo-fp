import matplotlib.pyplot as plt
import numpy as np

def draw_tree(ax, x, y, length, angle, depth, max_depth):
    """Рекурсивне малювання дерева Піфагора"""
    if depth > max_depth:
        return

    # координати верхньої точки квадрата (стовбур дерева)
    x2 = x + length * np.cos(angle)
    y2 = y + length * np.sin(angle)

    # малюємо лінію (гілку)
    ax.plot([x, x2], [y, y2], color="brown", lw=1)

    # рекурсія для двох гілок
    new_length = length * 0.7
    draw_tree(ax, x2, y2, new_length, angle + np.pi/4, depth + 1, max_depth)
    draw_tree(ax, x2, y2, new_length, angle - np.pi/4, depth + 1, max_depth)


def pythagoras_tree(depth=7):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    draw_tree(ax, 0, -1, 1, np.pi/2, 1, depth)
    plt.show()


if __name__ == "__main__":
    pythagoras_tree(depth=8)  