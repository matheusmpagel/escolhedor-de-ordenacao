"""Testes de correção. Rodar da raiz do repositório: python testes/teste.py"""
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.algoritmos.insercao import insercao
from src.algoritmos.intercalacao import intercalacao
from src.algoritmos.rapido import rapido
from src.algoritmos.hibrido import hibrido
from src.algoritmos.contagem import contagem
from src.algoritmos.base import base
from src.seletor.escolhedor import escolher, ordenar

METODOS = [insercao, intercalacao, rapido, hibrido, contagem, base, ordenar]

CASOS = {
    "vazia": [],
    "um elemento": [7],
    "todos iguais": [5] * 100,
    "já ordenada": list(range(100)),
    "invertida": list(range(100, 0, -1)),
    "negativos": [-3, 10, -50, 0, 7, -1, -50, 2],
    "aleatória": [random.randint(-1000, 1000) for _ in range(500)],
}


def testar_correcao():
    for nome, caso in CASOS.items():
        esperado = sorted(caso)
        for metodo in METODOS:
            copia = list(caso)
            assert metodo(caso) == esperado, f"{metodo.__name__} falhou em: {nome}"
            assert caso == copia, f"{metodo.__name__} alterou a entrada em: {nome}"


def testar_escolhas():
    n = 10_000
    assert escolher([3, 1, 2]) is insercao
    assert escolher(list(range(n))) is insercao
    assert escolher([random.randint(0, 100) for _ in range(n)]) is contagem
    # Faixa gigante: a contagem alocaria 10^12 posições; o escolhedor não pode chamá-la.
    assert escolher([random.randint(0, 10**12) for _ in range(n)]) is base


if __name__ == "__main__":
    testar_correcao()
    testar_escolhas()
    print("ok")
