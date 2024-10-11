import math

from prettytable import PrettyTable


def find_p_h_with_d(p_h: float, a_m: float, d_h: int) -> float:
    return math.exp(-a_m * d_h) * p_h


def pr(z: int, k: int, p_h: float, a: float, a_m: float, d_h: int):
    first_multiplier = (p_h ** z) / math.factorial(z - 1)
    second_multiplier = math.exp(-a_m * z * d_h) * ((a_m * z * d_h) ** k) / math.factorial(k)
    third_multiplier = sum(math.factorial(z - i + 1) * math.comb(k, i) / (a * z * d_h) ** i for i in range(0, k + 1))
    return first_multiplier * second_multiplier * third_multiplier


def pz(z: int, p_h: float, a: float, a_m: float, d_h: int):
    p_h_with_d = find_p_h_with_d(p_h, a_m, d_h)
    p_m_with_d = 1 - p_h_with_d
    if p_m_with_d >= p_h_with_d:
        return 1
    return 1 - sum(pr(z, k, p_h, a, a_m, d_h) * (1 - (p_m_with_d / p_h_with_d) ** (z - k)) for k in range(0, z))


def main():
    a = 0.00167
    p_ms = [percent / 100 for percent in range(10, 41, 5)]
    p_hs = [1 - p for p in p_ms]
    d_hs = [15, 30, 60, 120, 180]
    probability_table = []
    for p_h in p_hs:
        probability_row = []
        a_m = a * (1 - p_h)
        for d_h in d_hs:
            block = 1
            while True:
                probability = pz(block, p_h, a, a_m, d_h)
                if probability < 0.0001:
                    break
                block += 1
            probability_row.append(block)
        probability_table.append(probability_row)

    table = PrettyTable()
    table.field_names = ['Ph', *(f"Dh = {d_h}" for d_h in d_hs)]
    for p_m, probability_row in zip(p_ms, probability_table):
        table.add_row([p_m, *probability_row])
    print(table)


if __name__ == '__main__':
    main()
