import math

from prettytable import PrettyTable


def attack_probability(z: int, q: float):
    p = 1 - q
    lam = z * (q / p)

    def first_term(k: int):
        dividend = math.exp(-lam)
        for i in range(1, k + 1):
            dividend *= lam / i
        return dividend

    return 1 - sum(first_term(k) * (1 - (q / p) ** (z - k)) for k in range(0, z + 1))


def main():
    qs = [percent / 100 for percent in range(10, 46, 5)]
    probability_limits = [1e-3, 1e-4, 1e-5]
    probability_table = []

    for q in qs:
        probability_row = []
        for probability_limit in probability_limits:
            block = 1
            while True:
                probability = attack_probability(block, q)
                if probability < probability_limit:
                    probability_row.append(block)
                    break
                block += 1
        probability_table.append(probability_row)

    table = PrettyTable()
    table.field_names = ['q', *(f"probability limit = {pl}" for pl in probability_limits)]
    for q, probability_row in zip(qs, probability_table):
        table.add_row([q, *probability_row])
    print(table)


if __name__ == '__main__':
    main()
