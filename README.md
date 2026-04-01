# Explicacao do Codigo - Caminho Mais Longo em Grafo

Este programa encontra o **caminho mais longo** (de maior peso) entre dois vertices de um grafo representado por matriz de adjacencia, com um limite maximo de vertices no caminho.

## Estrutura Geral

O programa e dividido em tres funcoes principais:

1. `parse_input` - Leitura e parsing do arquivo de entrada
2. `find_longest_path` - Algoritmo de busca do caminho mais longo
3. `print_result` - Exibicao do resultado

---

## 1. Leitura da Entrada (`parse_input`)

```python
def parse_input(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    data = []
    for line in lines:
        stripped = line.strip()
        if stripped == "" or stripped.startswith("#"):
            continue
        data.append(stripped)
```

Essa parte le o arquivo e filtra linhas vazias e comentarios (linhas que comecam com `#`), armazenando apenas as linhas uteis na lista `data`.

```python
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
```

O parsing segue esta ordem:

| Variavel | Descricao |
|----------|-----------|
| `n` | Numero de vertices do grafo |
| `matrix` | Matriz de adjacencia `n x n` (peso das arestas) |
| `source` | Vertice de origem |
| `dest` | Vertice de destino |
| `k` | Numero maximo de vertices permitidos no caminho |

---

## 2. Busca do Caminho Mais Longo (`find_longest_path`)

### Casos base

```python
def find_longest_path(n, matrix, source, dest, k):
    if source == dest and k >= 1:
        return [source], 0

    if k < 2:
        return None, None
```

- Se a origem e o destino sao o mesmo vertice e `k >= 1`, o caminho e trivial (peso 0).
- Se `k < 2`, nao e possivel formar um caminho entre dois vertices distintos.

### Busca em profundidade (DFS)

```python
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
```

O algoritmo utiliza **busca em profundidade com backtracking**:

- `best` armazena o melhor caminho encontrado ate o momento e seu peso total.
- A funcao `dfs` explora recursivamente todos os vizinhos do vertice atual `v`.
- `matrix[v][u] != 0` indica que existe uma aresta de `v` para `u`.
- `remaining` controla quantas arestas ainda podem ser percorridas (limitado por `k`).
- `path.pop()` desfaz a escolha anterior (backtracking), permitindo explorar outros caminhos.

```python
    dfs(source, [source], 0, k - 1)
```

A chamada inicial parte do vertice `source`, com peso 0 e `k - 1` arestas restantes (pois `k` e o limite de **vertices**, e o primeiro vertice ja esta no caminho).

---

## 3. Exibicao do Resultado (`print_result`)

```python
def print_result(path, weight):
    if path is None:
        print("Nao existe caminho valido.")
    else:
        print(f"Caminho maximo: {path}")
        print(f"Peso total: {weight}")
        print(f"Numero de vertices no caminho: {len(path)}")
```

Exibe o caminho encontrado, o peso total e a quantidade de vertices. Caso nao exista caminho valido, informa ao usuario.

---

## 4. Ponto de Entrada

```python
if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"
    n, matrix, source, dest, k = parse_input(filename)
    path, weight = find_longest_path(n, matrix, source, dest, k)
    print_result(path, weight)
```

O programa pode receber o nome do arquivo de entrada como argumento de linha de comando. Caso nenhum argumento seja passado, utiliza `entrada.txt` como padrao.

### Exemplo de uso

```bash
python main.py entrada.txt
```

---

## Complexidade

O algoritmo explora todos os caminhos possiveis com ate `k` vertices usando DFS com backtracking. No pior caso, a complexidade e **O(n^k)**, onde `n` e o numero de vertices e `k` o limite de vertices no caminho. Isso torna o algoritmo adequado para grafos pequenos.
