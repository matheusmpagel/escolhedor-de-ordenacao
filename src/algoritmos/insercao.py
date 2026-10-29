def insercao(v):
    """Ordenação por inserção. O(n²) no pior caso, O(n + inversões) em geral."""
    v = list(v)
    for i in range(1, len(v)):
        x = v[i]
        j = i - 1
        while j >= 0 and v[j] > x:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = x
    return v
