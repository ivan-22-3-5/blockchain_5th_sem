import math


def find_p_h_with_d(p_h: float, a_m: float, d_h: int) -> float:
    return math.exp(-a_m * d_h) * p_h


def pr(z, k, p_h, a, a_m, d_h):
    first_multiplier = (p_h ** z) / math.factorial(z - 1)
    second_multiplier = math.exp(-a_m * z * d_h) * ((a_m * z * d_h) ** k) / math.factorial(k)
    third_multiplier = sum(math.factorial(z - i + 1) * math.comb(k, i) / (a * z * d_h) ** i for i in range(0, k + 1))
    return first_multiplier * second_multiplier * third_multiplier


def pz(z, p_h, a, a_m, d_h):
    p_h_with_d = find_p_h_with_d(p_h, a_m, d_h)
    p_m_with_d = 1 - p_h_with_d
    if p_m_with_d >= p_h_with_d:
        return 1
    return 1 - sum(pr(z, k, p_h, a, a_m, d_h) * (1 - (p_m_with_d / p_h_with_d) ** (z - k)) for k in range(0, z))


def main():
    ...


if __name__ == '__main__':
    main()
