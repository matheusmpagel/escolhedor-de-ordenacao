# Escolhedor de Algoritmo de Ordenação

Trabalho da disciplina de **Estruturas Avançadas**.

**Dupla:** Matheus Martins Pagel e Daniel Bernardes Araújo

## Organização do projeto

- `src/algoritmos/`: implementação dos seis métodos vistos no semestre (`insercao.py`, `intercalacao.py`, `rapido.py`, `hibrido.py`, `contagem.py` e `base.py`).
- `src/seletor/escolhedor.py`: funções `escolher(v)` e `ordenar(v)`.
- `testes/teste.py`: testes de correção (lista vazia, um elemento, todos iguais, ordenada, invertida, negativos e aleatória) e verificação das decisões do escolhedor.
- `testes/medir.py`: script que mede os tempos nos quatro cenários, o custo isolado do `escolher` e o cenário em que a heurística falha.
- `RELATORIO.md`: resultados obtidos e discussão das perguntas do trabalho.

## Como rodar os testes e refazer as medições

O código usa apenas a biblioteca padrão do Python 3. Todos os comandos abaixo devem ser rodados a partir da raiz do repositório.

Para rodar os testes de correção:

```bash
python testes/teste.py
```

Para refazer as medições de tempo apresentadas no `RELATORIO.md`:

```bash
python testes/medir.py
```

O script `testes/medir.py` usa semente fixa (`random.seed(42)`) e `time.perf_counter()`, tirando a mediana de 5 execuções em cada cenário. Caso os tempos mudem em outra máquina e seja necessário recalibrar os cortes do seletor, as constantes ficam no topo de `src/seletor/escolhedor.py` (`LIMITE_PEQUENO`, `TOLERANCIA_DESCIDAS` e `FATOR_FAIXA`).
