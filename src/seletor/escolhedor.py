from src.algoritmos.insercao import insercao
from src.algoritmos.contagem import contagem
from src.algoritmos.base import base

# Regras calibradas com medições (ver RELATORIO.md). Ajuste aqui se refizer as medições.
LIMITE_PEQUENO = 16      # até esse tamanho a inserção empata ou ganha de todos
TOLERANCIA_DESCIDAS = 0.01  # até 1% de pares fora de ordem = "quase ordenado"
FATOR_FAIXA = 4          # contagem só se a faixa de valores <= 4 * n (memória O(n))


def escolher(v):
    """Olha a lista e devolve a função de ordenação mais adequada (só inteiros)."""
    n = len(v)
    if n <= LIMITE_PEQUENO:
        return insercao

    # Conta "descidas" (v[i] > v[i+1]) e para assim que passar da tolerância:
    # numa lista aleatória isso acontece em poucas dezenas de elementos,
    # então o laço só percorre tudo quando a lista é de fato quase ordenada.
    limite = int(n * TOLERANCIA_DESCIDAS)
    descidas = 0
    anterior = v[0]
    for x in v:
        if x < anterior:
            descidas += 1
            if descidas > limite:
                break
        anterior = x
    else:
        return insercao

    # min/max são embutidos em C: muito mais baratos que um laço em Python.
    menor, maior = min(v), max(v)
    if maior - menor + 1 <= FATOR_FAIXA * n:
        return contagem
    # Chaves grandes: no Python a base (radix) ficou ~3x mais rápida que rápida/híbrida.
    return base


def ordenar(v):
    return escolher(v)(v)
