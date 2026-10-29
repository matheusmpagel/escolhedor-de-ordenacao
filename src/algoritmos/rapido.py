import random


def _particionar(v, ini, fim):
    """Partição em três (< pivô, == pivô, > pivô) com pivô aleatório.
    Devolve (lt, gt): v[lt:gt+1] fica todo igual ao pivô."""
    pivo = v[random.randint(ini, fim)]
    lt, i, gt = ini, ini, fim
    while i <= gt:
        if v[i] < pivo:
            v[lt], v[i] = v[i], v[lt]
            lt += 1
            i += 1
        elif v[i] > pivo:
            v[i], v[gt] = v[gt], v[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _rapido(v, ini, fim):
    # Recursão só no lado menor e laço no maior: profundidade O(log n) garantida.
    # A partição em três evita O(n²) quando há muitas chaves repetidas.
    while ini < fim:
        lt, gt = _particionar(v, ini, fim)
        if lt - ini < fim - gt:
            _rapido(v, ini, lt - 1)
            ini = gt + 1
        else:
            _rapido(v, gt + 1, fim)
            fim = lt - 1


def rapido(v):
    """Quicksort com pivô aleatório. O(n log n) esperado."""
    v = list(v)
    _rapido(v, 0, len(v) - 1)
    return v
