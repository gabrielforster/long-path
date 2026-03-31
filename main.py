import sys


def parse_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    data = []
    for line in lines:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        data.append(stripped)

    idx = 0
    n = int(data[idx])
    idx += 1

    matrix = []
    for i in range(n):
        row = list(map(int, data[idx].split()))
        matrix.append(row)
        idx += 1

    source = int(data[idx])
    idx += 1
    dest = int(data[idx])
    idx += 1
    k = int(data[idx])
    idx += 1

    return n, matrix, source, dest, k


def find_longest_path(n, matrix, source, dest, k):
    if source == dest and k >= 1:
        return [source], 0

    if k < 2:
        return None, None

    best = [None, float("-inf")]

    def dfs(v, path, weight, remaining):
        if v == dest:
            if weight > best[1]:
                best[0] = list(path)
                best[1] = weight
            return

        if remaining <= 0:
            return

        for u in range(n):
            if matrix[v][u] != 0:
                path.append(u)
                dfs(u, path, weight + matrix[v][u], remaining - 1)
                path.pop()

    dfs(source, [source], 0, k - 1)

    if best[0] is None:
        return None, None
    return best[0], best[1]


def print_result(path, weight):
    if path is None:
        print("Não existe caminho válido.")
    else:
        print(f"Caminho máximo: {path}")
        print(f"Peso total: {weight}")
        print(f"Número de vértices no caminho: {len(path)}")


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"
    n, matrix, source, dest, k = parse_input(filename)
    path, weight = find_longest_path(n, matrix, source, dest, k)
    print_result(path, weight)
