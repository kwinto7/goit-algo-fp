from typing import Dict, List, Tuple

items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}

def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний підхід: беремо страви у порядку спадання (calories/cost),
    поки не вичерпано бюджет. НЕ гарантує оптимум (для 0/1 задачі).
    Повертає: (список_страв, сум_калорій, сум_вартості)
    """
    # формуємо список (name, cost, cal, ratio)
    rows = []
    for name, v in items.items():
        cost, cal = v["cost"], v["calories"]
        if cost <= 0:  # безпечний захист від ділення на 0/некоректних даних
            continue
        rows.append((name, cost, cal, cal / cost))

    # сортуємо за ratio ↓, при рівності — за калорійністю ↓, потім за меншою ціною ↑
    rows.sort(key=lambda t: (t[3], t[2], -t[1]), reverse=True)

    chosen, total_cal, total_cost = [], 0, 0
    for name, cost, cal, _ in rows:
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost
            total_cal += cal

    return chosen, total_cal, total_cost


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    0/1 рюкзак (оптимальний): максимізує калорійність при обмеженні бюджету.
    DP по вартості: O(n * budget) пам'ять і час.
    Повертає: (список_страв, сум_калорій, сум_вартості)
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals  = [items[n]["calories"] for n in names]
    n = len(names)

    # DP-таблиця: dp[w] = макс. калорій при бюджеті w (1D оптимізація)
    dp = [0] * (budget + 1)
    # Для відновлення вибору — зберігаємо, чи брали елемент на кроці i для ваги w
    take = [[False]*(budget + 1) for _ in range(n)]

    for i in range(n):
        cost_i, cal_i = costs[i], cals[i]
        # ідемо w від великого до малого (щоб кожен предмет використати не більше 1 разу)
        for w in range(budget, cost_i - 1, -1):
            if dp[w - cost_i] + cal_i > dp[w]:
                dp[w] = dp[w - cost_i] + cal_i
                take[i][w] = True

    # відновлення набору
    w = budget
    chosen_idx: List[int] = []
    for i in range(n - 1, -1, -1):
        if take[i][w]:
            chosen_idx.append(i)
            w -= costs[i]

    chosen_idx.reverse()
    chosen_names = [names[i] for i in chosen_idx]
    total_cal = sum(cals[i] for i in chosen_idx)
    total_cost = sum(costs[i] for i in chosen_idx)
    return chosen_names, total_cal, total_cost


if __name__ == "__main__":
    BUDGET =100

    g_items, g_cal, g_cost = greedy_algorithm(items, BUDGET)
    d_items, d_cal, d_cost = dynamic_programming(items, BUDGET)

    print("Бюджет:", BUDGET)
    print("\nЖАДІБНИЙ:")
    print("  sвибір:", g_items)
    print("  калорій:", g_cal, "  вартість:", g_cost)

    print("\nДИНАМІЧНЕ ПРОГРАМУВАННЯ (ОПТИМАЛЬНЕ):")
    print("  вибір:", d_items)
    print("  калорій:", d_cal, "  вартість:", d_cost)
