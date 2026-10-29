# Relatório - Escolhedor de Algoritmo de Ordenação

**Dupla:** Matheus Martins Pagel e Daniel Bernardes Araújo

## 1. Comparação nos quatro cenários

Os tempos abaixo foram obtidos rodando `python testes/medir.py`, que calcula a mediana de 5 execuções com `time.perf_counter()` e semente fixa (`random.seed(42)`). Nos três primeiros cenários usamos listas de tamanho n = 10.000; no cenário de lista minúscula usamos n = 12 (tirando a média de 500 listas por repetição para reduzir o ruído da medição).

| Cenário | `insercao` | `intercalacao` | `rapido` | `hibrido` | `contagem` | `base` | `ordenar` | Escolha feita |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Aleatório com chaves grandes (n = 10.000, valores até 10^12) | 1435,71 ms | 14,40 ms | 14,45 ms | 11,88 ms | MemError* | 4,21 ms | 4,51 ms | `base` |
| Faixa estreita (n = 10.000, valores de 0 a 100) | 1239,93 ms | 12,97 ms | 4,82 ms | 4,55 ms | 0,44 ms | 1,04 ms | 0,54 ms | `contagem` |
| Quase ordenado (n = 10.000, 25 trocas de vizinhos) | 0,56 ms | 8,59 ms | 12,59 ms | 10,46 ms | 1,47 ms | 1,74 ms | 0,80 ms | `insercao` |
| Lista minúscula (n = 12, valores de 0 a 1000) | 0,0023 ms | 0,0064 ms | 0,0052 ms | 0,0023 ms | 0,0188 ms | 0,0282 ms | 0,0024 ms | `insercao` |

*\*No cenário de chaves grandes, a faixa de valores `k = maior - menor + 1` fica na casa de 10^12. A contagem tentaria alocar uma lista desse tamanho na memória (vários terabytes de RAM), dando `MemoryError`.*

Olhando para a tabela, dá para ver que nenhum método fixo ganha em todas as situações: a inserção é ótima quando a lista é minúscula ou quase ordenada, mas demora mais de 1 segundo nas listas aleatórias maiores; a contagem é a mais rápida na faixa estreita, mas estoura a memória quando as chaves são grandes; a ordenação por base vai muito bem nas chaves grandes, mas tem muito custo fixo nas listas pequenas (chegando a ser 12 vezes mais lenta que a inserção para n = 12). O `ordenar(v)` consegue escolher o método vencedor nos quatro cenários e fica com o tempo muito próximo do melhor de cada linha.

## 2. Qual venceu cada cenário e por quê

**Aleatório com chaves grandes (`base`, 4,21 ms):**
Nesse cenário a contagem não pode ser usada por causa do consumo de memória O(k). Entre os demais, a ordenação por base (implementada com Radix Sort LSD em base 256, separando 1 byte por vez) venceu porque números de até 10^12 cabem em 40 bits, exigindo apenas 5 passadas lineares sobre o vetor com operações bit a bit. Já os métodos por comparação (`intercalacao`, `rapido` e `hibrido`) têm complexidade O(n log n) e sofrem mais com o custo de recursão e comparações no Python, ficando entre 11,88 ms e 14,45 ms.

**Faixa estreita (`contagem`, 0,44 ms):**
Com valores entre 0 e 100, a faixa `k = 101` é muito menor que `n = 10.000`. A contagem aloca um vetor pequeno de 101 posições, conta as repetições em uma única passada O(n) e monta a saída. Vale notar que o `rapido` e o `hibrido` caíram de ~14 ms para ~4,6 ms nesse cenário porque usamos a partição em três vias (menores, iguais e maiores que o pivô), que agrupa todos os elementos repetidos de uma vez só, mas ainda assim a contagem linear é cerca de dez vezes mais rápida.

**Quase ordenado (`insercao`, 0,56 ms):**
O custo da ordenação por inserção é O(n + inversões). Como a lista foi gerada a partir de um vetor ordenado fazendo apenas 25 trocas entre vizinhos, quase todos os elementos já estão na posição certa e o `while` interno raramente roda. Assim ela percorre a lista praticamente uma única vez, ganhando até da contagem (1,47 ms) e da base (1,74 ms), que ainda precisam calcular `min` e `max` e criar listas auxiliares mesmo com a entrada quase pronta.

**Lista minúscula (`insercao`, 0,0023 ms):**
Para n = 12, a diferença teórica entre O(n²) e O(n log n) não aparece porque o tamanho é muito pequeno; o que pesa de verdade é o custo fixo de cada função. A inserção faz apenas dois laços simples sobre uma cópia da lista, sem recursão, sem sorteio de pivô (`random.randint`) e sem alocar baldes ou vetores de contagem. O `hibrido` (0,0023 ms) empata com ela justamente porque o corte interno dele (`LIMITE_INSERCAO = 16`) manda listas de tamanho 12 direto para a inserção sem particionar.

## 3. Regras do `escolher` e de onde vieram

A função `escolher(v)` em `src/seletor/escolhedor.py` testa três condições em sequência, da mais barata para a mais cara:

