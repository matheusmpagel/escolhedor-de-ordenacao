from src.algoritmos.rapido import _particionar

# Abaixo disso a inserção ganha do quicksort (menos overhead por elemento).
LIMITE_INSERCAO = 16


def _insercao_trecho(v, ini, fim):
    for i in range(ini + 1, fim + 1):
        x = v[i]
        j = i - 1
        while j >= ini and v[j] > x:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = x


def _hibrido(v, ini, fim):
    while fim - ini + 1 > LIMITE_INSERCAO:
        lt, gt = _particionar(v, ini, fim)
        if lt - ini < fim - gt:
            _hibrido(v, ini, lt - 1)
            ini = gt + 1
        else:
            _hibrido(v, gt + 1, fim)
            fim = lt - 1
    _insercao_trecho(v, ini, fim)


def hibrido(v):
    """Quicksort com pivô aleatório que passa para inserção nos trechos pequenos."""
    v = list(v)
    _hibrido(v, 0, len(v) - 1)
    return v
