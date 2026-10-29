"""Medições de tempo dos métodos de ordenação e do escolhedor.
Rodar da raiz do repositório: python testes/medir.py
"""
import os
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.algoritmos.insercao import insercao
from src.algoritmos.intercalacao import intercalacao
from src.algoritmos.rapido import rapido
from src.algoritmos.hibrido import hibrido
from src.algoritmos.contagem import contagem
from src.algoritmos.base import base
from src.seletor.escolhedor import escolher, ordenar

METODOS = [insercao, intercalacao, rapido, hibrido, contagem, base, ordenar]
LIMITE_MEMORIA_CONTAGEM = 50_000_000  # evita estourar a RAM ao testar contagem pura


def gerar_quase_ordenado(n, trocas=20):
    v = list(range(n))
    for _ in range(trocas):
        i = random.randint(0, n - 2)
        v[i], v[i + 1] = v[i + 1], v[i]
    return v


def gerar_cenario_erro(n):
    """Lista que engana o escolher: tem <= 1% de descidas (parece quase ordenada),
    mas os menores elementos estão todos no final, gerando O(n²) inversões na inserção."""
    k = int(n * 0.01)
    return list(range(k, n)) + list(range(k, 0, -1))


def medir_funcao(fn, entradas, repeticoes=5):
    """Mede a mediana do tempo (em ms) de fn sobre uma lista de entradas."""
    tempos = []
    for _ in range(repeticoes):
        t0 = time.perf_counter()
        for v in entradas:
            fn(v)
        t1 = time.perf_counter()
        tempos.append((t1 - t0) * 1000.0 / len(entradas))
    return statistics.median(tempos)


def main():
    random.seed(42)
    n = 10_000

    cenarios = {
        "Aleatório (chaves grandes)": (
            [[random.randint(0, 10**12) for _ in range(n)]],
            5,
        ),
        "Faixa estreita": (
            [[random.randint(0, 100) for _ in range(n)]],
            5,
        ),
        "Quase ordenado": (
            [gerar_quase_ordenado(n, trocas=25)],
            5,
        ),
        "Lista minúscula (n=12)": (
            [[random.randint(0, 1000) for _ in range(12)] for _ in range(500)],
            5,
        ),
    }

    print(f"=== Comparação nos 4 cenários (n = {n} nos três primeiros, n = 12 no último) ===\n")
    cabecalho = f"{'Cenário':<28} | " + " | ".join(f"{m.__name__:>12}" for m in METODOS) + " | escolhido"
    print(cabecalho)
    print("-" * len(cabecalho))

    for nome, (entradas, rep) in cenarios.items():
        amostra = entradas[0]
        escolhido = escolher(amostra).__name__
        celulas = []
        for m in METODOS:
            if m is contagem and amostra:
                faixa = max(amostra) - min(amostra) + 1
                if faixa > LIMITE_MEMORIA_CONTAGEM:
                    celulas.append(f"{'MemError':>12}")
                    continue
            # Inserção em lista grande aleatória é O(n²): 1 repetição basta
            r = 1 if (m is insercao and len(amostra) >= 5000 and escolhido != "insercao") else rep
            t_ms = medir_funcao(m, entradas, repeticoes=r)
            if t_ms < 0.1:
                celulas.append(f"{t_ms:>9.4f} ms")
            else:
                celulas.append(f"{t_ms:>9.2f} ms")
        print(f"{nome:<28} | " + " | ".join(celulas) + f" | {escolhido}")

    print("\n=== Custo isolado do escolher(v) vs ordenar(v) ===\n")
    print(f"{'Cenário':<28} | {'escolher(v)':>14} | {'ordenar(v)':>14} | {'fração do total':>15}")
    print("-" * 80)
    for nome, (entradas, rep) in cenarios.items():
        t_esc = medir_funcao(escolher, entradas, repeticoes=rep * 5)
        t_ord = medir_funcao(ordenar, entradas, repeticoes=rep)
        frac = (t_esc / t_ord) * 100 if t_ord > 0 else 0
        fmt_esc = f"{t_esc:.5f} ms" if t_esc < 0.01 else f"{t_esc:.3f} ms"
        fmt_ord = f"{t_ord:.4f} ms" if t_ord < 0.1 else f"{t_ord:.3f} ms"
        print(f"{nome:<28} | {fmt_esc:>14} | {fmt_ord:>14} | {frac:>14.1f}%")

    print("\n=== Cenário em que o escolher erra a decisão ===\n")
    v_erro = [gerar_cenario_erro(n)]
    esc_erro = escolher(v_erro[0]).__name__
    print(f"Entrada: list(range(100, {n})) + list(range(100, 0, -1))  (<= 1% de descidas, mas menores no fim)")
    print(f"Método escolhido por escolher(v): {esc_erro}")
    for m in METODOS:
        t_ms = medir_funcao(m, v_erro, repeticoes=3)
        print(f"  {m.__name__:<14}: {t_ms:>8.2f} ms")


if __name__ == "__main__":
    main()