1. **Tamanho até 16 (`n <= 16` -> `insercao`):**
   Testamos vários tamanhos pequenos e vimos que até 16 elementos a inserção empata ou ganha da ordenação rápida por ter menos chamadas de função (o mesmo valor de corte foi usado no algoritmo híbrido). Como `len(v)` é O(1), essa verificação quase não tem custo.

2. **Proporção de descidas até 1% (`descidas <= 0.01 * n` -> `insercao`):**
   Para saber se a lista está quase ordenada sem gastar O(n log n) contando inversões, contamos quantas vezes um elemento é menor que o anterior (`v[i] < v[i-1]`). Se essa quantidade não passar de 1% do tamanho da lista, devolvemos `insercao`.
   Para atender ao aviso do enunciado e não percorrer a lista inteira à toa, o laço para com `break` assim que o número de descidas passa de 1%. Numa lista aleatória de 10.000 elementos, mais ou menos metade dos pares vizinhos estão fora de ordem, então o limite de 100 descidas estoura perto do elemento 200. Ou seja: em listas embaralhadas o laço olha apenas ~200 posições antes de parar, e só percorre tudo quando a lista realmente é quase ordenada (caso em que já retorna `insercao` direto, sem chamar `min` e `max`).

3. **Faixa de valores (`maior - menor + 1 <= 4 * n` -> `contagem`, senão `base`):**
   Se a lista não caiu nos casos anteriores, calculamos `min(v)` e `max(v)`. Usamos as funções nativas do Python porque elas são implementadas em C e rodam bem mais rápido do que um laço `for` escrito em Python para achar o menor e o maior juntos.
   Se a faixa `maior - menor + 1` for de no máximo `4 * n`, o gasto de memória da contagem continua O(n) e ela é mais rápida que os outros métodos, então devolvemos `contagem`. Acima de `4 * n`, descartamos a contagem (evitando lentidão e estouro de memória em chaves grandes) e devolvemos `base`, que ficou cerca de 3 vezes mais rápida que o `hibrido` e o `rapido` nos testes com inteiros.

## 4. Quanto custa rodar o `escolher` — ele compensa?

O script `testes/medir.py` também mede o tempo de chamar apenas `escolher(v)` separado do tempo total de `ordenar(v)`:

| Cenário | Tempo do `escolher(v)` | Tempo do `ordenar(v)` | Peso no tempo total |
| :--- | :---: | :---: | :---: |
| Aleatório com chaves grandes (n = 10.000) | 0,119 ms | 4,273 ms | 2,8% |
| Faixa estreita (n = 10.000) | 0,108 ms | 0,525 ms | 20,6% |
| Quase ordenado (n = 10.000) | 0,161 ms | 0,738 ms | 21,8% |
| Lista minúscula (n = 12) | 0,00004 ms | 0,0023 ms | 1,9% |

O custo do `escolher` compensa em todos os casos. Na lista minúscula, ele só olha o `len(v)` e gasta 0,00004 ms (menos de 2% do tempo). Nos cenários aleatório e de faixa estreita, o laço de descidas para logo no começo e o `min`/`max` gasta cerca de 0,11 ms; na faixa estreita isso dá ~20% do tempo total porque a contagem termina muito rápido (0,44 ms), mas o tempo final de ~0,54 ms ainda é quase a metade da `base` (1,04 ms) e oito vezes menor que o `hibrido` (4,55 ms). No quase ordenado, percorrer a lista no `escolher` custa 0,16 ms, mas economiza mais de 9 ms em comparação com o `hibrido` ou o `rapido`.

## 5. Um cenário em que o `escolher` erra a decisão

O ponto fraco do `escolher` está na regra de quase ordenado: contar apenas pares vizinhos fora de ordem (`v[i] < v[i-1]`) não mostra a distância que os elementos vão precisar andar. Uma lista pode ter pouquíssimas descidas e mesmo assim ter O(n²) inversões.

Um exemplo simples para n = 10.000 é colocar os números de 100 até 9.999 em ordem crescente e deixar os 100 menores números no final da lista, em ordem decrescente:

```python
v = list(range(100, 10_000)) + list(range(100, 0, -1))
```

Nessa lista existem exatamente 100 descidas (1% de n), todas concentradas na ponta final. Como não passa do limite de 1%, o `escolher(v)` acha que a lista está quase ordenada e escolhe `insercao`. O problema é que, para ordenar, cada um desses 100 menores elementos que estão no fim precisa voltar até o início da lista, atravessando todos os 9.900 elementos maiores (quase 1 milhão de trocas no `while` interno).

Medindo essa entrada no `testes/medir.py`:

- Escolha do `escolher(v)`: `insercao`, demorando **49,27 ms**.
- Se tivesse escolhido `contagem`: demoraria **1,43 ms** (cerca de 34 vezes mais rápido).
- Se tivesse escolhido `base`: demoraria **2,05 ms**.
- Mesmo `intercalacao` (8,50 ms), `hibrido` (10,13 ms) e `rapido` (12,32 ms) seriam de 4 a 6 vezes mais rápidos que a escolha feita.

*(Obs.: o mesmo erro acontece até com uma única descida se a lista for rotacionada, como `list(range(100, 10_000)) + list(range(100))`, porque os 100 menores valores continuam no final tendo que atravessar a lista inteira na inserção.)*
