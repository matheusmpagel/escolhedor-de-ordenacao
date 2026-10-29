def intercalacao(v):
    """Merge sort (intercalação). O(n log n) sempre, O(n) de memória extra."""
    if len(v) <= 1:
        return list(v)
    meio = len(v) // 2
    esq = intercalacao(v[:meio])
    dir = intercalacao(v[meio:])
    saida = []
    i = j = 0
    while i < len(esq) and j < len(dir):
        if esq[i] <= dir[j]:
            saida.append(esq[i])
            i += 1
        else:
            saida.append(dir[j])
            j += 1
    saida.extend(esq[i:])
    saida.extend(dir[j:])
    return saida
