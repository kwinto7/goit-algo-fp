import random
import matplotlib.pyplot as plt

# --- параметри ---
N = 1_000_00   # кількість симуляцій (чим більше, тим точніше)

# --- симуляція ---
counts = {s: 0 for s in range(2, 13)}
for _ in range(N):
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    s = d1 + d2
    counts[s] += 1

# --- обчислення ймовірностей ---
simulated_probs = {s: counts[s] / N for s in counts}

# --- аналітичні ймовірності ---
analytical_counts = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6,
                     8:5, 9:4, 10:3, 11:2, 12:1}
analytical_probs = {s: analytical_counts[s] / 36 for s in analytical_counts}

# --- вивід таблиці ---
print(f"{'Сума':<5}{'Монте-Карло (%)':<20}{'Аналітична (%)'}")
for s in range(2, 13):
    print(f"{s:<5}{simulated_probs[s]*100:<20.2f}{analytical_probs[s]*100:.2f}")

# --- графік ---
sums = list(range(2, 13))
sim_vals = [simulated_probs[s] for s in sums]
ana_vals = [analytical_probs[s] for s in sums]

plt.figure(figsize=(8,5))
plt.bar([s - 0.2 for s in sums], sim_vals, width=0.4, label="Монте-Карло")
plt.bar([s + 0.2 for s in sums], ana_vals, width=0.4, label="Аналітична")
plt.xticks(sums)
plt.ylabel("Імовірність")
plt.xlabel("Сума на кубиках")
plt.title(f"Ймовірності сум при {N:,} кидках двох кубиків")
plt.legend()
plt.show()
