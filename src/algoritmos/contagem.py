def contagem(v):
    """Counting sort para inteiros. O(n + k), k = maior - menor + 1.
    Aloca k posições: só use com faixa pequena (o escolhedor checa isso)."""
    if not v:
        return []
    menor, maior = min(v), max(v)
    cont = [0] * (maior - menor + 1)
    for x in v:
        cont[x - menor] += 1
    saida = []
    for i, c in enumerate(cont):
        if c:
            saida.extend([i + menor] * c)
    return saida
