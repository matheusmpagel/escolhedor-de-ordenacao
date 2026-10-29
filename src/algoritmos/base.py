BITS = 8
BALDES = 1 << BITS  # base 256: cada passada ordena um byte da chave


def base(v):
    """Radix sort LSD para inteiros, base 256. O(n * d), d = bytes da maior chave.
    Negativos: desloca tudo pelo menor valor, ordena e desfaz o deslocamento."""
    if len(v) <= 1:
        return list(v)
    menor = min(v)
    v = [x - menor for x in v]
    maior = max(v)
    desloc = 0
    while maior >> desloc:
        baldes = [[] for _ in range(BALDES)]
        for x in v:
            baldes[(x >> desloc) & (BALDES - 1)].append(x)
        v = [x for b in baldes for x in b]
        desloc += BITS
    return [x + menor for x in v]
